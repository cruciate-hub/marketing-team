# F22 · Pricing (framed)

- Status: approved (2026-10-12), from Amadeus's web library (v0.1, decision 8 October 2026); not yet in Webflow · Owner: Amadeus · Approved by: Stefan, 12 October 2026
- Source: the web library (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), its "Pricing" section, read 12 October 2026; Webflow name in the library: "Section / Pricing"
- Code: source.html (links `../../../tokens.css` and `../framed.css`) · Screenshot: none yet (render source.html)
- Captured section it replaces on a framed page: 60 Pricing / Plan cards, 62 Pricing / Additional fees (61 Compare table has no framed version yet)

The pricing block: the social.plus Suite with what is included and the add-ons, and the support packages as three cells.

## Use it when
The pricing page.

## Variants and behaviour
Variants: dark, the Suite and add-ons with one primary button; light, the support packages (Standard, Premium, Enterprise). Tiers, prices and features are the library's placeholders until the pricing page's content is confirmed.

## Rules
- A framed section sits on the frame: framed sections only on that page, never a captured section and never a captured section wrapped in the frame (Grid and frame section).
- Keep the structure and inner layout as source.html shows it; change only the content. Inside the frame there are cells divided by lines, no floating cards.
- Colours, type and spacing come from the role, type-scale and layout tokens (`framed.css` and the design system's tokens); in a Webflow build write their values (none is a Webflow variable yet).
- Text stays on the type scale; eyebrows in Geist Mono; one primary button per section. Dark is the default; the light variant only where the page is light (legal pages).

## Accessibility and mobile
- Headings in order (one `<h1>` per page, in the hero or page header); frame lines, markers and hatched bands are decorative.
- Cells collapse to two columns under 992px and one under 480px; splits stack with a frame line between. Rendered at 390px: no sideways scroll.
