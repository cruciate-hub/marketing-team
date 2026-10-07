# Colors

The 44 live Webflow variables (General and Typography collections) as swatches with name, value and use. The page is dark-first: `--social--dark` #111 is the page background and `--social--main-blue` #3B41EC is the only action colour.

- Status: draft (2026-10-07), as-is: current live values, no team decision applied; the brand extras at the end come from the former `colors-usage.md` and `website.md` · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/styleguide and the `:root` block of the live stylesheet (tokens.css, tokens.json)
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`)

## Values as measured
- Surfaces: `--social--dark` #111 (page), `--social--dark-gray-background` #1a1a1a (cards v2/v3/plain, secondary button fill), `--social--grey` #222 (card-v1 gradient start), `--secondary--menu-bg` #181818 (nav), `--social--dark-card` #161616, `--social--light-grey` #444, `--social--dark-pill` #2e2e2e; light: `--social--grey-background` #f9f9f9, `--main--whitesmoke`, `--main--white`
- Blue: `--social--main-blue` #3b41ec (buttons, tags, icons; 82 rules, every page embed), `--social--button-hover` #272b9d, `--social--button-pressed` #27265e, `--social--blue-transparent` #2a31e91a; gradient stops `--gradient--light-blue` #45a5ed, `--gradient--medium-blue` #3769ec, `--gradient--dark-blue` = main blue
- Text: white, `--text--text-color-grey-light` #b3b3b3 (body), `--text--text-color-grey-medium` #717275 (muted), `--text--text-color-grey-dark` #414347 and `--text--text-color-dark` #111 (on light); rarely used: grey-lighter #d1d1d1, grey-mid #a4a4a4, grey-muted #929292
- Borders: `--border--border-dark` #232324 (dividers, card borders), `--border--border-hover` #39393a, `--border--border-dark-grey` #666 (secondary button outline), light: `--border--border-med-grey` #d0d0d1, `--border--border-light-grey` #e7e7e7
- Secondary accents (decoration and status, never CTAs): green #1dc497, yellow #f7c506, red #ff305a, orange #ff6937, purple #9f72ff, pink #f568f0

## Known inconsistencies (as-is, no decision applied)
- Two blues: `--social--main-blue` #3b41ec (buttons, tags, icons) and `--gradient--medium-blue` #3769ec (links, superscripts). Page embeds add #6b9fff, #5c6ef8, #2f6bed, #3b82f6, #7b94fe. Open question 3 of the audit
- 192 of 224 colour values in the stylesheets are not a token; the ones regular sections depend on are listed at the bottom of the preview (#141414 radial gradient, #1b1b1b inputs, #dc3545 form errors, #3ccb7f/#093a20 `.tag.c-new`, #14152c industry hero)
- Token values typed as hex in rules (#111 ×14, #222 ×11, #1a1a1a ×8 …), so a token change would not reach them
- 17 deleted Webflow variables are still emitted; 13 of them are referenced by 27 live rules; the capture rewrites them to live equivalents (`deletedVariableMap` in capture.config.json) and tokens.css leaves them out
- Unused or single-use tokens: `--text--text-color-grey-muted` (no rule), grey-lighter, grey-mid, `--social--dark-pill` (one rule each)
- `--text--text-color-grey-medium` #717275 on #111 is 3.9:1, below 4.5:1; used on 114 pages (nav, footer)
- No light-surface pair, no radius or shadow tokens (radii in use: .5rem, 1rem, .75rem, .25rem, 1.5rem, 16px, 12px, pill 999px/99rem/100rem/20rem; the recurring shadow is `0 16px 2rem #12141914`)
- `--main--transparant` is spelled with an "a" on the site
- The site has one blue gradient on text: `linear-gradient(145deg, var(--gradient--light-blue), var(--gradient--dark-blue))` as a `background-clip: text` fill on superscripts (sections 42 and 60), next to the `h1` radial fill (typography foundation). Neither is a licence: see "No gradient on text" below

## Brand extras (emails, social graphics): not website tokens, clearly separate

Things emails and social graphics need that `tokens.css` does not define. They are not Webflow variables; on a web page use the tokens above.

- **Gradients as the site has them** (the captured CSS; use these, as CSS, for graphics and emails):
  - Site blue gradient: `linear-gradient(145deg, var(--gradient--light-blue), var(--gradient--dark-blue))` = `linear-gradient(145deg, #45a5ed, #3b41ec)`. Two stops; on the site it is a text fill on superscripts (a known inconsistency, above); for graphics use it as a background or a shape
  - Button fill: `linear-gradient(90deg, var(--social--main-blue), var(--social--button-hover))` = `#3b41ec` to `#272b9d` (every primary button)
  - Avatar ring: `linear-gradient(#f7c506, #f568f0 50%, #3b41ec)` (yellow to pink to main blue, top to bottom; thumbnail grid 30, featured item 31, article 40)
  - Logo mark, blue arm: `#3769ec` at 9.7%, `#3b41ec` at 46.9%, `#45a5ed` at 91% (artwork, from the SVG; not a CSS gradient on the site)
- **Warm gradient** (decoration and the logo mark only, never CTAs): `linear-gradient(to right, #f568f0, #ff6937, #f7c506)` = `--secondary--pink` to `--secondary--orange` to `--secondary--yellow` (the former "Brand Pink" with the token orange; the logo mark's own warm stop is #f66005, artwork, not a token). The 11 named gradients of the former `colors-usage.md` (Brand Blue, Solar, Brand Pink, Airy, Depth, Authority, Vibrant, Ember, Prestige, Gold, Energy) are retired: none is on the site
- **No gradient on text**: a gradient is a background or a shape; text stays one solid colour. The live `h1` radial text fill is a known inconsistency (typography foundation), not a licence
- **Light-mode email palette** (MailerLite emails render on white; the full spec is `emails/product-update-newsletter-spec.md`, which also sets the email font, Inter): page background `--main--whitesmoke` #f5f5f5, content `--main--white`, alternate sections `--social--grey-background` #f9f9f9; text `--text--text-color-dark` #111 headings, `--text--text-color-grey-dark` #414347 body, `--text--text-color-grey-medium` #717275 small text on white only (on the #f5f5f5 page background it is 4.41:1 and fails body text: use #414347 there, or keep #717275 for 19px bold and larger); `--text--text-color-grey-light` #b3b3b3 for the footer separator (decorative); borders `--border--border-light-grey` #e7e7e7; button `--social--main-blue` #3b41ec with white label, hover `--social--button-hover` #272b9d; outlined button text #3b41ec on white (6.66:1). The client dark-mode palette (`prefers-color-scheme: dark`: #1a1a1a = `--social--dark-gray-background`, #2d2d2d, #7b7fff links, #a0a0a3 secondary, #f0f0f0, #e0e0e0, #555555) and the email-only values (module badge pairs, social icon colours) are owned by the spec, not by this foundation
- **Blue text on dark**: `--social--main-blue` fails as a text colour on #111 (2.84:1). Page embeds and three AI-page rules on the site use #7b94fe (6.75:1) for that; it is not a token (TO CHECK: add it, or always use white text with a blue fill). The rule until then is in `brain.md`: links and icons on dark are white, or #7b94fe
- **Status colours** are the secondary tokens: green #1dc497 success, yellow #f7c506 warning (dark text on it), red #ff305a error (text on dark; white on red only for large text), `--gradient--light-blue` #45a5ed info (as the former palette had it). Light-mode variants of the former extended palette (#cc9202, #1b89dc, #f66005) are not on the site and are not used
