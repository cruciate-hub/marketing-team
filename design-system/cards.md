# social.plus Cards

Source: canonical design system HTML

Cards are the primary unit of information in social.plus. They surface communities, posts, members, and events. Soft slate background, generous radius, subtle lift on interaction.

---

## Card Tokens

| Token | Value |
|---|---|
| `--card-bg` | `bg-card` |
| `--card-border` | `border-subtle` |
| `--card-radius` | `radius-lg` (16px) |
| `--card-padding` | `space-4` (16px) |
| `--card-shadow` | `shadow-sm` |
| `--card-shadow-hover` | `shadow-md` |

---

## Community Card

### Default

- Gradient header area with a single-letter community avatar (Figtree Bold, 22px)
- Title row beneath the header
- Meta line: member count and daily post count (e.g., "3,240 members, 12 posts today")
- Description text
- Footer: avatar stack (mini chips showing member previews) + **Join** button (tinted style, sm size)

### Joined State

- Checkmark badge ("Joined") appears inline with the title
- Footer button changes from "Join" to **View** (secondary style)

### Compact / List View

- Horizontal row layout instead of vertical card
- Small community avatar (rounded square, ~36px)
- Title and meta text in a single content column
- Action button (Join or View) at the trailing edge, 32px height

---

## Post / Feed Card

- **Header**: User avatar (sm, 32px) + author name + community name + timestamp. Overflow menu (three-dot icon) at trailing edge.
- **Body**: Post text content. Optional image attachment area below the text.
- **Action bar**: Four actions in a row:
  - Like (heart icon + count)
  - Liked state (filled heart, accent color, "Liked" label)
  - Comment (speech bubble icon + reply count)
  - Share (share icon, pushed to trailing edge with `margin-left: auto`)

---

## Card States

| State | Behavior |
|---|---|
| **Hover** | Card lifts with `translateY(-2px)` and shadow increases to `shadow-md` |
| **Selected** | Border changes to `action-primary` color |
| **Disabled** | Opacity reduced to 40%, no interactions allowed |
