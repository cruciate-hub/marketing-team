# SVG Icon Transformer

Claude skill for transforming any SVG blob into minimal, accessible, inline-embed-ready icon markup. Output is designed to be pasted directly into a Webflow HTML Embed (or any inline `<svg>` use) with sizing and color controlled via CSS on the parent wrapper.

## What it does

- Strips editor noise — XML prologs, DOCTYPE, generator comments, `xmlns:*` declarations, `<metadata>`, unreferenced `<defs>`, wrapper `<g>` elements, Illustrator/Inkscape/Figma/Iconify artifacts.
- Inlines class-based styles — `<style>.st0{fill:#000}</style>` + `<path class="st0" .../>` becomes `<path fill="currentColor" .../>` with the `<defs>` removed.
- Applies correct accessibility defaults — `aria-hidden="true"` for decorative icons (the common case, ~90%), or `role="img" + aria-label` for standalone meaning-bearing icons.
- Uses `width="1em" height="1em"` — the icon scales with the parent's `font-size` and dodges the Safari flex/absolute collapse bug that makes `width="100%"` SVGs render at zero size inside flex or absolutely-positioned children.
- Converts `fill="#000"` and `stroke="#000"` to `currentColor` so icons inherit the parent's CSS `color`.
- Preserves path data exactly — no coordinate rounding, no re-optimization, zero rendering surprises.
- Preserves outline icons (`fill="none" + stroke="..."`), brand colors, and handles sprite-sheet edge cases sensibly.

## When it triggers

Any request to clean, format, or transform SVG markup for embed use. Trigger phrases include "clean this SVG", "format this icon", "make this embed-ready", "Webflow embed version", "prep this for Webflow", or pasted SVG markup with an implicit expectation of transformation.

## What it does NOT do

- Does not re-optimize path data. Use [SVGO](https://github.com/svg/svgo) for aggressive compression. This skill preserves coordinates exactly.
- Does not rasterize. SVG in, SVG out.
- Does not merge, split, or sprite-ify.
- Does not generate surrounding CSS or HTML wrappers. Sizing and color live on the embed's parent in Webflow.

## Decorative vs informative

By default, icons are output as **decorative** (`aria-hidden="true"`) because ~90% of icons in real UIs accompany text labels (nav items, buttons, cards, footer links) — the text provides the accessible name.

Switch to **informative** (`role="img" aria-label="..."`) only when the icon stands alone and must convey meaning without nearby text (icon-only buttons, standalone status indicators). The user must provide the label — the skill will ask if it's missing.

Never combine `aria-hidden="true"` with `role="img"`, `<title>`, or `aria-label` — they contradict each other.

## Target output

**Decorative (default):**

```svg
<svg aria-hidden="true" width="1em" height="1em" viewBox="0 0 24 24">
  <path fill="currentColor" d="..."/>
</svg>
```

**Informative:**

```svg
<svg role="img" aria-label="Search" width="1em" height="1em" viewBox="0 0 24 24">
  <path fill="currentColor" d="..."/>
</svg>
```

## Files

- `SKILL.md` — full transformation rules, strip/keep lists, color handling, edge cases
- `README.md` — this file
