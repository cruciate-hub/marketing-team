# social.plus Inputs and Selections

Source: canonical design system HTML

Inputs are the primary way users contribute. They should feel open and welcoming with a soft background, generous padding, and an expressive focus state. Selection controls let users make choices and should be immediately legible and satisfying to interact with.

---

## Input Component Tokens

| Token | References |
|-------|-----------|
| `--input-bg` | bg-sunken |
| `--input-border` | border-default |
| `--input-border-focus` | action-primary |
| `--input-border-error` | status-error |
| `--input-text` | text-primary |
| `--input-placeholder` | text-tertiary |
| `--input-radius` | radius-md (12px) |
| `--input-height` | 48px |

---

## Text Input States

| State | Visual |
|-------|--------|
| Default | border-subtle border, bg-sunken background, at rest |
| Focused | border: action-primary + 3px glow ring |
| Filled | User has typed, bg-sunken, border-default |
| Error | border: status-error + 3px glow ring + error hint text below |
| Success | Success border + confirmation hint text below |
| Disabled | Reduced opacity, not editable, no hover response |

---

## Adornments

Inputs support several adornment patterns:

- **Leading icon:** Search icon or contextual icon positioned at the left edge of the input. Input padding adjusts to accommodate.
- **Trailing action:** A clear button (x) on the right side, visible when the input has a value.
- **Label + helper text:** Label above the input, helper text below for format hints or constraints. Always use a label; placeholder text is not a substitute since it disappears on input.
- **Character count:** Displayed at the trailing edge of the input, showing current length against the maximum (e.g. 0/60).

---

## Textarea

Multi-line text input for longer content.

- Auto-grows with content
- Minimum 3 rows
- Same focus state as text inputs (action-primary border + glow ring)
- Same background and border tokens as single-line inputs

---

## Search Bar

App-level search with distinct styling:

- Leading search icon
- Pill radius (radius-pill)
- Clear button visible when the search is active
- Separate from inline text inputs; used for global or section-level search

---

## Selections

### Toggle / Switch

Pill-shaped switch for binary on/off settings.

| State | Visual |
|-------|--------|
| Off | border-default background |
| On | action-primary background, white thumb |
| Disabled | Reduced opacity, non-interactive |

- **Transition duration:** duration-fast
- **Easing:** ease-in-out

Component tokens:

| Token | References |
|-------|-----------|
| `--toggle-bg-off` | border-default |
| `--toggle-bg-on` | action-primary |
| `--toggle-thumb` | white |
| `--toggle-duration` | duration-fast |
| `--toggle-ease` | ease-in-out |

### Checkbox

Custom-styled square control for multi-select choices.

| State | Visual |
|-------|--------|
| Unchecked | Default border, no fill |
| Checked | action-primary background + white checkmark icon |
| Indeterminate | action-primary background + white horizontal dash |
| Disabled | Reduced opacity, non-interactive |

### Radio

Custom-styled circular control for single-select choices within a group.

| State | Visual |
|-------|--------|
| Unchecked | Default border, circular, no fill |
| Checked | action-primary ring + action-primary dot centered inside |
| Disabled | Reduced opacity, non-interactive |

### Filter Chips

Compact pill-shaped controls for filtering content by category.

| State | Visual |
|-------|--------|
| Default | Subtle background, standard text |
| Active | action-primary background + white text |
| Disabled | Reduced opacity, non-interactive |

Chips are typically displayed in a horizontal wrap layout. Multiple chips can be active simultaneously (multi-select behavior).

---

## Rules

- **Never remove the focus ring.** It is critical for keyboard accessibility.
- **Always use a label.** Placeholder text is not a substitute since it disappears on input.
- **Error messages go below the field**, never inside it. Always pair error state with a descriptive message, not just a red border.
- **One column on mobile.** Form grids should collapse to a single column below 768px.
- **Group related fields.** Name fields (first + last) can sit side by side at 2-col. Unrelated fields should not share a row just to fill space.
- **Required fields** should be marked with `*` in the label, not just validated on submit.
