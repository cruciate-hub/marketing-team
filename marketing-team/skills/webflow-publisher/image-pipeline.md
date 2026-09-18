# Image Pipeline — Resize, Convert to WebP, Upload

## Format: WebP at EXACT dimensions, sizes from the field map

Production images are **WebP** at exact dimensions. A collection's image fields enforce
exact sizes (min=max validation) — the API **rejects** anything off-size. The sizes live in
that content-type skill's own `webflow-fields.json` (`images[]` for CMS image fields,
`inline_images` for body figures), never in a script. For the blog:

| Role | Variant | Size | CMS field |
|---|---|---|---|
| `header` | `page-header` | 1578 × 888 | `image-page-header` |
| `grid` | `thumbnail` | 724 × 408 | `grid-thumbnail` |
| `menu` | `mega-menu` | 502 × 283 | `thumbnail-mega-menu` |
| inline | `img-N` | 1578 × 888 | inside the body as `<figure>` |

The glossary and answers maps currently declare **no** image fields (unknown — see their
`_images_confirm` notes); the resize step is skipped for them and `--image` is refused.

File naming: `{slug}_{variant}_{width}x{height}.webp` — self-documenting in the asset
library and produced automatically by the resize helper.

## Resize: Pillow via the helper (the ONLY reliable path)

```bash
python3 "$REPO/scripts/resize_images.py" <master.png|webp> <slug> <outdir> --collection <name> \
  [--inline img1.png img2.png ...]
# blog shorthand (same thing with --collection blog):
python3 "$REPO/scripts/resize_blog_images.py" <master> <slug> <outdir> [--inline ...]
```

The helper validates the master (at least as wide as the largest target, and the targets'
aspect ratio within 2%, so nothing distorts), then emits every size the map declares plus
`{slug}_img-N_{w}x{h}.webp` per inline image. Pillow, LANCZOS, quality 90.

**Why not sips or ffmpeg:** macOS `sips` cannot write WebP — it fails with
`Error 13: Can't write format: org.webmproject.webp` (observed on Darwin 25). ffmpeg is
commonly built without libwebp (`Unknown encoder 'libwebp'`). Pillow works everywhere
Python does. If Pillow is missing, the helper prints the install command and exits
(macOS's system Python blocks plain `pip install`; use
`python3 -m pip install --break-system-packages Pillow` or a venv).

Accepted input: PNG or WebP. Some designers deliver only a `*_page-header.webp` master —
deriving the smaller sizes from it is fine.

## Dimension checks in the dry-run

`webflow-publisher.py --dry-run` opens every `--image` and `--inline` file with Pillow and
compares against the map. Without Pillow the check is skipped and says so; **with** Pillow,
an unreadable file is a FAIL (it used to be silently skipped). The `.webp` extension is
checked regardless.

## Sourcing images from Google Drive

- `download_file_content` returns small files inline (base64). **Large files arrive as a
  sidecar `.txt`** under `~/.claude/projects/<project>/tool-results/` containing JSON
  `{content, id, mimeType, title}` — base64-decode the `content` field and verify the
  bytes start with `RIFF…WEBP` (or the PNG magic) before using them.
- A direct `curl https://drive.google.com/uc?export=download&id=…` fails for files that
  aren't link-shared (it returns the login HTML page). The Drive MCP is the only
  reliable path.
- Designer folder convention: `<Blog Title>/Thumbnail/{WebP,PNG}/…`, with `.DS_Store`
  noise throughout. Folder names are blog **titles**, not slugs — match them to CMS
  items with a slug lookup (`GET /items?slug=…`). Some folders ship every variant plus
  an `*_open-graph.webp`, which has **no CMS field** — ignore it.

## Upload to Webflow

`webflow-publisher.py` handles the upload (register asset → multipart POST to S3 → use the
S3 hostedUrl). Key facts, all verified in production:

- The usable URL is `https://s3.amazonaws.com/{bucket}/{key}` built from
  `uploadDetails` — a hand-constructed `cdn.prod.website-files.com` URL 403s, and an
  image field fed a 403 URL is **silently dropped**.
- S3 multipart: form fields first, the file part LAST (named `file`). Success is HTTP
  **201** (the `success_action_status`). All calls carry timeouts (30s API / 60s S3) —
  a hung connection exits with an error instead of blocking forever.
- Webflow dedupes assets by `fileHash`: identical bytes across items return the existing
  asset under its *original* filename. Functionally fine (same image); the asset-library
  name just won't match the new item's slug.
- Via the **Webflow MCP** instead (no token): `data_assets_tool > create_asset` returns
  the same details but with **camelCase keys** — map them to the exact S3 form-field
  names (`xAmzAlgorithm→X-Amz-Algorithm`, `policy→Policy`,
  `successActionStatus→success_action_status`, etc.) or S3 rejects the POST.

## Updating images on an existing item

Use `webflow-publisher.py --update <item_id> --collection <name> --image <role>=<path> …`
(see SKILL.md). Two behaviours that look like bugs but aren't:

- **Webflow rewrites the URL on update.** PATCHing an image field makes Webflow
  re-ingest the file under a NEW fileId; the response URL differs from what you sent
  (your filename survives as the suffix). Verify by filename, never by URL equality.
- **Partial updates are safe.** Sending only the image fields in `fieldData` preserves
  every other field — no need to round-trip the whole item. `{"url": …}` alone is a
  sufficient image-field payload.

## Working-file hygiene

`/tmp` (and `mktemp -d`) does not survive between sessions. Fine for a single publish
run; put anything reusable (downloaded sources, fielddata you may re-publish) in a
stable path.
