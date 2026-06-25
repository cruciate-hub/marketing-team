# social.plus Overlays

Source: canonical design system HTML

Modals, bottom sheets, and tooltips layer above the current screen. They use the z-index scale and always sit behind a darkened overlay backdrop.

---

## Bottom Sheet

- **Handle bar**: Small rounded bar centered at the top of the sheet, indicating swipe-to-dismiss
- **Title**: Bold heading text (e.g., "Join this community?")
- **Body**: Supporting descriptive text below the title
- **Action buttons**: Full-width buttons stacked vertically; primary action first, secondary action below
- Sits above the overlay backdrop (darkened screen)
- Slides up from the bottom of the screen

---

## Modal / Dialog

- **Icon area**: Circular icon container with a tinted background matching the action type (e.g., `status-error-subtle` background with `status-error` icon for destructive dialogs)
- **Title**: Bold heading text (e.g., "Leave community?")
- **Body**: Explanation text describing the consequences or context of the action
- **Action buttons**: Side-by-side buttons; destructive action on the left, cancel on the right. Both use `flex: 1` for equal width.
- Centered on the overlay backdrop

---

## Context Menu

- Vertical list of menu items, each with a leading icon and label text
- Items are separated by spacing; a **divider** line separates standard items from destructive items
- **Destructive item** at the bottom uses red text and icon color
- Compact padding, card-like container with rounded corners

---

## Tooltip

- Small dark box with brief instructional text
- Arrow/caret pointing toward the trigger element
- Can be positioned above, below, or to the left of the trigger
- Used for hover or tap-to-reveal explanatory text on interactive elements
