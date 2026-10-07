# 16 · Image-card grid (use cases, industries)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/industry/gaming, section "Use cases that keep players coming back"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (heading + 6 static image cards in 3 columns: image, title, one line); `--four-columns-cms` (https://www.social.plus/white-label/social-network: 8 CMS cards in 4 columns, radial-gradient background)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
Linking to use cases, industries or features that each have a product image: industry pages, white-label pages, the use-cases overview.

## Don't use it when
The items have no image (13, 15) or are customer stories (19).

## Content slots
- Heading H2, 4 to 8 words (`.max-ch-23` on the live page)
- Cards: product image (rounded, about 4:3), title `h2.h5-font-size` on the live page (TO CHECK: should be `<h3>`), one line of 6 to 12 words; each card links to its page
- 6 cards in 3 columns, or 8 in 4 columns from the CMS (Use Cases collection)

## Allowed variations
- 3 or 4 columns; static or CMS-driven; background plain dark or `.c-radial-gradient`

## Not allowed
- Cards without images, icons instead of images, text longer than one line, more than 8 cards

## Accessibility and mobile
- Card titles are `<h2>` on the live page (a heading-level skip; TO CHECK); images need alt text
- 3 or 4 columns become 2 under 992px and 1 under 480px; no sideways scroll at 390px

## Webflow note
- Webflow components "Industry / Use Case" (60 instances) and "Industry / 4 Grid". Class names are not a concern.
