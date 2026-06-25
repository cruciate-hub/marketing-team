# social.plus Feedback

Source: canonical design system HTML

Toasts, banners, progress indicators, and skeleton loaders. The system's way of communicating status without disrupting the user's flow.

---

## Toast Tokens

| Token | Value |
|---|---|
| `--toast-bg` | `bg-card` |
| `--toast-border` | `border-subtle` |
| `--toast-shadow` | `shadow-lg` |
| `--toast-radius` | `radius-xl` |
| `--toast-z` | `z-toast` (400) |

---

## Toast Variants

| Variant | Icon Color | Action |
|---|---|---|
| **Success** | Green (`status-success`) | Dismiss button (X) |
| **Error** | Red (`status-error`) | Retry action button |
| **Info** | Blue (`status-info`) | View action button |
| **Warning** | Yellow (`status-warning`) | Dismiss button (X) |

### Toast Anatomy

- **Icon**: Status-colored icon at the leading edge
- **Title**: Bold primary text describing the event
- **Body** (optional): Supporting detail text beneath the title
- **Action**: Either a dismiss button (X) or a contextual action button (Retry, View) at the trailing edge

Maximum width: 440px. Toasts stack vertically with `space-3` gap.

---

## Progress Indicators

Linear bar with a label row showing the metric name and percentage.

| Color | Usage |
|---|---|
| `action-primary` | Default progress (e.g., profile completion) |
| `status-warning` | Near full / approaching limit (e.g., community capacity at 91%) |
| `status-success` | Complete (e.g., upload finished, shows "Done") |

### Animated State

Active uploads show a spinner icon inline with the label text and an animated progress fill bar.

---

## Skeleton Loaders

Placeholder UI shown while content is loading. Uses pulsing animation on grey shapes.

### Post Skeleton

- Circle placeholder (avatar position)
- Two short lines (author name and meta)
- Three text lines of varying widths (100%, 88%, 70%)
- Rectangle placeholder (image attachment area)

### Community Card Skeleton

- Rectangle placeholder at the top (header image area, 72px tall)
- Title line (140px wide, 16px tall)
- Two shorter lines (meta and description)
- Footer: three small overlapping circle placeholders (avatar stack) + rectangle placeholder (button area, 60px wide, 32px tall)
