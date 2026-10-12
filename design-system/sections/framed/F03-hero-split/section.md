# F03 · Hero / Split (framed)

- Status: approved (2026-10-12), from Amadeus's web library (v0.1, decision 8 October 2026); not yet in Webflow · Owner: Amadeus · Approved by: Stefan, 12 October 2026
- Source: the web library's page demo (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), read 12 October 2026; Webflow name in the library: "Section / Hero"
- Code: source.html (links `../../../tokens.css` and `../framed.css`) · Screenshot: none yet (render source.html)
- Captured section it replaces on a framed page: 01 Hero / Product, 03 Hero / Industry

Text cell and visual cell divided by a frame line on the column 6/7 edge.

## Use it when
Product, feature, industry and solution pages: one product, one promise, one visual.

## Variants and behaviour
Variants: dark with the visual right (default); light with the visual left (reversed); dark 5/7 split for dashboards.

## Rules
- A framed section sits on the frame: framed sections only on that page, never a captured section and never a captured section wrapped in the frame (Grid and frame section).
- Keep the structure and inner layout as source.html shows it; change only the content. Inside the frame there are cells divided by lines, no floating cards.
- Colours, type and spacing come from the role, type-scale and layout tokens (`framed.css` and the design system's tokens); in a Webflow build write their values (none is a Webflow variable yet).
- Text stays on the type scale; eyebrows in Geist Mono; one primary button per section.

## Accessibility and mobile
- Headings in order (one `<h1>` per page, in the hero); frame lines, markers and hatched bands are decorative.
- Cells collapse to two columns under 992px and one under 480px; splits stack with a frame line between. Rendered at 390px: no sideways scroll.
