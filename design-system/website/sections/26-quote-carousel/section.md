# 26 · Quote / Carousel

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/, section with the customer quotes (first `section.section.padding_y.overflow-hidden`)
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (one large quote with name, role, company logo and a "Read the story" text link; the logo tabs under it switch the quote)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
Customer voices in their own words on the home page or an overview page: 3 to 5 quotes from the CMS.

## Don't use it when
Only one quote exists (put it in the two-column 11 as text), or next to the customer story strip (19).

## Content slots
- Quote: 25 to 50 words in quotation marks, `blockquote` size (24px/600 white)
- Author: name, role and company on one line; the customer logo; "Read the story" text link (blue variant) to the customer story
- Logo tabs: one logo per quote under the slider (script switches; the first quote shows in source.html)

## Allowed variations
- 3 to 5 quotes. Nothing else

## Not allowed
- Photos of the authors, autoplay without pause, quotes without a story link

## Accessibility and mobile
- Quotes are inside `[role=list]` items; the logo tabs are not buttons on the live site (TO CHECK)
- On phones the quote wraps and the logo row scrolls sideways inside the section; no page sideways scroll at 390px

## Webflow note
- Home-page section (CMS list) with its own `<style>` embed (kept). Class names are not a concern.
