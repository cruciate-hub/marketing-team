# social.plus website sections

The section set for website pages. Each folder holds one section type as it is on the live site: `section.md` (when to use it, content slots, allowed variations, what is not allowed, accessibility and mobile; uncertain items are marked TO CHECK), `source.html` (self-contained HTML with the site's own CSS rules, tokens kept as `var(--…)`, see `../tokens.css`), `styles.css` (the same rules alone), `desktop.png` (1440 wide) and `mobile.png` (390 wide). Variants of a section sit in the same folder with a `--<variant>` suffix (`source--video.html`, `desktop--video.png`, …). `index.html` is a gallery of every foundation and section for a quick review.

Captured from the live site by `../capture/capture.mjs` (see `../capture/README.md`; re-run it after a site change). The screenshots, HTML and CSS are regenerated; `section.md` is written by hand and never overwritten. Foundations (colours, type, spacing, buttons, cards, rich text, inputs, tags, accordion rows, dividers, image ratios) are in `../foundations/`.

## The rule

Paste this into the design system's instructions and into every website project in Claude Design:

> Build pages only from the social.plus section set in `sections/` and the foundations in `foundations/`. Use each section as written there: its structure, its content slots and only its allowed variations. Use only the values in `tokens.css`: dark background (`--social--dark`), Figtree, one blue for actions (`--social--main-blue`). Do not invent a new section, text effect, icon style, shadow or colour. If the page needs something the set does not have, stop and propose it: name the section, say what it is for, show one example, and mark it "proposed" in the conversation. A proposed section may be used on the page only after Stefan or Amadeus approves it; then it is added to the set. Follow the page recipes in `sections/recipes/` for the section order. Facts about the product come from `messaging/product-capabilities.md`.

## Index

Numbers group the sections by family: G global chrome, 01 to 05 heroes, 10 to 26 content sections, 30 to 32 listings, 40 to 43 articles, 50 to 53 the /vs/ family, 60 to 62 the pricing family. "Draft" means captured and described, waiting for approval by Stefan or Amadeus (then the status line in `section.md` changes to "approved"). New sections wait in `proposals/` as `YYYY-MM-DD-<name>.md` until approved.

| # | Section | Folder | Variants captured | Source pages | Status |
|---|---|---|---|---|---|
| G1 | Nav | `global/nav/` | dark, mega menu closed | /vs/circle | draft |
| G2 | Sub-nav | `global/sub-nav/` | product (Chat); `--blog` | /chat, /blog | draft |
| G3 | Breadcrumb bar | `global/breadcrumb-bar/` | dark; `--light` (plain class) | /customer-story/activerse, /tutorials/… | draft |
| G4 | Footer CTA band | `global/footer-cta-band/` | heading, line, one button | /vs/circle | draft |
| G5 | Footer | `global/footer/` | with newsletter; `--no-newsletter` | /vs/circle, /contact/contact-sales | draft |
| 01 | Hero / Product (two-column) | `01-hero-product/` | image right; `--video`; `--two-buttons` | /social/uikit, /chat, /chat/sdk/ios | draft |
| 02 | Hero / Simple | `02-hero-simple/` | eyebrow, title, buttons, logos row; `--illustration` | /ai/mcp-server, /chat/sdk | draft |
| 03 | Hero / Industry | `03-hero-industry/` | one | /industry/gaming | draft |
| 04 | Article / Title header | `04-article-title-header/` | glossary | /glossary/activity-feed | draft |
| 05 | Hero / vs | `05-hero-vs/` | two brand tiles | /vs/circle | draft |
| 10 | Logo wall | `10-logo-wall/` | grid (hover chips); `--marquee` | /vs/circle, /chat | draft |
| 11 | Two-column / Text + image | `11-two-column/` | image right; `--checklist`; `--image-left`; `--video-cta`; `--three-rows` | /why-social, /chat/sdk/ios, /chat | draft |
| 12 | Feature grid (3 columns) | `12-feature-grid/` | CMS features | /chat | draft |
| 13 | Card grid / Feature icons | `13-card-grid-icons/` | v2 4 columns; `--v3-link-cards`; `--v3-docs` | /industry/gaming, /use-case/1-1-chat, release note | draft |
| 14 | Card grid / Bordered (v1) | `14-card-grid-bordered/` | 3 columns with text links | /social/uikit | draft |
| 15 | Card grid / Plain | `15-card-grid-plain/` | 2 columns; `--three-columns` | /industry/gaming, /use-case/1-1-chat | draft |
| 16 | Image-card grid | `16-image-card-grid/` | 3 columns static; `--four-columns-cms` | /industry/gaming, /white-label/social-network | draft |
| 17 | Accordion with image | `17-accordion-with-image/` | image left; `--square-image` (right) | /industry/gaming, /use-case/1-1-chat | draft |
| 18 | FAQ accordion | `18-faq/` | gradient background; `--border-top` (long list, Expand overlay) | /vs/circle, /ai/mcp-server | draft |
| 19 | Customer story strip | `19-customer-story-strip/` | 5 stories; `--six-stories` | /chat, /customer-story/activerse | draft |
| 20 | Why social.plus grid | `20-why-social-plus/` | with heading; `--no-heading` (badges, SDK icons) | /industry/gaming, /chat | draft |
| 21 | Feature grid / Product details | `21-product-details/` | tile grid | /product | draft |
| 22 | Explore more | `22-explore-more/` | two link tiles | /chat | draft |
| 23 | CTA band (inline) | `23-cta-band-inline/` | one grey button; `--two-buttons` | /pricing, /ai/mcp-server | draft |
| 24 | Form section | `24-form-section/` | contact; `--with-image` (download) | /contact/contact-sales, /social/uikit | draft |
| 25 | Numbers band | `25-numbers-band/` | 4 numbers | / | draft |
| 26 | Quote / Carousel | `26-quote-carousel/` | first quote shown | / | draft |
| 30 | Thumbnail grid | `30-thumbnail-grid/` | blog overview; `--related-aside` | /blog, blog post | draft |
| 31 | Featured item | `31-featured-item/` | blog | /blog | draft |
| 32 | Updates list (with tags) | `32-updates-list/` | latest releases | release note | draft |
| 40 | Article | `40-article/` | blog post; `--answer`; `--release-note` | blog post, answer, release note | draft |
| 41 | Customer story hero | `41-customer-story-hero/` | one | /customer-story/activerse | draft |
| 42 | Customer story body | `42-customer-story-body/` | one | /customer-story/activerse | draft |
| 43 | Glossary entry | `43-article-glossary/` | one | /glossary/activity-feed | draft |
| 50 | vs / Statement band | `50-vs-statement-band/` | one | /vs/circle | draft |
| 51 | vs / Side-by-side (sticky) | `51-vs-side-by-side/` | one, static state | /vs/circle | draft |
| 52 | vs / Comparison table | `52-vs-comparison-table/` | one, all categories shown | /vs/circle | draft |
| 53 | vs / Customer stories + form | `53-vs-customer-stories-form/` | one, first story shown | /vs/circle | draft |
| 60 | Pricing / Plan cards | `60-pricing-plan-cards/` | one | /pricing | draft |
| 61 | Pricing / Compare table | `61-pricing-compare-table/` | one | /pricing | draft |
| 62 | Pricing / Additional fees | `62-pricing-additional-fees/` | one | /pricing | draft |

Not in the set (audit section 7, "outside the set"): the home-only sections (hero, what-we-do columns, industry items, stage cards, add-on cards, stats tiles), the AI pages' own sections (stack cards, comparison matrix, timeline, showcase), the AWS, careers, consulting, partner-program and customer-stories-overview heroes, the service-plan table, the people grid, the investor logos, the Stories tabs. The Community Corner and podcast sections are out of scope (Stefan, 7 Oct). Anything from this list is proposed first.

## Recipes

Fixed section order and content slots per page type, in `recipes/`: [`vs.md`](recipes/vs.md), [`product-page.md`](recipes/product-page.md), [`sdk-page.md`](recipes/sdk-page.md), [`industry-page.md`](recipes/industry-page.md), [`blog-post.md`](recipes/blog-post.md), [`answer.md`](recipes/answer.md), [`glossary-entry.md`](recipes/glossary-entry.md), [`customer-story.md`](recipes/customer-story.md).

## Reading the files

- `source.html` opens in any browser from this folder (it links `../../tokens.css`, or `../../../tokens.css` for the global ones). Images and videos load from the site's CDN.
- Where a section is driven by a script on the live site (tabs, slider, sticky swap, accordion, marquee, count-up), `source.html` shows one static state and says so in an HTML comment at the top and in a "static state" block at the end of its `<style>`.
- Class names come from Webflow and are not a concern; the copied CSS needs them. Page `<style>` embeds that the section depends on are kept inside the section.
