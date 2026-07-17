---
name: claude-design-to-webflow
description: Turning a Claude-generated design or prototype (claude.ai/design HTML/CSS/JS, a Claude Code artifact, or pasted markup) into a live Webflow build via the Webflow MCP, and iterating on Claude-built Webflow sections. Use whenever the user pastes HTML/CSS and wants it in Webflow, asks to rebuild/redo a section or a whole multi-page site in Webflow, weighs native-Style-record vs custom-code decisions, makes a section or component responsive across breakpoints, edits CSS/JS embeds or Site/Page head/footer code through the API, uploads design images or self-hosted fonts, authors reusable components with API-bound props and variants, works with shared classes or component instances, deletes redundant components, fixes cascade conflicts between custom code and native styles, strips JS-injected static content so the Designer can see it, binds hardcoded hex to Webflow variables, publishes to the staging subdomain, or hits Webflow gotchas (all:unset, color-mix corruption, nth-child(N), containing-block traps, sticky/overflow conflicts, whtml-builder combo-selector/link/image quirks, un-writable DOM ids, publish propagation lag, Chromium-vs-Safari differences). Covers the social.plus site (variable IDs in references/).
---

# Claude design/code → Webflow playbook

Verified on the official Webflow Connector (`mcp.webflow.com`). Depth lives in the reference files — leave them unread until needed:
- `references/pitfalls.md` — full anti-pattern + gotcha catalog (the numbered items indexed below)
- `references/worked-examples.md` — real before/after diffs (incl. the 2026-07 responsive nav)
- `references/variable-ids.md` — social.plus site ID + pre-mapped variable IDs (load ONLY when binding variables on that site)

## Core principle
**Native first, code only for what Webflow can't express.** Native styles are Style-panel-adjustable and publish cleanly; code that duplicates a native rule silently overrides it by cascade order. For the initial build of a whole section, **`data_whtml_builder` in one call** beats rebuilding element-by-element.

## The tool stack — what's headless, what needs the Designer
| Layer | Tools | Needs the Designer tab? |
|---|---|---|
| **Data API** (`data_*`) | `data_style_tool`, `data_element_tool`, `data_element_settings_tool`, `data_component_tool` (+ `data_component_variants_tool`, `data_component_props_tool`), `data_scripts_tool`, `data_pages_tool`, `data_sites_tool`, `data_variable_tool`, `data_assets_tool`, `data_fonts_tool`, `data_whtml_builder`, `data_element_builder` | **No** — fully headless. Do all style / element / embed / code / asset / publish work here. |
| **Designer bridge** | `designer_tool`, `element_snapshot_tool`, live canvas ops | **Yes** — active + focused, else a "check the Webflow Designer MCP app" timeout. |

- Webflow MCP tools are often **deferred**: load their schemas in one `ToolSearch` (`select:data_style_tool,data_element_tool,data_element_settings_tool,…`). Call `webflow_guide_tool` once per session for the current capability list.
- Call **`data_agent_instructions_tool search_instructions` early** — it returns site-specific rules the team encoded.
- The official **`webflow/webflow-skills` plugin** adds `safe-publish`, `custom-code-management`, `cms-best-practices` — compose with them, don't reinvent.

## Fastest build path — `data_whtml_builder`
One call turns `html` + `css` into a native Webflow section (auto-mapped to classes + breakpoints). Constraints (from the Webflow guide):
- **Single root element.** No `<style>` in `html` — CSS goes in the `css` param.
- **No `@keyframes`, no custom `@media`** — Webflow breakpoints only (below). Keep keyframes / custom-media in freeform head code.
- Build the section, THEN refine natively (bind variables, split hybrids). Far fewer tokens than N × `data_element_builder` + `create_style`.
- **Quirks to fix right after the call (→ Pitfalls 22-24):** write combo-class CSS as the **full chained selector** (`.base.combo{…}`, never `.combo{…}` alone — a bare combo selector spawns an orphan global rule + an *empty* combo record); it **drops `target="_blank"`** and leaves `href`/`rel` as raw attributes → re-set the link via `data_element_settings_tool set_settings` key `link`, then `remove_attribute`; and it does **not** bind `<img src>` to the asset library even at the canonical CDN URL → `set_image_asset` by asset ID afterwards. It DOES keep inline `<svg>` as native DOM, plus `<br>`, soft hyphens and curly quotes verbatim — no HtmlEmbed detour for those.

## Native vs code decision
**Native** (`data_style_tool` Style record): single-class rules; combo classes (`parent_style_names`); supported pseudos (`:hover :focus :focus-visible :active ::before ::after :nth-child(odd/even) :first/last-child :focus-within …`); responsive breakpoint values; variable bindings (`variable_as_value`).
**Code** (freeform head/footer, or an HTML embed): `@keyframes`, `@property`; descendant (`.a .b`) + attribute (`[data-x]`) selectors; `:nth-child(N)`; custom / feature queries (`prefers-reduced-motion`); `color-mix()` (Designer corrupts it on save — keep in code, OR store it as a variable `custom_value` and bind the property to that variable); section-root `--var:` definitions descendants inherit; all JS behavior.

## Breakpoints (authoritative)
`main` = base/desktop (≥992) · `medium` ≤991 (`max-width:991px`) · `small` ≤767 (`max-width:767px`) · `tiny` ≤479 (`max-width:479px`) · up-scaling `large`≥1280 / `xl`≥1440 / `xxl`≥1920. **Styles cascade DOWN** (main→medium→small→tiny): set at `small` and it also applies at `tiny` unless overridden. In em: 48em=768, 47.9375em=767, 61.9375em=991, 29.9375em=479. Round Claude's odd breakpoints (1200/720/520) to these, or keep that `@media` block in code.

## Responsive & components
- **Make ONE component responsive** instead of shipping a mobile-duplicate: native breakpoint styles + (when a shared embed needs a mobile-only tweak) edit the shared CSS/JS embed once, scoping any JS with `matchMedia` so other breakpoints stay byte-for-byte identical. → worked-examples E/F. Component **variants** (`data_component_variants_tool`) give per-component style overrides for non-breakpoint variations.
- **Author a reusable component headlessly:** build one instance (`data_whtml_builder`) → `data_component_tool transform_element_to_component` → define props (`data_component_props_tool create_prop`) → **bind each prop to its element** (`data_element_settings_tool set_settings` with `binding {source_type:'prop'}`) → reuse via `insert_component_instance` + `set_component_instance_prop_values` (a `variant` value selects a variant per instance). Reuse a component only where the pattern **visually matches its default**; where the design diverges, build bespoke elements and say why — don't force the component.
- **Shared-class / shared-embed blast radius:** class names are global site-wide and embeds are frequently shared components — one `update_style` or embed edit hits every instance. Check reach with `data_component_tool` `includeInstanceCount`; usually a feature (consistent everywhere), but say so to the user. → Pitfall 18.
- **Removing a redundant component:** no bulk instance-delete exists and `unregister_component` errors while the component is in use → hand the user the Designer **right-click → Delete Component** (removes definition + every instance atomically, undoable). → Pitfall 20.

## Custom code is API read/write now (reverses the old paste-by-hand advice)
- **Site/Page freeform head + footer:** `data_scripts_tool` `get_site_freeform_code`/`set_site_freeform_code`, `get_page_freeform_code`/`set_page_freeform_code` (location `head`|`footer`). Read → edit → write back; no human paste.
- **HTML embeds** (`<style>`/`<script>` inside a component or page): they're `HtmlEmbed` elements — read/write via `data_element_settings_tool` `get_settings`/`set_settings`, key **`code`** (`static_text.value` = the whole `<style>…</style>`/`<script>…</script>` string). Find them with `data_element_tool query_elements` `element_filter.type:"HtmlEmbed"` (`scope_component_id` for component-nested embeds). Still snapshot the original block to a local file before a big rewrite.

## Assets & fonts (headless upload — a faithful rebuild needs the real images + fonts)
- **Images:** `data_assets_tool create_asset` (file name + MD5 of the bytes) → POST the bytes to the returned presigned-S3 form → `set_image_asset` on the element by asset ID; alt text via `update_asset`. Upload first, bind by ID (whtml won't bind a raw CDN URL). Big JP/PNG → optional `compress_assets` to webp/avif (replaces the file in place — confirm first).
- **Self-hosted fonts:** `data_fonts_tool create_font` (same presigned-S3 + MD5 flow). A Google Fonts `css2` request returns ONE variable-font file per family (pass the `wght` axis range in `axes`), so a whole family is ~1-3 uploads — self-hosted is GDPR-friendlier than the Google CDN. Fallback: the user adds the family in Site Settings → Fonts by hand.

## Gotcha index (one line each — depth in references/pitfalls.md)
**Input anti-patterns:** A1 section-root mega-rule → split · A2 `all:unset` → native resets · A3 hardcoded hex → bind variable · A4 custom @media → round or keep in code · A5 JS-injected static content → rebuild native · A6 `:nth-child(N)` → distinct classes · A7 `color-mix()` → code/variable only · A8 class-fixer IIFE → classes in HTML · A9 mobile x-overflow → fix the child, never `body{overflow-x:hidden}` · A10 Claude Design canvas (`.dc.html`) = inline-styled frames side-by-side → read per `data-screen-label`, distil the inline styles into a pre-agreed class contract before building.
**Migration pitfalls:** 1 code overrides native (delete the dupe) · 2 orphan style records (verify usage first) · 3 injected DOM invisible to Designer · 4 color-mix corruption · 5 breakpoint mismatch · 6 brittle combo cascade · 7 all:unset · 8 duplicated `--var`s · 9 **Data tools are headless; only Designer-bridge needs the tab** · 10 must publish to ship · 11 **custom code IS API read/write now** · 12 class-fixer runtime adds · 13 wrap runtime IIFEs in `Webflow.push()` · 14 canvas-vs-published animation (`w-editor`) · 15 **canvas ignores embed CSS → add a native hide too** · 16 **containing-block trap** (transform/backdrop-filter breaks `position:fixed`) · 17 **`body{overflow-x:hidden}` breaks sticky** · 18 shared-class blast radius · 19 **Chromium-only = iOS-Safari blind spot** · 20 no bulk instance-delete · 21 **publish propagation lag** · 22 **whtml combo-CSS needs the chained selector** (`.base.combo`) else orphan global + empty combo · 23 **whtml drops `target=_blank`** → re-set the link, strip leftover `href`/`rel` · 24 **whtml won't bind `<img>`** to the asset library → `set_image_asset` by ID · 25 **DOM `#id` write can fail** ("component map" conflict on whtml-built / nested elements) → anchor/in-page links may need a one-time Designer step · 26 **no Navbar element type; DropdownToggle refuses `set_text`** → mobile menu via the Dropdown element or a JS-free checkbox-hack, toggle label via whtml children (verify textContent) · 27 **dropdown hover-open isn't a setting** → `data-hover`/`data-delay` attributes + CSS-hover fallback · 28 **Body takes no class** → edit the `body` tag Style record (global) or a page-scoped `<style>` embed (per-page bg) · 29 **read-back surprises** — `update_page_settings` mirrors the SEO title into the page name (send `title` in the same call); `query_elements` shows page-links as `linkType:"none"` (raw settings are the truth); form-input placeholders aren't API-settable (Designer step).

## Token-efficient workflow
- **One `data_whtml_builder` per section** > many element/style calls.
- **Read the page ID from the live DOM** (`document.documentElement.getAttribute('data-wf-page')`) instead of `list_pages`.
- `data_pages_tool list_pages` returns huge payloads (auto-saved to a file) → **jq/grep the saved file**; paginate with `limit`/`offset` (`total` is in `pagination`). Same for any 50k+ tool response — slice the file, never re-read it into context.
- **Query styles narrowly:** `data_style_tool query_styles` by `name_path`; add `include_breakpoints`/`include_properties` only when you need them (breakpoint queries are the heavy ones).
- **Verify with measurements, not screenshots:** JS `getComputedStyle` / `getBoundingClientRect` / CSSOM in the browser, or `element_snapshot_tool` (single-element PNG). Full-page screenshot only for the final human-facing proof — and note the in-app browser captures from **scroll-position 0 only** and Webflow **lazy-loads images**, so a full-page shot silently misses below-the-fold visuals; force `loading=eager` + scroll the page through first, or take the proof shot with a headless engine.
- **Batch** style/element writes via the `actions[]` array; **edit a shared embed once** instead of per page.

## Verify on staging (browser, not guesswork)
1. Publish to staging (below).
2. **Propagation lags** — re-navigate once or twice; confirm the new bundle is live by checking the page-CSS hash changed (`site.webflow.<pageId>.<hash>.opt.min.css`) or by fetching the CSS and grepping for your rule, THEN measure. → Pitfall 21.
3. Assert computed styles / rects + `read_console_messages` (expect zero errors) across the REAL scenarios (announcement banner on/off, each breakpoint, menu open, sticky at rest & scrolled). Screenshot last.
4. Chromium can't reproduce Safari bugs → flag any fixed-inside-transform / reveal-animation risk for a real-device retest. A **headless WebKit engine** (e.g. Playwright's WebKit) catches many — not all — of those render quirks the in-app Chromium browser can't, and works without a physical device. → Pitfall 19.

## Build / migration playbook
1. **Recon:** `data_agent_instructions_tool` (site rules) · `data_variable_tool query_variables` (name→ID map; social.plus pre-mapped in references/variable-ids.md) · `data_style_tool query_styles name_path` (existing classes) · read the target page's live DOM. Back up any freeform block you'll rewrite. For a **multi-page site or a Claude Design `.dc.html` canvas**, split frames by `data-screen-label` and lock a shared **class contract** (shared `bb-`-style names + per-page prefixes) up front, so parallel section-builds don't collide on naming — Anti-pattern A10.
2. **Build** the section with `data_whtml_builder` (element-by-element only when you need fine control).
3. **Categorize** each remaining rule: native-eligible → `update_style`/`create_style`; code-only → freeform/embed; hybrid section-root → `--var:` in code, properties native.
4. **Bind variables** (`variable_as_value`) wherever a value matches a brand token; always keep a literal fallback in code.
5. **Rebuild JS-injected static content** as native elements; keep JS for behavior only, wrapped in `Webflow.push()`.
6. **Trim the code** — delete every rule now native (cascade conflicts are the #1 killer). Write embeds/freeform back via the API.
7. **Publish to staging + verify** (above). Iterate. Production ONLY on explicit go-ahead.

## Publish
`data_sites_tool publish_site` → `publishToWebflowSubdomain: true`, `customDomains: []` = staging (`*.webflow.io`) only. A **full publish pushes ALL pending changes** to production — do it only on explicit user go-ahead. For isolated iteration, the branch API (`data_pages_tool create_branch → publish_branch → merge_branch` with conflict resolution) keeps work off main.

## When NOT to use
Pure Webflow work with no design/prototype input → generic `webflow-skills:*`. One-off CSS tweaks with no migration. Pure Claude-artifact iteration with no Webflow target. Content writing / CMS edits → the content skills + `webflow-skills:safe-publish`.

---
Depth on demand → `references/pitfalls.md` · `references/worked-examples.md` · `references/variable-ids.md`
