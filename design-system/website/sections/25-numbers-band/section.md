# 25 · Numbers band

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/, section "Built to move the numbers your board actually asks about"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (heading; 4 big numbers with a line each; footnote)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
Four outcome numbers with sources, on the home page or an overview page. The audit keeps it in the set because it is generic.

## Don't use it when
The numbers are not sourced or are fewer than three; on pages that already show customer metrics (41, 53).

## Content slots
- Heading H2, 6 to 10 words
- 4 numbers: value with unit ("22%"), one line of 5 to 9 words ("lift in monthly active users")
- Footnote `.text-size-tiny`: the source or the caveat ("Representative client results. Outcomes vary …")

## Allowed variations
- 3 or 4 numbers. TO CHECK: whether it may be used outside the home page

## Not allowed
- Numbers without the footnote, icons, images, more than 4

## Accessibility and mobile
- The count-up is a script on the live site; the numbers are static text in source.html. The number and its line are `<div>`s (TO CHECK: use a list)
- 4 across on desktop, 2 by 2 under 992px, stacked on phones; no sideways scroll at 390px

## Webflow note
- Home-page section with its own `<style>` embed (kept). Class names are not a concern.
