# Grid and frame

One grid and a visible frame, from the web library: hairlines on the container edges run the full page height, every section starts with a rule, and content is divided by frame lines into cells instead of floating cards. The Frame card in the Foundations group shows every part in dark and light.

- Status: decision (8 October 2026, Amadeus), not yet in Webflow and not yet used by any captured section · Owner: Amadeus
- Source: the web library (Foundations > Layout: grid and frame; Sections > Structure: frame)
- Since 12 October 2026 the web library's framed sections are in the set (`sections/framed/`, the "Framed · …" groups): a page is built either framed, on one frame from the navigation to the footer, or in the current look (the captured sections); the person who asks for the page chooses, and Claude asks when the request does not say (Stefan, 12 October 2026). Framed recipes exist today for the product landing, industry and /vs/ pages. The captured sections do not use the frame and are never wrapped in it

## The grid

- 12 equal columns spanning the frame (`container-l`, 1280px between the frame lines), with no gaps.
- Content sits one `column-inset` (24px to 32px, the dashed line) inside its column edge, so every frame line is a column edge and every text edge lines up down the page.
- Layouts use whole columns: halves (6 + 6: split hero, feature row, split header, all on the column 6/7 edge), thirds (feature grid), quarters (4-column feature grid), sixths (logo wall). A wide split is 5 + 7.
- Breakpoints are Webflow's defaults: 992px and up 12 columns; 768 to 991px most sections stack to 2; 480 to 767px 1 column (the logo wall 2); below 480px 1 column.

## The frame

| Part | Class | Tokens | Rule |
|---|---|---|---|
| Frame lines | `.frame` on `.container-l` | `color-frame` (neutral-850 on dark, neutral-200 on light) | Hairlines on both container edges, full height. Every framed section has them. Kept quiet on purpose (22 October 2026) |
| Inner padding | `.frame_inner` | `frame-inset` | Text inside the frame starts one column inset from the line |
| Section rule | `.is-ruled` on the section | `color-frame` | A full-width hairline at the top of a section |
| Plus markers | (drawn by `.is-ruled .frame`) | `frame-marker` 8px, `color-frame-marker` | Where a section rule crosses a frame line. Rounded ends: one path with round caps, 1.3px thick, used as a mask, on a box 1px larger than `frame-marker` so it stays centred on the crossing (decision 22 October 2026, Amadeus; was 11px with square 1px arms). Decorative |
| Closing rule | `.is-ruled-bottom` on the section, `<span class="frame_end" aria-hidden="true"></span>` last in `.frame` | `color-frame`, `frame-marker`, `color-frame-marker` | The mirror of the section rule: a full-width hairline at the bottom with plus markers on both frame lines. Only where the frame ends (a framed section on its own, or the last framed section before something unframed); never between two framed sections. Stefan, 12 October 2026; not yet in Webflow |
| Cells | `.frame_cells` > `.frame_cell` | `--cells` (3 by default), `--cells-tablet` (2), `cell-pad` | Content divided by 1px frame lines, no radius, no card fill. The cell count fills complete rows |
| Split | `.frame_split` (`.is-wide-right`, `.is-reversed`) | | Two cells divided by one vertical frame line on the 6/7 edge (5/7 wide). Stacks under 992px with a line between |
| Hatched band | `.section_divider` | `divider-band` 48px, `color-frame` | Between major parts of a page; at most two per page |
| Art panel | `.art-panel` | `blue-600` to `blue-900`, `gradient-light-blue`, `purple-500` (light: `blue-200` to `blue-500`, `purple-300`) | Behind hero and feature visuals only. The one place purple is allowed as a tint |

Structure of every framed section:

```html
<section class="section_[name] is-ruled">
  <div class="padding-global">                 <!-- gutter -->
    <div class="container-l frame">            <!-- frame lines -->
      <div class="frame_inner section-pad-m">  <!-- or frame_cells / frame_split -->
        …
      </div>
    </div>
  </div>
</section>
```

The class names are the web library's (Client-First: `section_[name]`, `padding-global`, `container-l`, `frame`, `frame_inner`); the frame exists only in new work, so it takes the new names. In a Webflow build the token values are written as their literal values (none is a Webflow variable yet).

## Rules

- Inside the frame there are cells, not cards: no card fill, no radius, no gap between them; the frame lines do the separating. Cards (`radius-m`, `color-surface`) are for content outside the frame (a pop-up, a floating panel).
- One frame per page: the lines run unbroken from the nav to the footer. A section never draws its own vertical lines outside the container edges.
- Every text edge sits on a column inset. Nothing starts between two insets.
- Cells fill complete rows: 3, 6 or 9 cells in thirds; 4 or 8 in quarters; 6 or 12 in sixths.
- A section closes with a bottom rule only where the frame ends. Between framed sections the next `.is-ruled` is the dividing line; a second rule there would double it.
- Markers, rules and hatched bands are structure, not decoration: never coloured, never animated, never added inside a cell.
- The art panel is the only gradient surface and sits only behind a product visual. No glow, no shadow on the visual inside it.
- Frame lines, markers and bands are decorative (no contrast requirement, `aria-hidden` on the band); they carry no meaning.
- Mobile: the frame lines stay on the gutter edges; cells collapse to 2 columns on tablets and 1 on phones; splits stack with a line between.

## In Webflow (social.plus site)

Build with the site's existing layout classes (`section padding_Y > page-padding > container-large`, grids such as `developer-portal_grid`, cards from `Card / Button` / `card-v1`). Never add a parallel class set for the frame. Frame lines and markers use the modifiers approved on the Developer Portal (31 Oct 2026): `c-framed` on the section, `container-large` and `grid-4`, `frame-marker` (+ `is-right`) for the plus markers, `c-cell` on `card-v1`, `c-tile` on `card-icon-v2`. Never add a parallel set; anything new is proposed to Stefan first.
