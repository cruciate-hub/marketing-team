# 61 · Pricing / Compare table

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/pricing, `section.pricing-slider-section`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (usage sliders and the feature comparison table, rows from the CMS, radial-gradient background)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The pricing page only, under the plan cards (60).

## Don't use it when
Comparing with a competitor (that is 52).

## Content slots
- Heading ("Usage & Features"), the usage sliders with their values (script; static here)
- Table: feature rows grouped by category (CMS, Pricing features collection), one column per plan, checks or values; tooltips on some rows (script)

## Allowed variations
- Row set from the CMS; number of plan columns

## Not allowed
- A fourth column of text, rows without a plan value, images in the table

## Accessibility and mobile
- A real `<table>` is not used on the live site (rows are `<div>`s; TO CHECK); sliders are custom controls without keyboard support in source.html
- The table scrolls sideways inside the section on phones (no page sideways scroll at 390px)

## Webflow note
- Webflow components "Pricing / Features" and "CC / Table Styling" (8). Class names are not a concern.
