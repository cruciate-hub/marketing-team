# F14 · FAQ (framed)

- Status: draft (2026-10-12), from Amadeus's web library (v0.1, decision 8 October 2026); not yet in Webflow · Owner: Amadeus · Approved by: TO CHECK (Stefan or Amadeus)
- Source: the web library's page demo (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), read 12 October 2026; Webflow name in the library: "Section / FAQ"
- Code: source.html (links `../../../tokens.css` and `../framed.css`) · Screenshot: none yet (render source.html)
- Captured section it replaces on a framed page: 18 FAQ

Questions on the accordion, with FAQPage structured data generated from the same content for search and AI answers.

## Use it when
Every product, landing and pricing page, before the closing CTA.

## Variants and behaviour
The preview shows the questions closed; a question opens on click (script). Answers stay short and factual.

## Rules
- A framed section sits on the frame: framed sections only on that page, never a captured section and never a captured section wrapped in the frame (Grid and frame section).
- Keep the structure and inner layout as source.html shows it; change only the content. Inside the frame there are cells divided by lines, no floating cards.
- Colours, type and spacing come from the role, type-scale and layout tokens (`framed.css` and the design system's tokens); in a Webflow build write their values (none is a Webflow variable yet).
- Text stays on the type scale; eyebrows in Geist Mono; one primary button per section.

## Accessibility and mobile
- Headings in order (one `<h1>` per page, in the hero); frame lines, markers and hatched bands are decorative.
- Cells collapse to two columns under 992px and one under 480px; splits stack with a frame line between. Rendered at 390px: no sideways scroll.
