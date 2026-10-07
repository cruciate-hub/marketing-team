# Shadows and radius

The border radii and shadows the live site uses, with rule counts from the 7 October 2026 audit of the two Webflow stylesheets, and the reduced set the audit proposes. Neither has a token today; the proposal waits for the team's decision.

- Status: draft (2026-10-07), as-is: values as the stylesheet has them, no team decision applied; replaces the former `design-system/shadows.md` and `border-radius.md` · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: the audit (`2026-10-07-audit-report.md`, section 2.6, with `raw/css-values.json`) and the captured sections' CSS
- Preview: preview.html (hand-made, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Not produced by capture/: the preview is written by hand and survives re-runs

## Border radius as measured (55 distinct values in the stylesheet)

| Value | Rules | Where |
|---|---|---|
| `.25rem` 4px | 33 | custom checkbox, announcement bar, blog share box, `.input-field` (4px), `.tag.c-nav-webinar`; the form error box |
| `.36rem` | 3 | `.tag`, `.blog-tag`, `.pu-tag` (the blog grid overrides it to 2px) |
| `.5rem` 8px | 65 | cards v1, v2, v3 and plain, `.card-icon-v2`, AWS logo box, AI page cards, pop-up triggers |
| `.75rem` 12px | 40 | accordion image wrapper, story thumbnails, consultation CTA, careers and gallery cards, `.block` |
| `1rem` 16px | 52 | image ratio classes, thumbnails, forms, pop-ups, answers image, rich-text images in product updates |
| `1.5rem` 24px | 11 | rich-text images (`.rich-text`), hero tag, `.image_radius-parent`, slider |
| `10em` / `25em` | 2 / 2 | `.cta-button` outer and `.cta-button_bg` inner (primary and secondary buttons) |
| `999px`, `99rem`, `100rem`, `20rem`, `25rem`, `10rem` | 20 | nav links, `.card-icon-v1`, filter tags, `.button` submit, rounded inputs, `.tag.c-new`: six ways to write "pill" |
| `50%` / `100%` | 18 / 7 | avatars, author images, the button arrow circle, dots |
| other | 31 | one or two rules each (`.375rem`, `.85rem`, `1.25rem`, `2rem`, `12px`, `16px`, `20px`, mixed corners such as `0 1.5rem 1.5rem` on blog images) |

## Shadows as measured (24 values, none a token)

| Value | Rules | Where |
|---|---|---|
| `0 16px 2rem #12141914` | 10 | the card shadow: AWS logo box, hero tag, news featured, SDK language card, pop-up content, testimonial link, video lightbox hover |
| `0 16px 2rem #12141929` | 5 | the same shadow at 16%: forms, hover state of the cards above |
| `0 8px 2rem #12141929` | 2 | hover of the pop-up trigger and the testimonial link |
| `0 0 1rem #12141929` | 1 | pricing tooltip |
| `0 -24px 50px #00000073` | 1 | mobile nav sheet (upwards) |
| `0 16px 40px -20px #3b41ec73` | 3 | blue glow on the AI pages (code block, folder, term) |
| `0 0 24px #3b41ec2e` | 1 | blue glow on the /vs/ comparison highlight card |
| `0 0 40px #3b41ec1a` | 1 | blue glow on the AI page "ours" column |
| `0 0 .1875rem #3b41ec80` | 1 | text field focus ring (see the accessibility foundation) |
| Webflow and AI-page one-offs | 9 | `#3898ec` checkbox focus, `#e76043` swiper, `vise-*` and `vcmp-*` panels, the Webflow badge |

## Depth on dark pages

Depth comes from lighter surfaces, not from shadows: page `--social--dark` #111, nav `--secondary--menu-bg` #181818, raised block `--social--dark-gray-background` #1a1a1a (cards v2, v3, plain; secondary button fill), panel `--social--grey` #222 (card-v1 gradient start, product tiles), icon holder #2b2b2b (not a token), chip `--social--light-grey` #444. Same-colour layers are separated by `--border--border-dark` #232324 or `--border--border-hover` #39393a. The card shadow is for light tiles (forms, logo boxes, pop-ups) where a border would look heavy. A glow is interactive feedback or a single highlight, never a resting state on every card.

## Proposed set (to decide: Stefan or Amadeus)

From the audit, open question 9 ("add radius and shadow tokens"):

| Token (proposed) | Value | Replaces |
|---|---|---|
| radius small | 8px | `.5rem`; also the 4px and 12px uses, unless the team keeps 4px for inputs and checkboxes |
| radius medium | 16px | `1rem`, `12px`, `16px` |
| radius large | 24px | `1.5rem`, `1.25rem`, `2rem` |
| radius pill | `100rem` | `10em`, `25em`, `999px`, `99rem`, `100rem`, `20rem`, `25rem`, `10rem` |
| radius circle | `50%` | `100%`, `999rem` |
| shadow card | `0 16px 2rem #12141914` (hover `#12141929`) | the four `#121419` variants |
| shadow glow | `0 0 24px #3b41ec2e` | the three blue glows |

The former `shadows.md` scale (`--shadow-sm` to `--shadow-xl`, light and dark values, eight z-index layers) and the former `border-radius.md` nine-step scale were not on the site; the values above are what the site has. Until the team decides, use the measured value of the section you are building from, and the proposed set for anything new.

## Known inconsistencies (as-is, no decision applied)
- Four radii on one card family (8px cards, 16px thumbnails, 24px rich-text images, pill icons) and six spellings of "pill"
- The card shadow sits on dark cards on some pages where it is invisible (SDK language card)
- Blog images mix corner radii (`0 1.5rem 1.5rem`: square top-left corner)
- Buttons use `10em` and `25em` where every other pill uses a rem or px value
