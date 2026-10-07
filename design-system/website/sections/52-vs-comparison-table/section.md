# 52 · vs / Comparison table

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/vs/circle, section "The full comparison"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css
- Variant captured: 5 category pills plus a table with two value columns
- Captured on 2026-10-07 from https://www.social.plus/vs/circle by capture/capture.mjs

## Use it when
A page compares social.plus with one named competitor, feature by feature.

## Don't use it when
There is no second column to compare against. Use the feature grid (12) or the side-by-side (51) instead.

## Content slots
- Heading (H2, max 6 words; live: "The full comparison") and one intro line (max 20 words)
- Pills: 3 to 5 feature categories; live: Social, Chat and video, Monetization, Analytics and moderation, Developer experience. The active pill has a blue outline and blue text (`w--current`)
- One `<tbody>` per category. Rows per category on the live page: 9, 3, 7, 5, 6. Each row: capability name (bold white) with a one-line description below it (grey), the social.plus value, the competitor value
- Values: a white check mark ("Yes"), a grey dash ("No"), or a short note chip (up to 5 words, for example "Discussion threads only"). Facts come from `messaging/product-capabilities.md`
- Column heads: "CAPABILITY" in small caps; the social.plus logo; the competitor wordmark. The social.plus column sits on a blue-to-dark gradient card, the competitor column on a dark card

## Allowed variations
- Number of pills (3 to 5) and rows. Dark background only

## Not allowed
- New colours, icons instead of check/dash/chip, a third value column, animation beyond the pill switch, light background

## Accessibility and mobile
- A real `<table>` with `<caption>` (visually hidden), `<thead>` with `scope="col"`, row headers with `scope="row"`; pills are `<button aria-pressed aria-controls>` inside a `role="group"`
- Without JavaScript all categories show (which is what `source.html` does, so the file is about 2160 px taller than the live screenshot, where one category shows); the screenshot shows the Social category
- Phones: pills in one row that scrolls sideways inside the section; the page itself has no sideways scroll at 390 px. The two value columns narrow to 23% each; the table stays readable
- Reduced motion: instant category switch

## Webflow note
- Custom section; the pill script is not in source.html. Class names are not a concern.
