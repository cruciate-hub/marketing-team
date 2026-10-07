# 32 · Updates list (with tags)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/release-note/1-1-chat-support-for-ios-and-android-uikit, section "Latest Releases"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (heading + date-ordered list of release notes, each with date, title and tags; radial-gradient background)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
Under a release note or product update, and on the release notes overview: the latest items as a compact list, not cards.

## Don't use it when
Articles with images to show (30), customer stories (19).

## Content slots
- Heading H2 ("Latest Releases")
- Rows from the CMS: date, title (link), tags (`.tag.c-dark`, `.tag.c-new` for new items); 5 to 10 rows
- The overview page adds tag filters (checkboxes, script) and shows every item

## Allowed variations
- Number of rows; with or without the filter form (overview only)

## Not allowed
- Images in the rows, excerpts, more than 3 tags per row

## Accessibility and mobile
- Titles are links; tags are `<div>`s inside the link (TO CHECK)
- Rows wrap on phones: date above the title, tags below; no sideways scroll at 390px

## Webflow note
- CMS list with the "CC / Product Update Tags" embed. Class names are not a concern.
