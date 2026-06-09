# Claude-design → Webflow

Claude skill for migrating a Claude-generated HTML/CSS/JS prototype to a native Webflow section via the Webflow MCP.

This is the engineering-side counterpart to `design-system` and `site-intelligence`: where those describe *what* the brand and site look like, this skill prescribes *how* to translate a Claude-drafted UI into Webflow's Designer + Style Records without leaving cascade conflicts behind.

## What it does

Captures the lessons from the social.plus MCP Server page rebuild (2026-05) plus community patterns adapted from public Webflow-conversion skills (sans the moden.club paste-tool path — this skill targets the official `mcp.webflow.com` Connector). Specifically:

- **Decision rule** for whether a CSS rule belongs natively (Webflow Style record) or stays in custom Site/Page head code — the wrong choice silently overwrites Style-panel edits because Site Settings → Head loads *after* Webflow's compiled CSS.
- **Anti-pattern catalog** (9 entries, A1–A9): section-root mega-rules, `all: unset`, hardcoded brand-color hex, custom @media breakpoints (1200/720/520), JS-injected static content, `:nth-child(N)`, `color-mix()` Designer corruption, class-fixer IIFEs, mobile horizontal overflow.
- **Pitfalls** (14 entries) with symptom / cause / fix triples, including: cascade-order conflicts, orphan native records (no element uses the class), invisible JS-injected elements, `color-mix()` `pxpxpxpx black` corruption, custom-breakpoint mismatch, brittle combo-class cascades, `Webflow.push()` runtime timing, and `inDesigner` canvas-vs-published render differences.
- **Pre-flight checklist** — 6 steps to run before touching anything (backup head/footer locally, inventory variables, inventory native styles, verify class usage, map breakpoint strategy, identify JS-injected static content).
- **Migration playbook** — 6-step process from categorising rules through publishing to `.webflow.io`.
- **Worked examples** — 4 real before/after diffs from the social.plus session (section split, descendant trim, JS-injection strip, transform-cascade fix).
- **Webflow MCP cheatsheet** — one-line API calls for the common operations.
- **Pre-mapped variable IDs** — 31 brand colors + 1 font + 7 size variables with their Webflow IDs and site identity fields, so calls to `style_tool update_style` can use `variable_as_value` without a prior `query_variables` round-trip.

## When it triggers

- Migrating a Claude-generated HTML/CSS/JS prototype to a native Webflow section.
- Iterating on a previously-Claude-built Webflow section and the user mentions code-vs-native cleanup, JS-injection removal, or cascade conflicts.
- The user pastes Webflow head or footer code and asks what should move to native.
- The user asks why a Style-panel change isn't taking effect (almost always a cascade-order issue).
- The user is choosing between Webflow's standard breakpoints (992/768/480) and custom `@media` values from the prototype.
- The user hits the `color-mix()` `pxpxpx black` Designer corruption.
- The user runs into Webflow MCP query timeouts and the Designer Bridge tab being idle.

## When it does NOT trigger

- Pure Webflow-only work with no Claude prototype as input — use the appropriate `webflow-skills:*` skill instead.
- Pure Claude artifact iteration without a Webflow target — the skill assumes a Webflow MCP destination.
- Content writing (blog, brand, AEO, case study) — those go to the content-creation skills.
- Routine CMS edits or publish operations — those go to `webflow-skills:safe-publish`, `webflow-skills:bulk-cms-update`, etc.

## Skill location

- [`marketing-team/skills/claude-design-to-webflow/SKILL.md`](../marketing-team/skills/claude-design-to-webflow/SKILL.md)

## Related skills

- `design-system` — visual design tokens (colors, typography, spacing). Used as the source-of-truth reference for which variables to bind to.
- `site-intelligence` — what content lives on the site. Useful when the migration target is an existing page.
- `webflow-skills:custom-code-management` (official Webflow plugin) — managing site-level Head/Footer scripts.
- `webflow-skills:safe-publish` (official Webflow plugin) — the publish step at the end of the playbook.
