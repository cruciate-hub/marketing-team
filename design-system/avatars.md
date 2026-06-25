# social.plus Avatars

Source: canonical design system HTML

Avatars represent people and communities. User avatars show photos or initials. Community avatars use the gradient palette to give each community a distinct, warm identity.

---

## Component Tokens

| Token | Value |
|---|---|
| `--avatar-size-xs` | 24px |
| `--avatar-size-sm` | 32px |
| `--avatar-size-md` | 44px |
| `--avatar-size-lg` | 56px |
| `--avatar-size-xl` | 72px |
| `--avatar-radius` | `radius-full` (fully round) |
| `--avatar-border` | `bg-elevated` 2px |

---

## User Avatars

Five sizes, each displaying initials on a gradient background. Initials use **Figtree Bold**.

| Size | Diameter | Token |
|---|---|---|
| xs | 24px | `--avatar-size-xs` |
| sm | 32px | `--avatar-size-sm` |
| md | 44px | `--avatar-size-md` |
| lg | 56px | `--avatar-size-lg` |
| xl | 72px | `--avatar-size-xl` |

When a user photo is available, it replaces the initials. The gradient background serves as the fallback.

---

## States and Decorators

| State | Visual |
|---|---|
| **Online indicator** | Small green dot positioned at the bottom-right of the avatar |
| **Offline** | Small grey dot positioned at the bottom-right of the avatar |
| **Notification badge** | Red circle with count number at the top-right corner |
| **Verified** | Blue checkmark circle at the bottom-right corner |
| **Add button** | Dashed border (`border-default`) with a plus icon centered; background uses `bg-sunken` |
| **Placeholder** | User silhouette icon on `bg-sunken` background; used when no photo or initials are available |

---

## Avatar Stacks

Overlapping avatar chips used for member previews. Each chip uses the sm (32px) size.

- Chips overlap with a **-8px margin** between each
- An overflow counter (e.g., "+24") appears at the end when the member count exceeds the visible chips
- A label beneath the stack displays context (e.g., "28 members" or "3 mutual friends")

---

## Community Avatars

Each community picks from the gradient palette. The letter mark uses **Figtree Bold**.

- Display a single uppercase letter representing the community name
- Background uses one of the system gradient tokens (`--grad-warm`, `--grad-forest`, `--grad-cinema`, `--grad-gold`, `--grad-night`, `--grad-ember`, `--grad-clay`, `--grad-river`)
- Fully round shape, same as user avatars
- Typically accompanied by community name and member count
