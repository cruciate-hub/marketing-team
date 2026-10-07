# 30 · Thumbnail grid

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/blog, `section#blogs-all`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (blog overview: 3 columns of thumbnail cards, radial-gradient background); `--related-aside` (https://www.social.plus/blog/10-common-…, `aside.section`: heading + 3 related posts at the end of an article)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
Any list of articles: the blog, news, product updates and tutorials overviews, and the "related" block at the end of every blog post, news item, product update and tutorial. The most used content section on the site (476 pages).

## Don't use it when
Listing customer stories (19), use cases (16) or release notes (32).

## Content slots
- Optional heading (related variant: "Related posts" or similar; TO CHECK the live wording per template)
- Cards from the CMS: image (16px radius), tags (`.tag`), title (28px, the h4 size), author row with avatar and name or a date; the card is the link
- 3 columns; the overview loads more rows (script, not in source.html); the related aside shows 3

## Allowed variations
- Blog, news, product updates, tutorials (same card, different fields: author, date, tags); overview or 3-item related aside; background plain dark or `.c-radial-gradient`

## Not allowed
- 2 or 4 columns on desktop, cards without images, excerpts in the card, a carousel

## Accessibility and mobile
- Cards are `<a>` with the title as the accessible name; the author avatar is decorative. Filters, load-more and category tabs are scripts (Finsweet) and are not in source.html
- 3 columns, 2 under 992px, 1 under 480px; no sideways scroll at 390px

## Webflow note
- CMS lists on the templates and overview pages; no component. Class names are not a concern.
