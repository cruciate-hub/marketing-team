# Accordion row

The FAQ row (`.accordion_item`) and the feature accordion item (`.add-ons_accordion-item`) as single rows, open.

- Status: draft (2026-10-07), as-is: current live values, no team decision applied · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: Live rows from the FAQ on /vs/circle and the feature accordion on /industry/gaming
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`)

## Values as measured (1440)
- FAQ row `.accordion_item` / `.accordion_top`: 1px bottom border `--border--border-dark`; row padding 12px / 8px; question 19.2px/400 white with a chevron on the right; answer `.accordion_bottom` as rich text (height animated by a Webflow interaction; open here). FAQ on 8 pages
- Feature accordion `.add-ons_accordion-item`: header with `h3.h5-font-size`, body with one line, a timeline line on the left; `.active` opens the item and shows its image (script). 12 pages

## Known inconsistencies (as-is, no decision applied)
- Two accordion families with different borders and paddings; the audit proposes one accordion with a FAQ variant and a feature-with-image variant
- The row headers are not `<button>`s on the live site, so keyboard users cannot open them (TO CHECK)
- FAQ questions are 19.2px/400 where every other heading is 600
