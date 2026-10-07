# Icons

The icons the live site uses: inline SVG interface icons that take the text colour (arrow, checkmark, external link, chevron, info mark, nav and social glyphs) and white feature glyphs as image files inside two holders. There is no icon font on the site.

- Status: draft (2026-10-07), as-is: current live use, no team decision applied; replaces the former `design-system/iconography.md` · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: the captured sections (buttons 23, pricing table 61, FAQ 18, docs cards 13, nav G1, footer G5, bordered cards 14, icon cards 13, Why social.plus 20) and the Webflow component list of 7 October 2026
- Preview: preview.html (hand-made; the SVGs are read from the captured sections, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Not produced by capture/: the preview is written by hand and survives re-runs

## Values as measured

| Icon | Markup | Size | Colour | Where |
|---|---|---|---|---|
| Arrow (Webflow component Icon / Arrow, 1,234 instances) | inline SVG `.arrow-social`, `viewBox 0 0 24 25`, `fill="currentColor"`, `aria-hidden="true"` | 1.25rem glyph in a 1.75rem circle (`--cta-button_icon-size`) | white on `--social--main-blue` (`.button-icon_wrapper`); `.c-grey` holder `--border--border-dark-grey` on the secondary button | every primary and secondary button, the footer CTA |
| Arrow, small | `.arrow-social.c-small` | 1rem | inherits (white, grey on hover) | text links (`.text-link`) |
| Checkmark (Icon / Checkmark, 50) | inline SVG, circled check, `viewBox 0 0 16 16` | 1.25rem | `--social--main-blue` | pricing table, checklist two-column (11) |
| External link (Icon / External link, 32) | inline SVG in `.icon-small` | 1rem | inherits | documentation cards (13 v3-docs) |
| Chevron | `.accodrion-icon` embed, `width="1em"` | 1.5rem (font size of the row) | white | FAQ rows (18); rotates when open (script) |
| Info mark | `.pricing_icon-info` | 1rem | `--text--text-color-grey-light` | pricing tooltips (61) |
| Nav glyphs | `.nav-icon-embed`, 9-dot grid and others | 1.5rem | white | mega menu (G1) |
| Social glyphs | brand SVGs with `<title>` and `<desc>`, `role="img"` | 1.25rem | white | footer (G5): LinkedIn, X, Instagram, YouTube |
| Feature glyph, bordered card | `img.icon-full` (SVG from the CDN) in `.card-icon-v1` | 3rem = 48px circle, radius 99rem | white glyph on `--social--main-blue` | card-v1 (14), SDK cards |
| Feature glyph, icon card | `img.icon-full` in `.card-icon-v2` | 4.5rem = 72px square, radius .5rem | white glyph on #2b2b2b (not a token) | card-v2 and v3 (13) |
| Bare glyph | `img` WebP, about 40px | 2.5rem | white | Why social.plus (20), industry pages |

## Rules

- Interface icons are inline SVG with `fill="currentColor"`: they inherit the text colour, so a hover or a grey variant needs no second file. Decorative icons carry `aria-hidden="true"`; an icon that is the only content of a link carries a `<title>` or the link carries `aria-label`.
- Line style, one weight, no fills: the arrow, chevron and external-link glyphs are outlined; the checkmark and the info mark are the two filled circles. Do not mix a third style into a section.
- Sizes as used: 1rem inline, 1.25rem in buttons and lists, 1.5rem for chevrons and nav, 48px and 72px holders for feature glyphs. No other sizes.
- Blue is the only accent: the button circle and the card-v1 circle are `--social--main-blue`; glyphs are white (or inherit). No coloured icons apart from the social brand glyphs, which keep their shape but render white.
- Feature glyphs are files (SVG or WebP) in Webflow assets: new ones follow the same look (white line glyph, 2px stroke, rounded caps) and go into one of the two holders. Do not draw a new icon style for a page; propose it (see `sections/README.md`).
- Pair icons with text. An icon alone carries no meaning in body copy and does not localise.

## Differences from the former iconography.md (now removed)

- The site does not load Material Symbols or any icon font; the former file prescribed Material Symbols Outlined with variable axes. What the site has is a handful of inline SVG embeds and image glyphs, listed above.
- The former colour table (`rgba(255,255,255,0.7)` default, `#7B94FE` accent on dark) is not what the site renders: icons are white or inherit; the accent is `--social--main-blue` as a holder, never as a glyph colour on dark (2.84:1).
- Sizes: the former 16 / 20 / 24 / 32 / 40 / 48px scale maps to 1rem / 1.25rem / 1.5rem and the 48px holder; 32 and 40px exist only as the bare Why social.plus glyphs.

## Known inconsistencies (as-is, no decision applied)
- `.card-icon-v2` background #2b2b2b is not a token; the audit suggests `--social--light-grey` #444 or a new token
- The X (Twitter) footer glyph's `<title>` says "Social+'s Twitter Profile" and the Instagram one says "social.plus Instagram Profile" (no possessive); the wording differs per glyph
- Chevron class is spelled `.accodrion-icon` on the site; `.accordion-icon` is the wrapper
- The arrow glyph is 24x25, not square; it sits 0.5px low in a round holder
