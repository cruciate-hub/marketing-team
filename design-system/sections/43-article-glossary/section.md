# 43 · Glossary entry

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/glossary/activity-feed, `section.section`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (table of contents left, `.rich-text` body right)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The body of every glossary entry, after the title header (04).

## Don't use it when
Answers, blog posts (40).

## Content slots
- Table of contents: the entry's h2 headings as links (built by a script on the live site; the links present in the HTML are kept). This is the site's one table-of-contents style: use it on every page with a contents list (articles, Community Framework stages), never a plain link list. As rendered live (read 2026-10-29):
  - `nav.toc-wrapper` (sticky, top 8rem), Figtree 14px/1.2, links white
  - `.toc-header` "Table of contents": 16px 20px padding, background #232324, 1px white left border, 700, uppercase, letter-spacing 1px
  - `.toc-list-wrapper`: a 1px `.toc-progress-track` (#232324) with a white `.toc-progress-indicator` that grows with reading progress, beside `ul.toc-list` (1px #232324 border on right and bottom, bottom-right radius 8px)
  - `.toc-item`: 1px #232324 line between items; `a.toc-link` padding 12px 20px 12px 16px; the current section `.active` (aria-current="location") turns 700
- Body `.rich-text`: definition first (h2 "What is …?"), then the fixed sections of the glossary format, tables allowed
- Bottom: related terms (TO CHECK)

## Allowed variations
- Body length; with or without tables

## Not allowed
- Images in the body (TO CHECK), a sidebar form, a different body style

## Accessibility and mobile
- Body headings start at h2; the table of contents is a `<nav aria-label="Table of contents">` with a list (the live markup)
- One column on phones, contents above the body; no sideways scroll at 390px

## Webflow note
- Glossaries template. The TOC script is removed from source.html. Class names are not a concern.
