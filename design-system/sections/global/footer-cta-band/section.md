# G4 · Footer CTA band

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/vs/circle, `section.footer` (the CTA part above the site footer)
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css
- Variant captured: heading, one line, one primary button
- Captured on 2026-10-07 from https://www.social.plus/vs/circle by capture/capture.mjs

## Use it when
The last section of every website page, directly above the footer (G5).

## Don't use it when
Blog posts and glossary entries do not carry it on the live templates (as-is; TO CHECK). Do not place it in the middle of a page; a mid-page call to action is the inline CTA band (23) or the form section (24).

## Content slots
- Heading (max 7 words; live: "Turn your app into a growth engine", 1.75 rem to 3 rem, bold white), left
- One line under it (max 20 words, `--text--text-color-grey-light`)
- One primary button on the right: "Contact Sales" with arrow icon, scaled 1.2x (pill, main blue, hover `--social--button-hover`), linking to /contact/contact-sales
- Hairlines above and below the band (1 px `--border--border-dark`)

## Allowed variations
- Heading and line text. Button text may change to another sales action (TO CHECK)

## Not allowed
- A second button, a form, an image, a light background, a centred layout

## Accessibility and mobile
- Button is an `<a aria-label="Contact Sales">` with visible text; the arrow SVG is `aria-hidden`
- Desktop: text left, button right on one row. Phones: text on top, button below, full width; no sideways scroll at 390 px
- Static section, no script

## Webflow note
- Webflow component "Section / Footer CTA" (82 instances). Class names are not a concern.
