# Webflow Configuration — Blog Publisher

**Source of truth: `marketing-team/skills/webflow-publisher/collections/blog.json`.** The
scripts read every ID, field slug and category ID from that file; nothing below is read by
code. This page is the human-readable companion — field notes and display names — and must
be kept in step with the JSON when a field changes.

## Site

| Key | Value |
|---|---|
| Site ID | `66e2765d540e1939a89db4bb` |
| Blog collection ID | `66e2765d540e1939a89db6a4` |
| API base | `https://api.webflow.com/v2` |
| Auth header | `Authorization: Bearer $WEBFLOW_API_TOKEN` |
| Live URL prefix | `https://www.social.plus/blog/` |

## Blog Post Field Slugs

### Required (must always be present)

| Display name | Slug | Type | Notes |
|---|---|---|---|
| Page title | `name` | PlainText | Title tag + CMS item name. Max 60 chars for SEO. From the intermediate's `# Title`. |
| Slug | `slug` | PlainText | URL path. Lowercase, hyphens only. Never a year, never the leading listicle count (`slug_rules`). |

### Content fields

| Display name | Slug | Type | Notes |
|---|---|---|---|
| Introduction text | `post-summary` | PlainText | Bold intro paragraph. 1–3 sentences. The first paragraph of the intermediate (`fields.intro`). |
| Post Content | `post-content` | RichText | Full body as HTML (`fields.body`). |
| Meta description | `meta-description` | PlainText | Max 160 chars including spaces (`max_length`). |
| Minutes to read | `min-read` | PlainText | Whole number as a string, e.g. `"12"`. Defaults to `"5"` when the doc has none. |
| Date Published | `date-published` | DateTime | ISO 8601, e.g. `"2026-06-04T00:00:00.000Z"` (`fields.date`, set at conversion). |

### Image fields (16:9, exact pixel dimensions)

| Display name | Slug | Role | Dimensions | Notes |
|---|---|---|---|---|
| Image \| Page Header | `image-page-header` | `header` | 1578 × 888 px | Set as `{fileId, url, alt: null}` (matches production). |
| Image \| Thumbnail grid | `grid-thumbnail` | `grid` | 724 × 408 px | Set as `{fileId, url, alt: null}`. |
| Image \| Mega Menu | `thumbnail-mega-menu` | `menu` | 502 × 283 px | Set as `{fileId, url, alt: null}`. |
| Image alt text | `image-alt-text` | — | PlainText | The accessible description. `alt` inside each image object stays `null`; this standalone field holds the real alt text. |

Inline body images: 1578 × 888 px, inside `post-content` as a full-width `<figure>`
(`inline_images` in the field map).

Note: the skill targets these fields by **slug**, never by display name — so renaming a
field's label in the Designer (e.g. "Image | Mega Menu small thumbnail" → "Image | Mega Menu")
has no effect on publishing.

### Taxonomy

| Display name | Slug | Type | Notes |
|---|---|---|---|
| Main Category Tag | `category` | Reference | Single item ID string. First valid name on the doc's `Main Category Tag:` line. |
| Tags | `category-multi-reference-3` | MultiReference | Array of item ID strings. Always includes the Main Category Tag (`must_include`). |

### Switches (all default `false`)

| Display name | Slug |
|---|---|
| Blog without images | `blog-without-images` |
| Show as Featured | `featured` |
| Show on Careers page | `show-on-careers-page` |

### Optional fields the scripts never set

| Display name | Slug | Set by |
|---|---|---|
| Related webinar | `related-webinar-to-show-on-page` | blog-publisher Phase 6 (added to `fielddata.json` by hand) |
| Blog ID | `blog-id-3` | user, if the post must appear in a specific location |
| Name / Description Careers page | `name-careers-page`, `description-careers-page` | user, careers content only |

## Category IDs

The 16 category name → item ID pairs live in `collections/blog.json` under
`taxonomies.categories` and are resolved by the converter (case-insensitive). Look one up:

```bash
python3 -c "import json;print(json.load(open('$REPO/marketing-team/skills/webflow-publisher/collections/blog.json'))['taxonomies']['categories'])"
```

To add a category created in Webflow: add its display name and item ID to that object (and
mention it in blog-seo-content's "Main Category Tag" list). An unknown name on the doc's
`Main Category Tag:` line is skipped with a warning; if none resolve, conversion stops.
