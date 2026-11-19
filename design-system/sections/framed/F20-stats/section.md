# F20 · Stats (framed)

- Status: approved (2026-10-12), from Amadeus's web library (v0.1, decision 8 October 2026); Webflow: see "Webflow note" (checked 19 Nov 2026) · Owner: Amadeus · Approved by: Stefan, 12 October 2026
- Source: the web library (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), its "Stats" section, read 12 October 2026; Webflow name in the library: "Section / Stats"
- Code: source.html (links `../../../tokens.css` and `../framed.css`) · Screenshot: none yet (render source.html)
- Captured section it replaces on a framed page: 25 Numbers band

Headline numbers in frame cells, each with a short label, and a source line under them.

## Use it when
Proof in numbers between feature sections.

## Variants and behaviour
Variants: dark with a split header and four numbers; light, three numbers, no header. The numbers in the preview are placeholders: real numbers come from `messaging/evidence-bank.md` with their source line, never invented (taste rule 11).

## Rules
- A framed section sits on the frame: framed sections only on that page, never a captured section and never a captured section wrapped in the frame (Grid and frame section).
- Keep the structure and inner layout as source.html shows it; change only the content. Inside the frame there are cells divided by lines, no floating cards.
- Colours, type and spacing come from the role, type-scale and layout tokens (`framed.css` and the design system's tokens); in a Webflow build use the site's variables and classes (Webflow is king); a value with no Webflow equivalent is raised as a drift, never added on the fly.
- Text stays on the type scale; eyebrows in Geist Mono; one primary button per section. Dark is the default; the light variant only where the page is light (legal pages).

## Accessibility and mobile
- Headings in order (one `<h1>` per page, in the hero or page header); frame lines, markers and hatched bands are decorative.
- Cells collapse to two columns under 992px and one under 480px; splits stack with a frame line between. Rendered at 390px: no sideways scroll.

## Webflow note
- Checked 19 Nov 2026 (read-only, `query_components`). No component. Closest existing: the home-page numbers band (own embed). Framed build: `section padding_Y background-color_dark border-top c-framed` > `page-padding` > `container-large c-framed` (with `frame-marker` divs) > cells as `grid-4 c-framed` / `grid-3 c-framed` > `card-v1 c-cell` (`c-clickable` when the cell is a link).
