---
name: claude-design-to-webflow
description: Migrating a Claude-generated HTML/CSS/JS prototype to Webflow via the Webflow MCP, or iterating on a previously-Claude-built Webflow section. Use this skill whenever the user pastes HTML/CSS from a Claude artifact and wants a Webflow version, asks to rebuild or redo a section in Webflow, mentions code-vs-native decisions, fixes cascade conflicts between custom head/footer code and native Style records, strips JS-injected static content so Designer can see it, binds hardcoded colors to Webflow variables, troubleshoots Webflow MCP query timeouts, or works on the social.plus MCP Server page (jp-section, sp-workflow, sp-node, sp-stage and their combos). Also use when the user pastes Webflow head or footer code and asks what should move to native, when they ask why a Style-panel change isn't taking effect, when they're choosing between Webflow's breakpoints (992/768/480) and custom @media values, or when they hit anti-patterns like all:unset, hardcoded hex, color-mix() corruption, nth-child(N), or class-fixer IIFEs.
---

# Claude-design → Webflow migration playbook

Captures the lessons from the social.plus MCP Server page session (2026-05) where a Claude HTML prototype was rebuilt in Webflow and we ran into ~14 distinct gotchas, plus patterns adapted from community Webflow-conversion work. The goal: future migrations should never repeat them.

## Core principle

**Native first, code only for what Webflow can't express.** The Designer can represent most CSS — when something is achievable natively, putting it in code creates cascade conflicts that overwrite native edits silently.

## Webflow Connector architecture

You're on the **official Webflow Connector** (`mcp.webflow.com`), launched with the Webflow × Anthropic native connector in Feb 2026. This is the hosted, first-party MCP server — not the older standalone setups some community guides reference.

**Three layers in the stack:**

| Layer | Where | What it does |
|---|---|---|
| Webflow MCP server | `https://mcp.webflow.com/mcp` (hosted) | Exposes Designer + Data APIs as MCP tools |
| Designer Bridge | Inside your active Webflow Designer browser tab | Translates MCP tool calls into Designer canvas operations |
| Webflow Skills plugin | `~/.claude/plugins/` (from `github.com/webflow/webflow-skills`) | 18 official workflows: `safe-publish`, `cms-best-practices`, `custom-code-management`, etc. |

**Critical operational detail:** the Webflow Designer browser tab MUST be **active and focused**. Background, idle, or closed → MCP tool calls time out. If you see "tool call timed out, please check Webflow Designer MCP app is running on Webflow Designer", that's the Designer Bridge of this same architecture (not a separate older system) — ask the user to focus the Designer tab and retry. No setup work needed mid-session; if the user is running migrations, the Connector is already wired up.

## Decision rule — native vs code

### Native (Webflow Style record)
- Single-class rules with property declarations: `.jp-bar { padding: 10px; background: … }`
- Combo classes (`.sp-node` + `.sp-nd-build`) via `parent_style_names`
- Pseudo states the API supports: `:hover`, `:focus`, `:focus-visible`, `:active`, `:pressed`, `::before`, `::after`, `:nth-child(odd/even)`, `:first-child`, `:last-child`, `:focus-within`, `:visited`, `:empty`, `::placeholder`
- Webflow's standard breakpoints: xxl (1920+), xl (1440+), large (1280+), main (≥992), medium (<992), small (<768), tiny (<480)
- Variable bindings (`variable_as_value`) for color/font/size tokens

### Code (Site Settings → Head, or Page Settings → Footer)
- `@keyframes`, `@property`
- Descendant selectors (`.jp-bar .title`)
- Attribute selectors (`[data-stage="build"]`, `[aria-current="true"]`)
- `:nth-child(N)` (specific number) — Webflow only supports odd/even/first/last
- Custom media queries with non-standard breakpoints
- `prefers-reduced-motion`, other feature queries
- `color-mix()` — Designer can corrupt these on save (see Pitfall #4)
- Section-root CSS custom property definitions that descendants inherit (`--ff: var(--font--figtree, …)`)
- JS behavior (event listeners, state transitions, animation loops)

## Anti-pattern catalog — what Claude's HTML prototypes typically emit

When the user hands you a Claude-generated HTML/CSS prototype, these patterns appear constantly. Recognize them on the way in, plan migrations on the way out.

### A1. Section-root mega-rule mixing vars and properties
**Typical:**
```css
.jp-section {
  --ff: var(--font--figtree, 'Figtree', sans-serif);
  --surface-0: var(--social--dark, #111);
  /* …20+ more --var defs… */
  font-family: var(--ff);
  background: var(--surface-0);
  padding: clamp(64px, 9vw, 128px) 0;
  position: relative;
  overflow: hidden;
  isolation: isolate;
}
```
**Migration:** split into two halves. Code keeps only the `--var:` lines (descendants inherit them). Native receives the property declarations, with `font-family`/`color`/`background-color` bound to brand variables.

### A2. `all: unset` on every interactive element
**Typical:** `.jp-pip { all: unset; display: grid; … }`
**Migration:** `all: unset` wipes inherited properties within the rule and overrides native via cascade. Either set specific resets natively (`background: transparent; border-width: 0; padding: 0; font-family: inherit`) or accept the rule stays in code (loses Style-panel adjustability for that single class).

### A3. Hardcoded brand-color hex values
**Typical:** `background: linear-gradient(135deg, #45A5ED, #5C6EF8, #3B41EC)`, `background: #FF305A`.
**Migration:** wrap in `var(--token, hex-fallback)` for code, bind via `variable_as_value` for native. See the variable ID appendix at the bottom of this skill.

### A4. Custom @media breakpoints (1200/980/720/560/520)
**Typical:** `@media (max-width: 1200px) { … }`
**Migration:** Webflow's native breakpoints are 1920/1440/1280/992/768/480. Either round to the nearest (1200→1280, 720→768, 520→480) and move responsive properties into Style-panel breakpoint values, OR keep the @media block in code unchanged. Pick per-block based on how cleanly the design maps.

### A5. JS-injected static content
**Typical:** an IIFE that runs `orb.insertAdjacentHTML('beforeend', '<div class="logo"><svg>…</svg></div>')` on DOM ready.
**Migration:** Designer can't see runtime-injected elements. Rebuild static visual content as native elements (HTML Embed for inline SVG, Image element for assets, Heading/Paragraph for text). Keep the IIFE only if it also does runtime behavior (animation, event handlers, dynamic updates) — strip the injection block.

### A6. `:nth-child(N)` for specific positions
**Typical:**
```css
.jp-lights span:nth-child(1) { background: red }
.sp-stage:nth-child(1) { --c: var(--build) }
```
**Migration:** Webflow's API supports `nth-child(odd/even)`, `first-child`, `last-child` — not specific numbers. Either keep in code, or refactor to distinct classes (`.jp-light-red`, `.sp-stg-build`) that ARE native-addressable. The class refactor is usually worth it for Style-panel adjustability per item.

### A7. `color-mix(in srgb, currentColor X%, transparent)`
**Typical:** active-state shadows that tint by the current text color.
**Migration:** Webflow Designer's serializer mangles these on save — stored value comes back as garbage like `pxpxpxpxpx black`. Keep `color-mix()` in code only. If you must store one natively, set once via API and never touch it in Style panel afterwards.

### A8. Class-fixer JS that injects classes by DOM position
**Typical:** an IIFE that walks `.sp-stage` children and `classList.add('idx')` / `.add('label')` / `.add('sub')` based on positional indexes.
**Migration:** Designer doesn't track these runtime classes — Style Selectors panel reports them as orphan styles even though CSS works at runtime. Best path: restructure HTML to put the classes directly on elements, drop the fixer. If you must keep the fixer, document which classes it adds so future Style-panel work doesn't get confused.

### A9. Mobile horizontal overflow from unconstrained children
**Typical:** Claude's prototype previews look fine because the local viewport is desktop-width, but on real mobile the page scrolls sideways because some descendant (a wide gradient, an absolute-positioned element, a `width: 100vw` block inside a padded container) overflows the body.
**Migration:** add `body { overflow-x: hidden; max-width: 100vw }` natively via Webflow's "Body (All Pages)" Style record, or as a single line in Site Settings → Head. Don't wait until QA on the published `.io` URL to discover this — set it preemptively.

## The 14 pitfalls (and how to avoid each)

### 1. Code rules silently override native records
**Symptom:** You set a property in the Webflow Style panel, but the page renders the old value.
**Cause:** Site Settings → Custom Code → Head loads **after** Webflow's compiled CSS. For same specificity, code wins by cascade order.
**Fix:** When migrating a rule to native, **delete it from code**. Don't leave duplicates "for safety" — they actively break Style-panel adjustability.

### 2. Native records for classes no element uses
**Symptom:** Webflow's Style Selectors panel says "X styles not associated with any page elements".
**Cause:** The original Claude CSS referenced classes (e.g., `.jp-eyebrow`, `.sp-title`) that the actual elements never had — the design used Webflow's built-in heading/paragraph styles instead.
**Fix:** Before `create_style`, verify usage:

```
element_tool query_elements → element_filter.style: "class-name"
```

If `total_matches: 0`, don't create the record. If user already created orphans, Webflow's "Clean up" panel is safe.

### 3. JS-injected content is invisible to the Designer
**Symptom:** Element renders on the live page but Designer's element tree doesn't show it; Style panel can't reach it.
**Cause:** Prototype scripts often use `insertAdjacentHTML`, `innerHTML`, `appendChild` to inject markup. Designer only tracks elements in its own tree.
**Fix:** For **static content** that should be editable in Designer:
- Logos / illustrations → HTML Embed with inline SVG, or Image element with uploaded asset
- Headings/paragraphs → Webflow Heading/Paragraph elements
- Cards/wrappers → Div Block

**Only** use JS for *behavior* — event listeners, animation state, dynamic content updates. Never for injecting visible static structure.

### 4. `color-mix()` gets corrupted on save
**Symptom:** Native box-shadow / background-color reads as `pxpxpxpxpxpxpx black` (or similar garbage) after editing in Style panel.
**Cause:** Webflow's serializer mangles `color-mix(in srgb, currentColor X%, transparent)` when re-saving the property through the Designer UI.
**Fix:**
- For static colors → use plain rgba or hex
- For dynamic per-stage tints → keep `color-mix()` **in code only**, where you control the literal string
- If you must put `color-mix()` natively, **don't edit that property in Style panel** afterwards

### 5. Custom CSS breakpoints don't map to Webflow's
**Symptom:** Layout works in Claude's HTML preview but breaks in Webflow Designer's responsive view.
**Cause:** Claude often emits `@media (max-width: 1200px)`, `(max-width: 720px)`, `(max-width: 520px)`. Webflow's native breakpoints are 1920/1440/1280/**992**/**768**/**480**.
**Fix:** Two strategies — pick one per breakpoint:
1. **Round to Webflow's**: change `1200` → use `large` (≥1280) or just `<992 medium`. Move properties into Style panel's breakpoint values. Lose precision, gain Designer adjustability.
2. **Keep in code**: leave the original `@media (max-width: 1200px)` block in the head. Used when the design rules don't map cleanly. Lose Style-panel adjustability for those rules.

### 6. Combo-class cascade is brittle
**Symptom:** Two single-class records on the same element (e.g., `.idx` + `.sp-idx-build`) fight for the same property — color flips depending on which Webflow emits first.
**Cause:** Same specificity (0,1,0), order in compiled CSS decides.
**Fix:**
- Put base properties on ONE class (the more generic one).
- Combo classes should override **only the variant property** (e.g., `color` per stage).
- If both must set the same property, enforce via a higher-specificity descendant code rule (`.sp-stage .idx { color: var(--dim) }`).

### 7. `all: unset` interferes with native
**Symptom:** Button (or other interactive element) ignores native style record values.
**Cause:** `all: unset` in code resets all properties to inherit/initial for that rule, defeating the Webflow-compiled cascade.
**Fix:** Avoid `all: unset` when possible. Set specific resets natively instead: `background: transparent; border-width: 0; padding: 0; font-family: inherit`. If `all: unset` is truly needed (e.g., third-party UI library), keep it in code and accept that single class isn't Style-panel adjustable.

### 8. Duplicated `--variable` definitions
**Symptom:** Section-scoped vars (`--ff`, `--surface-0`) don't resolve to brand tokens.
**Fix:** Define each custom property in exactly ONE place — the section-root code rule (e.g., `.sp-workflow { --ff: var(--font--figtree, …); --surface-0: var(--social--dark, …); }`). Descendants inherit. Pattern: `var(--brand-token, fallback)` — always include the literal fallback.

### 9. Native query timeouts
**Symptom:** `style_tool query_styles` with `include_all_breakpoints: true` returns "tool call timed out".
**Causes:** (a) Webflow Designer tab is in the background, (b) too many classes queried at once with all-breakpoints.
**Fix:**
- Ensure the Designer tab is **active and focused** before MCP calls
- Query without `include_all_breakpoints` first (gets main breakpoint only — usually enough)
- If breakpoint values needed, query one or two classes at a time

### 10. Forgetting to publish — native changes don't show
**Symptom:** API style updates succeed but the live `.io` URL still shows old styles.
**Fix:** Native changes only ship at publish time. Workflow:
1. API style updates → stored in Webflow Designer
2. Code paste (head/footer) → stored in Custom Code
3. **Publish to `.webflow.io`** → both ship live (`publishToWebflowSubdomain: true`, no custom domain)

Production custom domain only on **explicit user go-ahead**.

### 11. Site Settings & Page Settings Custom Code are not API-readable
**Symptom:** `get_page_script` / `list_applied_scripts` return 404 or empty.
**Cause:** The Designer Custom Code panels (Site Settings → Head/Footer; Page Settings → Head/Footer) are **not exposed** by the Webflow Data API. Only App-registered scripts (which appear under "Code added by Apps") are accessible.
**Fix:** **Always snapshot the current code locally before iterating.** Ask the user to paste the contents into a working file. Build versioned working files (e.g., `site-head-v2.html`, `page-footer-v2.html`) that the user pastes back when ready. Never rely on being able to read current state through the API.

### 12. Class-fixer JS still does runtime adds — Designer can't see them
**Symptom:** Classes like `idx`, `caret`, `pip`, `bot`, `heading` show up in the rendered DOM but Webflow Designer shows different (or no) classes.
**Cause:** Claude-generated prototypes often include a "class-fixer" IIFE that walks the DOM and `.classList.add(…)` based on positional rules.
**Fix (depends on intent):**
- If Designer adjustability matters → restructure the prototype to put classes in HTML directly, drop the fixer
- If you keep the fixer → document which classes it adds, so future edits don't break selector assumptions
- Either way: **don't rely on Designer's Style Selectors panel** for class-fixer-added classes; they'll appear "unused" but the runtime class is real

### 13. Custom JS runs before Webflow's runtime is initialized
**Symptom:** Console errors like `Webflow is undefined`, or interactions break on the published page (but work in the Designer canvas, where the runtime is always present). Race condition between your IIFE and Webflow's bundled JS.
**Cause:** Claude prototypes typically use plain `(() => { … })()` IIFEs that fire at script-parse time. On the published site, Webflow's IX2/runtime script may still be loading.
**Fix:** wrap any IIFE that needs Webflow's runtime (or just runs alongside Webflow interactions) in `Webflow.push()`:
```js
window.Webflow = window.Webflow || [];
window.Webflow.push(() => {
  // your IIFE body here
});
```
For local Claude-artifact preview where there's no Webflow runtime, the `window.Webflow ||= []` shim makes `.push()` a harmless `Array.prototype.push` call — your code still runs. In production, Webflow replaces the array with its real implementation and invokes the callback when ready.

### 14. Designer canvas renders animations differently than the published page
**Symptom:** ScrollTrigger / IntersectionObserver / scroll-driven animations look fine on `.webflow.io` but stutter, freeze, or show ghost positions inside the Webflow Designer canvas — making it hard to design with the section live-loaded.
**Cause:** The Designer canvas loads pages in an iframe with non-standard scroll and resize semantics. Code that watches `window.scroll` or uses viewport-relative measurements gets confused.
**Fix:** detect Designer mode and short-circuit to a static "final-frame" render:
```js
const inDesigner =
  !!document.documentElement.classList.contains('w-editor') ||
  (window.self !== window.top); // iframe = Designer canvas
if (inDesigner) {
  // apply the static "rest" state and bail — no animation loops
  setActive(0);
  return;
}
// normal animation setup below
```
The Designer marks `<html>` with class `w-editor` while you're editing. Tune the predicate to your needs (some setups also check the parent's origin).

## Pre-flight checklist (do these before touching anything)

1. **Backup** current head + footer code locally — paste into versioned files in a `backups/<date>/` folder. The API can't read these.
2. **Inventory variables** — `variable_tool query_variables` for `Color`, `FontFamily`, `Size`. Build a name→ID map (need IDs for `variable_as_value`). For social.plus, the appendix below has the IDs pre-mapped.
3. **Inventory existing native styles** — `style_tool query_styles` with `name_path: ["prefix-"]`. Note what already exists.
4. **Verify class usage** — `element_tool query_elements` with `element_filter.style: "name"` for any class you plan to `create_style` for. Skip orphans.
5. **Map breakpoint strategy** — for each `@media` in the prototype, decide: round to Webflow native (lose precision, gain adjustability) or keep in code (keep precision, lose adjustability).
6. **Identify JS-injected static content** — anything Designer should be able to edit → plan to rebuild as native elements.

## Migration playbook (step-by-step)

### Step 1: Categorize each CSS rule
- **Native-eligible**: single class, simple properties → `update_style` or `create_style`
- **Code-only**: keyframes / pseudo / descendant / attribute / custom-media / `prefers-reduced-motion` → keep in code
- **Hybrid**: section-root rule with `--var` definitions → keep root rule in code, migrate `font-family`/`color`/`background`/`padding` to native

### Step 2: Bind variables natively
Use `variable_as_value` (not literal hex) when the value matches a brand token. Brand catalog for social.plus:
- Colors: `--social--main-blue`, `--social--dark`, `--social--grey`, `--social--light-grey`, `--social--dark-gray-background`, `--secondary--green/yellow/pink/orange/red/purple`, `--gradient--light-blue/medium-blue/dark-blue`, `--main--white`, `--text--text-color-grey-light/medium/dark`
- Fonts: `--font--figtree` (no monospace token — use static `ui-monospace, monospace`)
- Always include literal fallback in code: `var(--social--main-blue, #3B41EC)`

### Step 3: Rebuild static content natively
For each piece of JS-injected static content, replace with a Designer element. Common ones:
- Logo SVG → HTML Embed inside the orb wrapper, or Image element
- Star/icon SVGs → HTML Embeds with the inline SVG
- Card text → Webflow Heading/Paragraph/Div Block

Keep JS only for: orbit ring updates, comet rotation, beam line endpoint, scene cycling, typing animation, IntersectionObserver gating.

### Step 4: Apply native styles
Batch via `style_tool` actions array:
```
[
  { update_style: { style_name: "...", properties: [{ property_name: "color", variable_as_value: "variable-id" }] } },
  { update_style: { style_name: "...", properties: [{ property_name: "transition-property", property_value: "transform, border-color, ..." }, ...], remove_properties: ["transition"] } },
  { create_style: { name: "new-class", properties: [...] } }
]
```

### Step 5: Trim the code block
- Strip every rule that's now native (cascade conflicts are the #1 killer)
- Replace remaining static colors with `var(--token, fallback)`
- Keep: section-root with `--var` definitions, keyframes, pseudo/attribute/descendant rules, custom @media queries, `prefers-reduced-motion`
- Save versioned working file (`site-head-v2.html`, `page-footer-v2.html`)

### Step 6: Publish to staging
1. User pastes versioned files into Site Settings → Head and Page Settings → Footer
2. User publishes to **`.webflow.io` only**
3. Iterate by editing the working file + native styles; user re-pastes + re-publishes
4. Production custom domain ONLY on explicit user go-ahead

## Worked examples (real before/after from the social.plus session)

### Example A: splitting a section-root mega-rule

**BEFORE** — everything in head code:
```css
.jp-section {
  --ff: var(--font--figtree, 'Figtree', sans-serif);
  --surface-0: var(--social--dark, #111);
  /* ~25 more --var defs */
  font-family: var(--ff);
  color: var(--text);
  background: var(--surface-0);
  padding: clamp(64px, 9vw, var(--space-12)) 0;
  position: relative;
  overflow: hidden;
  isolation: isolate;
}
```

**AFTER** — code keeps only the var definitions:
```css
.jp-section {
  --ff: var(--font--figtree, 'Figtree', sans-serif);
  --surface-0: var(--social--dark, #111);
  /* var defs only */
}
```

**AFTER** — native `.jp-section` Style record holds:
- `background-color` → bound to `--social--dark`
- `color` → bound to `--main--white`
- `font-family` → bound to `--font--figtree`
- `padding-top` / `padding-bottom` → `clamp(64px, 9vw, 128px)` (static)
- `position: relative`, `overflow: hidden`, `isolation: isolate`

**Why this works:** `--var:` definitions stay accessible to descendants via CSS inheritance. The section's own properties become Style-panel adjustable. Cascade conflict eliminated.

### Example B: descendant rule trimmed to just the override

**BEFORE:**
```css
.sp-stage .idx {
  font-family: var(--ffm);
  font-size: 18px;
  font-weight: 600;
  color: var(--dim);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-2);
  width: 36px;
  height: 36px;
  display: grid;
  place-items: center;
  transition: color 0.4s, border-color 0.4s, background 0.4s;
}
.sp-stage[aria-current="true"] .idx {
  color: var(--c);
  border-color: rgba(255,255,255,0.3);
  background: rgba(255,255,255,0.05);
}
```

**AFTER** — code keeps only what native can't express:
```css
.sp-stage .idx { color: var(--dim) }
.sp-stage[aria-current="true"] .idx { color: var(--c) }
```

**AFTER** — native `.idx` Style record gets the layout + base appearance:
- `font-family: ui-monospace, monospace`, `font-size: 18px`, `font-weight: 600`
- `width: 36px`, `height: 36px`, `display: grid`, `place-items: center`
- `border: 1px solid rgba(255,255,255,0.12)`, `border-radius: 8px`
- `transition-property: color, border-color, background`, `transition-duration: 0.4s`
- `color` → bound to `--text--text-color-grey-light`

Active-state `border-color` + `background` move to native `.sp-idx-current` (the combo the JS toggles).

**Why this works:** the descendant attribute selector (`[aria-current="true"] .idx`) can't be native, so the active-color override stays in code. Everything else — layout, base appearance, base color — becomes Style-panel adjustable.

### Example C: stripping a JS injection

**BEFORE** — head script injects logo at runtime:
```js
var orb = o.querySelector('.sp-orb');
if (orb && !orb.querySelector('.sp-orb-logo')) {
  orb.insertAdjacentHTML('beforeend',
    '<div class="sp-orb-logo"><svg viewBox="0 0 2500 2500">…</svg></div>'
  );
}
```

**AFTER** — user adds an `<img>` natively inside the mask via Webflow Designer:
```html
<div class="sp-aurora-soft-mask">
  <img src="https://cdn.prod.website-files.com/.../mcp-glyph.svg"
       class="sp-orb-logo-glyph" alt="">
</div>
```

**AFTER** — head script: the entire injection block is deleted. Star SVG injection and spark span creation stay (those still need runtime work).

**Why this works:** static visual content belongs in HTML so Designer can manage it. JS keeps its role for *behavior* (animations, state). Net win: ~1.5 KB less head script, native Style-panel control over logo size/position, no duplicate logo on first render.

### Example D: resolving a transform-cascade conflict

**BEFORE** — code rule overrode the user's native scale value:
```css
.sp-node.is-active {
  transform: translate(-50%, -50%) scale(1.06);
  border-color: var(--c);
  box-shadow: 0 20px 48px -16px var(--c-shadow), 0 0 48px var(--c-shadow-soft);
  background: var(--c-bg);
}
```
User had set `.sp-nd-active { transform: translate(-50%,-50%) scale(1.04) }` natively, but code's higher specificity (`.sp-node.is-active` is 0,2,0 vs native's 0,1,0) made code win.

**AFTER** — code rule loses just the transform line:
```css
.sp-node.is-active {
  border-color: var(--c);
  box-shadow: 0 20px 48px -16px var(--c-shadow), 0 0 48px var(--c-shadow-soft);
  background: var(--c-bg);
}
```

**Why this works:** native `.sp-nd-active` now wins for `transform`. Border/shadow/background stay in code because they use the local `--c-shadow`/`--c-bg` vars defined per `[data-stage="X"]` (attribute selectors, code-only).

## Webflow MCP cheatsheet

| Task | API call |
|---|---|
| List colors | `variable_tool query_variables` with `type: "Color"` |
| List size/font vars | same, `type: "Size"` / `"FontFamily"` |
| Find native classes by prefix | `style_tool query_styles` with `name_path: ["sp-"]` |
| Check class is on any element | `element_tool query_elements` with `element_filter.style: "name"` |
| Update existing native | `style_tool update_style` |
| Bind property to variable | `update_style` with `variable_as_value: "variable-id"` |
| Remove a property | `update_style` with `remove_properties: ["name"]` |
| Create new class | `style_tool create_style` (optional `parent_style_names` for combo) |
| Read footer/head code | NOT EXPOSED — paste-by-hand |
| Publish | `data_sites_tool publish_site` with `publishToWebflowSubdomain: true` (custom domain only with explicit go-ahead) |

## When NOT to use this skill

- Pure Webflow-only work (no Claude prototype as input) — use generic Webflow skills instead
- One-off CSS tweaks to an existing Webflow page (no migration involved)
- Pure Claude artifact iteration without a Webflow target

---

## Appendix: social.plus Webflow variable IDs

Pre-mapped variable IDs from the social.plus site (`66e2765d540e1939a89db4bb`). Use these directly in `update_style` calls' `variable_as_value` field — saves a round-trip per session.

If the site's variables get renamed or rebuilt, re-run `variable_tool query_variables` and update this table.

### Site identity

| Field | Value |
|---|---|
| Site ID | `66e2765d540e1939a89db4bb` |
| Staging URL | `https://social-plus.webflow.io` |
| Production URL | `https://www.social.plus` |
| Designer URL | `https://social-plus.design.webflow.com` |

### Colors

| Variable name | CSS name | Resolved value | Variable ID |
|---|---|---|---|
| Main / White | `--main--white` | white | `variable-64679256` |
| Main / Whitesmoke | `--main--whitesmoke` | whitesmoke | `variable-64b3418a-aee4-0527-65cd-08e01561063f` |
| Main / Transparant | `--main--transparant` | rgba(0,0,0,0) | `variable-db517b61-7872-ac88-bdfa-14051268d017` |
| Social+ / Dark | `--social--dark` | #111 | `variable-4b9c57ec` |
| Social+ / Grey | `--social--grey` | #222 | `variable-93f1af9a-ee0a-62f6-5fb2-ce43081d7eda` |
| Social+ / Light Grey | `--social--light-grey` | #444 | `variable-a08161c0-23fb-489b-eebf-f535db04ade6` |
| Social+ / Main Blue | `--social--main-blue` | #3b41ec | `variable-90f1b4a4` |
| Social+ / Button Hover | `--social--button-hover` | #272b9d | `variable-7d4fe31d-0948-1b55-a84b-21deba3e4a6b` |
| Social+ / Button Pressed | `--social--button-pressed` | #27265e | `variable-8012071c-6fc9-c9a8-525f-c192cee5618b` |
| Social+ / Grey - Background | `--social--grey-background` | #f9f9f9 | `variable-f3ca0706` |
| Social+ / Dark Gray - Background | `--social--dark-gray-background` | #1a1a1a | `variable-0531ab56-9952-a6da-1c2c-8262ee55d79f` |
| Social+ / Blue - Transparent | `--social--blue-transparent` | rgba(42,49,233,0.1) | `variable-a1df43dd-b4b0-8263-c5e4-f38eb4513a63` |
| Border / Med Grey | `--border--border-med-grey` | #d0d0d1 | `variable-1ebfe481` |
| Border / Light Grey | `--border--border-light-grey` | #e7e7e7 | `variable-e1e41c15-557c-5595-6f23-7e4c9178fd09` |
| Border / Dark Grey | `--border--border-dark-grey` | #666 | `variable-c5053a4c-e7fa-05c0-7283-5ef0a55c0e29` |
| Border / Dark | `--border--border-dark` | #232324 | `variable-ee98de1f-5b66-8a8d-2010-ae0db98dd8e9` |
| Border / Hover | `--border--border-hover` | #39393a | `variable-2c99aafc-aeb3-0ebc-3d92-c92e7891f273` |
| Secondary / Green | `--secondary--green` | #1dc497 | `variable-18f1dead-7525-dd3f-bdd3-7cd00945b38c` |
| Secondary / Yellow | `--secondary--yellow` | #f7c506 | `variable-07fd785f` |
| Secondary / Red | `--secondary--red` | #ff305a | `variable-d9410529` |
| Secondary / Orange | `--secondary--orange` | #ff6937 | `variable-f5e53ba8` |
| Secondary / Purple | `--secondary--purple` | #9f72ff | `variable-9af8501e` |
| Secondary / Pink | `--secondary--pink` | #f568f0 | `variable-3e1afd9e-e8c4-70f8-a2d3-be13897db84e` |
| Secondary / menu-bg | `--secondary--menu-bg` | #181818 | `variable-e58813e9-3707-fe97-0d83-e8ebd9babe88` |
| Text / Grey Light | `--text--text-color-grey-light` | #b3b3b3 | `variable-fe935cb0` |
| Text / Grey Medium | `--text--text-color-grey-medium` | #717275 | `variable-40c37db5` |
| Text / Grey Dark | `--text--text-color-grey-dark` | #414347 | `variable-69de6259-0e11-0c77-68bb-b61792bb5111` |
| Text / Dark | `--text--text-color-dark` | #111 | `variable-ff7e9502` |
| Gradient / Light Blue | `--gradient--light-blue` | #45a5ed | `variable-27b4895e-439b-ad85-273f-1cab7a1c66dd` |
| Gradient / Medium Blue | `--gradient--medium-blue` | #3769ec | `variable-9d2daeaf-7873-d545-1df4-c1f6bbdd293f` |
| Gradient / Dark Blue | `--gradient--dark-blue` | (refs Main Blue) | `variable-21c7e8f0-11db-ff41-5442-73fa0b30e44b` |

### Fonts

| Variable name | CSS name | Variable ID |
|---|---|---|
| Font / Figtree | `--font--figtree` | `variable-349b794c-a39f-b897-5ec6-dcc9abc79896` |

*No monospace variable exists — use static `ui-monospace, monospace` for code-style fonts.*

### Sizes

| Variable name | CSS name | Resolved value | Variable ID |
|---|---|---|---|
| CTA button icon size | `--cta-button_icon-size` | 1.75rem | `variable-908831f1-6b53-3941-0c6a-a6f11bfeaa5a` |
| H1 font-size | `--_typography---h1-font-size` | clamp(2.75rem, 1.5rem + 2svw, 5rem) | `variable-a8a20bf7-5527-65d0-d6f2-13a566cde28f` |
| H2 font-size | `--_typography---h2-font-size` | clamp(2.25rem, 1.5rem + 2svw, 3.25rem) | `variable-a5470ceb-ca75-3139-a1a5-75465e71c1d2` |
| H3 font-size | `--_typography---h3-font-size` | clamp(1.75rem, 1rem + 2svw, 2.25rem) | `variable-bae162a2-2440-1569-6548-bcdea4b7d040` |
| H4 font-size | `--_typography---h4-font-size` | clamp(1.5rem, 0.875rem + 2svw, 1.75rem) | `variable-58495678-3e36-43ed-7f9c-e2f27035eb9d` |
| H5 font-size | `--_typography---h5-font-size` | 1.25rem | `variable-09545625-e631-25f7-8e80-69a6f1657a38` |
| H6 font-size | `--_typography---h6-font-size` | 1.125rem | `variable-c49a7ca3-a0e4-72a0-c2c7-8f944dfc0734` |
