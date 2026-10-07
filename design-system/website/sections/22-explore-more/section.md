# 22 · Explore more (links with images)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/chat, section "Explore more of social.plus"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (heading, intro; 2 link tiles with image, title `.h3-font-size`, text and a grey button; radial-gradient background)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The end of a product page: point to the two other product families (Social, Video, Chat) before the footer CTA band.

## Don't use it when
Industry pages, articles, /vs/ pages; never more than two tiles.

## Content slots
- Heading `.h2-font-size` "Explore more of social.plus"; intro 20 to 30 words (`.max-ch-50`)
- Two tiles: product image (rounded), title `h3.h3-font-size` 4 to 6 words, text 15 to 25 words, grey button ("Explore Social", "Explore Video")

## Allowed variations
- Which two products. Nothing else

## Not allowed
- Three tiles, a primary blue button, tiles without images, a light background

## Accessibility and mobile
- Titles `<h3>`; the button is the link, the tile itself is not (TO CHECK)
- The two tiles stack on phones; no sideways scroll at 390px

## Webflow note
- Plain section repeated on the product pages (7 pages). Class names are not a concern.
