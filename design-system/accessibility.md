# social.plus Accessibility

social.plus targets WCAG 2.1 AA compliance across all products and marketing surfaces. Accessibility is built into every component decision, not treated as a post-launch concern.

Source: canonical design system HTML

---

## Color Contrast

### Brand color contrast behavior

The design system handles branded text contrast automatically through the `--action-accent` token:

| Mode | `--action-accent` resolves to | Hex | Contrast ratio | WCAG AA |
|------|-------------------------------|-----|----------------|---------|
| Light mode | `--ultra-600` | `#3B41EC` | 6.66:1 on `#FAFAFA` | Pass |
| Dark mode | `--ultra-400` | `#7B94FE` | 6.75:1 on `#111111` | Pass |

Always use `--action-accent` for branded text and icon color. Never hard-code `#3B41EC` for text on dark backgrounds.

### Critical contrast failures

| Foreground | Background | Ratio | Result |
|-----------|------------|-------|--------|
| Ultramarine `#3B41EC` as TEXT | Dark `#111111` | 2.9:1 | FAILS AA. Never use as text or icon color on dark backgrounds. |

### Verified pairings

| Foreground | Background | Ratio | Result |
|-----------|------------|-------|--------|
| White `#FFFFFF` | Ultramarine `#3B41EC` | 4.8:1 | Passes AA for normal text |
| `--action-accent` (`#7B94FE`) | Dark `#111111` | 6.75:1 | Passes AA. Use this for branded text/icons on dark. |
| `--action-accent` (`#3B41EC`) | Light `#FAFAFA` | 6.66:1 | Passes AA. Light mode branded text. |

### Minimum ratios

| Context | Minimum | Target |
|---------|---------|--------|
| Body text | 4.5:1 | 7:1 |
| Large text (18px+ bold or 24px+ regular) | 3:1 | 4.5:1 |
| UI components and graphical elements | 3:1 | 4.5:1 |

---

## Touch Targets

All interactive elements must meet a 44px minimum touch target size (per WCAG 2.5.5). Buttons, icon buttons, toggles, and tappable list items all enforce this minimum in the component library.

---

## Reduced Motion

All transitions and animations check `prefers-reduced-motion`. When enabled:

- Durations collapse to **1ms**
- Transforms are replaced with opacity-only fades

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 1ms !important;
    transition-duration: 1ms !important;
  }
}
```

Never use flashing content that exceeds 3 flashes per second.

---

## Focus Indicators

Visible focus rings use a 3px outline with the `--action-primary-subtle` color. The system uses `box-shadow` rather than `outline` to create the focus ring:

```css
.input-shell:focus-within {
  border-color: var(--action-accent);
  box-shadow: 0 0 0 3px var(--action-primary-subtle);
}
```

Rules:

- Every interactive element must have a visible focus indicator
- Never use `outline: none` without providing a custom alternative
- Use `:focus-visible` (not `:focus`) to avoid showing focus rings on mouse click while preserving them for keyboard navigation
- Focus ring color uses `--action-accent` for the border and `--action-primary-subtle` for the outer glow

---

## Text Sizing

Minimum text size is **12px**. No text in the system is smaller than `--text-xs` (12px).

The type scale enforces this floor:

| Token | Size |
|-------|------|
| `--text-xs` | 12px (minimum) |
| `--text-sm` | 13px |
| `--text-base` | 15px |

Never set font size below `--text-xs` for any element that conveys information.

---

## Keyboard Navigation

All interactive elements must be reachable and operable via keyboard alone.

| Component | Keyboard behavior |
|-----------|-------------------|
| Button | `Enter` or `Space` to activate |
| Link | `Enter` to follow |
| Select / dropdown | `Enter` to open, arrow keys to navigate, `Enter` to select, `Escape` to close |
| Modal / dialog | `Escape` to close, focus trapped inside while open |
| Toggle | `Space` to toggle |
| Checkbox | `Space` to check/uncheck |
| Radio group | Arrow keys to move between options |

Tab order must follow the visual reading order (left to right, top to bottom).

---

## ARIA Patterns

| Pattern | Requirement |
|---------|-------------|
| Icon-only button | `aria-label="[action]"` |
| Loading state | `aria-busy="true"` on the container |
| Error message | `aria-live="polite"` on the error region; `aria-describedby` linking input to error |
| Modal | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` pointing to the title |
| Toggle | `role="switch"`, `aria-checked="true/false"` |
| Navigation | `role="navigation"`, `aria-label` to distinguish multiple navs |

Do not use `role="button"` on a `<div>`. Use a real `<button>` element. Do not rely on color alone to communicate status.

---

## Checklist

Before shipping any component or page:

- [ ] All text meets minimum contrast ratio (4.5:1 for body, 3:1 for large text)
- [ ] `--action-accent` used for branded text (never hard-coded Ultramarine on dark)
- [ ] All interactive elements are keyboard accessible
- [ ] Focus rings are visible on all focusable elements
- [ ] Touch targets meet 44px minimum
- [ ] No information is conveyed by color alone
- [ ] All images have appropriate `alt` text
- [ ] All icon-only buttons have `aria-label`
- [ ] Form inputs have associated labels
- [ ] Error states include text, not just color
- [ ] Animations respect `prefers-reduced-motion`
- [ ] No text smaller than 12px (`--text-xs`)
- [ ] Tab order matches visual reading order
