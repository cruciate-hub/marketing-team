# Plan: rework the `claude-design-to-webflow` skill

Status: executed 19 Nov 2026 (marketing-team 13.91, web-dev kit 1.9.0). Deviations: the Claude Design card notes are re-synced after merge (design-system/claude-design/SYNC.md re-syncs the page from merged GitHub only); `tool-names` lives in `references/api-and-code.md`. Original draft v2 below.

## Why

The pricing build (19 Nov 2026) needed 43 corrections. The top causes were:
- an old or assumed board (8);
- no real check against the board (7);
- wrong class chains (6);
- process slips (6);
- invented styles (5);
- rebuilding something that already existed (4).

About 40% happened in subagent builds. Most of these mistakes were already covered by written rules: pitfalls 64, 70, 86 and 88, feedback 31, and SKILL rule 1. The skill is 50 KB in 154 lines, and the 134 pitfalls are too much to find and follow. The goal is a shorter skill with a check that ships with it, not more rules.

## Principles (decided)

1. **Webflow is king.** Webflow tokens, gutters, type scale, class chains and components are the source of truth. The board adapts to Webflow, never the reverse.
2. **Reuse first.** Existing component, then existing class chain, then a new native class (with Stefan's OK), then code last.
3. **Measured, not eyeballed.** A check script ships with the skill. "Done" requires its output in the report.
4. **"Publish" means staging (`.webflow.io`).** Production only when Stefan says "publish to the real website", with a warning first that it also pushes every other unpublished change on the site (decided 19 Nov 2026).
5. **Style embeds sit next to what they style.** For CSS states Webflow can't style natively (`:has()`, checked, keyframes), use a small `<style>` HtmlEmbed placed inside or right beside the section or element it applies to, scoped to that section's classes. Several small embeds are fine; one general embed for the whole page is not, and never page head code. Never for layout a native class can do. Each embed is listed in the report with what it styles. Pitfall 15 (the Designer canvas doesn't show embed CSS) is accepted for these states (Stefan, 19 Nov 2026).
6. **Raise every drift.** Whenever Webflow wins over the board (a gutter, type scale, component or class chain that differs), the build raises it and asks Stefan for OK to update the Claude Design board artifact(s) and the Claude Design system (`design-system/`, card notes) to match Webflow. Never silently, never the reverse. Drifts are tracked in a "Webflow won" list in the report (Stefan, 19 Nov 2026).
7. **Complement the native Webflow skills** (`webflow-mcp:accessibility-audit`, `webflow-mcp:safe-publish`) as optional extras. Our publish rule wins.

## Open decisions for Stefan

1. ~~Pitfall 86 versus "Webflow is king"~~: **decided 19 Nov 2026**, rewrite 86 (step 5).
2. ~~Framed `section.md` approval~~: **decided 19 Nov 2026**, no approval needed. Only the text notes change (Webflow status, component, class chain); `source.html`, `styles.css`, `framed.css` and the card previews stay untouched, so nothing looks different. Amadeus is mentioned in the PR.

## What stays the same

- **Pitfall numbers.** They are referenced across the repo, `design-system/feedback.md` and memory files. New pitfalls get new numbers; nothing is renumbered.
- The `variable-ids.md` and `worked-examples.md` content, and the framed rules.
- The skill name, and its place in the web-dev kit.

## Steps (in this order)

### 1. Teammate uploads first
Run the org-upload check (`skill-distribution/RUNBOOK.md`, `org-merge.py`) and merge teammate changes before editing. This skill is in `DESC_OVERRIDDEN` (`org-merge.py`), so a description change by a teammate shows as a conflict.

### 2. Build the check script inside the skill
Location: `skills/claude-design-to-webflow/scripts/check-board.mjs` (ES module), so it ships in the kit.
- **Setup:** relative paths only. Playwright is a declared dependency with a one-line install in the skill. It uses the system Chrome if found, otherwise Playwright's Chromium. It writes to an output folder passed as an argument.
- **Fallback:** if the script can't run, the skill says how to do the same checks by hand (board read, screenshots at 3 widths, a 1:1 crop of every frame line) and the report says so.
- **Inputs:** the board `.dc.html`, the staging URL, and a small role map per page (board selector → staging selector for each section and its key elements, as in `compare-board-pricing.js`). The role map is written during the Map step.
- **Section matching:** ordered `<section>` matching plus the role map. Not heading text: sections without headings, such as the logo wall, would be skipped.
- **Checks at 1440, 800 and 390:**
  - section and element sizes and positions, plus font size, weight and padding for each mapped role;
  - frame lines and + markers (pixel scan, from `compare-board-lines.py`);
  - horizontal scroll;
  - "new CSS is live", from a list of new classes or rules given as an input;
  - axe-core accessibility (WCAG AA, including contrast), plus our extras: one `<main>`, decorative SVGs with `aria-hidden` and `focusable`, icon-only links with an aria-label, duplicate ids;
  - internal links return 200 (external links are reported, never failed).
- **Output:** PASS / FAIL / NOTE per check, plus side-by-side images. Known Webflow-owned differences, such as the gutter, are NOTE.
- **Tests:** pass on `/pricing-conversational` against `Pricing.dc.html`, and fail on a deliberately broken case (a removed frame line, a missing section, a wrong font size). A check that can't fail isn't a check.

### 3. Move table and the new reference files
Before cutting anything from SKILL.md, write a table in the PR mapping each current SKILL.md section to its new home. Nothing is dropped without a destination.
- `references/site-conventions.md`: current rules 1–8 (components, links, SVGs, framed grids, variables, class system, embeds, gate 8), native vs code, breakpoints, responsive and components.
- `references/api-and-code.md`: the tool stack (current Webflow MCP tools and actions, `agent_id`/`session_id`, headless vs Designer, publish limit and 429s), whtml quirks, custom code (freeform, embeds, the 2000-character script limit, no app-registered scripts), assets and fonts, third-party embeds, publish settings (`publishToWebflowSubdomain:true, customDomains:[]`).
- `references/subagent-brief.md`: a template with the five gates, the report format and "no done without check output".
- Keep: `pitfalls.md`, `worked-examples.md`, `variable-ids.md`.

### 4. Rewrite `SKILL.md`
Budget: at most 12 KB (now 50 KB). Contents:
- **Principles** (above).
- **Five steps, each with a gate of 3–4 items:**
  - **Brief:** confirm the target page and that it's staging; read the board fresh (version id in the report); list its sections.
  - **Map:** for each board section, name the Webflow component or existing section and its exact class chain (from the section notes, then `query_components`); write the role map for the check. Make no new classes without OK. Never swap in a nearby site section.
  - **Build:** whtml for structure only; styles via `data_style_tool` with variables; the full framed chain; component instances; preview the blast radius before editing shared classes or components; snapshot before changes.
  - **Check:** run `check-board.mjs` and attach its output. No FAIL left, and every NOTE explained.
  - **Publish and sync:**
    - check for unpublished site changes first (compare lastUpdated with lastPublished);
    - publish to staging and confirm it landed;
    - write a rollback note;
    - list every "Webflow won" drift and ask for OK to update the board artifact(s) and the Claude Design system; after OK, update both and re-publish the canvas.
- **Report format:** gate results with the check output, any embed or new class and why, and what wasn't verified.
- **Record:** lessons go to a new pitfall number, `design-system/feedback.md` and the vault.
- **Topic index of the pitfalls**, numbers unchanged:
  - board and design source;
  - components and classes;
  - framed sections;
  - whtml and tool quirks;
  - CSS traps;
  - custom code;
  - CMS;
  - checking;
  - publishing.

### 5. Resolve contradictions explicitly
- **The embed rule:**
  - rule 7 (`SKILL.md:24`), gate 8 (`:25`), the visible element gate (`:34`) and the checklist (`:137`) become principle 5;
  - add a note to the `webflow-native-first` memory.
- **Pitfall 86, new text (decided):** "A framed component is built with Webflow's existing classes and variables. `framed.css` shows the intended look (layout, spacing, type); build that look from the site's components, class chains and variables. A value with no Webflow equivalent is raised as a drift (principle 6); a missing variable or class needs Stefan's OK and is never created on the fly." The About logo-wall example stays as the cautionary story; the instruction to create missing variables goes.
- **23 vs 66 on `rel`:** 74 is correct (no `rel`). Mark 23 "superseded by 74"; 66 points to 74.
- **The only duplicate merge:** 23 and 66 point to each other. The other four pairs I named (101/127, 64/131, 93/132, 86/124) are not duplicates and stay as they are.
- **Back-references:** fix pitfalls 64, 70, 71 and 88 (around lines 393, 413, 416 and 467), which cite "rule 6", "rule 4" and "Site conventions first". They now point to `site-conventions.md`.
- **Figma as a page-design source:** remove "or a Figma design via the Figma MCP" from the kit description (`build-kits.sh:169`) to match `SKILL.md:3` and `:14` (page designs come from Claude Design, never Figma-to-Webflow). Figma stays allowed for images (illustration skill, Figma AI photos) and for pitfall 61; that wording is untouched.
- **Dead links to webflow-skills:** remove them from `SKILL.md` (around lines 14, 51 and 150), `docs/claude-design-to-webflow.md` and `CLAUDE.md`. Locally the namespace is `webflow-mcp:`.

### 6. Section notes (checked 19 Nov 2026)
Current state: the 36 captured sections have a `## Webflow note` block. The 23 framed sections name their Webflow component ("Webflow name in the library: Section / Logo Wall") but all say "not yet in Webflow" and "write their values (none is a Webflow variable yet)". Git authorship is all Stefan's; the Owner field says Amadeus (design origin), approved by Stefan.
- **Framed (23):** replace "not yet in Webflow" with the real status, read-only from `query_components` (e.g. `Section / Logo Wall` exists and is used). Add a `## Webflow note` block in the same format as the captured ones: component, exact class chain, embeds, date checked. Replace "write their values" with "use Webflow's variables and classes".
- **Captured (36):** check each note against `query_components`, date-stamp class chains.
- **`sections/README.md:87`** ("Class names … are not a concern") and `framed/README.md` ("Not yet in Webflow"): update.
- **Claude Design card notes** mirror `section.md` (`capture/claude-design-check.py`, step 4), so every edit shows as DIFF until re-synced. Re-sync in the same PR, under the drift rule (principle 6).
- **Timing:** design-system goes live at merge, the skill after the kit upload; do both the same day.
- **Visuals untouched:** only `section.md` text and the mirrored card notes change; previews, `source.html` and CSS stay as they are.

### 7. Twelve rules taken from the native skills
They land in the gates or `api-and-code.md`, not as a new list:
1. Check for unpublished changes.
2. Confirm the publish landed.
3. Publish wording: "publish" = staging, "publish to the real website" = production, with a warning.
4. Rate findings as FAIL, WARN or NOTE.
5. Snapshots before changes.
6. Preview a shared edit before making it.
7. Accessibility via axe (in the script).
8. Internal link check (in the script).
9. Asset check: size, format, and alt text, with decorative alt left empty.
10. Rollback note.
11. Script hygiene.
12. Site inventory before a rebuild.

### 8. Related files and versions
- `build-kits.sh`: the new description (1024-character limit, no Figma as a page-design source) and a `WD_VERSION` bump from 1.8.0 to 1.9.0 (`guard_version` stops the build otherwise).
- `marketing-team/.claude-plugin/plugin.json` and `marketplace.json`: version bump; they must match (`scripts/audit-skills.sh`).
- `docs/claude-design-to-webflow.md`, `brain.md`, `README.md`, `CLAUDE.md`: updated descriptions.
- `CHANGELOG.md` entry; run `scripts/audit-skills.sh`.

### 9. Dry run
- Run the check script's pass and fail tests (step 2).
- A fresh subagent gets only the new skill plus the brief template and does a read-only Map step for `/pricing-conversational`. Its mapping must match what was actually built: `Section / Logo Wall`, the framed chain, the stories section.

### 10. Ship
- Branch and PR (checkpoint C) with the move table. Stefan reviews.
- After merge: org-upload check, kit rebuild and upload per the RUNBOOK on the same day, and a weekly log line.

## Checkpoints
- **A (done):**
  - one style embed allowed;
  - no `data-ds` attributes;
  - five gates instead of a long list;
  - accessibility check every build.
  - "publish" = staging; "publish to the real website" = production.
- **Open decisions:** none.
- **C:** the PR.

## Out of scope
- Any change to Webflow tokens, variables or classes.
- The pricing page itself: the Basin test and the production publish are Stefan's.
