# Recipe: an SDK hub page, framed (interim)

The framed version of a product family's SDK hub (https://www.social.plus/social/sdk, /chat/sdk, /video/sdk): one page that lists every platform SDK of the family. First page of the redesign rollout (wave 1). Built and reviewed on the Claude Design canvas "Social SDK framed" (https://claude.ai/artifact/CvjvLtvLj37K399rnwf6ZZ, artboard v6), with Amadeus's notes of 27 October 2026 and Stefan's of 27 and 28 October 2026.

- Status: draft (2026-10-28) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Interim: until the framed navigation, sub-nav and footer ship site-wide (rollout wave 4), the page uses the current ones, and the hero sits outside the frame. This is the one allowed mix of current and framed on a page (feedback 22). When the framed global sections ship, F01 and F16 replace them and the hero joins the frame.
- For a single-platform SDK page (/social/sdk/ios …) use `sdk-page.md` (current look only).

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| G1 | Nav (current) | none (shared) | the live layout: one 1280px card, logo left, menu centred, Contact Sales pill with arrow circle right |
| G2 | Sub-nav (current) | the family's links | inside the same card under a hairline: Overview, the family toggle with its icon and arrow, Features, SDK, UIKit, Docs with the external-link icon; the current page white with a 3px white underline on the card's bottom edge, the rest grey |
| F03 | Hero / Split, without the frame | row of platform marks, eyebrow (the SDK name, Geist Mono), H1 5 to 9 words, lead 25 to 45 words, Contact Sales (blue) + Documentation (secondary), the UI ↔ code slider in the visual cell | no `is-ruled`, no `frame` class and no middle line; text left, visual right (not `is-reversed`). Marks white (feedback 20), React Native shares React's mark so it is not repeated |
| F04 | Logo wall (inline) | customers | the frame starts here |
| F07 | Feature grid, 4 columns (`is-4col`) | section header (eyebrow, H2, lead); one cell per platform SDK: white platform mark in the icon tile, "<Platform> <Family> SDK", one sentence, "Learn more →" and "Docs ↗" | complete rows only (4 or 8 cells); both links as on the live cards (feedback 21) |
| CTA | CTA band (`section_cta-band`, F15) | heading, line, one primary button | the proposed "CTA with routes" (`../proposals/2026-10-27-cta-routes.md`) may replace it once approved |
| G5 | Footer (current) | none (shared) | the live footer, rebuilt to match `../global/footer/` |

## The hero visual: UI ↔ code slider

The live page's idea, kept: a feed post and the code that renders it, split by a draggable line.

- One card (radius 28px, `#202022`, the single focal shadow). Left of the line the post: avatar, name, time, two text bars, two photos, like and comment chips, a small avatar stack. Right of the line the same post as code (system monospace on `#161616`), a file name and the label "Illustrative example".
- The line is the page's one accent in the visual: `color-link` 2px, a `color-accent-fill` round handle with a left-right arrow. It sweeps slowly until someone grabs it; then it follows the pointer and the arrow keys (a transparent range input covers the card). No animation under reduced motion.
- No blue glow and no art-panel gradient behind it (Stefan, 27 October 2026).
- Photos are editable slots (`avatarSrc`, `photo1Src`, `photo2Src` in the artboard's Tweaks › Photos), so Claude can swap them. The avatar comes from the design system's avatar set (`api/assets/Avatars.md`); the post photos from the live page's own hero image. Names on screen are fictional.
- The code uses only fields the live page's code shows (`postedUser`, `data`, `reactionsCount`, `commentsCount`, `myReactions`); have it checked or replace it with a snippet from the docs before it ships.

## Rules for the page

- Every primary and secondary button carries the arrow circle (`.button_circle`, feedback 19).
- Platform and language marks are white everywhere on the page (feedback 20).
- Nothing is added that the live page or the set does not have; where the page needs something new, it is proposed first.
- Before delivery, go through the definition of done in `../../README.md`.
