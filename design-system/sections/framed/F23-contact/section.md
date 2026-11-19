# F23 · Contact form (framed)

- Status: approved (2026-10-12), from Amadeus's web library (v0.1, decision 8 October 2026); Webflow: see "Webflow note" (checked 19 Nov 2026) · Owner: Amadeus · Approved by: Stefan, 12 October 2026
- Source: the web library (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), its "Contact form" section, read 12 October 2026; Webflow name in the library: "Section / Contact"
- Code: source.html (links `../../../tokens.css` and `../framed.css`) · Screenshot: none yet (render source.html)
- Captured section it replaces on a framed page: 24 Form section, 53 vs / Customer stories + form (the form part)

The contact or demo form beside the reasons to talk: text and three reasons in columns 1 to 5, the form in 7 to 12.

## Use it when
The contact-sales page and the conversion point of a /vs/ page.

## Variants and behaviour
Variants: dark and light. The form is static here; in Webflow it posts to the existing contact flow. Consent text and privacy link stay as on the live form.

## Rules
- A framed section sits on the frame: framed sections only on that page, never a captured section and never a captured section wrapped in the frame (Grid and frame section).
- Keep the structure and inner layout as source.html shows it; change only the content. Inside the frame there are cells divided by lines, no floating cards.
- Colours, type and spacing come from the role, type-scale and layout tokens (`framed.css` and the design system's tokens); in a Webflow build use the site's variables and classes (Webflow is king); a value with no Webflow equivalent is raised as a drift, never added on the fly.
- Text stays on the type scale; eyebrows in Geist Mono; one primary button per section. Dark is the default; the light variant only where the page is light (legal pages).

## Accessibility and mobile
- Headings in order (one `<h1>` per page, in the hero or page header); frame lines, markers and hatched bands are decorative.
- Cells collapse to two columns under 992px and one under 480px; splits stack with a frame line between. Rendered at 390px: no sideways scroll.

## Webflow note
- Checked 19 Nov 2026 (read-only, `query_components`). No framed component. Existing forms: `CC / Contact Form` (9), `CC / Form` (5), `Form Privacy Disclaimer` (12); inputs are the one `input-field` component (Pitfall 123). Copy the live form, never restyle it. Exception: the conversational pricing form (`pricing-chat`, posting to the same Basin endpoint as the live pricing form) on /pricing-conversational, built from the approved pricing board (19 Nov 2026).
