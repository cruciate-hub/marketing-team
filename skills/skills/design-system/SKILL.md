---
name: design-system
description: >
  Reference for the social.plus design system — colors, typography, spacing, buttons,
  inputs, layout, shadows, icons, imagery, accessibility, and logo usage.
  Use this skill for: writing CSS, styling components, building Webflow elements,
  creating HTML mockups, designing visual layouts, or any output where visual accuracy
  matters for social.plus. Also trigger when someone asks about brand colors, the
  color palette, button states, dark mode colors, design tokens, spacing, border
  radius, typography, or layout. Trigger even for quick questions like "what blue
  do we use" or "what's the hover color for buttons."
  Do NOT trigger for written content only (use brand-messaging skill) — this skill
  is for visual output and design token reference.
---

# social.plus Design System

This skill provides the full social.plus design system reference. The source of truth lives on GitHub and must be fetched fresh every time.

## How to fetch reference files

<!-- FETCH-BLOCK:START v1 -->
Fetch reference files ONLY with `curl` from `raw.githubusercontent.com`, using these exact flags:

    curl -fsSL --max-time 30 --connect-timeout 10 --retry 2 --retry-delay 1 \
      https://raw.githubusercontent.com/cruciate-hub/marketing-team/main/<path>

The repo is public — no authentication required. When fetching multiple files in one step, run the curl commands in parallel (single Bash message, multiple commands) — do not serialise.

Validate every response before using it:
- Markdown files must start with `#` (a leading heading line)
- JSON files must start with `{` or `[`
- HTML files must start with `<`
- Content must be non-empty

If any fetch fails (non-zero exit, empty output, or content that fails the above check):
- Do NOT reconstruct the file from memory or training data.
- Do NOT fall back to WebFetch or any other tool.
- Stop immediately and respond with exactly this line:

  `Fetch failed: <path>. Please check your network connection and rerun.`
<!-- FETCH-BLOCK:END v1 -->

## What to do

1. Fetch `brain.md` for cross-domain routing, precedence rules, and the compliance check.

2. Fetch `design-system/brain.md` (the design system router).

3. Follow the design system router's instructions — it tells you which additional files to fetch based on the user's task.

4. If the output includes any text content (headings, labels, CTAs, descriptions), also fetch `messaging/brain.md`.

5. Before delivering, run the compliance check from the main brain.
