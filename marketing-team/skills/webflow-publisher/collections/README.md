# Collection field maps

One JSON file per Webflow CMS collection the publisher can target. Every shared script
takes `--collection <name>` (a file in this folder) or `--field-map <path>` (any file with
this schema). `python3 "$REPO/scripts/webflow_fieldmap.py" --list` shows which maps are
ready and which still have unconfirmed slugs.

| File | Collection | Status |
|---|---|---|
| `blog.json` | Blog Posts `66e2765d540e1939a89db6a4` | Ready. Single source of truth for blog field slugs and category IDs (moved out of the Python scripts). |
| `glossary.json` | Glossary `66e2765d540e1939a89db93e` | **Stub.** Collection ID and URL prefix are real; every field slug except `name`/`slug` is `null` pending confirmation. |
| `answers.json` | Answers `68f643838f7abffca74efbc1` | **Stub, not wired.** Same situation; shipped because aeo-content's draft is already in the intermediate shape. |

## Schema (v1)

```jsonc
{
  "schema_version": 1,
  "collection": "blog",                       // registry name; matches the file name
  "display_name": "Blog Posts",
  "site_id": "…",                             // Webflow site ID
  "collection_id": "…",                       // Webflow collection ID
  "live_url_prefix": "https://www.social.plus/blog/",

  "fields": {                                 // structural fields (slug or null)
    "title": "name",                          //   H1 → CMS item name (always "name")
    "slug":  "slug",                          //   always "slug"
    "body":  "post-content",                  //   RichText body; null = unconfirmed (blocks publish)
    "intro": "post-summary",                  //   first paragraph lifted out of the body; null = stays in body
    "date":  "date-published"                 //   ISO 8601 UTC set at conversion time; null = no date field
  },

  "metadata": {                               // draft `Label: value` line → CMS field
    "Meta description": {"slug": "meta-description", "required": true, "max_length": 160},
    "Minutes to read":  {"slug": "min-read", "required": true, "default": "5"},
    "Alt text":         {"slug": "image-alt-text"},                       // optional text field
    "Category":         {"slug": "category", "required": true,
                         "type": "reference", "taxonomy": "categories"},  // first name → one item ID
    "Tags":             {"slug": "category-multi-reference-3", "required": true,
                         "type": "multi_reference", "taxonomy": "categories",
                         "must_include": "Category"}                      // all names → IDs; Category's ID prepended
  },

  "taxonomies": {"categories": {"Community": "66e2…", "…": "…"}},         // display name → item ID (case-insensitive lookup)
  "defaults": {"featured": false},                                        // merged when absent from the draft

  "images": [                                                             // one entry per CMS image field
    {"role": "header", "slug": "image-page-header", "variant": "page-header", "width": 1578, "height": 888}
  ],
  "inline_images": {"variant": "img", "width": 1578, "height": 888},      // body <figure> images; null = none

  "slug_rules": {"strip_years": true, "strip_leading_count": true},
  "checks": {
    "require_internal_links": true,                                       // dry-run: ≥1 internal <a href>
    "forbidden_body_strings": ["OUTREACH VERSION"]                        // dry-run: must not appear in the body
  }
}
```

Rules:

- Keys starting with `_` (e.g. `_doc`, `_confirm`, `_status`) are documentation; the loader
  strips them. Use them for provenance and CONFIRM notes.
- **`null` means unconfirmed, never "absent".** Delete an entry the collection genuinely
  does not have; keep `null` for one that exists but whose slug you have not read from
  Webflow yet. The converter parks values for `null` slugs under `__unconfirmed__` in
  `fielddata.json`; `webflow-publisher.py` fails `--dry-run` and refuses to publish while any
  required slug is `null` or `__unconfirmed__` is present.
- Confirm a slug by reading it, never by guessing: Webflow Designer → collection settings,
  or `GET https://api.webflow.com/v2/collections/{collection_id}` with a token that has
  `cms:read`.
- Image sizes are exact (the CMS fields use min=max validation). Files are named
  `{slug}_{variant}_{width}x{height}.webp` by `scripts/resize_images.py`.

## Adding a collection

1. Copy `glossary.json`, rename, set `collection`, `collection_id`, `live_url_prefix`.
2. Fill the confirmed slugs; leave `null` + `_confirm` for the rest.
3. `python3 "$REPO/scripts/webflow_fieldmap.py" <name>` validates the schema.
4. Add a fixture in `../tests/fixtures/` and an expectation in `../tests/run_tests.py`.
