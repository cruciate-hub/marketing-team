# social.plus website design system

The design system of the social.plus website (https://www.social.plus), captured from the live site on 2026-10-07: the foundations (colours with the brand extras, typography, spacing, buttons, cards, rich text, inputs, tags, accordion rows, dividers, imagery, logo, icons, accessibility, shadows and radius), 41 section types with their variants (56 captures), 9 page recipes, and `taste.md` on how to combine the sections. Built for Claude Design (Design systems → New design system) and for anyone who builds a social.plus web page.

The sections and the measured values are as the site is today. Since 8 October 2026 the colours, typography, spacing, shadows and radius foundations and the new grid and frame foundation also carry the web library's decisions (Amadeus), marked as decisions and not yet in Webflow. Known inconsistencies are listed in each `foundation.md` so nobody mistakes them for rules. The logo, icons, imagery, accessibility and shadows-and-radius foundations also carry the brand rules (what to do), marked as such.

## The rule

> Build pages only from the social.plus section set in `sections/` and the foundations in `foundations/`. Use each section as written there: its structure, its content slots and only its allowed variations. Keep its inner layout as its screenshots and `source.html` show it (in the card grids the icon sits top-left above the title, never beside the text); a different inner layout is a proposal. Use only the values in `tokens.css`: dark background (`--social--dark` #111), Figtree from `figtree.woff2` (never Google Fonts or another source, no `font-feature-settings`; fallback Arial, sans-serif) and Geist Mono from `geist-mono.woff2` for all-caps eyebrows and labels only, code in the system monospace (emails are the exception and follow the email spec), colours through the role tokens (`color-*`), one blue for actions (`color-accent-fill`, = `--social--main-blue` #3B41EC). Do not invent a new section, text effect, icon style, shadow or colour. If the page needs something the set does not have, stop and propose it: name the section, say what it is for, show one example, and mark it "proposed". A proposed section may be used only after Stefan or Amadeus approves it; then it is added to the set. Follow the page recipes in `sections/recipes/` for the section order. Combine the sections as `taste.md` says. Every page is built in one of two looks, chosen per page by the person who asks for it: **current** (the captured sections, the site as it is on Webflow today) or **framed** (the framed sections in `sections/framed/`, on one frame from the navigation to the footer; not yet in Webflow). When the request does not say which look, ask before building: "Current Webflow look or the new framed design?" Never mix the two on one page and never wrap a captured section in the frame. Product landing, industry and /vs/ pages have a recipe in both looks; the other page types exist only in the current look (say so when framed is asked for).
>
> **Definition of done.** Before saying a page is finished, check each point and report it in the reply:
> 1. The page is in one look, the one the person chose (current or framed; asked before building when the request did not say), and follows that look's recipe in `sections/recipes/`; if none fits, the reply names the closest recipe and where and why the page departs from it.
> 2. The global nav (G1) and the footer (G5) are on the page, and the footer CTA band (G4) where the recipe has it.
> 3. Every section is one from the set, used as its `section.md` allows, with its inner layout as captured (where the icon, image and text sit, their alignment and order; only the content changes). Anything else is marked "proposed" on the page itself and in the reply.
> 4. Only values from `tokens.css`, colours through the role tokens; Figtree from `figtree.woff2`, Geist Mono from `geist-mono.woff2` for all-caps eyebrows and labels only, code in the system monospace; no new text effect, icon style, shadow or colour.
> 5. One primary (blue) button per section: the first button in a group is blue, every button after it is secondary (grey border), then at most one text link. Never two blue buttons, also not for a product that connects to two AI apps (Agentry: "Connect on Claude" blue, "Connect on ChatGPT" grey border). Decision: Stefan, 12 October 2026 (replaces the two-primary exception of the same day).
> 6. Example or illustrative numbers, charts and sample answers carry the visible label "Illustrative example"; real numbers carry their source.
> 7. Third-party logos only from the approved set in `assets/third-party/` (listed in `foundations/logo/foundation.md`, "Third-party logos") or files supplied by the team; a tool or company without an approved file is written as text.
> 8. Links that do not exist yet are clear placeholders (`href="#"` and a note of the intended path), never invented URLs.
> 9. Accessibility basics: one `<h1>`, headings in order, alt text on meaningful images, token pairs with AA contrast, interactive parts (tabs, accordions) are real buttons that work with the keyboard, or the static state is used.
> 10. Render the page at 1440 and 390, check it against the design system, `taste.md` and `feedback.md` (the details already corrected once), and list every mismatch in the reply ("none found" counts as a check).

Short form for a project's instructions: dark background, Figtree from `figtree.woff2` (never Google Fonts or another source, no `font-feature-settings`; fallback Arial, sans-serif) and Geist Mono from `geist-mono.woff2` for all-caps eyebrows and labels only (code in the system monospace), one blue for actions; only these sections, only these tokens; anything new is proposed and marked "proposed".

## How it is organised

```
README.md                 this file
taste.md                  how to combine the sections so a page feels like social.plus (a do and a don't per rule)
tokens.css                the 44 live Webflow variables as CSS custom properties (+ the Figtree @font-face)
tokens.json               the same tokens with their use, machine-readable
figtree.woff2             the main font file (social.plus Figtree build)
geist-mono.woff2          Geist Mono, for all-caps eyebrows and labels only (SIL Open Font License, embedded in the file)
assets/media/             the images the previews use, copied as served from the site (plus one first-frame still per video; videos are not included)
foundations/<name>/       preview.html (self-contained), styles.css, foundation.md (values, rules, inconsistencies), desktop.png, mobile.png
sections/README.md        the rule and the index of all sections
sections/<nn-name>/       section.md (use it when, don't, content slots, allowed variations, not allowed, accessibility and mobile),
                          source.html (self-contained: the live HTML and the matching CSS rules, tokens as var(--…)),
                          styles.css, desktop.png (1440 wide), mobile.png (390 wide);
                          variants: the same files with a --<variant> suffix (source--video.html, desktop--video.png, …)
sections/global/<name>/   nav, sub-nav, breadcrumb bar, footer CTA band, footer
sections/recipes/<page>.md  the fixed section order per page type (12): vs, product page, product landing, industry page and /vs/ each with a framed version, SDK page, industry page, blog post, answer, glossary entry, customer story
```

Numbers group the sections by family: G global chrome, 01 to 05 heroes, 10 to 26 content sections, 30 to 32 listings, 40 to 43 articles, 50 to 53 the /vs/ family, 60 to 62 the pricing family. Start with `sections/README.md`.

## Reading the files

- Every `source.html` and `preview.html` opens in a browser as it is, with no network: images come from `assets/media/`; the video sections show the video's first frame as poster (the videos are not in the pack); the CSS is the site's own (Webflow class names kept so the rules work; they are not a concern).
- Where the live section depends on a script (tabs, sliders, sticky swaps, accordions, marquees, count-ups), the file shows one static state and says so in a comment at the top.
- Screenshots are 1x (1440 and 390 CSS pixels wide) with a 256-colour palette to keep the pack small; the repository holds the 2x originals.
- "TO CHECK" in a note marks something nobody has decided yet.

## Source and upkeep

Captured by Playwright scripts in the `marketing-team` repository (`design-system/capture/`; the logo, icons, accessibility and shadows-and-radius previews are written by hand), read-only towards the site, no AI calls. Re-run the capture after a site change and rebuild this pack; the notes (`section.md`, `foundation.md`) are written by hand and survive re-runs.
