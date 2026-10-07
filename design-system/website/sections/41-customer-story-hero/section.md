# 41 · Customer story hero

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/customer-story/activerse, `section.cs-story_hero`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (customer logo, title, intro; key metrics; image right)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The opening of every customer story, directly under the breadcrumb bar (G3).

## Don't use it when
Any other page type.

## Content slots
- Customer logo (white), title H1 8 to 14 words ("How Activerse enhances fitness & wellness apps with …"), intro 25 to 45 words
- Metrics: 2 or 3 numbers with a label each (CMS fields)
- Image: the customer's app screenshot or photo, rounded, right column

## Allowed variations
- 2 or 3 metrics; with or without the intro

## Not allowed
- Buttons in the hero, a video, a light background

## Accessibility and mobile
- One `<h1>`; the logo image alt is the customer name; metrics are `<div>`s (TO CHECK: use a list)
- Image above or below the text on phones (TO CHECK in mobile.png); no sideways scroll at 390px

## Webflow note
- Customer Stories template. Class names are not a concern.
