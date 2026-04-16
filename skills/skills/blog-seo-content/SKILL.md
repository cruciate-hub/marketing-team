---
name: blog-seo-content
description: >
  Write SEO-optimized blog posts and long-form articles for social.plus.
  Use this skill for: blog posts, thought leadership articles, SEO content,
  pillar pages, comparison articles ("social.plus vs X"), how-to guides,
  industry trend pieces, guest posts, or any long-form written content intended
  for the social.plus blog or external publication under the social.plus name.
  Trigger on phrases like "write a blog post", "SEO article", "thought leadership
  piece", "comparison article", "content marketing", "pillar page", or when the
  user wants long-form content that will be published on the web.
  Do NOT trigger for website page copy (use brand-messaging), email content
  (use newsletters), social media posts (use social-media), or customer stories
  (use case-study).
---

# social.plus Blog & SEO Content

This skill produces long-form, brand-aligned content for the social.plus blog. The output maps directly to the Webflow CMS collection fields so content can be pasted into the CMS without reformatting.

## What to do

1. Fetch the main brain for cross-domain routing, precedence rules, and the compliance check:
```
https://github.com/cruciate-hub/marketing-team/blob/main/brain.md
```

2. Fetch the messaging router:
```
https://github.com/cruciate-hub/marketing-team/blob/main/messaging/brain.md
```

3. Follow the messaging router's **"Long-form content"** routing. This loads:
   - `terminology.md` + `tone.md` (always)
   - `narrative.md` (messaging hierarchy and 5-step narrative structure)
   - `value-story.md` (differentiation framework, core problems)
   - `positioning.md` (company overview, product pillars)

4. `value-story.md` is already loaded via the long-form routing above. For comparison or competitive content, lean on its differentiation framework especially heavily.

5. If the article needs awareness of what the website already says (to avoid contradicting it, to link to relevant marketing pages, or to cross-link to existing blog posts), fetch any of these as relevant:
```
https://github.com/cruciate-hub/marketing-team/blob/main/website/pages-marketing.json
https://github.com/cruciate-hub/marketing-team/blob/main/website/pages-blog.json
https://github.com/cruciate-hub/marketing-team/blob/main/website/pages-glossary.json
```

`pages-blog.json` is especially useful for:
- **Avoiding duplicates** — check if a similar topic has been covered before; if yes, suggest updating the existing post rather than writing a new one
- **Internal links** — suggest 3-5 contextually relevant blog posts to link to from the new article (strengthens SEO)
- **Cross-topic references** — find adjacent content to reference (e.g., a "user retention" article linking to an existing "app engagement" post)

Each item in `pages-blog.json` has `url`, `metaTitle`, `metaDescription`, and `content` (heading hierarchy). Scan `metaTitle` and `content` for topic overlap.

## Webflow CMS field mapping

Every blog post is a CMS item in the `📖 Blog Posts` collection. When writing a blog post, produce content for each of these fields. Present each field clearly labeled so the user can paste directly into Webflow.

### Required fields

**Page title** (`name`, PlainText, max 256 chars)
This is the CMS item name AND the title tag (the blue link in Google search results). Keep under 60 characters for SEO. Front-load the target keyword.

**Slug** (`slug`, PlainText, max 256 chars)
URL-safe slug. Lowercase, hyphens, no spaces. Keep it short. Example: `best-chat-apis-messaging-sdks`, `building-your-in-app-community-why-it-matters`.

### Meta

**Meta description** (`meta-description`, PlainText, max 160 chars including spaces)
SEO meta description. Include the target keyword. Write a compelling reason to click — not a summary of the post.

### Content fields

**Introduction text** (`post-summary`, PlainText)
Bold introduction paragraph shown at the top of the blog page. 1-3 sentences that set the scene and hook the reader. This is NOT the meta description — it's longer and more narrative.

Examples from the live site:
- "Mobile app marketing is the process of promoting a mobile app to users to increase its visibility and encourage downloads. A successful mobile app marketing plan…"
- "Creating an engaged community within your app can become the differentiator keeping you ahead of the competition. Why should you invest in building your in-app community?"
- "OpenAI is embedding ecommerce into ChatGPT through product suggestions, in-chat purchasing links, and an autonomous shopping agent called Operator. The implications…"

**Post Content** (`post-content`, RichText)
The full article body. Uses standard HTML — no custom tags (unlike customer stories).

#### Content structure

Follow the narrative structure from `narrative.md`: Context → Tension → Infrastructure → Impact → Advantage. But expressed as blog structure:

1. **Opening paragraphs** (2-3 paragraphs) — Set the market context. Open with the shift or tension, not with "social.plus does X."
2. **H2 sections** — Each major point gets an H2 subheading. Use H3 for sub-points within a section.
3. **CTA section** — End with a clear next step. Link to a relevant social.plus product page.

#### HTML formatting rules

- Use `<h2>` and `<h3>` for subheadings. Place an H2 or H3 every 200-300 words.
- Use `<strong>` for emphasis within paragraphs. Don't overuse.
- Use `<a href="..." target="_blank">` for all links (external links open in new tab).
- Use `<ul>` and `<li>` for lists where appropriate.
- Inline images: use `<figure>` and `<img>` tags. Add alt text to every image. Leave image URLs as `[IMAGE_URL]` placeholders for the user to upload.
- No custom HTML tags. No `<sprscript-green>` (that's for customer stories only).

#### Content guidelines

- Target length: 5,000–12,000 characters (matching the typical range on the live blog).
- Include the target keyword in the H1 (page title), first paragraph of post-content, and at least one H2.
- Suggest 3-5 internal links to relevant social.plus pages.
- Never fabricate statistics, customer names, quotes, or performance claims.
- Never use emojis in blog content.

### Taxonomy

**Main Category Tag** (`category`, Reference → Blog Categories)
Tell the user which single primary category to select. Choose from:

| Category | Use when the post is about… |
|---|---|
| Community | Building, growing, or managing digital communities |
| App Growth | User acquisition, growth strategies, app marketing |
| Insights | Industry trends, thought leadership, market analysis |
| Engagement | User engagement, retention mechanics, social features |
| Retention | User retention, churn reduction, loyalty |
| Acquisition | User acquisition specifically |
| News | Company news, product announcements |
| Social+ | social.plus-specific content, product deep dives |
| Vertical Social Networks | Industry-specific social network strategies |
| Community Stories | Customer/community spotlight content |
| Monetization | Revenue models, monetization strategies |
| Education | EdTech, learning communities |
| Hospitality | Travel, hospitality industry |
| Events | Event-related content |
| People | Team profiles, culture content |

**Tags** (`category-multi-reference-3`, MultiReference → Blog Categories)
Tell the user which additional categories to tag. Always include the Main Category Tag plus 1-2 secondary tags. Example: Main = "Community", Tags = ["Community", "Engagement"].

### Author

**Author** (`author-reference`, Reference → Authors)
Recommend an author based on the topic:

| Author | Role | Best for |
|---|---|---|
| Napassorn Esharoe | Product Marketing Manager | Product-focused content, feature articles |
| Amadeus Noren | VP of Marketing | Strategic content, market analysis |
| Francesca Gargaglia | CEO | Vision pieces, company direction |
| Ivana Istochka | VP Community & Demand Generation | Community strategy, demand gen |
| social.plus Team | Generic byline | News, trend pieces, general content |

If no author fits, default to "social.plus Team."

### Reading time

**Minutes to read** (`min-read`, PlainText)
Calculate based on ~250 words per minute (aligned with LinkedIn's calculation as noted in the CMS help text). Round to nearest whole number.

### Images

The blog requires three image sizes, all 16:9 aspect ratio:

| Field | Slug | Dimensions | Use |
|---|---|---|---|
| Image \| Page Header | `image-page-header` | 1578 × 888 px | Top of the blog post page |
| Image \| Thumbnail grid | `grid-thumbnail` | 724 × 408 px | Blog overview grid |
| Image \| Mega Menu small thumbnail | `thumbnail-mega-menu` | 502 × 283 px | Navigation mega menu |

**Image alt text** (`image-alt-text`, PlainText)
Descriptive text that conveys the meaning and context of the visual. Not "decorative" — write a real description.

Tell the user what images are needed and at what sizes. Suggest a descriptive concept for the featured image that matches the article topic.

### Display controls

**Show as Featured** (`featured`, Switch)
Recommend yes/no. Only one post should be featured at a time on the blog overview — remind the user to disable the current featured post first.

**Blog without images** (`blog-without-images`, Switch)
Tell the user to toggle this if no header image is provided.

**Blog ID** (`blog-id-3`, PlainText)
Only needed if the blog must appear in a specific location on the site. Leave blank unless the user specifies.

### Careers page fields (only if relevant)

- **Show on Careers page** (`show-on-careers-page`, Switch)
- **Name Careers page** (`name-careers-page`, PlainText)
- **Description Careers page** (`description-careers-page`, PlainText)

Only populate these if the post is about company culture, hiring, or team content.

## Output format

Present the output as a clearly labeled field-by-field mapping. The user copies each value into the corresponding Webflow CMS field.

```
## [Article Title] — Blog Post

**Page title:** [value — under 60 chars for SEO]
**Slug:** [value]
**Date Published:** [today's date or user-specified]
**Main Category Tag:** [category name]
**Tags:** [list of category names]
**Author:** [author name]
**Minutes to read:** [number]

**Meta description:** [value — under 160 chars]

**Introduction text:**
[1-3 sentence intro paragraph]

**Post Content:**
[Full HTML body]

**Image alt text:** [value]
**Image concept:** [description of what the featured image should show]
**Image sizes needed:** 1578×888 (header), 724×408 (grid), 502×283 (mega menu)

**Display recommendations:**
- Featured: [yes/no]
- Blog without images: [yes/no]
- Blog ID: [value or "N/A"]
- Show on Careers page: [yes/no]
```

## What NOT to do

- Never fabricate statistics, customer names, quotes, or performance claims.
- Never position social.plus as a "social network" or "forum platform" (see terminology.md).
- Never use competitor names in a disparaging way — compare on facts and positioning only.
- Never use emojis in blog content.
- Never skip the taxonomy fields. Every post needs a category, tags, and author.
- Never use `<sprscript-green>` tags — those are for customer stories only.

## Before delivering

Run the compliance check from `brain.md`. Blog posts are high-visibility, long-lived content — terminology violations and tone drift compound over time.

## Important: URL format

**Always use `github.com/.../blob/...` URLs when fetching files.** Never attempt `raw.githubusercontent.com` — it is blocked by network egress settings.
