# social.plus Colour System — Gradients, Usage & Variables

Fetch alongside `colors-palette.md` for the full colour palette.

---

## Brand Gradients

### Brand Blue Gradient

Direction: 135° (top-left to bottom-right)
`#45A5ED` (Sky Blue) → `#3769EC` (Blue) → `#3B41EC` (Ultramarine)

```css
background: linear-gradient(
  135deg,
  var(--gradient--light-blue),
  var(--gradient--medium-blue),
  var(--gradient--dark-blue)
);
```

| Step | HEX | Webflow variable |
|------|-----|------------------|
| Start (light) | `#45A5ED` | `var(--gradient--light-blue)` |
| Middle | `#3769EC` | `var(--gradient--medium-blue)` |
| End (brand blue) | `#3B41EC` | `var(--gradient--dark-blue)` |

### Brand Pink Gradient

Direction: left → right
`#F568F0` (Electric Pink) → `#F66005` (Orange, ~51%) → `#F7C506` (Yellow)

```css
background: linear-gradient(to right, #F568F0, #F66005 51.5%, #F7C506);
```

Use these gradients for hero sections, feature cards, and key visual moments.
Never tile or repeat them — they should feel intentional and impactful.

---

## Flat Gradient Pairs (for components and cards)

Two-stop gradients for smaller UI elements:

| From | To | Feel |
|------|----|------|
| Ultramarine `#3B41EC` | Blue `#3769EC` | Cool authority |
| Blue `#3769EC` | Sky Blue `#45A5ED` | Airy, digital |
| Red `#FF305A` | Electric Pink `#F568F0` | Urgent energy |
| Electric Pink `#F568F0` | Orange `#F66005` | Warm vibrancy |
| Orange `#F66005` | Yellow `#F7C506` | Optimism |
| Black `#111111` | Dark Grey `#272727` | Depth |
| Dark Navy `#27265E` | Deep Dark Navy `#100F26` | Prestige |

---

## Colour Usage Principles

**Dark-first:** The brand lives on dark backgrounds. `#111` is the default canvas.
Text is white or light grey on this background.

**Ultramarine leads:** When you need one brand colour to anchor a design, reach for
Ultramarine. It is the most recognisable social.plus colour.

**social.plus Blue is the only CTA colour.** Accents are for decoration and status,
never for primary buttons or calls to action.

**Buttons always need three states.** Default, hover, and pressed. Never ship a button
with only one colour state.

**Gradients for moments:** Use the Brand Blue and Brand Pink gradients for hero sections
and key visual backgrounds. Never apply gradients to text — this includes CSS
`background-clip: text` effects. Text should always be a solid colour (white, black,
or a single brand colour).

**Cards and content boxes are greyscale by default:** When displaying a group of cards,
tiles, or content boxes, use consistent neutral background colours from the greyscale
palette (`#1e1e1e` or `#272727`) with a subtle border (`rgba(255,255,255,0.12)`). Do not
use different brand colours or gradients across cards in the same set — reserve colour
and gradients for intentional singular highlights (e.g. a featured card, a hero CTA
block).

**Respect the text hierarchy.** Headings are darkest, body text is medium, supporting
text is lighter. Don't skip levels.

**Accessibility:** When placing text on coloured backgrounds, ensure sufficient contrast.
White text works on Ultramarine, Blue, Dark Navy, and Black. Dark text should be used
on Yellow and Sky Blue. Electric Pink requires care — test before use.

**Only use colours from this palette.** If a colour isn't listed here, don't use it. If
a design requires a new colour, flag it to the marketing team first.

---

## For Developers: Webflow CSS Variables

All colours above are available as Webflow CSS variables. When writing CSS for the
social.plus website, always use the variable syntax instead of hardcoding hex values.

**Pattern:** `var(--{category}--{variable-name})`

| Colour | CSS Variable |
|--------|-------------|
| social.plus Blue | `var(--social--main-blue)` |
| Button Hover | `var(--social--button-hover)` |
| Button Pressed | `var(--social--button-pressed)` |
| Dark | `var(--social--dark)` |
| Grey | `var(--social--grey)` |
| Light Grey | `var(--social--light-grey)` |
| Grey Background | `var(--social--grey-background)` |
| Dark Gray Background | `var(--social--dark-gray-background)` |
| Blue Transparent | `var(--social--blue-transparent)` |
| White | `var(--main--white)` |
| Whitesmoke | `var(--main--whitesmoke)` |
| Transparent | `var(--main--transparant)` |
| Border Med Grey | `var(--border--border-med-grey)` |
| Border Light Grey | `var(--border--border-light-grey)` |
| Border Dark Grey | `var(--border--border-dark-grey)` |
| Border Dark | `var(--border--border-dark)` |
| Border Hover | `var(--border--border-hover)` |
| Green | `var(--secondary--green)` |
| Yellow | `var(--secondary--yellow)` |
| Red | `var(--secondary--red)` |
| Orange | `var(--secondary--orange)` |
| Purple | `var(--secondary--purple)` |
| Pink | `var(--secondary--pink)` |
| Menu BG | `var(--secondary--menu-bg)` |
| Text Grey Light | `var(--text--text-color-grey-light)` |
| Text Grey Medium | `var(--text--text-color-grey-medium)` |
| Text Grey Dark | `var(--text--text-color-grey-dark)` |
| Text Dark | `var(--text--text-color-dark)` |
| Gradient Light Blue | `var(--gradient--light-blue)` |
| Gradient Medium Blue | `var(--gradient--medium-blue)` |
| Gradient Dark Blue | `var(--gradient--dark-blue)` |
