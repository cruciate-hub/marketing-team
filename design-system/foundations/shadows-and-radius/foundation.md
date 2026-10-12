# Shadows and radius

The radius set and the one shadow new work uses (web library, decision 8 October 2026, Amadeus; not yet in Webflow), then the border radii and shadows the live site uses, with rule counts from the 7 October 2026 audit of the two Webflow stylesheets.

## Radius and shadow (use these)

Radius grows with the element, so cards, panels and buttons read as different things.

| Token | Value | Use | Replaces (live) |
|---|---|---|---|
| `radius-s` | 8px | Icon tiles, inputs, small controls | `.5rem`; `.25rem` on inputs and checkboxes |
| `radius-m` | 16px | Free-standing cards, thumbnails, images | `1rem`, `.75rem`; cards move up from `.5rem` |
| `radius-l` | 24px | Panels, large visuals | `1.5rem`, `1.25rem`, `2rem` |
| `radius-pill` | 999px | Buttons, badges and tags, tabs, chips | the six pill spellings, `10em`, `25em`; the `.36rem` tag |
| `radius-circle` | 50% | Avatars, dots, round icon holders | `100%`, `999rem` |
| `shadow-float` | `0 12px 32px -8px #0000002e, 0 2px 6px #0000000f` | Floating layers only: menus, dropdowns, popovers, the nav sheet | the card shadows and blue glows (retired for new work) |

Frame cells have no radius: inside the frame, content is divided by lines, not by rounded cards. Depth comes from tonal surfaces (`color-surface`, `color-surface-raised`) and `color-border`, never from a shadow or a glow.

- Status: draft (2026-10-08): the radius set and shadow-float are decisions (Amadeus, 8 October 2026); the measured values are as-is; replaces the former `design-system/shadows.md` and `border-radius.md` · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: rule counts over the two live Webflow stylesheets, measured on 7 October 2026 by the site audit (the counts are reproduced in the tables below), and the captured sections' CSS
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
| `999px`, `99rem`, `100rem`, `20rem`, `25rem`, `10rem` | 26 (7 + 4 + 4 + 6 + 2 + 3) | nav links, `.card-icon-v1`, filter tags, `.button` submit, rounded inputs, `.tag.c-new`: six ways to write "pill" |
| `50%` / `100%` | 18 / 7 | avatars, author images, the button arrow circle, dots |
| `12px`, `16px`, `8px`, `0` | 8, 8, 7, 7 | px spellings on the AI pages (`.vise-*`, `.vcmp-*`, `.jp-*`) and Webflow defaults; `0` on blog image wrappers and nav lists |
| other (35 values) | 56 | `2px` ×4; `.125rem`, `.375rem`, `10px`, `4px`, `3px` and `0 1.5rem 1.5rem` ×3 each; 11 values ×2; 18 values ×1 (`.85rem`, `1.25rem`, `2rem`, `20px`, `999rem`, mixed corners such as `0 1rem 1rem` on featured images) |

## Shadows as measured (24 values, none a token)

Of the 41 captured section types only the hero illustration variant (02 `--illustration`, the white slider box) carries the card shadow; its other uses (AWS, pricing pop-ups, forms, news, SDK cards) are on pages outside the set.

| Value | Rules | Where |
|---|---|---|
| `0 16px 2rem #12141914` | 10 | the card shadow: AWS logo box, hero tag, news featured, SDK language card, pop-up content, testimonial link, video lightbox hover |
| `0 16px 2rem #12141929` | 5 | the same shadow at 16%: forms, hover state of the cards above |
| `0 8px 2rem #12141929` | 2 | hover of the pop-up trigger and the testimonial link |
| `0 0 1rem #12141929` | 1 | pricing tooltip |
| `0 -24px 50px #00000073` | 1 | mobile nav sheet (upwards) |
| `0 16px 40px -20px #3b41ec73` | 3 | blue glow on the AI pages (code block, folder, term) |
| `0 4px 20px #3b41ec73` | 1 | blue glow on the AI page agent mark |
| `0 0 24px #3b41ec2e` | 1 | blue glow on the /vs/ comparison highlight card |
| `0 0 40px #3b41ec1a` | 1 | blue glow on the AI page "ours" column |
| `0 0 .1875rem #3b41ec80` | 1 | text field focus ring (see the accessibility foundation) |
| Webflow and AI-page one-offs (14 values) | 17 | `#3898ec` checkbox focus and `#e76043` swiper ×2 each, `0 8px 18px #00000080` AI pills ×2; one rule each: `0 16px 2rem #12021929` (the pricing pop-up, a mistyped card shadow), `0 0 1rem #0000001a`, `vise-*` and `vcmp-*` panels, `var(--shadow-3)` on the AI page, the Webflow badge and slider defaults |

## Depth on dark pages

Depth comes from lighter surfaces, not from shadows: page `--social--dark` #111, nav `--secondary--menu-bg` #181818, raised block `--social--dark-gray-background` #1a1a1a (cards v2, v3, plain; secondary button fill), panel `--social--grey` #222 (card-v1 gradient start, product tiles), icon holder #2b2b2b (not a token), chip `--social--light-grey` #444. Same-colour layers are separated by `--border--border-dark` #232324 or `--border--border-hover` #39393a. The card shadow is for light tiles (forms, logo boxes, pop-ups) where a border would look heavy. A glow is interactive feedback or a single highlight, never a resting state on every card.

## The audit's proposed set (decided 8 October 2026)

From the audit, open question 9 ("add radius and shadow tokens"). Decided with the web library: the radii as proposed, pill written 999px; the card shadow and the glow are not taken (one `shadow-float` instead).

| Token (proposed) | Value | Replaces |
|---|---|---|
| radius small | 8px | `.5rem`; also the 4px and 12px uses, unless the team keeps 4px for inputs and checkboxes |
| radius medium | 16px | `1rem`, `12px`, `16px` |
| radius large | 24px | `1.5rem`, `1.25rem`, `2rem` |
| radius pill | `100rem` | `10em`, `25em`, `999px`, `99rem`, `100rem`, `20rem`, `25rem`, `10rem` |
| radius circle | `50%` | `100%`, `999rem` |
| shadow card | `0 16px 2rem #12141914` (hover `#12141929`) | the four `#121419` variants |
| shadow glow | `0 0 24px #3b41ec2e` | the four blue glows |

The design system page (Claude Design) lists the measured radii and shadows as tokens (`radius-4` to `radius-circle`, `shadow-card` to `shadow-focus-field`) so pages built there can name them; they are not Webflow variables and are written as literals in Webflow.

The former `shadows.md` scale (`--shadow-sm` to `--shadow-xl`, light and dark values, eight z-index layers) and the former `border-radius.md` nine-step scale were not on the site; the values above are what the site has. New work uses the set at the top of this page.

## Known inconsistencies (as-is, no decision applied)
- Four radii on one card family (8px cards, 16px thumbnails, 24px rich-text images, pill icons) and six spellings of "pill"
- The card shadow sits on dark cards on some pages where it is invisible (SDK language card)
- Blog images mix corner radii (`0 1.5rem 1.5rem`: square top-left corner)
- Buttons use `10em` and `25em` where every other pill uses a rem or px value
