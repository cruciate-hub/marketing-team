# 15 · Card grid / Plain

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/industry/gaming, section "Players start strong, but churn hits fast."
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (heading + 4 plain cards in 2 columns: problem statements); `--three-columns` (https://www.social.plus/use-case/1-1-chat: heading + plain cards in 3 columns)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
Short statements that belong together and need no icon or link: the problems a page solves (industry pages), the reasons for a use case.

## Don't use it when
Items need an icon (13), a link (14), or are more than 6.

## Content slots
- Heading H2, 5 to 9 words (`.max-width-prop` keeps it narrow)
- Cards `.card-plain`: title `h3.h5-font-size` 3 to 6 words, one sentence `.text-size-small` 8 to 16 words
- 4 cards in 2 columns (default) or 3 to 6 cards in 3 columns

## Allowed variations
- 2 or 3 columns; 3 to 6 cards

## Not allowed
- Icons or images in the cards, links, a bordered card, 4 columns, more than one paragraph per card

## Accessibility and mobile
- Titles `<h3>`; nothing interactive
- Cards stack to one column under 480px; no sideways scroll at 390px

## Webflow note
- Webflow component "Cards / Plain" (43 instances). Class names are not a concern.
