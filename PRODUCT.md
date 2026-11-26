# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

A single developer running local models on their own machine, usually at a desktop
workstation for long, dense sessions. They keep Relay open beside an editor and a
terminal while they read code, search a repository, run commands, write files, and
supervise multi-step agent work. They are technical, impatient with ceremony, and
comfortable with dense tooling.

## Product Purpose

Relay is a local-first agent harness: a reasoning model thinks in natural language, a
small action model turns each intent into one tool call, and the runtime owns
validation, confidence gates, approvals, execution, and the next reasoning turn. The
browser console makes that loop visible and steerable — streaming reasoning, tool
calls, approvals, results, run history, and workspace state. Success means the
developer can see exactly what the agent intends, approve or stop it, and trust what
actually ran.

## Positioning

Relay is the harness, not the model. It separates natural-language reasoning from a
narrow translator and puts every executable action behind a runtime the developer
controls. A neighbouring chat product cannot copy that truthfully: Relay never lets
the reasoning model emit JSON or execute tools, never executes a high-confidence
invalid call, and keeps severe actions behind tiered, editable approvals.

## Operating Context

- Runs as a local Python server; the browser is a thin client over HTTP + SSE.
- Used with local model servers (llama.cpp, Ollama, Needle, a fine-tuned FunctionGemma
  translator) or a hosted OpenAI/Anthropic-compatible endpoint.
- The workspace is a real filesystem root; paths are resolved and contained.
- Work is long and multi-step: transcripts grow, runs accumulate, context budgets and
  stalls matter. `tasks.md` in the workspace root carries durable multi-step work.
- The demo mode is deterministic and offline; live mode is explicit, never a silent
  fallback.
- Settings are session-local; portable TOML can be exported and imported.
- Sessions persist write-through to SQLite; per-token model traces never persist.

## Capabilities and Constraints

- Playground with streaming reasoning, draft tool cards, approvals with diffs,
  `ask_user` pause/resume, cancellation, and a per-run inspector (pipeline, activity,
  model I/O).
- Files browser with bounded previews; Tools catalog of 33 canonical definitions;
  Run history with exportable JSON traces; Settings for models, limits, context,
  streaming, prompts, and appearance.
- 33 tools across filesystem, editing, execution, git, web, environment, utility, and
  interaction.
- Tiered approvals, confidence gates (0.85 write / 0.5 read-only), 20 tool steps,
  3 stalled turns, context compression past ~80%.
- Frontend is static vanilla HTML/CSS/JS with no build step and no framework; core
  dependencies stay LangGraph, Pydantic, and cactus-needle.
- Light and dark themes plus custom UI/accent colors must keep working.
- All existing features and behavior must survive a visual overhaul.
- This is a personal development console, not a multi-tenant service.

## Brand Commitments

- The product name is **Relay**; **Needle** names only the external action-model engine.
  Keep that distinction in UI copy.
- Voice: direct, technical, honest. No hype, no invented capability, no fabricated
  confidence.
- The logo mark may be redrawn; the name may not change.

## Evidence on Hand

- `docs/final-spec.md`, `docs/spec-v0.md`, `docs/configuration.md`,
  `docs/streaming.md`, and `README.md` carry the product truth and the exact numbers
  above.
- `src/relay/web/` holds the incumbent implementation and its copy.
- There are no customer logos, testimonials, pricing, or benchmarks to display; do not
  fabricate any.

## Product Principles

1. **Show the loop.** Every state — intent, translation, gate, approval, result — is
   visible in the console; nothing important happens off-screen.
2. **Density is respect.** A developer in a long session should see more, scan faster,
   and scroll less.
3. **The runtime is the authority.** Visual language should make the gates and
   boundaries legible, not soften them.
4. **Local and honest.** Offline, demo, buffered, and uncalibrated states are labelled
   plainly; no fake liveness.
5. **The console recedes.** The work — transcript, files, diffs, traces — is the
   content; chrome stays quiet and consistent.

## Accessibility & Inclusion

No product-specific standard was established. Preserve semantic HTML, keyboard
operation, visible focus, reduced-motion support, and readable contrast in both
themes.
