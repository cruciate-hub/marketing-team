# social.plus List Items

Source: canonical design system HTML

The repeating unit of every feed, settings screen, and member list. Consistent height, generous touch target, clear visual hierarchy across leading, content, and trailing zones.

---

## Anatomy

Every list item follows a three-zone layout:

| Zone | Purpose |
|---|---|
| **Leading** | Icon wrap, avatar, or community avatar |
| **Content** | Title (primary text) + optional subtitle (secondary text) |
| **Trailing** | Chevron, toggle, button, badge, or other action element |

---

## Variants

### Basic Row

Title text only with a trailing chevron.

### With Subtitle

Title + subtitle text. Subtitle provides secondary context (e.g., "Manage alerts for communities and messages"). Trailing chevron.

### Leading Icon

Tinted icon wrap (colored background circle with matching icon) + title + subtitle. The icon wrap background uses a subtle variant of the icon color (e.g., `action-primary-subtle` with `action-accent` stroke).

### With Avatar (Member Row)

User avatar (sm, 32px) in the leading zone. Title shows the member name, subtitle shows handle and community count. Trailing zone contains a tinted **Follow** button.

### With Community Avatar

Community avatar (gradient background, letter mark, rounded square, ~36px) in the leading zone. Title shows community name, subtitle shows member count and post activity. Trailing zone may contain a notification badge.

### With Toggle

Leading icon wrap + title + subtitle. Trailing zone contains a toggle switch instead of a chevron.

### Destructive

Red icon in `status-error-subtle` background. Title text uses destructive (red) color. No trailing element. Used for actions like "Leave community."

### Disabled

Locked icon in `bg-sunken` background. Title and subtitle use muted colors. Trailing zone shows a "Pro" badge indicating the feature requires an upgrade. Entire row is non-interactive.

---

## Grouped Section List

Settings-style pattern with items organized into labeled groups.

- **Section header**: Uppercase label text above each group
- **Grouped items**: Items within a group share a card-like container with inset borders between rows
- The last item in each group has no bottom border
- Each group is separated by vertical spacing
