# Spacing and containers

The spacing steps, section rhythm, gutter, grid gap and containers every page uses. They follow the web library (decision 8 October 2026, Amadeus; not yet in Webflow); the live values are measured below for reading the captured sections.

- Status: draft (2026-10-08): the steps, section rhythm, gutter, grid gap and containers are decisions (Amadeus); the measured values are as-is · Owner: Stefan · Approved by: Amadeus (decisions); measured values TO CHECK (Stefan or Amadeus)
- Source: the web library (Foundations > Layout: grid and frame, spacing, section rhythm); the live values from https://www.social.plus/styleguide and the stylesheet rules for `.section.padding_y`, `.page-padding`, `.grid-2/3/4`

## Spacing steps (use these)

Nine steps on a 4px grid. Every gap, margin and padding uses one of them.

| Token | Value | Typical use |
|---|---|---|
| `space-3xs` | 4px | Icon to label, badge padding |
| `space-2xs` | 8px | Inside buttons and chips, label to input |
| `space-xs` | 12px | Eyebrow to heading, between buttons |
| `space-s` | 16px | Heading to paragraph, card gaps on phones |
| `space-m` | 24px | Button padding, gaps inside cards |
| `space-l` | 32px | Card padding, hero lead to buttons |
| `space-xl` | 48px | Heading block to its grid |
| `space-2xl` | 64px | Hero text to its visual |
| `space-3xl` | 96px | The largest gap inside a section |

## Section rhythm, gutter and grid gap

Fluid between a 360px and a 1440px screen (Layout tokens).

| Token | 390px | 1440px | Use |
|---|---|---|---|
| `section-pad-s` | about 49px | 80px | Logo walls, bands, thin sections |
| `section-pad-m` | about 65px | 112px | The default for every section |
| `section-pad-l` | about 82px | 144px | Heroes, the closing CTA |
| `gutter` | 20px | 40px | Page padding left and right |
| `grid-gap` | 16px | 32px | Gaps in grids that are not frame cells |

The default section padding grows from the live 80px to 112px on desktop: pages get more room between sections. Do not add a spacer to "give it air"; pick the padding size instead.

## Containers

| Token | Width | Use | Live equivalent |
|---|---|---|---|
| `container-l` | 1280px | Default for sections; the frame lines sit on its edges | `container-large` (same) |
| `container-m` | 1024px | Pricing, tables, text-heavy sections | `container-medium-large` 1040px |
| `container-s` | 768px | Centred heroes, FAQ, articles | `container-medium` 760px |
| (none) | | | `container-small` 480px, forms (TO CHECK: a form container in the library) |

Breakpoints are Webflow's defaults, desktop first: 992px and up (12 columns), 768 to 991px (most sections stack to 2), 480 to 767px (1 column, the logo wall 2), below 480px (1 column). The 12-column grid, the column inset and the frame come with the frame step.

## Live values as measured (7 October 2026)
- Steps: xs .3rem = 4.8px · s .625rem = 10px · m 1.5rem = 24px · l 3.125rem = 50px · xl 6rem = 96px (4rem under 768px; `.margin-bottom_xl` only). Classes: `.padding_<step>`, `.padding-top/-bottom/-left/-right_<step>`, same for `.margin…`
- Section rhythm: `.section.padding_y` 5rem top and bottom (3rem under 480px); `.is-first` drops the top padding. 103 of 103 pages use it
- Page gutter: `.page-padding` 2.5rem (1.5rem under 992px, 1rem under 480px); the nav uses the same three values
- Containers (max-width): `.container-large` 80rem = 1280px (102 pages) · `.container-medium-large` 65rem = 1040px (12) · `.container-medium` 47.5rem = 760px (15) · `.container-small` 30rem = 480px (1). `.container-heading` centres a heading block (67 pages); `.max-ch-NN` caps a paragraph at NN characters
- Grids: `.grid-2` 4rem column and row gap (token `grid-2-gap`), 2rem vertical padding; `.grid-3` and `.grid-4` collapse to 2 columns under 992px and 1 under 480px

## Known inconsistencies of the live values
- The steps are not a scale (ratios 2.1 / 2.4 / 2.1 / 1.9) and the stylesheet mostly uses other values: 1rem ×447, 1.5rem ×298, .5rem ×242, 2rem ×247, 2.5rem ×139, .75rem ×112, plus px values (10, 16, 14, 20, 8, 12px); the named steps appear 13 to 15 times each
- Section padding (5rem) and the page gutter (2.5rem) are not steps. Audit open question 8 proposes a 0.25rem scale
- The style guide labels `.container-medium-large` as 60rem / 960px; the CSS says 65rem = 1040px
