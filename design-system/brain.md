# social.plus Design System — Router

This file is the entry point for all social.plus visual design tasks. It tells you which files to load based on what you're creating.

Reference files live in the public `cruciate-hub/marketing-team` repo. Skills load them via the canonical fetch block at the top of each SKILL.md, which shallow-clones the repo to `$MT_REPO` (default `/tmp/cruciate-hub-marketing-team`). Paths in this file are relative to the design-system folder — for example `colors-palette.md` is at `$MT_REPO/design-system/colors-palette.md`.

## How to use this file

1. You loaded this file first. Good.
2. Also load the main brain if you haven't already: `cat "$MT_REPO/brain.md"` — it has cross-domain routing, precedence rules, and the compliance check you must run before delivering.
3. Read the user's request.
4. Match it against the routing table below.
5. Read the listed files with `cat "$MT_REPO/design-system/<file>"`.
6. Apply everything you load. Design tokens are non-negotiable.
7. **If the output includes any text content** (headings, labels, descriptions, CTAs), you also need the messaging router: `cat "$MT_REPO/messaging/brain.md"` — follow its instructions to load terminology and tone files. Visual output without correct brand language is incomplete.

## Routing table

### Any visual task (always load these)
- `colors-palette.md` — Brand colours, supporting colours, neutrals, state colours, text colours, borders.
- `colors-usage.md` — Gradients, flat gradient pairs, usage principles, Webflow CSS variables. Load both — together they are the full colour system. This is law.
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

### Design review or audit (checking existing designs against the system)
- Load ALL files. Compare the design under review against every guideline.

## Rules

- **Design tokens are law.** Use the exact values from these files. Never approximate colours, spacing, or border-radius.
- **Dark-first.** `#111111` is the default background. Design on dark unless a specific light context is needed.
- **Ultramarine leads.** When you need one brand colour, reach for `#3B41EC`.
- **No gradient text.** `background-clip: text` is forbidden. Text is always a solid colour.
- **One primary button per section.** Never stack two gradient CTAs.
- **12px minimum.** No UI text below 12px. Ever.
- **Use `var()` for CSS.** When writing CSS for the website, always use Webflow CSS variables. Hex codes for non-CSS contexts only.
- **If a load fails** (clone error, missing file, or wrong format), follow the canonical fetch block's hard-fail rule — do not proceed with stale or memorized tokens.
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
