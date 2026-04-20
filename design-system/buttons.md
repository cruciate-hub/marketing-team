# Buttons

## Variants

### Primary
The main call-to-action. Use once per section maximum.

- **Background:** Brand Blue Gradient — `linear-gradient(135deg, #45A5ED 0%, #5C6EF8 50%, #3B41EC 100%)` (`picton-blue-400` → `ultramarine-500` → `ultramarine-600`)
- **Text:** `#FFFFFF`
- **Border:** none
- **Hover:** background becomes solid `ultramarine-700` `#3133D1` + `box-shadow: 0 4px 16px rgba(59, 65, 236, 0.4)`
- **Pressed:** background becomes solid `ultramarine-800` `#2B2FA8`, `transform: scale(0.97)`
- **Disabled:** `opacity: 0.4`, `cursor: not-allowed`, gradient preserved

### Secondary
Paired alongside primary when a second action is needed.

- **Background:** transparent
- **Text:** `rgba(255, 255, 255, 0.85)`
- **Border:** `1px solid rgba(255, 255, 255, 0.3)`
- **Hover:** border becomes `rgba(255, 255, 255, 0.6)`, text becomes `#FFFFFF`
- **Active:** `transform: scale(0.97)`
- **Disabled:** `opacity: 0.4`, `cursor: not-allowed`

### Ghost
Low-emphasis actions. No border, no background.

- **Background:** transparent
- **Text:** `rgba(255, 255, 255, 0.6)`
- **Border:** none
- **Hover:** text becomes `#FFFFFF`, background `rgba(255, 255, 255, 0.06)`
- **Active:** `transform: scale(0.97)`
- **Disabled:** `opacity: 0.4`, `cursor: not-allowed`

### Destructive
Dangerous or irreversible actions only. Use sparingly. Destructive uses a system-only red (not part of the primitive palette).

- **Background:** `#FF5252`
- **Text:** `#FFFFFF`
- **Border:** none
- **Hover:** `filter: brightness(1.08)` + `box-shadow: 0 4px 16px rgba(255, 82, 82, 0.35)`
- **Active:** `transform: scale(0.97)`
- **Disabled:** `opacity: 0.4`, `cursor: not-allowed`

---

## Sizes

| Size   | Height | H. Padding | Font Size | Font Weight | Letter Spacing |
|--------|--------|------------|-----------|-------------|----------------|
| Small  | 32px   | 12px       | 13px      | 500         | 0.01em         |
| Medium | 44px   | 20px       | 15px      | 500         | 0.01em         |
| Large  | 56px   | 28px       | 17px      | 600         | 0.02em         |

All sizes use `font-family: 'Figtree', sans-serif` and `text-transform: none`.

---

## Shape

- **Default:** `border-radius: var(--radius-2)` (8px) for all standard buttons
- **Pill modifier:** `border-radius: var(--radius-full)` (9999px) — reserved for tags and chips only, not page-level buttons

---

## States

Primary button hover and pressed follow a clean step ladder up the Ultramarine scale: default `ultramarine-600` → hover `ultramarine-700` → pressed `ultramarine-800`.

| State    | Behaviour |
|----------|-----------|
| Default  | As defined per variant above |
| Hover    | As defined per variant above |
| Focus    | `outline: 2px solid #3B41EC; outline-offset: 3px` — always visible for accessibility |
| Active / Pressed | Primary: solid `ultramarine-800` `#2B2FA8`. All variants: `transform: scale(0.97)` |
| Disabled | `opacity: 0.4; cursor: not-allowed; pointer-events: none` — all variants |
| Loading  | Label replaced with spinner SVG; button width locked to prevent layout shift; `cursor: wait` |

---

## Icon Buttons

When a button contains only an icon (no label):

- Width equals height (square)
- Use Medium size by default (44×44px)
- Icon size: 20px for medium, 16px for small, 24px for large
- Same variant rules apply
- Always include an `aria-label`

---

## CSS Custom Properties Reference

```css
/* Sizes */
--btn-height-sm: 32px;
--btn-height-md: 44px;
--btn-height-lg: 56px;
--btn-px-sm: 12px;
--btn-px-md: 20px;
--btn-px-lg: 28px;

/* Primary gradient + state ladder */
--btn-primary-bg: linear-gradient(135deg, #45A5ED 0%, #5C6EF8 50%, #3B41EC 100%);
--btn-primary-bg-hover: #3133D1;    /* ultramarine-700 */
--btn-primary-bg-pressed: #2B2FA8;  /* ultramarine-800 */
--btn-primary-shadow-hover: 0 4px 16px rgba(59, 65, 236, 0.4);

/* Secondary */
--btn-secondary-border: rgba(255, 255, 255, 0.3);
--btn-secondary-border-hover: rgba(255, 255, 255, 0.6);

/* Destructive */
--btn-destructive-bg: #FF5252;
--btn-destructive-shadow-hover: 0 4px 16px rgba(255, 82, 82, 0.35);

/* Shared */
--btn-focus-ring: 2px solid #3B41EC;
--btn-transition: all 0.15s ease;
--btn-radius: var(--radius-2);
```

---

## Rules

- **Never** use more than one primary button in a single section or card.
- **Never** place a primary button next to a destructive button without a clear visual separator.
- **Do not** stretch buttons to full width unless inside a mobile-width container (≤ 400px) or a form flow.
- **Do not** use gradient text inside buttons — button labels are always solid `#FFFFFF` or `rgba(255,255,255,0.85)`.
- Icon + label buttons: icon always leads (left side), 8px gap between icon and label.
- Minimum touch target: 44×44px — never use the small size for mobile-primary interactions.
