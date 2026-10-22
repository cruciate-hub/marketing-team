# Typography

Two fonts. **Figtree** for everything (`fonts/figtree.woff2`: social.plus's own variable build, weights 300 to 900; Inter is loaded on the live site but unused). The single-storey "a" is already the default glyph, so never load Figtree from Google Fonts, the Webflow CDN or any other source, and never add `font-feature-settings`. The file holds basic Latin only; anything else falls back to Arial, sans-serif (`font-family: "Figtree", Arial, sans-serif`). **Geist Mono** for all-caps eyebrows and all-caps labels only (`fonts/geist-mono.woff2`, variable 100 to 900, SIL Open Font License; stack `"Geist Mono", ui-monospace, SFMono-Regular, Menlo, monospace`, token family `eyebrow`): never for code, captions, body text or anything in sentence case. Code, SDK snippets, API paths and token names use the system monospace (token family `mono`, stack `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`, no web font). Decisions 8 and 16 October 2026 (Amadeus), not yet in Webflow. Emails are the exception: they follow the email spec (`emails/product-update-newsletter-spec.md`, Inter with system fallbacks). `html` 16px. The type scale is the web library's (decision below); the live site's own scale is measured further down.

- Status: draft (2026-10-08): the measured values are as-is; the two-font rule, the type scale, the eyebrow and the code styles are decisions (Amadeus, 8 October 2026; Geist Mono limited to all caps and code moved to the system monospace on 16 October 2026) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/styleguide (the style guide's own heading, text, weight, alignment and colour samples)
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`)

## Decisions (8 October 2026, Amadeus; not yet in Webflow)

- **Type scale**: the web library's. Fluid from a 360px to a 1440px screen (Type scale tokens `fluid-*`); headings weight 600 (the library hero's 700 is not taken).

| Style | 390px | 1440px | Line height | Letter spacing | Live today (1440) |
|---|---|---|---|---|---|
| display | 45px | 80px | 1.05 | -0.025em | (none) |
| h1 | 36.7px | 60px | 1.1 | -0.025em | 52.8px / 1.2 |
| h2 | 30.4px | 46px | 1.1 | -0.015em | 52px / 1.25 |
| h3 | 24.2px | 32px | 1.1 | -0.015em | 36px / 1.25 |
| h4 | 20.1px | 24px | 1.3 | 0 | 28px / 1.25 |
| h5 | 18px | 18px | 1.3 | 0 | 20px / 1.25 |
| (h6) | | | | | 18px: maps to h5 |
| lead | 18.1px | 22px | 1.6 | 0 | enlarged-paragraph 19.2px |
| body | 18px | 18px | 1.6 | 0 | 17.6px |
| small | 16px | 16px | 1.6 | 0 | text-size-small 16px / 1.4 |
| caption | 14px | 14px | 1.6 | 0 | text-size-tiny 14.4px / 1.4 |
| stat-xl | 44.6px | 64px | 1.05 | -0.03em | numbers band (own sizes) |
| stat-lg | 32.2px | 40px | 1.05 | -0.03em | |

  Line lengths: `measure-body` 65ch, `measure-lead` 52ch, `measure-title` 20ch. What it fixes: h1 and h2 are no longer the same size on desktop, the phone sizes no longer differ between tags and classes, and one scale replaces the three "small" sizes.

- **Geist Mono is for all caps only** (decision 16 October 2026, Amadeus; applies to the website, the framed sections and illustrations). It sets the eyebrow and the short all-caps labels that do the eyebrow's job: column headings in the footer and nav panels, table group headers, plan and resource-type labels, the logo-wall caption, the "Works in" label, status badges ("LIVE") and the headers in product mockups. Every such label is uppercase with the eyebrow's letter spacing. Anything that is not all caps is Figtree (captions, chips, pills, notes); code is the system monospace.
- **Eyebrow** (the short label above a heading; Webflow class `.superscript`): Geist Mono 13px (.8125rem), weight 500, UPPERCASE, letter spacing .08em, line height 1rem, colour `color-link` (blue-400 #6F89FC on dark, 5.99:1 on #111; blue-600 on light). Replaces the live Figtree 14px 600, .044rem, #3769EC (3.95:1, fails). Use it only when it adds information: the label is the eyebrow, the claim is the heading. Type style `superscript`.
- **Code**: the system monospace (family `mono`, `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`; not Geist Mono since 16 October 2026). Blocks and SDK snippets `code` (15px / 1.6, 400); API paths and token names `code-small` (13px / 1.6). Captions are `caption` in Figtree. Inline code in running text takes 0.875em of the surrounding size.
- The table below is still what the live site renders; the captured section previews keep showing the live eyebrow until Webflow is updated.

## Values as measured (1440 / 390)
| Item | Size | Line height | Weight | Letter spacing | Colour |
|---|---|---|---|---|---|
| h1 | 52.8px / 36px | 63.4 / 39.6 | 600 | -0.025em | white, radial gradient text fill |
| h2 | 52px / 30.4px | 65 / 33.4 | 600 | -0.025em | white |
| h3 | 36px / 25.6px | 45 / 28.2 | 600 | -0.025em | white |
| h4 | 28px / 22.4px | 35 / 24.6 | 600 | -0.025em | white |
| h5 | 20px / 20px | 25 / 22 | 600 | 0 | white |
| h6 | 18px / 18px | 22.5 / 19.8 | 600 | 0 | white |
| .h1-font-size | 52.8px / 36px | | 600 | -0.025em | inherits grey (only .h2 and .h5 classes set white) |
| .h2-font-size | 52px / 36px | | 600 | | white |
| .h3-font-size | 36px / 30.4px | | 600 | | inherits |
| .h4-font-size | 28px / 25.6px | | 600 | | inherits |
| .h5-font-size | 20px / 22.4px | | 600 | | white |
| .h6-font-size | 18px / 20px | | 600 | | inherits |
| .heading-small | 20px / 18px | 25 / 19.8 | 600 | 0 | white |
| .heading-xsmall | 14.4px | 18 | 600 | 0 | white |
| body, p, li | 17.6px | 28.2 | 400 | 0 | #b3b3b3 |
| .enlarged-paragraph | 19.2px / 17.6px | 30.7 / 28.2 | 400 | | #b3b3b3 |
| .text-size-small | 16px | 22.4 | 400 | | #b3b3b3 |
| .text-size-tiny | 14.4px | 20.2 | 400 | | #b3b3b3 |
| .superscript | 14px | 16 | 600, uppercase | +.044rem | #3769ec |
| a (plain) | 17.6px | 28.2 | 400 | | #3769ec |
| blockquote | 24px / 22.4px | 30 / 28 | 600 | | white |

Weights in use: 400 body, 500 buttons and links, 600 headings, 700 rich-text headings. Text colour classes: `.text-color-dark` #111, `-grey-dark` #414347, `-grey-medium` #717275, `-grey-light` #b3b3b3, `-white`; not on the style guide but used: `.text-color-blue`, `.text-color-grey-4` (101 pages, no grey-4 token), `-green`, `-red`, `-yellow`, `-pink`.

## Known inconsistencies (as-is, no decision applied)
- H1 and H2 are the same size on desktop (52.8 vs 52px): the h1 clamp only passes h2 above 2,520px wide. Audit open question 2
- Mobile sizes differ between tags and classes (h2 30.4 vs .h2-font-size 36; h3 25.6 vs 30.4; h4 22.4 vs 25.6; h5 20 vs 22.4; h6 18 vs 20)
- Page overrides: industry hero title 64px/700, blog title 48px, footer CTA headline 52px, card-v3 and thumbnail headings 28px, FAQ question 19.2px/400
- Three "small" sizes: .heading-xsmall .9rem, .text-size-tiny .9rem, .superscript .875rem; .heading-small duplicates h5
- h1 carries a gradient text fill that every rich-text style has to undo
- 87 font-size values in the CSS next to the six tokens
