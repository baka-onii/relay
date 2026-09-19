"""Provider-independent reasoning contract plus a stdlib OpenAI-compatible client."""

from __future__ import annotations

import http.client
import json
import urllib.error
import urllib.request
from collections.abc import Callable, Iterator
from typing import Any, Protocol

from relay.config import AgentConfig, normalize_model_url
from relay.models.streaming import (
    GenerationCancelled,
    IncompleteGeneration,
    ModelDelta,
    check_cancelled,
    check_finish,
    decode_packet,
    response_deltas,
    sse_payloads,
    streaming_transport,
    usage_counts,
)
from relay.tools.base import Tool
from relay.tools.filesystem import workspace_description

MAX_RESPONSE_BYTES = 2_000_000


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never forward a provider's Authorization header to a redirected host.
        return None


class ReasoningModel(Protocol):
    def generate(self, messages: list[dict[str, Any]]) -> str:
        """Return text in the <tool>/<final> protocol, never a structured tool call."""
        ...


class StreamingReasoningModel(Protocol):
    def stream(
        self,
        messages: list[dict[str, Any]],
        *,
        cancelled: Callable[[], bool] | None = None,
    ) -> Iterator[ModelDelta | str]:
        """Optional streaming contract. Only returned content can be executable intent."""
        ...


def build_system_prompt(tools: list[Tool], config: AgentConfig | None = None) -> str:
    config = config or AgentConfig()
    descriptions = "\n".join(tool.reasoning_description() for tool in tools)
    return (
        config.reasoning_prompt.rstrip()
        + "\n\nRuntime workspace context:\n"
        + workspace_description(config)
        + "\n\nAvailable tools (generated from the canonical registry):\n"
        + descriptions
    )


def build_translator_prompt(config: AgentConfig) -> str:
    return (
        config.translator_prompt.rstrip()
        + "\n\nRuntime workspace context:\n"
        + workspace_description(config)
    )


def api_base_url(base_url: str) -> str:
    base = normalize_model_url(base_url)
    lowered = base.lower()
    # Google AI Studio's OpenAI-compatible base ends at .../v1beta/openai
    # (which already plays the role of "/v1"). Appending another "/v1"
    # produces .../openai/v1, which is wrong per docs even though Google
    # currently tolerates it. Treat it as complete, like a trailing /v1.
    if lowered.endswith("/v1") or lowered.endswith("/openai"):
        return base
    return base + "/v1"


ANTHROPIC_VERSION = "2023-06-01"


def anthropic_base_url(base_url: str) -> str:
    """Anthropic native base; the Messages API lives under /v1/messages."""
    base = normalize_model_url(base_url)
    return base if base.lower().endswith("/v1") else base + "/v1"


def _anthropic_headers(api_key: str | None) -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Anthropic-Version": ANTHROPIC_VERSION,
    }
    if api_key:
        headers["X-Api-Key"] = api_key
    return headers


def _split_anthropic_messages(
    messages: list[dict[str, Any]],
) -> tuple[str, list[dict[str, str]]]:
    """System text goes to `system`; the rest become alternating user/assistant turns.

    The runtime transcript can hold consecutive same-role observations, which the
    Anthropic API rejects. Merge those turns so any transcript stays sendable.
    """
    system_parts: list[str] = []
    turns: list[dict[str, str]] = []
    for message in messages:
        role = message.get("role")
        content = message.get("content")
        if not isinstance(content, str):
            raise ValueError("Message content must be text.")
        if role == "system":
            system_parts.append(content)
            continue
        normalized = "assistant" if role == "assistant" else "user"
        if turns and turns[-1]["role"] == normalized:
            turns[-1]["content"] += "\n\n" + content
        else:
            turns.append({"role": normalized, "content": content})
    if not turns:
        raise ValueError("At least one user or assistant message is required.")
    return "\n\n".join(part for part in system_parts if part), turns


def _anthropic_text(content: Any) -> str:
    """Join text blocks; native tool_use blocks fail closed like OpenAI tool_calls."""
    if not isinstance(content, list):
        raise ValueError("Missing content blocks.")
    texts: list[str] = []
    for block in content:
        if not isinstance(block, dict):
            raise ValueError("Invalid content block.")
        kind = block.get("type")
        if kind == "text":
            text = block.get("text")
            if not isinstance(text, str):
                raise ValueError("Invalid text block.")
            if text:
                texts.append(text)
        elif kind in {"tool_use", "server_tool_use", "function_call"}:
            raise RuntimeError(
                "Reasoning returned native tool calls; use the <tool>/<final> text protocol."
            )
        # Thinking/redacted blocks are provider-internal; only text is executable intent.
    text = "".join(texts)
    if not text:
        raise ValueError("Missing text content.")
    return text


class OpenAICompatibleReasoningModel:
    """llama.cpp, Ollama, or a hosted compatible server; no SDK dependency."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout_s: float | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        api_key: str | None = None,
    ) -> None:
        defaults = AgentConfig()
        self._base = api_base_url(defaults.llm_base_url if base_url is None else base_url)
        self._model = defaults.llm_model if model is None else model
        self._timeout_s = defaults.llm_timeout_s if timeout_s is None else timeout_s
        self._max_tokens = defaults.llm_max_tokens if max_tokens is None else max_tokens
        self._temperature = defaults.llm_temperature if temperature is None else temperature
        self._api_key = api_key

    def _request(
        self, path: str, payload: dict | None = None, timeout: float | None = None
    ) -> dict:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        request = urllib.request.Request(
            self._base + path,
            data=json.dumps(payload, allow_nan=False).encode() if payload is not None else None,
            headers=headers,
        )
        try:
            opener = urllib.request.build_opener(_NoRedirect())
            with opener.open(request, timeout=timeout or self._timeout_s) as response:
                raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise RuntimeError("Reasoning backend response exceeded the size limit.")
            body = json.loads(raw)
            if not isinstance(body, dict):
                raise RuntimeError("Reasoning backend returned a non-object response.")
            return body
        except urllib.error.HTTPError as exc:
            try:
                detail = exc.read(2000).decode("utf-8", "replace")
            except (OSError, ValueError):
                detail = ""
            suffix = f" Detail: {detail[:500]}" if detail.strip() else ""
            raise RuntimeError(
                f"Reasoning backend returned HTTP {exc.code}. Check the model, URL, and "
                f"server-side API key configuration.{suffix}"
            ) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise RuntimeError(
                "Reasoning backend is unreachable or timed out. Start the model server and "
                "check its URL from the machine running Relay."
            ) from exc
        except (ValueError, UnicodeError) as exc:
            raise RuntimeError("Reasoning backend returned invalid JSON.") from exc

    def generate(self, messages: list[dict[str, Any]]) -> str:
        # Internal context annotations never go to the provider. No tools/tool_choice.
        clean = [{"role": message["role"], "content": message["content"]} for message in messages]
        body = self._request(
            "/chat/completions",
            {
                "model": self._model,
                "messages": clean,
                "max_tokens": self._max_tokens,
                "temperature": self._temperature,
                "stream": False,
            },
        )
        try:
            choice = body["choices"][0]
            check_finish(choice.get("finish_reason"))
            message = choice["message"]
            # Non-streaming requests retain the same native-call/encoding guards.
            list(response_deltas(message))
            content = message.get("content")
            if not isinstance(content, str):
                raise ValueError("Missing text content.")
            return content
        except (KeyError, IndexError, TypeError, AttributeError, ValueError) as exc:
            raise RuntimeError("Bad reasoning backend response: expected assistant text.") from exc

    @property
    def model_name(self) -> str:
        return self._model

    def stream(
        self,
        messages: list[dict[str, Any]],
        *,
        cancelled: Callable[[], bool] | None = None,
    ) -> Iterator[ModelDelta]:
        """Read actual provider SSE. An application/json response is an honest fallback.

        A provider that rejects streaming should be configured with llm_stream=false;
        there is no automatic duplicate request, demo fallback, or invented token stream.
        """
        clean = [{"role": message["role"], "content": message["content"]} for message in messages]
        payload = {
            "model": self._model,
            "messages": clean,
            "max_tokens": self._max_tokens,
            "temperature": self._temperature,
            "stream": True,
            "stream_options": {"include_usage": True},
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream, application/json",
        }
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        request = urllib.request.Request(
            self._base + "/chat/completions",
            data=json.dumps(payload, allow_nan=False).encode(),
            headers=headers,
        )
        try:
            with streaming_transport(cancelled, _NoRedirect(), timeout_s=self._timeout_s) as opener:
                with opener.open(request, timeout=self._timeout_s) as response:
                    content_type = response.headers.get_content_type()
                    if content_type == "application/json":
                        raw = response.read(MAX_RESPONSE_BYTES + 1)
                        check_cancelled(cancelled)
                        if len(raw) > MAX_RESPONSE_BYTES:
                            raise RuntimeError(
                                "Reasoning backend response exceeded the size limit."
                            )
                        body = decode_packet(raw.decode("utf-8"))
                        choice = body["choices"][0]
                        check_finish(choice.get("finish_reason"))
                        yield ModelDelta(kind="metadata", streamed=False)
                        yield from response_deltas(choice["message"])
                        yield ModelDelta(
                            kind="metadata",
                            usage=usage_counts(body.get("usage")),
                            finish_reason="stop",
                        )
                        return
                    if content_type != "text/event-stream":
                        raise RuntimeError(
                            "Reasoning backend must return text/event-stream or application/json."
                        )
                    yield ModelDelta(kind="metadata", streamed=True)
                    finished = False
                    for data in sse_payloads(response, cancelled):
                        if data.strip() == "[DONE]":
                            finished = True
                            break
                        body = decode_packet(data)
                        counts = usage_counts(body.get("usage"))
                        if counts:
                            yield ModelDelta(kind="metadata", usage=counts)
                        choices = body.get("choices", [])
                        if not isinstance(choices, list):
                            raise RuntimeError("Reasoning stream returned an invalid choices list.")
                        for choice in choices:
                            if not isinstance(choice, dict):
                                raise RuntimeError("Reasoning stream returned an invalid choice.")
                            if choice.get("index", 0) != 0:
                                continue
                            delta = choice.get("delta", {})
                            if not isinstance(delta, dict):
                                raise RuntimeError("Reasoning stream returned an invalid delta.")
                            if finished and (
                                delta.get("content")
                                or delta.get("reasoning_content")
                                or delta.get("reasoning")
                            ):
                                raise IncompleteGeneration(
                                    "Provider sent text after its finish marker."
                                )
                            yield from response_deltas(delta)
                            finish = choice.get("finish_reason")
                            check_finish(finish)
                            if finish is not None:
                                finished = True
                    check_cancelled(cancelled)
                    if not finished:
                        raise IncompleteGeneration(
                            "Reasoning stream disconnected before completion; "
                            "no partial tool call was executed."
                        )
                    yield ModelDelta(kind="metadata", finish_reason="stop")
        except (GenerationCancelled, IncompleteGeneration):
            raise
        except urllib.error.HTTPError as exc:
            check_cancelled(cancelled)
            exc.close()
            raise RuntimeError(
                f"Reasoning backend returned HTTP {exc.code}. "
                "Check the model, URL, and server-side "
                "API key. If this provider cannot stream, disable model streaming in Settings."
            ) from exc
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as exc:
            check_cancelled(cancelled)
            raise RuntimeError(
                "Reasoning backend is unreachable, disconnected, or timed out during streaming."
            ) from exc
        except (ValueError, KeyError, IndexError, TypeError, AttributeError) as exc:
            check_cancelled(cancelled)
            raise RuntimeError(
                "Bad reasoning backend stream: expected assistant text deltas."
            ) from exc

    def check_connection(self) -> list[str]:
        body = self._request("/models", timeout=min(self._timeout_s, 10.0))
        return [
            item["id"]
            for item in body.get("data", [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        ]


class AnthropicCompatibleReasoningModel:
    """Anthropic Messages API (native or Anthropic-compatible proxy); no SDK dependency."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout_s: float | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        api_key: str | None = None,
    ) -> None:
        defaults = AgentConfig()
        raw = defaults.llm_base_url if base_url is None else base_url
        if base_url is None and (defaults.llm_provider or "openai") == "anthropic":
            raw = "https://api.anthropic.com"
        self._base = anthropic_base_url(raw)
        self._model = defaults.llm_model if model is None else model
        self._timeout_s = defaults.llm_timeout_s if timeout_s is None else timeout_s
        self._max_tokens = defaults.llm_max_tokens if max_tokens is None else max_tokens
        self._temperature = defaults.llm_temperature if temperature is None else temperature
        self._api_key = api_key

    def _request(
        self, path: str, payload: dict | None = None, timeout: float | None = None
    ) -> dict:
        request = urllib.request.Request(
            self._base + path,
            data=json.dumps(payload, allow_nan=False).encode() if payload is not None else None,
            headers=_anthropic_headers(self._api_key),
        )
        try:
            opener = urllib.request.build_opener(_NoRedirect())
            with opener.open(request, timeout=timeout or self._timeout_s) as response:
                raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise RuntimeError("Reasoning backend response exceeded the size limit.")
            body = json.loads(raw)
            if not isinstance(body, dict):
                raise RuntimeError("Reasoning backend returned a non-object response.")
            return body
        except urllib.error.HTTPError as exc:
            try:
                detail = exc.read(2000).decode("utf-8", "replace")
            except (OSError, ValueError):
                detail = ""
            suffix = f" Detail: {detail[:500]}" if detail.strip() else ""
            raise RuntimeError(
                f"Reasoning backend returned HTTP {exc.code}. Check the model, URL, "
                f"provider, and server-side API key configuration.{suffix}"
            ) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise RuntimeError(
                "Reasoning backend is unreachable or timed out. Start the model server and "
                "check its URL from the machine running Relay."
            ) from exc
        except (ValueError, UnicodeError) as exc:
            raise RuntimeError("Reasoning backend returned invalid JSON.") from exc

    def _payload(self, messages: list[dict[str, Any]], *, stream: bool) -> dict:
        system, turns = _split_anthropic_messages(messages)
        payload: dict[str, Any] = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "messages": turns,
            "stream": stream,
        }
        if system:
            payload["system"] = system
        if self._temperature is not None:
            payload["temperature"] = self._temperature
        return payload

    def generate(self, messages: list[dict[str, Any]]) -> str:
        try:
            body = self._request("/messages", self._payload(messages, stream=False))
            check_finish(body.get("stop_reason"))
            return _anthropic_text(body.get("content"))
        except (KeyError, IndexError, TypeError, AttributeError, ValueError) as exc:
            raise RuntimeError("Bad reasoning backend response: expected assistant text.") from exc

    @property
    def model_name(self) -> str:
        return self._model

    def stream(
        self,
        messages: list[dict[str, Any]],
        *,
        cancelled: Callable[[], bool] | None = None,
    ) -> Iterator[ModelDelta]:
        """Read actual provider SSE. No automatic non-streaming retry or invented tokens."""
        try:
            payload = self._payload(messages, stream=True)
        except ValueError as exc:
            raise RuntimeError("Bad reasoning backend request: invalid messages.") from exc
        request = urllib.request.Request(
            self._base + "/messages",
            data=json.dumps(payload, allow_nan=False).encode(),
            headers={
                **_anthropic_headers(self._api_key),
                "Accept": "text/event-stream, application/json",
            },
        )
        try:
            with streaming_transport(cancelled, _NoRedirect(), timeout_s=self._timeout_s) as opener:
                with opener.open(request, timeout=self._timeout_s) as response:
                    content_type = response.headers.get_content_type()
                    if content_type != "text/event-stream":
                        raise RuntimeError(
                            "Reasoning backend must return text/event-stream. "
                            "If this provider cannot stream, disable model streaming in Settings."
                        )
                    yield ModelDelta(kind="metadata", streamed=True)
                    finished = False
                    for data in sse_payloads(response, cancelled):
                        if data.strip() in {"[DONE]", ""}:
                            continue
                        body = decode_packet(data)
                        kind = body.get("type")
                        if kind == "message_start":
                            counts = usage_counts((body.get("message") or {}).get("usage"))
                            if counts:
                                yield ModelDelta(kind="metadata", usage=counts)
                        elif kind == "content_block_start":
                            block = body.get("content_block") or {}
                            if (block.get("type") or "") in {
                                "tool_use",
                                "server_tool_use",
                            }:
                                raise RuntimeError(
                                    "Reasoning returned native tool calls; use the "
                                    "<tool>/<final> text protocol."
                                )
                        elif kind == "content_block_delta":
                            delta = body.get("delta") or {}
                            dtype = delta.get("type")
                            if dtype == "text_delta":
                                text = delta.get("text", "")
                                if not isinstance(text, str):
                                    raise RuntimeError("Reasoning stream returned non-text.")
                                if text:
                                    text.encode("utf-8")
                                    yield ModelDelta(text=text, kind="content")
                            elif dtype == "thinking_delta":
                                text = delta.get("thinking", "")
                                if isinstance(text, str) and text:
                                    text.encode("utf-8")
                                    yield ModelDelta(text=text, kind="reasoning")
                        elif kind == "message_delta":
                            delta = body.get("delta") or {}
                            if "stop_reason" in delta:
                                check_finish(delta.get("stop_reason"))
                                finished = True
                            counts = usage_counts(body.get("usage"))
                            if counts:
                                yield ModelDelta(kind="metadata", usage=counts)
                        elif kind == "message_stop":
                            finished = True
                        elif kind == "error":
                            raise RuntimeError("Reasoning backend reported a stream error.")
                    check_cancelled(cancelled)
                    if not finished:
                        raise IncompleteGeneration(
                            "Reasoning stream disconnected before completion; "
                            "no partial tool call was executed."
                        )
                    yield ModelDelta(kind="metadata", finish_reason="stop")
        except (GenerationCancelled, IncompleteGeneration):
            raise
        except urllib.error.HTTPError as exc:
            check_cancelled(cancelled)
            exc.close()
            raise RuntimeError(
                f"Reasoning backend returned HTTP {exc.code}. "
                "Check the model, URL, provider, and server-side "
                "API key. If this provider cannot stream, disable model streaming in Settings."
            ) from exc
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as exc:
            check_cancelled(cancelled)
            raise RuntimeError(
                "Reasoning backend is unreachable, disconnected, or timed out during streaming."
            ) from exc
        except (ValueError, KeyError, IndexError, TypeError, AttributeError) as exc:
            check_cancelled(cancelled)
            raise RuntimeError(
                "Bad reasoning backend stream: expected assistant text deltas."
            ) from exc

    def check_connection(self) -> list[str]:
        request = urllib.request.Request(
            self._base + "/models",
            headers=_anthropic_headers(self._api_key),
        )
        try:
            opener = urllib.request.build_opener(_NoRedirect())
            with opener.open(request, timeout=min(self._timeout_s, 10.0)) as response:
                body = json.loads(response.read(MAX_RESPONSE_BYTES + 1))
            if not isinstance(body, dict):
                raise RuntimeError("Reasoning backend returned a non-object response.")
            return [
                item["id"]
                for item in body.get("data", [])
                if isinstance(item, dict) and isinstance(item.get("id"), str)
            ]
        except urllib.error.HTTPError as exc:
            raise RuntimeError(
                f"Reasoning backend returned HTTP {exc.code}. Check the model, URL, "
                "provider, and server-side API key configuration."
            ) from exc
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            raise RuntimeError(
                "Reasoning backend is unreachable or returned an unusable model list."
            ) from exc


def build_reasoning_model(
    base_url: str | None = None,
    model: str | None = None,
    timeout_s: float | None = None,
    max_tokens: int | None = None,
    temperature: float | None = None,
    api_key: str | None = None,
    provider: str | None = None,
) -> OpenAICompatibleReasoningModel | AnthropicCompatibleReasoningModel:
    """Provider dropdown entry point: same contract, OpenAI- or Anthropic-styled transport."""
    active = provider if provider is not None else AgentConfig().llm_provider
    if active == "anthropic":
        return AnthropicCompatibleReasoningModel(
            base_url=base_url,
            model=model,
            timeout_s=timeout_s,
            max_tokens=max_tokens,
            temperature=temperature,
            api_key=api_key,
        )
    if active != "openai":
        raise ValueError("llm_provider must be 'openai' or 'anthropic'.")
    return OpenAICompatibleReasoningModel(
        base_url=base_url,
        model=model,
        timeout_s=timeout_s,
        max_tokens=max_tokens,
        temperature=temperature,
        api_key=api_key,
    )


# Preserve the original public name used by V0 integrations.
LlamaServerReasoningModel = OpenAICompatibleReasoningModel
