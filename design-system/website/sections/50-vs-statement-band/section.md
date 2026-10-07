# 50 · vs / Statement band

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/vs/circle, section "Build and monetize in-app community experiences you fully own"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css
- Variant captured: dark, two columns: heading left, paragraph right
- Captured on 2026-10-07 from https://www.social.plus/vs/circle by capture/capture.mjs

## Use it when
One big claim needs one paragraph of explanation, right after a hero. On /vs/ pages it positions social.plus against the competitor in plain words.

## Don't use it when
There is more than one point to make (use the side-by-side, 04) or when the text needs a button (use the CTA band, 12).

## Content slots
- Heading (H2, 8 to 14 words; the live one has 11), left column. `no-wrap` span keeps "in-app" together
- One paragraph (60 to 90 words; the live one has 73), right column, `--text--text-color-grey-light`
- No image, no button

## Allowed variations
- Text length within the ranges. Dark background only (`--social--dark`)

## Not allowed
- Images, buttons, a third column, a heading above the paragraph, light background

## Accessibility and mobile
- `.grid-2`: two equal columns on desktop; stacks (heading, then paragraph) under 768 px
- Section padding `padding_y`; heading uses `--_typography---h2-font-size`
- Plain text, nothing interactive

## Webflow note
- Standard "Section / Grid 2" layout. Class names are not a concern.
