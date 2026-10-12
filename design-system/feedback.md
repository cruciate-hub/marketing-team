# Feedback from tests

Details the team has already corrected once. Each one must hold on every page, in every set (captured and framed). Check the rendered page against this list before calling it done (definition of done, point 10). Newest first.

How an item gets here: someone spots a detail on a test page that was right before or that the team decided ("this was picked up before, now it is gone"). The fix goes into the section's preview or source first, because Claude Design copies what the previews show; then the item is added here with where it lives and how to check it, and both land in one pull request the same day.

| # | Date | Detail that must hold | Where it lives | How to check |
|---|---|---|---|---|
| 6 | 2026-10-12 | Two primary buttons only for a product that connects to two AI apps on equal terms (Agentry: Claude and ChatGPT), one per app, in the hero and the CTA band. Everywhere else one primary per section. Decision: Stefan | Definition of done point 5; `taste.md`; both product landing recipes | Count the blue buttons per section |
| 5 | 2026-10-12 | The "Works in" row under a hero: the label "Works in" centred between two fading hairlines, then each tool as its approved icon in a 40px tile with the name beside it, then "+ Any MCP-compatible tool" (or the product's own wording from `messaging/product-capabilities.md`). Never names alone when an approved icon exists, never lettered or redrawn icons, only tools the product supports today. Picked up in Test 2, lost on the framed hero in Test 3 | Captured: `sections/02-hero-simple/` (`.text-divider`, `.mcp-logo`). Framed: `sections/framed/F02-hero-centered/` (second hero, `.hero_works`) | The row is there, the label has the two lines, every named tool shows its icon tile |
| 4 | 2026-10-09 | Inside the frame there are cells divided by lines, never floating cards (no fill, no radius, no gap); a captured section is never wrapped in the frame. A page is framed or captured, never both | `foundations/grid-and-frame/foundation.md`; `sections/framed/README.md` | No rounded or filled boxes between the frame lines |
| 3 | 2026-10-07 | Card icons sit top-left above the title, never beside the text | `sections/13-card-grid-icons/section.md`; `taste.md` | Icon above the title in every card or cell |
| 2 | 2026-10-07 | Third-party logos only from the approved files in `assets/third-party/` (Claude mark for Claude Code, OpenAI mark for ChatGPT and Codex) | `foundations/logo/foundation.md`, "Third-party logos" | Every logo is one of the approved files |
| 1 | 2026-10-07 | The social.plus logo keeps its colours (white wordmark on dark): use the files with colours on the shapes | `foundations/logo/foundation.md`; `assets/media/` logo | The logo is not black or one colour |
