# G3 · Breadcrumb bar

> Legacy: feedback 30 (11 Nov 2026) settled the breadcrumb as the one-line `cc-res-crumbs` style ("Parent / Current", never the old chevron bar). This chevron bar is still live on the Customer Stories and Tutorials templates until they move to `cc-res-crumbs`; it follows the same gap rule (feedback 38) meanwhile.

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/customer-story/activerse, `div.breadcrumb-bar` (`.c-dark`)
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (dark, `.c-dark`); `--light` (https://www.social.plus/tutorials/add-a-vector-database-to-your-gpt-custom-content-bot: the plain class without `.c-dark`)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
An article page that belongs to a collection with an overview page: customer stories, tutorials, FAQ entries, legal pages, people, resources. It is the first thing under the nav, above the article hero or title.

## Don't use it when
Marketing pages, product pages, home, /vs/ pages. Blog posts, answers and glossary entries do not use it on the live site (the glossary header carries its own breadcrumb line, see 04).

## Content slots
- One line: overview link ("Customer Stories") › current page name, or just the overview link with a chevron (live: "Customer Stories" only)
- Nothing else: no icons, no dates

## Allowed variations
- Dark (`.c-dark`) is the one to use; the plain class is how the tutorials template renders it (TO CHECK: both look the same on the dark page background; keep one)

## Not allowed
- More than two levels, a different text size, a background band, breadcrumbs inside the hero

## Accessibility and mobile
- `<nav aria-label="Breadcrumb">` is missing on the live site (TO CHECK: add it); the link is a plain `<a>`
- `<nav aria-label="Breadcrumb">` on the bar, `aria-current="page"` on the current item (set on Customer Stories and Tutorials templates, 17 Nov 2026)
- Spacing (17 Nov 2026, Stefan: "must be systematically correct"): the shared `.breadcrumb-bar` class owns the gap under the floating nav, 2rem top (1.5rem at ≤479px), 0.75rem bottom. Never fix the gap per page with margins on the hero or a spacer div.
- Style: uppercase Geist Mono, grey-muted link (hover white), `›` chevron in grey-dark, current page in link blue.
- Text full width on phones, no sideways scroll at 390px

## Webflow note
- NOT a component: two hand-built copies, Customer Stories Template (`breadcrumb-bar c-dark` > `container-large` > `display-flex is-wrap`) and Tutorials Template (`breadcrumb-bar` > `container-large` > `breadcrumb-wrapper`). Styling lives on the shared classes so both stay identical; any new template copies this markup and these classes, never new ones.

## Site-wide gap rule (approved by Stefan 18 Nov 2026)
- Every breadcrumb sits 32px under the nav (24px at ≤479px), on both systems: `.breadcrumb-bar` (Customer Stories, Tutorials) and `.cc-res-crumbs` (blog, FAQ, glossary, answers, library, news, collateral, Community Corner, Community Framework).
- Owned by the crumb classes: `.cc-res-crumbs` padding-top 2rem / tiny 1.5rem; `.cc-res-crumbs-flush` and `.cc-fw-crumbs` margin-top -3rem / tiny -1.5rem (pulls out of `section padding_y` 5rem / 3rem).
- Removed per-template offsets: `c-glossary` padding-top, `cc-fw-hero` top margins/padding, `cc-fw-hero-left` top padding; Answers hero grid got `grid-2 c-flush-top`.
