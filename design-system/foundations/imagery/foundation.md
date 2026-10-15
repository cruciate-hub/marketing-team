# Imagery

Image ratios as the site's style guide defines them, plus the style rules for product illustrations, photography, blog headers and decorative visuals (formerly `design-system/imagery.md`). One foundation: the shapes an image takes on a page and what goes inside them.

- Status: draft (2026-10-07), as-is: ratio values are current live values, no team decision applied; the style rules are the brand rules of 1 October 2026 (blog headers) and the brand guidelines · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/styleguide (images block) and the live blog, answers and glossary templates
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`); this file is written by hand and survives re-runs

## The illustration system (since 14 October 2026)

Illustrations and editorial images are made with Amadeus's illustration skills, which carry the rules in full:

- `marketing-team/skills/social-plus-illustration/` — the visual language for every surface: dark #111 ground, design-system neutrals, exactly one accent per image (ultramarine for about 70% of images, another brand colour when the topic calls for it), Figtree and Geist Mono, 2 to 4 big objects that leave the frame, a quiet grey social layer, official third-party logos when the content is about other companies. Grain is an editorial treatment: on for blog, answers and glossary images and anything built from an article, off for website, product and brand work.
- `marketing-team/skills/blog-thumbnails/` — blog headers and thumbnails (1578 × 888, 724 × 408, 502 × 283 WebP), in-blog charts, flows and diagrams (1578 × 888), answer-page images (1240 × 840) and glossary images (in the article body only, 1578 × 888: the Glossary collection has no image field). Built on claude.ai Design canvases, two concepts per image.
- `marketing-team/skills/social-plus-motion/` — loops of a finished static and explainer videos (Reels, shorts).

Where this foundation differs from those skills, the skills win. Superseded below: the product-illustration rule "blue is the only accent, no pink, orange or yellow", the blog-header rules (one photographic element, no readable text, built in the shared Figma image file) and the table row for blog, answer and glossary images. The ratios and the photography rules still apply.

## Ratios as measured
- `.image-16-9`, `.image-2-1`, `.image-3-1`, `.image-3-2`: max-width 100%, `aspect-ratio`, 16px radius. The style guide shows Webflow placeholder images; the preview swaps in one site image per class (the gaming hero cover) so the ratio and radius show
- `.image-4-3`: no radius (the only one)
- Pages mostly use `.image-square_radius` (33 pages), `.image-fw-radius` (9), `.image-full-width_cover` (8) and `.image-3-2` (14); the other ratio classes are used on one or two pages
- Fixed sizes the CMS templates expect (WebP): blog header 1578 × 888 and its thumbnails 724 × 408 and 502 × 283 (all 16:9); answer page image 1240 × 840 (field `image-2`, optional); glossary: no image field, images go in the article body at 1578 × 888; customer story and product update images have no fixed size on record (TO CHECK)

## Two modes, never mixed on one layout

**Product illustrations** (feature sections, documentation, product pages, empty states): *Since 14 October 2026 made in the social-plus-illustration system (clean, no grain); its one-accent-by-meaning rule replaces "blue is the only accent, no pink, orange or yellow" below.* 3D object-based, UI-metaphor driven (toggles, cards, panels, SDK logos), one concept per image. Dark background always (`--social--dark` #111, `--social--dark-gray-background` #1a1a1a, `--social--grey` #222; the former brand file said #111111, #1e1e1e, #272727 and the existing illustration files follow those: TO CHECK which set new work uses); blue (`--social--main-blue` and the blue gradient stops) is the only accent; everything else in muted dark greys; one soft blue glow on the focal object, never neon. Generous rounding (16 to 24px), layered planes with depth. No human figures, no pink, orange or yellow, no light backgrounds, no flat icon sheets.

**Photography** (campaign heroes, social media, events): people in real collaboration or technology environments; candid, diverse, purposeful, no stock clichés. Dark and high-contrast, cool slightly desaturated grade with a blue shift in the shadows; a dark overlay (`rgba(17,17,17,0.5 to 0.7)`) when text sits on it. No warm or golden grades, no bright high-key images.

**The one exception: blog headers** (also answer page images and glossary concept images). *Superseded on 14 October 2026 by the blog-thumbnails skill (see the top of this file); kept for the record.* A dark interface scene with a blue glow, anchored by one real element: a cut-out person, a hand holding a phone, faces in avatar slots, a group photo, or official app logos for listicles and comparisons. Rules:
- Dark ground #111 with a soft ultramarine-to-violet glow behind the subject; floating interface cards (posts, chat, stats, charts, notifications, profile chips) in muted dark glass, styled like the product illustrations. Two deliberate exceptions to the illustration rules: the photographic element below, and official third-party logos in comparisons, which keep their own colours
- One lit focal element (an ultramarine card or tile) carries the post's point; the rest recedes in grey
- At most one photographic element (a cut-out person, portrait or half body; a hand holding a phone; faces in avatar slots; a group photo). Photos follow the photography treatment and people guidelines: dark, cool grade, no warm tones, real-feeling people, cut out cleanly where the slot asks for it
- Logos only official, unaltered, only the products the post names; the post's focus (or social.plus) is the lit tile in front
- No readable text: grey bars stand in for copy; a number appears only when the article quotes it, no made-up counters
- Each image starts from the page's own idea: two concepts are drafted (metaphor, lit element, real element), each guided by the reference headers that fit it, and the team picks one. The shared kit keeps images on brand; the composition differs from page to page rather than repeating a recent layout
- Built as editable vectors in the shared Figma image file (brand colour variables, effect and text styles, components with photo slots); reviewed by someone on the team before it goes live; exported at the exact sizes as WebP. A post whose header already has this style keeps it

**Decorative visuals** (hero backgrounds, dividers, loading states): blurred brand-blue or warm gradient shapes at low opacity, simple rounded shapes at 5 to 15% opacity, or fine grain on #111. Always behind content, never competing with it.

| Context | Mode |
|---|---|
| Feature section, product page, documentation, empty state | Product illustration, in the social-plus-illustration system (clean, no grain) |
| Marketing hero | Photography or gradient abstract |
| Blog post header, answer page image, glossary in-article image | blog-thumbnails skill (editorial, grain on) |
| Customer story | TO CHECK (no rule in the former brand file) |
| Section divider, background texture | Decorative visual |
| Email header | Gradient abstract or product illustration |

## Known inconsistencies (as-is, no decision applied)
- `.image-4-3` has no radius while the other four have 16px
- Image radii across the site: 16px (ratio classes, thumbnails), 1rem and 1.5rem (rich text), .5rem (cards); no radius token (see the shadows-and-radius foundation)
- Older blog headers are pastel illustrations; one is replaced only when a new header in this style is approved. A rewrite of the post does not touch its image fields (`blog-seo-content`)
