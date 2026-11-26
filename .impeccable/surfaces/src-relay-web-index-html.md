---
version: 1
slug: "src-relay-web-index-html"
primary_target: "src/relay/web/index.html"
related_targets: []
---

# Surface: Relay operator console

Mode: Operate. The whole browser console (`src/relay/web/`): Playground, Files,
Tools, Run history, Settings, dialogs.

Audience: a solo developer running local models, in long dense sessions, supervising
multi-step agent work. Task: send a request, watch reasoning/tool/gate states, approve
or deny severe actions, inspect files and runs, tune the runtime.

## Direction contract

THESIS: Relay is a job control console, not a chat app. Every request is an INPUT
field, every reply is an operation record with return codes, and a persistent
Operator Information Area tells the truth about runtime state. The category-default
arrangement — a centered welcome hero over floating cards and a bubbly composer —
is refused.

OWN-WORLD: Flat blue-black console panels (#0b1014 ground, #11181d panel, 1px
#26343d rules, 2px radius max), reversed label bars, tabular monospace data, square
status lamps. Signal palette: turquoise interactive, green ready, amber attention,
red alarm. Light theme is a cool printout grey with the same field grammar.
Typography: Spline Sans Mono for data and labels, Spline Sans for prose.

STORY: The developer sees what the agent intends, which gate it is at, what ran, and
what it returned — without opening a modal or decoding a bubble.

FIRST VIEWPORT: 44px system bar with breadcrumb; compact job header (PLAYGROUND ·
READY · OFFLINE DEMO); left-aligned operation log with an INPUT bar and a RELAY /
RESPONSE record; 300px operator panel at right; command-line composer; 26px OIA
status line along the bottom. The empty state reads READY. with four coded starter
rows, not a decorative hero.

FORM: grounded candidate 3 of 7 (mainframe operations console), seed key 7669534c.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish
review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.
