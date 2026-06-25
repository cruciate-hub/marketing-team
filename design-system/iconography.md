# social.plus Iconography

Source: canonical design system HTML

## Library

**Google Material Symbols**, the variable font icon library from Google.
Not to be confused with the older Material Icons library; Material Symbols is the current standard and supports variable axes for weight, fill, grade, and optical size.

**Import:**
```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-25..200" />
```

**Usage:**
```html
<span class="material-symbols-outlined">chat</span>
```

---

## Style

**Outlined** is the default style for social.plus. It reads as clean, precise, and premium, consistent with Figtree's geometric character and the brand's bold confidence.

**Filled** is reserved for active and selected states only. A filled icon signals that something is on, selected, or active. Do not use filled icons as decorative defaults.

---

## Variable Axes

Material Symbols is a variable font with four axes. social.plus uses the following defaults:

| Axis | Token | Value | Notes |
|------|-------|-------|-------|
| `opsz` (Optical size) | - | Match icon size in px | 20 for small UI, 24 for default, 40+ for decorative |
| `wght` (Weight) | - | `300` for light UI, `400` default, `500` for emphasis | Match surrounding text weight where possible |
| `FILL` | - | `0` default (outlined), `1` for active/selected state | Never use fractional fill values |
| `GRAD` (Grade) | - | `0` default | Increase to `100-200` only for very large decorative icons |

```css
.icon {
  font-family: 'Material Symbols Outlined';
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}

.icon--active {
  font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
```

---

## Sizes

Icon sizes are tied to the spacing scale and to context.

| Size | Value | Use |
|------|-------|-----|
| XS | 16px | Dense UI: table cells, badges, inline labels |
| SM | 20px | Compact components: small buttons, tags, input adornments |
| MD | 24px | Default: nav, standard buttons, cards, list items |
| LG | 32px | Feature callouts, section headers, empty states |
| XL | 40px | Decorative: hero sections, large feature blocks |
| 2XL | 48px | Illustration-scale: onboarding, empty states, marketing |

Always set `opsz` to match the rendered size in px.

---

## Colour

| Context | Colour |
|---------|--------|
| Default (on dark background) | `rgba(255, 255, 255, 0.7)` |
| Emphasis / label icon | `#FFFFFF` |
| Muted / disabled | `rgba(255, 255, 255, 0.3)` |
| Accent on light | `#3B41EC` (action-primary) |
| Accent on dark | `#7B94FE` (action-accent, 6.75:1 on #111) |
| Success (light) | `#1B89DC` |
| Success (dark) | `#1DC497` |
| Warning (light) | `#CC9202` |
| Warning (dark) | `#F7C506` |
| Error / destructive | `#FF305A` |
| Inherit from parent text | `currentColor` (preferred in components) |

---

## Pairing with Buttons

When placing an icon inside a button, follow the button system rules:

- Icon always leads (left side of label)
- Gap between icon and label: `var(--space-2)` (8px)
- Icon size matches button size: SM button = 16px icon, MD = 20px icon, LG = 24px icon
- Icon colour inherits from button text (`currentColor`)

---

## Rules

- **Use outlined by default.** Only switch to filled for active/selected states.
- **Never mix styles.** Do not use some outlined and some filled icons in the same component or section unless intentionally communicating state.
- **Never scale icons with arbitrary px values.** Use the size table above and set `opsz` accordingly.
- **Do not use icons alone as the only affordance.** Always pair with a label or `aria-label` for accessibility.
- **Do not use icons decoratively in body text.** Icons in running copy are disruptive and hard to localise.
- **Prefer semantic icon choices.** Use the icon that most literally represents the action. Avoid abstract or clever metaphors that users may not recognise.
