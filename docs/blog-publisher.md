# Blog Publisher

Claude skill for publishing a completed blog article from Google Docs to the social.plus Webflow blog — live immediately, or `--staged` for review first. Also refreshes hero images on existing posts with `--update`.

It is the **blog adapter** on top of the shared [`webflow-publisher`](./webflow-publisher.md) skill: this skill owns reading the Google Doc, the listicle-specific parsing, blog slug rules and webinar matching; conversion, the image pipeline, dry-run validation and the Webflow Data API calls are the shared skill's, driven by the `blog` field map (`blog-seo-content/webflow-fields.json`).

## What it does

- Reads the source article from Google Docs using the Google Drive MCP (no copy-paste required).
- Detects multiple articles in one doc (e.g. a listicle batch) and lets the user pick which to publish.
- Normalizes the doc's export into the common markdown intermediate (`gdoc_to_fielddata.py`): `# Listicle N` slicing, `**Page title:**`-style metadata, `### **Platform: tagline**` entries → H3 + inline-image slot, `###` sections → H2, OUTREACH/INTERNAL/disclosure blocks dropped — then converts it with the shared converter (headings, lists, comparison table inside a Webflow Embed, bold, links).
- Invokes `internal-linking-strategist` in draft mode and places its suggestions deterministically (`apply_internal_links.py`); internal links open in the same tab.
- Runs the standard compliance check (terminology, tone, no fabricated claims, no em dashes).
- Validates the master image (≥ 1578 px wide, ~16:9), then resizes and converts to WebP via `resize_blog_images.py` (Pillow — macOS `sips` cannot write WebP) — producing `{slug}_page-header_1578x888.webp`, `{slug}_thumbnail_724x408.webp`, `{slug}_mega-menu_502x283.webp` (sizes from the field map).
- Picks the related webinar (`related-webinar-to-show-on-page`) from the allowed pool.
- `--dry-run` validates the whole payload without touching the API, including the structural table checks and exact image dimensions.
- Uploads all images to the Webflow asset library via the three-step upload process (MD5 hash → asset metadata API → S3 multipart POST).
- Publishes the blog post via `POST /v2/collections/{id}/items/live` (or stages it with `--staged`). Prints the live URL and CMS item ID on success.

## When it triggers

"Publish blog", "post to Webflow", "upload article to CMS", "put this live", "the article is ready", "publish listicle [N]".

Must have a Google Doc URL/ID and a PNG file path. If either is missing, the skill asks before proceeding.

If the user asks to write AND publish, run `blog-seo-content` first, then this skill. For a glossary entry or any other collection, use `webflow-publisher` directly.

## Prerequisites

| Requirement | How to set it up |
|---|---|
| `WEBFLOW_API_TOKEN` env var | Webflow → Site Settings → Integrations → API Access. Token must have **cms:write** AND **assets:write** scopes (plus **sites:read** for the pre-flight). |
| Python 3 | The publish scripts are standard-library only — no `pip install`, no virtualenv. |
| Pillow (for resizing) | The resize helper checks for it and prints the install command if missing. |
| Google Drive MCP connected | Needed to read the Google Doc. The doc must be shared with the account the MCP is authenticated as. |

## Inputs

1. **Google Doc ID** — from the URL: `docs.google.com/document/d/{DOC_ID}/edit`
2. **PNG file path** — absolute path to the master image. Must be ≥ 1578 px wide.
3. **Inline PNGs** (optional) — body images in platform order.

## Pipeline

| Phase | What happens |
|---|---|
| 1. Read doc | Google Drive MCP reads the article. If multiple articles are in the doc, user picks one. |
| 2. Convert | `gdoc_to_fielddata.py` normalizes the export into the intermediate and the shared converter builds `fielddata.json` (categories → IDs, year/count-free slug, table in an Embed, image placeholders). |
| 3. Internal linking | `internal-linking-strategist` suggestions → `links.json` → `apply_internal_links.py`. |
| 4. Compliance check | Terminology, tone, claims, em dashes, emojis — all fixed before proceeding. |
| 5. Resize images | `resize_blog_images.py` emits all exact WebP sizes (Pillow). |
| 6. Webinar matching | Best related webinar from the allowed pool → `related-webinar-to-show-on-page`. |
| 7. Dry-run + publish | `blog-publisher.py … --dry-run`, then the same command live or `--staged`. Pre-flight checks token scopes and slug availability before any upload. |

## What it does NOT do

- Does not write blog content — use `blog-seo-content` for that, then hand the result here.
- Does not trigger a full Webflow site publish. After the CMS item is live, trigger a manual Webflow publish to refresh the CDN and regenerate `website/pages-blog.json`.
- Does not handle author attribution — `author-reference` is left null (matches current site convention).
- Never resolves a slug collision by appending a suffix — it stops and asks.

## Image naming convention

```
{slug}_page-header_1578x888.webp   →  image-page-header  (top of post)
{slug}_thumbnail_724x408.webp      →  grid-thumbnail     (blog overview grid)
{slug}_mega-menu_502x283.webp      →  thumbnail-mega-menu (nav mega menu)
{slug}_img-N_1578x888.webp         →  inline <figure> N in post-content
```

## Files

```
blog-publisher/
├── SKILL.md               Skill orchestrator — 7-phase pipeline, blog slug rules, webinar matching, error handling
├── webflow-config.md      Human-readable field notes; the IDs live in blog-seo-content/webflow-fields.json
└── IMPROVEMENTS.md        Backlog and resolved field feedback

webflow-publisher/         Shared engine docs: html-conversion.md, image-pipeline.md, field-map-schema.md
blog-seo-content/          webflow-fields.json — the blog field map lives here, not in webflow-publisher

scripts/  (repo root)
├── gdoc_to_fielddata.py   Blog adapter: Google Doc export → intermediate → fielddata.json
├── blog-publisher.py      Wrapper: positional blog CLI → webflow-publisher.py --collection blog
├── resize_blog_images.py  Wrapper: → resize_images.py --collection blog
├── apply_internal_links.py Deterministic internal-link placement from strategist output
└── (shared) md_to_webflow_html.py, webflow-publisher.py, resize_images.py, webflow_fieldmap.py
```
