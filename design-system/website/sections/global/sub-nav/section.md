# G2 · Sub-nav

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/chat, `header.sub-navbar`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (product: Chat); `--blog` (https://www.social.plus/blog, `div.sub-navbar`: the blog categories)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
A page belongs to a product family (Chat, Social, Video, Analytics, white-label, AI) or to a resource family (blog, product updates, release notes). It sits directly under the main nav on every page of that family.

## Don't use it when
Home, industry pages, /vs/ pages, contact pages, articles (blog posts, answers, glossary entries, customer stories), pricing-free landing pages. One sub-nav per page, never two.

## Content slots
- Left: the family name as a dropdown toggle (live: "Chat" with Social and Video in the dropdown), then an "Overview" link
- Links: 3 to 5 short items (live: Features, SDK, UIKit, Docs). External links (Docs) keep the external-link icon
- Right: nothing on the live product sub-nav; TO CHECK whether a button is allowed
- Blog variant: the category links (All, Community, Product, …), no dropdown

## Allowed variations
- Link set per product family or resource family; dropdown contents follow the family. Bar height and type stay the same
- Background: `--social--dark` on most pages; the pricing page shows the bar on `--secondary--menu-bg` (#181818, TO CHECK which one is intended)

## Not allowed
- More than 5 links, a second row, icons other than the external-link icon, a different height, a light bar

## Accessibility and mobile
- Links are plain `<a>`; the dropdown toggle is a link with `role="button"` on the live site (TO CHECK: keyboard opening is script driven and not in source.html)
- Bar height 4.5rem (72px); 1px bottom border `--border--border-hover`. On phones the links scroll sideways inside the bar (no page sideways scroll at 390px)

## Webflow note
- Webflow components "Nav / Sub / CSS", "Nav / Sub / JS", "Nav / Chat", "Nav / Social", "Nav / Video", "Nav / Blog", "Nav / Product Updates": all render this one bar. The dropdown script is removed from source.html; class names are not a concern.
