# Dividers

The `.divider` line and the text divider of the logo wall.

- Status: draft (2026-10-07), as-is: current live values, no team decision applied · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/styleguide (`.divider`) and the logo wall on /vs/circle (`.text-divider`)
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`)

## Values as measured
- `.divider`: 1px, `--border--border-light-grey` #e7e7e7 (a light grey line on a dark site); `.divider-v2` exists on 1 page
- `.text-divider`: a `.superscript.c-divider` line ("Trusted by some of the world's biggest brands") between two `.divider.c-divider` lines that fade to `--text--text-color-grey-medium` (the right one `.c-reversed`)
- Section separators elsewhere are `border-top` on the section (`.border-top`, see section 18 `--border-top`) with `--border--border-dark`

## Known inconsistencies (as-is, no decision applied)
- The style guide divider colour (#e7e7e7) is a light-mode value; dark pages use `--border--border-dark` #232324 for the same job
