# Cards

The four card styles as they are today (v1, v2, v3, plain), the thumbnail card of every listing and the customer story card.

- Status: draft (2026-10-07), as-is: current live values, no team decision applied · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/styleguide (card-v1) and live cards from /social/uikit (card-v1), /industry/gaming (card-v2, card-plain), /use-case/1-1-chat (card-v3), the release-note template (card-v3 docs), /blog (thumbnail), /chat (story card)
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`)

## Values as measured (1440; phone value in brackets)
| Card | Box | Heading | Body | Pages / uses | Webflow component |
|---|---|---|---|---|---|
| `.card-v1` | 1px `--border--border-dark`, radial gradient `--social--grey` 55% to `--social--dark-gray-background`, radius 8px, padding 40px (24px); `.c-outline` transparent, `.c-centered`, `.c-link` hover lifts 2px | h3 `.h5-font-size` 20px/600 white, icon `.card-icon-v1` 48px blue circle | `.text-size-small` 16px/1.4 | 15 / 70 | Card / v1 (31) |
| `.card-v2` | #1a1a1a, no border, radius 8px, padding 16px | 20px/600; icon 72px | 16px #b3b3b3 | 10 / 80 | Card / v2 (80) |
| `.card-v3` | #1a1a1a, no border, radius 8px, padding 32px | 28px/600 | – | 7 / 27 | none |
| `.card-plain` | #1a1a1a, no border, radius 8px, padding 32px | 20px/600 | 16px | 11 / 43 | Cards / Plain (43) |
| Thumbnail card | image wrapper radius 16px; tags above the title | 28px/600 | author row, date | every listing | none (CMS lists) |
| Story card `.cs-cta_link-block` | photo, dark gradient overlay, logo | story title | – | 23 pages | Section / Customer Stories, CC / Customer Stories Section |

## Known inconsistencies (as-is, no decision applied)
- Four paddings (40 / 16 / 32 / 32px), two border treatments, two heading sizes (20 vs 28px). The audit proposes one card with three variants: bordered (v1), icon-compact (v2 and v3 merged), plain. Audit open question 4
- `Card / Button` exists as a Webflow component (4 instances) but no live page renders it
- card-v3 has no Webflow component (27 uses); the thumbnail card has none either
- Card radius .5rem (v1 to plain) next to 1rem on thumbnails and rich-text images
