# Colors

The colours follow the social.plus web library (decision 8 October 2026, Amadeus): **role tokens** for everything new, in a dark theme (default) and a light theme, built on **scales** of 11 steps per hue. The 36 live Webflow variables are kept under their own names below them, because the captured sections use them; 19 point to the identical scale step, 17 keep their live value until the site is merged. The page is dark-first: `color-bg` (neutral-950 #111) is the page and `color-accent-fill` (blue-600 #3B41EC) is the only action colour.

- Status: draft (2026-10-08). Roles and scales: decision (Amadeus), not yet in Webflow. Live variables: as-is, current live values · Owner: Stefan · Approved by: Amadeus (roles and scales); live variables TO CHECK (Stefan or Amadeus)
- Source: the web library (Foundations > Color: scales, roles, surfaces and layering, legibility fixes); the live variables from https://www.social.plus/styleguide and the `:root` block of the live stylesheet

## Roles (use these)

Components use role names, never scale steps. Every role has a dark and a light value; switch the theme, not the token.

| Role | Dark | Light | Use |
|---|---|---|---|
| `color-bg` | neutral-950 #111111 | #FFFFFF | Page |
| `color-bg-alt` | neutral-900 #1A1A1A | neutral-100 #F5F5F5 | Alternate band |
| `color-surface` | neutral-850 #202022 | neutral-50 #F9F9F9 | Cards, panels |
| `color-surface-raised` | neutral-800 #29292B | #FFFFFF | Menus, hover, inline code |
| `color-border` | neutral-800 | neutral-200 | Hairlines, card outlines (decorative) |
| `color-border-strong` | neutral-750 #343437 | neutral-300 | Control borders, dividers that must show (TO CHECK: below 3:1, see Accessibility) |
| `color-text` | #FFFFFF | neutral-950 | Headings, primary text |
| `color-text-muted` | neutral-400 #B3B3B3 | neutral-700 #414347 | Body and secondary text |
| `color-text-subtle` | neutral-500 #939497 | neutral-600 #666666 | Captions, meta, placeholders |
| `color-link` | blue-400 #6F89FC | blue-600 #3B41EC | Links, eyebrows, link-coloured icons |
| `color-focus` | blue-400 | blue-600 | Focus ring, focused input border |
| `color-error` | red-300 #FC9198 | red-600 #B70E39 | Error text and border |
| `color-frame`, `color-frame-marker` | neutral-850 #202022, neutral-500 | neutral-200, neutral-400 | The frame lines and plus markers (web library layout). Dark lines one step quieter since 22 October 2026 (was neutral-800) |
| `color-accent-fill` (`-hover`, `-press`) | `primary` blue-600 (blue-700, blue-800) | same | Primary button and blue fills |
| `color-on-accent` | `on-primary` #FFFFFF | same | Text and icons on the blue fill |

## Surfaces and layering

Depth comes from tonal layers, not shadows. Each layer is one step apart (page, alternate band, surface, raised), and a border sits one step above the layer it outlines.

## Scales

Eleven steps per hue (50 to 950); neutral has two extra dark steps, 750 and 850, for layering dark surfaces. Brand colours are fixed on their step; the other steps are generated so each step has a similar lightness across hues. Text rule: on light backgrounds use step 600 or darker (yellow 700); on dark backgrounds 400 or lighter.

| Hue | Brand step | Live variable on that step |
|---|---|---|
| neutral | (none) | 950 `social--dark`, 900 `social--dark-gray-background`, 400 `text--text-color-grey-light`, 700 `text--text-color-grey-dark`, 600 `border--border-dark-grey`, 300 `border--border-med-grey`, 200 `border--border-light-grey`, 100 `main--whitesmoke`, 50 `social--grey-background` |
| blue | 600 #3B41EC | `social--main-blue` (`primary`) |
| green | 300 #1DC497 | `secondary--green` |
| yellow | 400 #F7C506 | `secondary--yellow` |
| red | 400 #FF305A | `secondary--red` |
| orange | 400 #FF6937 | `secondary--orange` |
| purple | 400 #9F72FF | `secondary--purple` |
| pink | 300 #F568F0 | `secondary--pink` |

Gradient stops `gradient-light-blue` #45A5ED and `gradient-medium-blue` #3769EC are kept (the same values as the live gradient variables).

## Legibility fixes (live pairs that fail, and their new step)

| Live today | Ratio | New | Ratio |
|---|---|---|---|
| Brand blue as a link on dark (`social--main-blue` on #111) | 2.84:1 | `color-link` blue-400 #6F89FC | 5.99:1 |
| `gradient--medium-blue` #3769EC for links and eyebrows on dark | 3.95:1 | `color-link` blue-400 | 5.99:1 |
| Subtle grey on dark (`text--text-color-grey-medium` #717275 on #111) | 3.93:1 | `color-text-subtle` neutral-500 #939497 | 6.23:1 |
| Subtle grey on light grey (#717275 on #F5F5F5) | 4.41:1 | `color-text-subtle` (light) neutral-600 #666666 | 5.27:1 |
| Green text on white (#1DC497) | 2.24:1 | green-600 #0D7055 | 6.1:1 |

## Live Webflow variables and their replacement

Kept for the captured sections; new work uses the roles. Same value as a step (19, now aliases of it): see the Scales table, plus `gradient--light-blue` and `gradient--medium-blue` (= the gradient stops). Different value (keep until the merge, then replace):

| Live variable | Live value | Replace with |
|---|---|---|
| `text--text-color-grey-medium` | #717275 | `color-text-subtle` (neutral-500 #939497) |
| `social--grey` | #222 | `color-surface` (neutral-850 #202022) |
| `border--border-dark` | #232324 | `color-border` (neutral-800 #29292B) |
| `border--border-hover` | #39393a | `color-border-strong` (neutral-750 #343437) |
| `social--button-hover` | #272b9d | `color-accent-fill-hover` (blue-700 #3235CF) |
| `social--button-pressed` | #27265e | `color-accent-fill-press` (blue-800 #282BAD) |
| `text--text-color-grey-lighter` | #d1d1d1 | neutral-300 #D0D0D1 |
| `text--text-color-grey-muted` | #929292 | neutral-500 #939497 |
| `text--text-color-grey-mid` | #a4a4a4 | no step: neutral-400 or neutral-500 |
| `secondary--menu-bg` | #181818 | no step: nearest neutral-900 (TO CHECK) |
| `social--dark-card` | #161616 | no step: nearest neutral-900 (TO CHECK) |
| `social--dark-pill` | #2e2e2e | no step: nearest neutral-800 (TO CHECK) |
| `social--light-grey` | #444 | no step: nearest neutral-700 (TO CHECK) |

`main--white` (#FFFFFF), `main--transparant`, `social--blue-transparent` and `gradient--dark-blue` (an alias of `social--main-blue`) stay as they are.

## Live variables as measured (7 October 2026)
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
- No light-surface pair, no radius or shadow tokens (the design system page holds the measured values as tokens, see shadows-and-radius; radii in use: .5rem, 1rem, .75rem, .25rem, 1.5rem, 16px, 12px, pill 999px/99rem/100rem/20rem; the recurring shadow is `0 16px 2rem #12141914`)
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
- **Blue text on dark**: `--social--main-blue` fails as a text colour on #111 (2.84:1). Decision 8 October 2026: blue text, links, eyebrows and link-coloured icons on dark are `color-link` (blue-400 #6F89FC, 5.99:1 on #111); the #7b94fe some page embeds use (6.75:1) is retired with them
- **Status colours** are the secondary tokens: green #1dc497 success, yellow #f7c506 warning (dark text on it), red #ff305a error (text on dark; white on red only for large text), `--gradient--light-blue` #45a5ed info (as the former palette had it). Light-mode variants of the former extended palette (#cc9202, #1b89dc, #f66005) are not on the site and are not used

## In Webflow (social.plus site)

Every colour in a Webflow class binds to a site variable (collection `General`), never a typed hex. Variables added 30 Oct 2026: `Frame/Frame - Line` #202022, `Frame/Frame - Marker` #939497, `Text/Text Color - Link Blue` #6F89FC, `Border/Border - Tile` #29292B, `Font/Geist Mono`. Prefer an existing variable; add a new one only for a design token that has none.
