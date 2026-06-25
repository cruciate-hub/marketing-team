# social.plus Spacing

Source: canonical design system HTML

## Base unit

All spacing uses a **4px base grid**. Every layout decision (padding, gap, margin) maps to a named step. This keeps rhythm consistent across every screen in the app.

---

## Spacing scale

11 tokens. Always use a token from this scale. Do not use arbitrary pixel values.

| Token | Value | Multiplier | Common usage |
|-------|-------|------------|--------------|
| `--space-1` | 4px | 1x | Icon gap, badge padding, micro nudges |
| `--space-2` | 8px | 2x | Chip inner padding, tight icon + label |
| `--space-3` | 12px | 3x | Button padding (vertical), input inner padding |
| `--space-4` | 16px | 4x | Button padding (horizontal), card inner gap, nav item |
| `--space-5` | 20px | 5x | Card padding, section inner gap |
| `--space-6` | 24px | 6x | Card padding (large), modal padding |
| `--space-8` | 32px | 8x | Section gap, screen horizontal padding |
| `--space-10` | 40px | 10x | Between major sections on screen |
| `--space-12` | 48px | 12x | Hero padding, large screen breathing room |
| `--space-16` | 64px | 16x | Page-level vertical rhythm |
| `--space-20` | 80px | 20x | Bottom nav safe area clearance |

---

## Usage guidance

### Micro spacing (4-8px)

- `space-1` (4px): the smallest intentional gap. Use between an icon and its label when they need to sit tight, or for badge internal padding.
- `space-2` (8px): standard chip padding, the gap between an avatar and adjacent text inside list items, or tight vertical stacking.

### Component spacing (12-24px)

- `space-3` (12px): vertical padding inside buttons, inner padding of input fields, and the gap between stacked cards.
- `space-4` (16px): horizontal button padding, inner gap of card content, nav item padding, and the standard horizontal screen padding on mobile.
- `space-5` (20px): standard card padding, inner gap within a section.
- `space-6` (24px): large card padding, modal inner padding.

### Layout spacing (32-80px)

- `space-8` (32px): gap between major sections within a screen, horizontal page padding on larger viewports.
- `space-10` (40px): separation between major content sections.
- `space-12` (48px): hero section padding, generous breathing room on large screens.
- `space-16` (64px): page-level vertical rhythm between top-level content blocks.
- `space-20` (80px): reserved for bottom content padding that clears the bottom navigation bar on mobile.

---

## Mobile screen anatomy

A typical mobile screen applies these tokens in layers:

- **Screen horizontal padding:** `space-4` (16px) on both sides
- **App bar height rhythm:** `space-4` (16px) vertical padding
- **Gap between stacked cards:** `space-3` (12px)
- **Card inner padding:** `space-4` (16px)
- **Avatar-to-text gap in list items:** `space-2` (8px)
- **Bottom content clearance:** `space-20` (80px) to clear the navigation bar

---

## Touch targets

All interactive elements must meet a **44px minimum** touch target size per iOS and Android guidelines. This is independent of the spacing scale but interacts with it: a button using `space-3` vertical padding on `text-base` text naturally reaches the 44px minimum.

---

## Principles

1. **Always use a token.** Never hard-code a pixel value for spacing. If no token fits, round to the nearest one.

2. **Consistent insets.** When a container uses `space-4` for horizontal padding, use `space-4` vertically too, unless a deliberate asymmetry is needed (e.g., buttons use `space-3` vertical and `space-4` horizontal).

3. **Spacing grows with hierarchy.** Small elements (chips, badges) use `space-1` to `space-2`. Components (cards, inputs) use `space-3` to `space-6`. Layout-level gaps use `space-8` and above.

4. **Breathing room scales up.** The jump from `space-6` to `space-8` (24px to 32px) marks the transition from component-level to section-level spacing. Use this boundary intentionally.
