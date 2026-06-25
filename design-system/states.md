# social.plus States

Source: canonical design system HTML

Every interactive element exists in multiple states. This matrix shows how each component responds to user actions, system conditions, and data states, so nothing is left undesigned.

---

## Component x State Matrix

### Button (Primary)

| State | Visual |
|---|---|
| Default | Standard primary fill and text |
| Hover | Slightly lighter/darker fill shift |
| Pressed | Depressed appearance with reduced brightness |
| Focused | 3px `action-primary-subtle` outline with 2px offset |
| Disabled | Reduced opacity, non-interactive |
| Loading | Spinner icon before label text, disabled state |
| Error | N/A |
| Success | Green background with checkmark, "Done" label |

### Input (Text Field)

| State | Visual |
|---|---|
| Default | Standard border, placeholder text |
| Hover | Filled/highlighted border |
| Pressed | Active input, focused border with accent color |
| Focused | `action-accent` border color with 3px `action-primary-subtle` outline, 2px offset |
| Disabled | Muted background and text, non-interactive |
| Loading | N/A |
| Error | `status-error` border color |
| Success | `status-success` border color |

### Toggle (Switch)

| State | Visual |
|---|---|
| Default | Off position (grey track, thumb at left) |
| Hover | Slightly darkened track |
| Pressed | Slight scale-down (0.95) |
| Focused | On position with 3px `action-primary-subtle` outline, 2px offset |
| Disabled | Muted colors, non-interactive |
| Loading | N/A |
| Error | N/A |
| Success | On position with `status-success` green track |

### Checkbox (Selection)

| State | Visual |
|---|---|
| Default | Unchecked, standard border |
| Hover | Border changes to `action-accent` |
| Pressed | `action-accent` border with slight scale-down (0.92) |
| Focused | Checked state with 3px `action-primary-subtle` outline, 2px offset |
| Disabled | Muted border and fill, non-interactive |
| Loading | N/A |
| Error | `status-error` border with `status-error-subtle` shadow ring |
| Success | `status-success` background and border, white checkmark |

### Card (Feed / Community)

| State | Visual |
|---|---|
| Default | Standard card with `shadow-sm` |
| Hover | Lift with `translateY(-2px)` and `shadow-md` |
| Pressed | Scale-down (0.98) with `shadow-sm` |
| Focused | `action-accent` border with 2px `action-primary-subtle` ring |
| Disabled | 40% opacity |
| Loading | Skeleton lines replacing content |
| Error | `status-error` border with `status-error-subtle` ring, "Failed to load" text |
| Success | `status-success` border, checkmark with "Joined!" text |

### List Item (Row)

| State | Visual |
|---|---|
| Default | Standard row appearance |
| Hover | `border-faint` background fill |
| Pressed | `bg-sunken` background fill |
| Focused | 2px `action-accent` outline inset |
| Disabled | 40% opacity |
| Loading | Spinner icon + "Loading" text |
| Error | `status-error` text color |
| Success | `status-success` text color with checkmark, "Saved" label |

---

## Screen-Level States

| State | Description | Recovery |
|---|---|---|
| **Loading** | Skeleton screens and spinners while content fetches. Never block the whole screen; load progressively. | Automatic on data arrival |
| **Error** | Clear message, a reason if possible, and a recovery action. Uses error icon on `status-error-subtle` background. | "Try again" button |
| **Offline** | No network connection. Show cached content where possible. Disable actions that require connectivity. | Automatic reconnect |
| **Success** | Action completed. Show confirmation, then transition automatically or let the user continue. Uses checkmark icon on `status-success-subtle` background. | Auto-transition or user dismiss |
| **Partial load** | Some content loaded, some failed. Show what is available, indicate what is missing with inline error states. | Per-section retry |
| **Permission gate** | Feature requires a permission (notifications, camera). Explain why before requesting. Never surprise the OS dialog. Uses shield icon on `action-primary-subtle` background. | "Allow [permission]" button |
