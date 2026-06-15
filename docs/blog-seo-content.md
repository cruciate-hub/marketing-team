# Blog SEO Content

Claude skill for writing SEO-optimized blog posts for social.plus/blog.

Output maps directly to the Webflow CMS `📖 Blog Posts` collection fields so content can be pasted in without reformatting — page title, slug, meta description, introduction, post content HTML, taxonomy, reading time, image specs.

## What it does

- Fetches the full messaging stack via the brain + router — terminology, tone, narrative, value-story, positioning.
- Checks `website/pages-blog.json` for duplicate topics; suggests updating an existing post when a close match exists.
- Delegates internal links to the `internal-linking-strategist` skill before delivery — the optimizer returns 3–7 SEO-grounded `<a href>` tags via the canonical anchor map in `link-strategy.md`.
- Produces clean HTML body copy (5,000–12,000 characters) following the Context → Tension → Infrastructure → Impact → Advantage narrative structure.
- Runs a **two-stage production flow**: drafts a markdown intermediate, checks it with a deterministic script (`scripts/compliance.py` — em dashes, emojis, brand casing, forbidden terminology, length, slug, heading hierarchy), then converts the body to HTML. The script is an additional gate on top of the brain.md terminology/tone review, not a replacement.
- Labels every CMS field so the user can copy-paste into Webflow field-by-field.

## When it triggers

When the user wants a blog post for social.plus/blog on a **non-product topic** — industry trends, opinion pieces, listicles, third-party tools, general community/social-engagement subjects. Trigger phrases include "write a blog post about [non-product topic]", "SEO article on [trend]", "listicle", "opinion piece", or "how-to / tutorial on a general topic".

The skill is **not** for:
- Blog posts about a social.plus product, feature, module, or capability (e.g. "blog post on the Block feature", "article about our AI Copilot") — use `brand-messaging`, which owns all product content regardless of format (blog, page, CMS item).
- AEO/answer pages for `/answers/` (use `aeo-content`).
- Website page copy (use `brand-messaging`).
- Email content (use `newsletters`).
- Customer stories (use `case-study`).
- Press releases (use `press-release`).

## Workflow

1. Fetch `brain.md` and `messaging/brain.md`. Load `terminology.md`, `tone.md`, `positioning.md`, `value-story.md`, and `narrative.md` from `messaging/`.
2. For comparison or competitive content, lean on `value-story.md`'s differentiation framework.
3. If the article needs site-awareness (to avoid contradicting existing pages or to find adjacent topics to reference), fetch any of `website/pages-marketing.json`, `pages-industry.json`, `pages-blog.json`, `pages-glossary.json`.
4. Scan `pages-blog.json` `metaTitle` + `content` for topic overlap before drafting.
5. Draft the **markdown intermediate** at `outputs/[slug].draft.md` — H1 title, labeled-paragraph metadata, markdown body.
6. Run `python3 scripts/compliance.py outputs/[slug].draft.md` and fix every failure (exit 1) before continuing. This is the mechanical gate; the brain.md terminology + tone review still applies in full.
7. Convert the markdown body to HTML (wrap images in `<figure>`, add `target="_blank"` to links, disable smart punctuation so it can't reintroduce em dashes).
8. Invoke `internal-linking-strategist` in **draft mode** on the HTML — it returns 3–7 SEO-grounded `<a href>` tags (anchor + URL + insertion point) using the canonical anchor map in `link-strategy.md`. Before embedding each anchor, vet its visible text with `python3 scripts/compliance.py --scan-text 'anchor text'`; reject and request a replacement on any FAIL (the linker runs after the draft.md compliance pass, so its output otherwise bypasses the gate).
9. Embed cleared anchors in `post-content` and deliver every CMS field labeled clearly for copy-paste into Webflow.

## Webflow CMS fields

Every blog post is a CMS item in `📖 Blog Posts`. The skill produces each field:

### Required
- **Page title** (`name`, ≤256 chars, ideally ≤60 for SEO — front-load target keyword)
- **Slug** (`slug`, lowercase-hyphens)

### Meta
- **Meta description** (`meta-description`, ≤160 chars — compelling reason to click, not a summary)

### Content
- **Introduction text** (`post-summary`, 1–3 sentence narrative hook shown at the top of the page)
- **Post Content** (`post-content`, RichText HTML — `<h2>`/`<h3>` every 200–300 words, `<strong>` sparingly, `<a target="_blank">` on links, `<figure>`/`<img>` for inline images with `[IMAGE_URL]` placeholders)

### Taxonomy
- **Main Category Tag** (single primary category — Community, App Growth, Insights, Engagement, Retention, Acquisition, News, Product, Social+, Vertical Social Networks, Community Stories, Monetization, Education, Hospitality, Events, People)
- **Tags** (main category + 1–2 secondary)

### Reading time
**Minutes to read** — calculated at ~250 words/minute, rounded.

### Images
Three 16:9 sizes required:

| Field | Dimensions | Use |
|---|---|---|
| Image \| Page Header | 1578 × 888 px | Top of the blog post page |
| Image \| Thumbnail grid | 724 × 408 px | Blog overview grid |
| Image \| Mega Menu small thumbnail | 502 × 283 px | Navigation mega menu |

Plus `image-alt-text` (real description, not "decorative") and a suggested image concept matching the article topic.

### Display controls
- **Show as Featured** — only one featured post at a time; remind the user to disable the current featured post first.
- **Blog without images** — toggle if no header image is provided.
- **Blog ID** — only if the post must appear in a specific location.

### Careers page fields (only if relevant)
- Show on Careers page, Name Careers page, Description Careers page — populated only for culture/hiring/team content.

## Content rules

- **Length:** 5,000–12,000 characters (matches existing blog posts on the live site). The compliance script flags posts under 900 or over 2,200 words as an advisory `WARN`.
- **Keyword placement:** target keyword in H1 (page title), first paragraph of post-content, and at least one H2.
- **Internal links:** delegated to `internal-linking-strategist` — it returns 3–7 anchor + URL + insertion-point suggestions using the canonical map in `link-strategy.md`. Never improvise.
- **No `<sprscript-green>` tags** — those are for customer stories only.
- **No emojis.**
- **No fabricated statistics, customer names, quotes, or performance claims.**
- **No disparaging competitor comparisons** — compare on facts and positioning only.

## Output format

A clearly labeled field-by-field mapping. Example:

```
## [Article Title] — Blog Post

**Page title:** [value — under 60 chars for SEO]
**Slug:** [value]
**Main Category Tag:** [category]
**Tags:** [list]
**Minutes to read:** [number]

**Meta description:** [value — under 160 chars]

**Introduction text:**
[1-3 sentence intro]

**Post Content:**
[Full HTML body]

**Image alt text:** [value]
**Image concept:** [description]
**Image sizes needed:** 1578×888, 724×408, 502×283

**Display recommendations:**
- Featured: [yes/no]
- Blog without images: [yes/no]
```

## URL format

All reference files are loaded from a shallow clone of this repo (`git clone --depth 1`) into `$MT_REPO`. The canonical fetch block at the top of each SKILL.md handles the clone; skills then read files with `cat "$MT_REPO/<path>"`.

## Boundary with `aeo-content`

This skill and `aeo-content` are explicitly separated to prevent router collisions. In a real Cowork session, a colleague typed "write an AEO article on ..." and the router loaded `blog-seo-content` instead — "AEO" and "SEO" differ by one letter, and this skill's trigger list was dominating the embedding match. Both skills' `description:` fields now include explicit anti-triggers pointing at each other. This skill is for SEO blog posts only; AEO articles go through `aeo-content` and deliver a `.docx` for the `/answers/` collection, not markdown for the blog. **Do not remove the AEO exclusion from this skill's description without making the matching edit in `aeo-content/SKILL.md`** — drop one side and the collision returns. Any request mentioning AEO, GEO, answer pages, `/answers/`, AI citation, or AI search must route to `aeo-content`, not here.
