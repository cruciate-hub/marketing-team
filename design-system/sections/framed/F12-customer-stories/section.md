# F12 · Customer stories (framed)

- Status: approved (2026-10-12), from Amadeus's web library (v0.1, decision 8 October 2026); Webflow: see "Webflow note" (checked 19 Nov 2026) · Owner: Amadeus · Approved by: Stefan, 12 October 2026
- Source: the web library's page demo (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), read 12 October 2026; Webflow name in the library: "Section / Customer Stories"
- Code: source.html (links `../../../tokens.css` and `../framed.css`) · Screenshot: none yet (render source.html)
- Captured section it replaces on a framed page: 19 Customer story strip

Story cards bound to the customer story CMS.

## Use it when
Proof near the end of a product or industry page.

## Variants and behaviour
Grid: three cards in frame cells. Gallery: photo tiles, the hovered story widens (swipe on phones). Photos are the library's placeholders.

## Rules
- Use the tile as is (feedback 56): logo size and the hover widening come from `framed.css`; a page never restyles `.story-tile*` or `.uc_logo` (no fixed logo height, no white filter, no photo brightening, no extra "Read the story" line).
- A framed section sits on the frame: framed sections only on that page, never a captured section and never a captured section wrapped in the frame (Grid and frame section).
- Keep the structure and inner layout as source.html shows it; change only the content. Inside the frame there are cells divided by lines, no floating cards.
- Colours, type and spacing come from the role, type-scale and layout tokens (`framed.css` and the design system's tokens); in a Webflow build use the site's variables and classes (Webflow is king); a value with no Webflow equivalent is raised as a drift, never added on the fly.
- Text stays on the type scale; eyebrows in Geist Mono; one primary button per section.

## Accessibility and mobile
- Headings in order (one `<h1>` per page, in the hero); frame lines, markers and hatched bands are decorative.
- Cells collapse to two columns under 992px and one under 480px; splits stack with a frame line between. Rendered at 390px: no sideways scroll.

## Webflow note
- Checked 19 Nov 2026 (read-only, `query_components`, then built). Component `Section / Customer Stories Framed` (new 19 Nov 2026, duplicated from `Section / Customer Stories` to keep the CMS list): `section padding_Y background-color_dark border-top c-framed` (`#section-cs-stories`) > `page-padding` > `container-large c-framed` with four `frame-marker`s > `pricing-header is-stacked` (eyebrow `pricing-eyebrow`, plain `h2` with `max-CH-23`, lead `pricing-header_lead is-below`) > `CC / Customer Stories Section` + `cs-cta c-pricing` list; its own `<style>` embed sets the active tile 4:1, 16px radius, logos at the top and the "Read the story" line. Used on /pricing-conversational. The unframed `Section / Customer Stories` (12 instances) stays for current-look pages.
