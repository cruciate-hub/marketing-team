# 12 · Feature grid (3 columns, icon + text)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/chat, section "All the messaging features your app needs"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (heading, intro, grey button; 6 CMS features in 3 columns with icon, title, one line; the button repeats below)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
A product's features need a scannable overview: 6 to 12 features, each one icon, one name, one line. Product and SDK pages (25 pages).

## Don't use it when
Fewer than 6 features (use plain cards 15 or a two-column 11), features that need a paragraph each (13), or reasons to choose social.plus (20).

## Content slots
- Heading H2 `.h3-font-size`, 5 to 8 words; intro paragraph 15 to 30 words; one grey button ("All Chat Features") above and the same below the grid
- Features from the CMS (Features collection): icon (white line icon, 48px), title `h3.feature-heading`, one sentence (10 to 18 words)
- 3 columns, 2 rows on the live page (6 items); multiples of 3

## Allowed variations
- 6, 9 or 12 features; with or without the lower button; CMS-driven or static items with the same markup
- Background `.c-radial-gradient` (default) or plain dark

## Not allowed
- Coloured icons, images instead of icons, 2 or 4 columns, cards with borders (that is 13 or 14), links on every item

## Accessibility and mobile
- Icons are `<img>` with the feature name as alt on the live site (TO CHECK); titles are `<h3>`
- 3 columns, 2 under 992px, 1 under 480px; no sideways scroll at 390px

## Webflow note
- Webflow component "Section / Community Features" (CMS list). Class names are not a concern.
