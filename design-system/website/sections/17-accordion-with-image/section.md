# 17 · Accordion with image (features)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/industry/gaming, section "From sessions to seasons"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (heading; 3 accordion items with a timeline line, image on the left `.c-reversed`); `--square-image` (https://www.social.plus/use-case/1-1-chat: 4 items, square image on the right)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
Three to five steps or examples that each have their own picture, told one at a time: how a product works over time (industry pages), examples of a use case.

## Don't use it when
The items have no picture of their own (15), or the questions are FAQs (18).

## Content slots
- Heading H2, 3 to 6 words
- Items `.add-ons_accordion-item`: title `h3.h5-font-size` 3 to 6 words, one sentence 8 to 16 words; the open item shows its image
- Images: one per item, rounded; left (`.c-reversed`) or right; square (`.c-square`) on the use-case variant

## Allowed variations
- 3 to 5 items; image left or right; square or 4:3 image

## Not allowed
- More than one open item, items without an image, links inside items, a video

## Accessibility and mobile
- Opening an item is a script on the live site (`.add-ons_js-accordion`); the first item is open in source.html and the screenshots. TO CHECK: the headers are not `<button>`s, keyboard users cannot open them
- On phones the image sits above the list; no sideways scroll at 390px

## Webflow note
- Webflow component "Industry / Accordion". Class names are not a concern.
