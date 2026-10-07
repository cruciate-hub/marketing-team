# G3 · Breadcrumb bar

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/customer-story/activerse, `div.breadcrumb-bar` (`.c-dark`)
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (dark, `.c-dark`); `--light` (https://www.social.plus/tutorials/add-a-vector-database-to-your-gpt-custom-content-bot: the plain class without `.c-dark`)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
An article page that belongs to a collection with an overview page: customer stories, tutorials, FAQ entries, legal pages, people, resources. It is the first thing under the nav, above the article hero or title.

## Don't use it when
Marketing pages, product pages, home, /vs/ pages. Blog posts, answers and glossary entries do not use it on the live site (the glossary header carries its own breadcrumb line, see 04).

## Content slots
- One line: overview link ("Customer Stories") › current page name, or just the overview link with a chevron (live: "Customer Stories" only)
- Nothing else: no icons, no dates

## Allowed variations
- Dark (`.c-dark`) is the one to use; the plain class is how the tutorials template renders it (TO CHECK: both look the same on the dark page background; keep one)

## Not allowed
- More than two levels, a different text size, a background band, breadcrumbs inside the hero

## Accessibility and mobile
- `<nav aria-label="Breadcrumb">` is missing on the live site (TO CHECK: add it); the link is a plain `<a>`
- Height 46px; text `.text-size-tiny` on `--text--text-color-grey-light`. Full width on phones, no sideways scroll at 390px

## Webflow note
- A symbol on the CMS templates; class names are not a concern.
