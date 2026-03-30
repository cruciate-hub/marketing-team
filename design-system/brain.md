# social.plus Design System — Router

This file is the entry point for all social.plus visual design tasks. It tells you which files to fetch based on what you're creating.

All files are hosted at:
`https://github.com/socialplus-tools/marketing-team/blob/main/design-system/`

**Warning:** Always use `github.com/.../blob/...` URLs when fetching. Never convert to `raw.githubusercontent.com` or `api.github.com` — both are blocked by network egress restrictions and will fail.

## How to use this file

1. You fetched this file first. Good.
2. Also fetch the main brain if you haven't already: `https://github.com/socialplus-tools/marketing-team/blob/main/brain.md` — it has cross-domain routing, precedence rules, and the compliance check you must run before delivering.
3. Read the user's request.
4. Match it against the routing table below.
5. Fetch the listed files using WebFetch on the GitHub blob URLs above.
6. Apply everything you fetch. Design tokens are non-negotiable.
7. **If the output includes any text content** (headings, labels, descriptions, CTAs), you also need the messaging router: `https://github.com/socialplus-tools/marketing-team/blob/main/messaging/brain.md` — follow its instructions to fetch terminology and tone files. Visual output without correct brand language is incomplete.

## Routing table

### Any visual task (always fetch these)
- `colors-palette.md` — Brand colours, supporting colours, neutrals, state colours, text colours, borders.
- `colors-usage.md` — Gradients, flat gradient pairs, usage principles, Webflow CSS variables. Fetch both — together they are the full colour system. This is law.
- `typography.md` — Figtree type scale, weights, minimum sizes, line heights.

### Visual output with layout (HTML pages, decks, documents, multi-section designs)
- `spacing.md` — 12-token spacing scale (4pt/8pt hybrid grid).
- `border-radius.md` — 7-token radius scale with component defaults.
- `shadows.md` — 5 elevation levels + 7 per-colour brand glows.
- `layout.md` — Breakpoints, containers, 12-column grid, vertical rhythm.

### Interactive or web output (HTML, components, forms, Webflow elements)
- `buttons.md` — 4 variants × 3 sizes, all states, CSS tokens.
- `inputs.md` — 6 form component types, all states, focus rings.
- `accessibility.md` — WCAG 2.1 AA, contrast ratios, focus states, ARIA patterns, motion.

### Output containing icons
- `iconography.md` — Material Symbols Outlined, sizes, weights, colour rules.

### Output containing images or illustrations
- `imagery.md` — Illustration style, photography treatment, decorative rules.

### Output containing or referencing the logo
- `logo.md` — SVG data, variants, clearspace, background rules, do/don'ts.

### Social media content
- `social-posts.md` — LinkedIn, Instagram, Twitter/X format specs and copy guidelines.

### Design review or audit (checking existing designs against the system)
- Fetch ALL files. Compare the design under review against every guideline.

## Rules

- **Design tokens are law.** Use the exact values from these files. Never approximate colours, spacing, or border-radius.
- **Dark-first.** `#111111` is the default background. Design on dark unless a specific light context is needed.
- **Ultramarine leads.** When you need one brand colour, reach for `#3B41EC`.
- **No gradient text.** `background-clip: text` is forbidden. Text is always a solid colour.
- **One primary button per section.** Never stack two gradient CTAs.
- **12px minimum.** No UI text below 12px. Ever.
- **Use `var()` for CSS.** When writing CSS for the website, always use Webflow CSS variables. Hex codes for non-CSS contexts only.
- **If a fetch fails**, tell the user the GitHub content is unavailable and you cannot guarantee brand alignment. Do not proceed with stale or memorized tokens.
- **Run the compliance check** from `brain.md` (the main brain) before delivering your output.

## Available files

| File | Contains |
|---|---|
| `colors-palette.md` | Brand colours, supporting colours, neutrals, state colours, text colours, borders |
| `colors-usage.md` | Gradients, flat gradient pairs, usage principles, Webflow CSS variables |
| `typography.md` | Figtree type scale, weights, line heights, email/social typography |
| `spacing.md` | 12-token spacing scale, component/section/page spacing guide |
| `border-radius.md` | 7-token radius scale, component defaults |
| `buttons.md` | 4 variants, 3 sizes, all states, icon buttons, CSS tokens |
| `shadows.md` | 5 elevation levels, 7 brand glow variants, CSS custom properties |
| `layout.md` | Breakpoints, containers, 12-col grid, vertical rhythm |
| `iconography.md` | Material Symbols Outlined, sizes, weights, variable axes |
| `inputs.md` | 6 form types, all states, focus rings, accessibility |
| `imagery.md` | Illustration style, photography, decorative rules |
| `accessibility.md` | WCAG 2.1 AA, contrast, focus, ARIA, motion, checklist |
| `logo.md` | SVG paths, variants, clearspace, usage rules, do/don'ts |
| `social-posts.md` | Platform specs, copy structure, visual guidelines |
