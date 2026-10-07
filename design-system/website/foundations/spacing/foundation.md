# Spacing and containers

The five named steps, the four containers, and the section rhythm and page gutter every page relies on.

- Status: draft (2026-10-07), as-is: current live values, no team decision applied · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/styleguide (padding, margin and container samples) and the stylesheet rules for `.section.padding_y`, `.page-padding`, `.grid-2/3/4`
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`)

## Values as measured
- Steps: xs .3rem = 4.8px · s .625rem = 10px · m 1.5rem = 24px · l 3.125rem = 50px · xl 6rem = 96px (4rem under 768px; `.margin-bottom_xl` only). Classes: `.padding_<step>`, `.padding-top/-bottom/-left/-right_<step>`, same for `.margin…`
- Section rhythm: `.section.padding_y` 5rem top and bottom (3rem under 480px); `.is-first` drops the top padding. 103 of 103 pages use it
- Page gutter: `.page-padding` 2.5rem (1.5rem under 992px, 1rem under 480px); the nav uses the same three values
- Containers (max-width): `.container-large` 80rem = 1280px (102 pages) · `.container-medium-large` 65rem = 1040px (12) · `.container-medium` 47.5rem = 760px (15) · `.container-small` 30rem = 480px (1). `.container-heading` centres a heading block (67 pages); `.max-ch-NN` caps a paragraph at NN characters
- Grids: `.grid-2` 4rem column and row gap, 2rem vertical padding; `.grid-3` and `.grid-4` collapse to 2 columns under 992px and 1 under 480px

## Known inconsistencies (as-is, no decision applied)
- The steps are not a scale (ratios 2.1 / 2.4 / 2.1 / 1.9) and the stylesheet mostly uses other values: 1rem ×447, 1.5rem ×298, .5rem ×242, 2rem ×247, 2.5rem ×139, .75rem ×112, plus px values (10, 16, 14, 20, 8, 12px); the named steps appear 13 to 15 times each
- Section padding (5rem) and the page gutter (2.5rem) are not steps. Audit open question 8 proposes a 0.25rem scale
- The style guide labels `.container-medium-large` as 60rem / 960px; the CSS says 65rem = 1040px
