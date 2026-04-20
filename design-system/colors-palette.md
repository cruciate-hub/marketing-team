# social.plus Colour System — Palette

Source of truth: Figma `Social--Website-Production` → Design System page (node `239:289`)
https://www.figma.com/design/hLl6r9XhWxZdZUUDwhGGAB/Social--Website-Production?node-id=239-289

Fetch alongside `colors-usage.md` for gradients, usage principles, and Webflow CSS variables.

The palette is a two-layer system:
1. **Primitive scales** — six colour families (plus Black and White) on a 50–950 step scale.
2. **Semantic tokens** — named roles (primary, hover, body text, border, etc.) that map to primitives. Use semantic tokens in component CSS. Reach for primitives only when no semantic token fits.

---

## 1. Primitive colour scales

### Neutral

| Token | HEX | RGB |
|-------|-----|-----|
| `neutral-white` | `#FFFFFF` | rgb(255, 255, 255) |
| `neutral-black` | `#000000` | rgb(0, 0, 0) |

### Slate (greys)

| Token | HEX | RGB |
|-------|-----|-----|
| `slate-50`  | `#FAFAFA` | rgb(250, 250, 250) |
| `slate-100` | `#F5F5F5` | rgb(245, 245, 245) |
| `slate-200` | `#E6E6E6` | rgb(230, 230, 230) |
| `slate-300` | `#D3D3D3` | rgb(211, 211, 211) |
| `slate-400` | `#A3A3A3` | rgb(163, 163, 163) |
| `slate-500` | `#727272` | rgb(114, 114, 114) |
| `slate-600` | `#535353` | rgb(83, 83, 83) |
| `slate-700` | `#404040` | rgb(64, 64, 64) |
| `slate-800` | `#272727` | rgb(39, 39, 39) |
| `slate-900` | `#1A1A1A` | rgb(26, 26, 26) |
| `slate-950` | `#111111` | rgb(17, 17, 17) |

### Ultramarine (primary brand family)

| Token | HEX | RGB |
|-------|-----|-----|
| `ultramarine-50`  | `#EDF4FF` | rgb(237, 244, 255) |
| `ultramarine-100` | `#DFE9FF` | rgb(223, 233, 255) |
| `ultramarine-200` | `#C4D5FF` | rgb(196, 213, 255) |
| `ultramarine-300` | `#A1BAFF` | rgb(161, 186, 255) |
| `ultramarine-400` | `#7B94FE` | rgb(123, 148, 254) |
| `ultramarine-500` | `#5C6EF8` | rgb(92, 110, 248) |
| `ultramarine-600` | `#3B41EC` | rgb(59, 65, 236) ← brand hero |
| `ultramarine-700` | `#3133D1` | rgb(49, 51, 209) |
| `ultramarine-800` | `#2B2FA8` | rgb(43, 47, 168) |
| `ultramarine-900` | `#2A2F85` | rgb(42, 47, 133) |
| `ultramarine-950` | `#191B4D` | rgb(25, 27, 77) |

### Picton Blue

| Token | HEX | RGB |
|-------|-----|-----|
| `picton-blue-50`  | `#F1F7FE` | rgb(241, 247, 254) |
| `picton-blue-100` | `#E2EFFC` | rgb(226, 239, 252) |
| `picton-blue-200` | `#BEDEF9` | rgb(190, 222, 249) |
| `picton-blue-300` | `#84C2F5` | rgb(132, 194, 245) |
| `picton-blue-400` | `#45A5ED` | rgb(69, 165, 237) |
| `picton-blue-500` | `#1B89DC` | rgb(27, 137, 220) |
| `picton-blue-600` | `#0D6BBC` | rgb(13, 107, 188) |
| `picton-blue-700` | `#0C5598` | rgb(12, 85, 152) |
| `picton-blue-800` | `#0E497E` | rgb(14, 73, 126) |
| `picton-blue-900` | `#123E68` | rgb(18, 62, 104) |
| `picton-blue-950` | `#0C2745` | rgb(12, 39, 69) |

### Pink Flamingo

| Token | HEX | RGB |
|-------|-----|-----|
| `pink-flamingo-50`  | `#FFF4FF` | rgb(255, 244, 255) |
| `pink-flamingo-100` | `#FEE8FF` | rgb(254, 232, 255) |
| `pink-flamingo-200` | `#FBD1FD` | rgb(251, 209, 253) |
| `pink-flamingo-300` | `#FAADF8` | rgb(250, 173, 248) |
| `pink-flamingo-400` | `#F568F0` | rgb(245, 104, 240) |
| `pink-flamingo-500` | `#EB4AE5` | rgb(235, 74, 229) |
| `pink-flamingo-600` | `#CF2AC5` | rgb(207, 42, 197) |
| `pink-flamingo-700` | `#AC1FA1` | rgb(172, 31, 161) |
| `pink-flamingo-800` | `#8D1B83` | rgb(141, 27, 131) |
| `pink-flamingo-900` | `#731C69` | rgb(115, 28, 105) |
| `pink-flamingo-950` | `#4C0643` | rgb(76, 6, 67) |

### Blaze Orange

| Token | HEX | RGB |
|-------|-----|-----|
| `blaze-orange-50`  | `#FFF8EC` | rgb(255, 248, 236) |
| `blaze-orange-100` | `#FFEFD4` | rgb(255, 239, 212) |
| `blaze-orange-200` | `#FFDAA7` | rgb(255, 218, 167) |
| `blaze-orange-300` | `#FFBF70` | rgb(255, 191, 112) |
| `blaze-orange-400` | `#FF9836` | rgb(255, 152, 54) |
| `blaze-orange-500` | `#FF7A0F` | rgb(255, 122, 15) |
| `blaze-orange-600` | `#F66005` | rgb(246, 96, 5) |
| `blaze-orange-700` | `#C84606` | rgb(200, 70, 6) |
| `blaze-orange-800` | `#9E370E` | rgb(158, 55, 14) |
| `blaze-orange-900` | `#7F2F0F` | rgb(127, 47, 15) |
| `blaze-orange-950` | `#451505` | rgb(69, 21, 5) |

### Supernova

| Token | HEX | RGB |
|-------|-----|-----|
| `supernova-50`  | `#FEFDE8` | rgb(254, 253, 232) |
| `supernova-100` | `#FFFBC2` | rgb(255, 251, 194) |
| `supernova-200` | `#FFF589` | rgb(255, 245, 137) |
| `supernova-300` | `#FFE845` | rgb(255, 232, 69) |
| `supernova-400` | `#FCD513` | rgb(252, 213, 19) |
| `supernova-500` | `#F7C506` | rgb(247, 197, 6) |
| `supernova-600` | `#CC9202` | rgb(204, 146, 2) |
| `supernova-700` | `#A36805` | rgb(163, 104, 5) |
| `supernova-800` | `#86510D` | rgb(134, 81, 13) |
| `supernova-900` | `#724211` | rgb(114, 66, 17) |
| `supernova-950` | `#432205` | rgb(67, 34, 5) |

---

## 2. Semantic tokens — use these in component CSS

### Primary brand (buttons, links, focus)

Hover and pressed follow a clean step ladder up the Ultramarine scale (600 → 700 → 800).

| Role | Primitive | HEX | Webflow variable |
|------|-----------|-----|------------------|
| Brand primary | `ultramarine-600` | `#3B41EC` | `var(--social--main-blue)` |
| Button hover | `ultramarine-700` | `#3133D1` | `var(--social--button-hover)` |
| Button pressed | `ultramarine-800` | `#2B2FA8` | `var(--social--button-pressed)` |

### Surfaces — dark palette (default)

| Role | Primitive | HEX | Webflow variable |
|------|-----------|-----|------------------|
| Canvas / page bg | `slate-950` | `#111111` | `var(--social--dark)` |
| Elevated surface / bg layer | `slate-900` | `#1A1A1A` | `var(--social--dark-gray-background)` |
| Card surface / mid | `slate-800` | `#272727` | `var(--social--grey)` |
| Border-strong | `slate-700` | `#404040` | `var(--social--light-grey)` |
| Menu background | `slate-900` | `#1A1A1A` | `var(--secondary--menu-bg)` |

Brand Black (`slate-950` / `#111`) is the default canvas. The dark palette defines elevation surfaces for cards, modals, and layered UI (see `shadows.md` for the full elevation scale).

### Surfaces — light palette

| Role | Primitive | HEX | Webflow variable |
|------|-----------|-----|------------------|
| Canvas (white) | `neutral-white` | `#FFFFFF` | `var(--main--white)` |
| Subtle background | `slate-100` | `#F5F5F5` | `var(--main--whitesmoke)` |
| Off-white background | `slate-50` | `#FAFAFA` | `var(--social--grey-background)` |

### Text — on dark backgrounds

| Role | Primitive | HEX |
|------|-----------|-----|
| Headings / primary | `neutral-white` | `#FFFFFF` |
| Secondary | `slate-300` | `#D3D3D3` |
| Muted / tertiary | `slate-400` | `#A3A3A3` |
| Disabled | `slate-500` | `#727272` |

### Text — on light backgrounds

| Role | Primitive | HEX | Webflow variable |
|------|-----------|-----|------------------|
| Headings | `slate-950` | `#111111` | `var(--text--text-color-dark)` |
| Body | `slate-700` | `#404040` | `var(--text--text-color-grey-dark)` |
| Secondary | `slate-500` | `#727272` | `var(--text--text-color-grey-medium)` |
| Muted | `slate-400` | `#A3A3A3` | `var(--text--text-color-grey-light)` |

### Borders and dividers

| Role | Primitive | HEX | Webflow variable |
|------|-----------|-----|------------------|
| Light (on light bg) | `slate-200` | `#E6E6E6` | `var(--border--border-light-grey)` |
| Medium (on light bg) | `slate-300` | `#D3D3D3` | `var(--border--border-med-grey)` |
| Dark (on light bg) | `slate-500` | `#727272` | `var(--border--border-dark-grey)` |
| Dark (on dark bg) | `slate-800` | `#272727` | `var(--border--border-dark)` |
| Dark hover (on dark bg) | `slate-700` | `#404040` | `var(--border--border-hover)` |

For subtle dividers on dark backgrounds, use `rgba(255,255,255,0.12)` rather than a solid token — solid white is too harsh.

### Accent colours (tags, highlights, illustrations — never CTAs)

Accents are for visual variety, category highlights, status indicators, and illustrations. Never use an accent as a primary CTA — that role belongs to `ultramarine-600`. Never combine more than 2–3 accents in a single composition.

| Role | Primitive | HEX | Webflow variable |
|------|-----------|-----|------------------|
| Sky Blue | `picton-blue-400` | `#45A5ED` | — |
| Yellow | `supernova-500` | `#F7C506` | `var(--secondary--yellow)` |
| Orange | `blaze-orange-600` | `#F66005` | `var(--secondary--orange)` |
| Electric Pink | `pink-flamingo-400` | `#F568F0` | `var(--secondary--pink)` |

### Transparent / misc

| Role | Value | Webflow variable |
|------|-------|------------------|
| Brand primary at 10% | `rgba(59, 65, 236, 0.10)` | `var(--social--blue-transparent)` |
| Transparent | — | `var(--main--transparant)` |

---

## 3. State / utility colours

State colours are **system-only tokens** — they do not live in the Figma primitive palette. Keep using them for their functional roles and do not mix them with accents.

| Role | HEX | Use | Webflow variable |
|------|-----|-----|------------------|
| Error / destructive | `#FF305A` | Error states, alerts, destructive actions | `var(--secondary--red)` |
| Secondary destructive | `#FF5252` | Inline error borders, destructive button bg | — |
| Success | `#1DC497` | Success states, positive indicators, growth metrics | `var(--secondary--green)` |

Do not use state colours for decoration.

---

## What changed (from previous version)

- **New:** full 6-family × 11-step primitive scale (Slate, Ultramarine, Picton Blue, Pink Flamingo, Blaze Orange, Supernova) plus Black/White.
- **New:** semantic/primitive layering — all named roles (primary, hover, border, body, etc.) now map to primitive tokens.
- **Changed:** button hover `#272B9D` → `ultramarine-700` `#3133D1`; button pressed `#27265E` → `ultramarine-800` `#2B2FA8` (clean step ladder).
- **Changed:** minor realignments of neutrals, text, and border hexes to their nearest Slate step (typically ≤ 10-point shifts).
- **Retired:** Purple (`#9F72FF`), Dark Navy (`#27265E`) and Deep Dark Navy (`#100F26`) as named tokens. The mid-blue gradient stop `#3769EC` is also retired — gradients now use `ultramarine-500` `#5C6EF8`.
- **Unchanged:** brand hero `#3B41EC`, Sky Blue `#45A5ED`, Yellow `#F7C506`, Orange `#F66005`, Electric Pink `#F568F0`, Brand Black `#111111`, Whitesmoke `#F5F5F5`, White `#FFFFFF`, and all state colours.
- **Webflow variable names are unchanged.** Only the values they resolve to have shifted (and most haven't). No site-wide CSS refactor required.
