# Accessibility

WCAG 2.1 AA is the target for every page, email and graphic. This foundation holds the contrast of the live token pairs (computed from tokens.css), the site's focus rules, touch targets, text sizes, motion, keyboard and structure rules, and the open items the section notes marked TO CHECK.

- Status: draft (2026-10-07), as-is: ratios computed from the live tokens, rules from the brand guidelines (formerly `design-system/accessibility.md`) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: tokens.css (WCAG 2.1 relative luminance), the captured sections' CSS (`a:focus-visible`, `.text-field:focus`), the section notes
- Preview: preview.html (hand-made, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Not produced by capture/: the preview is written by hand and survives re-runs. Re-compute the table when tokens.css changes

## Contrast of the token pairs (computed 2026-10-07)

Body text needs 4.5:1; large text (24px, or 19px bold) and interface parts (borders of controls, icons) 3:1.

| Text | Background | Ratio | Verdict | Where |
|---|---|---|---|---|
| `--main--white` #ffffff | `--social--dark` #111 | 18.88:1 | AA | headings, white text |
| `--text--text-color-grey-light` #b3b3b3 | `--social--dark` | 9.01:1 | AA | body text on every page |
| `--text--text-color-grey-lighter` #d1d1d1 | `--social--dark` | 12.37:1 | AA | rarely used |
| `--text--text-color-grey-mid` #a4a4a4 | `--social--dark` | 7.58:1 | AA | rarely used |
| `--text--text-color-grey-muted` #929292 | `--social--dark` | 6.07:1 | AA | no rule uses it |
| `--text--text-color-grey-medium` #717275 | `--social--dark` | 3.93:1 | large text and UI only | nav and footer small text on 114 pages: TO CHECK (use grey-light, or keep it for 19px bold and larger) |
| `--main--white` | `--social--dark-gray-background` #1a1a1a | 17.40:1 | AA | card headings |
| `--text--text-color-grey-light` | `--social--dark-gray-background` | 8.30:1 | AA | card body |
| `--text--text-color-grey-medium` | `--social--dark-gray-background` | 3.62:1 | large text and UI only | muted text on cards |
| `--main--white` | `--secondary--menu-bg` #181818 | 17.76:1 | AA | nav links |
| `--text--text-color-grey-medium` | `--secondary--menu-bg` | 3.69:1 | large text and UI only | nav small text |
| `--main--white` | `--social--grey` #222 | 15.91:1 | AA | panels |
| `--text--text-color-grey-light` | `--social--grey` | 7.59:1 | AA | panel body |
| `--main--white` | `--social--main-blue` #3b41ec | 6.66:1 | AA | primary button label, tags on blue |
| `--main--white` | `--social--button-hover` #272b9d | 10.95:1 | AA | primary button hover |
| `--main--white` | `--social--button-pressed` #27265e | 13.77:1 | AA | primary button pressed |
| `--social--main-blue` #3b41ec | `--social--dark` | 2.84:1 | fails | blue as text or icon colour on dark: never. Blue is a fill (button, circle, tag background), not a text colour on dark |
| `--gradient--medium-blue` #3769ec | `--social--dark` | 3.95:1 | large text and UI only | plain links and superscripts on the live site: TO CHECK (underline or a lighter blue such as #7b94fe, 6.75:1, which page embeds already use) |
| `--social--main-blue` | `--main--whitesmoke` #f5f5f5 | 6.11:1 | AA | `.tag` text |
| `--social--main-blue` | `--main--white` | 6.66:1 | AA | blue text and outlined buttons on white (emails) |
| `--gradient--medium-blue` | `--main--white` | 4.78:1 | AA | links on white |
| `--text--text-color-dark` #111 | `--main--white` | 18.88:1 | AA | text on light sections |
| `--text--text-color-grey-dark` #414347 | `--main--white` | 9.91:1 | AA | secondary text on light, email body |
| `--text--text-color-grey-medium` | `--main--white` | 4.81:1 | AA | muted text on light, email small text |
| `--text--text-color-dark` | `--social--grey-background` #f9f9f9 | 17.94:1 | AA | text on grey sections |
| `--text--text-color-grey-dark` | `--social--grey-background` | 9.41:1 | AA | |
| `--text--text-color-grey-medium` | `--social--grey-background` | 4.57:1 | AA | just above the line |
| `--secondary--green` #1dc497 | `--social--dark` | 8.45:1 | AA | status text |
| `--secondary--yellow` #f7c506 | `--social--dark` | 11.64:1 | AA | status text |
| `--secondary--red` #ff305a | `--social--dark` | 5.24:1 | AA | status and error text |
| `--secondary--orange` #ff6937 | `--social--dark` | 6.59:1 | AA | decoration |
| `--secondary--purple` #9f72ff | `--social--dark` | 5.69:1 | AA | decoration |
| `--secondary--pink` #f568f0 | `--social--dark` | 7.30:1 | AA | decoration |
| `--main--white` | `--secondary--green` | 2.24:1 | fails | white text on green: never |
| `--main--white` | `--secondary--red` | 3.61:1 | large text and UI only | white on red: large text or an icon |
| `--text--text-color-dark` | `--secondary--yellow` | 11.64:1 | AA | dark text on yellow |
| `--border--border-dark-grey` #666 | `--social--dark` | 3.29:1 | UI passes (3:1) | secondary button outline |
| `--border--border-hover` #39393a | `--social--dark` | 1.64:1 | decorative | card borders carry no meaning |
| `--border--border-dark` #232324 | `--social--dark` | 1.20:1 | decorative | dividers |
| `--border--border-med-grey` #d0d0d1 | `--main--white` | 1.54:1 | decorative | light input border: the input needs another cue (label, focus ring) |

Values regular sections use that are not tokens: `#dc3545` form error on #111 is 4.17:1 (below 4.5:1, TO CHECK: use `--secondary--red`); `.tag.c-new` #3ccb7f on #093a20 is 6.13:1; input background #1b1b1b with grey-light text is 8.21:1.

## Focus

- Links: `a:focus-visible { outline: .125rem solid; outline-offset: .125rem }` in the text colour (the live rule on every page).
- Text fields: `.text-field:focus { box-shadow: 0 0 .1875rem #3b41ec80 }` (3px blue glow) on the 1px `--social--main-blue` border.
- Buttons: browser default (TO CHECK: the nav sets a 2px white ring; give every button the link rule). Webflow's custom checkbox and radio focus ring is `0 0 3px 1px #3898ec`, a Webflow default rather than a brand colour (TO CHECK: `--social--main-blue`).
- Never `outline: none` without a replacement; use `:focus-visible` so mouse clicks do not show the ring; the ring must be visible on dark and on light.

## Touch targets and text size

- 44px minimum for every interactive element (the brand keeps 44 although WCAG 2.5.8 asks 24). The primary and secondary buttons are 2.8rem = 44.8px; the form submit is 52px; text links and footer links are a text line of about 22px and need padding or spacing (TO CHECK); accordion rows are 12px padding around a 19.2px line, about 43px (TO CHECK).
- 12px is the floor. Smallest live sizes: `.tag` .8rem = 12.8px, `.superscript` 14px, `.text-size-tiny` and `.heading-xsmall` 14.4px. The blog grid overrides the tag to 10.8px (TO CHECK: below the floor).
- Uppercase only at tag and superscript size, with letter spacing (.025rem on tags, .044rem on superscripts).

## Motion

- Every animation and transition respects `prefers-reduced-motion: reduce` (durations to 1ms, transforms become opacity fades); nothing flashes more than 3 times a second.
- On the live site only the nav and the /vs/ hero carry a reduced-motion rule. The logo marquee (10), the count-up numbers (25), the quote carousel (26), the hero slider (02) and the GSAP reveals keep moving (TO CHECK). The captured sections show the still state, which is also the reduced-motion state to build.

## Keyboard and structure (rules, with the live gaps)

| Rule | Live site today |
|---|---|
| Accordion headers are `<button>`s with `aria-expanded`; `Enter` and `Space` open them | FAQ (18) and accordion with image (17) rows are `<div>`s opened by a script; keyboard users cannot open them (TO CHECK) |
| Tabs and sliders are reachable and operable with the keyboard | /vs/ customer stories tabs (53), quote carousel logo tabs (26) and pricing sliders (61) are not (TO CHECK) |
| Plain links are `<a href>` without `role="button"` | Footer links (G5) and logo wall cards (10) carry `role="button"` (TO CHECK: drop it) |
| Breadcrumbs sit in `<nav aria-label="Breadcrumb">` | Missing on the breadcrumb bar (G3) and the article title header (04) (TO CHECK) |
| One `<h1>` per page, no heading-level skips, card titles are `<h3>` | Image-card grid (16) titles are `<h2>`; Why social.plus (20) titles are `<div>`s (TO CHECK) |
| Meaningful images have alt text; decorative ones `alt=""` | Two-column (11), product details (21), feature grid (12), hero industry (03) often ship empty alt on meaningful images; the hero video (01) has no text alternative (TO CHECK) |
| Icon-only links carry `aria-label` or a `<title>`; decorative icons `aria-hidden="true"` | Social glyphs and the arrow do this already |
| Tables of data are `<table>`; key-value rows are a list or `<dl>` | Pricing compare (61) and additional fees (62) rows are `<div>`s; customer story metrics (41) are `<div>`s (TO CHECK) |
| Form fields have a visible `<label>`; errors are text next to the field with `aria-describedby` | Labels float inside the field (24); the error block is a Webflow div (TO CHECK: link it to the field) |
| Tab order follows the reading order; focus is trapped in open dialogs; `Escape` closes them | Pop-ups are script driven and not captured |
| No information by colour alone | Status tags (`.tag.c-new`) carry text; the pricing checkmarks are icons without text (TO CHECK: add visually hidden "Included") |

## Checklist before a page or email ships

- [ ] Every text and background pair is in the table above with AA, or large text at 3:1
- [ ] No `--social--main-blue` text or icon on a dark background
- [ ] Focus ring visible on every link, button and field, on dark and on light
- [ ] 44px targets; nothing under 12px
- [ ] Headings in order, one `<h1>`, card titles `<h3>`
- [ ] Alt text on meaningful images, `alt=""` on decorative ones, a text alternative for video
- [ ] Accordions, tabs and sliders work with the keyboard, or the page uses the static state
- [ ] Forms: visible labels, text errors linked to the field
- [ ] Reduced motion: nothing keeps moving
- [ ] Emails: the same pairs on white (`#414347` body, `#717275` small text, `#3b41ec` links and buttons with white labels)
