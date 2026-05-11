---
name: blog-seo-content
description: >
  Do NOT use this skill for AEO articles, GEO articles, answer pages, or any
  content destined for /answers/ — use aeo-content instead. This skill is for
  SEO blog posts only. aeo-content delivers .docx for /answers/; this skill
  delivers markdown for the blog.

  Use this skill for: blog posts that will be published on social.plus/blog.
  Trigger on phrases like "write a blog post" or "SEO article".
  Do NOT trigger for AEO/GEO/answer content (use aeo-content), website page copy
  (use brand-messaging), email content (use newsletters), or customer stories
  (use case-study).
---

# social.plus Blog & SEO Content

This skill produces brand-aligned blog posts for the social.plus blog. The output maps directly to the Webflow CMS collection fields so content can be pasted into the CMS without reformatting.

## How to fetch reference files

<!-- FETCH-BLOCK:START v2 -->
Reference files live in the public `cruciate-hub/marketing-team` GitHub repo. Fetch them by shallow-cloning the repo once per session, then loading individual files with `cat`. Use this exact pattern at the start of every skill that needs reference files:

    REPO="${MT_REPO:-/tmp/cruciate-hub-marketing-team}"
    if [ ! -d "$REPO/.git" ]; then
      git clone --depth 1 --quiet https://github.com/cruciate-hub/marketing-team.git "$REPO"
    else
      git -C "$REPO" pull --ff-only --quiet
    fi

After the clone exists, read files with `cat "$REPO/<path>"`. Examples: `cat "$REPO/brain.md"`, `cat "$REPO/messaging/terminology.md"`.

The Bash tool truncates large stdout when the output exceeds the harness's token/byte cap (observed at ~50 KB in Cowork; varies by environment). When this happens the harness emits one of these signals — both mean the same thing:
- `Output too large (NkB). Full output saved to: …` followed by a short preview, OR
- `Error: result (N characters) exceeds maximum allowed tokens` with no preview, just a sidecar-file pointer.

In either case, the rest of the file is invisible to you in-call. Most files in this repo are small enough that `cat` returns them in full and you never see either signal. **If you do see either form, never proceed using the partial output as if it were the whole file** — switch to one of the patterns below.

- **Truncated markdown** (you saw either truncation signal above) — read in line-range chunks instead. First check the total line count: `wc -l "$REPO/<path>"`. Then read each chunk:

      sed -n '1,250p'     "$REPO/<path>"
      sed -n '251,500p'   "$REPO/<path>"
      sed -n '501,$p'     "$REPO/<path>"

  Each ~250-line chunk fits under the preview cap. Concatenate the chunks mentally. For files much larger than 750 lines, add more chunks at 250-line intervals until you reach the total.

  **If a chunk itself comes back as a truncated preview** (output above the harness's display cap — visible as an "Output too large" or similar marker, with the rest spilled to a file you can't see in-call), halve the chunk size and retry. For example, swap `sed -n '1,250p'` for `sed -n '1,125p'` then `sed -n '126,250p'`. Repeat until each chunk lands in full. Never proceed using a truncated chunk as if it were complete.

- **Large JSON inventories** (`website/pages-*.json`, up to 228 KB) — never `cat` raw. Process with `python3` or `jq` and emit only the fields you need:

      python3 -c "import json; d=json.load(open('$REPO/website/pages-blog.json')); print(len(d['pages']))"
      jq '.pages[].url' "$REPO/website/pages-blog.json"

  Skill helper scripts (e.g. `scripts/duplicate_check.py`) already follow this pattern.

Note: Claude Code's `Read` tool can't reach files in `$REPO` — Cowork sandboxes Read to connected directories and `/tmp` is not connected by default. Use the `cat` / `sed` / `python` patterns above.

Validate every file before using it:
- Markdown: content must start with `#`
- JSON: content must start with `{` or `[`
- HTML: content must start with `<`
- Content must be non-empty

If anything fails — clone error, missing file, empty content, or wrong format:
- Do NOT reconstruct from memory or training data.
- Do NOT fall back to WebFetch or any other tool.
- Stop immediately and respond with exactly this line:

  `Fetch failed: <path>. Please check your network connection and rerun.`
<!-- FETCH-BLOCK:END v2 -->

## What to do

1. Fetch `brain.md` for cross-domain routing, precedence rules, and the compliance check.

2. Fetch `messaging/brain.md` (the messaging router).

3. Follow the messaging router's **"Long-form content"** routing. This loads:
   - `terminology.md` + `tone.md` (always)
   - `narrative.md` (messaging hierarchy and 5-step narrative structure)
   - `value-story.md` (differentiation framework, core problems)
   - `positioning.md` (company overview, product pillars)

4. `value-story.md` is already loaded via the long-form routing above. For comparison or competitive content, lean on its differentiation framework especially heavily.

5. If the article needs awareness of what the website already says (to avoid contradicting it or to find adjacent content to reference), fetch any of these as relevant:
   - `website/pages-marketing.json`
   - `website/pages-industry.json`
   - `website/pages-blog.json`
   - `website/pages-glossary.json`

These fetches serve **content awareness** (not linking — internal linking is handled by the `internal-linking-strategist` skill in a dedicated step). Use them for:
- **Avoiding duplicates** — check if a similar topic has been covered before; if yes, suggest updating the existing post rather than writing a new one.
- **Cross-topic references** — find adjacent content to reference (e.g., a "user retention" article that mentions concepts from an existing "app engagement" post).
- **Tone and terminology calibration** — see how similar topics have been written about previously.

Each item has `url`, `metaTitle`, `metaDescription`, and `content` (heading hierarchy). Scan `metaTitle` and `content` for topic overlap.

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
- Internal links: do NOT improvise. Internal links are inserted by the `internal-linking-strategist` skill in a dedicated step before delivery (see "Internal links" section below). Write the draft without internal links; the optimizer adds 3-7 SEO-grounded `<a href>` tags using the canonical anchor map and cannibalization warnings in `link-strategy.md`.
- Never fabricate statistics, customer names, quotes, or performance claims.
- Never use emojis in blog content.

### Taxonomy

**Main Category Tag** (`category`, Reference → Blog Categories)
Tell the user which single primary category to select. Choose from:

| Category | Use when the post is about… |
|---|---|
| Community | Building, growing, or managing digital communities |
| App Growth | User acquisition, growth strategies, app marketing |
| Insights | Industry trends and market analysis |
| Engagement | User engagement, retention mechanics, social features |
| Retention | User retention, churn reduction, loyalty |
| Acquisition | User acquisition specifically |
| News | Company news, product announcements |
| Product | Product-focused content, feature deep dives, product announcements |
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

## Internal links

After writing the draft and before the compliance check, invoke the `internal-linking-strategist` skill in **draft mode**. Pass it:

- The full draft article (title + post-content HTML + post-summary)
- The target keyword
- The category (so it can map to the correct topic cluster)
- Content type: blog (so it returns HTML `<a href>` tags, not markdown)

The optimizer fetches `link-strategy.md` plus `pages-marketing.json`, `pages-use-cases.json`, `pages-industry.json`, `pages-glossary.json`, `pages-blog.json`, and `pages-customer-stories.json`. It returns 3-7 link suggestions (anchor + URL + insertion point + reasoning) plus any cannibalization warnings.

Embed each suggestion into the `post-content` HTML as `<a href="..." target="_blank">anchor</a>` at the suggested insertion point.

Resolve cannibalization warnings before final output:
- If the optimizer flags a competing anchor → page mapping, follow its recommendation.
- If the draft's primary keyword is itself flagged as cannibalized, surface this to the user before delivering — it may affect the publishing decision.

Never improvise internal links — the optimizer is the source of truth. The 3-7 link target is a guideline, not a quota: if the optimizer returns 4 strong suggestions, use 4.

## Before delivering

Run the compliance check from `brain.md`. Blog posts are high-visibility, long-lived content — terminology violations and tone drift compound over time.

