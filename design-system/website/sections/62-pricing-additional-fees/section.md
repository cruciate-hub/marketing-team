# 62 · Pricing / Additional fees

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/pricing, `section#payment-information`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (heading + fee rows in two columns)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The pricing page only, after the compare table (61).

## Don't use it when
Any other page.

## Content slots
- Heading H2 ("Additional fees"), optional line
- Rows: fee name and a short explanation, in two columns

## Allowed variations
- Number of rows

## Not allowed
- Prices without an explanation, a third column, images

## Accessibility and mobile
- Rows are `<div>`s (TO CHECK: a definition list would fit)
- One column on phones; no sideways scroll at 390px

## Webflow note
- Webflow component "Pricing / Payment information". Class names are not a concern.
