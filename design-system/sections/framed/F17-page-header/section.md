# F17 · Page header (framed)

- Status: approved (2026-10-12), from Amadeus's web library (v0.1, decision 8 October 2026); not yet in Webflow · Owner: Amadeus · Approved by: Stefan, 12 October 2026
- Source: the web library (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), its "Page header" section, read 12 October 2026; Webflow name in the library: "Section / Page Header"
- Code: source.html (links `../../../tokens.css` and `../framed.css`) · Screenshot: none yet (render source.html)
- Captured section it replaces on a framed page: 04 Article / Title header (and the top of 40 Article, 43 Glossary entry)

Compact opening section for content and listing pages: breadcrumb, H1, lead and one optional extra (category filters, a search field, or article meta).

## Use it when
The top of a blog index, the glossary, an article or answer page, a legal page.

## Variants and behaviour
Variants (all four in source.html): blog with category filters (dark); glossary with search (dark); article with author, date and reading time (light); legal (light, the default in the library). The filter counts and the author are placeholders.

## Rules
- A framed section sits on the frame: framed sections only on that page, never a captured section and never a captured section wrapped in the frame (Grid and frame section).
- Keep the structure and inner layout as source.html shows it; change only the content. Inside the frame there are cells divided by lines, no floating cards.
- Colours, type and spacing come from the role, type-scale and layout tokens (`framed.css` and the design system's tokens); in a Webflow build write their values (none is a Webflow variable yet).
- Text stays on the type scale; eyebrows in Geist Mono; one primary button per section. Dark is the default; the light variant only where the page is light (legal pages).

## Accessibility and mobile
- Headings in order (one `<h1>` per page, in the hero or page header); frame lines, markers and hatched bands are decorative.
- Cells collapse to two columns under 992px and one under 480px; splits stack with a frame line between. Rendered at 390px: no sideways scroll.
