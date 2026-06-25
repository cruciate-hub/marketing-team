# social.plus Badges and Tags

Source: canonical design system HTML

Badges communicate counts and status. Tags label content. Both are compact, high-signal, and should never compete with primary content for attention.

---

## Badge Tokens

| Token | Value |
|---|---|
| `--badge-bg` | `action-primary` |
| `--badge-text` | `text-inverse` |
| `--badge-radius` | `radius-pill` |
| `--badge-size` | 18px |
| `--badge-font` | `text-xs` / bold |

---

## Notification Badges

| Variant | Description |
|---|---|
| **Count** | Red pill with numeric count (e.g., "3") positioned at the top-right of the host element |
| **Dot** | Small red dot with no number; indicates unread activity without a specific count |
| **Max (99+)** | When count exceeds 99, display "99+" to cap the label width |
| **New** | Green background (`status-success`) with the text "New"; used on avatars or icons to flag new items |

---

## Status Badges

Inline pill badges used to communicate the state of an item.

| Variant | Color | Example |
|---|---|---|
| **Success** | Green | "Joined" |
| **Warning** | Yellow | "Pending" |
| **Error** | Red | "Declined" |
| **Info** | Blue | "New" |
| **Neutral** | Grey | "Draft" |

---

## Tags

Tags label content with category or attribute information.

### Filled

Solid background tags using the palette colors: terra, sage, sand, neutral.

### Outlined

Border-only tags with transparent fill: terra, sage, sand variants.

### With Icon

Tags can include a leading icon or emoji alongside the label text. Icon and text are laid out inline with a 4px gap.

### Dismissible

Tags with an "X" button at the trailing edge. Clicking the X removes the tag. Available in terra, sage, sand color variants.
