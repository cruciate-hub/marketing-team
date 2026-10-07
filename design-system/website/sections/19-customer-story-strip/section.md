# 19 · Customer story strip

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/chat, section "Leading brands grow with social.plus"
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (heading, intro; 5 story cards with photo, gradient overlay, logo and headline; one button); `--six-stories` (https://www.social.plus/customer-story/activerse, `<aside>`: 6 cards under a customer story, "More in-app communities powered by social.plus")
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
Social proof near the end of a product, industry or overview page, and as the related list at the end of a customer story.

## Don't use it when
The page already has the tabbed customer stories (53) or a quote carousel (26) right next to it; on a page with the logo wall (10), keep the two apart.

## Content slots
- Heading H2, 4 to 7 words (live: "Leading brands grow with social.plus", "Real results, from real apps"); intro 15 to 25 words
- Cards `.cs-cta_link-block` from the CMS (Customer Stories): photo with a dark gradient overlay, customer logo, headline (the story title, 8 to 12 words); the card is the link
- 3 to 6 cards in one row (5 on product pages, 6 under a story); one grey button ("All customer stories") TO CHECK

## Allowed variations
- 3 to 6 cards; which stories; with or without the button

## Not allowed
- Cards without a photo, a second row, a light background, a carousel

## Accessibility and mobile
- Each card is one `<a>` with the headline as its text; photos are decorative on the live site (TO CHECK)
- The row scrolls sideways inside the section on phones (no page sideways scroll at 390px)

## Webflow note
- Webflow components "Section / Customer Stories" (12) and "CC / Customer Stories Section" (26) render the same cards. Class names are not a concern.
