# 21 · Feature grid / Product details

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/product, section "White-label social features"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (tile grid: text tiles with title and paragraph, image tiles)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The product overview page: a wall of tiles that each name one capability with a short paragraph and a product image.

## Don't use it when
Any single-product page (use 11, 12 or 13).

## Content slots
- Heading H2, 3 to 5 words
- Tiles: title `h3`, 1 to 2 sentences, an image; 6 to 10 tiles in a 2-column tile grid

## Allowed variations
- Number of tiles. TO CHECK with Stefan or Amadeus whether this section stays in the set or becomes product-page only (it exists on one page)

## Not allowed
- Tiles without an image, links inside tiles, a 3-column version

## Accessibility and mobile
- Titles `<h3>`; images need alt text (TO CHECK)
- Tiles stack to one column under 480px; no sideways scroll at 390px

## Webflow note
- Webflow component "Section / Product Overview" (1 instance). Class names are not a concern.
