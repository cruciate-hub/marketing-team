# Blog Publisher

Claude skill for publishing a completed blog article from Google Docs to the social.plus Webflow blog — live immediately, or `--staged` for review first. Also refreshes hero images on existing posts with `--update`.

Handles the full pipeline end-to-end: reads the doc, converts to Webflow-clean HTML, adds SEO-grounded internal links, resizes the master PNG to all three required image sizes, uploads assets to Webflow via the Data API v2, and publishes the CMS item immediately.

## What it does

- Reads the source article from Google Docs using the Google Drive MCP (no copy-paste required).
- Detects multiple articles in one doc (e.g. a listicle batch) and lets the user pick which to publish.
- Converts the doc's markdown-like content to Webflow Rich Text HTML: headings, lists, tables, bold, links — following the rules in `html-conversion.md`.
- Invokes `internal-linking-strategist` in draft mode to add 3–7 SEO-grounded internal links before publish.
- Runs the standard compliance check (terminology, tone, no fabricated claims, no em dashes).
- Validates the master image (≥ 1578 px wide, ~16:9), then resizes and converts to WebP via the `resize_blog_images.py` helper (Pillow — macOS `sips` cannot write WebP) — producing three files named `{slug}_page-header_1578x888.webp`, `{slug}_thumbnail_724x408.webp`, `{slug}_mega-menu_502x283.webp`.
- Uploads all three images to the Webflow asset library via the three-step upload process (MD5 hash → asset metadata API → S3 multipart POST).
- Publishes the blog post immediately via `POST /v2/collections/{id}/items/live` — never creates a draft.
- Prints the live URL and CMS item ID on success.

## When it triggers

"Publish blog", "post to Webflow", "upload article to CMS", "put this live", "the article is ready", "publish listicle [N]".

Must have a Google Doc URL/ID and a PNG file path. If either is missing, the skill asks before proceeding.

If the user asks to write AND publish, run `blog-seo-content` first, then this skill.

## Prerequisites

| Requirement | How to set it up |
|---|---|
| `WEBFLOW_API_TOKEN` env var | Webflow → Site Settings → Integrations → API Access. Token must have **cms:write** AND **assets:write** scopes. |
| Python 3 | The publish script is standard-library only — no `pip install`, no virtualenv. |
| Pillow (for resizing) | The resize helper checks for it and prints the install command if missing. The publish script itself is stdlib-only. |
| Google Drive MCP connected | Needed to read the Google Doc. The doc must be shared with the account the MCP is authenticated as. |

## Inputs

1. **Google Doc ID** — from the URL: `docs.google.com/document/d/{DOC_ID}/edit`
2. **PNG file path** — absolute path to the master image. Must be ≥ 1578 px wide.

## Pipeline

| Phase | What happens |
|---|---|
| 1. Read doc | Google Drive MCP reads the article. If multiple articles are in the doc, user picks one. |
| 2. Convert to HTML | Markdown-like doc content → Webflow Rich Text HTML (headings, lists, tables, links). |
| 3. Internal linking | `internal-linking-strategist` adds 3–7 `<a href>` tags grounded in `link-strategy.md`. |
| 4. Compliance check | Terminology, tone, claims, em dashes, emojis — all fixed before proceeding. |
| 5. Resize images | `resize_blog_images.py` validates the master and emits all exact WebP sizes (Pillow). |
| 6. Upload assets | 3-step Webflow upload (MD5 → asset API → S3) × 3 images. |
| 7. Publish live | `POST /items/live` with all 22 CMS fields populated. Prints live URL + item ID. |

## What it does NOT do

- Does not write blog content — use `blog-seo-content` for that, then hand the result here.
- Publishes live by default; `--staged` creates the item for review (goes live on the next site publish). A side-effect-free `--dry-run` validates everything first.
- Does not trigger a full Webflow site publish. After the CMS item is live, trigger a manual Webflow publish to refresh the CDN and regenerate `website/pages-blog.json`.
- Does not handle author attribution — `author-reference` is left null (matches current site convention).
- Pre-flight checks run before any upload: token scopes and slug availability — a taken slug stops the run before images are wasted (and is never resolved by appending a suffix).

## Image naming convention

```
{slug}_page-header_1578x888.webp   →  image-page-header  (top of post)
{slug}_thumbnail_724x408.webp      →  grid-thumbnail     (blog overview grid)
{slug}_mega-menu_502x283.webp      →  thumbnail-mega-menu (nav mega menu)
```

## Files

```
blog-publisher/
├── SKILL.md               Skill orchestrator — 7-phase pipeline, error handling
├── webflow-config.md      Site ID, collection ID, all 22 field slugs, all 16 category IDs
├── html-conversion.md     Google Doc → Webflow Rich Text HTML conversion rules
└── image-pipeline.md      Pillow resize helper, WebP naming, Drive sourcing, S3 upload notes

scripts/
├── gdoc_to_fielddata.py   Doc text → fielddata.json (HTML, slug rules, categories, placeholders)
├── apply_internal_links.py Deterministic internal-link placement from strategist output
├── resize_blog_images.py  Master + inline images → exact WebP sizes (Pillow)
└── blog-publisher.py      Publish engine: pre-flight, asset upload, create/--staged/--update, --dry-run
```
