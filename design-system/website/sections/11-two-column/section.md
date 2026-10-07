# 11 · Two-column / Text + image

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/why-social, `section#main-content` (first section of the page)
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (heading + paragraph left, image right); `--checklist` (https://www.social.plus/chat/sdk/ios: text with a 3-item checklist left, image right); `--image-left` (same page: image left, text with a grey button right, radial-gradient background); `--video-cta` (same page, `<aside>`: eyebrow, text, grey button left, product video right); `--three-rows` (https://www.social.plus/chat: eyebrow + heading, then three alternating text/image rows with grey buttons)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
One idea needs a picture: a feature explained next to a screenshot or illustration. The workhorse of product, SDK and industry pages (39 pages use it).

## Don't use it when
There are more than three ideas in a row (use the feature grid 12 or a card grid 13 to 15), the picture is a customer photo (19), or the text is a list of reasons (20).

## Content slots
- Optional eyebrow `.superscript` (live: "Social Chat", "Discover more")
- Heading: H2 (`.h2-font-size` on an H1 when it is the first section), 5 to 12 words
- Paragraph: 30 to 60 words, line length capped with `.max-ch-44` to `.max-ch-56`
- Optional checklist `ul.list` with `.list-item.is-checkmark`, 3 to 5 items
- Optional buttons: grey `.cta-button.c-grey` (one or two, live: "1:1 Chat", "Group Chat", "UI Kit"); the primary button is for heroes and CTA bands
- Media: one image (rounded, `.image-square_radius` or the page's own class) or a looping product video in the dark frame
- Three-rows variant: one heading block, then up to 3 `.grid-2` rows; the image side alternates (`.is-resp-reversed` flips a row)

## Allowed variations
- Image left or right (`.grid-2.is-resp-reversed`), image or video, with or without checklist, eyebrow and buttons
- Background: plain `--social--dark` or `.c-radial-gradient`; `.is-first` drops the top padding when it is the first section
- Up to three rows in one section (three-rows variant)

## Not allowed
- Two images in one row, text on both sides, centred text, a primary blue button, a form (24), a light background

## Accessibility and mobile
- Headings are real `<h2>` (an `<h1 class="h2-font-size">` when it opens the page). Images need meaningful alt text; the live site often leaves it empty (TO CHECK)
- Videos: `muted`, `loop`, `playsinline`; `autoplay` removed in source.html so the first frame shows
- `.grid-2`: 2 columns with a 4rem gap, 1 column under 992px; the image goes above the text on phones in every variant; no sideways scroll at 390px

## Webflow note
- Plain `.grid-2` sections on the pages, no component. Class names are not a concern.
