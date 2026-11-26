---
name: Relay Operator Console
description: A mainframe job-control surface for supervising local agent runs.
colors:
  console-ground: "#0b1014"
  console-panel: "#111a20"
  console-panel-soft: "#16232a"
  console-panel-hover: "#1b2b33"
  console-rail: "#070c0f"
  console-topbar: "#0e1519"
  console-ink: "#d6e4e6"
  console-rule: "#383f42"
  console-on-accent: "#04100f"
  signal-turquoise: "#2fd4c4"
  signal-green: "#57d98b"
  signal-amber: "#e3a63f"
  signal-red: "#f06a6a"
  printout-ground: "#e9eef0"
  printout-panel: "#f4f7f8"
  printout-panel-soft: "#e2e9eb"
  printout-rail: "#dfe7e9"
  printout-ink: "#12211f"
  printout-on-accent: "#ffffff"
  teal-accent: "#0f7d78"
  printout-green: "#177a4a"
  printout-amber: "#8a5a06"
  printout-red: "#ad2a22"
typography:
  display:
    fontFamily: "Spline Sans Mono, SFMono-Regular, Consolas, monospace"
    fontSize: "clamp(30px, 4.4vw, 44px)"
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "0.01em"
  headline:
    fontFamily: "Spline Sans Mono, SFMono-Regular, Consolas, monospace"
    fontSize: "15px"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0.02em"
  title:
    fontFamily: "Spline Sans Mono, SFMono-Regular, Consolas, monospace"
    fontSize: "13px"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.04em"
  body:
    fontFamily: "Spline Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "0em"
  label:
    fontFamily: "Spline Sans Mono, SFMono-Regular, Consolas, monospace"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.04em"
  brand:
    fontFamily: "Spline Sans Mono, SFMono-Regular, Consolas, monospace"
    fontSize: "17px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.03em"
  data:
    fontFamily: "Spline Sans Mono, SFMono-Regular, Consolas, monospace"
    fontSize: "15px"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0em"
  stat:
    fontFamily: "Spline Sans Mono, SFMono-Regular, Consolas, monospace"
    fontSize: "19px"
    fontWeight: 600
    lineHeight: 1
  stat-compact:
    fontFamily: "Spline Sans Mono, SFMono-Regular, Consolas, monospace"
    fontSize: "16px"
    fontWeight: 600
    lineHeight: 1
  dialog-title:
    fontFamily: "Spline Sans Mono, SFMono-Regular, Consolas, monospace"
    fontSize: "14px"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.03em"
  display-compact:
    fontFamily: "Spline Sans Mono, SFMono-Regular, Consolas, monospace"
    fontSize: "26px"
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "0.01em"
rounded:
  square: "0px"
components:
  button-primary:
    backgroundColor: "{colors.signal-turquoise}"
    textColor: "{colors.console-on-accent}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "6px 13px"
    height: "32px"
  button-default:
    backgroundColor: "{colors.console-panel}"
    textColor: "{colors.console-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "6px 13px"
    height: "32px"
  text-input:
    backgroundColor: "{colors.console-ground}"
    textColor: "{colors.console-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "7px 9px"
    height: "32px"
  status-badge-running:
    backgroundColor: "transparent"
    textColor: "{colors.signal-turquoise}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "2px 6px"
  oia-state-ready:
    backgroundColor: "{colors.signal-green}"
    textColor: "{colors.console-on-accent}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "0 12px"
    height: "26px"
  starter-row:
    backgroundColor: "transparent"
    textColor: "{colors.console-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.square}"
    padding: "9px 8px"
  input-record:
    backgroundColor: "{colors.console-panel}"
    textColor: "{colors.console-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.square}"
    padding: "9px 11px"
  composer-shell:
    backgroundColor: "{colors.console-panel}"
    textColor: "{colors.console-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.square}"
    padding: "0px"
---

# Design System: Relay Operator Console

## Overview

**Creative North Star: "The Job Control Deck"**

Relay is a job control deck, not a chat app. A request enters as an INPUT field, the
agent's work appears as operation records with return codes, and a persistent Operator
Information Area tells the truth about runtime state along the bottom edge. The 3270
field grammar is deliberate: reversed label bars, fixed-width data, square annunciator
lamps, and no decorative chrome between the operator and the machine.

The surface is flat blue-black in dark mode and cool printout grey in light mode, but
the grammar is identical in both. Panels are separated by 1px rules and small tonal
steps, never by drop shadows. Color is functional: turquoise means interactive, green
means ready or complete, amber means attention or pending, red means alarm or denied.
Nothing else gets a hue.

The console refuses the category defaults: no centered hero floating over cards, no
speech bubbles, no gradient glass, no pill-shaped chips, no rounded panels. Density is
the point. A solo developer should be able to watch the reasoning turn, the translator,
the gates, the tool result, and the context budget without opening a dialog or decoding
a bubble.

**Key Characteristics:**

- Square geometry: every surface has 0 radius; the spinner is the only circle.
- 1px rules and tonal steps carry structure; shadows belong only to overlays.
- Reversed ink label bars (`INPUT`, `RELAY`, `OPERATOR PANEL`, section labels) anchor
  the field grammar.
- Exactly four signal hues, each with one meaning, in both themes.
- Monospace for every label, number, path, tool name, and status token.
- The 26px OIA status line is always visible and never decorative.
- Light theme is a printout of the same console, not a separate design.
- Functional type never drops below 12px.

## Colors

Two registers, one grammar: a blue-black operations ground for dark, a cool printout
grey for light, with four signal lamps that keep their meaning in both.

### Primary

- **Signal Turquoise** (`#2fd4c4`, dark): Interactive state. Primary buttons, focus
  rings, selected navigation, current pipeline phase, active settings tab, links, and
  the send control. It should feel like the one live circuit on the board.
- **Teal Accent** (`#0f7d78`, light): The same role in the printout register. Darker
  and calmer so it holds contrast on grey paper without glowing.

### Secondary

Status is the only other color family, and it is strictly semantic:

- **Ready Green** (`#57d98b` dark / `#177a4a` light): Ready, complete, passing,
  approved, local-only operation.
- **Attention Amber** (`#e3a63f` dark / `#8a5a06` light): Waiting, pending review,
  demo mode, degraded but running.
- **Alarm Red** (`#f06a6a` dark / `#ad2a22` light): Denied, blocked, failed,
  destructive action.

### Neutral

Dark register:

- **Console Ground** (`#0b1014`): The page ground and the recessed side of inputs.
- **Console Panel** (`#111a20`): Records, cards, composer, raised working surfaces.
- **Console Panel Soft** (`#16232a`): Secondary fills, the OIA line, pressed or
  selected rows.
- **Console Panel Hover** (`#1b2b33`): Hover fill for rows, buttons, and starter rows.
- **Console Rail** (`#070c0f`): The navigation rail, darker than the work surface.
- **Console Topbar** (`#0e1519`): The breadcrumb bar, between rail and panel.
- **Console Ink** (`#d6e4e6`): Primary text and reversed bars.
- **Console Rule** (`#383f42`): The 1px divider; a computed mix of ground and ink, not
  a separate hue.
- **Console On-Accent** (`#04100f`): Text and glyphs on turquoise or green fills.

Light register:

- **Printout Ground** (`#e9eef0`): The page ground; a cool grey, never cream.
- **Printout Panel** (`#f4f7f8`): Records, cards, composer.
- **Printout Panel Soft** (`#e2e9eb`): Secondary fills and the OIA line.
- **Printout Rail** (`#dfe7e9`): The navigation rail.
- **Printout Ink** (`#12211f`): Primary text and reversed bars.
- **Printout On-Accent** (`#ffffff`): Text on the teal accent.

Muted and dim text are derived with `color-mix` from ink and ground (68% and 65% ink),
so they follow a custom base color instead of being hardcoded.

### Named Rules

**The Four-Lamp Rule.** Turquoise is interactive, green is ready, amber is attention,
red is alarm. There is no fifth hue and no decorative use of these four. If a new
element needs emphasis, use weight, a rule, or a reversed bar before reaching for color.

**The Two-Knob Rule.** The operator controls exactly two colors: a base and an accent.
`app.js` writes `--paper`, `--surface`, `--surface-soft`, `--surface-hover`,
`--sidebar-bg`, `--topbar-custom`, `--accent`, and `--accent-hover`. Every other value
derives from those. Never hardcode a palette hex in a component that should follow the
operator's theme.

**The Printout Mirror Rule.** Light mode keeps the same hue assignments and contrast
roles as dark mode. It does not introduce a second accent, warm the paper, or invert
the signal meanings.

## Typography

**Display Font:** Spline Sans Mono (with SFMono-Regular, Consolas, monospace)
**Body Font:** Spline Sans (with Segoe UI, system-ui, sans-serif)
**Label/Mono Font:** Spline Sans Mono (with Consolas, monospace)

**Character:** Spline Sans Mono is the console hardware: labels, codes, paths, counts,
tool names, and status tokens. Spline Sans is the human voice: prose answers, markdown,
and the composer. The pairing reads as a machine that reports clearly and a person who
explains, never the reverse.

Both families are bundled locally as woff2 with OFL licenses; the console must render
identically offline.

### Hierarchy

- **Display** (500, `clamp(30px, 4.4vw, 44px)`, line-height 1, `0.01em`, uppercase):
  The `READY.` empty-state word and its blinking block cursor. One per screen, never a
  decorative hero. Under 420px it uses the display-compact size of 26px.
- **Headline** (600, 15px, line-height 1.3, `0.02em`, uppercase, mono): Page titles
  (`PLAYGROUND`, `FILES`, `TOOLS`, `RUN HISTORY`, `SETTINGS`) and dialog headings.
- **Title** (600, 13px, line-height 1.4, `0.04em`, uppercase, mono): Record labels,
  card headings, empty-state headings, section titles.
- **Body** (400, 13px, line-height 1.55, Spline Sans): Prose answers and composer text.
  Markdown runs at 13px/1.68. Assistant bodies cap at 74ch, the conversation at 78ch,
  the welcome description at 62ch.
- **Label** (500-600, 12px, `0.04em`, uppercase, mono): Buttons, badges, nav keys,
  field labels, table headers, chips, timestamps. Status-line segments may reach
  `0.07em`; never wider.
- **Brand** (600, 17px, `-0.03em`, mono): The sidebar wordmark only. It is the one
  place where tracking goes negative.
- **Data** (600, 15px, mono, tabular): Step counts, elapsed time, and other figures that
  must align across rows.
- **Stat** (600, 19px/1 desktop, 16px/1 under 760px, mono): Run-history totals. The only
  numeric role allowed to exceed 15px.
- **Dialog title** (600, 14px, `0.03em`, uppercase, mono): Destructive confirmation
  headings, slightly tighter than a page headline to fit the dialog frame.

### Named Rules

**The 12px Floor.** No functional text renders below 12px. This includes badges,
timestamps, table headers, status segments, and helper copy. Legibility is not a
stylistic sacrifice.

**The Tabular Rule.** Every number, path, tool name, and status token is monospace with
tabular figures. `font-variant-numeric: tabular-nums` is set on the body so counts do
not jitter as they stream.

**The Quiet Tracking Rule.** Tracking tops out at `0.07em` (the OIA line). Labels sit
at `0.04em`, headings at `0.02em`, body at zero. Wide, airy tracking is refused; it
reads as marketing, not operations.

## Layout

The deck is a fixed three-column instrument with two horizontal rails:

- **Navigation rail:** 244px default, draggable from 64px to 320px. Below 150px it
  enters compact mode: labels and wordmarks drop, a 96px icon rail remains. Below 760px
  it becomes a 252px off-canvas drawer over a scrim.
- **Work column:** flexible, minimum width 0. Topbar 46px (48px on mobile), compact job
  header, scrolling operation log, composer docked at the bottom.
- **Operator panel:** 300px default, draggable from 220px to 480px. Below 1060px it
  hides and reopens as a fixed 300px overlay anchored 12px from the right, below the
  topbar and above the OIA.
- **Rails:** a 9px splitter between columns, a 26px OIA line across the full width.

Spacing is tight and consistent: 18px page gutters (12px on mobile), 13-14px panel
padding, 9-11px record padding, 4-8px row padding. Structural gaps are usually a 1px
rule rather than a margin. Conversation blocks use a 20px vertical gap.

Breakpoints:

- **1250px:** Page subheading hides; tool and history tables drop secondary columns.
- **1060px:** Inspector collapses to an overlay; files layout narrows to 236px.
- **900px:** Tool catalog drops the parameters column.
- **760px:** Sidebar goes off-canvas; topbar becomes 48px; compact badges hide.
- **420px:** Runtime status hides; display type drops to 26px; OIA segments condense.

## Elevation & Depth

This system is flat by default. Depth is conveyed by tonal steps (ground, panel, panel
soft, hover), 1px rules, and reversed label bars. Resting panels, cards, records, and
navigation never carry a shadow. A shadow means "this is temporarily above the deck":
dialogs, popovers, toasts, the fixed inspector overlay, and the mobile drawer.

### Shadow Vocabulary

- **Overlay (dark)** (`box-shadow: 0 18px 48px -12px rgba(0, 0, 0, 0.75)`): Dialogs,
  popovers, toasts, and fixed overlays over the blue-black ground.
- **Overlay (light)** (`box-shadow: 0 18px 44px -14px rgba(24, 40, 46, 0.35)`): The
  same overlays over printout grey; softer so it does not read as dirt on paper.
- **Input focus inset** (`box-shadow: inset 2px 0 0 var(--accent)`): The left edge bar
  on focused text fields. This is a state marker, not elevation.
- **Composer focus inset** (`box-shadow: inset 0 0 0 1px var(--accent)`): A 1px inner
  keyline when the composer has focus; amber when the run is waiting.

### Named Rules

**The Flat-By-Default Rule.** If a surface sits in the normal document flow, it has no
shadow. Add a rule or a tonal step instead.

**The Rule-Before-Shadow Rule.** Use a 1px border to separate two surfaces before
considering any other treatment. Shadows are reserved for things that genuinely float.

## Shapes

Square is the form language. Every panel, button, input, badge, chip, card, dialog,
and avatar has `border-radius: 0`. There are no pills and no rounded speech bubbles.
The only circle in the interface is the loading spinner, because rotation needs one.

Recurring geometry:

- 1px borders in rule or rule-strong; reversed label bars overlap the border by half
  their line height so the label appears cut into the frame.
- Annunciator lamps are 5-6px squares, never dots. Phase nodes are 11px squares joined
  by a 1px vertical rule.
- Icon tiles are 24px (starter rows), 26px (brand mark, avatar, tool icons), or 32px
  (empty states). Icons are 13-18px line glyphs with 1.5px strokes.
- Splitter rails are 9px wide with a 1px line; they are drag targets, not decoration.
- Tables and lists are separated by horizontal rules, not alternating fills.

## Components

### Buttons

- **Shape:** square (0 radius), 1px border, mono 12px uppercase at `0.06em`.
- **Primary:** turquoise fill, on-accent text, min-height 32px, padding 6px 13px,
  icon 13px. Used once per surface: send, save, confirm.
- **Default:** panel fill, rule-strong border, ink text. Hover moves to panel-hover.
- **Small:** min-height 27px, padding 4px 9px, same 12px type.
- **Danger:** alarm fill with white text; hover darkens the alarm by 18%.
- **Ghost / text:** transparent, muted text, no border; hover shifts to turquoise.
  Used for row actions, expand/collapse, and toolbar commands.
- **Focus:** the global 2px turquoise outline with 2px offset. Do not replace it with a
  glow.

### Chips and Badges

- **Status badge:** 2px 6px padding, 1px rule-strong border, 5px square lamp before the
  label, mono 12px uppercase. Running uses turquoise, waiting amber, error red.
- **Mode badge:** 5px 8px padding, 6px lamp, mono 12px. Offline demo shows amber; live
  shows green.
- **Composer chips** (workspace, model, permission): transparent 1px border, 3px 6px
  padding, 11px icons, mute text. Hover reveals a rule border and ink text. They open
  popovers, not dialogs.
- **Selected settings register:** a 16% turquoise tint with a turquoise border and ink
  text, not solid reverse video. This keeps dark-mode glare down while still reading as
  selected.

### Cards and Containers

- **Corner style:** square.
- **Background:** panel for records and working cards; ground for nested detail bodies.
- **Border:** 1px rule; the outer frame may use rule-strong.
- **Shadow:** none at rest; see Elevation.
- **Internal padding:** 7-11px. Summary rows are 26px minimum; detail bodies separate
  with a 1px rule and indent to the label column.
- Cards are disclosure surfaces, not marketing tiles. A tool card summarizes name,
  status, and duration; expanding reveals arguments, decision, confidence, and result.

### Inputs and Fields

- **Style:** ground fill, rule-strong border, 0 radius, mono 12px, 7px 9px padding.
  Labels are mono 12px uppercase at `0.04em` in dim text, set above the field.
- **Focus:** turquoise border plus an inset 2px left bar. No outer glow.
- **Disabled:** 50% opacity with a panel-soft fill.
- **Composer:** panel fill, 1px rule-strong, 13px Spline Sans textarea with a turquoise
  `>` prompt at 10px, 9px from the top. Focus draws a 1px inner turquoise keyline;
  waiting draws the same keyline in amber. The toolbar sits below a rule.
- **Color pickers:** 34px tall, 1px rule-strong border, an inset 1px ink keyline, and a
  visible uppercase hex readout (`#E9EEF0`) beneath each swatch.

### Navigation

- **Rail:** 244px, console-rail ground, 14px 12px padding, brand block separated by a
  rule. Brand mark is a 26px square with the relay glyph in turquoise.
- **Nav rows:** 32px minimum, 5px 7px padding, a 16px mono key code (`F1`-`F5`), a 15px
  icon, 12px label. Active rows use a 16% turquoise tint, 45% turquoise border,
  turquoise text, and a 6px square end lamp. Hover uses an 8% ink tint and a rule.
- **Section labels:** reversed bars at 12px mono, ink fill and rail-colored text.
- **Recent sessions:** 32px rows with a hover-revealed square delete control; no
  rounded avatars.
- **Compact mode:** under 150px the key, label, counts, and section text drop; icons
  center in a 96px rail. Mobile uses a 252px drawer with scrim and a 0.18s
  `cubic-bezier(0.16, 1, 0.3, 1)` slide.

### Operation Record (signature)

Every exchange is a record, not a bubble.

- The user's message is a panel-filled box with a 1px rule-strong border and a reversed
  `INPUT` label overlapping the top-left corner. Text is mono 12px/1.65, pre-wrapped.
- Relay's reply starts with a 20px square mark in turquoise, the `RELAY` label in mono
  uppercase, and a bordered mode token (`DEMO` or `LIVE`). The body is 13px Spline Sans
  markdown capped at 74ch.
- Tool and model traces stack beneath the reply as square disclosure cards, ordered
  chronologically. No chat bubbles, no alternating sides, no avatars.

### Operator Information Area (signature)

A 26px line pinned to the bottom of the viewport, always present. It is a row of
segments separated by 1px rules, mono 12px uppercase at `0.07em`:

- A solid state segment on the left (`READY` green, `BUSY` turquoise, `WAITING` amber,
  `ERROR` red) with a 6px square lamp.
- Fixed segments: `ROOT`, `JOB` (zero-padded run id), `STEPS` (`n/20`), `GATE`
  (`0.85`), `BUFFER` (`n/32k`), each label muted and each value ink, tabular.
- A flexible spacer, then a green `LOCAL` marker at the right edge.

This line is the system's honesty contract. It reflects real runtime state; it is never
filled with marketing copy or decorative telemetry.

### Runtime Pipeline (signature)

The operator panel's Activity tab lists the fixed pipeline: Reasoning, Parse intent,
Translate action, Sanitize call, Validate arguments, Confidence gate, Safety and
permissions, Execute tool, Observe result, Update context. "Request selection review"
appears only when a low-confidence review actually occurs.

- Each phase is a 12px mono row with an 11px square node and a 1px connector.
- Done nodes take a green check and green border; the current node takes a turquoise
  border with a 30% turquoise inset ring; pending nodes stay rule-strong on paper.
- A rejected action adds a bordered amber note stating the stage that blocked it; the
  phase list never pretends a blocked action executed.

### Starter Table (signature)

The empty state is a four-row task table, not a hero. A reversed header row reads
`CODE`, blank, `TASK / DETAIL`, blank. Each row is a grid of 42px code, 24px square
icon tile, flexible copy, and a 14px arrow:

- Codes `F1`-`F4` in dim mono; icon tiles tinted by signal (green explore, turquoise
  search, amber calculate, muted create).
- A bold prompt line and a 12px explanatory line.
- Hover fills the row with panel-hover and shifts the arrow 2px in turquoise.
- The display word `READY.` sits above with a blinking turquoise block cursor.

## Do's and Don'ts

- **Do** separate surfaces with a 1px rule or a tonal step before reaching for any
  other treatment.
- **Do** put field labels in reversed ink bars and keep them mono, uppercase, and 12px.
- **Do** set every number, path, tool name, and status token in Spline Sans Mono with
  tabular figures.
- **Do** keep one primary turquoise action per surface.
- **Do** keep the OIA line visible at every breakpoint, including mobile.
- **Do** derive new colors from the operator's base and accent via `color-mix`.
- **Don't** round a corner. The spinner is the only circle.
- **Don't** put a shadow on a resting panel, card, or nav row.
- **Don't** use turquoise, green, amber, or red decoratively; they are state, not
  styling.
- **Don't** render functional text below 12px or track labels wider than `0.07em`.
- **Don't** add gradients, glass, glow, or a second accent hue.
- **Don't** hide the pipeline, approvals, or run status behind a routine dialog; the
  deck shows them inline.
- **Don't** introduce a new signal hue for a new state. Reuse the four lamps and let
  the label carry the specificity.
