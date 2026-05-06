# Messaging

Brand messaging source of truth for social.plus. These files are fetched live from GitHub by the `brand-messaging` skill and other content skills in the [`product-marketing-team`](../skills) plugin — edits here go live immediately, no reinstall needed.

`brain.md` is the router: skills read it first, then pull whichever other files the task requires.

## Files

| File | Lines | Size | Description |
|---|---:|---:|---|
| [brain.md](./brain.md) | 75 | 4.8 KB | Router — entry point for brand-messaging tasks; maps requests to the files below. |
| [positioning.md](./positioning.md) | 235 | 11.0 KB | Company overview, category, positioning statements, audience, and differentiators. |
| [narrative.md](./narrative.md) | 108 | 3.4 KB | Messaging hierarchy and narrative frameworks — how to order emphasis in any piece. |
| [value-story.md](./value-story.md) | 129 | 5.8 KB | Core problems social.plus solves and the value pillars that address them. |
| [boilerplates.md](./boilerplates.md) | 49 | 3.5 KB | Standardized elevator pitches — 25-word, 50-word, and longer variants. |
| [tone.md](./tone.md) | 106 | 3.2 KB | Tone of voice and writing style for marketing and external content. |
| [terminology.md](./terminology.md) | 124 | 2.9 KB | Approved terminology — brand name, product names, capitalization, phrasing to avoid. |
| [ui-micro-copy.md](./ui-micro-copy.md) | 134 | 5.9 KB | Product UI copy conventions — labels, errors, buttons, tooltips, placeholders. |

## Precedence

- For **UI copy**, `ui-micro-copy.md` overrides `tone.md`.
- `terminology.md` applies everywhere and is never overridden.
- For cross-domain conflicts, consult the root [`brain.md`](../brain.md).

## Fetching

All messaging files are read from the shallow clone of this repo at `$MT_REPO/messaging/...`. The canonical fetch block at the top of each SKILL.md handles the clone.
