# Page recipes

Fixed section order and content slots per page type, from `sections/recipes/` (10). Nav (G1) above, footer CTA band (G4) and footer (G5) below every page. A product or feature that is not a product family of its own (Agentry, the MCP server, Vise, an add-on) uses the product landing recipe.

## Recipe: a product page

A page for one product family or product (Chat, Social, Video, Analytics, white-label), like https://www.social.plus/chat. Fixed order; a section may be left out only where the table says "optional". Nav (G1) and sub-nav (G2) above, footer CTA band (G4) and footer (G5) below.

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| G1 | Nav | none (shared) | always |
| G2 | Sub-nav | product family links | the family's own link set |
| 01 | Hero / Product (two-column) | H1, paragraph, Contact Sales (+ optional grey button), product video or image | `--video` on product pages, `--two-buttons` on SDK pages |
| 10 | Logo wall (`--marquee`) | customers from the CMS | the marquee, not the grid, on product pages |
| 11 | Two-column / Text + image | eyebrow, heading, paragraph, grey buttons, image per row | `--three-rows` for 2 or 3 capabilities, or one default two-column; `.is-first` on the first |
| 12 | Feature grid | heading, intro, grey button, 6 to 12 CMS features | |
| 19 | Customer story strip | heading, intro, 5 stories from the CMS | |
| 20 | Why social.plus grid (`--no-heading`) | the fixed reasons, badges, SDK icons | optional on sub-pages |
| 22 | Explore more | the two other product families | |
| G4 | Footer CTA band | heading, line | "Contact Sales" button |
| G5 | Footer | none (shared) | always |

Rules for the page:

- Dark background throughout; the only CTA colour is `--social--main-blue`, used once in the hero and once in the footer CTA band. Everything in between uses grey buttons or text links.
- Product facts come from `messaging/product-capabilities.md`; feature names match the Features collection.
- Nothing is added between the sections. If a product page needs more (a form, pricing, a comparison), propose a section first (see `../README.md`).

## Recipe: a product or feature landing page

A page for one product or feature that is not a product family of its own: Agentry, the MCP server (https://www.social.plus/ai/mcp-server), Vise (https://www.social.plus/ai/vise), an add-on. Derived from the live AI pages and the product pages (/chat, /analytics): the AI pages open with the simple hero and a "Works in" row, show the value in link cards, explain how it works in steps, close with a CTA band, a FAQ and the footer band. Fixed order; a section may be left out only where the table says "optional". Nav (G1) above, footer CTA band (G4) and footer (G5) below. Where the live AI pages use a section outside the set (steps timeline, showcase), this recipe names the set section that does the job.

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| G1 | Nav | none (shared) | always |
| G2 | Sub-nav | the family's links | optional: only when the product belongs to a family that has a sub-nav (Chat, Social, Video); the live AI pages have none |
| 01 | Hero / Product (two-column) | eyebrow optional, H1 5 to 9 words (the product's promise), paragraph 25 to 45 words, primary button + grey secondary, optional text link; right: product image or looping product video | with a product visual. `--two-buttons` when Documentation is the secondary |
| 02 | Hero / Simple | eyebrow (the product name, `.superscript`), H1 6 to 9 words, paragraph 20 to 40 words, primary + grey secondary, "Works in" row (icons) | instead of 01 when there is no product visual (as on /ai/mcp-server and /ai/vise). Never both |
| 10 | Logo wall (`--marquee`) | customers from the CMS | optional; only with hero 01. With hero 02 the "Works in" row is the logo row; never both. Logos only from `assets/media/` or approved files; otherwise a text list |
| 13 | Card grid / Feature icons (`--v3-link-cards`) | heading H2 4 to 8 words (the value in one claim), optional intro; 3 or 6 cards with icon, title 3 to 6 words, 1 to 2 sentences; icon top-left above the title, never beside it | the value cards (live: "Full platform knowledge in every conversation", 3 cards). 12 Feature grid instead when there are 6 to 12 short features of a product with a Features collection |
| 17 | Accordion with image | heading H2 3 to 6 words; 3 to 5 steps or use cases, each a title, one sentence and its own image | how it works, or the use cases. 11 Two-column (`--three-rows`) instead when the 2 or 3 steps need a paragraph each. Until the use-case tabs proposal is approved (`../proposals/2026-10-07-use-case-tabs.md`), question-and-answer use cases are built here and the reply says so |
| 19 | Customer story strip | heading, intro, 3 to 5 stories from the CMS | optional: only when stories for this product exist. Never invented; a product without stories has no proof section |
| 23 | CTA band (inline, `--two-buttons`) | heading 2 to 6 words ("Start building"), one line, primary + grey | optional: the live AI pages have it; leave it out on a page with fewer than five content sections |
| 18 | FAQ accordion (`--border-top`) | 5 to 10 questions with one-paragraph answers | at least: what it is, what it works with, what data it reads or changes, who controls access, how to get started |
| G4 | Footer CTA band | heading, line | "Contact Sales" button, or the page's primary action (TO CHECK, see G4) |
| G5 | Footer | none (shared) | always |

Rules for the page:

- Dark background throughout; the only CTA colour is `--social--main-blue`. One primary button per section: hero, inline CTA band, footer CTA band, each with the same primary action. Beside the primary: one grey secondary (`.cta-button.c-grey`) and, at most, one text link. Two actions of equal weight (two blue buttons, two products to "connect") need approval from Stefan or Amadeus; until then one is primary and the other a grey button or a text link, and the reply says which choice was made.
- Hero: 01 with a real product visual (screenshot in the dark rounded frame, or a product video with poster), or 02 without one. Not a drawn diagram or an abstract illustration in the place of the product (`../../taste.md`, rule 4). When the product visual does not exist yet and the page must show where it goes, use the approved placeholder in 01: a rounded frame (`.product-video-wrapper` look: `--social--dark-gray-background`, 1px `--border--border-dark`, the same radius as the frame) with the centred label "Product visual to come" in `--text--text-color-grey-light`; mark it "placeholder" in the reply.
- Numbers in a visual (a mock dashboard, a sample answer) carry the visible label "Illustrative example" (`.text-size-tiny`, grey-light) next to the visual; real numbers carry their source. Product facts come from `messaging/product-capabilities.md`; the "Works in" list names only what the product supports today.
- The "Works in" row is 02's row as captured: each tool as its icon tile (the approved files in `../../assets/third-party/ai-tools/`, listed in `../../foundations/logo/foundation.md`) with the name beside it, then "+ Any MCP-compatible tool". A tool without an approved icon is the name only, never a redrawn or lettered stand-in; the reply names it so the team can add the file.
- Links that do not exist yet are `href="#"` with the visible text unchanged and an HTML comment or a reply note "link to come: <intended path>"; no invented URLs.
- Nothing is added between the sections. A page that needs more (a comparison, a pricing block, tabs) proposes the section first (see `../README.md`) and builds on the closest set section until it is approved.
- Before delivery, go through the definition of done in `../README.md`.

## Recipe: an SDK page

A page for one SDK on one platform (Chat SDK for iOS, Social SDK for Android, …), like https://www.social.plus/chat/sdk/ios. Fixed order. Nav (G1) and sub-nav (G2) above, footer CTA band (G4) and footer (G5) below.

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| G1 | Nav | none (shared) | always |
| G2 | Sub-nav | product family links | Chat or Social family |
| 01 | Hero / Product (`--two-buttons`) | H1 with the platform name, paragraph, Contact Sales + Documentation, product video | `<header>` tag on SDK pages |
| 10 | Logo wall (`--marquee`) | customers from the CMS | |
| 11 | Two-column (`--checklist`) | heading, paragraph, 3 to 5 checklist items, image | "Easily integrate … in your <platform> app" |
| 11 | Two-column (`--image-left`) | heading, paragraph, grey button "UI Kit", image | the open-source UI kit for the platform; radial-gradient background |
| 12 | Feature grid | heading, intro, grey button, CMS features | the same features as the product page |
| 11 | Two-column (`--video-cta`) | eyebrow "Discover more", heading, paragraph, grey button, video | points to the other SDK (Social or Chat) for the same platform |
| G4 | Footer CTA band | heading, line | "Contact Sales" button |
| G5 | Footer | none (shared) | always |

Rules for the page:

- Three two-column sections, in this order and with these variants; the image side alternates (right, left, right).
- One platform per page; the platform name appears in the H1 and in the checklist heading.
- Nothing else is added. An SDK page never carries pricing, a form or a customer story strip.

## Recipe: an industry page

A page for one industry (gaming, fintech, retail, sports, …), like https://www.social.plus/industry/gaming. Fixed order. Nav (G1) above (no sub-nav), footer CTA band (G4) and footer (G5) below.

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| G1 | Nav | none (shared) | always |
| 03 | Hero / Industry | H1, enlarged paragraph, Contact Sales, industry image | |
| 10 | Logo wall (grid) | customers from the CMS | 12 logos on desktop |
| 15 | Card grid / Plain | heading (the problem in one sentence), 4 problem cards | 2 columns |
| 17 | Accordion with image | heading, 3 steps with a title, a line and an image each | image left |
| 16 | Image-card grid | heading, 6 use cases with image, title, line | 3 columns, static |
| 13 | Card grid / Feature icons (v2) | heading, 8 or 16 icon cards | 4 columns |
| 20 | Why social.plus grid | heading, line, 5 reasons | |
| 11 | Two-column / Text + image | heading, paragraph, image | "Made for product teams that build fast" |
| 19 | Customer story strip | heading, intro, 5 stories | pick stories from the industry where they exist |
| G4 | Footer CTA band | heading, line | "Contact Sales" button |
| G5 | Footer | none (shared) | always |

Rules for the page:

- The industry sets the words and the images; the structure does not change between industries.
- Every claim in the problem cards and the numbers in the stories need a source. Product facts come from `messaging/product-capabilities.md`.
- Nothing is added between the sections; a page-specific idea is proposed first (see `../README.md`).

## Recipe: a /vs/ page

A page that compares social.plus with one named competitor, like https://www.social.plus/vs/circle. Fixed order, no extra sections. Nav (G1) above, footer CTA band (G4) and footer (G5) below.

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| G1 | Nav | none (shared) | always |
| 05 | Hero / vs | competitor tile image and name | left tile is always social.plus |
| 50 | vs / Statement band | heading (8 to 14 words), paragraph (60 to 90 words) | positions social.plus against the competitor in plain words |
| 10 | Logo wall (grid) | divider line text; customers from the CMS | 12 logos on desktop |
| 51 | vs / Side-by-side | heading; 3 to 5 blocks: title, paragraph, illustration | what social.plus delivers beyond the competitor |
| 52 | vs / Comparison table | heading, intro line; 3 to 5 categories; rows with Yes / No / short note | facts from `messaging/product-capabilities.md`; the competitor's facts need a source |
| 53 | vs / Customer stories + form | heading; 4 stories from the CMS; form title | the conversion point |
| 18 | FAQ accordion | 5 to 10 questions with one-paragraph answers | at least: difference, what each offers that the other does not, data ownership, migration |
| G4 | Footer CTA band | heading, line | "Contact Sales" button |
| G5 | Footer | none (shared) | always |

Rules for the page:

- Dark background throughout (`--social--dark`); the only CTA colour is `--social--main-blue`.
- The competitor is named plainly and compared on facts; no logos of the competitor beyond the hero tile and the table head.
- Nothing is added between the sections (no banners, no extra CTAs). If a /vs/ page needs more, propose a section first (see `../README.md`).

## Recipe: a blog post

A post on https://www.social.plus/blog/…, like https://www.social.plus/blog/10-common-online-community-challenges-and-how-to-overcome-them. Nav (G1) above, footer (G5) below; no footer CTA band on the live template.

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| G1 | Nav | none (shared) | always |
| 40 | Article (blog post) | tags, title, author, date, share buttons, intro, hero image, `.rich-text.c-blog` body, aside tile | body headings start at h2 |
| 30 | Thumbnail grid (`--related-aside`) | heading, 3 related posts from the CMS | |
| G5 | Footer | none (shared) | always |

Rules for the page:

- The body uses the rich-text style of the template as it is today (`.rich-text.c-blog`); no inline styling, no custom blocks beyond h2, h3, p, lists, blockquote, images, tables and links.
- Images in the body have alt text; one image at the top, the rest where the text needs them.
- No CTA band and no form on a blog post (as-is today; TO CHECK with Stefan or Amadeus whether the footer CTA band should be added to the template).

## Recipe: an answer page

A page on https://www.social.plus/answers/…, like https://www.social.plus/answers/api-for-adding-online-community-features-to-mobile-apps. Nav (G1) above, footer CTA band (G4) and footer (G5) below.

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| G1 | Nav | none (shared) | always |
| 40 | Article (`--answer`) | title (the question), hero image, `.answers_rich-text` body | one column, dark |
| G4 | Footer CTA band | heading, line | "Contact Sales" button |
| G5 | Footer | none (shared) | always |

Rules for the page:

- The question is the H1; the first paragraph answers it; the body follows the answers format of the content skills (`aeo-content`).
- No related grid, no form, no tags (as-is today).

## Recipe: a glossary entry

A page on https://www.social.plus/glossary/…, like https://www.social.plus/glossary/activity-feed. Nav (G1) above, footer (G5) below; no footer CTA band on the live template.

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| G1 | Nav | none (shared) | always |
| 04 | Article / Title header | breadcrumb (Glossary › term), H1 (the term) | |
| 43 | Glossary entry | table of contents, `.rich-text` body (definition first, then the fixed sections, at least one table) | |
| G5 | Footer | none (shared) | always |

Rules for the page:

- The body follows the glossary format of the content skills (`glossary-content`): 7 fixed sections, 500 to 900 words, answer-first definition.
- No images, no form, no CTA band (as-is today; TO CHECK with Stefan or Amadeus whether the footer CTA band should be added).

## Recipe: a customer story

A page on https://www.social.plus/customer-story/…, like https://www.social.plus/customer-story/activerse. Nav (G1) above, footer CTA band (G4) and footer (G5) below.

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| G1 | Nav | none (shared) | always |
| G3 | Breadcrumb bar | "Customer Stories" | dark |
| 41 | Customer story hero | customer logo, title, intro, 2 or 3 metrics, image | |
| 42 | Customer story body | aside facts and tags, rich text with h2 sections and images | |
| 19 | Customer story strip (`--six-stories`) | heading "More in-app communities powered by social.plus", 6 stories | |
| G4 | Footer CTA band | heading, line | "Contact Sales" button |
| G5 | Footer | none (shared) | always |

Rules for the page:

- Metrics in the hero are the customer's own numbers with their source in the body; nothing is rounded up.
- The story follows the case-study format of the content skills (`case-study`): challenge, solution, results.
- Nothing is added between the sections.

## Recipe: a product or feature landing page, framed

The framed version of the product landing recipe (`product-landing.md`): the same page type (Agentry, the MCP server, Vise, an add-on), built from the framed sections in `../framed/` on the web library's frame. This is the version to build since 12 October 2026; the captured version stays for reading the live AI pages. Never mix the two on one page. Fixed order; a section may be left out only where the table says "optional".

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| F01 | Navigation | none (shared) | always |
| F02 | Hero / Centered | eyebrow (the product name, Geist Mono), H1 6 to 9 words, lead 20 to 40 words, primary + secondary button, the "Works in" row under the buttons | when there is no product visual; the art-panel visual is left out |
| F03 | Hero / Split | eyebrow, H1 5 to 9 words, lead 25 to 45 words, primary + secondary, product visual in the art panel | instead of F02 when a real product visual exists. Never both |
| F04 | Logo wall (inline) | customers | optional; only with F03. With F02 the "Works in" row is the logo row |
| F07 | Feature grid | section header (eyebrow optional, H2 4 to 8 words: the value in one claim, optional lead); 3 or 6 cells, each an icon tile, a title of 3 to 6 words and 1 to 2 sentences | the value cells ("Your team asks. Your first-party data answers."): cells divided by frame lines, never cards |
| F06 | Feature tabs | section header (H2 3 to 6 words); 3 to 5 tabs, each a title, one or two sentences and its own visual | the use cases or how it works ("Every team's question, answered in seconds") |
| F12 | Customer stories (grid) | 3 stories from the CMS | optional: only when stories for this product exist; never invented |
| F14 | FAQ | 5 to 10 questions with one-paragraph answers | at least: what it is, what it works with, what data it reads or changes, who controls access, how to get started |
| F15 | CTA band | heading 2 to 6 words, one line, one primary button (the page's primary action) | always, last before the footer |
| F16 | Footer | none (shared) | always |

Rules for the page:

- One frame from the nav to the footer: every section is framed, none is a captured section, and no captured section is wrapped in the frame (the Grid and frame foundation).
- Inside the frame, content sits in cells divided by frame lines: no card fill, no radius, no gap between cells. Cards exist only outside the frame (a pop-up, a floating panel).
- Colours through the role tokens, type on the type scale, spacing on the steps and section paddings; eyebrows in Geist Mono. The art panel is the only gradient surface and sits only behind a product visual.
- One primary button per section: hero and CTA band with the same primary action. Two actions of equal weight need approval from Stefan or Amadeus.
- Numbers in a visual carry the visible label "Illustrative example"; product facts come from `messaging/product-capabilities.md`; the "Works in" row uses the approved icons in `../../assets/third-party/ai-tools/` and names only what the product supports today.
- Links that do not exist yet are `href="#"` with a note of the intended path. A visual that does not exist yet is the library's placeholder in the art panel, marked "placeholder" in the reply.
- Before delivery, go through the definition of done in `../README.md`.
