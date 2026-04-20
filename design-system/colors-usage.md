# social.plus Colour System — Gradients, Usage & Variables

Fetch alongside `colors-palette.md` for the full colour palette (primitives + semantic tokens).

---

## Brand Gradients

### Brand Blue Gradient

Direction: 135° (top-left to bottom-right)
`picton-blue-400` → `ultramarine-500` → `ultramarine-600`

```css
background: linear-gradient(
  135deg,
  var(--gradient--light-blue),
  var(--gradient--medium-blue),
  var(--gradient--dark-blue)
);
```

| Step | Token | HEX | Webflow variable |
|------|-------|-----|------------------|
| Start (light) | `picton-blue-400` | `#45A5ED` | `var(--gradient--light-blue)` |
| Middle | `ultramarine-500` | `#5C6EF8` | `var(--gradient--medium-blue)` |
| End (brand blue) | `ultramarine-600` | `#3B41EC` | `var(--gradient--dark-blue)` |

### Brand Pink Gradient

Direction: left → right
`pink-flamingo-400` → `blaze-orange-600` (~51%) → `supernova-500`

```css
background: linear-gradient(to right, #F568F0, #F66005 51.5%, #F7C506);
```

Use these gradients for hero sections, feature cards, and key visual moments.
Never tile or repeat them — they should feel intentional and impactful.

---

## Flat Gradient Pairs (for components and cards)

Two-stop gradients for smaller UI elements:

| From | To | Tokens | Feel |
|------|----|--------|------|
| `#3B41EC` | `#5C6EF8` | `ultramarine-600 → ultramarine-500` | Cool authority |
| `#5C6EF8` | `#45A5ED` | `ultramarine-500 → picton-blue-400` | Airy, digital |
| `#FF305A` | `#F568F0` | Red → `pink-flamingo-400` | Urgent energy |
| `#F568F0` | `#F66005` | `pink-flamingo-400 → blaze-orange-600` | Warm vibrancy |
| `#F66005` | `#F7C506` | `blaze-orange-600 → supernova-500` | Optimism |
| `#111111` | `#272727` | `slate-950 → slate-800` | Depth |
| `#1A1A1A` | `#191B4D` | `slate-900 → ultramarine-950` | Prestige |

---

## Colour Usage Principles

**Dark-first:** The brand lives on dark backgrounds. `slate-950` (`#111`) is the default canvas. Text is white or light grey on this background.

**Ultramarine leads:** When you need one brand colour to anchor a design, reach for `ultramarine-600` (`#3B41EC`). It is the most recognisable social.plus colour.

**social.plus Blue is the only CTA colour.** Accents are for decoration and status, never for primary buttons or calls to action.

**Buttons always need three states.** Default, hover, and pressed. The default → hover → pressed ladder steps up the Ultramarine scale: `ultramarine-600` → `ultramarine-700` → `ultramarine-800`.

**Gradients for moments:** Use the Brand Blue and Brand Pink gradients for hero sections and key visual backgrounds. Never apply gradients to text — this includes CSS `background-clip: text` effects. Text should always be a solid colour (white, black, or a single brand colour).

**Cards and content boxes are greyscale by default:** When displaying a group of cards, tiles, or content boxes, use consistent neutral background colours from the Slate scale (`slate-900` `#1A1A1A` or `slate-800` `#272727`) with a subtle border (`rgba(255,255,255,0.12)`). Do not use different brand colours or gradients across cards in the same set — reserve colour and gradients for intentional singular highlights (e.g. a featured card, a hero CTA block).

**Respect the text hierarchy.** Headings are darkest, body text is medium, supporting text is lighter. Don't skip levels.

**Accessibility:** When placing text on coloured backgrounds, ensure sufficient contrast. White text works on Ultramarine 600+ shades, Picton Blue 600+, Slate 700+, and all dark surfaces. Dark text should be used on Supernova (yellows) and Picton Blue 400 and lighter. Pink Flamingo 400 requires care — test before use.

**Only use colours from this palette.** If a colour isn't listed in `colors-palette.md`, don't use it. If a design requires a new colour, flag it to the marketing team first so it can be added to the Figma source of truth.

---

## For Developers: Webflow CSS Variables

All colours above are available as Webflow CSS variables. When writing CSS for the
social.plus website, always use the variable syntax instead of hardcoding hex values.

**Pattern:** `var(--{category}--{variable-name})`

| Role | Resolves to | CSS Variable |
|------|-------------|-------------|
| social.plus Blue | `ultramarine-600` `#3B41EC` | `var(--social--main-blue)` |
| Button Hover | `ultramarine-700` `#3133D1` | `var(--social--button-hover)` |
| Button Pressed | `ultramarine-800` `#2B2FA8` | `var(--social--button-pressed)` |
| Dark | `slate-950` `#111111` | `var(--social--dark)` |
| Grey | `slate-800` `#272727` | `var(--social--grey)` |
| Light Grey | `slate-700` `#404040` | `var(--social--light-grey)` |
| Grey Background | `slate-50` `#FAFAFA` | `var(--social--grey-background)` |
| Dark Gray Background | `slate-900` `#1A1A1A` | `var(--social--dark-gray-background)` |
| Blue Transparent | `rgba(59, 65, 236, 0.10)` | `var(--social--blue-transparent)` |
| White | `neutral-white` `#FFFFFF` | `var(--main--white)` |
| Whitesmoke | `slate-100` `#F5F5F5` | `var(--main--whitesmoke)` |
| Transparent | — | `var(--main--transparant)` |
| Border Med Grey | `slate-300` `#D3D3D3` | `var(--border--border-med-grey)` |
| Border Light Grey | `slate-200` `#E6E6E6` | `var(--border--border-light-grey)` |
| Border Dark Grey | `slate-500` `#727272` | `var(--border--border-dark-grey)` |
| Border Dark | `slate-800` `#272727` | `var(--border--border-dark)` |
| Border Hover | `slate-700` `#404040` | `var(--border--border-hover)` |
| Green | `#1DC497` (system) | `var(--secondary--green)` |
| Yellow | `supernova-500` `#F7C506` | `var(--secondary--yellow)` |
| Red | `#FF305A` (system) | `var(--secondary--red)` |
| Orange | `blaze-orange-600` `#F66005` | `var(--secondary--orange)` |
| Pink | `pink-flamingo-400` `#F568F0` | `var(--secondary--pink)` |
| Menu BG | `slate-900` `#1A1A1A` | `var(--secondary--menu-bg)` |
| Text Grey Light | `slate-400` `#A3A3A3` | `var(--text--text-color-grey-light)` |
| Text Grey Medium | `slate-500` `#727272` | `var(--text--text-color-grey-medium)` |
| Text Grey Dark | `slate-700` `#404040` | `var(--text--text-color-grey-dark)` |
| Text Dark | `slate-950` `#111111` | `var(--text--text-color-dark)` |
| Gradient Light Blue | `picton-blue-400` `#45A5ED` | `var(--gradient--light-blue)` |
| Gradient Medium Blue | `ultramarine-500` `#5C6EF8` | `var(--gradient--medium-blue)` |
| Gradient Dark Blue | `ultramarine-600` `#3B41EC` | `var(--gradient--dark-blue)` |

**Note on retired variables:** `--secondary--purple` is retired (no Purple scale in the new palette). Any existing usages should be flagged for replacement or removed.
