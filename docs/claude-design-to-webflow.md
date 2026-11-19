# Claude Design → Webflow

The skill that builds social.plus website pages and sections in Webflow (through the Webflow MCP) from Claude Design canvas boards, Claude artifacts or pasted HTML/CSS, and checks the result against the board on staging.

Restructured on 19 Nov 2026 after the pricing build needed 43 corrections, most of them covered by rules the old 50 KB skill already had. The plan and its reasons: [`claude-design-to-webflow-rework.md`](claude-design-to-webflow-rework.md).

## How it works

- **Principles:** Webflow is king (the site's components, class chains and variables win over the board); reuse first; measured, not eyeballed; "publish" means staging; style embeds sit next to what they style; every place Webflow wins is raised so the board and the design system can follow.
- **Five gates**, in order: Brief (fresh board read, target page), Map (each board section to a Webflow component and its class chain, plus a roles file), Build, Check (`scripts/check-board.mjs` at 1440/800/390), Publish and record.
- **The check script** compares the board and staging per role (sizes, type, spacing), checks frame lines per section, horizontal scroll, accessibility (axe, WCAG A/AA), internal links and whether new CSS is live, and writes a report with side-by-side images. `selftest.mjs` proves it catches deliberate breakage.

## Files

- [`SKILL.md`](../marketing-team/skills/claude-design-to-webflow/SKILL.md): principles, gates, report format, pitfalls by topic.
- `references/site-conventions.md`: social.plus Webflow rules (components, links, SVGs, framed grids, variables, class system, embeds), breakpoints, responsive, the detailed checklist.
- `references/api-and-code.md`: tool stack, whtml, custom code, assets and fonts, staging verification, publishing.
- `references/check-board.md`: the check script, roles files and the manual fallback.
- `references/subagent-brief.md`: brief template that carries the gates.
- `references/pitfalls.md`: 135 numbered pitfalls (numbers never change) and a one-line index.
- `references/worked-examples.md`, `references/variable-ids.md`.
- `scripts/`: `check-board.mjs`, `selftest.mjs`, `examples/pricing.roles.json` (`npm install` once).

## When it does not trigger

- CMS content (`webflow-publisher`), blog posts (`blog-publisher`), website copy (`brand-messaging`).
- Pure Webflow work with no design input: Webflow's own skills (`webflow-mcp:*`) where installed.
- Page designs from Figma: they go back into Claude Design first. Figma stays fine for images.

## Related skills

- `design-system`: tokens, foundations and the section library (`design-system/sections/**/section.md`, whose Webflow notes feed the Map gate).
- `site-intelligence`: what the live site says.
- Webflow's `accessibility-audit` and `safe-publish`: optional extras; this skill's publish rule wins.
