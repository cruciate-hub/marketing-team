# webflow-publisher — design note

Internal engineering note for the refactor that turns `blog-publisher`'s publish
mechanics into a shared, collection-agnostic skill. Written before the code; the
"Deviations" section at the end records where the implementation ended up differing.

## Problem

Two skills write content for the social.plus Webflow site, and only one can publish:

- `blog-publisher` publishes, but is welded to one content shape: a Google Doc listicle
  (`# Listicle N` slicing, `### **Platform: tagline**` entries, an "At-a-Glance" table).
  Its dry-run table checks only fired when the body contained the literal strings
  `At-a-Glance` or `Comparison`; a flattened table under any other heading shipped silently.
- `glossary-content` has no publish path at all (delivers `.docx`, field slugs unconfirmed).
- `aeo-content` claims "a downstream automation converts the .docx to Webflow HTML".
  Nothing in this repo implements or references such an automation (see "aeo-content
  finding" below).

## Name and ownership

**Skill name: `webflow-publisher`** (`marketing-team/skills/webflow-publisher/`).
It names the destination and the action, parallels `blog-publisher` so the relationship is
obvious, and does not over-specify the input (the input is a markdown intermediate, not a
"doc"). Rejected: `doc-to-webflow` (input-centric, and "doc" is ambiguous between Google
Doc, `.docx`, and markdown), `cms-publisher` (vague).

| Owned by `webflow-publisher` (shared, mechanical) | Stays per content-type skill |
|---|---|
| Markdown intermediate → Webflow rich-text HTML (headings, lists, tables → Embed block, inline formatting, links, image placeholders) | Writing rules, tone, structure, word counts |
| Per-collection field mapping (`collections/<name>.json`) and taxonomy lookup | Compliance scripts (`glossary-content/scripts/compliance.py`, `blog-seo-content/scripts/compliance.py`, … stay exactly as they are) |
| Slug derivation + the year/leading-count rules (configurable per collection) | Source-specific parsing (e.g. the Google Doc export → intermediate, in `gdoc_to_fielddata.py`) |
| Image resize to exact WebP sizes (sizes come from the field map) | Choosing images, alt text, image concepts |
| Webflow Data API v2: pre-flight, asset upload, create live / staged, `--update` image refresh | Anything editorial: internal-link *selection* (`internal-linking-strategist`), webinar matching, named-editor gate |
| Side-effect-free `--dry-run` validation, incl. the structural table checks | Deciding *whether* to publish |

Scripts follow the repo convention and live at repo-root `scripts/` (skills invoke them as
`$REPO/scripts/...`); the skill folder holds docs, field maps and tests.

## The common intermediate

Every content-type skill already produces the same shape as its compliance-checked draft
(`outputs/[slug].draft.md` in blog-seo-content, aeo-content and glossary-content), so that
shape *is* the contract. No new format:

```
# Title                      ← the only H1; becomes the CMS item name

Meta description: …          ← contiguous block of `Label: value` lines directly under the H1
Slug: …                        (unknown labels are kept and reported as unmapped; a wrapped
Alt text: …                     value continues on the next line, as compliance.py parses it)
Category: …
Tags: …

[first paragraph]            ← if the field map declares an `intro` field this paragraph is
                               lifted out of the body into it (blog: post-summary); otherwise
                               it stays in the body (glossary: the definition paragraph)

## Section                   ← ## → <h2>, ### → <h3>, #### → <h4>. No H1 in the body.
Paragraph text with **bold**, *italic*, [links](https://…).
- bullets (indented `  - ` nest under the previous top-level item)
1. numbered lists → <ol>
| GFM | table |             ← → <div data-rt-embed-type='true'><table><thead>…<tbody>…</table></div>
|---|---|                      bold markers inside cells are stripped (Webflow renders them literally)
![alt](anything)             ← an image line → __INLINE_IMG_N__ placeholder (N in document order);
__INLINE_IMG_N__               a bare placeholder line is accepted as-is. The engine swaps each
                               for Webflow's full-width <figure> once the upload URL is known.
```

Rules carried over from the old converter, now generic: `\*\*` and `\~` Google-export
artifacts are unescaped; multi-line paragraphs are joined with a space; `<style>`, `<h1>`,
`<script>`, `<iframe>` never appear in output. Links get `target="_blank"` **only when
external** (relative or `social.plus` hrefs open in the same tab, which is what both
`html-conversion.md` and blog-seo-content's rules already said; the old code ignored that).

A content-type skill hands over: the draft in this shape, the collection name (or a field-map
path), and, where the collection has image fields, the master image(s).

## Field-mapping config

One JSON file per Webflow collection in
`marketing-team/skills/webflow-publisher/collections/<name>.json`, selected on every CLI
with `--collection <name>`; `--field-map <path>` accepts an arbitrary file so a future skill
can ship its own map without touching the shared skill. The registry lives in the shared
skill because the shared skill defines and validates the schema and because a collection is
a property of the site, not of a writing skill; `--field-map` keeps the per-skill option open.

```jsonc
{
  "schema_version": 1,
  "collection": "blog",                       // registry name
  "site_id": "…", "collection_id": "…",       // Webflow IDs (glossary/answers IDs come from the
  "live_url_prefix": "https://www.social.plus/blog/",   //   site inventories' _meta.collectionId)
  "fields": { "title": "name", "slug": "slug", "body": "post-content",
              "intro": "post-summary",        // null → first paragraph stays in the body
              "date": "date-published" },     // null → no date field is set
  "metadata": {                               // draft label → CMS field
    "Meta description": {"slug": "meta-description", "required": true, "max_length": 160},
    "Minutes to read":  {"slug": "min-read", "required": true, "default": "5"},
    "Alt text":         {"slug": "image-alt-text"},
    "Category":         {"slug": "category", "required": true, "type": "reference", "taxonomy": "categories"},
    "Tags":             {"slug": "category-multi-reference-3", "required": true,
                         "type": "multi_reference", "taxonomy": "categories", "must_include": "Category"}
  },
  "taxonomies": { "categories": { "Community": "66e2…", … } },   // display name → item ID
  "defaults":   { "featured": false, … },     // switches etc., merged if absent
  "images": [ {"role": "header", "slug": "image-page-header", "variant": "page-header",
               "width": 1578, "height": 888}, … ],              // exact sizes (min=max in CMS)
  "inline_images": {"variant": "img", "width": 1578, "height": 888},
  "slug_rules": {"strip_years": true, "strip_leading_count": true},
  "checks": {"require_internal_links": true, "forbidden_body_strings": ["OUTREACH VERSION", …]}
}
```

**Unconfirmed slugs** are `null`, with a sibling `_confirm` note saying how to confirm them.
Keys starting with `_` are documentation and ignored by the loader. The converter parks
values whose slug is `null` under a top-level `__unconfirmed__` key in `fielddata.json`
(so nothing is lost), and the engine refuses to publish and fails `--dry-run` while any
required slug is unconfirmed or `__unconfirmed__` is present. That is how `glossary.json`
ships today: `name`/`slug` (Webflow built-ins on every collection) and the collection ID are
real; everything else is `null` and marked `CONFIRM WITH STEFAN`.

`fielddata.json` stays a **flat `fieldData` dict** (plus the optional `__unconfirmed__`),
exactly what the API receives, so `apply_internal_links.py` and the hand-added
`related-webinar-to-show-on-page` field keep working unchanged.

## Pipeline and CLIs

| Script (repo-root `scripts/`) | Role |
|---|---|
| `webflow_fieldmap.py` | Loader/validator for `collections/*.json` (importable) |
| `md_to_webflow_html.py` | Intermediate → `fielddata.json` for a collection (importable + CLI) |
| `webflow-publisher.py` | Engine: `--dry-run`, live, `--staged`, `--update <item_id>`, `--list-collections`; images as `--image <role>=<path>` and `--inline …` |
| `resize_images.py` | Master (+ inline) → exact WebP sizes read from the field map |
| `apply_internal_links.py` | Unchanged algorithm; body field now comes from `--collection` (default `post-content`) |
| `gdoc_to_fielddata.py` | **Blog adapter**: Google Doc export → intermediate → `md_to_webflow_html` (same CLI as before) |
| `blog-publisher.py`, `resize_blog_images.py` | **Thin wrappers** that translate the old positional CLIs onto the engine with `--collection blog`, so every documented command keeps working |

Flow for any collection: draft → (skill's own compliance) → `md_to_webflow_html.py
--collection X` → `apply_internal_links.py` if the skill uses the strategist's `links.json`
→ `resize_images.py --collection X` (if the collection has image fields) →
`webflow-publisher.py --dry-run` → `webflow-publisher.py` (`--staged` or live).

## Dry-run validation

Field-map driven: required fields (incl. `max_length`), slug rules as configured,
`must_include` taxonomy consistency, `forbidden_body_strings`, no `<h1>`/`<style>`/
`<script>`/`<iframe>`, internal links present when required, placeholder ↔ inline-image
count, exact image dimensions per role, `.webp` extension, and a hard FAIL on any
unconfirmed slug or `__unconfirmed__` payload. Pre-flight (token via `GET /sites/{id}`,
slug availability) runs before any upload in a real run, as before.

**The table check, generalized.** Three structural layers, none keyed on heading text:

1. `content:table-not-flattened` — FAIL if any `<p>` carries a flattened-table signature
   (text beginning with `|` or containing `|---`), or, when `--source <draft.md>` is passed,
   if the number of GFM table blocks in the source exceeds the number of `<table>` elements
   in the output. The blog adapter and the glossary flow both pass `--source`.
2. `content:table-in-embed` — FAIL unless every `<table>` is wrapped as
   `<div data-rt-embed-type='true'><table>` (count equality), whenever at least one table exists.
3. `content:table-structure` — every table has `<thead>` and `<tbody>`.

So a glossary "Active User Metrics" or "How to Calculate Churn" table gets the same protection
the blog's "At-a-Glance" table had.

## What moved out of the shared path (blog-specific)

Kept in `gdoc_to_fielddata.py`, which now *emits the intermediate* and calls the shared
converter (inspect it with `--emit-intermediate <path>`):

- `# Listicle N` slicing, `**Page title:**` / `**Meta description**` / `Main Category Tag:`
  / `Minutes to read:` / `Introduction text` / `Image alt text:` extraction (incl. the
  cut-at-next-label fix), OUTREACH/INTERNAL/Display trailers.
- Heading normalization: the export uses `###` for top sections → promoted to `##`;
  `####` → `###`; `### **Name: tagline**` platform entries → `### Name: tagline` followed by
  a bare `__INLINE_IMG_N__` line (so they still land as `<h3>` + placeholder).
- `Main Category Tag: A, B, C` → `Category: A` + `Tags: A, B, C`.
- Dropping the `[OPTIONAL DISCLOSURE …]` paragraph.

Kept in `blog-publisher/SKILL.md` as agent steps: reading the doc via the Drive MCP,
webinar matching (Phase 6), the compliance pass, the NON-NEGOTIABLE slug rules.

Category IDs are no longer hard-coded in Python; `collections/blog.json` is the single
source (`blog-publisher/webflow-config.md` points at it).

## Deliberate behavior deltas vs. the old scripts

Everything not listed here is byte-identical for the Google Doc listicle path; a golden
fixture generated with the *original* `gdoc_to_fielddata.py` is asserted in
`webflow-publisher/tests/`.

1. Internal links no longer get `target="_blank"` (converter and `apply_internal_links.py`).
   Documented policy in `html-conversion.md` and blog-seo-content; the code never followed it.
2. Numbered lists convert to `<ol>` (documented in `html-conversion.md`, never implemented).
3. `  - ` bullets nest under a preceding top-level bullet (documented, never implemented).
   Listicle "Key strengths:" bullets have no parent item, so their output is unchanged.
4. A table indented with leading whitespace is still recognized as a table (was flattened).
5. Image dimension check: "Pillow missing" still skips, but "Pillow present, file unreadable"
   is now a FAIL instead of a silent skip.
6. `>` blockquotes → `<blockquote>`, a lone `---` rule is dropped rather than emitted as `<p>---</p>`.
7. The two table checks run for every table, not only under "At-a-Glance"/"Comparison".

## Glossary wiring — what exists and what is blocked

Exists: `collections/glossary.json` (collection `66e2765d540e1939a89db93e` from
`website/pages-glossary.json` `_meta`, URL prefix `/glossary/`), the converter handles the
six-section draft as-is (the definition paragraph stays in the body because no separate
field is known; the Metrics table lands in an Embed; Related Terms links satisfy the
internal-link check), and glossary-content's SKILL.md now has a "Publishing" section that
runs compliance → convert → dry-run → publish.

**Blocked, only Stefan can unblock:** every glossary field slug except `name`/`slug`. Read
them from the Designer's collection settings or `GET https://api.webflow.com/v2/collections/
66e2765d540e1939a89db93e` and fill the `null` slugs in `glossary.json` (`body` first — the
dry-run fails on that alone). Also unknown: whether Glossary has a category taxonomy at all
(`taxonomies.categories` is empty), any image fields (`images` is `[]`), and a date field.
Nothing here is guessed.

## aeo-content finding

The "downstream automation converts the .docx to Webflow HTML and publishes to /answers/"
statement (SKILL.md, `references/workflow-phases.md`, `docs/aeo-content.md`) has no
implementation, script, worker, or Make-scenario reference anywhere in this repo. From the
repo alone it is aspirational or lives entirely outside it; treat it as unverified. The
glossary SKILL.md additionally claimed blog-seo-content relies on the same automation, which
is wrong (blog's real path is blog-publisher's Google Doc → `gdoc_to_fielddata.py`); that
sentence is corrected in this change.

Wiring aeo-content would be cheap: its `.draft.md` is already the intermediate (labels
`Meta description`, `Slug`, `Alt text`, `Intent`), so `collections/answers.json` is shipped
as a stub (collection `68f643838f7abffca74efbc1` from `pages-answers.json`, all field slugs
`null`, `Intent` is writer-side metadata and unmapped). Not wired further: aeo-content's
SKILL.md is not edited in this change beyond what the design requires — the automation
claim may refer to something outside the repo, so the decision is left to Stefan.

## Distribution, CI, checks

- `webflow-publisher/SKILL.md` carries the canonical FETCH-BLOCK byte-for-byte
  (`scripts/audit-skills.sh` reports 0 drift).
- `.github/workflows/ci.yml` gains a step running `webflow-publisher/tests/run_tests.py`
  (stdlib only; image-dimension assertions are skipped when Pillow is absent, as in the engine).
- `marketing-team/.claude-plugin/plugin.json` bumped; README/brain/docs updated.
- `skill-distribution/build-kits.sh` is git-ignored and not visible from a worktree clone —
  adding `webflow-publisher` to its skill arrays is a manual follow-up for Stefan.

## Deviations from the plan above

None at the time of implementation; the code matches this note. (Update this section if
the field-map schema or the intermediate rules change.)
