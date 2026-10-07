# 43 · Glossary entry

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/glossary/activity-feed, `section.section`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (table of contents left, `.rich-text` body right)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The body of every glossary entry, after the title header (04).

## Don't use it when
Answers, blog posts (40).

## Content slots
- Table of contents: the entry's h2 headings as links (built by a script on the live site, Finsweet TOC; the links present in the HTML are kept)
- Body `.rich-text`: definition first (h2 "What is …?"), then the fixed sections of the glossary format, tables allowed
- Bottom: related terms (TO CHECK)

## Allowed variations
- Body length; with or without tables

## Not allowed
- Images in the body (TO CHECK), a sidebar form, a different body style

## Accessibility and mobile
- Body headings start at h2; the table of contents is a `<nav>`-less list (TO CHECK)
- One column on phones, contents above the body; no sideways scroll at 390px

## Webflow note
- Glossaries template. The TOC script is removed from source.html. Class names are not a concern.
