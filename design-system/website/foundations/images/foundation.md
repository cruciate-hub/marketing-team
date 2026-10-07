# Image ratios

The image ratio classes of the style guide.

- Status: draft (2026-10-07), as-is: current live values, no team decision applied · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/styleguide (images block)
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`)

## Values as measured
- `.image-16-9`, `.image-2-1`, `.image-3-1`, `.image-3-2`: max-width 100%, `aspect-ratio`, 16px radius. The style guide shows Webflow placeholder images; the preview swaps in one site image per class (the gaming hero cover) so the ratio and radius show
- `.image-4-3`: no radius (the only one)
- Pages mostly use `.image-square_radius` (33 pages), `.image-fw-radius` (9), `.image-full-width_cover` (8) and `.image-3-2` (14); the other ratio classes are used on one or two pages

## Known inconsistencies (as-is, no decision applied)
- `.image-4-3` has no radius while the other four have 16px
- Image radii across the site: 16px (ratio classes, thumbnails), 1rem and 1.5rem (rich text), .5rem (cards); no radius token
