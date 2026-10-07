# G1 · Nav

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/vs/circle, `header.nav` (the same nav is on every page)
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css
- Variant captured: dark, mega menu closed
- Captured on 2026-10-07 from https://www.social.plus/vs/circle by capture/capture.mjs

## Use it when
Every website page. It is the only nav.

## Don't use it when
Never leave it out. Landing pages without navigation are not part of the set (TO CHECK: Stefan or Amadeus).

## Content slots
- Logo (social.plus wordmark, links to /)
- 5 menu items in this order: Product, Use Cases, Pricing, Resources, Company. Product, Use Cases, Resources and Company open a mega-menu panel (`.nav-dropdown-list`); Pricing is a plain link
- Panels: a left intro column (short text plus a grey "overview" button) and a right column with link lists (title plus one-line description, some with an "Add-on" tag), a CMS list of the 2 latest product updates or customer stories, and an "All …" text link
- One primary button on the right: "Contact Sales" (pill, main blue, arrow icon)
- Announcement bar above the nav exists on the site (CMS driven, closable); it is not in this capture

## Allowed variations
- Panel content follows the CMS (product updates, customer stories). Menu item names and order are fixed
- On small screens the menu collapses behind a hamburger (three lines, right side) and opens as a sheet

## Not allowed
- Extra menu items, a second button, light background, logo variants, search field in the bar

## Accessibility and mobile
- `<nav aria-label="Main navigation">`, menu as `role="list"`, dropdown toggles with `role="button"`, `aria-expanded` and `aria-controls`; keyboard focus ring is 2 px white
- Bar height 5.75 rem on desktop (4.25 rem on phones), background `--secondary--menu-bg` (#181818), 1 px border `--border--border-hover`, radius .25 rem, frosted-glass blur behind it
- Sticky at the top of the page (`position: sticky`). Mobile: hamburger with `aria-label="Open menu"`, `aria-haspopup`, `aria-controls="nav-menu"`
- Open panels and hover states are script driven and not shown in the screenshots. TO CHECK: capture one open panel as a second screenshot

## Webflow note
- Webflow component "Nav / Main". Captured from the live site; class names are not a concern. The dropdown script and the right-click logo menu were removed from source.html.
