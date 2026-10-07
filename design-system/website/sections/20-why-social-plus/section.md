# 20 · Why social.plus grid

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/industry/gaming, section "Why social.plus"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (heading, one line; 5 reasons in a vertical grid with small icons); `--no-heading` (https://www.social.plus/chat: 4 reasons without a heading, with compliance badges and SDK icons)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The fixed set of reasons to choose social.plus, near the end of a product or industry page, before the closing sections.

## Don't use it when
The page already states the reasons in prose; never twice on a page.

## Content slots
- Optional heading H2 "Why social.plus" with one line (live: "An all in-one community solution built for modern retail apps"; TO CHECK: the gaming page copy says retail)
- Reasons: 4 or 5 blocks, each a small white icon, a title of 2 to 5 words and one line of 6 to 12 words (live: fully white-label, fast to launch, developer-friendly SDKs, in-app engagement, privacy-first)
- Product-page form: "All-in-one platform", "Enterprise-ready" with SOC2 / GDPR / ISO 27001 / 99.99% uptime badges, "SDKs & UIKits" with platform icons, "You own the data"

## Allowed variations
- With or without the heading; 4 or 5 reasons; badge and icon rows on the product-page form

## Not allowed
- Reasons other than the fixed set without a messaging decision, images instead of icons, buttons

## Accessibility and mobile
- Titles are `<div>`s on the live site (TO CHECK: use `<h3>`); icons are `<img>` with empty alt
- The grid stacks to one column on phones; no sideways scroll at 390px

## Webflow note
- Webflow component "Industry / Why social.plus"; the product pages use the same `.product-details-grid_*` classes. Class names are not a concern.
