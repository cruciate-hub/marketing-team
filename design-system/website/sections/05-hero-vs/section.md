# 05 · Hero / vs

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/vs/circle, `section.vs-hero`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css
- Variant captured: two brand tiles with glows (the only variant)
- Captured on 2026-10-07 from https://www.social.plus/vs/circle by capture/capture.mjs

## Use it when
The page compares social.plus with one named competitor (a /vs/ page). It is the first section, directly under the nav.

## Don't use it when
Any other page. Product, home and landing pages use the product hero (01), the simple hero (02) or the industry hero (03).

## Content slots
- H1 made of two brand blocks: tile image (rounded square, about 7.5 rem) plus brand name, separated by a small "vs"
- Left brand is always social.plus (dark tile with the plus mark); right brand is the competitor (its own tile, white for Circle)
- Background: two blue radial glows (left and right image layers) and a dark vignette in the middle; page background `--social--dark`
- No text below the title, no button. The statement band (50) follows immediately

## Allowed variations
- Competitor tile and name. Nothing else

## Not allowed
- Three brands, a subtitle, buttons, a different glow colour, a light variant

## Accessibility and mobile
- Real `<h1>` with the two names as text ("social.plus vs Circle"); tiles are decorative (`alt=""`)
- Entrance animation (fade, slide, glow breathing) is CSS inside the section and switched off under `prefers-reduced-motion`; desktop mouse parallax is a script and is not in source.html
- On phones the tiles shrink and the title stays on one row; section height about 320 px at 390 wide

## Webflow note
- Built 5 Oct as a custom section on the /vs/ template. Class names are not a concern.
