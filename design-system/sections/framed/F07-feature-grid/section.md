# F07 · Feature grid (framed)

- Status: approved (2026-10-12), from Amadeus's web library (v0.1, decision 8 October 2026); not yet in Webflow · Owner: Amadeus · Approved by: Stefan, 12 October 2026
- Source: the web library's page demo (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), read 12 October 2026; Webflow name in the library: "Section / Feature Grid"
- Code: source.html (links `../../../tokens.css` and `../framed.css`) · Screenshot: none yet (render source.html)
- Captured section it replaces on a framed page: 12 Feature grid, 13 Card grid / Icon cards, 14 Bordered, 15 Plain

Three, four, six or eight features in frame cells on whole columns, under a section header.

## Use it when
A set of short benefits or features with an icon each ("Your team asks. Your first-party data answers."). Use this, not a card grid, inside the frame.

## Variants and behaviour
Variants: centred header with six features in three columns; split header with three linked features. 3 or 6 cells in thirds, 4 or 8 in quarters, complete rows only. Linked cells end in one tertiary button with an arrow; SDK cards carry two, "Learn more →" and "Docs ↗", as on the live site (feedback 21).

## Rules
- A framed section sits on the frame: framed sections only on that page, never a captured section and never a captured section wrapped in the frame (Grid and frame section).
- Keep the structure and inner layout as source.html shows it; change only the content. Inside the frame there are cells divided by lines, no floating cards.
- Colours, type and spacing come from the role, type-scale and layout tokens (`framed.css` and the design system's tokens); in a Webflow build write their values (none is a Webflow variable yet).
- Text stays on the type scale; eyebrows in Geist Mono; one primary button per section.

## Accessibility and mobile
- Headings in order (one `<h1>` per page, in the hero); frame lines, markers and hatched bands are decorative.
- Cells collapse to two columns under 992px and one under 480px; splits stack with a frame line between. Rendered at 390px: no sideways scroll.

In Webflow (Developer Portal, 31 Oct 2026): linked cells lighten one step on hover and show a focus ring; the cell grid is a list (`role="list"` / `role="listitem"`); the section closes with a full-width bottom rule and bottom + markers.
