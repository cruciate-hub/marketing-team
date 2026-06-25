# social.plus Typography

Source: canonical design system HTML + Webflow heading scale

## Typeface

social.plus uses a single typeface for all surfaces: **Figtree**, a geometric, warm, confident sans-serif available from Google Fonts with variable weight support (300-900).

**Font stack:**
```
'Figtree', 'Inter', sans-serif
```

Both `--font-display` and `--font-body` resolve to the same stack. Figtree Bold carries display moments (headlines, CTAs, quotes, hero copy). Regular and Medium keep body copy clear and human.

---

## Heading scale (fluid clamp)

All headings use Figtree Bold (700) and scale fluidly with viewport width via `clamp()`. The `svw` unit ensures consistent scaling across all viewport types.

| Level | CSS value | Range | Line height |
|-------|-----------|-------|-------------|
| H1 Display | `clamp(2.75rem, 1.5rem + 2svw, 5rem)` | 44px - 80px | 1.1 |
| H2 Section | `clamp(2.25rem, 1.5rem + 2svw, 3.25rem)` | 36px - 52px | 1.25 |
| H3 Sub-section | `clamp(1.75rem, 1rem + 2svw, 2.25rem)` | 28px - 36px | 1.25 |
| H4 Small heading | `clamp(1.5rem, 0.875rem + 2svw, 1.75rem)` | 24px - 28px | 1.25 |
| H5 Compact heading | `1.25rem` | 20px | 1.25 |
| H6 Smallest heading | `1.125rem` | 18px | 1.25 |

---

## Body text scale

Interface and body text sizes. These are fixed (no clamp).

| Token | Size (rem) | Size (px) | Line height | Weight | Usage |
|-------|-----------|-----------|-------------|--------|-------|
| `text-lg` | 1.25rem | 20px | 1.3 | 500 | Section headings within UI |
| `text-md` | 1.0625rem | 17px | 1.35 | 500 / 400 | Card titles, strong body text |
| `text-base` | 0.9375rem | 15px | 1.45 | 400 | Default body text |
| `text-sm` | 0.8125rem | 13px | 1.4 | 400 / 500 | Secondary labels, metadata |
| `text-xs` | 0.75rem | 12px | 1.4 | 500 / 600 | Captions, overlines, badges (uppercase, letter-spacing 0.06em) |

**Minimum font size:** 0.75rem (12px). Nothing in the system goes smaller.

---

## Font weights

Five named weight tokens spanning the variable font range actually used.

| Token | Value | Name |
|-------|-------|------|
| `--weight-light` | 300 | Light |
| `--weight-regular` | 400 | Regular |
| `--weight-medium` | 500 | Medium |
| `--weight-semibold` | 600 | Semibold |
| `--weight-bold` | 700 | Bold |

**Display usage:** weights 400 (italic), 600, and 700. Headlines, CTAs, quotes, hero copy.

**Body usage:** weights 300, 400, 500, 600, 700. Body text, UI labels, inputs, captions.

---

## Line heights

Four named line-height tokens.

| Token | Value | Usage |
|-------|-------|-------|
| `--leading-tight` | 1.1 | Display headlines, hero text |
| `--leading-snug` | 1.25 | Sub-headings, card titles, H2-H6 |
| `--leading-normal` | 1.45 | Default body text |
| `--leading-relaxed` | 1.6 | Long-form body, metadata |

---

## Type pairings

Recommended heading + body combinations drawn from the design system.

### Feed post header
- **Title:** 22px / Bold 700 / line-height 1.1
- **Meta:** 13px / Regular 400 / line-height 1.5 / secondary color

### CTA / Onboarding
- **Headline:** 26px / Bold 700 / line-height 1.05 (white on dark)
- **Accent word:** italic, brand accent color
- **Supporting text:** 13px / Regular 400 / line-height 1.5 / 60% white

### Section title + body
- **Overline:** 12px / Semibold 600 / uppercase / letter-spacing 0.10em / accent color
- **Title:** 17px / Semibold 600
- **Description:** 14px / Regular 400 / line-height 1.5 / secondary color

### Profile name + handle
- **Name:** 20px / Bold 700
- **Handle:** 13px / Regular 400 / tertiary color

---

## Typesetting principles

1. **Heading line height stays tight.** Display text uses line heights between 1.1 and 1.25. Tighter leading keeps headlines punchy and compact.

2. **Body line height opens up.** Body text at `text-base` and below uses 1.4 to 1.45 for comfortable reading. Long-form content can stretch to 1.6.

3. **Letter spacing for caps.** Any uppercase text (`text-xs` captions, overlines, badges) must include letter-spacing of at least 0.06em. Section overlines use 0.10em.

4. **Uppercase is reserved.** Only use uppercase for captions, overlines, and small badges at `text-xs`. Never set body text, headings, or button labels in all caps.

5. **One typeface everywhere.** Figtree is the only typeface. Do not introduce secondary faces. Weight and size alone create hierarchy.

6. **Weight creates hierarchy, not size alone.** Pair weight shifts with size shifts. A card title at 17px / Semibold 600 sits above body text at 15px / Regular 400.
