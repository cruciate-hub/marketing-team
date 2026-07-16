# Worked examples — real before/after diffs

Concrete migrations pulled from real social.plus sessions. Load this when you want a pattern to copy.

---

## A. Split a section-root mega-rule (vars stay in code, properties go native)

Claude emits one giant rule mixing `--var:` definitions with real properties. `--var:` lines must stay in code so descendants inherit them; the properties become Style-panel-adjustable natively.

**Before** (all in head code):
```css
.jp-section {
  --ff: var(--font--figtree, 'Figtree', sans-serif);
  --surface-0: var(--social--dark, #111);
  /* ~25 more --var defs */
  font-family: var(--ff);
  background: var(--surface-0);
  padding: clamp(64px, 9vw, 128px) 0;
  position: relative; overflow: hidden; isolation: isolate;
}
```
**After** — code keeps only the var block:
```css
.jp-section { --ff: var(--font--figtree, 'Figtree', sans-serif); --surface-0: var(--social--dark, #111); /* var defs only */ }
```
**After** — native `.jp-section` Style record: `background-color`→bind `--social--dark`, `font-family`→bind `--font--figtree`, `padding-top/bottom` `clamp(64px,9vw,128px)`, `position:relative`, `overflow:hidden`, `isolation:isolate`. Cascade conflict gone; descendants still resolve the vars.

---

## B. Trim a descendant rule to just its override

The attribute/descendant selector can't be native — keep ONLY that line in code; move layout + base appearance native.

**Before:**
```css
.sp-stage .idx { font-family: var(--ffm); font-size: 18px; font-weight: 600; color: var(--dim);
  border: 1px solid var(--border-soft); border-radius: 8px; width: 36px; height: 36px;
  display: grid; place-items: center; transition: color .4s, border-color .4s, background .4s; }
.sp-stage[aria-current="true"] .idx { color: var(--c); border-color: rgba(255,255,255,.3); background: rgba(255,255,255,.05); }
```
**After** — code keeps only what native can't express:
```css
.sp-stage .idx { color: var(--dim) }
.sp-stage[aria-current="true"] .idx { color: var(--c) }
```
Native `.idx` gets the layout/appearance; the active border+bg move to the combo class the JS toggles. `transition` splits into `transition-property` + `transition-duration` (Webflow stores them separately).

---

## C. Strip a JS injection, rebuild as a native element

**Before** — head script injects a logo at runtime (Designer can't see it):
```js
orb.insertAdjacentHTML('beforeend', '<div class="sp-orb-logo"><svg viewBox="0 0 2500 2500">…</svg></div>');
```
**After** — an `<img>`/HTML-Embed added natively inside the wrapper; the injection block is deleted from the script. Keep the script only for genuine runtime behavior (animation, event handlers). Net: less head JS, Style-panel control, no first-paint duplicate.

---

## D. Resolve a transform-cascade conflict

User set `.sp-nd-active { transform: … scale(1.04) }` natively, but a code rule `.sp-node.is-active { transform: … scale(1.06) }` won on specificity (0,2,0 > 0,1,0).

**Fix** — drop ONLY the `transform` line from the code rule; keep border/shadow/background there (they use per-stage `--c-*` vars from attribute selectors, code-only). Native now wins for `transform`.

---

## E. Make ONE component responsive instead of a mobile-duplicate (2026-07 nav)

**Problem:** a sub-navbar (product tabs: Overview/Features/SDK/…) was `display:none` at `small`, so each product page shipped a separate **"Nav / X / Responsive"** duplicate component (13+13+3+9 = 38 instances). Classic anti-pattern.

**Fix — make the single real component work on mobile, then delete the duplicates:**

1. **Show it + make it a horizontal scroll strip** via native breakpoint styles (`data_style_tool`, `breakpoint_id: "small"`; cascades to `tiny`):
   - `.sub-navbar` → `display:block`, edge geometry.
   - `.sub-navbar_content` → `overflow-x:auto`, `max-width:none`.
2. **Scrollbar hide + a mobile-only tweak** live in the shared CSS **embed** — edited via `data_element_settings_tool set_settings` (key `code`) on the shared "Nav/Sub/CSS" component, so ONE write covers all 48 instances:
   ```css
   @media (max-width:47.9375em){ .sub-navbar_content{scrollbar-width:none} .sub-navbar_content::-webkit-scrollbar{display:none} }
   ```
3. **A dead `<div>` toggle needed behavior** → added to the shared JS embed, but **scoped to mobile with `matchMedia` so tablet/desktop are byte-for-byte unchanged**:
   ```js
   var mq = window.matchMedia('(max-width:47.9375em)');
   toggle.addEventListener('click', function(){ if (mq.matches) location.href = link.getAttribute('href'); });
   ```
4. **Delete the 38 duplicate instances.** The API can't: `unregister_component` errors "Cannot unregister a component that is in use," and there's no bulk instance-delete. → the Webflow **Designer's right-click → Delete Component** removes definition + all instances atomically (and is undoable). Told the user; they did the 4 clicks.

**Why it works:** the real component already has the right links/icons; the responsive treatment is pure CSS/JS on shared classes + shared embeds, so it lands everywhere at once, and desktop/tablet stay untouched because every change is scoped to `small`/`tiny` or guarded by `matchMedia`.

---

## F. Connect a mobile bar to the navbar as one card (2026-07 nav)

**Problem:** the mobile sub-navbar was full-width edge-to-edge while the navbar above it is an *inset floating card* (parent `.nav` has `padding:0 24px`; card has 1px border + 4px radius). The bar stuck out wider on both sides = "an ugly loose bar." Desktop already joins the two into one card.

**Fix — make the bar the bottom half of the navbar card:**
- Subnav `small`: `background:transparent` + `padding-left/right:1.5rem` (insets it to the SAME width as the navbar — verify `getBoundingClientRect().x/right` match).
- Subnav content `small`: restore side + bottom + top 1px borders + `border-bottom-radius:0.25rem` (top radius 0) → it's the rounded bottom of the card; the 1px top border is the row divider (matches desktop).
- Navbar: the "lose your bottom border + bottom corners" rule (in the shared embed) was `@media (min-width:48em)` — made it **unconditional** (safe: that embed only exists on pages that HAVE a subnav, and the subnav now renders at every width).
- Sticky stays gap-0 at rest AND scrolled: subnav sticky `top = navbarHeight + 8`, which equals the navbar's own 8px top offset, so bottoms/tops meet exactly.

**Verify (JS, not screenshots):** `nav.getBoundingClientRect().x === content.getBoundingClientRect().x` and `.right === .right` (aligned), `getComputedStyle(nav).borderBottomWidth === '0px'`, `content.scrollWidth > content.clientWidth` (still scrollable). Screenshot once at the end for the human.
