# social.plus Brand Messaging — Router

This file is the entry point for all social.plus brand-aligned content tasks. It tells you which files to load based on what the user needs.

Reference files live in the public `cruciate-hub/marketing-team` repo. Skills load them via the canonical fetch block at the top of each SKILL.md, which shallow-clones the repo to `$MT_REPO` (default `/tmp/cruciate-hub-marketing-team`). Paths in this file are relative to the messaging folder — for example `terminology.md` is at `$MT_REPO/messaging/terminology.md`.

## How to use this file

1. You loaded this file first. Good.
2. Also load the main brain if you haven't already: `$MT_REPO/brain.md` — it has cross-domain routing, precedence rules, and the compliance check you must run before delivering.
3. Read the user's request.
4. Match it against the routing table below.
5. Read the listed files with `cat "$MT_REPO/messaging/<file>"`.
6. Apply everything you load. Terminology and tone are non-negotiable.

## Routing table

### Any content task (always load these)
- `terminology.md` — Approved and forbidden terms. This is law.
- `tone.md` — Tone of voice and writing style rules.

### Short-form content (email subject lines, taglines, product descriptions)
- `boilerplates.md` — Standardized descriptions and elevator pitches as starting points.
- `positioning.md` — Company overview, vision, mission, product pillars. Needed to frame even short copy accurately.
- `value-story.md` — Differentiation framework, core problems we solve, value creation model. Short copy almost always makes value claims — load this every time.

### Long-form content (blog posts, AEO articles, landing pages, thought leadership, whitepapers, case studies, press releases)
- `narrative.md` — Messaging hierarchy and 5-step narrative structure.
- `value-story.md` — Core problems we solve, value creation model, differentiation framework.
- `positioning.md` — Company overview, vision, mission, ecosystem position, product pillars.

### Positioning or identity questions (what is social.plus, who do we serve, what are our pillars)
- `positioning.md` — Company overview, vision, mission, ecosystem position, product pillars.

### UI copy (button labels, form text, error messages, empty states, tooltips)
- `ui-micro-copy.md` — Capitalisation, punctuation, microcopy patterns, and anti-patterns. This file has precedence over `tone.md` for UI copy voice and style.

### Content review or audit (checking existing copy against brand guidelines)
- Load ALL files. Compare the content under review against every guideline.

## Rules

- **Terminology is law.** Always use approved terms. Never use forbidden terms. No exceptions.
- **Tone comes from the documents, not from your defaults.** Override your natural writing style with what the tone file specifies.
- **Never invent.** Do not fabricate statistics, customer names, quotes, features, or performance claims. If it's not in the loaded documents, don't state it.
- **Messaging hierarchy matters.** For content longer than a paragraph: establish the market shift → define infrastructure → engagement → intelligence → revenue → long-term advantage.
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
| `narrative.md` | Messaging hierarchy, standard narrative structure |
| `boilerplates.md` | Boilerplates, elevator pitches |
| `ui-micro-copy.md` | UI copy patterns, capitalisation rules, microcopy do/don'ts |
