# F21 · Comparison table (framed)

- Status: approved (2026-10-12), from Amadeus's web library (v0.1, decision 8 October 2026); not yet in Webflow · Owner: Amadeus · Approved by: Stefan, 12 October 2026
- Source: the web library (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), its "Comparison table" section, read 12 October 2026; Webflow name in the library: "Section / Comparison"
- Code: source.html (links `../../../tokens.css` and `../framed.css`) · Screenshot: none yet (render source.html)
- Captured section it replaces on a framed page: 52 vs / Comparison table

A feature-by-feature comparison as a real table on the frame: the feature column in columns 1 to 6, the products share 7 to 12, the social.plus column highlighted, rows grouped by category.

## Use it when
/vs/ pages and any page that compares social.plus with alternatives.

## Variants and behaviour
Variants: dark, social.plus against one competitor; light, against two. Cells: included, not included, partial or a short text. On phones the table scrolls sideways in its own box with the feature column fixed (`contain: paint`, a social.plus addition). Competitor facts need a source; social.plus facts come from `messaging/product-capabilities.md`.

## Rules
- A framed section sits on the frame: framed sections only on that page, never a captured section and never a captured section wrapped in the frame (Grid and frame section).
- Keep the structure and inner layout as source.html shows it; change only the content. Inside the frame there are cells divided by lines, no floating cards.
- Colours, type and spacing come from the role, type-scale and layout tokens (`framed.css` and the design system's tokens); in a Webflow build write their values (none is a Webflow variable yet).
- Text stays on the type scale; eyebrows in Geist Mono; one primary button per section. Dark is the default; the light variant only where the page is light (legal pages).

## Accessibility and mobile
- Headings in order (one `<h1>` per page, in the hero or page header); frame lines, markers and hatched bands are decorative.
- Cells collapse to two columns under 992px and one under 480px; splits stack with a frame line between. Rendered at 390px: no sideways scroll.
