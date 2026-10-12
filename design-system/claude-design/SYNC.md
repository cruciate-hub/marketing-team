# Claude Design and this folder

The design system lives in two places: this folder on GitHub and the "social.plus" page in Claude → Design (https://claude.ai/artifact/EtY7zLfKmoKRJVTpVjPAm7). They must hold the same thing. This file says where every file of the page comes from, and the rule that keeps them the same.

## The rule

- A change can start in either place. A change made on the page (by anyone, with Claude or by hand) comes back here **the same day**, as a pull request.
- Re-sync the page from GitHub only when `capture/claude-design-check.py` reports no difference. A re-sync over a page that holds work GitHub does not have overwrites that work.
- Before any re-sync or a big change on the page, keep a copy of the page's files (outside this repository).

## Where each page file comes from

| Page file (under `project/`) | Source here | How |
|---|---|---|
| `01-colors.md` to `08-accessibility.md`, `03b-grid-and-frame.md` | `foundations/<name>/foundation.md` | the same file |
| `09-sections.md` | `sections/README.md` | the same file |
| `11-taste.md` | `taste.md` | the same file |
| `10-recipes.md`, `12-proposals.md` | `claude-design/` (they gather `sections/recipes/*.md` and `sections/proposals/*.md` under a short intro) | the same file |
| `README.md` (the brand book) | `claude-design/README.md` | the same text; the page appends its generated "Consuming this system" and "Index" |
| `tokens.json` | `claude-design/tokens.json` | the same file. It holds the live Webflow variables (from `tokens.json` here, which the capture writes) and the tokens decided but not yet in Webflow (role colours and scales, type scale, spacing steps, layout, radius, shadow, containers, heading sizes, Geist Mono). A new live value goes into both files |
| `fonts/figtree.woff2`, `fonts/geist-mono.woff2` | `figtree.woff2`, `geist-mono.woff2` | the same file |
| `components/<Card>/preview.html` | the source named in `claude-design/cards.json` (`sources`) | line 1 is the card line from `cards.json` (`cards`); then the source without its `tokens.css` link, with images from the page's asset store instead of `../../assets/` |
| `components/PricingCompareTable/preview.html` | `claude-design/components/PricingCompareTable/preview.html` | the same file (a shortened version of the captured table) |
| `components/Cover/preview.html`, `components/bundle.css` | `claude-design/components/` | the same file |
| `components/<Card>/README.md` | `claude-design/components/<Card>/README.md` where it exists; otherwise the section's `section.md` or the foundation's `foundation.md` without its title line, under a one-line summary | as said |
| `assets/<group>/README.md` | `claude-design/assets/<group>/README.md` | the same file |
| images in `assets/` | `assets/media/`, `assets/third-party/`, the logo files in the repository root `assets/` | uploaded to the page's asset store |
| `design-system.json`, `api/`, `tokens.css`, `manifest.json` | none | the page writes them |

Cards that are not on the page: `cards.json` lists them under `notShown` (Colors, Typography, Spacing, Shadows and radius since 9 October 2026: the token views show the same values). Their `preview.html` stays in `foundations/` for GitHub Pages and the pack.

The Frame card (`foundations/grid-and-frame/preview.html`) uses the role and layout tokens, which only the page's `tokens.css` has; opened from this folder it shows without them.

## Checking

1. Read the page's files with Claude into a folder outside this repository: `SKILL.md`, `index.html` and everything under `project/`.
2. Run `python3 capture/claude-design-check.py <that folder>/project`. It prints MATCH or DIFF for every page file and exits with 1 when anything differs.
3. For each DIFF, copy the page's version to the source the table names (for a card body: make the same edit in its source), then run the check again until it reports no difference.
4. After a sync, set `meta.ref` (`main@<commit>`) and `meta.synced` (the date) in `claude-design/tokens.json` to the commit the page now matches, here and on the page in the same change.
