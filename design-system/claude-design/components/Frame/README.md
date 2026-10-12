# Frame

The visible structure every framed section sits in: frame lines on the container edges, a rule with plus markers at the top of each section, cells divided by lines instead of cards, the 6/7 split, the hatched band and the art panel, on the 12-column grid. Web library, decision 8 October 2026; not yet in Webflow.

- **Use** for every new section built on the web library's structure. The full rules, the class structure and the tokens are in the Grid and frame section.
- **Do not use** around the captured live sections: they have their own padding and cards and were not built for it. The "Building a page" rule switches to the frame when the library's framed sections join the set.
- **Consumer provides** the section content (header, cells, visual). The frame itself is CSS only: `.frame`, `.frame_inner`, `.is-ruled`, `.frame_cells` / `.frame_cell` (`--cells`, `--cells-tablet`), `.frame_split` (`.is-wide-right`, `.is-reversed`), `.section_divider`, `.art-panel`, on `.padding-global` > `.container-l`.
- **Tokens:** `color-frame`, `color-frame-marker`, `frame-inset`, `column-inset`, `cell-pad`, `frame-marker`, `divider-band`, `container-l`, `gutter`, `section-pad-*`.
- **Allowed:** 3, 4, 6 or 8 cells per row in complete rows; the split 6/6 or 5/7, either side; at most two hatched bands per page; the art panel behind a product visual only.
- **Not allowed:** cards, radius or gaps inside the frame; coloured or animated lines and markers; a second frame inside a section; the art panel behind text.
- **Accessibility:** lines, markers and bands are decorative and carry no meaning; the hatched band is `aria-hidden="true"`.
- **Mobile:** cells collapse to the tablet count under 992px and to one column under 480px; splits stack with a frame line between.
