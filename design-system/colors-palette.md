# social.plus Colour System — Palette

Source of truth: Figma file node `131:3733`
https://www.figma.com/design/nDIDa7goXwKlqGWdKKlbIX/2026-Website-Visuals?node-id=131-3733

Fetch alongside `colors-usage.md` for gradients, usage principles, and Webflow CSS variables.

---

## Primary Brand Colour

| Preview | Name | HEX | RGB | Webflow variable |
|---------|------|-----|-----|------------------|
| ![](https://placehold.co/40x40/3b41ec/3b41ec) | **social.plus Blue (Ultramarine)** | `#3B41EC` | rgb(59, 65, 236) | `var(--social--main-blue)` |

Ultramarine is the hero colour. Use it for primary CTAs, key highlights, and primary
interactive elements. It appears prominently on the dark brand background. It is the
most recognisable social.plus colour.

### Interactive states (buttons, links)

| Preview | State | HEX | Webflow variable |
|---------|-------|-----|------------------|
| ![](https://placehold.co/40x40/3b41ec/3b41ec) | Default | `#3B41EC` | `var(--social--main-blue)` |
| ![](https://placehold.co/40x40/272b9d/272b9d) | Hover | `#272B9D` | `var(--social--button-hover)` |
| ![](https://placehold.co/40x40/27265e/27265e) | Pressed | `#27265E` | `var(--social--button-pressed)` |

---

## Supporting Colours

Used for visual variety, tags, status indicators, feature category highlights, and
illustrations. Never use accents as primary call-to-action colours — that role belongs
to social.plus Blue. Never use more than 2–3 of these together in a single
composition — let them breathe.

| Preview | Name | HEX | RGB | Webflow variable |
|---------|------|-----|-----|------------------|
| ![](https://placehold.co/40x40/3769ec/3769ec) | Blue | `#3769EC` | rgb(55, 105, 236) | — |
| ![](https://placehold.co/40x40/45a5ed/45a5ed) | Sky Blue | `#45A5ED` | rgb(69, 165, 237) | — |
| ![](https://placehold.co/40x40/f7c506/f7c506) | Yellow | `#F7C506` | rgb(247, 197, 6) | `var(--secondary--yellow)` |
| ![](https://placehold.co/40x40/f66005/f66005) | Orange | `#F66005` | rgb(246, 96, 5) | `var(--secondary--orange)` |
| ![](https://placehold.co/40x40/f568f0/f568f0) | Electric Pink | `#F568F0` | rgb(245, 104, 240) | `var(--secondary--pink)` |
| ![](https://placehold.co/40x40/27265e/27265e) | Dark Navy | `#27265E` | rgb(39, 38, 94) | — |
| ![](https://placehold.co/40x40/9f72ff/9f72ff) | Purple | `#9F72FF` | rgb(159, 114, 255) | `var(--secondary--purple)` |

---

## Neutral / Base Colours

### Dark palette

| Preview | Name | HEX | RGB | Webflow variable |
|---------|------|-----|-----|------------------|
| ![](https://placehold.co/40x40/111111/111111) | **Brand Black** | `#111111` | rgb(17, 17, 17) | `var(--social--dark)` |
| ![](https://placehold.co/40x40/1a1a1a/1a1a1a) | Dark Gray Background | `#1A1A1A` | rgb(26, 26, 26) | `var(--social--dark-gray-background)` |
| ![](https://placehold.co/40x40/222222/222222) | Grey | `#222222` | rgb(34, 34, 34) | `var(--social--grey)` |
| ![](https://placehold.co/40x40/272727/272727) | Dark Grey | `#272727` | rgb(39, 39, 39) | — |
| ![](https://placehold.co/40x40/444444/444444) | Light Grey | `#444444` | rgb(68, 68, 68) | `var(--social--light-grey)` |
| ![](https://placehold.co/40x40/100f26/100f26) | Deep Dark Navy | `#100F26` | rgb(16, 15, 38) | — |

### Light palette

| Preview | Name | HEX | RGB | Webflow variable |
|---------|------|-----|-----|------------------|
| ![](https://placehold.co/40x40/ffffff/ffffff) | **Brand White** | `#FFFFFF` | rgb(255, 255, 255) | `var(--main--white)` |
| ![](https://placehold.co/40x40/f5f5f5/f5f5f5) | Whitesmoke | `#F5F5F5` | rgb(245, 245, 245) | `var(--main--whitesmoke)` |
| ![](https://placehold.co/40x40/f9f9f9/f9f9f9) | Grey Background | `#F9F9F9` | rgb(249, 249, 249) | `var(--social--grey-background)` |

Brand Black (`#111`) is the default background. White is for primary text on dark
backgrounds. The dark palette defines elevation surfaces for cards, modals, and
layered UI.

---

## State / Utility Colours

| Preview | Name | HEX | Use | Webflow variable |
|---------|------|-----|-----|------------------|
| ![](https://placehold.co/40x40/ff305a/ff305a) | Red | `#FF305A` | Error states, alerts, destructive actions | `var(--secondary--red)` |
| ![](https://placehold.co/40x40/ff5252/ff5252) | Dark Orange | `#FF5252` | Warnings, secondary destructive states | — |
| ![](https://placehold.co/40x40/1dc497/1dc497) | Green | `#1DC497` | Success states, positive indicators, growth metrics | `var(--secondary--green)` |

These are functional colours. Do not use them for decorative purposes.

---

## Special

| Preview | Name | HEX / Value | Webflow variable |
|---------|------|-------------|------------------|
| ![](https://placehold.co/40x40/2a31e9/2a31e9) | Blue Transparent | `rgba(42, 49, 233, 0.1)` | `var(--social--blue-transparent)` |
| ![](https://placehold.co/40x40/181818/181818) | Menu Background | `#181818` | `var(--secondary--menu-bg)` |
| — | Transparent | — | `var(--main--transparant)` |

---

## Text Colours

### On light backgrounds

| Preview | Level | HEX | Webflow variable |
|---------|-------|-----|------------------|
| ![](https://placehold.co/40x40/111111/111111) | Headings | `#111111` | `var(--text--text-color-dark)` |
| ![](https://placehold.co/40x40/414347/414347) | Body text | `#414347` | `var(--text--text-color-grey-dark)` |
| ![](https://placehold.co/40x40/717275/717275) | Secondary text | `#717275` | `var(--text--text-color-grey-medium)` |
| ![](https://placehold.co/40x40/b3b3b3/b3b3b3) | Muted text | `#B3B3B3` | `var(--text--text-color-grey-light)` |

### On dark backgrounds

Use `#FFFFFF` (white) for headings and primary text. Use `#D0D0D1` for secondary text.
Use `#A0A1A3` for muted/tertiary text. Use `#717275` for disabled text.

---

## Borders and Dividers

### On light backgrounds

| Preview | Name | HEX | Webflow variable |
|---------|------|-----|------------------|
| ![](https://placehold.co/40x40/e7e7e7/e7e7e7) | Light Grey | `#E7E7E7` | `var(--border--border-light-grey)` |
| ![](https://placehold.co/40x40/d0d0d1/d0d0d1) | Med Grey | `#D0D0D1` | `var(--border--border-med-grey)` |
| ![](https://placehold.co/40x40/666666/666666) | Dark Grey | `#666666` | `var(--border--border-dark-grey)` |

### On dark backgrounds

| Preview | Name | HEX | Webflow variable |
|---------|------|-----|------------------|
| ![](https://placehold.co/40x40/232324/232324) | Dark | `#232324` | `var(--border--border-dark)` |
| ![](https://placehold.co/40x40/39393a/39393a) | Hover | `#39393A` | `var(--border--border-hover)` |

Use `rgba(255,255,255,0.12)` for subtle dividers on the dark background. Do not use
solid white — it is too harsh.
