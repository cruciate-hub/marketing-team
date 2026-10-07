# Website Design System

[View live style guide](https://cruciate-hub.github.io/marketing-team/design-system/website/style-guide.html)

- `../website.md`: the tokens with their use, written for people.
- `tokens.css` and `tokens.json`: the live tokens as captured from the site (generated, do not edit by hand). `figtree.woff2` is the fallback font file `tokens.css` points to.
- `foundations/`: colours, typography, spacing and containers, buttons, cards, rich text, form inputs, tags, accordion rows, dividers, image ratios: one folder each with a self-contained `preview.html`, `styles.css`, a hand-written `foundation.md` (values as measured, known inconsistencies, no team decision applied) and screenshots.
- `sections/`: the section set, one folder per section type with notes, HTML, CSS and screenshots (variants with a `--<variant>` suffix). Start with [`sections/README.md`](sections/README.md) (the rule and the index) and the gallery `sections/index.html` (foundations and sections).
- `sections/recipes/`: page recipes (fixed section order per page type): vs, product page, SDK page, industry page, blog post, answer, glossary entry, customer story.
- `capture/`: the Playwright scripts that build `sections/`, `foundations/` and the tokens from the live site, verify them and assemble the upload pack for Claude Design. See [`capture/README.md`](capture/README.md). No AI calls.
- `taste.md`: what good looks like for social.plus (to be drafted).
