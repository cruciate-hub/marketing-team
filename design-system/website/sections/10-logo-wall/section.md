# 10 · Logo wall

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/vs/circle, `section.c-hmpg_wall`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css
- Variants captured: default (grid: divider heading, 12 logos on desktop, 6 on phones, hover chips); `--marquee` (https://www.social.plus/chat, `section.logo-row`: one scrolling row of logos under a fade divider, as on product pages)
- Captured on 2026-10-07 from https://www.social.plus/vs/circle by capture/capture.mjs

## Use it when
Social proof is needed early on a page: after the hero or the statement band, before the detailed sections.

## Don't use it when
The page already shows customer stories with logos right above or below (then keep one of the two), or on pages for a single customer.

## Content slots
- Divider heading: a short line in small caps between two hairlines ("Trusted by some of the world's biggest brands", 7 words)
- Logo cards: CMS list of customers (24 on the live site). The CSS shows the first 12 on desktop (6 columns by 2 rows) and 6 picked ones on phones (3 by 2). Each card is a dark gradient tile with a 1 px `--border--border-dark` border, radius .5 rem, white logo (SVG, brightened)
- Each logo links to its customer story; on hover a "Read customer story" chip with an arrow fades in
- Soft blue radial glow in the bottom right corner (`.bg-circle-gradient`)

## Allowed variations
- Which customers and how many rows (6 per row on desktop). Heading text. Without the glow (TO CHECK)
- Marquee variant: the same CMS logos in one row that scrolls sideways (CSS animation; stands still under reduced motion and in source.html). Use it on product pages where the grid would be too heavy

## Not allowed
- Coloured logos, logos without cards (grid), more than 2 rows, a light background, both variants on one page

## Accessibility and mobile
- Each card has `aria-label` with the customer name; images have "<Name> logo" alt text; the links are `<a role="button">` (TO CHECK: should be plain links)
- 4 columns on tablet, 3 on phones; no sideways scroll at 390 px
- The hover chip is hidden on touch screens

## Webflow note
- Webflow "Logo wall" CMS section; the hover chip and the responsive logo picks are a `<style>` embed inside the section (kept in source.html). Class names are not a concern.
