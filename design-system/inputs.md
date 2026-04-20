# social.plus Form Inputs

---

## Foundation

All inputs share the same foundational visual language. Colour references below use the primitive token names from `colors-palette.md` where applicable. Error red is a system-only token — it is not part of the primitive palette.

| Property | Value |
|----------|-------|
| Background | `--surface-2` (`slate-800` / `#272727`) — one step above cards, feels inset |
| Border (default) | `1px solid rgba(255,255,255,0.1)` |
| Border (hover) | `1px solid rgba(255,255,255,0.2)` |
| Border (focus) | `1px solid var(--ultramarine)` (`ultramarine-600` / `#3B41EC`) + `box-shadow: 0 0 0 3px rgba(59,65,236,0.25)` |
| Border (error) | `1px solid #FF5252` (system) + `box-shadow: 0 0 0 3px rgba(255,82,82,0.2)` |
| Border radius | `var(--radius-2)` — 8px |
| Font | Figtree 400, 15px |
| Placeholder colour | `rgba(255,255,255,0.35)` |
| Disabled | `opacity: 0.4; cursor: not-allowed` |
| Transition | `border-color 0.15s, box-shadow 0.15s` |

---

## Field Anatomy

Every input field uses this structure:

```
[Label]           ← 13px, Figtree 500, rgba(255,255,255,0.6)
[Input element]   ← 44px height (single-line), surface-2 background
[Helper / Error]  ← 12px, below input, 4px gap
```

**Label:** Always above the input. Required fields marked with a red asterisk `*` (`#FF5252`).

**Helper text:** Muted (`rgba(255,255,255,0.4)`), used for format hints or constraints.

**Error text:** Red (`#FF5252`), prefixed with a filled `error` Material Symbol at 14px.

---

## Components

### Text Input

Single-line. Height: **44px**. Horizontal padding: `var(--space-3)` (12px).

```css
input[type="text"], input[type="email"], input[type="password"] {
  height: 44px;
  background: var(--surface-2);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: var(--radius-2);
  color: #ffffff;
  font-family: 'Figtree', sans-serif;
  font-size: 15px;
  padding: 0 var(--space-3);
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}

input:focus {
  border-color: var(--ultramarine);
  box-shadow: 0 0 0 3px rgba(59, 65, 236, 0.25);
}
```

**With leading icon:** Icon is 20px Material Symbol, `rgba(255,255,255,0.4)`, positioned absolutely left. Input padding-left increases to accommodate.

### Textarea

Multi-line. Minimum height: **100px**. Padding: `var(--space-3)` all sides. `resize: vertical` — never horizontal.

### Select

Height: **44px**. Native `<select>` with `appearance: none`. Custom chevron via `expand_more` Material Symbol positioned absolutely right. Padding-right must accommodate the chevron.

### Checkbox

Custom-styled. Size: **18×18px**.

| State | Appearance |
|-------|------------|
| Unchecked | `surface-2` background, `rgba(255,255,255,0.3)` border, `radius-1` |
| Checked | `var(--ultramarine)` (`ultramarine-600`) background and border, white `check` icon (FILL 1, weight 600) |
| Disabled | `opacity: 0.4` |

### Radio

Custom-styled. Size: **18×18px**, fully circular.

| State | Appearance |
|-------|------------|
| Unselected | `surface-2` background, `rgba(255,255,255,0.3)` border |
| Selected | `ultramarine-600` border, 8px `ultramarine-600` dot centred inside |
| Disabled | `opacity: 0.4` |

### Toggle

Pill-shaped switch. Track: **40×22px**, `radius-full`. Thumb: **16×16px**, white circle.

| State | Track | Thumb |
|-------|-------|-------|
| Off | `rgba(255,255,255,0.15)` | White, `opacity: 0.5`, left |
| On | `var(--ultramarine)` (`ultramarine-600`) | White, `opacity: 1`, right (translateX 18px) |

Transition: `background 0.2s`, `transform 0.2s`.

---

## States

| State | Visual |
|-------|--------|
| Default | `rgba(255,255,255,0.1)` border |
| Hover | `rgba(255,255,255,0.2)` border |
| Focus | `ultramarine-600` border + `0 0 0 3px rgba(59,65,236,0.25)` ring |
| Filled | `rgba(255,255,255,0.2)` border — slightly brighter to show value |
| Error | `#FF5252` border + `0 0 0 3px rgba(255,82,82,0.2)` ring + error message below |
| Disabled | `opacity: 0.4`, `cursor: not-allowed`, `pointer-events: none` |

---

## Rules

- **Never remove the focus ring.** It is critical for keyboard accessibility.
- **Always use a label.** Placeholder text is not a substitute — it disappears on input.
- **Error messages go below the field**, never inside it. Always pair error state with a descriptive message, not just a red border.
- **One column on mobile.** Form grids should collapse to a single column below 768px.
- **Group related fields.** Name fields (first + last) can sit side by side at 2-col. Unrelated fields should not share a row just to fill space.
- **Required fields** should be marked with `*` in the label, not just validated on submit.
- **Input height is always 44px** for single-line fields — matches the medium button height so paired button+input rows align perfectly.
