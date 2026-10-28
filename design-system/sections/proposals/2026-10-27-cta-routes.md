# Proposed section: CTA with routes

- Status: proposed (2026-10-27) — needs approval by Stefan or Amadeus · Proposed by: Stefan, after Amadeus asked for "a better CTA section for all pages" (27 October 2026)
- Not in the set. Until approved, pages use F15 CTA band (framed) or G4 Footer CTA band (current). Built once on the "Social SDK framed" canvas (https://claude.ai/artifact/CvjvLtvLj37K399rnwf6ZZ, artboard v6).

## What it is for

The last section before the footer on every page. The current band offers one action (Contact Sales) to every visitor; this one keeps that action first and adds a route for the developer and for the visitor who wants proof, so fewer people leave at the end of the page.

## Structure

- On the frame (`section_block is-ruled`, `container-l frame`).
- Top row, 12 columns: left (8) the eyebrow ("Get started"), a large H2 (the band's heading, `cta-band_title` at display size, max 14ch) and the band's line (`cta-band_lead`); right (4) one primary button, `.button.is-large` with the arrow circle.
- Below, `frame_cells` in 3 columns, one route per cell, each a whole-cell link: white icon in an icon tile, a title (20px/600), one sentence (`color-text-muted`), and a text link with an arrow at the bottom:
  - Talk to sales → /contact/contact-sales
  - Start building → the family's docs
  - See it in real apps → /customer-stories
- No photos or avatar stack (removed on review, Stefan, 27 October 2026). No second blue button.

## What it reuses

F15 CTA band (heading and line styles), the frame cells of F07, the icon tile, the live buttons. Nothing new beyond the arrangement.
