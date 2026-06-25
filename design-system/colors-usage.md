# social.plus Color Usage

Source: canonical design system HTML

Semantic tokens, named gradients, and usage principles. For the full primitive palette, see `colors-palette.md`.

---

## 1. Semantic Tokens

Semantic tokens map primitives to functional roles. Always use semantic tokens in component CSS; reach for primitives only when no semantic token fits.

### Background

| Token | Light mode | Dark mode |
|-------|-----------|-----------|
| `--bg-base` | `#FAFAFA` (slate-50) | `#111111` |
| `--bg-elevated` | `#FFFFFF` | `#1A1A1A` |
| `--bg-card` | `#F5F5F5` (slate-100) | `#272727` |
| `--bg-card-alt` | `#FFFFFF` | `#404040` |
| `--bg-sunken` | `#E6E6E6` | `#000000` |
| `--bg-overlay` | `rgba(17, 17, 17, 0.48)` | `rgba(0, 0, 0, 0.72)` |

### Text

| Token | Light mode | Dark mode |
|-------|-----------|-----------|
| `--text-primary` | `#111111` (slate-950) | `#FFFFFF` |
| `--text-secondary` | `#535353` (slate-600) | `rgba(255, 255, 255, 0.66)` |
| `--text-tertiary` | `#A3A3A3` (slate-400) | `rgba(255, 255, 255, 0.36)` |
| `--text-inverse` | `#FFFFFF` | `#111111` (slate-950) |
| `--text-on-primary` | `#FFFFFF` | `#FFFFFF` |

### Border

| Token | Light mode | Dark mode |
|-------|-----------|-----------|
| `--border-faint` | `rgba(17, 17, 17, 0.06)` | `rgba(255, 255, 255, 0.05)` |
| `--border-subtle` | `rgba(17, 17, 17, 0.10)` | `rgba(255, 255, 255, 0.08)` |
| `--border-default` | `rgba(17, 17, 17, 0.16)` | `rgba(255, 255, 255, 0.14)` |
| `--border-strong` | `rgba(17, 17, 17, 0.28)` | `rgba(255, 255, 255, 0.22)` |

### Action (primary, secondary, tertiary)

| Token | Light mode | Dark mode |
|-------|-----------|-----------|
| `--action-primary` | `#3B41EC` (ultra-600) | `#3B41EC` |
| `--action-primary-hover` | `#3133D1` | `#3133D1` |
| `--action-primary-press` | `#2B2FA8` (ultra-800) | `#2B2FA8` |
| `--action-primary-subtle` | `#EDF4FF` (ultra-50) | `rgba(59, 65, 236, 0.14)` |
| `--action-accent` | `#3B41EC` (6.66:1 on white) | `#7B94FE` (6.75:1 on #111) |
| `--action-primary-text` | `#FFFFFF` | `#FFFFFF` |
| `--action-secondary` | `#727272` (slate-500) | `#A3A3A3` |
| `--action-secondary-subtle` | `#F5F5F5` (slate-100) | `rgba(163, 163, 163, 0.14)` |
| `--action-tertiary` | `#1B89DC` (picton-500) | `#45A5ED` |
| `--action-tertiary-subtle` | `#F1F7FE` (picton-50) | `rgba(69, 165, 237, 0.14)` |

### Status

| Token | Light mode | Dark mode |
|-------|-----------|-----------|
| `--status-success` | `#1DC497` | `#1DC497` |
| `--status-success-subtle` | `rgba(29, 196, 151, 0.12)` | `rgba(29, 196, 151, 0.14)` |
| `--status-warning` | `#CC9202` | `#F7C506` |
| `--status-warning-subtle` | `#FEFDE8` | `rgba(247, 197, 6, 0.14)` |
| `--status-error` | `#FF305A` | `#FF305A` |
| `--status-error-subtle` | `rgba(255, 48, 90, 0.08)` | `rgba(255, 48, 90, 0.14)` |
| `--status-info` | `#1B89DC` | `#45A5ED` |
| `--status-info-subtle` | `#F1F7FE` | `rgba(69, 165, 237, 0.14)` |

### Shadows

| Token | Light mode | Dark mode |
|-------|-----------|-----------|
| `--shadow-sm` | `0 1px 3px rgba(17,17,17,0.08), 0 1px 2px rgba(17,17,17,0.06)` | `0 1px 4px rgba(0,0,0,0.3)` |
| `--shadow-md` | `0 4px 12px rgba(17,17,17,0.10), 0 2px 4px rgba(17,17,17,0.06)` | `0 4px 14px rgba(0,0,0,0.4)` |
| `--shadow-lg` | `0 12px 32px rgba(17,17,17,0.12), 0 4px 8px rgba(17,17,17,0.08)` | `0 12px 36px rgba(0,0,0,0.5)` |
| `--shadow-xl` | `0 24px 48px rgba(17,17,17,0.14), 0 8px 16px rgba(17,17,17,0.08)` | `0 28px 70px rgba(0,0,0,0.6), 0 4px 14px rgba(0,0,0,0.4)` |
| `--shadow-glow` | `0 0 40px rgba(59,65,236,0.18)` | `0 0 60px rgba(59,65,236,0.25)` |

### Glass

| Token | Light mode | Dark mode |
|-------|-----------|-----------|
| `--glass` | `rgba(250, 250, 250, 0.72)` | `rgba(17, 17, 17, 0.55)` |
| `--glass-strong` | `rgba(250, 250, 250, 0.90)` | `rgba(17, 17, 17, 0.72)` |

---

## 2. Named Gradients

All gradients are theme-independent (same in both light and dark modes). Each has a CSS custom property and a descriptive display name used in the design system UI.

| Token | Display name | CSS value |
|-------|-------------|-----------|
| `--grad-warm` | Brand Blue | `linear-gradient(135deg, #45A5ED 0%, #5C6EF8 50%, #3B41EC 100%)` |
| `--grad-gold` | Solar | `linear-gradient(135deg, #F66005 0%, #F7C506 100%)` |
| `--grad-dusk` | Brand Pink | `linear-gradient(to right, #F568F0 0%, #F66005 51.5%, #F7C506 100%)` |
| `--grad-forest` | Airy | `linear-gradient(135deg, #5C6EF8 0%, #45A5ED 100%)` |
| `--grad-clay` | Depth | `linear-gradient(135deg, #111111 0%, #272727 100%)` |
| `--grad-river` | Authority | `linear-gradient(135deg, #3B41EC 0%, #5C6EF8 100%)` |
| `--grad-cinema` | Vibrant | `linear-gradient(135deg, #F568F0 0%, #F66005 100%)` |
| `--grad-ember` | Ember | `linear-gradient(135deg, #FF305A 0%, #F568F0 100%)` |
| `--grad-night` | Prestige | `linear-gradient(135deg, #1A1A1A 0%, #191B4D 100%)` |
| `--grad-amber` | Gold | `linear-gradient(135deg, #FCD513 0%, #CC9202 100%)` |
| `--grad-sunset` | Energy | `linear-gradient(160deg, #F568F0 0%, #FF305A 100%)` |

---

## 3. Usage Principles

### Dark-first design

The brand lives on dark backgrounds. `#111111` (slate-950) is the default canvas. Design for dark surfaces first, then adapt to light.

### Ultramarine leads

When you need one brand color to anchor a design, reach for `#3B41EC` (ultra-600). It is the most recognizable social.plus color.

### CTA color rules

social.plus Blue is the only CTA color. Accents are for decoration and status, never for primary buttons or calls to action. Buttons always need three states following the Ultramarine ladder: default (ultra-600) to hover (#3133D1) to pressed (ultra-800).

On dark surfaces, ultra-600 fills are paired with white labels. For text-level and icon-level ultramarine, step up to ultra-400 (`--action-accent`) to hold WCAG AA contrast (6.75:1 on #111).

### Gradient usage

Use gradients for hero sections, feature cards, and key visual moments. Never tile or repeat them. Never apply gradients to text (no `background-clip: text` effects). Text should always be a solid color.

### Card styling

Cards and content boxes are greyscale by default. Use consistent neutral backgrounds from the Slate scale with subtle borders. Do not use different brand colors or gradients across cards in the same set. Reserve color and gradients for intentional singular highlights such as a featured card or a hero CTA block.

### Text hierarchy

Respect the three-level text hierarchy in both modes:

- **Primary**: full contrast (`--text-primary`)
- **Secondary**: reduced weight (`--text-secondary`)
- **Tertiary**: muted, supporting content (`--text-tertiary`)

Do not skip levels. Headings are darkest, body text is medium, supporting text is lighter.

### Accessibility

White text works on ultra-600 and darker, picton-500 and darker, and all dark surfaces. Dark text should be used on yellows and light blues. Always verify contrast ratios when placing text on colored backgrounds.

### No gradient on text

Never apply gradients to text. This includes CSS `background-clip: text` effects. Text should always be a solid color (white, black, or a single brand color).

### Only use palette colors

If a color is not listed in `colors-palette.md`, do not use it. If a design requires a new color, flag it to the marketing team first so it can be added to the canonical source.
