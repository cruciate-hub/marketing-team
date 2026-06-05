# Webflow Configuration — Blog Publisher

## Site

| Key | Value |
|---|---|
| Site ID | `66e2765d540e1939a89db4bb` |
| Blog collection ID | `66e2765d540e1939a89db6a4` |
| API base | `https://api.webflow.com/v2` |
| Auth header | `Authorization: Bearer $WEBFLOW_API_TOKEN` |

## Blog Post Field Slugs

### Required (must always be present)

| Display name | Slug | Type | Notes |
|---|---|---|---|
| Page title | `name` | PlainText | Title tag + CMS item name. Max 60 chars for SEO. |
| Slug | `slug` | PlainText | URL path. Lowercase, hyphens only. No spaces or special chars. |

### Content fields

| Display name | Slug | Type | Notes |
|---|---|---|---|
| Introduction text | `post-summary` | PlainText | Bold intro paragraph. 1–3 sentences. |
| Post Content | `post-content` | RichText | Full body as HTML. |
| Meta description | `meta-description` | PlainText | Max 160 chars including spaces. |
| Minutes to read | `min-read` | PlainText | Whole number as a string, e.g. `"12"`. |
| Date Published | `date-published` | DateTime | ISO 8601, e.g. `"2026-06-04T00:00:00.000Z"`. |

### Image fields (16:9, exact pixel dimensions)

| Display name | Slug | Dimensions | Notes |
|---|---|---|---|
| Image \| Page Header | `image-page-header` | 1578 × 888 px | Set as `{fileId, url, alt: null}` (matches production). |
| Image \| Thumbnail grid | `grid-thumbnail` | 724 × 408 px | Set as `{fileId, url, alt: null}`. |
| Image \| Mega Menu | `thumbnail-mega-menu` | 502 × 283 px | Set as `{fileId, url, alt: null}`. |
| Image alt text | `image-alt-text` | PlainText | The accessible description. `alt` inside each image object stays `null`; this standalone field holds the real alt text. |

Note: the skill targets these fields by **slug**, never by display name — so renaming a
field's label in the Designer (e.g. "Image | Mega Menu small thumbnail" → "Image | Mega Menu")
has no effect on publishing.

### Taxonomy

| Display name | Slug | Type | Notes |
|---|---|---|---|
| Main Category Tag | `category` | Reference | Single item ID string. |
| Tags | `category-multi-reference-3` | MultiReference | Array of item ID strings. Always include the Main Category Tag. |

### Switches (all default `false`)

| Display name | Slug |
|---|---|
| Blog without images | `blog-without-images` |
| Show as Featured | `featured` |
| Show on Careers page | `show-on-careers-page` |

## Category IDs

| Category | ID |
|---|---|
| Acquisition | `66e2765d540e1939a89dc2e9` |
| App Growth | `66e2765d540e1939a89dc04c` |
| Community | `66e2765d540e1939a89dc049` |
| Community Stories | `66e2765d540e1939a89dc2e8` |
| Education | `66e2765d540e1939a89dc2eb` |
| Engagement | `66e2765d540e1939a89dc04b` |
| Events | `66e2765d540e1939a89dc48f` |
| Hospitality | `66e2765d540e1939a89dc2e3` |
| Insights | `66e2765d540e1939a89dbfd7` |
| Monetization | `66e2765d540e1939a89dc2e5` |
| News | `66e2765d540e1939a89dc2e6` |
| People | `66e2765d540e1939a89dc029` |
| Product | `69d8d99d7d17ee9ca3ede77f` |
| Retention | `66e2765d540e1939a89dc2ea` |
| Social+ | `66e2765d540e1939a89dc2e2` |
| Vertical Social Networks | `66e2765d540e1939a89dc2e7` |
