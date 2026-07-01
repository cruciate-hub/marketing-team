---
name: blog-publisher
description: >
  Publishes a completed blog article from Google Docs directly to the
  social.plus Webflow blog — live, never draft. Accepts a Google Doc ID
  and a master PNG; resizes to the 3 required image sizes, uploads all
  assets, and publishes the CMS item immediately via Webflow Data API v2.

  Does NOT write content — for that, use blog-seo-content first.
  Does NOT accept Word documents — Google Docs only.

  Requires: WEBFLOW_API_TOKEN env var set with CMS write access.
when_to_use: >
  "publish blog", "post to Webflow", "upload to CMS", "put this live",
  "the article is ready", "publish listicle [N]".
  Must have a Google Doc URL/ID and a PNG file path. If either is missing, ask.
  If the user asks to write AND publish, run blog-seo-content first, then this.
---

# Blog Publisher

Reads a Google Doc, converts content to Webflow HTML, adds internal links,
resizes the master PNG to 3 sizes, uploads all assets, and publishes live.

## NON-NEGOTIABLE RULES

These override convenience, recovery shortcuts, and every other instruction below.

1. **A slug must NEVER contain a year OR the leading listicle count.** Strip both, so
   the slug survives a re-titled edition ("5 Best Chat SDKs" and a later "7 Best Chat
   SDKs (2027)" both map to the same URL — you can change the count or year without
   breaking links or creating a duplicate).
   - Title: `6 Best In-App Community Platforms for Consumer Apps (2026)`
   - ✅ slug: `best-in-app-community-platforms-for-consumer-apps`
   - ❌ `6-best-in-app-community-platforms-for-consumer-apps` (has the count)
   - ❌ `best-in-app-community-platforms-for-consumer-apps-2026` (has the year)
   - This applies to the title-derived slug, a user `--slug` override, AND — critically —
     **never resolve a slug collision by appending a year/number/suffix.**
   - `gdoc_to_fielddata.py` strips the leading count and every `19xx`/`20xx` token
     automatically. If you build a slug by hand, strip both yourself.

2. **On a slug collision (Webflow 400 "slug already exists"), STOP and ask the user.**
   Do NOT append anything to make it unique — not the year, not `-2`, not `-new`,
   not `-draft`. Webflow holds a slug permanently after an item is deleted (until the
   next full site publish clears the tombstone). Resolving a clash by appending a
   suffix is forbidden. Surface the conflict and let the user decide: update the
   existing item, pick a genuinely different slug, or publish the site to free the old one.

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

After the repo is ready, load these reference files in parallel:

```bash
cat "$REPO/brain.md"
cat "$REPO/marketing-team/skills/blog-publisher/webflow-config.md"
cat "$REPO/marketing-team/skills/blog-publisher/html-conversion.md"
cat "$REPO/marketing-team/skills/blog-publisher/image-pipeline.md"
cat "$REPO/messaging/terminology.md"
```

## Inputs

Confirm you have these before proceeding. If any are missing, ask:

1. **Google Doc ID** — from the URL: `docs.google.com/document/d/{DOC_ID}/edit`
2. **Master PNG** — absolute path to the hero image (must be ≥ 1578 px wide)
3. **Inline PNGs** (optional) — paths to body images, in section order (img-1 = first platform, img-2 = second, etc.)

## Phase 1 — Read the Google Doc

Use the Google Drive MCP tool with `fileId: {DOC_ID}` and save the raw response to a
file (a standalone helper script cannot reach the MCP):

```bash
# Save the Drive MCP output verbatim to a temp file
echo "$DRIVE_MCP_RAW_RESPONSE" > "$TMPDIR/raw-doc.txt"
```

The doc may contain multiple articles separated by `# Listicle N` headings.

- If multiple articles are present, list them with title + listicle number and ask which to publish.
- If the user already specified one (by number or partial title), use it.
- If only one article exists, proceed without asking.

## Phase 2 — Convert to fielddata.json

Run the helper — it does all metadata extraction, HTML conversion, category
mapping, slug derivation (year-stripped), and `__INLINE_IMG_N__` placeholder
insertion in one deterministic step. Do NOT hand-write conversion logic.

```bash
python3 "$REPO/scripts/gdoc_to_fielddata.py" \
  "$TMPDIR/raw-doc.txt" <listicle_number> \
  --out "$TMPDIR/fielddata.json"
# --slug <slug>   optional override; default strips a trailing "(YEAR)"
# --date <iso>    optional; defaults to a fixed date — set today's date
```

The helper prints a summary (name, slug, category count, char count, inline
placeholder count) and warns if `meta-description`, `post-summary`, or
`image-alt-text` came back empty. **If it warns about a missing field, ask the
user to supply it** — don't invent one. The conversion rules it applies are
documented in `html-conversion.md` for reference; the helper is the source of truth.

Inline placeholders (`__INLINE_IMG_1__` …) are inserted after each platform `<h2>`
(headings containing a colon, e.g. `social.plus: Best for…`). Section headings like
"What Is…", "How to Choose", "At-a-Glance" get none. `blog-publisher.py` replaces each
placeholder with a Webflow `<figure>` tag at publish time.

## Phase 3 — Internal linking

Invoke the `internal-linking-strategist` skill in **draft mode**. Pass:

- The converted HTML (post-content) — the `fielddata.json` from Phase 2
- Target keyword (from the article title)
- Category names
- Content type: `blog`

**Do not hand-embed the links** — that drifts (a long "Insert at" sentence fails to match
on punctuation/spacing). Instead, turn the strategist's suggestions into a `links.json`
and let the helper place them deterministically. For each suggestion the strategist
returns, capture:

```json
[
  {"anchor": "community SDK", "url": "https://www.social.plus/social/sdk",
   "insert_at": "<the strategist's verbatim 'Insert at' sentence>"},
  {"anchor": "content moderation", "url": "https://www.social.plus/moderation",
   "insert_at": "<original sentence>", "rephrase": "<the strategist's 'Rephrase suggestion'>"}
]
```

Include `insert_at` from every suggestion (it tells the helper *where*). Include `rephrase`
only when the strategist provided one (anchor isn't already in that sentence). Then:

```bash
python3 "$REPO/scripts/apply_internal_links.py" "$TMPDIR/fielddata.json" "$TMPDIR/links.json"
```

The helper locates each `insert_at` sentence (whitespace-flexible), wraps the anchor there
or swaps in the rephrase, never links inside headings or the comparison-table embed, and
prints a JSON summary `{applied, unplaced}`. For any `unplaced` entry (rare — neither the
anchor nor the sentence was found), apply that one by hand using its `rephrase`, or drop it.

Resolve any cannibalization warnings from the strategist before proceeding.

## Phase 4 — Compliance check

Run the compliance check from `brain.md`:

1. Terminology — no forbidden terms (from `terminology.md`)
2. Tone — sounds like social.plus, not default Claude
3. Claims — no fabricated stats, names, or quotes
4. Em dashes — replace `—` with comma, parentheses, or sentence restructure
5. Emojis — none in body text

Fix all violations before continuing. Do not flag and proceed.

## Phase 5 — Resize images

All production blog images are **WebP** at exact dimensions — the collection's image
fields enforce them (min=max validation), so the API rejects anything off-size. One
command does master + inline:

```bash
python3 "$REPO/scripts/resize_blog_images.py" "$PNG" "$SLUG" "$TMPDIR" \
  --inline "img-1.png" "img-2.png" ...    # omit --inline if no body images
```

It validates the master (≥ 1578 px wide, ~16:9), then writes
`{slug}_page-header_1578x888.webp`, `{slug}_thumbnail_724x408.webp`,
`{slug}_mega-menu_502x283.webp`, and `{slug}_img-N_1578x888.webp` per inline image.

Do NOT use `sips` or `ffmpeg` for the WebP step — macOS `sips` cannot write WebP
("Can't write format: org.webmproject.webp") and ffmpeg is often built without libwebp.
The helper uses Pillow, which works everywhere Python does; if Pillow is missing it
prints the install command and exits. PNG or WebP input both work (some designers ship
only a `*_page-header.webp` master — deriving the smaller sizes from it is fine; an
`*_open-graph.webp` variant has no CMS field and is unused).

Note on working files: `$TMPDIR` (and `/tmp` generally) does not survive between
sessions. Fine for a single publish run; anything you want to reuse later (downloaded
images, fielddata you may re-publish) belongs in a stable path instead.

## Phase 6 — Webinar matching

Every published blog post should have a related webinar set via the
`related-webinar-to-show-on-page` Reference field (points to the Webinars
collection `66e2765d540e1939a89db84e`). This phase picks the best match.

### Allowed webinar pool

Only webinars created **after** 2024-09-19 are eligible. The 24 older webinars
are excluded as outdated. The cutoff is the webinar "Understanding Zero-Party
Data (Part 3)" and everything before it.

The 22 allowed webinars with Webflow item IDs:

| ID | Slug |
|---|---|
| `670ce177f9a5437c8f42ab70` | `leveraging-gamification-and-in-app-interactions` |
| `670fd09afede82bbdd2681f9` | `why-social-features-are-essential-for-growth` |
| `673b3a2919c9b6b906a7f4e7` | `in-app-social-data-driven-innovation-and-digital-transformation` |
| `6744466b83a74e561a48b9c2` | `digitizing-the-football-fandom-experience` |
| `67508264108fc18c4aaf8526` | `from-acquisition-to-engagement-tuning-in-to-consumer-voices` |
| `67592d1ba11bc2120121e4fc` | `moderation-monetization-and-feedback` |
| `6788c3dbfb89b5cfbd1b195d` | `integrating-ai-and-manual-moderation-for-enhanced-community-engagement` |
| `679361ab4de547d8f18cf963` | `enhancing-ux-to-keep-players-coming-back` |
| `67aa2fc67637a3630ac104ea` | `driving-user-engagement-headspaces-approach` |
| `67b434e1013c296932839481` | `from-bookings-to-belonging-why-travel-apps-need-a-community-layer` |
| `67c173581ea64b42a6a222ad` | `building-engaging-health-tech` |
| `67c804913759af1f5564a120` | `revolutionizing-retail-master-social-driven-shopping-and-boost-customer-engagement` |
| `67f8cfdbea4aef476e15ed0c` | `mastering-app-stickiness-how-gamified-profiles-drive-user-retention` |
| `680b648f197b3f75226eb1c0` | `how-cnbc-builds-trust-through-engagement-and-education` |
| `6819e4850c9747df05432d8d` | `launch-in-app-communities-faster-with-the-new-ui-kit-4` |
| `6846c6b79dfc413c0061a8c1` | `doing-moderation-right-how-to-build-trust-in-your-in-app-community` |
| `686e2ff8d323fe2a62ff0b29` | `how-to-build-sticky-social-features-without-slowing-your-team` |
| `689c75839fa59f8a6eddc65e` | `why-brands-are-bringing-short-form-video-inside-their-apps` |
| `69379ec4b4a7543f891fdfbf` | `integrating-webhooks-and-real-time-events-with-your-tech-stack-from-dashboards-to-engagement` |
| `69ca544a27e94726c5bfc898` | `how-to-build-a-community-that-shows-up-events-and-livestream-in-practice` |
| `6a0d84b6e70d843b95c1de9a` | `from-engagement-to-revenue-building-commerce-into-every-community-moment` |
| `6a2a96c52e68776c0cc1230a` | `working-with-the-social-plus-mcp-server-a-live-build-in-claude-cursor-vs-code` |

When new webinars are added to the collection, add them to this table.
When the pool grows stale, move the cutoff date forward and remove old entries.

### Priority matching by vertical

Match the blog's topic to the closest webinar. Use this table as a starting
point, then fall back to topical judgment for articles that span multiple
verticals.

| Blog vertical / topic | First-choice webinar slug |
|---|---|
| Retail / e-commerce | `revolutionizing-retail-master-social-driven-shopping-and-boost-customer-engagement` |
| Gaming / betting / esports | `enhancing-ux-to-keep-players-coming-back` |
| Fitness / wellness / health | `building-engaging-health-tech` |
| Travel / hospitality | `from-bookings-to-belonging-why-travel-apps-need-a-community-layer` |
| Sports / fandom | `digitizing-the-football-fandom-experience` |
| Media / news / publishing | `how-cnbc-builds-trust-through-engagement-and-education` |
| Moderation / trust & safety | `doing-moderation-right-how-to-build-trust-in-your-in-app-community` |
| AI + moderation | `integrating-ai-and-manual-moderation-for-enhanced-community-engagement` |
| SDK / build-vs-buy / developer tooling | `how-to-build-sticky-social-features-without-slowing-your-team` |
| UIKit / implementation / quick start | `launch-in-app-communities-faster-with-the-new-ui-kit-4` |
| Gamification / profiles / retention | `mastering-app-stickiness-how-gamified-profiles-drive-user-retention` |
| Video / short-form / livestream content | `why-brands-are-bringing-short-form-video-inside-their-apps` |
| Events / livestream / community building | `how-to-build-a-community-that-shows-up-events-and-livestream-in-practice` |
| Monetization / commerce / revenue | `from-engagement-to-revenue-building-commerce-into-every-community-moment` |
| Webhooks / integration / tech stack | `integrating-webhooks-and-real-time-events-with-your-tech-stack-from-dashboards-to-engagement` |
| Engagement / social features (general) | `why-social-features-are-essential-for-growth` |
| Mindfulness / meditation / mental health | `driving-user-engagement-headspaces-approach` |
| Product growth / data / innovation | `in-app-social-data-driven-innovation-and-digital-transformation` |
| Gamification / activation / onboarding | `leveraging-gamification-and-in-app-interactions` |
| MCP / developer tools / Claude integration | `working-with-the-social-plus-mcp-server-a-live-build-in-claude-cursor-vs-code` |

**Fallback:** When no vertical-specific match fits, use
`moderation-monetization-and-feedback` (`67592d1ba11bc2120121e4fc`). It covers
community trends broadly and works as a catch-all.

### How to apply

**During a new publish (this skill):**

1. After Phase 5, look up the best webinar from the priority table above.
2. Add `"related-webinar-to-show-on-page": "<item-id>"` to the fielddata.
3. If the match is ambiguous, pick the webinar whose title a reader would
   find most relevant after finishing the blog post.

**Bulk backfill (all blogs with null webinar):**

1. `data_cms_tool > list_collection_items` on the Blog Posts collection
   (paginate with offset; max 100 per call).
2. Filter for items where `related-webinar-to-show-on-page` is null.
3. Match each to the best webinar using the priority table.
4. `data_cms_tool > update_collection_items` with the webinar ID.
5. `data_cms_tool > publish_collection_items` to push live.

If `related-webinar-to-show-on-page` is already set, skip unless the user
explicitly asks to re-evaluate.

## Phase 7 — Build and publish

1. Look up the category ID(s) from `webflow-config.md` using the extracted category name(s).

2. Build `fielddata.json` in `$TMPDIR`:

```json
{
  "name":                      "...",
  "slug":                      "...",
  "post-summary":              "...",
  "post-content":              "<h2>...</h2><p>...</p>...",
  "meta-description":          "...",
  "min-read":                  "12",
  "date-published":            "2026-06-04T00:00:00.000Z",
  "image-alt-text":            "...",
  "category":                  "<main-category-id>",
  "category-multi-reference-3": ["<id1>", "<id2>", "<id3>"],
  "featured":                  false,
  "blog-without-images":       false,
  "show-on-careers-page":      false
}
```

Use today's date for `date-published` (ISO 8601 UTC).
For `category-multi-reference-3`, always include the main category ID plus any secondary tag IDs.

3. **Always dry-run first.** Append `--dry-run` to validate the entire payload
   (required fields, slug-has-no-year, table not flattened, no `<style>` block,
   placeholder/inline count match, exact image dimensions) without touching the API.
   It writes `dry-run-report.json` and exits non-zero on any failure. Fix anything it
   flags before the real run. This is cheap insurance against a broken publish.
   Use the absolute `$REPO/scripts/...` path so it works from any working directory:

```bash
python3 "$REPO/scripts/blog-publisher.py" \
  "$TMPDIR/fielddata.json" \
  "$TMPDIR/${SLUG}_page-header_1578x888.webp" \
  "$TMPDIR/${SLUG}_thumbnail_724x408.webp" \
  "$TMPDIR/${SLUG}_mega-menu_502x283.webp" \
  "$TMPDIR/${SLUG}_img-1_1578x888.webp" ... \
  --dry-run
```

4. Run the real publish — same command, swap `--dry-run` for `--staged` (review
   before going live) or no flag (publish immediately). Hero images first, inline after:

```bash
python3 "$REPO/scripts/blog-publisher.py" \
  "$TMPDIR/fielddata.json" \
  "$TMPDIR/${SLUG}_page-header_1578x888.webp" \
  "$TMPDIR/${SLUG}_thumbnail_724x408.webp" \
  "$TMPDIR/${SLUG}_mega-menu_502x283.webp" \
  "$TMPDIR/${SLUG}_img-1_1578x888.webp" \
  "$TMPDIR/${SLUG}_img-2_1578x888.webp" \
  ... \
  --staged
```

Note: the helper scripts live at the repo root (`$REPO/scripts/`), not inside the
skill folder. Always invoke them with the `$REPO/scripts/...` absolute path.

Inline images are passed as additional positional args after the 3 hero images.
The script uploads them and replaces `__INLINE_IMG_1__` … `__INLINE_IMG_6__`
placeholders in `post-content` with real Webflow CDN URLs before publish.

Omit inline image args if the article has no body images.

The script prints the live URL to stdout on success. Surface it to the user:

```
✓ Published: https://www.social.plus/blog/{slug}
  Item ID: {itemId}
```

## Updating images on an EXISTING post (refresh mode)

When a designer delivers new hero images for an already-published post (e.g. a periodic
image refresh), do NOT re-create the post — refresh it in place:

```bash
# 1. Resize the new master to the 3 exact sizes
python3 "$REPO/scripts/resize_blog_images.py" "$NEW_PNG" "$SLUG" "$TMPDIR"

# 2. Re-upload + patch + publish in one command
python3 "$REPO/scripts/blog-publisher.py" --update <item_id> \
  "$TMPDIR/${SLUG}_page-header_1578x888.webp" \
  "$TMPDIR/${SLUG}_thumbnail_724x408.webp" \
  "$TMPDIR/${SLUG}_mega-menu_502x283.webp"
```

Find the `<item_id>` by slug: `GET /v2/collections/{collection}/items?slug={slug}`.
The update PATCHes **only** the 3 image fields — a partial update preserves every other
field, so the post's content, links, and metadata are untouched.

Expect the response image URLs to DIFFER from what was sent: Webflow re-ingests the
file under a new fileId on update (your filename survives as the URL suffix). That is
normal — the script verifies via the filename, not URL equality.

If image sources come from Google Drive: `download_file_content` returns large files as
a sidecar `.txt` (JSON with a base64 `content` field) under the project's
`tool-results/` directory — decode it and confirm the bytes start with `RIFF…WEBP`.
A direct `drive.google.com/uc?export=download` curl fails for non-link-shared files
(returns the login page); the Drive MCP is the only reliable path. Designer folders are
usually named by blog TITLE, not slug — match them to CMS items via a slug lookup.

## No-token fallback: the Webflow MCP

If `WEBFLOW_API_TOKEN` is not set, the same flow works through the Webflow MCP's own
OAuth — no token needed:

1. `data_assets_tool > create_asset` — registers the asset; returns the presigned S3
   upload details and the final hostedUrl.
2. Upload the file to S3 yourself (curl with `--max-time 60`, or the multipart pattern
   in `blog-publisher.py`). **Gotcha:** the MCP returns `uploadDetails` keys in
   camelCase, but S3 wants the exact form-field names — map them:
   `xAmzAlgorithm→X-Amz-Algorithm`, `xAmzCredential→X-Amz-Credential`,
   `xAmzDate→X-Amz-Date`, `policy→Policy`, `xAmzSignature→X-Amz-Signature`,
   `successActionStatus→success_action_status`, `contentType→Content-Type`,
   `cacheControl→Cache-Control`, plus `key`, `acl`, `bucket` as-is. The file part must
   be the LAST form field, named `file`. Success is HTTP **201**.
3. `data_cms_tool > update_collection_items` (or `create_collection_items`), then
   `publish_collection_items`.

## Error handling

| Error | Action |
|---|---|
| `WEBFLOW_API_TOKEN` not set | Use the Webflow MCP fallback above, or ask the user to `export WEBFLOW_API_TOKEN=…` |
| Google Doc unreadable (401) | Stop. Tell user to check file sharing permissions. |
| PNG width < 1578 px | Stop. Ask for the full-resolution export (min 1578×888 px). |
| Wrong image dimensions | The collection enforces exact sizes (min=max) — the API rejects off-size images. Re-run the resize helper. |
| S3 upload fails | Retry once. If still failing, report the HTTP status and stop. |
| Network call hangs | Script calls time out by themselves (30s API / 60s S3) and exit with an error. Any hand-written curl must carry `--max-time`. |
| Webflow 401 | Token invalid or expired. Ask user to refresh `WEBFLOW_API_TOKEN`. |
| Webflow 400 "slug already exists" | Stop. Surface the conflict — do not append any suffix. See Slug rules above. |
| Webflow 429 (rate limited) | Wait 10 s, retry once. |
| `python3` not found | Stop. The publish script needs Python 3 (stdlib only); the resize helper additionally needs Pillow. |

## What NOT to publish

- Content that fails the compliance check — fix first, then re-run
- Posts that still contain `INTERNAL USE ONLY` or `OUTREACH VERSION` sections
- Posts with the `[OPTIONAL DISCLOSURE]` line accidentally left in (remove it unless user confirms it should stay)
- Posts whose primary keyword is flagged as cannibalized by `internal-linking-strategist` — surface the warning and let the user decide before publishing
