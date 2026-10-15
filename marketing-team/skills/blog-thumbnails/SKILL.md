---
name: blog-thumbnails
description: Editorial images for social.plus blog posts — blog headers and thumbnails, in-blog (inline) images such as data charts and flow diagrams, plus answer-page images and glossary in-article images — in the social.plus illustration system with the editorial grain treatment. Use whenever someone asks for a blog thumbnail, blog header, featured image, cover/OG image for an article, in-blog or inline images, charts or diagrams for an article, or "visuals for this post", even with only a title or a URL. Builds on the social-plus-illustration skill (read it first); for a moving version or a reel from the post, hand over to social-plus-motion.
---

# Blog thumbnails

Editorial images for posts. The visual language, ideation method and review checklist live in **social-plus-illustration** — read its SKILL.md and references first (find it in the available skills list). This skill adds what is specific to blog images.

## Specifics

- **Treatment: grain on**, over the whole image (shell `grain` default 0.9).
- **Files the blog CMS requires** (Webflow blog collection, from blog-seo-content's `webflow-fields.json`; each field validates exact size, so anything else is rejected):

  | Field | Use | Size | File name |
  |---|---|---|---|
  | `image-page-header` | header on the post page | 1578×888 | `{slug}_page-header_1578x888.webp` |
  | `grid-thumbnail` | blog grid card | 724×408 | `{slug}_thumbnail_724x408.webp` |
  | `thumbnail-mega-menu` | navigation mega-menu | 502×283 | `{slug}_mega-menu_502x283.webp` |

  Format **WebP**. Design at 1578×888; check every concept at 502px, the smallest place it appears. **Answer pages**: one optional image, 1240×840 WebP, field `image-2`, named `{slug}_answer_1240x840.webp` — design it on a 1240×840 artboard and export with `--answers`. **Glossary**: the collection has no image field, so glossary images only go inside the article body, as in-blog images (1578×888, `--inline N`).
- **Logos**: when the post is about named companies or technologies, their official logos are part of the image (see step 1).
- **Text**: the title sits next to the image on the site, so no headline inside it. Readable words only per `content-and-locale.md`; a number only if the post quotes it.
- **Canvas naming**: one Design canvas per post titled `Blog thumbnail: <post title>`; artboards `Concept A — <archetype>: <focal object>`.

## In-blog images

When asked for images inside the article, read `references/in-blog-images.md`. They are descriptive, not atmospheric: charts of the article's own data, flows of the processes it describes, labelled system diagrams, annotated UI — as many as the article warrants (decided per article: candidates per section, filtered for clean data, related stats merged, spaced out — see the reference), 1578×888, `{slug}_img-N_1578x888.webp`, grain on. Build them on the same canvas as the thumbnail concepts, on a second row titled "In-blog images".

## Workflow

1. **Read the whole post** (the full article is normally provided; given a URL, fetch it). State your reading of the claim in one line. Title only and the argument isn't obvious: ask one question.
   - **List the companies and technologies the post is about** — a tutorial's technology (Flutter), the products a listicle compares (all six chat SDKs), both sides of a migration. Their logos go in the thumbnail, per the master's `third-party-logos.md`: official files only, never drawn from memory; ask for any you don't have, in the same message as the concepts, and build with neutral placeholder tiles until they arrive. Names only from the article itself — never guessed from the title.
2. **Variety check**: `Artifact` `list` (scope "mine", then "all"), find canvases titled `Blog thumbnail: …`, read the `project/canvas.json` of the 3–5 most recent. Your two concepts must use archetypes not used by the last 3 chosen thumbnails, and not reuse the last focal object. Note the recent thumbnails' accent colors too, and pick this one's accent by meaning within the balance rules (master's `color-accents.md`).
3. **Ideate** with the master's `ideation.md`: idea table (10 ideas, 8 lenses), crossed-out pairings, 2 picks as five-line briefs.
4. **Build** both artboards from the master's `assets/shell.dc.html`, grain on.
5. **Review** with the master's `review-checklist.md`, then present: one line per concept, recommendation, trade-off.
6. **Export**: thumbnail — run `scripts/export_blog_images.py <artboard.dc.html> --slug <post-slug> --fonts <social-plus-illustration>/assets/fonts [--assets <folder of logo files named by blob id>]` on the chosen artboard (read it back from the canvas first). It renders each size natively, so grain and type stay crisp, lightens the grain on the smaller sizes (strength × (width/1578)^0.75, so the 724 and 502 images feel as grainy as the header, not heavier; `--grain-falloff` tunes it), and writes the three WebP files with the exact names and sizes above; present them (`present_files` on claude.ai; in Claude Code, list the output paths). These are the files webflow-publisher uploads. In-blog images — the same script with `--inline N` writes `{slug}_img-N_1578x888.webp` only. A loop of the chosen image → social-plus-motion (thumbnail loop).

`references/worked-examples.md` records how earlier posts went, including the feedback rounds to pre-empt.
