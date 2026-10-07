# Typography

Figtree (variable font 300 to 900; Inter is loaded but unused). `html` 16px; `body` 1.1rem = 17.6px / 1.6 on `--text--text-color-grey-light`. Heading sizes live on six typography tokens; the preview measures every sample at 1440 and 390 px.

- Status: draft (2026-10-07), as-is: current live values, no team decision applied · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/styleguide (the style guide's own heading, text, weight, alignment and colour samples)
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`)

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
