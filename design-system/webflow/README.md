# Framed pages in Webflow

How a framed page (built from `../sections/framed/`) goes into Webflow. First used for the Agentry page on 12 October 2026: draft page "✨ Agentry · framed (draft, Claude)", `/ai/agentry-framed`, not published.

- Status: in use since 12 October 2026 · Owner: Stefan
- The page stays a draft until Stefan or Amadeus publishes it. Claude never publishes.

## How it is built

1. **Source.** The approved page from Claude Design (its canvas markup), with every state written in (first tab active, first FAQ answer open).
2. **Convert.** `python3 framed-to-webflow.py <page.html> <out>` (needs `tinycss2`). It reads `../sections/framed/framed.css` and `../tokens.css` and:
   - prefixes every class with `fr-` (the live site already has `.button`, `.button-group` and others; the prefix keeps the framed styles from touching live pages);
   - writes every token as its value (definition of done point 4: no `var(--…)` in Webflow);
   - splits the rules: one-class and combo-class rules (with `:hover`, `:focus`, `:active` and the 991, 767 and 479 breakpoints) become Webflow classes, editable in the Designer; everything Webflow classes cannot hold (descendant and attribute selectors, `::before`/`::after` such as the frame markers, `:focus-visible`, other media queries, local custom properties such as `--cells`) goes into `head.css`;
   - gives every class at least one rule, because the Webflow builder drops a class that has none.
3. **Insert.** Each section's `{html, css}` goes in with the Webflow MCP `data_whtml_builder`, into one `fr-page` wrapper: navigation, `<main class="fr-main">` with the sections, footer. Images that are site assets (the logo) are linked to the asset afterwards (`set_image_asset`).
4. **Head code.** `head.css` goes into the page's own head code (page settings), never the site's.
5. **Script.** `framed-page.js` (tabs with arrow keys, FAQ open and close, keyboard access, placeholder links) is registered once on the site and applied to the page only.
6. **Fonts.** Figtree and Geist Mono are custom fonts on the site (Geist Mono uploaded 12 October 2026 from `../geist-mono.woff2`).
7. **Check.** Render the converted page locally at 1440 and 390 and compare it with the Claude Design page; then open the draft in the Designer and preview it.

## Known limits

- In Webflow, `<button>` becomes a link block; the script gives tabs and FAQ triggers keyboard focus and Enter/Space.
- The rules in the head code show on the published page and in Preview, not on the Designer canvas (frame markers, tab and FAQ states, hover details).
- The framed navigation's menus have no panels yet (the canvas has none either); a page that goes live needs them or the live navigation's menus.
- The newsletter form becomes a Webflow form; before publishing, connect it to the same endpoint as the live footer.
- Not yet Webflow components: once the sections are approved in Webflow, turn each into a component ("Framed / …") so the next page reuses them.
