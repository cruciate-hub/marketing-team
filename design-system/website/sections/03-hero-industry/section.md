# 03 · Hero / Industry

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/industry/gaming, `section.industry-hero`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (title, enlarged paragraph, one button, centred image right)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The first section of an industry page (gaming, fintech, retail, sports, …): one sentence that names the outcome for that industry, one image.

## Don't use it when
Product pages (01), overview pages (02), articles (04), /vs/ pages (05).

## Content slots
- H1 `.industry-title`: 5 to 8 words (live: "Turn your game into a living community"). Note: this title is 64px/700 on the live site where the style guide H1 is 52.8px/600 (as-is, flagged in foundations/typography)
- Paragraph `.enlarged-paragraph.max-ch-41`: 15 to 25 words
- One primary button ("Contact Sales")
- Image: one industry illustration, centred in the right column, no frame

## Allowed variations
- Image per industry. Text lengths within the ranges. Nothing else

## Not allowed
- Two buttons, a video, a logo row inside the hero (the logo wall 10 follows), a light background

## Accessibility and mobile
- One `<h1>`; the image is decorative on the live site (`alt=""`; TO CHECK)
- Background #14152c tint in the hero on the live page (not a token; as-is). Stacks on phones, image below the text; no sideways scroll at 390px

## Webflow note
- Webflow component "Industry / Hero". Class names are not a concern.
