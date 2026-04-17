# Blog SEO Content

Claude skill for writing long-form, SEO-optimized blog posts and articles for the social.plus blog.

Output maps directly to the Webflow CMS `📖 Blog Posts` collection fields so content can be pasted in without reformatting — page title, slug, meta description, introduction, post content HTML, taxonomy, author, reading time, image specs.

## What it does

- Fetches the full messaging stack via the brain + router — terminology, tone, narrative, value-story, positioning.
- Checks `website/pages-blog.json` for duplicate topics; suggests updating an existing post when a close match exists.
- Recommends 3–5 internal links from the existing blog inventory to strengthen SEO.
- Produces clean HTML body copy (5,000–12,000 characters) following the Context → Tension → Infrastructure → Impact → Advantage narrative structure.
- Labels every CMS field so the user can copy-paste into Webflow field-by-field.

## When it triggers

When the user wants long-form written content that will be published on the web. Trigger phrases include "write a blog post", "SEO article", "thought leadership piece", "comparison article", "content marketing", "pillar page", or any long-form blog-style request.

The skill is not for website page copy (use `brand-messaging`), email content (use `newsletters`), social media posts (use `social-media`), or customer stories (use `case-study`).

## Workflow

1. Fetch `brain.md` and `messaging/brain.md`. Follow the **"Long-form content"** routing to load terminology, tone, narrative, value-story, and positioning.
2. For comparison or competitive content, lean on `value-story.md`'s differentiation framework.
3. If the article needs site-awareness (to avoid contradictions or add internal links), fetch any of `website/pages-marketing.json`, `pages-industry.json`, `pages-blog.json`, `pages-glossary.json`.
4. Scan `pages-blog.json` `metaTitle` + `content` for topic overlap before drafting.
5. Produce every CMS field labeled clearly for copy-paste into Webflow.
6. Run the compliance check from `brain.md` before delivering.

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
- **Main Category Tag** (single primary category — Community, App Growth, Insights, Engagement, Retention, Acquisition, News, Social+, Vertical Social Networks, Community Stories, Monetization, Education, Hospitality, Events, People)
- **Tags** (main category + 1–2 secondary)

### Author
Recommend based on topic:

| Author | Role | Best for |
|---|---|---|
| Napassorn Esharoe | Product Marketing Manager | Product-focused content, feature articles |
| Amadeus Noren | VP of Marketing | Strategic content, market analysis |
| Francesca Gargaglia | CEO | Vision pieces, company direction |
| Ivana Istochka | VP Community & Demand Generation | Community strategy, demand gen |
| social.plus Team | Generic byline | News, trend pieces, general content |

Default to "social.plus Team" when no author fits.

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

- **Length:** 5,000–12,000 characters (matches existing blog posts on the live site).
- **Keyword placement:** target keyword in H1 (page title), first paragraph of post-content, and at least one H2.
- **Internal links:** suggest 3–5 relevant social.plus pages (strengthens SEO).
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
**Author:** [author name]
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

Always fetch via `github.com/.../blob/...` URLs. Never use `raw.githubusercontent.com` — blocked by network egress.
