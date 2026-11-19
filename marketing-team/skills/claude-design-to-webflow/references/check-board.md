# Board check (`scripts/check-board.mjs`)

The Check step's tool. It renders the Claude Design board and the staging page at 1440, 800 and 390 and reports PASS / FAIL / WARN / NOTE per check, with side-by-side screenshots. A build is not done while a FAIL is unexplained.

## Setup (once per machine)

```bash
cd <skill folder>/scripts && npm install && npx playwright install chromium
```

It uses the system Chrome when it finds one, otherwise Playwright's Chromium. Node 18 or newer.

## Inputs

1. **The board**, fresh: `Artifact read` the canvas right before checking and use the saved `.dc.html` (note its version id in the report). A board read hours ago is not the board (Pitfall 124).
2. **The staging URL** (`https://<site>.webflow.io/<page>`), published after the last change.
3. **A roles file**, written in the Map step. JSON:
   - `roles`: `{ "name": ["board selector", "staging selector"] }`. Start with one role per section in page order, named `section1_…`, `section2_…` (sections without a heading too, such as a logo wall: Pitfall 131). Then the elements that carry the look: titles, leads, cards, cells, tiles, chips. Roles named `section…` also get the frame-line checks.
   - `known`: accepted Webflow-owned differences, e.g. `{ "widths": [800, 390], "roles": "*", "props": ["x", "w", "paddingLeft", "paddingRight"], "why": "Webflow page gutters" }`. They report as NOTE and go on the "Webflow won" list for the board.
   - `newCss`: class names or rule text this build added; the check confirms they are in the live CSS (stale CDN, Pitfall 21).
   - `a11yScope` (default `main`), `selftest` cases (below), optional tolerances `tolerancePx` (3), `toleranceCss` (1.5), `toleranceColor` (4).
   - Example: `scripts/examples/pricing.roles.json`.

## Run

```bash
node check-board.mjs --roles <roles.json> --board <Board.dc.html> --url <staging url> --out <folder>
```

Exit code 1 when anything FAILs. `report.md`, `results.json` and `side-by-side-<width>.png` land in `--out`.

## What it checks

- **Roles** at each width: present, visible, x / width / height, and font size, line height, weight, letter spacing, colour (text elements only), padding, gap (flex/grid only), effective background, radius, border widths.
- **Frame lines per section**: a line at the top and bottom edge when the board has one, and at least as many vertical lines as the board (Pitfalls 93, 94, 132, 133).
- **Horizontal scroll** at each width.
- **Accessibility** on staging: axe-core WCAG 2.1 A/AA inside `main` (serious and critical = FAIL, others WARN), plus one `<main>`, decorative SVGs with `aria-hidden` + `focusable="false"`, duplicate ids, raw `href` attributes on non-links, stray `<link rel>` after anchors (Pitfalls 23, 66, 74, 101, 127).
- **Internal links** answer below 400; external links are listed, not failed.
- **New CSS is live** for every `newCss` entry.

## Reading the result

- A FAIL is either a build fault (fix it) or a board-vs-Webflow difference where Webflow wins (add it to `known` with a `why` and raise it as a drift). Never widen a tolerance to make a FAIL go away.
- **Fonts:** a local board can't load its `/_blob` fonts, so the script loads Figtree and Geist Mono from Google Fonts. A WARN "board fonts" means that failed: text sizes and wraps are then unreliable (the 19 Nov 2026 pricing build was tuned against an Arial fallback this way, and its headings wrapped one line too many).
- Board images stay blank locally; that doesn't move the layout.

## Prove it can fail

```bash
node selftest.mjs --roles <roles.json> --board <Board.dc.html>
```

Runs a baseline, then each `selftest` case (CSS injected into staging: a removed frame line, a wrong font size, a hidden section, a forced overflow) and expects a new FAIL each time. Run it when you change the script or write a roles file for a new page type.

## When the script can't run

Do the same checks by hand and say so in the report: fresh board read; screenshots of board and staging at 1440, 800 and 390; `getComputedStyle` / `getBoundingClientRect` for each section and its key elements; a 1:1 crop of every section edge for frame lines and "+" markers; `document.scrollingElement.scrollWidth` at each width; Webflow's `accessibility-audit` skill or a manual axe run.
