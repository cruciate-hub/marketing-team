# social.plus design system

One structure, built from the live website (https://www.social.plus) and kept in step with it: the tokens the site runs on, the foundations a page is made of, the 41 section types with their recipes, and the scripts that capture all of it. Skills read it through [`brain.md`](brain.md); people start with the gallery.

- Gallery (GitHub Pages): https://cruciate-hub.github.io/marketing-team/design-system/sections/index.html (every foundation and section, desktop and mobile; `brand-guidelines.html`, `website/style-guide.html` and `website/sections/index.html` redirect here)
- Router for skills: [`brain.md`](brain.md)
- The section set and the rule: [`sections/README.md`](sections/README.md)
- The capture: [`capture/README.md`](capture/README.md)

## How it is organised

```
design-system/
  README.md               this file
  brain.md                router: what to load for which task (every skill reads it)
  tokens.css, tokens.json the 44 live Webflow variables (+ Figtree @font-face); the JSON adds a use per token
  figtree.woff2           the only font file (social.plus Figtree build; see "Font" below)
  foundations/<name>/     foundation.md (values as measured, rules, known inconsistencies), preview.html (self-contained markup),
                          styles.css (the site's own rules), desktop.png (1440), mobile.png (390)
    colors, typography, spacing, buttons, cards, rich-text, form-inputs, tags, accordion-row, dividers, imagery   captured from the site
    logo, icons, accessibility, shadows-and-radius   written by hand (brand rules and measured values), same files
  sections/README.md      the rule for building pages, the index of the 41 section types, the recipes
  sections/<nn-name>/     section.md (use it when, content slots, allowed variations, accessibility), source.html, styles.css, screenshots;
                          variants with a --<variant> suffix; global/ holds nav, sub-nav, breadcrumb bar, footer CTA band, footer
  sections/recipes/       fixed section order per page type: vs, product page, SDK page, industry page, blog post, answer, glossary entry, customer story
  sections/proposals/     new sections wait here (YYYY-MM-DD-<name>.md) until approved
  sections/index.html     the gallery
  capture/                Playwright capture, foundations builder, verify, gallery, compact-screenshots.py, pack.py (no AI calls)
  brand-guidelines.html   redirect to the gallery (keeps the old public link alive)
  website/                two more redirect stubs (style-guide.html, sections/index.html) for the old public URLs
```

Everything is as the site is today. No team decision from the 7 October 2026 audit has been applied; each `foundation.md` and `section.md` lists its "Known inconsistencies" and marks undecided points "TO CHECK". The logo, icons, imagery, accessibility and shadows-and-radius foundations also carry the brand rules (what to do), separate from the measured values.

## The rule

> Build pages only from the social.plus section set in `sections/` and the foundations in `foundations/`. Use each section as written there: its structure, its content slots and only its allowed variations. Use only the values in `tokens.css`: dark background (`--social--dark`), Figtree from `figtree.woff2` only (never Google Fonts or another source, no `font-feature-settings`; fallback Arial, sans-serif; emails are the exception and follow the email spec), one blue for actions (`--social--main-blue`). Do not invent a new section, text effect, icon style, shadow or colour. If the page needs something the set does not have, stop and propose it: name the section, say what it is for, show one example, and mark it "proposed" in the conversation. A proposed section may be used on the page only after Stefan or Amadeus approves it; then it is added to the set. Follow the page recipes in `sections/recipes/` for the section order. Facts about the product come from `messaging/product-capabilities.md`.

The same text, for pasting into Claude Design, is in `sections/README.md`.

## Font

**Font:** the only font is `figtree.woff2` in this folder: social.plus's own build of Figtree (variable, weights 300 to 900). The single-storey "a" is already the default glyph, so never load Figtree from Google Fonts, the Webflow CDN or any other source, and never add `font-feature-settings`. The file holds basic Latin only; anything else falls back to Arial, sans-serif (`font-family: "Figtree", Arial, sans-serif`). Emails are the exception: they follow the email spec (`emails/product-update-newsletter-spec.md`, Inter with system fallbacks); the Figtree-only rule covers the website and every other visual output.

## Who approves

Changes to the design system (a new section, a changed rule, a decided inconsistency) are approved by Stefan or Amadeus. Until then a section's status line says "draft" and a foundation's "Approved by: TO CHECK".

## How to update

1. **The site changed** (a token, a section, a style): re-run the capture from `capture/` (`node capture.mjs`, then `node foundations.mjs`, `node verify.mjs`, `python3 compact-screenshots.py`). Screenshots, HTML, CSS, `tokens.css` and `tokens.json` are regenerated; `section.md`, `foundation.md` and the hand-made foundations are never overwritten. The tokens diff at the end of `capture/README.md` lists new, changed and gone tokens; give a new token its one-line use in `tokens.json` and the colors foundation; when a token changes, update `marketing-team/skills/claude-design-to-webflow/references/variable-ids.md` (the Webflow variable IDs) with it. Details in [`capture/README.md`](capture/README.md).
2. **A rule changed** (a decision from Stefan or Amadeus): edit the `foundation.md` or `section.md` concerned, remove the item from "Known inconsistencies" or "TO CHECK", and update the status line. Keep "as measured" and "rule" apart.
3. **A new section**: write `sections/proposals/YYYY-MM-DD-<name>.md` (name, purpose, one example); after approval add it to `capture/capture.config.json`, capture it, write its `section.md`, add it to the index in `sections/README.md`.
4. **A new hand-made foundation**: a folder with `foundation.md`, `preview.html` (link `../../tokens.css`, wrap the content in `<main class="fx-page">`, no scripts, images from https), `styles.css`; run `node verify.mjs --only foundations/<name>` for the screenshots and `node gallery.mjs` for the gallery, then `python3 compact-screenshots.py`.
5. **For Claude Design**: `python3 capture/pack.py` assembles the upload pack (tokens, foundations, sections, recipes) in `~/Downloads/socialplus-website-design-system` and zips it.

Commit the regenerated files together with the notes. The capture is read-only towards the site and makes no AI calls.

## History

Until 7 October 2026 this folder held a second, generic design system (22 markdown files from a canonical HTML document, an app UI kit, `website.md` with the Webflow tokens, a brand guidelines page and a style guide). It is gone: what was still true moved into the foundations (logo, icons, imagery, accessibility, shadows and radius, the brand extras in colors); the app UI kit files (avatars, badges, cards, list items, navigation, overlays, feedback, states, empty states) were about the in-app product, not the website, and were removed. The old files are backed up outside the repository.
