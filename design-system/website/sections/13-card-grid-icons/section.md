# 13 · Card grid / Feature icons (v2, v3)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/industry/gaming, section "Everything you need to make your app social-powered"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (card-v2: 4 columns, 8 compact icon cards); `--v3-link-cards` (https://www.social.plus/use-case/1-1-chat: 3 columns of card-v3 with icon, title, text); `--v3-docs` (https://www.social.plus/release-note/…: 3 card-v3 link cards with a checklist each, radial-gradient background; ends every release note and tutorial)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
A set of capabilities or links that each need an icon and a line or two, inside a flat card. Industry pages (v2 grid), use-case pages (v3), the "Explore our documentation" block on release notes and tutorials (v3 docs).

## Don't use it when
The items are long (two-column 11), need a border and a text link (14), or have no icon (15).

## Content slots
- Heading H2, 4 to 8 words; optional intro
- card-v2: 72px icon, title `h3.h5-font-size` (20px), one line `.text-size-small`; 8 or 16 cards in 4 columns
- card-v3: icon, title (28px, the h4 size), 1 to 2 sentences; 3 or 6 cards in 3 columns
- v3 docs: 3 link cards, each with a title, a short line and a 3-item checklist; the whole card is the link

## Allowed variations
- 3 or 4 columns; v2 or v3 card; link cards or plain cards; background plain dark or `.c-radial-gradient`
- The audit recommends merging v2 and v3 into one icon card; until decided both are captured as-is

## Not allowed
- Mixing v2 and v3 in one grid, bordered cards (14), images instead of icons, more than 16 cards, 2 columns on desktop

## Accessibility and mobile
- Titles are `<h3>`; link cards are one `<a>` with the title as the accessible name (TO CHECK on the docs variant)
- 4 columns become 2 under 992px and 1 under 480px; no sideways scroll at 390px

## Webflow note
- Webflow component "Card / v2" (80 instances); there is no component for card-v3 (27 uses) and no component for the docs block beyond "Section / Explore docs". Class names are not a concern.
