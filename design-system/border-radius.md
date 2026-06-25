# social.plus Border Radius

Source: canonical design system HTML

## Philosophy

social.plus uses generous, soft curves that echo the rounded logo mark. The feel should be warm and approachable, never cold or boxy. Radius scales from sharp utility elements up to fully circular avatars, with a clear semantic role at each step.

---

## Radius scale

9 tokens. Always use a token from this scale. Do not use arbitrary radius values.

| Token | Value | Context |
|-------|-------|---------|
| `--radius-xs` | 4px | Tags, code badges, micro chips |
| `--radius-sm` | 8px | Buttons (small), nav items, tooltips |
| `--radius-md` | 12px | Buttons (default), input fields, small cards |
| `--radius-lg` | 16px | Feed cards, list items, dropdowns |
| `--radius-xl` | 20px | Large cards, context panels |
| `--radius-2xl` | 24px | Modal sheets, featured cards |
| `--radius-3xl` | 32px | Bottom sheets, hero images |
| `--radius-pill` | 100px | Pill buttons, search bar, toggles |
| `--radius-full` | 50% | Avatars, icon buttons, indicators |

---

## Usage guidance

### Micro radius (4-8px)

- `radius-xs` (4px): the sharpest rounding in the system. Used for inline tags, code-style badges, and small filter chips where a subtle softening is enough.
- `radius-sm` (8px): small buttons, nav items within a tab bar, and tooltips.

### Component radius (12-20px)

- `radius-md` (12px): the default for most interactive elements. Standard buttons, input fields, and compact cards all use this value. This is the go-to when nothing more specific applies.
- `radius-lg` (16px): feed cards, list item containers, and dropdown menus. The step up from `radius-md` signals a larger container surface.
- `radius-xl` (20px): large cards and context panels that need more visual softness.

### Container radius (24-32px)

- `radius-2xl` (24px): modal sheets and featured/highlight cards. The generous rounding signals an elevated, focused surface.
- `radius-3xl` (32px): bottom sheets and hero image containers. The largest fixed-pixel radius in the system.

### Special shapes

- `radius-pill` (100px): creates a fully rounded capsule shape on elements shorter than 200px. Used for pill-style buttons, the search bar, and toggle tracks.
- `radius-full` (50%): creates a perfect circle when applied to a square element. Used exclusively for avatars, circular icon buttons, and status indicators.

---

## Radius in context

| Element | Token | Result |
|---------|-------|--------|
| "Join Community" button | `radius-md` | 12px rounded corners |
| "Follow" pill button | `radius-pill` | Fully rounded capsule |
| "Photography" / "Outdoors" tags | `radius-xs` | 4px subtle rounding |
| Feed card (post preview) | `radius-lg` | 16px soft corners |
| User avatars (all sizes) | `radius-full` | Perfect circle |
| "Invite to community" modal | `radius-2xl` | 24px generous rounding |

---

## Principles

1. **Never use sharp corners.** Every visible surface has at least `radius-xs` (4px). Zero-radius rectangles do not appear in the product.

2. **Radius matches element scale.** Small inline elements use small radii. Large container surfaces use large radii. A feed card at `radius-lg` (16px) contains a tag at `radius-xs` (4px); the nesting creates visual hierarchy.

3. **Buttons have two shapes.** Standard action buttons use `radius-md` (12px). Pill/follow-style buttons use `radius-pill` (100px). Do not mix other radii on buttons.

4. **Avatars are always circles.** Any avatar, at any size, uses `radius-full` (50%). No rounded-square avatars.

5. **Nested radius rule.** When a rounded container holds a rounded child, the child's radius should be smaller than the parent's. A `radius-2xl` modal should contain `radius-md` buttons, not `radius-2xl` buttons.
