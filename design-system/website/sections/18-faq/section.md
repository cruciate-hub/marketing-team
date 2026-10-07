# 18 · FAQ accordion

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/vs/circle, section "FAQ"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css
- Variants captured: default (dark, radial-gradient background, CMS questions, first answer open); `--border-top` (https://www.social.plus/ai/mcp-server: the same accordion on the plain dark background with a 1px top border; a long list collapsed to 30rem with an "Expand" overlay, as live; the script expands it). The pricing FAQ is rich text, not this section
- Captured on 2026-10-07 from https://www.social.plus/vs/circle by capture/capture.mjs

## Use it when
A page has 5 to 10 real questions buyers ask, near the end of the page, before the closing CTA band.

## Don't use it when
There are fewer than 5 questions (put the answers in the copy) or the questions are marketing claims in disguise.

## Content slots
- Heading: "FAQ" (H2 at H3 size, centred). TO CHECK: whether "Frequently asked questions" is also allowed
- 5 to 10 items (live: 9). Each item: question (H3, 1.2 rem, white, one or two lines) with a chevron on the right; answer as rich text (one paragraph, 60 to 120 words, grey) that opens on click
- Live questions: What is the difference between social.plus and Circle? · What does social.plus offer that Circle doesn't? · What does Circle offer that social.plus doesn't? · Can I use just one part, or do I need the whole platform? · Which platforms do the SDKs support? · Who owns the data, and where is it stored? · How does moderation compare? · How would we move a community from Circle to social.plus? · What is Vise?
- Content width `container-medium` (47.5 rem); items separated by a 1 px `--border--border-dark` line

## Allowed variations
- Number of items (5 to 10). Links inside answers. Radial-gradient background (default) or plain dark with a top border (`--border-top`)
- Long lists (more than 10): the `.faq-long_wrapper` collapses the list with a fade and an "Expand" button (`--border-top` variant)

## Not allowed
- Two columns, icons other than the chevron, images in answers, more than one paragraph per answer (TO CHECK), all items open at once

## Accessibility and mobile
- FAQPage schema.org microdata on the list (`itemscope`, `mainEntity`, `acceptedAnswer`) is kept in source.html
- The live page closes every answer (Webflow interaction sets height 0 and animates on click); `source.html` shows the first answer open and the others closed via static-state CSS. TO CHECK: the question rows are not real `<button>`s, so keyboard users cannot open them
- Full width on phones, questions wrap to two lines; no sideways scroll at 390 px

## Webflow note
- Webflow "Accordion" with a FAQ CMS collection. Class names are not a concern.
