# social.plus Elevation & Shadows

Shadows create depth and visual hierarchy. In light mode, depth comes from soft neutral shadows that intensify as the layer rises. In dark mode, depth is communicated through progressively lighter background surfaces, not heavier shadows.

Source: canonical design system HTML

---

## Shadow Scale

Five named shadow tokens plus a brand glow, defined as CSS custom properties. Light and dark mode each have their own values.

### Light mode shadows

| Token | CSS value | Use |
|-------|-----------|-----|
| `--shadow-sm` | `0 1px 3px rgba(17,17,17,0.08), 0 1px 2px rgba(17,17,17,0.06)` | Chips, input fields, subtle cards on light background |
| `--shadow-md` | `0 4px 12px rgba(17,17,17,0.10), 0 2px 4px rgba(17,17,17,0.06)` | Cards, dropdowns, context menus |
| `--shadow-lg` | `0 12px 32px rgba(17,17,17,0.12), 0 4px 8px rgba(17,17,17,0.08)` | Floating action buttons, sticky headers, toasts |
| `--shadow-xl` | `0 24px 48px rgba(17,17,17,0.14), 0 8px 16px rgba(17,17,17,0.08)` | Modals, bottom sheets, popovers |
| `--shadow-glow` | `0 0 40px rgba(59,65,236,0.18)` | Primary CTA buttons on hover/focus, featured items |

### Dark mode shadows

| Token | CSS value | Use |
|-------|-----------|-----|
| `--shadow-sm` | `0 1px 4px rgba(0,0,0,0.3)` | Same use cases; heavier opacity compensates for dark surfaces |
| `--shadow-md` | `0 4px 14px rgba(0,0,0,0.4)` | Cards, dropdowns, context menus |
| `--shadow-lg` | `0 12px 36px rgba(0,0,0,0.5)` | Floating action buttons, sticky headers, toasts |
| `--shadow-xl` | `0 28px 70px rgba(0,0,0,0.6), 0 4px 14px rgba(0,0,0,0.4)` | Modals, bottom sheets, popovers |
| `--shadow-glow` | `0 0 60px rgba(59,65,236,0.25)` | Primary CTA buttons on hover/focus, featured items |

### Elevation levels

| Level | Token | Typical use |
|-------|-------|-------------|
| Flat | none | Inline elements, selected states with border, tab items |
| Level 1 | `--shadow-sm` | Chips, input fields, subtle cards |
| Level 2 | `--shadow-md` | Cards, dropdowns, context menus |
| Level 3 | `--shadow-lg` | FABs, sticky headers, toasts |
| Level 4 | `--shadow-xl` | Modals, bottom sheets, popovers |
| Glow | `--shadow-glow` | Primary CTA hover/focus, featured items |

---

## Background Layering

Depth is also expressed through background surface tokens. Each layer has a named token that differs between light and dark modes.

### Light mode surfaces

Depth moves from sunken inputs up to pure-white elevated surfaces.

| Token | Hex | Role |
|-------|-----|------|
| `bg-sunken` | `#E6E6E6` | Inputs, recessed areas |
| `bg-base` | `#FAFAFA` | App base background (cream) |
| `bg-card` | `#F5F5F5` | Cards, feed rows |
| `bg-elevated` | `#FFFFFF` | Nav bar, modals |

### Dark mode surfaces

Surfaces get progressively lighter as they rise. No heavy drop shadows needed.

| Token | Hex | Role |
|-------|-----|------|
| `bg-sunken` | `#000000` | Inputs, recessed areas |
| `bg-deep` | `#000000` | Deepest background |
| `bg-base` | `#111111` | App base background |
| `bg-elevated` | `#1A1A1A` | Nav bar, sidebars |
| `bg-card` | `#272727` | Cards, panels |
| `bg-card-2` | `#404040` | Nested cards, chips |

---

## Z-Index Scale

Eight named layers prevent z-index collisions. Always use the tokens, never magic numbers.

| Token | Value | Layer |
|-------|-------|-------|
| `--z-base` | 0 | Page content |
| `--z-raised` | 10 | Sticky cards, inline floats |
| `--z-dropdown` | 100 | Dropdowns, context menus |
| `--z-sticky` | 200 | Sticky headers, bottom nav |
| `--z-toast` | 400 | Toasts, snackbars |
| `--z-overlay` | 500 | Modal backdrop |
| `--z-modal` | 600 | Modals, bottom sheets |
| `--z-top` | 900 | System alerts, debug panels |

---

## CSS Reference

```css
:root {
  /* Light mode shadows */
  --shadow-sm:  0 1px 3px rgba(17,17,17,0.08), 0 1px 2px rgba(17,17,17,0.06);
  --shadow-md:  0 4px 12px rgba(17,17,17,0.10), 0 2px 4px rgba(17,17,17,0.06);
  --shadow-lg:  0 12px 32px rgba(17,17,17,0.12), 0 4px 8px rgba(17,17,17,0.08);
  --shadow-xl:  0 24px 48px rgba(17,17,17,0.14), 0 8px 16px rgba(17,17,17,0.08);
  --shadow-glow:0 0 40px rgba(59,65,236,0.18);

  /* Z-index scale */
  --z-base:     0;
  --z-raised:   10;
  --z-dropdown: 100;
  --z-sticky:   200;
  --z-toast:    400;
  --z-overlay:  500;
  --z-modal:    600;
  --z-top:      900;
}

[data-theme="dark"] {
  --shadow-sm:  0 1px 4px rgba(0,0,0,0.3);
  --shadow-md:  0 4px 14px rgba(0,0,0,0.4);
  --shadow-lg:  0 12px 36px rgba(0,0,0,0.5);
  --shadow-xl:  0 28px 70px rgba(0,0,0,0.6), 0 4px 14px rgba(0,0,0,0.4);
  --shadow-glow:0 0 60px rgba(59, 65, 236, 0.25);
}
```

---

## Principles

**Shadow alone is not enough on dark backgrounds.** Always pair elevation shadow with the corresponding surface token. A `--shadow-md` card in dark mode sits on `bg-card` (`#272727`), not `bg-base`.

**Background layering replaces heavy shadows in dark mode.** Progressively lighter surfaces communicate depth without the visual noise of dark-on-dark shadows.

**Glow communicates brand energy, not depth.** The `--shadow-glow` token exists for interactive feedback on primary CTAs, not to imply elevation. Never use it as a resting state.

**Use z-index tokens, never raw numbers.** Raw z-index values create stacking conflicts. The eight named layers cover every standard UI pattern.
