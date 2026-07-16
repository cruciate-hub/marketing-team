# Pitfalls & anti-patterns — full catalog

Load this when debugging a specific symptom or planning a migration in detail. SKILL.md carries the one-line index; this file has the depth.

---

## Part 1 — Claude-prototype anti-patterns (recognize on the way IN)

What Claude's HTML/CSS prototypes emit constantly. Spot them as you read the prototype, plan the migration as you write it out.

| # | Pattern | Migration |
|---|---|---|
| A1 | **Section-root mega-rule** mixing `--var:` defs and real properties | Split: code keeps the `--var:` lines (descendants inherit); native gets the properties. → worked-examples A |
| A2 | **`all: unset`** on every interactive element | Wipes inherited props + beats native by cascade. Prefer specific native resets (`background:transparent; border-width:0; padding:0; font:inherit`), or keep in code and lose Style-panel control for that class. → Pitfall 7 |
| A3 | **Hardcoded brand hex** (`#3B41EC`, gradients) | Bind to a brand variable (`variable_as_value`) natively; in code wrap as `var(--token, #hex)` with the literal fallback. |
| A4 | **Custom @media breakpoints** (1200/980/720/560/520) | Webflow's are 1920/1440/1280/992/768/480. Round to nearest + move into Style-panel breakpoint values, OR keep the block in code. Per-block call. → Pitfall 5 |
| A5 | **JS-injected static content** (`insertAdjacentHTML`, `innerHTML`) | Designer can't see runtime-injected DOM. Rebuild static visuals as native elements (Embed for inline SVG, Image, Heading/Div). Keep JS only for behavior. → Pitfall 3 |
| A6 | **`:nth-child(N)`** for a specific position | API supports only `odd/even/first/last`. Refactor to distinct classes (`.jp-light-red`) for Style-panel control, or keep in code. |
| A7 | **`color-mix(in srgb, currentColor X%, transparent)`** | The Designer serializer mangles it to `pxpxpx black` on save. Keep in code only. → Pitfall 4 |
| A8 | **Class-fixer IIFE** that `classList.add()` by DOM index | Designer shows those classes as orphan/unused though they work at runtime. Prefer classes in HTML directly; drop the fixer. → Pitfall 12 |
| A9 | **Mobile horizontal overflow** from an unconstrained child (wide table/embed, `width:100vw` in a padded box, absolute element) | Fix the actual child (`max-width:100%; overflow-x:auto` on the wide element) via a site-head rule. Do NOT reach for `body{overflow-x:hidden}` — it silently kills `position:sticky`. Set preemptively; don't wait for QA on the `.io` URL. → Pitfall 17 |

---

## Part 2 — Migration pitfalls (symptom → cause → fix)

### 1. Code rules silently override native records
**Symptom:** you set a value in the Style panel but the page renders the old one.
**Cause:** Site/Page custom code loads AFTER Webflow's compiled CSS; equal specificity → code wins by order.
**Fix:** when migrating a rule to native, DELETE it from code. Never keep duplicates "for safety" — they break Style-panel adjustability.

### 2. Native records for classes no element uses
**Symptom:** "X styles not associated with any page elements."
**Cause:** the prototype referenced classes the real elements never got.
**Fix:** before `create_style`, verify usage: `data_element_tool query_elements` → `element_filter.style: "name"`. If `total_matches: 0`, don't create it.

### 3. JS-injected content is invisible to the Designer
**Symptom:** element renders live but Designer's tree/Style panel can't reach it.
**Fix:** rebuild static content as native elements (Embed for inline SVG, Image, Heading/Paragraph/Div). Use JS ONLY for behavior.

### 4. `color-mix()` (and `calc()`/`clamp()`) corrupted on save → `pxpxpx black`
**Cause:** the Designer serializer mangles `color-mix(in srgb, currentColor X%, transparent)` when the property is re-saved through the Style panel.
**Fix:** static colors → plain rgba/hex; dynamic per-state tints → keep `color-mix()` in code. **Cleanest native path:** create a **variable** whose `custom_value` is the `color-mix()`/`calc()`/`clamp()` expression (`data_variable_tool` accepts these as custom values), then bind the property to that variable with `variable_as_value` — the raw expression lives in the variable, untouched by the property serializer. If you must store it directly on a property, set it once via the API and never edit that property in the Style panel again.

### 5. Custom breakpoints don't map to Webflow's
**Cause:** Claude emits `1200/720/520`; Webflow's are `1920/1440/1280/992/768/480`.
**Fix:** round to native + move to Style-panel breakpoint values (lose precision, gain adjustability), OR keep the `@media` in code (keep precision, lose adjustability). Native breakpoint IDs + widths: `xxl` ≥1920, `xl` ≥1440, `large` ≥1280, `main` = base/desktop (≥992), `medium` ≤991, `small` ≤767, `tiny` ≤479. **Styles cascade DOWN** (main→medium→small→tiny): set at `small` and it also applies at `tiny` unless overridden. In em: `48em`=768px, `47.9375em`=767px, `61.9375em`=991px, `29.9375em`=479px.

### 6. Combo-class cascade is brittle
**Cause:** two single-class records fighting for one property at equal specificity (0,1,0); compiled order decides.
**Fix:** base props on ONE (generic) class; the combo overrides only the variant property. If both must set it, force via a higher-specificity descendant code rule.

### 7. `all: unset` beats native
**Fix:** prefer specific native resets. If truly needed (third-party UI), keep in code and accept that one class isn't Style-panel adjustable.

### 8. Duplicated `--variable` definitions
**Fix:** define each custom property in exactly ONE place — the section-root code rule; descendants inherit. Always `var(--brand-token, literal-fallback)`.

### 9. Query timeouts / "check the Designer MCP app" — but only for Designer-bridge tools
**Reality (corrected):** the **Data API tools (`data_*`) are headless** — `data_style_tool`, `data_element_tool`, `data_element_settings_tool`, `data_component_tool`, `data_scripts_tool`, `data_pages_tool`, `data_sites_tool`, `data_variable_tool` all work with **no Designer tab open**. Only **Designer-bridge tools** (`designer_tool`, `element_snapshot_tool`, live canvas ops) need the Designer tab active + focused. So: don't ask the user to open the Designer for style/element/code/publish work. If a Designer-bridge call times out with "check the Webflow Designer MCP app," THAT is when the tab must be focused.
**If a Data API query is slow/large:** query narrowly — `name_path` filter, and add `include_breakpoints`/`include_properties` only when you actually need them (breakpoint queries are the data-heavy ones).

### 10. Forgetting to publish — native changes don't show
**Fix:** native style edits + embed edits + freeform code all ship at publish time. Publish to staging: `data_sites_tool publish_site` with `publishToWebflowSubdomain: true`, `customDomains: []`. Production custom domain ONLY on explicit go-ahead (a full publish pushes ALL pending changes, not just yours).

### 11. Custom code IS API-readable/writable now (this reverses the old advice)
**Old (pre-2026-07):** "Site/Page Head/Footer code isn't exposed — paste by hand." **No longer true.**
- **Site & Page freeform Head/Footer:** `data_scripts_tool` → `get_site_freeform_code` / `set_site_freeform_code`, `get_page_freeform_code` / `set_page_freeform_code` (location `head` | `footer`). Read the current block, edit, write it back — no human paste.
- **HTML Embeds (the `<style>`/`<script>` blocks inside components or pages):** they're `HtmlEmbed` elements. Read/write their code with `data_element_settings_tool` → `get_settings` / `set_settings`, key **`code`** (`static_text.value` = the full `<style>…</style>` or `<script>…</script>` string). Find the embed element first: `data_element_tool query_elements` with `element_filter.type: "HtmlEmbed"` (scope to a component with `scope_component_id`).
- **Registered scripts** (App-added) are separate: `get_registered_scripts` / `add_site_script` etc.
**So:** you can iterate CSS/JS embeds and site code end-to-end via the API. Still worth backing up the original block to a local file before large rewrites, but paste-by-hand is no longer the default.

### 12. Class-fixer JS still does runtime adds — Designer can't see them
**Fix:** restructure so classes live in the HTML; drop the fixer. If kept, document which classes it adds; don't trust the Style Selectors panel for them.

### 13. Custom JS runs before Webflow's runtime
**Symptom:** `Webflow is undefined`, or interactions break on the published page (fine in the canvas).
**Fix:** wrap IIFEs that need the runtime in `Webflow.push()`:
```js
window.Webflow = window.Webflow || [];
window.Webflow.push(() => { /* your IIFE body */ });
```
Locally the `||= []` shim makes `.push()` a harmless array push; in production Webflow invokes it when ready.

### 14. Designer canvas renders animations differently than the published page
**Fix:** detect the canvas and short-circuit to a static final frame:
```js
const inDesigner = document.documentElement.classList.contains('w-editor') || window.self !== window.top;
if (inDesigner) { setActive(0); return; }
```

### 15. The Designer canvas does NOT apply custom-code embed CSS — only native styles
**Symptom:** an element you hid via a `<style>` embed (`visibility:hidden` / `display:none`) shows up **expanded/opaque in the Designer canvas**, blocking edits — even though it's correctly hidden on the published page.
**Cause:** the canvas renders native Style records but not your HTML-embed CSS.
**Fix:** add the hide as a **native** base style too (e.g. native `visibility:hidden` on the class), and let a higher-specificity code rule reveal it at runtime (`.is-open{visibility:visible}` = 0,2,0 beats native 0,1,0). Keeps both the canvas AND the live page correct. Don't use native `display:none` if a code rule toggles `visibility` (it would beat the toggle and kill fade animations).

### 16. Containing-block traps for `position:fixed`
**Symptom:** a `position:fixed` panel (mobile sheet, dropdown) mispositions or gets clipped.
**Cause:** any ancestor with `transform`, `filter`, `backdrop-filter`, `perspective`, or `will-change:transform` becomes the containing block for fixed descendants (they anchor to it, not the viewport). `overflow-x:auto` on an ancestor also clips both axes.
**Fixes:** move the blur off the wrapper onto a `::before` pseudo (`.wrapper::before{backdrop-filter:blur(7px)}`) so the wrapper isn't a containing block; keep floating panels OUT of an `overflow-x:auto` scroller (or make the open panel `position:fixed`). iOS Safari is stricter here (see Pitfall 19).

### 17. `body{overflow-x:hidden}` silently breaks sticky
**Symptom:** you add `overflow-x:hidden` to html/body to kill sideways scroll and the sticky nav stops sticking.
**Cause:** `overflow` on the document root turns the body into the scroll container, so `position:sticky`/`fixed` lose their viewport reference.
**Fix:** never scroll-lock via `overflow:hidden` on html/body. Fix the overflowing CHILD instead (Anti-pattern A9). For scroll-lock while a menu is open, use `touch-action:none` + a `passive:false` wheel listener that `preventDefault`s outside the menu — the document keeps its scroll position and sticky keeps working.

### 18. Shared-class / shared-embed blast radius
**Symptom:** you edited one page's nav and every product page changed.
**Cause:** in Webflow, a class or an embed (as a nested component like "Nav/Sub/CSS") is often shared across many components/pages. `data_style_tool` and `data_element_settings_tool` edits hit the CLASS/COMPONENT, i.e. every instance at once.
**Fix:** before editing a shared class/embed, check reach — `data_component_tool` with `includeInstanceCount`, and note the class isn't page-local. This is usually a FEATURE (one edit, consistent everywhere) but say so to the user, and scope anything that must stay per-breakpoint with the right `breakpoint_id` or a `matchMedia` guard in JS.

### 19. Chromium-only testing = an iOS-Safari blind spot
**Reality:** the in-app browser is Chromium; it will NOT reproduce Safari-only bugs. The frequent ones: `position:fixed` inside a `transform`ed+`overflow` ancestor mispositions or doesn't paint; opacity/`[data-animate]` reveal animations can fail to fire in a fixed/transform sheet, leaving content invisible.
**Fixes to apply preemptively:** prefer `position:absolute` anchored to a positioned ancestor over `fixed`-inside-transform; scope reveal-animations' initial `opacity:0` to `@media (min-width:48em)` so mobile content is never hidden behind an animation that might not run. Then flag it for a real-device retest — you can't self-verify Safari.

### 20. No bulk component-instance delete
**Symptom:** you want to remove a redundant component that has many instances.
**Reality:** `unregister_component` errors while the component is in use ("remove all instances first"), and there is NO bulk-delete-instances API — only per-page `remove_element`. Sweeping dozens of instances across 100+ pages via the API is disproportionate and error-prone.
**Fix:** for bulk removal, the Webflow **Designer's right-click → Delete Component** removes the definition + every instance atomically and is undoable (Cmd+Z). Surface this to the user — it's ~1 click per component vs a huge API sweep. Only you-the-agent hitting the API can't do it in one shot; the human can.

### 21. Publish propagation lag on the CDN
**Symptom:** right after `publish_site`, the live page still shows the OLD styles even with a cache-busting query param.
**Cause:** the compiled CSS/HTML takes ~1 navigation cycle (seconds to ~1 min) to propagate to the edge; the page-CSS file is content-hashed (`site.webflow.<pageId>.<hash>.opt.min.css`) so a stale HTML still points at the old hash.
**Fix:** after publishing, re-navigate the page once or twice; confirm propagation by checking the CSS filename hash changed, or by fetching the CSS and grepping for your new rule, or by asserting a computed style/marker in the DOM. Don't screenshot-verify until you've confirmed the new bundle is live.
