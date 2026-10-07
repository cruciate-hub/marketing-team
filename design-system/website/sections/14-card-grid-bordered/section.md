# 14 · Card grid / Bordered (v1)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/social/uikit, section "Open Source Social UIKits"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (heading, intro; 5 card-v1 cards in 3 columns with image, title, text and a "Docs" text link; radial-gradient background)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
Each item is a thing someone can go to (an SDK, a UIKit, a plan, a partnership track): image or icon, title, a sentence or two, and a text link. The style guide's own card.

## Don't use it when
Items are one-liners (13), have no link (15), or are customer stories (19).

## Content slots
- Heading H2, 3 to 6 words; intro paragraph 20 to 40 words (`.max-ch-72`)
- Cards `.card-v1`: optional image or 48px blue-circle icon (`.card-icon-v1`), title `h3.h5-font-size`, text `.text-size-small` 20 to 35 words, footer `.text-link` ("Docs", "Learn more")
- 2 to 6 cards; 3 columns (the live page shows 5 cards, the last row left-aligned)

## Allowed variations
- 2, 3 or 4 columns; `.c-outline` (transparent fill), `.c-centered`, `.c-link` (whole card is the link, lifts 2px on hover); with or without image
- Background plain dark or `.c-radial-gradient`

## Not allowed
- Cards without the border, blue primary buttons inside cards, two links per card, mixed card styles in one grid

## Accessibility and mobile
- Titles `<h3>`; the text link is a plain `<a>` with an arrow icon (`aria-hidden`)
- 3 columns, 2 under 992px, 1 under 480px; card padding 2.5rem (1.5rem under 480px); no sideways scroll at 390px

## Webflow note
- Webflow component "Card / v1" (31 instances). Class names are not a concern.
