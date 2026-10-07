# Recipe: a blog post

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
- No CTA band and no form on a blog post (as-is today; TO CHECK with Amadeus whether the footer CTA band should be added to the template).
