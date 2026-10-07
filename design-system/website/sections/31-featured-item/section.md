# 31 · Featured item

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/blog, `section.blog-overview`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (the newest post: large image left; tags, title, excerpt and author right)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The top of an overview page (blog, product updates): one item larger than the grid below it.

## Don't use it when
On article pages or product pages; never more than one.

## Content slots
- From the CMS: image (rounded), tags, title (H1 on the overview page), excerpt 20 to 40 words, author with avatar and date; the title and image link to the post

## Allowed variations
- Blog or product updates; the newest item or a pinned one (CMS)

## Not allowed
- Two featured items, a carousel, an item without an image

## Accessibility and mobile
- The title is the page `<h1>` on the live site (TO CHECK); image alt is the title
- Image above the text on phones; no sideways scroll at 390px

## Webflow note
- CMS list limited to 1 item. Class names are not a concern.
