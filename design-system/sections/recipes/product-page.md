# Recipe: a product page

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
