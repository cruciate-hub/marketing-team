# Image Pipeline — Resize, Convert to WebP, Upload

## Format: WebP only

All production blog images on social.plus use **WebP** (`.webp`).
The input from the designer is PNG. The pipeline resizes and converts to WebP in one step.

CDN URL pattern observed in production:
`https://cdn.prod.website-files.com/66e2765d540e1939a89db4e3/{assetId}_{filename}.webp`

## File naming convention (must match production)

| Variant | Filename |
|---|---|
| Page header (1578×888) | `{Article Title}_page-header.webp` |
| Grid thumbnail (724×408) | `{Article Title}_thumbnail.webp` |
| Mega menu (502×283) | `{Article Title}_mega-menu.webp` |

Use the article title as-is (not the slug). Spaces are fine — `sips` handles them.
Example for "6 Best In-App Community Platforms for Consumer Apps (2026)":
- `6 Best In-App Community Platforms for Consumer Apps (2026)_page-header.webp`
- `6 Best In-App Community Platforms for Consumer Apps (2026)_thumbnail.webp`
- `6 Best In-App Community Platforms for Consumer Apps (2026)_mega-menu.webp`

## Resize + convert with sips (macOS built-in)

`sips` handles resize AND WebP conversion in a single command.
Syntax: `sips -z <height> <width> -s format webp <input> --out <output>`

```bash
PNG="{absolute path to master PNG from user}"
TITLE="{article title, e.g. 6 Best In-App Community Platforms for Consumer Apps (2026)}"
TMPDIR=$(mktemp -d)

# Validate input
WIDTH=$(sips -g pixelWidth "$PNG" | awk '/pixelWidth/ {print $2}')
if [ "$WIDTH" -lt 1578 ]; then
  echo "ERROR: PNG is ${WIDTH}px wide — minimum required is 1578px. Ask for a higher-res export."
  exit 1
fi

# Resize to 3 sizes and convert to WebP in one step
sips -z 888 1578 -s format webp "$PNG" --out "$TMPDIR/${TITLE}_page-header.webp"
sips -z 408  724 -s format webp "$PNG" --out "$TMPDIR/${TITLE}_thumbnail.webp"
sips -z 283  502 -s format webp "$PNG" --out "$TMPDIR/${TITLE}_mega-menu.webp"

echo "Header:  $TMPDIR/${TITLE}_page-header.webp"
echo "Grid:    $TMPDIR/${TITLE}_thumbnail.webp"
echo "Menu:    $TMPDIR/${TITLE}_mega-menu.webp"
```

## Upload to Webflow (via blog-publisher.py)

The Python script handles the 3-step upload automatically:
1. MD5 hash of file binary
2. `POST /v2/sites/{siteId}/assets` → S3 pre-signed URL
3. POST WebP file to S3 as `image/webp`
4. `GET /v2/sites/{siteId}/assets/{id}` → retrieve `hostedUrl`

The script uses `Path(file).name` as the upload filename, so name your WebP files
correctly before passing them (the sips commands above do this automatically).

The resulting CMS image objects match production format:
```json
{
  "fileId": "<webflow-asset-id>",
  "url": "https://cdn.prod.website-files.com/66e2765d540e1939a89db4e3/..._page-header.webp",
  "alt": null
}
```

Note: `alt` is always `null` inside image objects. The `image-alt-text` PlainText field
on the CMS item is the separate accessible description — set that field in fielddata.json.

## Linux fallback (ImageMagick + cwebp)

If `sips` is unavailable:
```bash
# Resize with ImageMagick, then convert to WebP
convert "$PNG" -resize 1578x888^ -gravity Center -extent 1578x888 \
        -quality 90 "${TITLE}_page-header.webp"
convert "$PNG" -resize 724x408^  -gravity Center -extent 724x408  \
        -quality 90 "${TITLE}_thumbnail.webp"
convert "$PNG" -resize 502x283^  -gravity Center -extent 502x283  \
        -quality 90 "${TITLE}_mega-menu.webp"
```

## Troubleshooting

**"PNG too small"** — needs ≥ 1578 px wide. Ask for full-res Figma export (not a preview).

**S3 upload 403 / expired URL** — pre-signed URLs expire quickly. Re-run the full pipeline.

**WebP not supported by sips** — macOS 10.14+. If on older macOS, use ImageMagick fallback above.
