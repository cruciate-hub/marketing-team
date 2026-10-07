# 60 · Pricing / Plan cards

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/pricing, `section.pricing-hero`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (title, text, the plan cards with price, features and button)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The pricing page only.

## Don't use it when
Any other page; product pages link to pricing instead.

## Content slots
- H1 ("Simple, scalable pricing for your social platform"), one line
- Plan cards: plan name, price and unit, short line, feature list, button (primary on the highlighted plan, grey on the others); the monthly/yearly switch is a script
- Notes under the cards

## Allowed variations
- 2 to 4 plans; which plan is highlighted

## Not allowed
- Prices without the unit, more than one highlighted plan, cards without a button

## Accessibility and mobile
- One `<h1>`; the switch is not in source.html; prices are text
- Cards stack on phones; no sideways scroll at 390px

## Webflow note
- Pricing page section with its own `<style>` embeds (kept). Class names are not a concern.
