# F02 · Hero / Centered (framed)

- Status: approved (2026-10-12), from Amadeus's web library (v0.1, decision 8 October 2026); not yet in Webflow · Owner: Amadeus · Approved by: Stefan, 12 October 2026
- Source: the web library's page demo (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), read 12 October 2026; Webflow name in the library: "Section / Hero"
- Code: source.html (links `../../../tokens.css` and `../framed.css`) · Screenshot: none yet (render source.html)
- Captured section it replaces on a framed page: 02 Hero / Simple

One big statement with an optional wide visual in an art panel.

## Use it when
Homepage, product overview and hub pages: one promise for the whole page.

## Variants and behaviour
Variants: dark with the display title and a visual; light with an H1 and no visual. The line under the buttons holds a short proof (`.hero_note`). Variant "Works in" (social.plus addition, 12 October 2026, not in the library; the second hero in source.html; `../../../feedback.md` item 5): for a product that works inside AI tools (Agentry, the MCP server), no visual, and under the buttons the "Works in" block (`.hero_works`), the live site's pattern: the label "Works in" centred between two fading hairlines, then one link per tool, the approved icon from `assets/third-party/ai-tools/` in a 40px tile with the name beside it, then "+ Any MCP-compatible tool" (or the product's own wording). Only tools the product supports today (`messaging/product-capabilities.md`); never a lettered or redrawn icon, never names alone when an approved icon exists.

## Rules
- A framed section sits on the frame: framed sections only on that page, never a captured section and never a captured section wrapped in the frame (Grid and frame section).
- Keep the structure and inner layout as source.html shows it; change only the content. Inside the frame there are cells divided by lines, no floating cards.
- Colours, type and spacing come from the role, type-scale and layout tokens (`framed.css` and the design system's tokens); in a Webflow build write their values (none is a Webflow variable yet).
- Text stays on the type scale; eyebrows in Geist Mono; one primary button per section.

## Accessibility and mobile
- Headings in order (one `<h1>` per page, in the hero); frame lines, markers and hatched bands are decorative.
- Cells collapse to two columns under 992px and one under 480px; splits stack with a frame line between. Rendered at 390px: no sideways scroll.
