# Recipe: a /vs/ page

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
