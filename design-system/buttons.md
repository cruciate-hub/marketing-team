# social.plus Buttons

Source: canonical design system HTML

Every button maps to a clear intent hierarchy. Primary drives conversion. Secondary offers alternatives. Ghost keeps things quiet. Destructive signals consequence. All hit 44px minimum touch targets.

---

## Component Tokens

Each button owns a set of tokens that reference semantic tokens. Overriding a component token in a specific context never pollutes the rest of the system.

| Token | References |
|-------|-----------|
| `--btn-bg` | action-primary |
| `--btn-bg-hover` | action-primary-hover |
| `--btn-bg-press` | action-primary-press |
| `--btn-text` | text-inverse |
| `--btn-radius` | radius-md (12px) |
| `--btn-height` | 44px |
| `--btn-shadow` | shadow-glow |

---

## Variants

### 1. Primary

The main call-to-action. Use once per section maximum.

- **Background:** action-primary
- **Text:** white
- **Border:** none
- **Radius:** 12px

### 2. Secondary

Paired alongside primary when a second action is needed.

- **Background:** bg-elevated
- **Border:** border-default
- **Text:** text-primary

### 3. Ghost

Low-emphasis actions. No background, no border.

- **Background:** transparent
- **Text:** action-primary
- **Border:** none

### 4. Tinted

Soft emphasis that stays in the primary color family without full saturation.

- **Background:** action-primary-subtle
- **Text:** action-primary

### 5. Destructive

Dangerous or irreversible actions only. Use sparingly.

- **Background:** status-error
- **Text:** white

### 6. Pill

Compact rounded shape for inline actions like follow buttons.

- **Radius:** radius-pill
- **Padding:** compact horizontal padding
- Inherits color from the variant it is applied to

---

## Sizes

| Size | Height | Font Size |
|------|--------|-----------|
| xs | 32px | text-xs (12px) |
| sm | 36px | text-sm (13px) |
| md (default) | 44px | text-sm (13px) |
| lg | 52px | text-base (15px) |
| xl | 60px | text-md (17px) |

---

## States

### Primary States

| State | Visual |
|-------|--------|
| Default | action-primary background |
| Hover | action-primary-hover (`#3133D1`) + shadow-glow |
| Pressed | action-primary-press (`#2B2FA8`) + scale(0.97) |
| Loading | Spinner replaces label, button disabled, width locked to prevent layout shift, cursor: wait |
| Disabled | Reduced opacity, cursor: not-allowed |
| Success | status-success background with checkmark icon |

Primary hover and pressed follow a clean step ladder up the Ultramarine scale: default action-primary, hover action-primary-hover, pressed action-primary-press.

### Secondary States

| State | Visual |
|-------|--------|
| Default | bg-elevated background, border-default border |
| Hover | bg-card background, border-strong border |
| Pressed | bg-sunken background |
| Disabled | Reduced opacity, cursor: not-allowed |

---

## Icon Buttons

When a button contains only an icon (no label):

- Width equals height (square), same height as the corresponding text button size
- Available in Primary, Secondary, Ghost, and Destructive variants
- Same state rules apply (hover, pressed, disabled)
- Always include an `aria-label` for accessibility
- Icon size should be proportional to button size

---

## Full Width

Common on mobile screens. The button stretches to the full width of its container.

- Used in mobile layouts, form flows, or narrow containers
- Both Primary and Secondary variants support full-width mode
- Avoid full-width outside of constrained containers (keep to mobile-width or narrower)

---

## Rules

- **Never** use more than one primary button in a single section or card
- **Never** place a primary button next to a destructive button without a clear visual separator
- **Do not** stretch buttons to full width unless inside a mobile-width container or a form flow
- Icon + label buttons: icon always leads (left side), 8px gap between icon and label
- Minimum touch target: 44x44px. Never use the xs size for mobile-primary interactions
- **Never remove the focus ring.** It is critical for keyboard accessibility
