# Imagery

Image ratios as the site's style guide defines them, plus the style rules for product illustrations, photography, blog headers and decorative visuals (formerly `design-system/imagery.md`). One foundation: the shapes an image takes on a page and what goes inside them.

- Status: draft (2026-10-07), as-is: ratio values are current live values, no team decision applied; the style rules are the brand rules of 1 October 2026 (blog headers) and the brand guidelines · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/styleguide (images block) and the live blog, answers and glossary templates
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`); this file is written by hand and survives re-runs

## Ratios as measured
- `.image-16-9`, `.image-2-1`, `.image-3-1`, `.image-3-2`: max-width 100%, `aspect-ratio`, 16px radius. The style guide shows Webflow placeholder images; the preview swaps in one site image per class (the gaming hero cover) so the ratio and radius show
- `.image-4-3`: no radius (the only one)
- Pages mostly use `.image-square_radius` (33 pages), `.image-fw-radius` (9), `.image-full-width_cover` (8) and `.image-3-2` (14); the other ratio classes are used on one or two pages
- Fixed sizes the CMS templates expect (WebP): blog header 1578 × 888 and its thumbnails 724 × 408 and 502 × 283 (all 16:9); answer page image 1240 × 840; glossary concept image 1578 × 888; customer story and product update images per the `webflow-fields.json` of the publishing skills

## Two modes, never mixed on one layout

**Product illustrations** (feature sections, documentation, product pages, empty states): 3D object-based, UI-metaphor driven (toggles, cards, panels, SDK logos), one concept per image. Dark background always (`--social--dark` #111, `--social--dark-gray-background` #1a1a1a, `--social--grey` #222); blue (`--social--main-blue` and the blue gradient stops) is the only accent; everything else in muted dark greys; one soft blue glow on the focal object, never neon. Generous rounding (16 to 24px), layered planes with depth. No human figures, no pink, orange or yellow, no light backgrounds, no flat icon sheets.

**Photography** (campaign heroes, social media, events): people in real collaboration or technology environments; candid, diverse, purposeful, no stock clichés. Dark and high-contrast, cool slightly desaturated grade with a blue shift in the shadows; a dark overlay (`rgba(17,17,17,0.5 to 0.7)`) when text sits on it. No warm or golden grades, no bright high-key images.

**The one exception: blog headers** (also answer page images and glossary concept images). A dark interface scene with a blue glow, anchored by one real element: a cut-out person, a hand holding a phone, faces in avatar slots, a group photo, or official app logos for listicles and comparisons. Rules:
- Dark ground #111 with a soft ultramarine-to-violet glow behind the subject; floating interface cards (posts, chat, stats, charts, notifications, profile chips) in muted dark glass, styled like the product illustrations
- One lit focal element (an ultramarine card or tile) carries the post's point; the rest recedes in grey
- At most one photographic element; logos only official, unaltered, only the products the post names; the post's focus (or social.plus) is the lit tile in front
- No readable text: grey bars stand in for copy; a number appears only when the article quotes it
- Each image starts from the page's own idea: two concepts are drafted (metaphor, lit element, real element), the team picks one; the composition differs from page to page
- Built as editable vectors in the shared Figma image file (brand colour variables, effect and text styles, components with photo slots); reviewed by someone on the team; exported at the exact sizes as WebP. A post whose header already has this style keeps it

**Decorative visuals** (hero backgrounds, dividers, loading states): blurred brand-blue or warm gradient shapes at low opacity, simple rounded shapes at 5 to 15% opacity, or fine grain on #111. Always behind content, never competing with it.

| Context | Mode |
|---|---|
| Feature section, product page, documentation, empty state | Product illustration |
| Marketing hero | Photography or gradient abstract |
| Blog post header, answer page image, glossary concept image | Blog header (dark UI scene + one photographic element) |
| Customer story | Photography (the customer's own people or product) |
| Section divider, background texture | Decorative visual |
| Email header | Gradient abstract or product illustration |

## Known inconsistencies (as-is, no decision applied)
- `.image-4-3` has no radius while the other four have 16px
- Image radii across the site: 16px (ratio classes, thumbnails), 1rem and 1.5rem (rich text), .5rem (cards); no radius token (see the shadows-and-radius foundation)
- Older blog headers are pastel illustrations; they are replaced when a post is rewritten, not all at once
