# social.plus design system: router

The entry point for every visual task. The design system is built from the live website (captured 7 October 2026): `tokens.css` holds the 44 live Webflow variables, `foundations/` the building blocks with their rules, `sections/` the 41 section types a page is made of, with recipes per page type. Read [`README.md`](README.md) once for the structure; this file tells you what to load for a task.

Files are read from the clone the canonical fetch block makes (`$MT_REPO`, default `/tmp/cruciate-hub-marketing-team`). Paths below are relative to `design-system/`: `cat "$MT_REPO/design-system/<path>"`. Load `brain.md` at the repo root first (cross-domain routing, precedence, the compliance check); when the output contains text, also `messaging/brain.md`.

## Routing

| Task | Load |
|---|---|
| **Any visual task** (always) | `tokens.css` (the values), `foundations/colors/foundation.md`, `foundations/typography/foundation.md`, `foundations/spacing/foundation.md` |
| **A website page or section** (Webflow build, landing page, section mockup, Claude Design prompt, marketing HTML that must match the site) | the always-load files + `sections/README.md` (the rule and the index) + `sections/recipes/<page>.md` for the page type + for every section you use: `sections/<folder>/section.md` and its `source.html` (the live HTML and CSS) + the foundations the section needs (`buttons`, `cards`, `rich-text`, `form-inputs`, `tags`, `accordion-row`, `dividers`, `imagery`) |
| **Blog, answers, glossary and customer story visuals** (header images, in-article figures, thumbnails) | the always-load files + `foundations/imagery/foundation.md` (sizes, blog header rules) + `sections/recipes/blog-post.md`, `answer.md`, `glossary-entry.md` or `customer-story.md` |
| **Emails and newsletters** | the always-load files (the "Brand extras" part of the colors foundation has the email palette and the gradients) + `foundations/logo/foundation.md` (inline SVG) + `foundations/accessibility/foundation.md` (the pairs on white). The email HTML itself comes from the newsletters skill and `emails/` |
| **Social graphics, decks, one-off visuals** | the always-load files (brand extras: gradients) + `foundations/logo/foundation.md` + `foundations/imagery/foundation.md` + `foundations/icons/foundation.md` |
| **Output with the logo** | `foundations/logo/foundation.md` (variants, clear space, backgrounds, SVG data; files in `assets/`) |
| **Output with icons** | `foundations/icons/foundation.md` (the site's inline SVG icons, the two feature-glyph holders, sizes) |
| **Output with images or illustrations** | `foundations/imagery/foundation.md` (ratios, product illustration and photography rules, blog headers) |
| **Buttons, forms, cards, tags, accordions, dividers** | the matching `foundations/<name>/foundation.md` and its `preview.html` for the markup |
| **Shadows, radius, elevation** | `foundations/shadows-and-radius/foundation.md` (measured values, the proposed set marked "to decide") |
| **Accessibility question or check** | `foundations/accessibility/foundation.md` (contrast table of every token pair, focus, targets, motion, keyboard, the open items) |
| **A quick question** ("what blue", "the heading sizes", "the hover colour") | `tokens.css` and the matching `foundation.md`; answer with the token name and the value |
| **Design review or audit** | everything: `tokens.css`, every `foundations/*/foundation.md`, `sections/README.md` and the `section.md` of every section on the page under review. Compare against the measured values and the rules; list what differs |

How to read a foundation: `foundation.md` has the status line (draft until Stefan or Amadeus approves), the values as measured, the rules, and "Known inconsistencies" (true today, not a licence to copy). `preview.html` is the markup to build from; `styles.css` the site's own rules for it; `desktop.png` and `mobile.png` what it looks like.

## Rules

- **Font:** the only font is `figtree.woff2` in this folder: social.plus's own build of Figtree (variable, weights 300 to 900). The single-storey "a" is already the default glyph, so never load Figtree from Google Fonts, the Webflow CDN or any other source, and never add `font-feature-settings`. The file holds basic Latin only; anything else falls back to Arial, sans-serif (`font-family: "Figtree", Arial, sans-serif`).

- **Tokens are law.** Use the exact names and values in `tokens.css` (`var(--social--main-blue)` in CSS, `#3B41EC` where a hex is needed, as in emails). Never approximate. A colour that is not a token is listed in the colors foundation as "not a token" and is not used for new work.
- **Dark-first.** `--social--dark` #111 is the page; raised blocks are `--social--dark-gray-background` #1a1a1a; depth comes from lighter surfaces, not shadows. Light sections use `--social--grey-background` #f9f9f9 or white.
- **One blue for actions.** `--social--main-blue` fills buttons, tags and icon holders; hover `--social--button-hover` #272B9D, pressed `--social--button-pressed` #27265E. The secondary colours decorate and signal status; they never make a call to action.
- **Blue is never text on dark.** `--social--main-blue` on #111 is 2.84:1. Blue text goes on white; on dark the label is white on a blue fill.
- **Only these sections, only these tokens.** Build pages from `sections/` with the recipes. Anything the set does not have is proposed first (name, purpose, one example, marked "proposed") and used only after Stefan or Amadeus approves; then it joins the set. The rule in full is in `sections/README.md`.
- **No new text effects.** Text is one solid colour; no gradient fills, no glows, no new icon style, no new shadow (the measured ones are in the shadows-and-radius foundation).
- **12px is the floor; 44px is the target.** No text under 12px; every interactive element is at least 44px.
- **One primary button per section.**
- **Say what is undecided.** "TO CHECK" in a note means nobody decided yet; "Known inconsistencies" means the site does it today. Neither is a rule to follow; say which you applied.
- **If a load fails** (clone error, missing file, wrong format), follow the fetch block's hard-fail rule. Never work from memorised values.
- **Run the compliance check** from the root `brain.md` before delivering.

## Files

| Path | Contains |
|---|---|
| `README.md` | What the design system is, how it is organised, how to update it |
| `tokens.css`, `tokens.json` | The 44 live Webflow variables (+ Figtree `@font-face`); the JSON adds a one-line use per token |
| `foundations/colors/` | Every token as a swatch with its use; non-token colours regular sections depend on; brand extras for emails and graphics (gradients, light palette) |
| `foundations/typography/` | Figtree, the six heading tokens, body and text classes measured at 1440 and 390, weights |
| `foundations/spacing/` | The five spacing steps, four containers, section rhythm, page gutter, grids |
| `foundations/buttons/` | Primary, secondary, text link, form submit with hover and pressed states |
| `foundations/cards/` | Card v1, v2, v3, plain, thumbnail and story cards |
| `foundations/rich-text/` | Article body styles (blog, answers, glossary, product updates) |
| `foundations/form-inputs/` | Text fields, selects, textarea, checkbox, submit |
| `foundations/tags/` | The `.tag` pill and its variants |
| `foundations/accordion-row/` | FAQ row and feature accordion |
| `foundations/dividers/` | Line and text dividers |
| `foundations/imagery/` | Image ratio classes and the rules for illustrations, photography, blog headers |
| `foundations/logo/` | Logo variants, clear space, backgrounds, inline SVG |
| `foundations/icons/` | The site's icons: inline SVG interface icons, feature glyph holders, sizes |
| `foundations/accessibility/` | Contrast of every token pair, focus, touch targets, motion, keyboard and structure, open items |
| `foundations/shadows-and-radius/` | Radii and shadows the site uses, the proposed set to decide |
| `sections/README.md` | The rule, the index of the 41 section types, the recipes |
| `sections/<nn-name>/` | `section.md`, `source.html`, `styles.css`, screenshots per section type (variants with a `--<variant>` suffix); `global/` for nav, sub-nav, breadcrumb bar, footer CTA band, footer |
| `sections/recipes/` | Section order per page type: vs, product page, SDK page, industry page, blog post, answer, glossary entry, customer story |
| `sections/index.html` | The gallery of every foundation and section (also on GitHub Pages) |
| `capture/` | The scripts that build all of this from the live site (`capture/README.md`) |
