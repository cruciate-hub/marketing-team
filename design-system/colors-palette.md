# social.plus Color Palette

Source: canonical design system HTML

All primitive color tokens used across the social.plus product and marketing surfaces. These are the raw values; see `colors-usage.md` for semantic tokens, gradients, and usage principles.

---

## Ultramarine (primary brand family)

The signature social.plus color family. Ultra 600 is the brand hero and primary CTA fill. Ultra 400 is used for text and icons on dark backgrounds to maintain WCAG AA contrast.

| Token | Hex | Role |
|-------|-----|------|
| `--ultra-50` | `#EDF4FF` | Subtle tint, light-mode action background |
| `--ultra-300` | `#A1BAFF` | Mid-range accent |
| `--ultra-400` | `#7B94FE` | Text/icon on dark surfaces (6.75:1 on #111) |
| `--ultra-600` | `#3B41EC` | Brand hero, CTA fill, action-primary |
| `--ultra-800` | `#2B2FA8` | Button pressed state |

---

## Slate (neutrals)

Slate provides every neutral surface, text shade, and border tone. The scale runs from near-black (950) to near-white (50), plus pure white.

| Token | Hex | Role |
|-------|-----|------|
| `--slate-950` | `#111111` | Brand Black, dark-mode canvas |
| `--slate-800` | `#272727` | Dark-mode card surface |
| `--slate-600` | `#535353` | Light-mode secondary text |
| `--slate-500` | `#727272` | Light-mode secondary actions |
| `--slate-400` | `#A3A3A3` | Tertiary text, muted UI |
| `--slate-300` | `#D3D3D3` | Light borders |
| `--slate-200` | `#E6E6E6` | Light-mode sunken background |
| `--slate-100` | `#F5F5F5` | Light-mode card background |
| `--slate-50` | `#FAFAFA` | Light-mode base canvas |
| `--white` | `#FFFFFF` | Elevated surface, inverse text |

---

## Picton Blue (tertiary family)

A cooler blue used for tertiary actions, info states, and supporting highlights. Complements Ultramarine without competing with it.

| Token | Hex | Role |
|-------|-----|------|
| `--picton-50` | `#F1F7FE` | Subtle info background |
| `--picton-300` | `#84C2F5` | Mid-range highlight |
| `--picton-500` | `#1B89DC` | Tertiary action (light mode) |
| `--picton-700` | `#0C5598` | Deep Picton for contrast contexts |

---

## Accent Palette (community identities)

Used exclusively for community avatar gradients, category chips, and user-generated color identifiers. Never used for UI controls or primary CTAs.

| Token | Hex | Notes |
|-------|-----|-------|
| `--accent-orange` | `#F66005` | Primary orange |
| `--accent-orange-light` | `#FF9836` | Lighter orange variant |
| `--accent-orange-deep` | `#C84606` | Deeper orange for contrast |
| `--accent-yellow` | `#F7C506` | Primary yellow |
| `--accent-yellow-deep` | `#CC9202` | Deeper yellow for contrast |
| `--accent-pink` | `#F568F0` | Primary pink |
| `--accent-pink-deep` | `#CF2AC5` | Deeper pink for contrast |
| `--accent-sky` | `#45A5ED` | Sky blue accent |
| `--accent-sky-deep` | `#0D6BBC` | Deeper sky blue for contrast |
| `--accent-periwinkle` | `#7B94FE` | Periwinkle (matches Ultra 400) |
| `--accent-magenta` | `#EB4AE5` | Magenta accent |

---

## Status Colors

Functional colors for system feedback. Derived from semantic tokens; values differ between light and dark modes.

| Status | Light mode | Dark mode | Usage |
|--------|-----------|-----------|-------|
| Success | `#1DC497` | `#1DC497` | Positive indicators, growth metrics |
| Warning | `#CC9202` | `#F7C506` | Caution states, advisory notices |
| Error | `#FF305A` | `#FF305A` | Errors, alerts, destructive actions |
| Info | `#1B89DC` | `#45A5ED` | Informational callouts |

Each status color also has a subtle variant for tinted backgrounds (see `colors-usage.md` for exact values).

Do not use status colors for decoration. They are reserved for their functional roles.
