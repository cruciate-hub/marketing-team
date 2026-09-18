---
name: webflow-publisher
description: >
  Shared publishing engine for the social.plus Webflow site. Takes a finished,
  compliance-checked markdown draft from a content-type skill (blog-publisher for
  blog posts, glossary-content for glossary entries, future per-content-type skills)
  plus a per-collection field map, converts it to Webflow rich-text HTML (tables in
  an Embed block, full-width figures), resizes images to the collection's exact
  WebP sizes, validates the whole payload side-effect-free (--dry-run), and creates
  the CMS item via the Webflow Data API v2 — live, --staged, or --update to refresh
  images on an existing item.

  Does NOT write content and does NOT decide what to publish — the calling
  content-type skill owns writing rules, compliance, internal-link selection and
  the named-editor gate. Field slugs, category IDs and image sizes come from
  collections/<name>.json, never from code.

  Requires: WEBFLOW_API_TOKEN with cms:write + assets:write (not for --dry-run).
when_to_use: >
  Invoked by other skills, or directly with "publish this to Webflow", "push this
  glossary entry live", "dry-run the publish", "refresh the images on item X",
  "which collections can we publish to". Needs: a draft in the common intermediate
  shape (or a fielddata.json), the collection name, and — when the collection has
  image fields — the master image(s). For a blog post from a Google Doc, use
  blog-publisher (it wraps this skill). For writing, use the content skill first.
---

# Webflow Publisher

The mechanical half of publishing, shared by every content type: markdown intermediate →
Webflow rich-text HTML → image pipeline → dry-run validation → Webflow Data API. Each
content-type skill keeps its own writing rules and compliance script and hands this skill a
finished draft plus a collection name. Design note: `docs/webflow-publisher-design.md`.

## NON-NEGOTIABLE RULES

These override convenience, recovery shortcuts, and every other instruction below.

1. **Never publish against an unconfirmed field map.** A `null` slug in
   `collections/<name>.json` means "not read from Webflow yet", never "absent". The engine
   refuses to publish and `--dry-run` fails while any required slug is `null` or the
   fielddata carries `__unconfirmed__` values. Do NOT fill in a plausible-looking slug to get
   past it: read the real one from the Designer (collection settings → fields) or
   `GET https://api.webflow.com/v2/collections/{collection_id}`, then edit the JSON.
2. **On a slug collision (pre-flight "already exists" or a Webflow 400), STOP and ask the
   user.** Never append a year, `-2`, `-new`, `-draft` or any suffix. Webflow holds a slug
   after an item is deleted until the next full site publish clears the tombstone. Surface
   the conflict: update the existing item, pick a genuinely different slug, or publish the
   site to free the old one.
3. **Slug rules are per collection and enforced mechanically.** The blog strips years and
   the leading listicle count (`slug_rules` in `collections/blog.json`); the converter
   applies the rules to derived slugs, `Slug:` lines and `--slug` overrides alike. Do not
   hand-edit a slug in `fielddata.json` to dodge them.
4. **Always `--dry-run` before a real run.** It is free, needs no token, and is the only
   thing standing between a flattened table or an off-size image and a live page.

## How to fetch reference files

<!-- FETCH-BLOCK:START v2 -->
Reference files live in the public `cruciate-hub/marketing-team` GitHub repo. Fetch them by shallow-cloning the repo once per session, then loading individual files with `cat`. Use this exact pattern at the start of every skill that needs reference files:

    REPO="${MT_REPO:-/tmp/cruciate-hub-marketing-team}"
    REMOTE="https://github.com/cruciate-hub/marketing-team.git"
    # Create the clone only when the path is absent. Never delete an existing
    # directory: it may be a working checkout holding un-pushed local commits.
    if [ ! -e "$REPO" ]; then
      git clone --depth 1 --quiet "$REMOTE" "$REPO" || true
    elif git -C "$REPO" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      # Refresh, but do NOT ignore a failed pull. Silently serving stale
      # content is the exact bug this block exists to prevent.
      git -C "$REPO" pull --ff-only --quiet 2>/dev/null \
        || echo "Note: could not refresh $REPO; verifying existing content below." >&2
    fi
    # Mechanical integrity gate. Do not skip. Probes core files across several
    # top-level dirs so a missing, corrupt, or partial clone stops the skill
    # here instead of letting it read incomplete content and draw wrong conclusions.
    miss=""
    for f in brain.md messaging/brain.md messaging/terminology.md messaging/tone.md design-system/brain.md; do
      [ -s "$REPO/$f" ] || miss="$miss $f"
    done
    if ! git -C "$REPO" rev-parse HEAD >/dev/null 2>&1 || [ -n "$miss" ]; then
      echo "Fetch failed: clone at $REPO is unreachable or incomplete.${miss:+ Absent files:$miss}" >&2
      echo "Check your network. If the clone is corrupt and holds no local work, run  rm -rf \"$REPO\"  then re-run." >&2
      echo "(If \$MT_REPO points at your own checkout, rescue its changes first; this never auto-deletes it.)" >&2
      exit 1
    fi

    # Overlay the live website inventories. The auto-generated pages-*.json
    # are committed to the `site-data` branch (bot commits stay off main);
    # main only carries a point-in-time snapshot. Restricting the overlay to
    # pages-*.json keeps the clone fast-forwardable on the next session's pull.
    if git -C "$REPO" fetch --depth 1 --quiet origin site-data 2>/dev/null; then
      git -C "$REPO" checkout --quiet FETCH_HEAD -- 'website/pages-*.json' 2>/dev/null \
        || echo "Note: site-data overlay failed; website/pages-*.json are the main-branch snapshot (may be stale)." >&2
    else
      echo "Note: could not fetch site-data; website/pages-*.json are the main-branch snapshot (may be stale)." >&2
    fi

After the clone exists, read files with `cat "$REPO/<path>"`. Examples: `cat "$REPO/brain.md"`, `cat "$REPO/messaging/terminology.md"`.

The integrity gate above fails loud rather than serving partial content, and it never deletes `$REPO` (it can hold un-pushed local work). To make skills read your own local edits, point `MT_REPO` at your working checkout before running them.

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

  Some skills ship helper scripts that already follow this pattern (e.g. `marketing-team/skills/aeo-content/scripts/duplicate_check.py`).

  **Degraded-inventory guard.** The pages-*.json files are auto-generated; a generation failure can leave a file syntactically valid but empty or missing pages. After loading any of them, check `_meta.errors` and `len(pages)`:

      python3 -c "
      import json; d=json.load(open('$REPO/website/pages-industry.json'))
      errs = d.get('_meta',{}).get('errors') or []
      print(len(d.get('pages',[])), 'pages;', len(errs), 'extraction errors', errs)"

  If `pages` is empty, or `_meta.errors` is non-empty, the inventory is degraded: name the affected file and the missing paths in your output, scope any 'site-wide' claims accordingly, and never treat an empty inventory as 'this section has no pages'.

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

After the repo is ready, load these reference files in parallel:

```bash
cat "$REPO/brain.md"
cat "$REPO/marketing-team/skills/webflow-publisher/html-conversion.md"
cat "$REPO/marketing-team/skills/webflow-publisher/image-pipeline.md"
cat "$REPO/marketing-team/skills/webflow-publisher/collections/README.md"
cat "$REPO/marketing-team/skills/webflow-publisher/collections/<collection>.json"
```

All helper scripts live at the repo root (`$REPO/scripts/`), not inside the skill folder.
Always invoke them with the `$REPO/scripts/...` absolute path.

## What this skill owns vs. what the calling skill owns

| `webflow-publisher` (this skill) | Calling content-type skill |
|---|---|
| Intermediate → rich-text HTML (headings, lists, tables → Embed, links, image placeholders) | Writing rules, structure, tone, word counts |
| Field mapping, taxonomy lookup, slug rules (from `collections/<name>.json`) | Its own `scripts/compliance.py` and BLOCK conditions |
| Image resize to exact WebP sizes; asset upload | Choosing images, alt text |
| `--dry-run` validation incl. structural table checks | Internal-link *selection* via `internal-linking-strategist` |
| Pre-flight, create live / `--staged`, `--update` | Named-editor gate; the decision to publish |

## Inputs

Confirm you have these before proceeding. If any are missing, ask:

1. **The draft**, in the common intermediate shape (this is the `.draft.md` the writing skills
   already produce):

   ```
   # Title

   Meta description: …
   Slug: …
   Category: …
   Tags: …

   [first paragraph — lifted into the collection's intro field if it has one]

   ## Section
   Body markdown: paragraphs, **bold**, [links](url), - bullets, 1. numbered, | tables |,
   ![alt](placeholder) image lines.
   ```

   Which labels matter is decided by the field map; unknown labels are reported as unmapped
   and ignored. Full rules in `html-conversion.md`. Alternatively a ready `fielddata.json`.
2. **The collection**: a name from `collections/` (`blog`, `glossary`, `answers`), or a path
   to a field-map JSON via `--field-map`.
3. **Images**, only when the collection declares `images[]`: one master (≥ the largest
   target width, matching aspect ratio) and optional inline images in placeholder order.

Check readiness first — it tells you immediately whether a collection can publish at all:

```bash
python3 "$REPO/scripts/webflow-publisher.py" --list-collections
```

## Pipeline

Working files go in `$TMPDIR` (does not survive between sessions — fine for one run).

### 1. Convert the draft

```bash
python3 "$REPO/scripts/md_to_webflow_html.py" "$DRAFT" \
  --collection "$COLLECTION" --out "$TMPDIR/fielddata.json" --report "$TMPDIR/convert-report.json"
# --slug <slug>   override (still subject to the collection's slug rules)
# --date <iso>    value for the collection's date field (default: now, UTC)
# --html-only     print just the body HTML (blog-seo-content's opt-in HTML mode can use this)
```

The summary on stderr lists tables found (and tables in the source), inline placeholders,
unmapped labels, values parked under `__unconfirmed__`, and warnings such as an empty
required field. **If it warns about a missing field, ask the user to supply it** — do not
invent one. Do NOT hand-write conversion logic; the helper is the source of truth.

### 2. Internal links (when the calling skill uses the strategist's suggestions)

If the draft's links were already placed by the writer (glossary Related Terms), skip this.
Otherwise turn `internal-linking-strategist`'s draft-mode suggestions into a `links.json`
(shape in `scripts/apply_internal_links.py`) and place them deterministically:

```bash
python3 "$REPO/scripts/apply_internal_links.py" "$TMPDIR/fielddata.json" "$TMPDIR/links.json" \
  --collection "$COLLECTION"
```

It never links inside headings, existing links, table embeds or figures, and reports
`{applied, unplaced}`. Internal links open in the same tab (no `target="_blank"`).

### 3. Images (only if the collection declares image fields)

```bash
python3 "$REPO/scripts/resize_images.py" "$MASTER" "$SLUG" "$TMPDIR" \
  --collection "$COLLECTION" [--inline img-1.png img-2.png ...]
```

Writes `{slug}_{variant}_{w}x{h}.webp` per image field and `{slug}_img-N_{w}x{h}.webp` per
inline image, at the exact sizes the field map declares (the CMS fields use min=max
validation; the API rejects anything else). Pillow only — macOS `sips` cannot write WebP and
ffmpeg often lacks libwebp. Details and Drive-sourcing notes in `image-pipeline.md`.

### 4. Dry-run (always)

```bash
python3 "$REPO/scripts/webflow-publisher.py" "$TMPDIR/fielddata.json" --collection "$COLLECTION" \
  --image header="$TMPDIR/${SLUG}_page-header_1578x888.webp" \
  --image grid="$TMPDIR/${SLUG}_thumbnail_724x408.webp" \
  --image menu="$TMPDIR/${SLUG}_mega-menu_502x283.webp" \
  --inline "$TMPDIR/${SLUG}_img-1_1578x888.webp" ... \
  --source "$DRAFT" \
  --dry-run
```

Omit `--image`/`--inline` for collections without image fields. `--source` enables the
source-vs-output table count. It writes `dry-run-report.json` next to the fielddata and exits
non-zero on any failure. Checks: field-map readiness (no `null` required slugs), required
fields and `max_length`, slug rules, taxonomy consistency (e.g. Tags ⊇ Category),
`forbidden_body_strings`, no `<h1>`/`<style>`/`<script>`/`<iframe>`, internal links present
(when the map requires them), placeholder ↔ inline count, **structural table checks**
(`content:table-not-flattened`: no `<p>` carrying `| … |` syntax and no source table missing
from the output; `content:table-in-embed`: every `<table>` wrapped in
`<div data-rt-embed-type='true'>`; `content:table-structure`: `<thead>` + `<tbody>`), exact
image dimensions and `.webp` extension. Fix everything it flags, then re-run.

### 5. Publish

Same command without `--dry-run`. Add `--staged` to create the item for review (live on the
next Webflow site publish) instead of publishing immediately. Pre-flight runs first: one
`GET /sites/{id}` (token + scopes) and a slug lookup — a taken slug stops the run before any
upload. Then field images upload, inline images upload and replace their placeholders with
Webflow's full-width `<figure>`, and the item is created. Surface the result:

```
✓ Published: {live_url_prefix}{slug}
  Item ID: {itemId}
```

### Rewrite an EXISTING item in place (`--replace`)

For a rewrite that keeps the live slug and URL (the glossary's common case), do not create
a new item — pre-flight would reject the taken slug, and a suffix is forbidden anyway:

```bash
python3 "$REPO/scripts/webflow-publisher.py" "$TMPDIR/fielddata.json" --collection "$COLLECTION" \
  --replace <item_id> [--image role=… ...] [--inline …] [--source "$DRAFT"] --dry-run
python3 "$REPO/scripts/webflow-publisher.py" "$TMPDIR/fielddata.json" --collection "$COLLECTION" --replace <item_id>
```

Find `<item_id>` by slug: `GET /v2/collections/{collection}/items?slug={slug}`. The engine
verifies the live item's slug equals the draft's, PATCHes every field in `fielddata.json`
(fields not in the payload are preserved), re-uploads any images you pass, and publishes the
item. Images are optional in this mode (the dry-run skips `image:<role>:provided`); omitted
image fields keep their current files.

### Refresh images on an EXISTING item (`--update`)

```bash
python3 "$REPO/scripts/webflow-publisher.py" --update <item_id> --collection "$COLLECTION" \
  --image header=… --image grid=… --image menu=…      # any subset of the map's roles
```

Find `<item_id>` by slug: `GET /v2/collections/{collection}/items?slug={slug}`. The update
PATCHes **only** the given image fields (a partial update preserves everything else) and
publishes the item. Expect the response image URLs to DIFFER from what was sent: Webflow
re-ingests the file under a new fileId (your filename survives as the URL suffix). The
script verifies via the filename, not URL equality. `--dry-run` with `--update` checks
dimensions only.

## Adding or confirming a collection

Field maps live in `collections/` (schema in `collections/README.md`). To wire a new
content type: copy `glossary.json`, set `collection`, `collection_id`, `live_url_prefix`,
fill the slugs you have confirmed, leave `null` + a `_confirm` note for the rest, validate
with `python3 "$REPO/scripts/webflow_fieldmap.py" <name>`, add a fixture to `tests/`.
Collection IDs for existing collections are in the site inventories'
`website/pages-*.json` `_meta.collectionId`.

## No-token fallback: the Webflow MCP

If `WEBFLOW_API_TOKEN` is not set, the same flow works through the Webflow MCP's own OAuth
(run `--dry-run` first regardless — it needs no token):

1. `data_assets_tool > create_asset` — registers the asset; returns the presigned S3
   upload details and the final hostedUrl.
2. Upload the file to S3 yourself (curl with `--max-time 60`, or the multipart pattern
   in `webflow-publisher.py`). **Gotcha:** the MCP returns `uploadDetails` keys in
   camelCase, but S3 wants the exact form-field names — map them:
   `xAmzAlgorithm→X-Amz-Algorithm`, `xAmzCredential→X-Amz-Credential`,
   `xAmzDate→X-Amz-Date`, `policy→Policy`, `xAmzSignature→X-Amz-Signature`,
   `successActionStatus→success_action_status`, `contentType→Content-Type`,
   `cacheControl→Cache-Control`, plus `key`, `acl`, `bucket` as-is. The file part must
   be the LAST form field, named `file`. Success is HTTP **201**.
3. `data_cms_tool > create_collection_items` (or `update_collection_items`) with the
   `fieldData` from `fielddata.json` (image fields as `{"url": <hostedUrl>}`), then
   `publish_collection_items`.

## Error handling

| Error | Action |
|---|---|
| `--list-collections` says UNCONFIRMED / dry-run fails `fieldmap:required-slugs-confirmed` | Stop. The collection's field slugs must be read from Webflow and filled into `collections/<name>.json` first. Never guess them. |
| `WEBFLOW_API_TOKEN` not set | Use the Webflow MCP fallback above, or ask the user to `export WEBFLOW_API_TOKEN=…` |
| Master image too small / wrong ratio | Stop. Ask for a full-resolution export at the collection's aspect ratio. |
| Wrong image dimensions | The collection enforces exact sizes (min=max) — re-run `resize_images.py`. |
| `content:table-not-flattened` / `content:table-in-embed` fails | The draft's table did not survive conversion (check `--source` counts) or was hand-pasted as a bare `<table>`. Re-run the converter; never paste HTML by hand. |
| S3 upload fails | Retry once. If still failing, report the HTTP status and stop. |
| Network call hangs | Script calls time out by themselves (30s API / 60s S3) and exit with an error. Any hand-written curl must carry `--max-time`. |
| Webflow 401 | Token invalid or expired. Ask user to refresh `WEBFLOW_API_TOKEN`. |
| Webflow 403 on pre-flight | Token missing scopes — needs `sites:read`, `cms:write`, `assets:write`. |
| Pre-flight "slug already exists" / Webflow 400 slug | Stop. Surface the conflict — do not append any suffix. See NON-NEGOTIABLE rules. |
| Webflow 429 (rate limited) | Wait 10 s, retry once. |
| `python3` not found | Stop. The engine needs Python 3 (stdlib only); the resize helper additionally needs Pillow. |

## What NOT to publish

- Anything whose `--dry-run` did not pass on the current files.
- A draft that failed, or was not re-run through, the calling skill's own compliance script.
- Anything whose calling skill has a fired BLOCK condition (unverifiable claim, improvised
  internal link, missing named human editor at publish handoff — see that skill's SKILL.md).
- Body text still containing `[fill before publish]`, `OUTREACH VERSION`, `INTERNAL USE ONLY`
  or an `[OPTIONAL DISCLOSURE …]` line (the blog map lists these in `forbidden_body_strings`).

## Related skills

- `blog-publisher` — Google Doc listicle → this skill (`gdoc_to_fielddata.py` normalizes the
  doc export into the intermediate; webinar matching and the blog's positional CLIs live there)
- `glossary-content`, `blog-seo-content`, `aeo-content` — produce the drafts this skill publishes
- `internal-linking-strategist` — supplies the link suggestions `apply_internal_links.py` places
