# 42 · Customer story body

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/customer-story/activerse, `section#watch-video`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (aside with facts and tags left, rich text with images right)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The body of every customer story, after the hero (41).

## Don't use it when
Any other page type.

## Content slots
- Aside: industry, platform, products used (tags), website link, a "Watch the video" link if there is one (CMS fields)
- Body `.cs-story-rich-text`: h2 sections (challenge, solution, results), paragraphs, quotes, images

## Allowed variations
- Which aside fields are filled; body length

## Not allowed
- A second column of text, forms, the metrics repeated

## Accessibility and mobile
- The aside is sticky on the live site (`position: sticky`); body headings start at h2
- Aside above the body on phones; no sideways scroll at 390px

## Webflow note
- Customer Stories template with the "CC / Customer Stories - Rich Text Styler" embed (kept). Class names are not a concern.
