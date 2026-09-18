# Image Pipeline — Resize, Convert to WebP, Upload

## Format: WebP at EXACT dimensions

All production blog images are **WebP**. The Blog collection's image fields enforce
exact dimensions (min=max validation) — the API **rejects** anything off-size:

| Variant | Size | CMS field |
|---|---|---|
| Page header | 1578 × 888 | `image-page-header` |
| Grid thumbnail | 724 × 408 | `grid-thumbnail` |
| Mega menu | 502 × 283 | `thumbnail-mega-menu` |
| Inline body images | 1578 × 888 | (inside `post-content` as `<figure>`) |

File naming: `{slug}_{variant}_{width}x{height}.webp` — self-documenting in the asset
library and produced automatically by the resize helper.

## Resize: Pillow via the helper (the ONLY reliable path)

```bash
python3 "$REPO/scripts/resize_blog_images.py" <master.png|webp> <slug> <outdir> \
  [--inline img1.png img2.png ...]
```

The helper validates the master (≥ 1578 px wide, ~16:9 so nothing distorts), then emits
all hero sizes plus `{slug}_img-N_1578x888.webp` per inline image. Pillow, LANCZOS,
quality 90.

**Why not sips or ffmpeg:** macOS `sips` cannot write WebP — it fails with
`Error 13: Can't write format: org.webmproject.webp` (observed on Darwin 25). ffmpeg is
commonly built without libwebp (`Unknown encoder 'libwebp'`). Pillow works everywhere
Python does. If Pillow is missing, the helper prints the install command and exits
(macOS's system Python blocks plain `pip install`; use
`python3 -m pip install --break-system-packages Pillow` or a venv).

Accepted input: PNG or WebP. Some designers deliver only a `*_page-header.webp` master —
deriving the smaller sizes from it is fine.

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

`blog-publisher.py` handles the upload (register asset → multipart POST to S3 → use the
S3 hostedUrl). Key facts, all verified in production:

- The usable URL is `https://s3.amazonaws.com/{bucket}/{key}` built from
  `uploadDetails` — a hand-constructed `cdn.prod.website-files.com` URL 403s, and an
  image field fed a 403 URL is **silently dropped**.
- S3 multipart: form fields first, the file part LAST (named `file`). Success is HTTP
  **201** (the `success_action_status`). All calls carry timeouts (30s API / 60s S3) —
  a hung connection exits with an error instead of blocking forever.
- Via the **Webflow MCP** instead (no token): `data_assets_tool > create_asset` returns
  the same details but with **camelCase keys** — map them to the exact S3 form-field
  names (`xAmzAlgorithm→X-Amz-Algorithm`, `policy→Policy`,
  `successActionStatus→success_action_status`, etc.) or S3 rejects the POST.

## Updating images on an existing post

Use `blog-publisher.py --update <item_id> <header> <grid> <menu>` (see SKILL.md).
Two behaviours that look like bugs but aren't:

- **Webflow rewrites the URL on update.** PATCHing an image field makes Webflow
  re-ingest the file under a NEW fileId; the response URL differs from what you sent
  (your filename survives as the suffix). Verify by filename, never by URL equality.
- **Partial updates are safe.** Sending only the 3 image fields in `fieldData`
  preserves every other field — no need to round-trip the whole item. `{"url": …}`
  alone is a sufficient image-field payload.

## Working-file hygiene

`/tmp` (and `mktemp -d`) does not survive between sessions. Fine for a single publish
run; put anything reusable (downloaded sources, fielddata you may re-publish) in a
stable path.
