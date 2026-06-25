# social.plus Layout & Grid System

Source: canonical design system HTML

---

## Breakpoints

| Token | Value | Context |
|-------|-------|---------|
| `sm` | 480px | Large phones, landscape mobile |
| `md` | 768px | Tablets, small laptops |
| `lg` | 1080px | Desktop, primary design target |
| `xl` | 1280px | Wide desktop, dashboards |

Design mobile-first. The base style targets mobile, with overrides at `md`, `lg`, and `xl`.

---

## Containers

Three max-width containers. Always horizontally centered with `margin: 0 auto`.

| Token | Max-width | Use |
|-------|-----------|-----|
| `container-narrow` | 680px | Articles, blog posts, focused reading content, email-style layouts |
| `container-default` | 1080px | Standard page sections, the default for most layouts |
| `container-wide` | 1280px | Dashboards, data-heavy layouts, full-bleed feature sections |

---

## Horizontal Page Padding

Applied to the left and right of all containers to prevent content from touching the viewport edge.

| Breakpoint | Padding |
|------------|---------|
| Mobile (< 768px) | `var(--space-5)` / 24px |
| Tablet (>= 768px) | `var(--space-6)` / 32px |
| Desktop (>= 1080px) | `var(--space-8)` / 48px |

---

## Column Grid

| Breakpoint | Columns | Gutter |
|------------|---------|--------|
| Mobile (< 768px) | 4 | 16px (`var(--space-4)`) |
| Tablet (>= 768px) | 8 | 20px |
| Desktop (>= 1080px) | 12 | 24px (`var(--space-5)`) |

### Common column spans (desktop / 12-col)

| Layout | Columns |
|--------|---------|
| Full width | 12 |
| Two halves | 6 + 6 |
| Thirds | 4 + 4 + 4 |
| Quarters | 3 + 3 + 3 + 3 |
| Main + sidebar | 8 + 4 |
| Narrow centered content | 6 (offset 3) |

---

## Section Vertical Rhythm

Vertical spacing between page sections follows the spacing scale.

| Context | Top/bottom padding |
|---------|--------------------|
| Standard section | `var(--space-11)` / 96px |
| Compact section | `var(--space-9)` / 64px |
| Hero section | `var(--space-12)` / 128px |
| Footer | `var(--space-7)` / 40px |

---

## Motion System

Motion should feel warm and alive, never mechanical. Fast for micro-interactions, smooth for transitions, springy for moments of delight. All transitions respect `prefers-reduced-motion`.

### Duration scale

| Token | Value | Use |
|-------|-------|-----|
| `--duration-instant` | 80ms | State flips, active/inactive toggle, checkbox tick |
| `--duration-fast` | 150ms | Button press feedback, hover reveals, badge updates |
| `--duration-base` | 250ms | Default: theme switch, card expand, drawer slide |
| `--duration-enter` | 320ms | Screen entry, modal appear, page transitions |
| `--duration-slow` | 400ms | Bottom sheet rise, complex layout changes |

### Easing curves

| Token | Value | Use |
|-------|-------|-----|
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Entering elements. Fast start, soft landing. |
| `--ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Transitions between states. Smooth, symmetrical, controlled. |
| `--ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Delight moments: avatar pop, like animation, join confirmation. |

### Motion CSS reference

```css
:root {
  --duration-instant: 80ms;
  --duration-fast:    150ms;
  --duration-base:    250ms;
  --duration-slow:    400ms;
  --duration-enter:   320ms;

  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### Reduced motion

When `prefers-reduced-motion` is enabled, all durations collapse to 1ms and transforms are replaced with opacity-only fades. See [accessibility.md](accessibility.md) for the full implementation.

---

## Z-Index Scale

See [shadows.md](shadows.md) for the full z-index table (8 named layers from `--z-base` through `--z-top`).

---

## CSS Reference

```css
/* Containers */
.container        { max-width: 1080px; margin: 0 auto; padding: 0 var(--space-5); }
.container-narrow { max-width: 680px;  margin: 0 auto; padding: 0 var(--space-5); }
.container-wide   { max-width: 1280px; margin: 0 auto; padding: 0 var(--space-5); }

@media (min-width: 768px) {
  .container,
  .container-narrow,
  .container-wide { padding: 0 var(--space-6); }
}

@media (min-width: 1080px) {
  .container,
  .container-narrow,
  .container-wide { padding: 0 var(--space-8); }
}

/* Grid */
.grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(4, 1fr);
}

@media (min-width: 768px) {
  .grid { gap: 20px; grid-template-columns: repeat(8, 1fr); }
}

@media (min-width: 1080px) {
  .grid { gap: 24px; grid-template-columns: repeat(12, 1fr); }
}
```

---

## Principles

**12 columns on desktop, 4 on mobile.** Never design for an arbitrary number of columns. Always map to the grid. If a layout needs 5 equal columns, reconsider the design.

**Consistent horizontal padding over precise pixel-matching.** Content should breathe at every viewport width. Padding scales with breakpoint to keep line lengths comfortable.

**Vertical rhythm over arbitrary spacing.** Section padding always uses spacing tokens. Never set `padding-top: 73px`. Find the right token or adjust the design.

**Narrow container for reading.** Any content intended to be read continuously (articles, documentation, long-form copy) should use `container-narrow` (680px) to keep line lengths around 65 to 75 characters.

**Motion matches intent.** Instant for binary state changes, fast for button feedback, base for standard transitions, enter for screen-level arrivals, slow for complex layout shifts. Never use a single duration for everything.
