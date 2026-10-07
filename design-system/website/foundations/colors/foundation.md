# Colors

The 44 live Webflow variables (General and Typography collections) as swatches with name, value and use. The page is dark-first: `--social--dark` #111 is the page background and `--social--main-blue` #3B41EC is the only action colour.

- Status: draft (2026-10-07), as-is: current live values, no team decision applied · Owner: Stefan · Approved by: TO CHECK (Amadeus)
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
- 17 deleted Webflow variables are still emitted and referenced by 27 live rules; the capture rewrites them to live equivalents (`deletedVariableMap` in capture.config.json) and tokens.css leaves them out
- Unused or single-use tokens: `--text--text-color-grey-muted` (no rule), grey-lighter, grey-mid, `--social--dark-pill` (one rule each)
- `--text--text-color-grey-medium` #717275 on #111 is 3.9:1, below 4.5:1; used on 114 pages (nav, footer)
- No light-surface pair, no radius or shadow tokens (radii in use: .5rem, 1rem, .75rem, .25rem, 1.5rem, 16px, 12px, pill 999px/99rem/100rem/20rem; the recurring shadow is `0 16px 2rem #12141914`)
- `--main--transparant` is spelled with an "a" on the site
