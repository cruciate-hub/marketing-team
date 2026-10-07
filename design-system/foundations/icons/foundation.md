# Icons

The icons the live site uses: inline SVG interface icons that take the text colour (arrow, checkmark, external link, chevron, info mark, nav and social glyphs) and feature glyphs as image files inside two holders (white shapes in the blue circle, blue-gradient shapes in the grey square). The two site stylesheets load no icon font.

- Status: draft (2026-10-07), as-is: current live use, no team decision applied; replaces the former `design-system/iconography.md` · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: the captured sections (buttons 23, pricing table 61, FAQ 18, docs cards 13, nav G1, footer G5, bordered cards 14, icon cards 13, Why social.plus 20) and the Webflow component instance counts taken on 7 October 2026 by the site audit (quoted in the table)
- Preview: preview.html (hand-made; the SVGs are read from the captured sections, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Not produced by capture/: the preview is written by hand and survives re-runs

## Values as measured

| Icon | Markup | Size | Colour | Where |
|---|---|---|---|---|
| Arrow (Webflow component Icon / Arrow, 1,234 instances) | inline SVG `.arrow-social`, `viewBox 0 0 24 25`, `fill="currentColor"`, `aria-hidden="true"` | `.arrow-social` is 1.75rem (`--cta-button_icon-size`; 1.65rem under 480px) with .25rem padding, so the glyph draws at 1.25rem; the circle (`.button-icon_wrapper`) has no size of its own and wraps the arrow | white on `--social--main-blue` (`.button-icon_wrapper`); `.c-grey` holder `--border--border-dark-grey` on the secondary button | every primary and secondary button, the footer CTA |
| Arrow, small | `.arrow-social.c-small` | 1rem | inherits (white, grey on hover) | text links (`.text-link`) |
| Checkmark (Icon / Checkmark, 50) | inline SVG, circled check, `viewBox 0 0 16 16`, in `.checkmark-icon` | 1rem | `--social--main-blue` (white with `.c-pricing-top`) | pricing plan cards (60), pricing table (61), checklist two-column (11) |
| External link (Icon / External link, 32) | inline SVG in `.icon-small` | 1rem | inherits | documentation cards (13 v3-docs) |
| Chevron | `.accodrion-icon` embed, `width="1em"` | 1.1rem = 17.6px (`1em` of the inherited body size; the embed sits next to the 1.2rem question, not inside it) | inherits (`--text--text-color-grey-light`) | FAQ rows (18), additional fees (62); rotates when open (script) |
| Info mark | `.pricing_icon-info` | 1.15rem | `--main--white`, `--text--text-color-grey-medium` on hover | pricing tooltips (61) |
| Nav glyphs | `.nav-icon-embed`, 9-dot grid and others | 1rem | inherits (white) | mega menu (G1), sub-nav (G2) |
| Social glyphs | brand SVGs with `<title>` and `<desc>`, `role="img"`, in `a.footer-social-link` | 1.5rem | #d0d0d1 (typed as a hex; the value of `--border--border-med-grey`), `--social--main-blue` on hover | footer (G5): LinkedIn, X, Instagram, YouTube |
| Feature glyph, bordered card | `img.icon-full` (SVG file; the ones the sections use are in `assets/media/`) in `.card-icon-v1` | 3rem = 48px circle, radius 99rem, .125rem padding | white filled shape (`fill="white"` in the file) on `--social--main-blue` | card-v1 (14), SDK cards |
| Feature glyph, icon card | `img.icon-full` in `.card-icon-v2` | 4.5rem = 72px square, radius .5rem (3rem under 480px) | filled shape with a blue gradient in the file, #5c6ef8 to #1b89dc (not tokens), on #2b2b2b (not a token) | card-v2 and v3 (13) |
| Tile image, not a glyph | `img.product-details_img-1` WebP (file 616 × 742) | width 100% of the tile, pinned to its bottom | white shapes on the dark tile | Why social.plus (20): the "icons" of the reasons are tile images (TO CHECK: a glyph set for this section) |

## Rules

- Interface icons are inline SVG with `fill="currentColor"`: they inherit the text colour, so a hover or a grey variant needs no second file. Decorative icons carry `aria-hidden="true"`; an icon that is the only content of a link carries a `<title>` or the link carries `aria-label`.
- One style per family: the interface glyphs are single-colour shapes (`fill="currentColor"`; the external-link glyph is the one stroked outline), the checkmark and the info mark are filled circles. Do not mix a third style into a section.
- Sizes as used: 1rem for the text-link arrow, external link, checkmark and nav glyphs; 1.1rem the FAQ chevron; 1.15rem the info mark; 1.5rem the social glyphs; 1.75rem the button arrow and its circle (1.65rem under 480px); 48px and 72px holders for feature glyphs (the 72px holder is 48px under 480px). No other sizes.
- Blue is the only accent: the button circle and the card-v1 circle are `--social--main-blue`; interface glyphs are white or inherit the text colour; the card-v2 feature glyphs carry the blue gradient fill of their file; the footer social glyphs are #d0d0d1 and turn `--social--main-blue` on hover. No other coloured icons.
- Feature glyphs are files (SVG) in Webflow assets; every glyph the captured sections and previews show is in the repo (`assets/media/`, copied as served). A new one follows the look of the holder it goes into (white filled shape for `.card-icon-v1`, blue-gradient filled shape for `.card-icon-v2`; stroke weight and cap style are not documented: TO CHECK) and goes into one of the two holders. Do not draw a new icon style for a page; propose it (see `sections/README.md`).
- Pair icons with text. An icon alone carries no meaning in body copy and does not localise.

## Differences from the former iconography.md (now removed)

- The two site stylesheets load no icon font; the former file prescribed Material Symbols Outlined with variable axes. What the site has is a handful of inline SVG embeds and image glyphs, listed above. (The AI pages, outside the section set, load Material Symbols as page-level head code; `claude-design-to-webflow` pitfalls 46 to 48 describe the trouble that gives. New pages use inline SVG.)
- The former colour table (`rgba(255,255,255,0.7)` default, `#7B94FE` accent on dark) is not what the site renders: icons are white or inherit; the accent is `--social--main-blue` as a holder, never as a glyph colour on dark (2.84:1).
- Sizes: the former 16 / 20 / 24 / 32 / 40 / 48px scale is not what the site uses; the sizes in use are 1rem, 1.1rem, 1.15rem, 1.5rem, 1.75rem and the 48px and 72px holders (above).

## Known inconsistencies (as-is, no decision applied)
- `.card-icon-v2` background #2b2b2b is not a token; the audit suggests `--social--light-grey` #444 or a new token
- Two feature-glyph styles: white shapes in the v1 circle, blue-gradient shapes (#5c6ef8 to #1b89dc, not tokens) in the v2 square
- The footer social glyphs are #d0d0d1 typed as a hex, not `--border--border-med-grey`
- The X (Twitter) footer glyph's `<title>` says "Social+'s Twitter Profile" and the Instagram one says "social.plus Instagram Profile" (no possessive); the wording differs per glyph
- Chevron class is spelled `.accodrion-icon` on the site; `.accordion-icon` is the wrapper
- The arrow glyph is 24x25, not square; it sits 0.5px low in a round holder
