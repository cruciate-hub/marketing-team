# 51 · vs / Side-by-side (sticky)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/vs/circle, section "What social.plus delivers beyond the community platform"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css
- Variant captured: 5 blocks, dark, sticky illustration on desktop
- Captured on 2026-10-07 from https://www.social.plus/vs/circle by capture/capture.mjs

## Use it when
The page explains 3 to 5 points in depth, each with its own illustration. On /vs/ pages: what social.plus delivers that the competitor does not.

## Don't use it when
There are more than 5 points or each point fits in one line (use the feature grid, 12). For a straight feature-by-feature check use the comparison table (52).

## Content slots
- Section heading (H2, max 8 words, `max-ch-23`)
- 3 to 5 blocks. Each block: title (H3, 5 to 9 words, 3 rem on desktop), paragraph (55 to 80 words, `--text--text-color-grey-lighter`), illustration
- Illustration: a square card (`--social--dark-card` #161616, radius .75 rem) with stacked image layers (webp, full-card size); `role="img"` with an `aria-label` describing it
- Live /vs/ titles: Social and community layer built inside your app · Full-stack SDKs with complete white-label customization · Monetization built into every surface · AI-powered analytics and insights on data you fully own · Social engagement infrastructure that scales with you

## Allowed variations
- 3, 4 or 5 blocks. Illustrations are made per page in the same style (dark card, blue accents, phone or UI fragments). Dark background only

## Not allowed
- Photos instead of illustrations, buttons inside blocks, alternating left/right layout, light background, fewer than 3 blocks

## Accessibility and mobile
- Desktop (992 px and up): text in the left column (1.24 fr), illustration sticky in the right column; a script swaps the illustration as the matching text block reaches the middle of the viewport and dims the other text blocks to 35%. `source.html` shows the static state: every illustration next to its own text (see the comment in the file)
- Tablet and phone: each illustration sits above its text, builds once when scrolled into view; no sideways scroll at 390 px
- Reduced motion: no builds, no parallax, instant swap
- Images are `alt=""` inside a labelled `role="img"` container; headings are real `<h3>`

## Webflow note
- Custom section with a GSAP ScrollTrigger script (not in source.html). The `data-build`, `data-motion`, `data-depth` and `data-origin` attributes describe each layer's build step and are kept for reference. Class names are not a concern.
