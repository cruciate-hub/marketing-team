# Webflow Publisher

Shared Claude skill that publishes finished content to any social.plus Webflow CMS
collection. Content-type skills write and check the draft; this skill turns it into
Webflow rich-text HTML, resizes images to the collection's exact sizes, validates the
whole payload without touching the API (`--dry-run`), and creates the item through the
Webflow Data API v2 — live, `--staged`, or `--update` to refresh images on an existing item.

Design note with the reasoning: [`webflow-publisher-design.md`](./webflow-publisher-design.md).

## What it does

- Accepts the **common markdown intermediate** — `# Title`, a `Label: value` metadata block,
  a markdown body — which is exactly the `.draft.md` that `blog-seo-content`,
  `glossary-content` and `aeo-content` already produce for their compliance scripts.
- Reads a **per-collection field map** (`webflow-fields.json`, owned by the content-type skill
  that produces the draft — not by this skill): Webflow IDs, which label maps to which CMS
  field slug, category taxonomy, exact image sizes, slug rules, checks. Nothing is hard-coded
  in Python, and this skill carries no per-collection knowledge of its own — see
  [`field-map-schema.md`](../marketing-team/skills/webflow-publisher/field-map-schema.md).
- Converts the body: `##`/`###` headings, bold/italic, bullets (nested), numbered lists,
  blockquotes, external links in a new tab and internal links in the same tab, GFM tables
  wrapped in a Webflow Embed block (`<div data-rt-embed-type='true'>`) so the Designer's
  editor cannot mangle them, image lines → full-width `<figure>` placeholders.
- Resizes a master image to every size the collection declares (Pillow; WebP; exact pixels).
- `--dry-run`: required fields, slug rules, Tags ⊇ Category, forbidden strings, no
  `<h1>`/`<style>`/`<script>`, internal links, placeholder ↔ inline-image count, **structural
  table checks** (flattened-table signature, source-vs-output table count, every table in an
  Embed), exact image dimensions, and a hard fail on any field slug still unconfirmed.
- Publishes with pre-flight (token scopes + slug availability) before any upload; never
  resolves a slug collision by appending a suffix.

## Collections

| Collection | Field map | Status |
|---|---|---|
| Blog Posts | `blog-seo-content/webflow-fields.json` | Ready. Used by `blog-publisher`. |
| Glossary | `glossary-content/webflow-fields.json` | Ready. `body`/`Meta description` confirmed 2026-09-18 via `sync_fieldmap.py`; the collection has no `intro`/`date`/`Alt text`/`Category` field (confirmed absent). |
| Answers (AEO) | `aeo-content/webflow-fields.json` | Stub only, not wired into `aeo-content`. |

`python3 "$REPO/scripts/webflow-publisher.py" --list-collections` prints this at runtime.

## Pipeline

| Step | Command (`$REPO/scripts/…`) |
|---|---|
| Convert | `md_to_webflow_html.py <draft.md> --collection <name> --out fielddata.json` |
| Internal links (optional) | `apply_internal_links.py fielddata.json links.json --collection <name>` |
| Images (if the collection has image fields) | `resize_images.py <master> <slug> <outdir> --collection <name> [--inline …]` |
| Validate | `webflow-publisher.py fielddata.json --collection <name> --image role=path … --inline … --source draft.md --dry-run` |
| Publish | same without `--dry-run` (`--staged` to review first) |
| Refresh images | `webflow-publisher.py --update <item_id> --collection <name> --image role=path …` |

## Prerequisites

| Requirement | How to set it up |
|---|---|
| `WEBFLOW_API_TOKEN` | Webflow → Site Settings → Integrations → API Access. Scopes: **cms:write**, **assets:write**, **sites:read**. Not needed for `--dry-run`. |
| Python 3 | The converter and engine are standard-library only. |
| Pillow | Only for resizing and for image-dimension checks (skipped, with a note, if absent). |

## Files

```
webflow-publisher/
├── SKILL.md               Skill orchestrator — rules, pipeline, error handling
├── html-conversion.md     Intermediate → Webflow rich-text HTML rules (tables in Embed, figures, link policy)
├── image-pipeline.md      Resize helper, WebP naming, Drive sourcing, S3 upload notes
├── field-map-schema.md    Schema every content-type skill's webflow-fields.json follows (this skill owns no field maps itself)
└── tests/                 run_tests.py + fixtures (legacy golden for the blog adapter, glossary draft, table-bug regressions)

scripts/  (repo root)
├── webflow_fieldmap.py     Field-map loader/validator — discovers webflow-fields.json across skills/*/
├── sync_fieldmap.py        Fetches the live Webflow schema and proposes slugs for a field map's null entries
├── md_to_webflow_html.py   Intermediate → fielddata.json (importable + CLI)
├── webflow-publisher.py    Engine: --dry-run, live, --staged, --update, --list-collections
├── resize_images.py        Master + inline → exact WebP sizes from the field map
├── apply_internal_links.py Deterministic internal-link placement
├── gdoc_to_fielddata.py    Blog adapter (Google Doc export → intermediate → blog fielddata)
├── blog-publisher.py       Blog wrapper: old positional CLI → engine with --collection blog
└── resize_blog_images.py   Blog wrapper: old CLI → resize_images.py --collection blog
```
