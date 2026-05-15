---
name: svg-icon-transformer
description: Transform any SVG input into clean, accessible, inline-embed-ready icon markup. Strips editor noise (Illustrator, Inkscape, Iconify, Figma artifacts), applies correct accessibility defaults, and uses `1em` sizing that avoids the Safari flex/absolute collapse bug. Triggers whenever the user pastes SVG code and asks for cleanup, transformation, a Webflow-embed-ready version, or anything similar. Also triggers on phrases like "clean this SVG", "format this icon", "make this embed-ready", or just pasting SVG markup with an implicit expectation of transformation.
---

# SVG Icon Transformer

Transforms any SVG blob into a minimal, accessible, inline-ready icon. Output is designed to be pasted directly into an HTML embed (Webflow HTML Embed, inline `<svg>` in a component, etc.) with sizing and color controlled via CSS on a parent wrapper.

## Target output

**Decorative (default — icon sits next to a visible text label):**

```svg
<svg aria-hidden="true" width="1em" height="1em" viewBox="0 0 24 24">
  <path fill="currentColor" d="..."/>
</svg>
```

**Informative (icon stands alone, conveys meaning without nearby text):**

```svg
<svg role="img" aria-label="Search" width="1em" height="1em" viewBox="0 0 24 24">
  <path fill="currentColor" d="..."/>
</svg>
```

Never combine `aria-hidden="true"` with `role="img"`, `<title>`, or `aria-label` — they contradict each other.

## Accessibility decision

Default to **decorative**. 90%+ of icons in real UIs accompany text labels (nav items, buttons, cards, footer links), and the text provides the accessible name.

Switch to **informative** only when:
- The user explicitly requests it
- The user describes an icon-only button or standalone icon that conveys meaning

When informative, require a short label (e.g. "Search", "Close", "Menu"). If the user hasn't provided one, ask.

## Transformation rules

### Strip from document level
- `<?xml version="..." ?>`
- `<!DOCTYPE svg ...>`
- Editor comments (`<!-- Generator: Adobe Illustrator -->`, `<!-- Created with Inkscape -->`, etc.)

### Strip from root `<svg>`
- `xmlns="http://www.w3.org/2000/svg"` — not needed for inline HTML5
- `xmlns:xlink` — unless the SVG actually uses `xlink:href`
- `xmlns:svg`, `xmlns:dc`, `xmlns:rdf`, `xmlns:cc`, `xmlns:sodipodi`, `xmlns:inkscape` — always strip
- `version`
- `preserveAspectRatio` — `xMidYMid meet` is the default
- `focusable` — obsolete (only IE/pre-Chromium Edge needed it)
- `class` — styling hooks belong on the embed wrapper
- `id` — editor artifact
- Inline `style` — convert to attributes where possible, drop otherwise
- `data-*`
- `xml:space`

### Keep on root `<svg>`
- `viewBox`

### Add to root `<svg>`
- `width="1em"` and `height="1em"` — scales with parent `font-size`, avoids Safari flex/absolute collapse bug
- Accessibility attributes per the decision above

### Child element cleanup

**Strip entirely:**
- `<metadata>`
- `<sodipodi:namedview>` and all Inkscape-specific elements
- `<title>` and `<desc>` — unless in informative mode with explicit label

**Inline styles into path attributes:**
- `<defs><style>.st0 { fill: #fff; }</style></defs>` + `<path class="st0" .../>` becomes `<path fill="#fff" .../>` (with the `<defs>` removed)

**Keep only if referenced:**
- `<defs>` containing gradients, masks, clipPaths, symbols, patterns — strip if nothing in the SVG actually uses them

**Unwrap or preserve `<g>`:**
- Unwrap if it has no attributes, or only wraps a single child with no shared attributes
- Preserve if it carries `transform`, `opacity`, or other attributes used by multiple children

### Path and shape attribute rules

**Strip:**
- `class` (after inlining the style it pointed to)
- `id`
- Inline `style` (convert to attributes)
- Editor attributes (`sodipodi:*`, `inkscape:*`)
- Default values that match SVG defaults (`stroke-miterlimit="4"`, `fill-rule="nonzero"`)

**Keep:**
- `d` (path data) — never modify, never re-optimize
- `fill`, `stroke`
- Stroke attributes when present: `stroke-width`, `stroke-linecap`, `stroke-linejoin`, `stroke-dasharray`
- `fill-rule`, `clip-rule` — if non-default (e.g. `evenodd`)
- `opacity`, `fill-opacity`, `stroke-opacity` — if intentional
- `transform` — if present and non-identity

### Color handling

**Auto-convert to `currentColor`:**
- `fill="#000"`, `fill="#000000"`, `fill="black"` → `fill="currentColor"`
- `stroke="#000"`, `stroke="#000000"`, `stroke="black"` → `stroke="currentColor"`

**Preserve specific colors** (do NOT auto-convert):
- Brand colors, logo colors, any non-black intentional color
- When the SVG originally had `fill="#fff"` (common in icons designed for dark backgrounds), preserve as-is but note in the output commentary that the user may want to swap to `currentColor` for CSS color inheritance

**Stroke-based (outline) icons:**
- If the SVG uses `fill="none"` + `stroke="..."`, preserve the stroke approach — don't force `fill`

## Output formatting

- `<svg>` opening tag on one line, attributes space-separated
- Each `<path>` (or other shape element) on its own line, indented 2 spaces
- Preserve the original `d` attribute exactly — no path optimization, no coordinate rounding
- No trailing whitespace
- Close `</svg>` on its own line

## Handling multiple SVGs in one paste

Process each SVG independently. Output each in its own code block. Number them if helpful.

## Edge cases

**Input is already clean:** Return it with whatever adjustments the rules dictate. Note briefly that it was already close to target format.

**Input is a complex illustration, chart, or multi-color logo:** Flag that the `1em` + `currentColor` pattern may not suit this use case. Offer to preserve original dimensions and colors instead.

**Input is missing `viewBox`:**
- If `width` and `height` attributes are present, construct `viewBox="0 0 {width} {height}"`
- If neither is present, flag the SVG as broken and ask for the original source

**Input uses `<use xlink:href="#id">`:** Keep `xmlns:xlink` on the root and preserve the `<use>` element. Don't convert to `href="#id"` unless explicitly requested (browser support for bare `href` in `<use>` is solid in modern browsers but may fail in older contexts).

**Input is a sprite sheet with `<symbol>` elements:** This is outside the icon-transformation scope. Flag and ask what the user wants — extract a single icon, or treat the whole sheet.

## Output commentary

After transforming, briefly note in 1–2 sentences:
- Which mode was applied (decorative default, or informative with label "X")
- Any preserved non-black hardcoded colors that might warrant review
- If multiple SVGs were processed, a one-line summary per icon

Keep commentary minimal. The transformed SVG is the primary output; prose is secondary.

## What NOT to do

- Don't re-optimize path data (`d` attribute). Path optimization is SVGO's job, and it can introduce subtle rendering differences.
- Don't add `<title>` or `role="img"` to decorative icons — they contradict `aria-hidden="true"`.
- Don't add `xmlns` "just in case". The default use case is inline HTML, where it's noise.
- Don't add `focusable="false"`. It's obsolete.
- Don't wrap the SVG in extra containers or add surrounding CSS. The skill outputs SVG only.
- Don't change `viewBox` coordinates. Keep the original coordinate system.
- Don't invent accessibility labels for informative icons. Ask the user.

## Not in scope

This skill cleans and standardizes SVGs. It does not:
- Compress or optimize file size (use SVGO for that)
- Convert between SVG versions
- Merge or split icons
- Generate sprite sheets
- Rasterize to PNG/JPG

If the user needs any of the above, say so directly.
