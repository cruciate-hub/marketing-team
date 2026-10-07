# Design System

Claude skill for the social.plus design system reference: the live website's tokens, the foundations (colors, typography, spacing, buttons, cards, rich text, form inputs, tags, accordions, dividers, imagery, logo, icons, accessibility, shadows and radius) and the 41 section types with page recipes.

This is the generic design-system skill — it routes to the appropriate design files based on the task at hand. The source of truth lives on GitHub and is fetched fresh every time, never memorized.

## What it does

- Fetches `brain.md` for cross-domain routing, precedence rules, and the compliance check.
- Fetches `design-system/brain.md` (the design-system router) and follows its instructions to load the specific files the task needs: `tokens.css` and the foundations for any visual output; `sections/README.md`, the recipes and the sections for website pages.
- Optionally fetches `messaging/brain.md` when the output includes text content (headings, labels, CTAs, descriptions).
- Runs the main brain's compliance check before delivering.

## When it triggers

For any output where visual accuracy matters — writing CSS, styling components, building Webflow elements, creating HTML mockups, designing visual layouts. Also for quick reference questions about brand colors, color palette, button states, dark mode colors, design tokens, spacing, border radius, typography, or layout.

Trigger even for small questions like "what blue do we use" or "what's the hover color for buttons" (`--social--button-hover` `#272B9D`, from `tokens.css`).

The skill is not for written content only — use `brand-messaging` for copy without visual output.

## Workflow

1. Fetch `brain.md` — cross-domain routing, precedence rules, compliance check.
2. Fetch `design-system/brain.md` — the design-system router — and follow its task-specific instructions.
3. If the output includes any text content, also fetch `messaging/brain.md`.
4. Run the main brain's compliance check before delivering.

## Why this skill is thin

`design-system` is intentionally minimal — a dispatcher, not a content producer. The heavy lifting lives in the routing layer (`design-system/brain.md`), the tokens (`tokens.css`), the foundations (`foundations/<name>/foundation.md` with a `preview.html`) and the section set (`sections/`). Keeping the skill shell small means a re-run of the capture flows through without needing to rewrite this skill.

For format-heavy tasks (emails with specific MailerLite requirements), a dedicated skill loads format-specific design files directly — which is why `newsletters` fetches `tokens.css` and the colors and accessibility foundations itself rather than going through this router.

**One structure.** `design-system/` is built from the live website (captured 7 October 2026): `tokens.css` (the 44 live Webflow variables), `foundations/` (values as measured, rules, known inconsistencies, a preview per foundation) and `sections/` (41 section types with recipes and the rule for building pages). There is no second token layer any more; the former generic design system and app UI kit files were removed in 13.54. `design-system/README.md` explains the structure and how to update it.

## Files

```
design-system/
└── SKILL.md                          Skill entry point — minimal, routes to GitHub files
```

No `references/` subdirectory — the tokens, foundations and sections live in the repo root's `design-system/` folder and are fetched at runtime.

## URL format

All reference files are loaded from a shallow clone of this repo (`git clone --depth 1`) into `$MT_REPO`. The canonical fetch block at the top of each SKILL.md handles the clone; skills then read files with `cat "$MT_REPO/<path>"`. This applies to `brain.md` and every file it routes to.
