# Design System

Claude skill for the social.plus design system reference — colors, typography, spacing, buttons, inputs, layout, shadows, icons, imagery, accessibility, and logo usage.

This is the generic design-system skill — it routes to the appropriate design files based on the task at hand. The source of truth lives on GitHub and is fetched fresh every time, never memorized.

## What it does

- Fetches `brain.md` for cross-domain routing, precedence rules, and the compliance check.
- Fetches `design-system/brain.md` (the design-system router) and follows its instructions to load the specific files the task needs.
- Optionally fetches `messaging/brain.md` when the output includes text content (headings, labels, CTAs, descriptions).
- Runs the main brain's compliance check before delivering.

## When it triggers

For any output where visual accuracy matters — writing CSS, styling components, building Webflow elements, creating HTML mockups, designing visual layouts. Also for quick reference questions about brand colors, color palette, button states, dark mode colors, design tokens, spacing, border radius, typography, or layout.

Trigger even for small questions like "what blue do we use" or "what's the hover color for buttons".

The skill is not for written content only — use `brand-messaging` for copy without visual output.

## Workflow

1. Fetch `brain.md` — cross-domain routing, precedence rules, compliance check.
2. Fetch `design-system/brain.md` — the design-system router — and follow its task-specific instructions.
3. If the output includes any text content, also fetch `messaging/brain.md`.
4. Run the main brain's compliance check before delivering.

## Why this skill is thin

`design-system` is intentionally minimal — a dispatcher, not a content producer. The heavy lifting lives in the routing layer (`design-system/brain.md`) and the individual token files (colors, typography, spacing, buttons, etc.). Keeping the skill shell small means token updates flow through without needing to rewrite this skill.

For format-heavy tasks (emails with specific MailerLite requirements), a dedicated skill loads format-specific design files directly — which is why `newsletters` fetches `colors-palette.md` and `colors-usage.md` itself rather than going through this router.

## Files

```
design-system/
├── SKILL.md                          Skill entry point — minimal, routes to GitHub files
└── README.md                         This file
```

No `references/` subdirectory — all design tokens live in the repo root's `design-system/` folder and are fetched at runtime.

## URL format

Always fetch via `github.com/.../blob/...` URLs. Never use `raw.githubusercontent.com` — blocked by network egress. This applies to `brain.md` and every file it routes to.
