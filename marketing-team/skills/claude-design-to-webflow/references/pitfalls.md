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
| A10 | **Claude Design canvas export** (`.dc.html`) — all 7-ish page frames sit side-by-side, near-100% **inline-styled**; the shared `<style>` block is negligible | The "categorize the stylesheet's rules" plan assumes a stylesheet; here the work is **inline styles → class system**. Read frame-by-frame via the `<!-- PAGINA … -->` banners / `data-screen-label`; lock a shared class contract (shared names + per-page prefixes) BEFORE building so parallel section-builds don't collide. Ignore prototype-only mechanics (pan/zoom `support.js`, `data-comment-anchor`, Tweaks props, the grey frame caption). |

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
**Fix:** never scroll-lock via `overflow:hidden` on html/body. Fix the overflowing CHILD instead (Anti-pattern A9). **When you DO want a horizontal-overflow guard on body AND a sticky nav, use `overflow-x: clip` (not `hidden`)** — `clip` prevents sideways scroll WITHOUT establishing a scroll container, so `position:sticky` keeps working. That's the clean coexistence fix (→ Pitfall 30). For scroll-lock while a menu is open, use `touch-action:none` + a `passive:false` wheel listener that `preventDefault`s outside the menu (or a scoped `body:has(#menu-toggle:checked){overflow:hidden}`) — the document keeps its scroll position and sticky keeps working.

### 18. Shared-class / shared-embed blast radius
**Symptom:** you edited one page's nav and every product page changed.
**Cause:** in Webflow, a class or an embed (as a nested component like "Nav/Sub/CSS") is often shared across many components/pages. `data_style_tool` and `data_element_settings_tool` edits hit the CLASS/COMPONENT, i.e. every instance at once.
**Fix:** before editing a shared class/embed, check reach — `data_component_tool` with `includeInstanceCount`, and note the class isn't page-local. This is usually a FEATURE (one edit, consistent everywhere) but say so to the user, and scope anything that must stay per-breakpoint with the right `breakpoint_id` or a `matchMedia` guard in JS.

### 19. Chromium-only testing = an iOS-Safari blind spot
**Reality:** the in-app browser is Chromium; it will NOT reproduce Safari-only bugs. The frequent ones: `position:fixed` inside a `transform`ed+`overflow` ancestor mispositions or doesn't paint; opacity/`[data-animate]` reveal animations can fail to fire in a fixed/transform sheet, leaving content invisible.
**Fixes to apply preemptively:** prefer `position:absolute` anchored to a positioned ancestor over `fixed`-inside-transform; scope reveal-animations' initial `opacity:0` to `@media (min-width:48em)` so mobile content is never hidden behind an animation that might not run. Then flag it for a real-device retest. **Partial self-check:** a **headless WebKit engine** (e.g. Playwright's WebKit — browsers cache locally) reproduces many of these render quirks that the in-app Chromium browser cannot, and needs no physical device. Not identical to iOS Safari, but strong for containing-block / paint / lazy-load quirks; still flag the residual risk for a real device.

### 20. No bulk component-instance delete
**Symptom:** you want to remove a redundant component that has many instances.
**Reality:** `unregister_component` errors while the component is in use ("remove all instances first"), and there is NO bulk-delete-instances API — only per-page `remove_element`. Sweeping dozens of instances across 100+ pages via the API is disproportionate and error-prone.
**Fix:** for bulk removal, the Webflow **Designer's right-click → Delete Component** removes the definition + every instance atomically and is undoable (Cmd+Z). Surface this to the user — it's ~1 click per component vs a huge API sweep. Only you-the-agent hitting the API can't do it in one shot; the human can.

### 21. Publish propagation lag on the CDN
**Symptom:** right after `publish_site`, the live page still shows the OLD styles even with a cache-busting query param.
**Cause:** the compiled CSS/HTML takes ~1 navigation cycle (seconds to ~1 min) to propagate to the edge; the page-CSS file is content-hashed (`site.webflow.<pageId>.<hash>.opt.min.css`) so a stale HTML still points at the old hash.
**Fix:** after publishing, re-navigate the page once or twice; confirm propagation by checking the CSS filename hash changed, or by fetching the CSS and grepping for your new rule, or by asserting a computed style/marker in the DOM. Don't screenshot-verify until you've confirmed the new bundle is live.

---

## Part 3 — `data_whtml_builder` & headless-build gotchas (the fastest path has sharp edges)

### 22. whtml combo-class CSS silently splits into an orphan global + an empty combo
**Symptom:** a fragment with `class="bb-section bb-home-hero"` and CSS `.bb-home-hero{…}` renders fine, but the Designer shows TWO records — an unattached global `.bb-home-hero` holding the properties, and an *empty* combo `.bb-section.bb-home-hero` on the element. The datamodel is polluted; a Style-panel edit on the combo does nothing.
**Cause:** a single-class selector doesn't match the combo the element actually carries; whtml creates the global for the CSS and an empty combo for the class pairing.
**Fix:** write the selector as the **full chained selector** — `.bb-section.bb-home-hero{…}` — so the properties land directly on the combo record. Validated to depth 3 (`.bb-section.is-dark.bb-home-reviews`). Same rule for any combo you build via whtml.

### 23. whtml drops `target="_blank"`; `href`/`rel` survive only as raw attributes
**Symptom:** external links open in the same tab; `set_link` on a DropdownLink errors; `query_elements` shows the link as `linkType:"none"`.
**Cause:** whtml doesn't translate `target`/`rel` into the element's link *setting*; it leaves `href`/`rel` behind as plain HTML attributes (which don't drive Webflow's link behavior).
**Fix:** set the real link via `data_element_settings_tool set_settings` key **`link`** (mode `url` + `open_in_new_tab:true` + `rel`), then `data_element_tool remove_attribute ["href","rel"]` to clear the leftover attributes. `set_link` (element tool) works on Link/Button/TextLink but NOT on DropdownLink — use the settings key there.

### 24. whtml won't bind `<img src>` to the asset library
**Symptom:** an `<img>` in the fragment shows a "does not exist in asset library" warning and renders blank/broken, even when `src` is the canonical `cdn.prod.website-files.com/...` URL from `create_asset`.
**Cause:** whtml matches images by asset-library membership, not by URL; a raw CDN URL isn't recognized as an asset reference.
**Fix:** upload first (`data_assets_tool create_asset` → presigned-S3 POST), then `set_image_asset` on the Image element by **asset ID** after the fragment lands. The `alt` from the `<img>` tag is preserved.

### 25. Writing a DOM `#id` can fail on whtml-built / component-nested elements
**Symptom:** `data_element_settings_tool set_dom_id` (or a `domId` setting write) errors with a "component map" conflict; a poisoned source element then fails EVERY subsequent write.
**Cause:** the id-write path conflicts on certain element provenances (whtml-built, or nested in a component tree). Not universal — it works on many elements — but it recurs on exactly the elements you'd anchor to.
**Fix:** if it errors, delete + rebuild the element clean and retry once; if it still fails, hand the user a one-time Designer step (select the section → set the ID) so the in-page/anchor link resolves. Surface this as a manual to-do rather than silently shipping a dead anchor.
**Same conflict hits `set_attributes`** (e.g. tagging a container with `data-gsap-transition`), especially right after building the element or after **parallel writes on the same page**. So: **serialize mutations on one page** — don't run element builds and attribute writes concurrently. If an element stays unwritable even sequentially, the map is poisoned for that element; add the attribute once in the Designer (Settings → custom attribute), or rebuild the element fresh.

### 26. No Navbar element type, and the DropdownToggle subtree refuses `set_text`
**Symptom:** `data_element_builder` has no `Navbar` type; `set_text` on a block inside a `DropdownToggle` returns "this element doesn't support text" — and when you create such a block via `element_builder`, it silently keeps the placeholder ("This is some text inside of a div block.").
**Fix (nav):** build the mobile menu JS-free — a checkbox-hack (`input[type=checkbox]` + `label`, both via `BY_CUSTOM_TAG`) with toggle CSS (`:checked ~ .menu{…}`) in an HtmlEmbed (those selectors can't be native Style records), or use the native **Dropdown** element (tap works via webflow.js). **Fix (toggle label):** set the toggle's text by inserting a `<div>Label</div>` **whtml child** (whtml writes text at creation, bypassing `set_text`), then remove the placeholder block. Always re-read `textContent` to confirm.

### 27. Dropdown hover-to-open is not an element setting
**Symptom:** `get_settings` on a DropdownWrapper exposes only `domId`/`tag`/`visibility`/`attributes` — no "open on hover" toggle.
**Fix:** add `data-hover="true"` + `data-delay="300"` as custom **attributes** (webflow.js reads them off the DOM on the published site) and add a CSS `:hover` fallback (with a small `::before` gap-bridge) in an embed for desktop. Tap-to-open still works natively; no custom JS needed.

### 28. The Body element accepts no class
**Symptom:** `set_style` on the page's Body errors "this element doesn't support styles" (Body exposes only `domId`).
**Fix:** to restyle the body, edit the **`body` tag Style record** itself — `data_style_tool update_style style_name:"body"` (global, all pages; also where you neutralize a template's `padding-top` etc.). For a **per-page** body background (e.g. one dark page in a light site), add a page-scoped `<style>` embed (`body{background:var(--token)}`) since you can't scope the global tag style to one page; note it so the user can later move it onto Body in the Designer.

### 29. `update_page_settings` and link read-backs mislead
**Symptom (a):** setting SEO title via `update_page_settings` also renames the page's Navigator/display name. **Symptom (b):** `query_elements` reports a correctly page-bound link as `linkType:"none"`. **Symptom (c):** form-input `placeholder` won't set through the API.
**Fixes:** (a) pass `title` (the display name) in the **same** `update_page_settings` call as `seo.title`, so it isn't overwritten. (b) trust `data_element_settings_tool get_settings` `all_raw_settings` — it shows the real `source_type:page` binding; `query_elements`' `linkType` is unreliable for page/prop links. (c) placeholders are a Designer-only field right now → leave a manual to-do.

---

## Part 4 — sticky/animation & reveal gotchas (added after a full multi-page build)

### 30. Sticky nav vs the body horizontal-overflow guard → `overflow-x: clip`
**Symptom:** you set the nav to `position:sticky; top:0` and it doesn't stick — it scrolls away.
**Cause:** an ancestor with `overflow` other than `visible` becomes the scroll container for its sticky descendants. `body{overflow-x:hidden}` (a common guard against sideways scroll) is exactly that.
**Fix:** change the guard to **`overflow-x: clip`**. `clip` still prevents horizontal scrolling but does NOT establish a scroll container, so `position:sticky` works. (Well supported since 2022.) Keep `overflow-y` at its default `visible`. The nav itself: `position:sticky; top:0; z-index:100; background: <token>` + a hairline bottom border reads clean over scrolling content.

### 31. Scroll-reveal that never fires for above-the-fold content (ScrollTrigger)
**Symptom:** a GSAP/ScrollTrigger reveal (`autoAlpha:0→1` on `start:"top 95%"`, `once:true`) leaves the hero and other in-view-on-load content **permanently hidden**; below-the-fold reveals may work.
**Cause:** an element already scrolled past its start on load may never get an "enter" event (or a `ScrollTrigger.refresh()` re-applies the start state), so the reveal tween never plays — and it's stuck at `autoAlpha:0` behind the pre-paint visibility gate.
**Fix:** drive the reveal with an **IntersectionObserver** (fires reliably for elements intersecting on load) and let it trigger the GSAP tween:
```js
const io = new IntersectionObserver((es)=>es.forEach(e=>{ if(!e.isIntersecting) return;
  const t=e.target.children.length?[...e.target.children]:[e.target];
  gsap.to(t,{autoAlpha:1,y:0,duration:.6,stagger:.08,ease:'power2.out',overwrite:'auto'}); io.unobserve(e.target); }),
  {rootMargin:'0px 0px -8% 0px', threshold:.06});
groups.forEach(g=>{ gsap.set(targetsOf(g),{autoAlpha:0,y:20}); io.observe(g); });
setTimeout(()=>groups.forEach(revealAll), 4000); // FAILSAFE: never leave content hidden
```
Always ship the failsafe + a `prefers-reduced-motion` short-circuit (add a class that releases the gate) + keep the pre-paint hide keyed to an **attribute present in the HTML** (e.g. `[data-reveal] > *{visibility:hidden}`), not a JS-added class, to avoid a flash.

### 32. The in-app preview browser doesn't fire IntersectionObserver or scroll reveals
**Symptom:** after wiring reveals, the preview pane shows sections "stuck hidden" and `getComputedStyle(...).visibility === 'hidden'` even for the hero — but the code is correct.
**Cause:** the pane renders in a non-painting/background tab where IntersectionObserver callbacks and scroll-driven triggers don't run. It's a measurement artifact, not a site bug.
**Fix:** verify reveal/scroll animations in a **headless WebKit** run (Playwright): load, wait, assert `visibility`/`opacity`, scroll to below-fold elements and re-assert, screenshot for the human proof. (Also the Safari-render partial check — see Pitfall 19.) Don't diagnose "stuck hidden" from the pane.

### 33. Read (and reuse) the existing site freeform code before writing your own
**Symptom:** you `set_site_freeform_code` and overwrite an existing schema block / analytics / an already-wired GSAP reveal system; or you add a SECOND animation layer that fights the first.
**Cause:** `set_site_freeform_code` / `set_page_freeform_code` **REPLACE** the whole block, and many Webflow templates already ship a reveal system (e.g. GSAP+ScrollTrigger keyed to a `[data-…-transition]` attribute) plus schema/`::selection`/font-smoothing in the head.
**Fix:** `get_site_freeform_code` FIRST; preserve everything and append. If a reveal system already exists, **activate it** (tag the right wrappers) rather than adding your own — one source of motion. When you must improve it (e.g. add the missing reduced-motion guard, or swap ScrollTrigger→IntersectionObserver per Pitfall 31), edit that block in place and keep its fallbacks (`gsap-not-found`, `noscript`).
**Verify a large re-send byte-for-byte.** Appending to a freeform block or an `HtmlEmbed` means re-sending its *entire* existing content, and one wrong character in ~10KB of working nav JS kills that component on every page it ships to. Don't trust the retype: (1) **before** editing, fetch the live page and extract the existing `<script>`/`<style>` block to a file *mechanically* (regex over the fetched HTML — no transcription involved), (2) `node --check` it, (3) make the edit, (4) after publishing, extract again and diff against the saved file — the untouched part must come back **identical**, and a length difference alone tells you something drifted. Two further safety properties worth knowing: freeform/embed edits only reach the site on **publish**, so you can write → read back → verify → and only then publish; and appending *after* the existing block (rather than merging into it) keeps the original bytes contiguous and the diff trivial.

### 34. Premium mobile menu, JS-free (extends Pitfall 26)
**Pattern:** a full-screen overlay menu that reads as "designed," not a default dropdown: checkbox-hack (`input#toggle` + `label`), overlay `position:fixed; inset:0` with `opacity/visibility` transitions; large serif links that **stagger** via per-child `transition-delay` (nth-child or a `--i` var); the hamburger→X morph on 3 `<span>` bars; scroll-lock via `body:has(#toggle:checked){overflow:hidden}`; the primary CTA pinned at the bottom; and a `@media (prefers-reduced-motion:reduce)` branch that drops the transforms/stagger. Panel ~200-350ms, icon morph ~150-250ms. All CSS in the nav component's HTML embed → site-wide via the component.

---

## Part 5 — native Webflow Navbar & embed-layout traps (added after a native-navbar build)

### 35. Webflow `.w-container` clearfix `::before`/`::after` become flex items
**Symptom:** you set a NavbarContainer / Container to `display:flex; justify-content:space-between`, margins are `0`, only two real children are in flow (e.g. logo + hamburger), yet they render **centered** instead of pinned left/right. `getComputedStyle` confirms `justify-content:space-between` — the paradox.
**Cause:** Webflow's built-in `.w-container` ships a clearfix — `::before` and `::after` with `content:" "; display:table`. Inside a flex container those two zero-width pseudo-elements become **flex items**; with `space-between` there are now four items (`::before`, logo, hamburger, `::after`) and the pseudos seize the outer slots, pushing the real content toward the middle (the logo lands ~⅓ in, not at the edge). The measurement is genuinely paradoxical — margins 0, two real children, `space-between`, yet centered.
**Fix:** `#nav > div::before, #nav > div::after{display:none}` — the clearfix is useless in a flex row. Two neighbours of the same trap: `#nav > div` **also matches the sibling `.w-embed` `<style>` div** (both are direct children of the NavbarWrapper), so when you measure "the row" you may grab the wrong one; and `.w-container` carries Webflow's own **`max-width:728px` at ≤991**, the source of a mystery 728-px row width and a ~2 px off-centre when you expected full width. Override `max-width` when the nav must span like a wider content container. **Better — avoid the trap at the source:** use a plain **Block/Div** for the inner wrapper instead of the built-in **NavbarContainer** (`.w-container`); a Block has no clearfix `::before/::after`, so there's nothing to `display:none` and no 728-px cap to fight.

### 36. An embed's ID-selector layout silently overrides the Designer Style panel
**Symptom:** the user reduces padding on the nav's class (`.nav-container`) in the Style panel and "it doesn't even work" — the published site ignores every value.
**Cause:** the styling embed owns that box-model with an ID-scoped selector — `#nav > div{padding:…}` is specificity **(1 id, 0, 1 type)**, which outranks the element's class (`.nav-container` = 0,1,0). Same root as Pitfall 1 (code beats native), but here it's the *user's own Designer edits* that die, so the editor itself looks broken. (The class may not even exist on the published site yet — a Designer-only, unpublished class the embed was always going to override.)
**Fix:** decide who owns the box-model. Either (a) keep padding/margin/width in **native classes** (Style-panel-editable) and put only the un-native parts (the `:has()` overlay, the clearfix fix) in the embed; or (b) own it fully in the embed and tell the user that class won't move it. To align a nav with page content, don't hardcode a gutter — **match the content container's responsive padding at each breakpoint** inside the embed (worked example G), so the nav tracks the content automatically and no Style-panel edit is needed.

### 37. Component-nested HtmlEmbed: `get`/`set_settings` needs `scope_component_id` + an object `element_id`
**Symptom:** `get_settings` / `set_settings` on an `HtmlEmbed` inside a component returns **"Element not found"**, even though `get_all_elements` (with `scope_component_id`) just listed that exact element id.
**Cause:** the lookup for an element inside a component definition must be routed into that component's tree, and `element_id` must be the **object** form — a bare string or `{id}` is rejected (the tool asks for `component` + `element`).
**Fix:** pass `element_id:{component:<compId>, element:<elId>}` **and** `scope_component_id:<compId>` on the same action. The embed code lives under key **`code`**, value group `static_text` (`value` = the whole `<style>…</style>` / `<script>…</script>` string). Snapshot the current `code` to a local file first; after a large rewrite read it back and **hash-compare** to your file. Keep the `<style>` string free of literal double-quotes/backslashes (percent-encode data-URIs — `%22`, `%3C`, `%20` — and use single quotes in `content:''`) and it stays JSON-safe as a single-line tool argument, no escaping.

### 38. Native Webflow Navbar — you style one the user placed; you can't build it (extends Pitfall 26)
**Symptom:** you want a native nav but `data_element_builder` has no `NavbarLink` / `NavbarMenu` / `NavbarButton` type; and a freshly-dropped Navbar can be invisible to the Data API while it's still wrapped in a component.
**Flow:** the native Navbar is a fixed element family — `NavbarWrapper (#id, .w-nav) > NavbarContainer (.w-container) > NavbarBrand / NavbarMenu(NavbarLink…) / NavbarButton`. Ask the user to drop a Navbar element; if the API can't see it, ask them to **detach it from its component** so it surfaces in the page tree (you can re-componentize it yourself afterwards).
**Wiring (headless once visible):** native links are a **setting, not `set_link`** — `set_settings` key `link`, value `static_link:{mode:'page', to:<pageId>}` (a NavbarLink/Dropdown rejects `set_link`: *"only Link elements support links"*); an empty TextBlock or the DropdownToggle rejects `set_text` → initialise the text via `set_settings static_text.value` or write the inner `String` node; add `data-collapse="medium"` on the wrapper so the mobile breakpoint collapses. **Style from ONE HtmlEmbed inside the component**, every rule scoped under the wrapper's `#id`, because the Style panel can't express the fixed-overlay `:has()` mobile menu. This is the *native* counterpart to the JS-free checkbox-hack nav (Pitfall 34) — the mobile menu here keys off `#nav:has(.w-nav-button.w--open)` instead of a checkbox.

### 39. Migrating a custom nav → native leaves per-page duplicate navs
**Symptom:** after swapping a hand-built header for a native Navbar, the published site shows **two navs stacked** on most pages.
**Cause:** the old nav was a component placed **per page**, so removing it from the template (or one page) does NOT remove it elsewhere — old and new both render.
**Fix:** sweep every page headlessly (fetch each URL, check for the old nav's root class, e.g. `.old-nav`) to get an exact delete-list; remove the old component instance on each page in the Designer — `unregister_component` errors while it's in use, so per Pitfall 20 it's a right-click **Delete Component**. Re-sweep afterwards to confirm only the native wrapper (`#nav`) remains site-wide.

### 40. Webflow Interactions (IX2/IX3) can't be authored via ANY API → an agent's nav motion/open-state is genuinely code-only
**Symptom:** you want the mobile-menu open animation, a hamburger→X morph, or staggered link reveals done "the native way" (Webflow Interactions in the Designer) instead of custom CSS — but there's no tool for it.
**Cause (verified, 2026, against Webflow's own docs + staff):** neither the Data API nor the Designer API can **create, attach, or trigger** Webflow Interactions — the official MCP overview's *Limitations* section states the server "cannot yet create or apply Webflow Interactions (IX3)," Webflow staff confirmed the same for IX2 on the developer forum, and the Designer API reference enumerates elements/styles/components/variables/pages but **no** interactions/animations/keyframes. Separately, `data_style_tool` writes exactly ONE class/combo + ONE pseudo from a fixed enum — `noPseudo, hover, active, visited, focus, focus-visible, focus-within, placeholder, empty, before, after, first-child, last-child, nth-child(odd), nth-child(even)` — so it **cannot express `:has()`, arbitrary `:nth-child(N)`, descendant (`#nav .x`), attribute (`[class]`), compound-state (`.w-nav-button.w--open`), or ID-scoped selectors** at all. Result: for an agent, the `:has()` open-state overlay, the per-item `nth-child(2..N)` stagger, and the `.w--open` button morph have **no native-API expression whatsoever** — a scoped `<style>` embed is the only way, and it's exactly the custom-DOM/custom-code fallback Webflow's own docs prescribe for anything the visual tools can't express (so it's sanctioned, not a hack).
**The leaner-navbar division of labor** (what to put where): keep in ONE small embed only the three genuinely code-only effects — `#nav:has(.w-nav-button.w--open)` overlay open-state, `nth-child` stagger delays, and the `::before/::after` hamburger morph. Push everything else OUT of the embed and make it native: per-breakpoint gutters + max-width and tablet-and-below hover removal → native `update_style` records (breakpoint- and pseudo-scoped); the dropdown chevron → an inline `<svg>` via whtml (Pitfall 24), not a `mask-image` data-URI; the dropdown close-behaviour → the native `data-hover`/`data-delay` attributes (Pitfall 27); and dodge the clearfix fix entirely with a plain Block instead of the NavbarContainer (Pitfall 35). If the site is human-maintained, the overlay/morph/stagger can instead be handed off as a **Designer-only IX task** (Webflow ships official overlay+stagger templates built entirely in Interactions) — more "native," but unreachable by the agent, and less portable/diff-able than the scoped embed. Rule of thumb: on a navbar, roughly half of a naïve embed is code-only and half should have been native records — don't let the code-only half pull the rest into the embed with it.

---

## Part 6 — variables, style writes & the a11y-fix API surface (added after a variable-reorg + accessibility pass)

### 41. Dangling variable bindings after a variable rename/reorg — how to find and heal them headlessly
**Symptom:** after you (or the user) rename/move/delete Webflow variables — e.g. reorganising fonts into a `Headings/` group — the Style panel shows the property as **"… (deleted)"** (Font Serif (deleted), a colour (deleted), a size (deleted)). The published site may still render (it reflects the *last* publish) but it breaks on the next publish.
**Cause:** a style binds a property to a variable *by ID*. Deleting/replacing the variable leaves every binding dangling on the old, now-missing ID. One reorg can strand dozens of bindings (font-family AND colour/size/line-height).
**Detect (fully headless):** (1) read the live variable set — `data_variable_tool query_variables { queries:[{}] }` (the `queries` array is required; `pageId` is required top-level) — collect the valid `variable-…` IDs. (2) `data_style_tool get_styles { query:"all", include_properties:true }` — this is large and **persists to a file**; parse with Python/jq, don't inline it. Any property whose value is `{"id":"variable-…"}` where the ID is **not** in the live set is dangling. Group by the missing ID; infer intent from usage (serif/display font-sizes → the serif font var; small body/UI/button sizes → the sans).
**Fix:** `data_style_tool update_style { style_name, properties:[{ property_name:"font-family", variable_as_value:"variable-<new-id>" }] }`. Load-bearing facts, all verified: **`update_style` MERGES** — it changes only the named property and leaves size/colour/margins intact (so you can rebind one property safely); `variable_as_value` takes the **variable-id STRING**, not an object; use `property_value` instead for a literal; batch many via the `actions[]` array; then re-scan to confirm **zero** remaining dangling bindings on the target var. Caveat: a big variable cleanup usually also leaves dangling bindings on **orphan template classes** you don't use (`container-medium`, `text-color_*`, `margin-bottom_*` …) — those never render, so heal your real (used) classes and treat template orphans separately (leave or delete, don't rebind blindly).

### 42. Data-API dead-ends that force a Designer step (surfaced during an accessibility pass)
Some edits have **no** Data-API path and must be done in the Designer / Site Settings — know them so you don't burn calls discovering it live:
- **`set_tag` is rejected on Webflow-native widget elements.** A `DropdownList` (Webflow renders it as `<nav>`), and similar widget internals, return **"Element does not support setTag"**. So you can't re-tag the `<nav>` answer panels of an FAQ/accordion built on the Dropdown widget to `<div>` via the API — and a 12-item FAQ then floods the landmark list with a dozen `<nav>`s. Fix in the Designer (Element settings → Tag → Div), or neutralise the landmark with a `role` attribute via `set_attributes`.
- **`<html lang>` / the primary site locale is read-only** through the API (`data_localization_tool` writes only *secondary* locales). Set the site language in **Site Settings → General → Language** and republish — this is the single highest-impact a11y fix (WCAG 3.1.1, one setting fixes every page) and it is Designer-only.
- Interactions (IX2/IX3) → Pitfall 40. A skip-link's "visually-hidden-until-focus" CSS → Designer styling.

**What the Data API CAN do for accessibility (all headless):** add `aria-label` or any attribute — `data_element_tool set_attributes { id:{component,element}, scope_component_id?, attributes:[{name,value}] }` (fix the shared nav/footer component ONCE → it propagates to every page); change a real Heading/Block/Section tag — `data_element_settings_tool set_tag { element_id:{component,element}, static_value:"h3"|"main"|… }` (keep the element's style class so the visual size is unchanged); set `<img>` alt via element settings. **Verify-before-you-fix:** Webflow's runtime JS injects `role=button` / `aria-expanded` / `tabindex` onto its native menu-button and dropdown-toggle, so a raw-HTML "control has no accessible name / not focusable" finding is **partly self-healing with JS on** — still add a static `aria-label`, but confirm the dynamic state in a real browser before treating it as broken.

---

## Part 7 — registered scripts, an iOS-only paint bug & big-rewrite verification (added after a mobile-nav rescue)

### 43. `register_inline_script` is a maintenance trap — prefer an `HtmlEmbed` in the component that owns the behaviour
Registered site scripts (`data_scripts_tool register_inline_script` + `set_site_scripts` / `add_site_script`) look like the tidy way to ship site-wide JS. Four properties make them a poor default, all verified:
- **2000-character cap** on `source_code` (schema-enforced). Real fixes outgrow it fast and you end up code-golfing — shortening identifiers, dropping robustness guards — which is the opposite of maintainable.
- **The site owner cannot find them.** They are not in Site Settings → Custom Code (that page holds the *freeform* head/footer blocks) and not in the Designer. Only the API sees them, so a user who wants to read or tweak "that script you added" is stuck asking you.
- **Applied-script changes need a publish** to reach even staging — `set_site_scripts` alone changes nothing live.
- **They cannot be deleted.** `delete_registered_script` returns **HTTP 400** — tested while applied, while unapplied, and after a fresh publish with nothing applied. The registry is effectively append-only: every version you register stays listed forever. (`get_site_scripts` returning 404 *"Custom code block not found"* is just the **empty** state — nothing applied — not an error.)
**Use instead:** an `HtmlEmbed` inside the component that owns the behaviour (nav JS in the nav component → Pitfall 37 for the call shape). No length limit, visible and editable in the Designer next to the thing it affects, ships wherever the component ships, and deleting the element removes the code. Registered scripts remain reasonable for genuinely global third-party snippets you never intend to hand back to the user. Group by the reader's mental model — if the component already has embeds named `CSS` and `JS`, put CSS with CSS and JS with JS rather than inventing a feature-shaped hybrid; the owner's filing system wins on their own site.

### 44. iOS-only blank panel: a scrollable, absolutely-positioned panel inside a `position:fixed` sheet → portal it
**Symptom:** on a real iPhone a mobile-menu panel renders **blank** — the content is in the DOM with correct geometry, it simply isn't painted. Everything else in the sheet draws fine.
**Not reproducible** in Playwright/headless WebKit, Chrome device mode, or desktop Safari — Pitfall 19's blind spot in its sharpest form. Budget for on-device iteration, or you will keep "fixing" it against a green test suite.
**Cause:** an iOS compositing/paint failure for a scrollable (`overflow-y:auto`), absolutely-positioned child inside a `position:fixed` sheet. **Transforms are not the trigger** — verified by removing them from panel and sheet in turn; nor is opacity, nor forcing a repaint.
**Fix (portal / teleport):** when the panel opens, **move the real element** to `<body>` as `position:fixed` in a clean paint context, sized to the slot it occupied; restore it exactly on close (original parent, original next-sibling, original inline `style`). Move, don't clone — a clone duplicates DOM the owning JS still manages. Compute the slot from **stable neighbours** read fresh each time (e.g. pill-row bottom → CTA top), not from the panel's own cached rect: a cached rect goes stale on devices with a dynamic viewport and the panel then covers the whole screen.
**The tax you must pay back:** once the node leaves its parent, every `parent.querySelector('.child')` in the owning JS silently misses it (`if (!t || !p) return` skips that branch), and anything the JS does to the *sheet* no longer reaches the panel. So far that meant re-asserting "exactly one active tab" yourself, and mirroring the sheet's drag `transform`/`transition` onto the portaled node — mirror by *following* what the sheet does (observe its `style` attribute), never by reimplementing the gesture. **When a new symptom appears in a portaled UI, suspect this class of cause first.**
**Diagnosing without a debugger:** you can't attach devtools to someone else's phone. Ship a temporary gated script (`?diag=1`) that renders the state you need as **text on screen** for the user to screenshot, and a second one that switches between candidate fixes (`A`/`B`/`C` buttons) so a single hand-off tests several hypotheses instead of one.

### 45. A Webflow page serves TWO stylesheets — grep both, and don't read them from JS
**Symptom:** you fetch the page CSS, grep for a rule you know exists, find nothing, and conclude it isn't there (or that some other code owns the value).
**Cause:** the page links **two** sheets — `…webflow.shared.<hash>.min.css` (small, shared) and `…webflow.<siteId>.<hash>.opt.min.css` (large, page-optimised). Taking the first `<link rel=stylesheet>` (the reflexive `head -1`) usually lands on the small one.
**Also:** walking `document.styleSheets[].cssRules` from the page throws `SecurityError` for both — they're served cross-origin from the CDN — so an in-page scan reports "no matching rules" and, if you `catch { continue }`, does it silently.
**Fix:** collect every `<link rel=stylesheet>` href, fetch them all, concatenate, then search — stripping whitespace before matching, since the files are minified (`padding-left:1rem`, not `padding-left: 1rem`). Use the CSS only to find *which rule* supplies a value; for the effective value, `getComputedStyle` in the browser is ground truth. → sharpens Pitfall 21's "fetch the CSS and grep for your rule".
