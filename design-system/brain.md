# social.plus Design System Router

Source: canonical design system HTML

This file is the entry point for all social.plus visual design tasks. It tells you which files to load based on what you're creating.

Reference files live in the public `cruciate-hub/marketing-team` repo. Skills load them via the canonical fetch block at the top of each SKILL.md, which shallow-clones the repo to `$MT_REPO` (default `/tmp/cruciate-hub-marketing-team`). Paths in this file are relative to the design-system folder.

## How to use this file

1. You loaded this file first. Good.
2. Also load the main brain if you haven't already: `cat "$MT_REPO/brain.md"` for cross-domain routing, precedence rules, and the compliance check.
3. Read the user's request.
4. Match it against the routing table below.
5. Read the listed files with `cat "$MT_REPO/design-system/<file>"`.
6. Apply everything you load. Design tokens are non-negotiable.
7. **If the output includes any text content** (headings, labels, descriptions, CTAs), you also need the messaging router: `cat "$MT_REPO/messaging/brain.md"`.

## Routing table

### Any visual task (always load these)
- `colors-palette.md` - Primitive colour tokens: Ultramarine, Slate, Picton Blue, accents, status.
- `colors-usage.md` - Semantic tokens (light + dark mode), 11 named gradients, usage principles.
- `typography.md` - Figtree typeface, 9-step type scale, 5 weights, heading scale, line heights.

### Visual output with layout
- `spacing.md` - 11-token 4px-base spacing scale with usage annotations.
- `border-radius.md` - 9-token radius scale with component context.
- `shadows.md` - Shadow scale, background layering (light + dark), z-index (8 layers).
- `layout.md` - Motion system (durations, easing curves), z-index cross-reference.

### Interactive or web output
- `buttons.md` - 6 variants, 5 sizes, all states, icon buttons, component tokens.
- `inputs.md` - Text inputs, textarea, search bar, toggles, checkboxes, radios, chips.
- `accessibility.md` - WCAG AA contrast, action-accent auto-switch, touch targets, reduced motion, focus rings.

### Components
- `avatars.md` - 5 sizes, 6 states/decorators, avatar stacks, community avatars.
- `badges-tags.md` - Notification badges, status badges, tags (filled, outlined, with icon, dismissible).
- `cards.md` - Community cards, post/feed cards, compact/list view, card states.
- `list-items.md` - List item anatomy, 8 variants, grouped section lists.
- `navigation.md` - App bar variants, bottom tab bar, tab states.
- `overlays.md` - Bottom sheets, modals, context menus, tooltips.
- `feedback.md` - Toasts, progress indicators, skeleton loaders.

### Patterns
- `states.md` - Component x state matrix (6 components, 8 states), screen-level states.
- `empty-states.md` - Full-page empty states (6 screens), inline empty state variant.

### Output containing icons
- `iconography.md` - Material Symbols Outlined, variable axes, sizes, colour rules.

### Output containing images or illustrations
- `imagery.md` - Illustration style, photography treatment, decorative rules.

### Output containing or referencing the logo
- `logo.md` - SVG data, variants, clearspace, background rules, do/don'ts.

### Design review or audit
- Load ALL files. Compare the design under review against every guideline.

## Rules

- **Design tokens are law.** Use the exact values from these files. Never approximate colours, spacing, or border-radius.
- **Dark-first.** `#111111` is the default background. Design on dark unless a specific light context is needed.
- **Ultramarine leads.** When you need one brand colour, reach for `#3B41EC` (as background fill). For text/icons on dark, use `#7B94FE` (action-accent).
- **No gradient text.** `background-clip: text` is forbidden. Text is always a solid colour.
- **One primary button per section.** Never stack two primary CTAs.
- **12px minimum.** No UI text below 12px. Ever.
- **44px touch targets.** All interactive elements hit 44px minimum.
- **If a load fails** (clone error, missing file, or wrong format), follow the canonical fetch block's hard-fail rule. Do not proceed with stale or memorized tokens.
- **Run the compliance check** from `brain.md` (the main brain) before delivering your output.

## Available files

| File | Contains |
|---|---|
| `colors-palette.md` | Primitive colour tokens: Ultramarine, Slate, Picton Blue, accents, status |
| `colors-usage.md` | Semantic tokens (light + dark), gradients, usage principles |
| `typography.md` | Figtree type scale, weights, heading scale, line heights |
| `spacing.md` | 11-token 4px-base spacing scale |
| `border-radius.md` | 9-token radius scale with component context |
| `shadows.md` | Shadow scale, background layering, z-index |
| `layout.md` | Motion system, durations, easing curves |
| `buttons.md` | 6 variants, 5 sizes, all states, icon buttons |
| `inputs.md` | Text inputs, textarea, search, toggles, checkboxes, radios, chips |
| `avatars.md` | 5 sizes, states, stacks, community avatars |
| `badges-tags.md` | Notification badges, status badges, tags |
| `cards.md` | Community cards, post cards, card states |
| `list-items.md` | List item anatomy, variants, grouped sections |
| `navigation.md` | App bar, bottom tab bar, tab states |
| `overlays.md` | Bottom sheets, modals, context menus, tooltips |
| `feedback.md` | Toasts, progress indicators, skeleton loaders |
| `states.md` | Component x state matrix, screen-level states |
| `empty-states.md` | Full-page and inline empty states |
| `accessibility.md` | WCAG AA, contrast, touch targets, reduced motion, focus, ARIA |
| `iconography.md` | Material Symbols Outlined, sizes, weights, colour rules |
| `imagery.md` | Illustration style, photography, decorative rules |
| `logo.md` | SVG paths, variants, clearspace, usage rules |
