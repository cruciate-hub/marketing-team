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

After the repo is ready, load these reference files in parallel:

```bash
cat "$REPO/brain.md"
cat "$REPO/marketing-team/skills/blog-publisher/webflow-config.md"
cat "$REPO/marketing-team/skills/blog-publisher/html-conversion.md"
cat "$REPO/marketing-team/skills/blog-publisher/image-pipeline.md"
cat "$REPO/messaging/terminology.md"
```

## Inputs

Confirm you have both before proceeding. If either is missing, ask:

1. **Google Doc ID** — from the URL: `docs.google.com/document/d/{DOC_ID}/edit`
2. **PNG file path** — absolute path to the master image (must be ≥ 1578 px wide)

## Phase 1 — Read the Google Doc

Use the Google Drive MCP tool with `fileId: {DOC_ID}`.

The doc may contain multiple articles separated by `# Listicle N` headings.

- If multiple articles are present, list them with title + listicle number and ask which to publish.
- If the user already specified one (by number or partial title), find it.
- If only one article exists, proceed without asking.

From the selected article, extract these fields:

| Field | Location in doc |
|---|---|
| `name` | `**Page title:**` line |
| `slug` | Derive from name: lowercase, replace spaces with hyphens, strip special chars. Max 60 chars. |
| `post-summary` | `**Introduction text**` section (the paragraph after it, before the first `###`) |
| `meta-description` | `**Meta description**` line |
| `min-read` | `**Minutes to read:**` line (extract the number as a string) |
| `category` (name) | `**Main Category Tag:**` line |
| `image-alt-text` | `Image alt text:` line |
| Post content | Everything from the first `###` heading through the "How to Choose" section |

Do NOT include in post-content: metadata block, `Image alt text:` and subsequent lines,
`Display recommendations:` block, `OUTREACH VERSION` section, `INTERNAL USE ONLY` section,
or `[OPTIONAL DISCLOSURE: ...]` line.

## Phase 2 — Convert to HTML

Follow `html-conversion.md` exactly. Key rules:

- `### Heading` → `<h2>`, `#### Sub-heading` → `<h3>`
- `**bold**` → `<strong>`, `*italic*` → `<em>`
- Lists → `<ul><li>`, tables → `<table><thead><tbody>`
- All links → `<a href="..." target="_blank">`
- No `<h1>`, no `<div>`, no `style` attributes
- Strip escaped asterisks (`\*\*`) left by Google Doc export
- Strip bold from inside table cells (plain text only in `<td>/<th>`)

## Phase 3 — Internal linking

Invoke the `internal-linking-strategist` skill in **draft mode**. Pass:

- The converted HTML (post-content)
- Target keyword (from the article title)
- Category names
- Content type: `blog`

Embed the returned 3–7 `<a href="..." target="_blank">` tags into the HTML at the
suggested insertion points. Resolve any cannibalization warnings before proceeding.

## Phase 4 — Compliance check

Run the compliance check from `brain.md`:

1. Terminology — no forbidden terms (from `terminology.md`)
2. Tone — sounds like social.plus, not default Claude
3. Claims — no fabricated stats, names, or quotes
4. Em dashes — replace `—` with comma, parentheses, or sentence restructure
5. Emojis — none in body text

Fix all violations before continuing. Do not flag and proceed.

## Phase 5 — Resize images

Follow `image-pipeline.md`. Run these bash commands:

```bash
PNG="{absolute path from user input}"
SLUG="{derived slug}"
TMPDIR=$(mktemp -d)

# Validate input
WIDTH=$(sips -g pixelWidth "$PNG" | awk '/pixelWidth/ {print $2}')
if [ "$WIDTH" -lt 1578 ]; then
  echo "ERROR: PNG is ${WIDTH}px wide — minimum required is 1578px"
  exit 1
fi

# Resize
sips -z 888 1578 "$PNG" --out "$TMPDIR/${SLUG}-header.png"
sips -z 408  724 "$PNG" --out "$TMPDIR/${SLUG}-grid.png"
sips -z 283  502 "$PNG" --out "$TMPDIR/${SLUG}-menu.png"
echo "$TMPDIR"
```

If sips is not available (Linux), use the ImageMagick fallback in `image-pipeline.md`.

## Phase 6 — Build and publish

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

3. Run the publish script:

```bash
cd "$REPO"
python3 scripts/blog-publisher.py \
  "$TMPDIR/fielddata.json" \
  "$TMPDIR/${SLUG}-header.png" \
  "$TMPDIR/${SLUG}-grid.png" \
  "$TMPDIR/${SLUG}-menu.png"
```

The script prints the live URL to stdout on success. Surface it to the user:

```
✓ Published: https://www.social.plus/blog/{slug}
  Item ID: {itemId}
```

## Error handling

| Error | Action |
|---|---|
| `WEBFLOW_API_TOKEN` not set | Stop. Tell user: `export WEBFLOW_API_TOKEN=your_token` |
| Google Doc unreadable (401) | Stop. Tell user to check file sharing permissions. |
| PNG width < 1578 px | Stop. Ask for the full-resolution export (min 1578×888 px). |
| S3 upload fails | Retry once. If still failing, report the HTTP status and stop. |
| Webflow 401 | Token invalid or expired. Ask user to refresh `WEBFLOW_API_TOKEN`. |
| Webflow 400 "slug already exists" | Suggest appending `-2026` to the slug and ask user to confirm. |
| Webflow 429 (rate limited) | Wait 10 s, retry once. |
| `requests` not installed | Stop. Tell user: `pip install requests` |

## What NOT to publish

- Content that fails the compliance check — fix first, then re-run
- Posts that still contain `INTERNAL USE ONLY` or `OUTREACH VERSION` sections
- Posts with the `[OPTIONAL DISCLOSURE]` line accidentally left in (remove it unless user confirms it should stay)
- Posts whose primary keyword is flagged as cannibalized by `internal-linking-strategist` — surface the warning and let the user decide before publishing
