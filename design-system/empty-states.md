# social.plus Empty States

Source: canonical design system HTML

The moment before content exists. Empty states should feel warm and inviting, not clinical. Each one has a clear illustration area, a human headline, a supporting line, and one action.

---

## Full-Page Empty States

Each full-page empty state follows a consistent structure:

1. **Gradient illustration area**: A circular region (approximately 48x48 icon) with a gradient background from the palette, containing a white stroke icon
2. **Title**: A warm, human headline
3. **Body text**: One to two sentences of supporting context
4. **Primary action button**: A single clear call to action
5. **Screen label**: Identifies which screen this empty state belongs to

### Screens

| Screen | Gradient | Title | Action |
|---|---|---|---|
| Home feed (first visit) | `grad-warm` | Find your communities | Explore communities |
| Messages (empty inbox) | `grad-forest` | No messages yet | Start a conversation |
| Search (no results) | `grad-gold` | No results for "[query]" | Create a community + Clear search |
| Activity (all caught up) | `grad-cinema` | All caught up | None (informational only) |
| Members (no members) | `grad-ember` | No members yet | Invite members |
| Error (failed to load) | `bg-sunken` with `border-subtle` | Couldn't load this | Try again (secondary style) |

Notes:
- The Search empty state is unique in offering two actions: a primary button and a secondary button side by side.
- The Activity empty state has no action button since there is nothing for the user to do.
- The Error empty state uses a muted background instead of a gradient, with a grey icon, to differentiate it from feature-level empty states.

---

## Inline Empty State

Used within a card or list context when a subsection has no content.

- **Icon**: Smaller tinted circle (48px diameter, `action-primary-subtle` background) with an `action-accent` stroke icon
- **Title**: Short heading (14px, semibold)
- **Body**: Brief context text (13px, `text-secondary`)
- **Action button**: Tinted style, sm size

The inline variant is centered within its container, uses card padding (`space-8` vertical, `space-5` horizontal), and is non-interactive at the card level (cursor: default).
