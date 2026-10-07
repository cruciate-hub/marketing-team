# Tags

The `.tag` pill and its variants: default, `.c-dark`, `.c-new`, `.c-nav-webinar`.

- Status: draft (2026-10-07), as-is: current live values, no team decision applied · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: Live tags from /blog, the release-note template and the footer on /vs/circle
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`)

## Values as measured
- `.tag`: .8rem/500 uppercase, +.025rem tracking, `--social--main-blue` text on `--main--whitesmoke`, radius .36rem, padding .15rem .65rem; the blog grid overrides it to 10.8px with a 2px radius (`.c-inside-thumbnail`)
- `.tag.c-dark`: dark fill for the release-note tags; `.tag.c-grey`
- `.tag.c-new`: #3ccb7f on #093a20 (not tokens), radius 10rem ("New" badge)
- `.tag.c-nav-webinar`: the "Webinar" label in the nav; the "We're hiring" alert in the footer and nav is its own class `.nav-hiring-alert` (`.c-footer`)
- `.pu-tag.is--blue/red/purple/yellow` (product updates) use deleted Webflow variables; not captured (TO CHECK: 5 uses on one template)
- 113 pages, 1,813 occurrences

## Known inconsistencies (as-is, no decision applied)
- Two tag families (`.tag` and `.pu-tag`), colours off-token on `.c-new` and `.pu-tag`
- Four ways to say "round" across pills (999px, 99rem, 100rem, 20rem)
