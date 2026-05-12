# social.plus Brand Messaging — Router

This file is the entry point for all social.plus brand-aligned content tasks. It tells you which files to load based on what the user needs.

Reference files live in the public `cruciate-hub/marketing-team` repo. Skills load them via the canonical fetch block at the top of each SKILL.md, which shallow-clones the repo to `$MT_REPO` (default `/tmp/cruciate-hub-marketing-team`). Paths in this file are relative to the messaging folder — for example `terminology.md` is at `$MT_REPO/messaging/terminology.md`.

## How to use this file

1. You loaded this file first. Good.
2. Also load the main brain if you haven't already: `$MT_REPO/brain.md` — it has cross-domain routing, precedence rules, and the compliance check you must run before delivering.
3. Read the user's request.
4. Match it against the routing table below. Each row is an independent condition — load every row that applies to your output, not just one.
5. Read the listed files with `cat "$MT_REPO/messaging/<file>"`.
6. Apply everything you load. Terminology and tone are non-negotiable.

## Routing table

Each row below is a condition based on **what your output is or contains** — not how long it is. Multiple rows usually apply at once; load the union of every matching row.

### Any content task (always load these)
- `terminology.md` — Approved and forbidden terms. This is law.
- `tone.md` — Tone of voice and writing style rules (overridden by `ui-micro-copy.md` for UI surfaces).

### Content that describes what social.plus is or its category
- `positioning.md` — Company overview, vision, mission, ecosystem position, product pillars.

### Content that makes a value, differentiation, or problem/solution argument
- `value-story.md` — Core problems we solve, value creation model, differentiation framework.

### Content using approved company copy (taglines, social bios, ad footers, hero subtitles, "About social.plus" blocks, elevator pitches)
- `boilerplates.md` — Standardized descriptions at 25w / 50w / 70w / extended lengths, plus situational elevator pitches.

### Multi-section content following the messaging hierarchy (Context → Tension → Infrastructure → Impact → Advantage)
- `narrative.md` — 5-step narrative structure for press releases, blog posts, case studies, pitch decks, long-form pages.

### UI surface copy (buttons, errors, tooltips, empty states, form labels)
- `ui-micro-copy.md` — Microcopy patterns and capitalisation rules. Overrides `tone.md` for voice; `terminology.md` still applies.

### Content review or audit (checking existing copy against brand guidelines)
- Load ALL files. Compare the content under review against every guideline.

## Rules

- **Terminology is law.** Always use approved terms. Never use forbidden terms. No exceptions.
- **Tone comes from the documents, not from your defaults.** Override your natural writing style with what the tone file specifies.
- **Never invent.** Do not fabricate statistics, customer names, quotes, features, or performance claims. If it's not in the loaded documents, don't state it.
- **Messaging hierarchy matters.** For multi-section content: establish the market shift → define infrastructure → engagement → intelligence → revenue → long-term advantage.
- **Boilerplates are starting points.** Adapt to context but preserve meaning and claims.
- **If a load fails** (clone error, missing file, or wrong format), follow the canonical fetch block's hard-fail rule — do not proceed with stale or memorized content.
- **Run the compliance check** from `brain.md` (the main brain) before delivering your output.

## Available files

| File | Contains |
|---|---|
| `positioning.md` | Company overview, vision, mission, ecosystem position, what we are/aren't, product pillars |
| `value-story.md` | Core problems we solve, value creation model, differentiation framework |
| `terminology.md` | Approved terms, forbidden terms |
| `tone.md` | Tone of voice, writing style rules |
| `narrative.md` | Messaging hierarchy, 5-step narrative structure |
| `boilerplates.md` | Boilerplates (25w / 50w / 70w / extended), elevator pitches |
| `ui-micro-copy.md` | UI copy patterns, capitalisation rules, microcopy do/don'ts |
