---
name: claude-design-to-webflow
description: Builds social.plus website pages and sections in Webflow (via the Webflow MCP) from Claude Design canvas boards, Claude artifacts or pasted HTML/CSS, and iterates on Claude-built Webflow sections. Use whenever a design or prototype has to become a live Webflow page or section, a section must match a board, a page is rebuilt or restyled in Webflow, components, classes, variables, embeds, custom code, assets or fonts are created or changed through the API, a build is checked against its board on staging, or a Webflow gotcha appears (whtml-builder quirks, framed sections and frame lines, publish lag, freeform-code errors, class-list replacement, Designer-only limits). Webflow is king: the site's components, class chains and variables win over the board. Page designs come from Claude Design, never Figma-to-Webflow. Not for CMS content (webflow-publisher) or blog posts (blog-publisher).
---

# Claude Design → Webflow

The only Webflow build skill for social.plus website pages. Before it: `brand-messaging` / `site-intelligence` (words), `design-system` on a Claude Design canvas (design), the illustration and motion skills (visuals). After it: Stefan publishes to production.

## Principles

**Ground rule: native first.** Every look is built with native Webflow styles, classes, variables, states and assets before any custom code. When the API can't reach something Webflow does natively (the Checked state of a custom checkbox, Designer-only settings), the answer is a short Designer step for Stefan, not an embed. Code is the last resort, only for what Webflow cannot express at all, and it needs Stefan's OK (Stefan, 19 Nov 2026; checkbox example in Pitfall 138).

1. **Webflow is king.** Webflow's components, class chains, variables, gutters and type scale are the source of truth. The board adapts to Webflow; never change a Webflow variable or shared class to match a board (Pitfall 134).
2. **Reuse first.** Existing component → existing class chain → new native class (Stefan's OK first) → code last. Never hand-build what a component already does (Pitfalls 64, 70, 131).
3. **Measured, not eyeballed.** `scripts/check-board.mjs` compares board and staging. "Done" means its report is in your message (Pitfalls 124, 125, 133).
4. **"Publish" means staging** (`.webflow.io`). Production only when Stefan says "publish to the real website", after warning that it pushes every unpublished change on the site.
5. **Style embeds sit next to what they style.** CSS that native styles truly can't express (`:has()`, keyframes; not checked states, which Webflow's custom checkbox has natively), with Stefan's OK, goes in a small `<style>` HtmlEmbed inside or beside its section, scoped to that section's classes. Several small embeds are fine; one page-wide embed or page head code is not. Never for layout a native class can do. List each embed in the report.
6. **Raise every drift.** Wherever Webflow wins over the board, put it on a "Webflow won" list and ask Stefan for OK to update the Claude Design board(s) and the design system (`design-system/`, Claude Design card notes) to match. Never silently, never the reverse.
7. **Ask, never decide alone.** Any choice with more than one reasonable answer that changes what Stefan gets is his to make: original page or copy, which pages, new class or component, replacing or keeping a section, where something lives. Copying an existing section means the same component with only the asked difference, never extra links, text or elements (Pitfall 140). Ask in one line before acting, with your recommendation first. Deciding it yourself and mentioning it afterwards is a no-go (Stefan, 19 Nov 2026; Pitfall 139).

## The five gates

Work in this order. Each gate must pass before the next step. If one fails, stop and fix it or ask.

### 1. Brief
- [ ] Target page confirmed with Stefan (id and slug), and it's staging. Ask him, before building, whether the build goes on the original page or on a copy; never pick it yourself (Principle 7, Pitfall 139). A copy page stays a copy until Stefan says otherwise.
- [ ] Board read fresh with `Artifact read` right now (not from memory, not an earlier read). Note the version the read or the last publish reports; if there is none, the read time.
- [ ] Board sections listed in order, each with what it shows.
- [ ] Webflow MCP ready: send `session_id: "start"` on the first call and reuse the issued `ses_` id; choose one `agent_id` (model|harness|suffix) for the whole task. `webflow_guide_tool` once (its output is large: save it and grep it), `data_agent_instructions_tool search_instructions`.
- [ ] Does the target page already hold a build? Then map and restyle what is there (Pitfall 88) and run the check against it first; never rebuild it blind.

### 2. Map
- [ ] For each board section: the Webflow component or existing section it maps to, and its exact class chain. Sources: the section's `## Webflow note` in `design-system/sections/**/section.md` (public repo: your checkout, or `git clone --depth 1 https://github.com/cruciate-hub/marketing-team.git /tmp/cruciate-hub-marketing-team`, or `git -C` that folder `pull` if it exists), then `data_component_tool query_components` (keywords: section, logo, card, button, icon, form), then an existing page's `query_elements children_depth:-1`. A note without a chain: take the chain from a page that uses it and add it to the note. Never a nearby site section because it looks similar (Pitfall 124).
- [ ] Framed sections use the full chain `section padding_Y background-color_dark border-top c-framed` (Pitfall 132; `site-conventions.md` rule 4).
- [ ] New classes, variables or components: none, or each named with its reason and approved by Stefan.
- [ ] Roles file for the check written, starting from `scripts/examples/pricing.roles.json` as a template (one role per section, in order, plus the elements that carry the look; `references/check-board.md`).

### 3. Build
- [ ] Structure with `data_whtml_builder`, existing class names only, no `css` param; styles with `data_style_tool`, colours and fonts bound to variables, sizes in rem.
- [ ] Buttons, links, icons, nav, footer, logo wall and other recurring sections are component instances.
- [ ] Text uses the site's global tag styles: `h1`-`h6` and `p` get no class. Add a class to a text element only for something the tag style can't give (a utility like `text-size-small`, or a width cap with `max-CH-<n>`), and name it in the report (Pitfall 136).
- [ ] Before editing a shared class or component: list every page it reaches (`includeInstanceCount`, `query_styles`) and say so. Never experiment on a shared component or Collection List (Pitfall 90).
- [ ] Before a large change: snapshot what you replace (element tree, embed code, freeform code) to a local file, as the rollback.
- [ ] Images: uploaded to the asset library (WebP, sized for their slot, about 2x), bound by asset id; decorative images `alt=""`, content images a real alt.
- [ ] Fix the whtml quirks right after each call: links, raw `href`/`rel`, `focusable`, `for=""`, buttons turned into links, images (Pitfalls 23, 66, 74, 101, 127; `api-and-code.md`).

### 4. Check
- [ ] Publish to staging, then confirm it landed (new class or text in the fetched page).
- [ ] Run `node scripts/check-board.mjs` at 1440/800/390. No FAIL left unexplained; each Webflow-owned difference is a NOTE in `known` and on the "Webflow won" list.
- [ ] Look at the side-by-side images yourself, section by section, including every line and "+" marker.
- [ ] Accessibility: the script's axe check passes (no serious or critical). Webflow's `accessibility-audit` skill is an optional extra where installed.

### 5. Publish and record
- [ ] Before any publish: compare the site's `lastUpdated` with `lastPublished`; name unpublished changes you didn't make.
- [ ] Staging publish only. Production only on "publish to the real website".
- [ ] "Webflow won" list raised with Stefan for the board and the design system.
- [ ] Lessons added as new pitfall numbers (plus a one-liner in the index at the end of `pitfalls.md`), in `design-system/feedback.md` where it is a design rule (or, without the repo, sent to Stefan to add).

## Report format

1. What was built: page, sections, element ids, components used.
2. Check result: `report.md` summary line (FAIL / WARN / NOTE / PASS) and every FAIL or WARN left, with its reason.
3. Embeds and new classes, each with what it does and why.
4. "Webflow won" list, with the question about updating the board and the design system.
5. What you could not verify (e.g. a real form submission behind Turnstile, iOS Safari).

## Subagents

Brief them with `references/subagent-brief.md` (it carries the gates), and check their result yourself before you report it.

## Pitfalls by topic (numbers in `references/pitfalls.md`, which never change)

- **Board and design source:** 59-62, 86, 88, 124-126, 134, 135, 139
- **Components, classes and variables:** 140, 136, 137, 2, 6, 41, 18, 20, 22, 52, 53, 56, 64, 65, 67, 70-73, 89, 90, 97, 122, 123, 130, 131
- **Framed sections and frame lines:** 80-87, 91-95, 132, 133
- **whtml, element and API quirks:** 9, 23-29, 37, 42, 46, 47, 51, 54, 66, 68, 69, 74, 76, 78, 98-101, 114, 127
- **CSS and layout traps:** 1, 4, 5, 7, 8, 16, 17, 30, 35, 36, 55, 58, 96, 105-107, 109, 110, 113, 128, 129
- **Custom code and scripts:** 3, 11-15, 33, 40, 43, 49, 50, 104, 119
- **Nav and menus:** 26, 27, 34, 38, 39, 44
- **CMS:** 89, 99, 102, 111, 116-118, 120, 121
- **Assets, icons and fonts:** 24, 48, 112, 115
- **Accessibility and semantics:** 75, 76, 79, 108, 115
- **Checking and verification:** 19, 21, 31, 32, 45, 57, 60, 63, 77, 87, 103, 125, 133
- **Publishing:** 10, 21

## References

- `references/site-conventions.md`: site rules 1-8 (components, links, SVGs, framed grids, variables, class system, embeds, gate), core principle, build gates, native vs code, breakpoints, responsive and components, the detailed checklist.
- `references/api-and-code.md`: the Webflow MCP tool stack and capabilities, whtml, custom code (freeform, embeds, registered scripts), assets and fonts, third-party embeds, genuine 1:1 baking, the token-efficient workflow, staging verification, the build playbook, publish settings.
- `references/check-board.md`: the board check, roles files, self-test, fallback by hand.
- `references/subagent-brief.md`: the brief template.
- `references/pitfalls.md`: every pitfall, with the one-line index at the end.
- `references/worked-examples.md`: before/after examples. `references/variable-ids.md`: variable ids (load only when binding).
