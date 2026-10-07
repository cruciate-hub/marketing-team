# capture

Playwright scripts that capture the foundations and the sections of the live social.plus website for the design system in `design-system/`. **No AI calls**: the scripts only load the public site, read its HTML and CSS, and take screenshots. Everything that reads or writes Claude Design runs in Claude Code or Claude Design on a person's own seat.

Read-only towards the site: analytics, consent, form, video-host and anti-bot requests are blocked (`blockRequests` in the config); pages are loaded one after the other with a pause between them. Nothing is written to Webflow, Figma, GitHub or Claude Design.

## How to run

```sh
cd design-system/capture
npm install                       # playwright, prettier, pixelmatch, pngjs
npx playwright install chromium   # once per machine
node capture.mjs                  # all sections and snippets in capture.config.json (22 pages, about 25 minutes)
node capture.mjs --page chat      # one page (its sections and snippets)
node capture.mjs --only 11-two-column--image-left
node foundations.mjs              # builds foundations/<name>/preview.html from the snippets
node verify.mjs                   # opens every source.html and preview.html, compares with the live screenshots, writes raw/verify/report.md
node gallery.mjs                  # sections/index.html (capture.mjs also writes it at the end of a full run)
node localize-media.mjs           # images into ../assets/media/ and the references rewritten (capture.mjs and foundations.mjs run it at the end; --prune, --refresh)
python3 compact-screenshots.py    # before every commit: screenshots at 1440/390 wide, 256-colour palette (keeps the public repo small)
python3 pack.py                   # assembles the upload pack in ~/Downloads/socialplus-website-design-system (+ .zip), screenshots at 1x
```

Needs Node 20 or newer; `pack.py` and `compact-screenshots.py` need Python 3 with Pillow; `localize-media.mjs` needs `ffmpeg` on the PATH for the video stills (without it the run says so and the video gets no poster). Screenshots are taken at 1x (`deviceScaleFactor: 1` in `capture.config.json`) so the committed files and the check in `verify.mjs` use the same size.

## What `capture.mjs` does

Driven by `capture.config.json` (pages, sections, snippets, selectors, per-section static-state CSS). To add a section, a variant or a snippet, add an entry there; the script needs no change. A section id is `<folder>` or `<folder>--<variant>`; a variant's files get the `--<variant>` suffix inside the same folder and share the folder's `section.md`.

1. **Setup.** Headless Chromium, 2x device scale, `en-US`, `Europe/Amsterdam`. Two contexts: desktop 1440x900 and mobile 390x844 (iPhone user agent, touch). Reduced motion and dark colour scheme are emulated; the site's own switch hides the announcement bar. Stylesheets are fetched once per URL and cached in `raw/css/`: the shared Webflow sheet and the per-page sheet (Webflow emits one per page).
2. **Load and settle each page.** Wait for network idle and for Webflow, GSAP and ScrollTrigger; scroll the whole page down and up; load every image eagerly and swap `src` for the largest `srcset` candidate; pause videos; run GSAP to its end state and stop it; remove the inline styles the scripts left behind (opacity, transform, visibility, height); remove the announcement bar, consent nodes, pop-ups and form state blocks.
3. **Resolve each section** to exactly one element: a CSS selector (with optional `selectorIndex` and `containsText`) or an `h1`/`h2` text match (`headingText`, with optional `headingSelector` and `closest`, default `section`). The chosen element's tag, classes and first words are logged. Then the section's static-state CSS is injected (for example "show the first story").
4. **Screenshots** of the section element at both widths (`desktop.png`, `mobile.png`); the sticky chrome (nav, sub-nav) is hidden while other sections are shot. Full-page screenshots and the settled HTML of each page go to `raw/` (gitignored).
5. **HTML.** A clone of the section is cleaned: scripts, iframes, hidden inputs, tracking and Webflow runtime attributes, hash ids, inline styles and consent hooks are removed; links, image and poster sources are made absolute (step 9 then makes the media local); videos lose `autoplay`; Webflow's `<link rel=prefetch>` elements are dropped; the `w-dyn-*` and `w-embed` wrappers stay because the site's CSS targets them.
6. **CSS.** The shared sheet, the page's own sheet and the page's `<style>` embeds outside the section are parsed in Node (`css-rules.mjs`); every rule whose selector matches an element in the section is kept, as written (hex, `clamp()`, `var(--…)` untouched), including the `@media` blocks and the `@keyframes` the kept rules use. `:root` and `@font-face` go to `tokens.css` only. References to Webflow "deleted" variables are rewritten to their live equivalent (`deletedVariableMap`). `<style>` embeds inside a section are kept, minus consent and announcement rules.
7. **Snippets.** Small elements for the foundations (a card, a tag, a form, a rich-text body, the style guide's sample blocks) are cleaned and matched the same way and saved to `raw/snippets/<id>.html` and `.css`.
8. **Writes** `sections/<folder>/source[--variant].html` (prettier formatted), `styles[--variant].css`, `section.md` (header plus template, only when missing; otherwise `section.generated.md` for comparison), `../tokens.css`, `../tokens.json`, `../sections/index.html` (gallery, `gallery.mjs`) and the tokens diff at the end of this file.
9. **Media into the repo** (`localize-media.mjs`, also run at the end of `foundations.mjs`, and standalone). Every image, SVG and Lottie JSON that the written HTML and CSS reference on the site's CDN (`src`, `poster`, `data-src`, CSS `url()`, inline styles) is copied, as served and under its original Webflow file name (URL-decoded, so `Groups%20%26%20Forums.svg` is `Groups & Forums.svg` on disk), into `../assets/media/`, and the reference is rewritten to the relative path (`../../assets/media/<file>`, percent-encoded). A file already on disk is kept (`--refresh` downloads again); a full capture run prunes files nothing references any more (`--prune` standalone). `media.json` next to the scripts records the source URL of every file. **Videos are not copied** (team decision, 7 October 2026): a `<video>` loses its CDN `src`; the video is downloaded to a temporary folder, its first frame is saved as `../assets/media/<name>-still.jpg` with `ffmpeg`, the frame becomes the `poster`, and an HTML comment names the video. Requests are plain GETs, one at a time with a pause, read-only.

`foundations.mjs` assembles `foundations/<name>/preview.html` and `styles.css` from the snippets: it merges the matched rules (one copy of each), adds the preview's own `fx-*` chrome, copies `:hover`/`:active` rules onto `.sim-hover`/`.sim-active` for the static button states, trims long rich-text bodies, measures the computed type sizes at 1440 and 390 and writes them as labels. `foundation.md` is written by hand and never overwritten.

`verify.mjs` opens every `source[--variant].html` from disk at 1440 and 390 with every network request blocked (only `file:` URLs load), screenshots it, compares it pixel by pixel with the live screenshot (`raw/verify/*-diff.png`), checks for sideways scroll, broken images, remote or missing media files, leftover scripts and tracking attributes, and writes `raw/verify/report.md`. Foundation previews get the same checks and their `desktop.png`/`mobile.png` from this run. Verdicts: OK (under 4% differing pixels and at most 4px height delta), minor (more than that, or a known difference listed in the config), broken (leftovers, broken images, sideways scroll, or a large difference).

## Deviations from the live site (by design)

- **Static states.** Sections driven by scripts show one state: FAQ first answer open (live: all closed); side-by-side (51) every illustration next to its text (live: one sticky illustration); comparison table (52) all categories (live: one, switched by pills); customer stories (53) and quote carousel (26) first item; accordions with image (17) first item open; logo marquee (10) standing still; numbers band (25) final numbers without the count-up; hero illustration slider (02) first image. Each `source.html` says so at the top and in a "static state" block at the end of its `<style>`.
- **Videos** are not in the repo (team decision, 7 October 2026). The `<video>` keeps its attributes (muted, loop, playsinline) but has no `src`; it shows a poster made from the video's first frame (`assets/media/<name>-still.jpg`), which is the same dark frame the live page shows before the video plays. `media.json` holds the video's CDN URL.
- **Form sections and the footer newsletter.** `action`, hidden fields and the anti-bot attributes are removed; success and error blocks too. The contact page's script-driven "social.plus × customer" logo pair (a Webflow placeholder until a script fills it) is removed.
- **Table of contents** on the glossary entry and blog post is built by a script (Finsweet) on the live site; the HTML holds the empty container.
- **Wrappers kept.** `w-dyn-list` / `w-dyn-items` / `w-embed` divs are not unwrapped: the site's CSS targets those classes. Only empty `w-dyn-empty` nodes and `w-condition-invisible` copies are removed.
- **Inline styles** stay on custom checkboxes and radios, where Webflow hides the native input by inline style.
- **Tokens.** The live `:root` holds 61 variables: 17 are Webflow "deleted" leftovers (dropped, their uses rewritten), 44 are live. The heading sizes are named `--_typography---h1-font-size` and so on; `tokens.json` carries a one-line "use" per token that survives re-runs (new tokens get theirs by hand, see the tokens diff below).
- **Prettier** formats the HTML and CSS so re-runs give readable diffs.
- **Foundations** are previews assembled from live snippets, not captures of one live block, so they have no live screenshot to compare with; verify checks them for breakage only.
- **Media** are local copies (`assets/media/`), not the CDN files: same bytes, same file names. The style guide's card-v1 sample has a Webflow placeholder in its icon circle that the CDN does not serve (403); the cards preview shows the iOS glyph of the SDK cards there instead.

## Quality check (2026-10-07, re-run with the media in the repo and every network request blocked)

Every `source.html` rendered from disk at 1440 and 390, with every request that is not a `file:` URL blocked, and compared with the live screenshot (`node verify.mjs`). "Pixels differing" counts pixels that differ on the shared area (threshold 0.15); 1 to 4% is text anti-aliasing and image decoding noise, so a row near the 4% line (the quote carousel 26, the feature icon cards 13) can flip between OK and minor from one run to the next. Height delta is the rendered height minus the live height in CSS pixels.

<!-- quality-table:start -->
80 items checked: 65 OK, 15 minor, 0 broken.

| Item | Result | Desktop: pixels differing, height delta | Mobile: pixels differing, height delta, sideways scroll | Leftovers / broken images |
|---|---|---|---|---|
| G1 Nav | minor | 11.6%, -12px | 9.2%, -7px, no sideways scroll | none |
| G2 Sub-nav | OK | 0.4%, +0px | 3.5%, +0px, no sideways scroll | none |
| G2 Sub-nav (blog) (blog) | OK | 0.0%, +0px | 0.1%, +0px, no sideways scroll | none |
| G3 Breadcrumb bar | OK | 1.0%, +0px | 0.0%, +0px, no sideways scroll | none |
| G3 Breadcrumb bar (plain) (light) | OK | 0.2%, +0px | 0.5%, +0px, no sideways scroll | none |
| G4 Footer CTA band | OK | 1.1%, -1px | 0.8%, +0px, no sideways scroll | none |
| G5 Footer | OK | 1.1%, -1px | 0.5%, +0px, no sideways scroll | none |
| G5 Footer (no newsletter) (no-newsletter) | OK | 0.7%, +0px | 1.0%, -1px, no sideways scroll | none |
| 01 Hero / Product (two-column) | OK | 0.7%, +0px | 1.5%, +0px, no sideways scroll | none |
| 01 Hero / Product (video right) (video) | OK | 2.7%, +0px | 2.5%, +0px, no sideways scroll | none |
| 01 Hero / Product (two buttons) (two-buttons) | OK | 2.6%, +0px | 2.9%, +0px, no sideways scroll | none |
| 02 Hero / Simple (title, text, buttons) | OK | 0.7%, +0px | 1.6%, +0px, no sideways scroll | none |
| 02 Hero / Simple (with illustration) (illustration) | OK | 0.9%, +0px | 2.2%, +0px, no sideways scroll | none |
| 03 Hero / Industry | OK | 0.7%, +0px | 1.2%, +0px, no sideways scroll | none |
| 04 Article / Title header (breadcrumb + H1) | OK | 0.0%, +0px | 0.1%, +0px, no sideways scroll | none |
| 05 Hero / vs | OK | 1.0%, +0px | 3.8%, +0px, no sideways scroll | none |
| 10 Logo wall (grid) | OK | 1.4%, -1px | 3.4%, -1px, no sideways scroll | none |
| 10 Logo wall (marquee) (marquee) | OK | 1.1%, -1px | 1.6%, -1px, no sideways scroll | none |
| 11 Two-column / Text + image | OK | 0.8%, +0px | 1.7%, +0px, no sideways scroll | none |
| 11 Two-column (checklist) (checklist) | minor | 0.6%, -1px | 5.0%, -1px, no sideways scroll | none |
| 11 Two-column (image left, gradient) (image-left) | minor | 0.6%, -1px | 4.6%, +0px, no sideways scroll | none |
| 11 Two-column (video, CTA) (video-cta) | OK | 1.6%, -1px | 3.9%, +0px, no sideways scroll | none |
| 11 Two-column (three alternating rows) (three-rows) | OK | 1.0%, -1px | 3.6%, -1px, no sideways scroll | none |
| 12 Feature grid (3 columns, icon + text) | OK | 1.1%, -1px | 2.4%, -1px, no sideways scroll | none |
| 13 Card grid / Feature icons (v2) | minor | 1.1%, +0px | 4.5%, -1px, no sideways scroll | none |
| 13 Card grid / Icon cards (v3) (v3-link-cards) | OK | 0.9%, +0px | 3.9%, -1px, no sideways scroll | none |
| 13 Card grid / Documentation cards (v3) (v3-docs) | OK | 1.4%, +0px | 3.7%, -1px, no sideways scroll | none |
| 14 Card grid / Bordered (v1) | minor | 2.3%, -1px | 5.1%, -1px, no sideways scroll | none |
| 15 Card grid / Plain | OK | 1.2%, +0px | 2.9%, -1px, no sideways scroll | none |
| 15 Card grid / Plain (3 columns) (three-columns) | OK | 1.0%, +0px | 3.1%, +0px, no sideways scroll | none |
| 16 Image-card grid (use cases, industries) | OK | 0.6%, +0px | 1.0%, +0px, no sideways scroll | none |
| 16 Image-card grid (4 columns, CMS) (four-columns-cms) | minor | 1.2%, +29px | 2.4%, +0px, no sideways scroll | none |
| 17 Accordion with image (features) | OK | 1.1%, -1px | 1.3%, -1px, no sideways scroll | none |
| 17 Accordion with image (square image right) (square-image) | OK | 2.3%, -1px | 2.5%, +0px, no sideways scroll | none |
| 18 FAQ accordion | minor | 0.1%, +0px | 3.3%, -1px, no sideways scroll | by design: first answer open (live: all closed) |
| 18 FAQ accordion (border top) (border-top) | minor | 1.8%, -1px | 2.8%, -1px, no sideways scroll | by design: first answer open (live: all closed) |
| 19 Customer story strip | OK | 1.2%, +0px | 2.6%, +0px, no sideways scroll | none |
| 19 Customer story strip (6, aside) (six-stories) | OK | 0.3%, +0px | 2.6%, +0px, no sideways scroll | none |
| 20 Why social.plus grid | OK | 1.4%, -1px | 2.1%, -1px, no sideways scroll | none |
| 20 Why social.plus grid (no heading) (no-heading) | OK | 1.5%, -1px | 1.9%, -1px, no sideways scroll | none |
| 21 Feature grid / Product details | OK | 0.8%, +0px | 1.7%, -1px, no sideways scroll | none |
| 22 Explore more (links with images) | OK | 2.1%, +0px | 2.4%, +0px, no sideways scroll | none |
| 23 CTA band (inline) | minor | 1.9%, +0px | 4.9%, -1px, no sideways scroll | none |
| 23 CTA band (inline, two buttons) (two-buttons) | OK | 0.8%, -1px | 2.5%, -1px, no sideways scroll | none |
| 24 Form section | OK | 0.6%, +0px | 1.1%, +0px, no sideways scroll | none |
| 24 Form section (download, with image) (with-image) | OK | 2.9%, -1px | 2.2%, +0px, no sideways scroll | none |
| 25 Numbers band | minor | 1.6%, +0px | 5.3%, +0px, no sideways scroll | none |
| 26 Quote / Carousel | minor | 1.4%, +0px | 4.6%, +0px, no sideways scroll | none |
| 30 Thumbnail grid (blog) | OK | 0.6%, +0px | 1.9%, +0px, no sideways scroll | none |
| 30 Thumbnail grid (related, aside) (related-aside) | OK | 3.0%, -1px | 2.7%, +0px, no sideways scroll | none |
| 31 Featured item | OK | 0.2%, +0px | 0.3%, +0px, no sideways scroll | none |
| 32 Updates list (with tags) | minor | 1.1%, -1px | 6.6%, -1px, no sideways scroll | none |
| 40 Article (blog post) | OK | 1.3%, +0px | 2.5%, +0px, no sideways scroll | none |
| 40 Article (answer) (answer) | OK | 0.0%, +0px | 0.1%, +0px, no sideways scroll | none |
| 40 Article (release note) (release-note) | OK | 0.7%, +0px | 1.4%, +0px, no sideways scroll | none |
| 41 Customer story hero | OK | 0.4%, +0px | 1.5%, +0px, no sideways scroll | none |
| 42 Customer story body | OK | 1.5%, -1px | 4.0%, -1px, no sideways scroll | none |
| 43 Glossary entry | minor | 2.7%, -1px | 5.5%, -1px, no sideways scroll | none |
| 50 vs / Statement band | OK | 0.1%, +0px | 0.1%, +0px, no sideways scroll | none |
| 51 vs / Side-by-side (sticky) | minor | 1.4%, -1px | 5.1%, -1px, no sideways scroll | by design: static state: each illustration next to its text (live: one sticky illustration, inactive text dimmed) |
| 52 vs / Comparison table | minor | 1.1%, +2160px | 3.0%, +2239px, no sideways scroll | by design: all 5 categories show (the live page shows one at a time, a script switches) |
| 53 vs / Customer stories (tabbed) + form | OK | 2.0%, +0px | 2.3%, +0px, no sideways scroll | none |
| 60 Pricing / Plan cards | OK | 0.8%, +0px | 1.8%, +0px, no sideways scroll | none |
| 61 Pricing / Compare table | OK | 0.7%, -1px | 3.3%, -1px, no sideways scroll | none |
| 62 Pricing / Additional fees | OK | 1.3%, -1px | 3.0%, +0px, no sideways scroll | none |
| Foundation: accessibility | OK | – | – no sideways scroll | none |
| Foundation: accordion-row | OK | – | – no sideways scroll | none |
| Foundation: buttons | OK | – | – no sideways scroll | none |
| Foundation: cards | OK | – | – no sideways scroll | none |
| Foundation: colors | OK | – | – no sideways scroll | none |
| Foundation: dividers | OK | – | – no sideways scroll | none |
| Foundation: form-inputs | OK | – | – no sideways scroll | none |
| Foundation: icons | OK | – | – no sideways scroll | none |
| Foundation: imagery | OK | – | – no sideways scroll | none |
| Foundation: logo | OK | – | – no sideways scroll | none |
| Foundation: rich-text | OK | – | – no sideways scroll | none |
| Foundation: shadows-and-radius | OK | – | – no sideways scroll | none |
| Foundation: spacing | OK | – | – no sideways scroll | none |
| Foundation: tags | OK | – | – no sideways scroll | none |
| Foundation: typography | OK | – | – no sideways scroll | none |
<!-- quality-table:end -->

No leftover `<script>`, `<iframe>`, inline styles (other than the checkboxes), tracking attributes or consent code in any `source.html` or `preview.html`. Every image is a local file in `assets/media/` and every `<video>` shows a local poster: `verify.mjs` blocks every request that is not a `file:` URL, so a remote or missing file would show as broken. No sideways scroll at 390px.

## Tokens: live site against the previous capture

Every full run compares the live `:root` with the `tokens.json` committed by the previous run and writes the result here: unchanged, changed (a value moved in Webflow), new (add a "use" line in `tokens.json` and a swatch note in `foundations/colors/foundation.md`) and gone (remove it from the foundations). The first run after the move to `design-system/` lists everything as unchanged because the baseline is the 2026-10-07 capture.

<!-- tokens-diff:start -->
_Generated 2026-10-07 by capture.mjs. Live `:root` against the previously committed `tokens.json` (captured 2026-10-07)._

Tokens: 44 live variables; 44 unchanged since the last capture (2026-10-07); 0 changed; 0 new; 0 gone.

| Variable | Live value | Last capture | Note |
|---|---|---|---|
<!-- tokens-diff:end -->
