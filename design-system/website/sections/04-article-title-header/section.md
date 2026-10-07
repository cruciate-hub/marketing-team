# 04 · Article / Title header (breadcrumb + H1)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/glossary/activity-feed, `header.section.padding_y.c-glossary`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (glossary: breadcrumb line and H1)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The top of a glossary entry, a FAQ entry or a resource page: a breadcrumb line and the title, nothing else. The body follows in its own section (43 for the glossary).

## Don't use it when
Blog posts, answers, release notes (their title is inside the article section, 40), customer stories (41).

## Content slots
- Breadcrumb line: overview link › current term (live: "Glossary › Activity Feed")
- H1: the term or the question, 1 to 8 words

## Allowed variations
- Glossary, FAQ and resource pages share it; TO CHECK whether a one-line intro under the H1 is allowed

## Not allowed
- Images, buttons, dates, author rows, a background band

## Accessibility and mobile
- `<header>` with the page's only `<h1>`. The breadcrumb needs `<nav aria-label="Breadcrumb">` (TO CHECK)
- Height about 250px at 1440; stacks on phones; no sideways scroll at 390px

## Webflow note
- Glossaries template header. Class names are not a concern.
