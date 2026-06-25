# social.plus Navigation

Source: canonical design system HTML

App bar, bottom tab bar, and back navigation. The primary navigation chrome of social.plus: always visible, always present, never intrusive.

---

## Navigation Tokens

| Token | Value |
|---|---|
| `--nav-bg` | `bg-elevated` |
| `--nav-border` | `border-subtle` |
| `--nav-icon-active` | `action-primary` |
| `--nav-icon-default` | `text-tertiary` |
| `--nav-height` | 56px |

---

## App Bar Variants

### Default (Home)

- Leading: social.plus logo mark (28px) + "social.plus" wordmark (Figtree Bold, 17px)
- Trailing actions: Search icon button (ghost, 36px), Notification bell icon button (ghost, 36px) with optional notification dot, User avatar (sm)
- Notification dot: 8px red circle with `bg-elevated` border, positioned at top-right of the bell icon

### Screen Title (with Back Button)

- Leading: Back chevron button (ghost, 36px) + screen title text (Figtree Bold, 17px)
- Trailing: Overflow menu icon button (three dots, ghost, 36px)

### Search Mode (Expanded)

- Search input field expands to fill the available width
- Search icon inside the input at the leading edge
- Clear button ("X") at the trailing edge of the input
- **Cancel** text button at the far right to exit search mode
- Input uses `radius-pill` border radius

---

## Bottom Tab Bar

Five-tab layout in a fixed bottom bar.

| Position | Tab | Icon |
|---|---|---|
| 1 | Home | House |
| 2 | Discover | Magnifying glass |
| 3 | Create | Floating action button (FAB) with plus icon |
| 4 | Activity | Bell (with optional notification dot) |
| 5 | Profile | Person silhouette |

The **Create** tab uses a FAB (floating action button) with a gradient or accent-colored circular button raised above the tab bar. The plus icon is white.

---

## Tab States

| State | Visual |
|---|---|
| **Active** | Icon and label use `action-accent` color; label uses bold weight (700) |
| **Default** | Icon and label use `text-tertiary` color; label uses semibold weight (600) |
| **Pressed** | Background tint (`border-faint`) behind the icon area; icon uses `text-secondary` color |
