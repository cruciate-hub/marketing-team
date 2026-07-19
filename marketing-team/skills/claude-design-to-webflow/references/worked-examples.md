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

---

## G. Align a native Navbar to the content container's gutters (native Navbar)

**Problem:** a native Webflow Navbar's logo + hamburger didn't line up with the page content. The nav's padding was hardcoded in the styling embed (`#nav > div{padding:0 64px}` on desktop, `padding:.85rem 1.4rem` on mobile), so it matched content at desktop but drifted at tablet/mobile — and every Style-panel padding edit was silently overridden (Pitfall 36). The logo also rendered *centered* at tablet (the clearfix flex-item trap, Pitfall 35).

**Fix — make the nav container mirror the content container's box-model at every breakpoint:**
1. Kill the clearfix pseudo flex-items so only the real children lay out: `#nav > div::before,#nav > div::after{display:none}` (Pitfall 35).
2. **Measure** the content container's actual responsive padding + max-width (`getComputedStyle` at each breakpoint — don't assume). Here `.page-container` = `max-width:1408px` with padding **64 / 40 / 24 / 20** at **≥992 / ≤991 / ≤767 / ≤479**.
3. Replay those exact values in the embed at Webflow's breakpoints, and give the nav container the same `max-width` so it centres identically on wide screens (Webflow's `.w-container` otherwise caps at 728 ≤991):
   ```css
   #nav > div{max-width:1408px;margin:0 auto}                       /* base — match content width */
   @media (min-width:992px){#nav > div{padding:0 64px}}
   @media (max-width:991px){#nav > div{padding-left:40px;padding-right:40px}}
   @media (max-width:767px){#nav > div{padding-left:24px;padding-right:24px}}
   @media (max-width:479px){#nav > div{padding-left:20px;padding-right:20px}}
   ```

**Verify (JS, not screenshots):** at each breakpoint `logo.getBoundingClientRect().left === h1.left` and the hamburger's `.right` lands on the content's right gutter — the left-delta should be `0` at 1440 / 1280 / 991 / 768 / 767 / 479 / 390. (Then one guide-line screenshot for the human: draw 1-px lines at the gutter x-positions and confirm both the logo edge and the content edge sit on them.)

**Why it works:** the nav no longer owns an independent gutter — it replays the content container's exact responsive padding + width, so logo-left and hamburger-right land on the content margins at every width, and it tracks any later change to the content container. (If you instead want the user to *tweak* the gutter in the Designer, move the padding off the `#nav > div` embed rule and onto a native class per Pitfall 36 — you can't have both the embed override and Style-panel control.)

---

## H. Accessibility / semantic-HTML pass on a Webflow build

**Method:** audit the **published** HTML per page (raw `curl`, because attributes — `alt`, `aria-*`, `role`, `id`, `lang`, `for` — are what matter, not the rendered pixels); fix anything in the shared **nav/footer component ONCE** (it propagates to every page); do the rest per page; re-check heading order + landmarks after. Split each fix into API-doable vs Designer-only up front (Pitfall 42).

**Typical Webflow-build gaps and the fix for each:**

| Gap | Fix | Where |
|---|---|---|
| No `<main>` (content is bare `<section>`s) | wrap the content sections, tag the wrapper `main`, add `id="main"` | API (`set_tag` Block→main) |
| Native menu-button / dropdown-toggle = `<div>`, no accessible name in raw HTML | add `aria-label="Menu openen"` (JS supplies role/aria-expanded at runtime — verify) | API (`set_attributes`) |
| `<nav>` landmarks (main menu + dropdown) unlabelled | `aria-label` each (`Hoofdmenu`, `Voor VA's`) | API (`set_attributes`), in the nav component |
| Webflow Dropdown lists render as `<nav>` → FAQ/accordion floods the landmark list | change the dropdown-list tag to Div | **Designer** — `set_tag` is rejected on the widget (Pitfall 42) |
| Heading-order skip (h2→h4, h1→h3) | re-tag to the correct level, **keep the styling class** so the size is unchanged | API (`set_tag` on the Heading) |
| Decorative `<svg>` not hidden | `aria-hidden="true"` (`focusable="false"`) | API for native elements; **edit the embed code** for SVGs living in an HtmlEmbed |
| `<html lang>` missing | Site Settings → General → Language = the site's language | **Designer/Settings** — primary locale is API-read-only (Pitfall 42) |
| No skip-link | `<a href="#main">…</a>` + a visually-hidden-until-focus class | element is API-doable; the CSS class is **Designer** |

**Real numbers (this pass, 11 pages):** the actual writes were `set_attributes` for three nav `aria-label`s (once in the component → all pages) and `set_tag` for four heading-order corrections (three `h4`→`h3`, one `h3`→`h2`). Already-correct and left untouched: one `<h1>` per page, meaningful `img` alts, form labels, `aria-current`, `prefers-reduced-motion`. The `<html lang>`, the FAQ `<nav>`→Div re-tag, and the skip-link CSS were handed to the human as Designer steps. Don't publish an a11y batch without confirming — a Webflow publish pushes ALL pending site changes.
