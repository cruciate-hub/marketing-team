# Claude design/code → Webflow

Claude skill for turning a Claude-generated design or prototype (claude.ai/design HTML/CSS/JS, a Claude Code artifact, or pasted markup) into a live Webflow build via the Webflow MCP — and for iterating on Claude-built Webflow sections.

This is the engineering-side counterpart to `design-system` and `site-intelligence`: where those describe *what* the brand and site look like, this skill prescribes *how* to translate a Claude-drafted UI into Webflow's Style records, components, embeds, and custom code without leaving cascade conflicts behind.

## Structure (token-efficient, progressive disclosure)

The skill loads a lean `SKILL.md` on invocation and pulls depth from `references/` only when needed:

- **`SKILL.md`** — core: native-vs-code decision rule, the headless-vs-Designer tool stack, `data_whtml_builder` as the fast build path, breakpoints, responsive/component patterns, custom-code-via-API, a one-line gotcha index, a token-efficiency section, the staging verification loop, and the build/publish playbook.
- **`references/pitfalls.md`** — the full catalog: 9 input anti-patterns (A1–A9) + 21 migration pitfalls with symptom / cause / fix.
- **`references/worked-examples.md`** — real before/after diffs (section split, descendant trim, JS-injection strip, transform-cascade fix, plus the 2026-07 responsive-nav: making one component work on mobile and connecting a bar to the navbar as one card).
- **`references/variable-ids.md`** — social.plus site identity + pre-mapped brand variable IDs, so `data_style_tool` calls can pass `variable_as_value` without a `query_variables` round-trip.

## What it does

- **Decision rule** for whether a CSS rule belongs natively (a Webflow Style record) or in custom code — the wrong choice silently overwrites Style-panel edits because custom code loads *after* Webflow's compiled CSS.
- **Fast build path:** `data_whtml_builder` imports a whole section from `html` + `css` in one call (auto-mapped to classes + breakpoints), instead of a token-heavy element-by-element rebuild.
- **Corrected architecture:** the Data API tools (`data_*`) are **headless** — no active Designer tab needed for style/element/embed/code/publish work; only Designer-bridge tools require the focused tab.
- **Custom code is now API read/write** (this reverses the skill's old paste-by-hand advice): Site/Page freeform head+footer via `data_scripts_tool`, and `<style>`/`<script>` HTML embeds via `data_element_settings_tool` (`code` setting).
- **Responsive & components:** native breakpoint styles (main/medium/small/tiny), making one component responsive instead of shipping mobile-duplicates, shared-class blast radius, component variants, and the reality that bulk component-instance deletion only exists as the Designer's "Delete Component".
- **Anti-pattern catalog + pitfalls** (A1–A9 + 21) including cascade-order conflicts, orphan style records, invisible JS-injected DOM, `color-mix()` corruption (and the variable-`custom_value` workaround), breakpoint mismatch, brittle combo cascades, containing-block traps, `body{overflow-x:hidden}` breaking sticky, Chromium-vs-Safari blind spots, and publish propagation lag.
- **Token-efficiency workflow** — one `data_whtml_builder` per section, page ID from the live DOM, jq/grep on persisted large tool results, narrow `query_styles`, verify via computed styles / `element_snapshot_tool` instead of screenshots, batched writes.
- **Staging verification loop** — publish to `.webflow.io`, wait out CDN propagation, assert computed styles + console-clean across real scenarios, screenshot last; production only on explicit go-ahead.

## When it triggers

- Migrating a Claude-generated HTML/CSS/JS prototype to a native Webflow section, or iterating on one.
- Making a section or component responsive across Webflow breakpoints.
- Editing CSS/JS embeds or Site/Page head/footer code through the API.
- Working with shared classes, component instances, or variants; deleting redundant components.
- The user asks why a Style-panel change isn't taking effect (almost always a cascade-order or embed-vs-native issue).
- Choosing between Webflow's breakpoints (992/768/480) and a prototype's custom `@media` values.
- Hitting a Webflow gotcha: `color-mix()` corruption, containing-block traps, sticky/overflow conflicts, publish propagation lag, Chromium-vs-Safari differences.

## When it does NOT trigger

- Pure Webflow-only work with no Claude prototype as input — use the appropriate `webflow-skills:*` skill.
- Pure Claude-artifact iteration with no Webflow target.
- Content writing (blog, brand, AEO, case study) — those go to the content-creation skills.
- Routine CMS edits or publish operations — `webflow-skills:safe-publish`, `webflow-skills:bulk-cms-update`, etc.

## Skill location

- [`marketing-team/skills/claude-design-to-webflow/SKILL.md`](../marketing-team/skills/claude-design-to-webflow/SKILL.md)

## Related skills

- `design-system` — visual design tokens (colors, typography, spacing); the source of truth for which variables to bind.
- `site-intelligence` — what content lives on the site; useful when the migration target is an existing page.
- `webflow-skills:custom-code-management` — site-level Head/Footer scripts.
- `webflow-skills:safe-publish` — the publish step at the end of the playbook.
