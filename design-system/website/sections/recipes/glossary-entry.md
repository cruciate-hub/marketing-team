# Recipe: a glossary entry

A page on https://www.social.plus/glossary/…, like https://www.social.plus/glossary/activity-feed. Nav (G1) above, footer (G5) below; no footer CTA band on the live template.

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| G1 | Nav | none (shared) | always |
| 04 | Article / Title header | breadcrumb (Glossary › term), H1 (the term) | |
| 43 | Glossary entry | table of contents, `.rich-text` body (definition first, then the fixed sections, at least one table) | |
| G5 | Footer | none (shared) | always |

Rules for the page:

- The body follows the glossary format of the content skills (`glossary-content`): 7 fixed sections, 500 to 900 words, answer-first definition.
- No images, no form, no CTA band (as-is today; TO CHECK with Amadeus whether the footer CTA band should be added).
