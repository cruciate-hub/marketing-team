# F06 · Feature tabs (framed)

- Status: approved (2026-10-12), from Amadeus's web library (v0.1, decision 8 October 2026); not yet in Webflow · Owner: Amadeus · Approved by: Stefan, 12 October 2026
- Source: the web library's page demo (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), read 12 October 2026; Webflow name in the library: "Section / Feature Tabs"
- Code: source.html (links `../../../tokens.css` and `../framed.css`) · Screenshot: none yet (render source.html)
- Captured section it replaces on a framed page: 17 Accordion with image

Several features sharing one visual: tabs in columns 1 to 4 with a description for the active one; the visual cross-fades in columns 5 to 12.

## Use it when
Three to six features or use cases that are best shown one at a time ("Every team's question").

## Variants and behaviour
Click or the arrow keys switch the tab (script); the preview shows the first tab open.

## Rules
- A framed section sits on the frame: framed sections only on that page, never a captured section and never a captured section wrapped in the frame (Grid and frame section).
- Keep the structure and inner layout as source.html shows it; change only the content. Inside the frame there are cells divided by lines, no floating cards.
- Colours, type and spacing come from the role, type-scale and layout tokens (`framed.css` and the design system's tokens); in a Webflow build write their values (none is a Webflow variable yet).
- Text stays on the type scale; eyebrows in Geist Mono; one primary button per section.

- No line between the tabs (only the frame line on the right of the list). Tab icons are grey (`--color-text-muted`); the active tab's icon is link blue (`--color-link`), with the blue bar on the frame. Decision: Stefan, 12 October 2026 (`../../../feedback.md` item 9).
- Each panel shows a mockup built from the library's mockup parts (chat, app screen, stats), labelled "Illustrative example" when the numbers are made up. Never an empty image box where a mockup can show the feature.
- For an AI product (Agentry, the MCP server, Vise) each panel is the AI chat mockup (`.mk_ai` in `../framed.css`): the assistant's mark and name, the question as a blue bubble on the right, the answer as a card on the left with one visual (numbers, table, bars, rows or topics), a follow-up input below. Rises in success green, bars in one colour (`../../feedback.md` item 16). Each time a tab becomes active the chat plays once: the question slides in, Agentry "types" for half a second, the answer builds up (numbers and rows one by one, bars grow); off with reduced motion.

## Accessibility and mobile
- Headings in order (one `<h1>` per page, in the hero); frame lines, markers and hatched bands are decorative.
- Cells collapse to two columns under 992px and one under 480px; splits stack with a frame line between. Rendered at 390px: no sideways scroll.
