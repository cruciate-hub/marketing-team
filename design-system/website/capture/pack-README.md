# social.plus website design system

The design system of the social.plus website (https://www.social.plus), captured from the live site on 2026-10-07: the foundations (colours, type, spacing, buttons, cards, rich text, inputs, tags, accordion rows, dividers, image ratios), 41 section types with their variants (56 captures), and 8 page recipes. Built for Claude Design (Design systems → New design system) and for anyone who builds a social.plus web page.

Everything is as the site is today. No team decision from the 7 October audit has been applied; known inconsistencies are listed in each `foundation.md` so nobody mistakes them for rules.

## The rule

> Build pages only from the social.plus section set in `sections/` and the foundations in `foundations/`. Use each section as written there: its structure, its content slots and only its allowed variations. Use only the values in `tokens.css`: dark background (`--social--dark` #111), Figtree, one blue for actions (`--social--main-blue` #3B41EC). Do not invent a new section, text effect, icon style, shadow or colour. If the page needs something the set does not have, stop and propose it: name the section, say what it is for, show one example, and mark it "proposed". A proposed section may be used only after Amadeus approves it; then it is added to the set. Follow the page recipes in `sections/recipes/` for the section order.

Short form for a project's instructions: dark background, Figtree, one blue for actions; only these sections, only these tokens; anything new is proposed and marked "proposed".

## How it is organised

```
README.md                 this file
tokens.css                the 44 live Webflow variables as CSS custom properties (+ the Figtree @font-face)
tokens.json               the same tokens with their use, machine-readable
figtree.woff2             fallback font file for tokens.css
foundations/<name>/       preview.html (self-contained), styles.css, foundation.md (values and inconsistencies), desktop.png, mobile.png
sections/README.md        the rule and the index of all sections
sections/<nn-name>/       section.md (use it when, don't, content slots, allowed variations, not allowed, accessibility and mobile),
                          source.html (self-contained: the live HTML and the matching CSS rules, tokens as var(--…)),
                          styles.css, desktop.png (1440 wide), mobile.png (390 wide);
                          variants: the same files with a --<variant> suffix (source--video.html, desktop--video.png, …)
sections/global/<name>/   nav, sub-nav, breadcrumb bar, footer CTA band, footer
sections/recipes/<page>.md  the fixed section order per page type: vs, product page, SDK page, industry page, blog post, answer, glossary entry, customer story
```

Numbers group the sections by family: G global chrome, 01 to 05 heroes, 10 to 26 content sections, 30 to 32 listings, 40 to 43 articles, 50 to 53 the /vs/ family, 60 to 62 the pricing family. Start with `sections/README.md`.

## Reading the files

- Every `source.html` and `preview.html` opens in a browser as it is. Images and videos load from the site's CDN; the CSS is the site's own (Webflow class names kept so the rules work; they are not a concern).
- Where the live section depends on a script (tabs, sliders, sticky swaps, accordions, marquees, count-ups), the file shows one static state and says so in a comment at the top.
- Screenshots are 1x (1440 and 390 CSS pixels wide) with a 256-colour palette to keep the pack small; the repository holds the 2x originals.
- "TO CHECK" in a note marks something nobody has decided yet.

## Source and upkeep

Captured by Playwright scripts in the `marketing-team` repository (`design-system/website/capture/`), read-only towards the site, no AI calls. Re-run the capture after a site change and rebuild this pack; the notes (`section.md`, `foundation.md`) are written by hand and survive re-runs.
