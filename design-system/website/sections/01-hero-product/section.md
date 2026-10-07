# 01 · Hero / Product (two-column)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/social/uikit, `section.main-hero`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (image right, primary + secondary button); `--video` (https://www.social.plus/chat: looping product video right, one button); `--two-buttons` (https://www.social.plus/chat/sdk/ios: `header.main-hero`, video right, Contact Sales + Documentation)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
The first section of a product, feature, SDK, UIKit or white-label page: one product, one promise, one call to action.

## Don't use it when
Industry pages (03), /vs/ pages (05), pages without a product image or video (02), articles (04).

## Content slots
- H1: 5 to 9 words (live: "Save time with ready-to-use UIKits", "Build in-app messaging faster with a Chat SDK")
- Paragraph: 25 to 45 words; `.enlarged-paragraph` on the video variant, plain `<p>` on the others (TO CHECK: pick one)
- Buttons: primary "Contact Sales" always; optional secondary grey button (Documentation, Access Figma UI Kit)
- Right column: one product image (rounded, about 1:1) or a looping product video in the dark rounded frame `.product-video-wrapper` (poster shows when the video does not play)

## Allowed variations
- Image or video right; one or two buttons; the `<section>` or `<header>` tag (SDK pages use `<header>`)
- Grid `.main-hero-grid.is-oneven`: text column wider than the media column

## Not allowed
- A form in the hero (that is the form section, 24), three buttons, centred text, a background image or glow, a light variant, a second paragraph

## Accessibility and mobile
- One `<h1>` per page; the video is `muted`, `loop`, `playsinline`, no controls; TO CHECK: the video has no text alternative on the live site
- On phones the text stacks above the media; the media keeps its rounded frame; no sideways scroll at 390px
- Section height about 620px at 1440

## Webflow note
- Webflow components "Page / Chat SDK" and "Page / Social SDK" (hero part). The video `src` is the site's CDN mp4; `autoplay` is removed in source.html so the copy shows the first frame.
