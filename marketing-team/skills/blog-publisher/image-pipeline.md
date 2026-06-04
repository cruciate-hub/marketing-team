# Image Pipeline — Resize, Convert to WebP, Upload

## Format: WebP only

All production blog images on social.plus use **WebP** (`.webp`).
The input from the designer is PNG. The pipeline resizes and converts to WebP in one step.

CDN URL pattern observed in production:
`https://cdn.prod.website-files.com/66e2765d540e1939a89db4e3/{assetId}_{filename}.webp`

## File naming convention

Format: `{slug}_{variant}_{width}x{height}.webp`

| Variant | Filename |
|---|---|
| Page header | `{slug}_page-header_1578x888.webp` |
| Grid thumbnail | `{slug}_thumbnail_724x408.webp` |
| Mega menu | `{slug}_mega-menu_502x283.webp` |

Use the CMS slug (lowercase, hyphens, no spaces). Dimensions are embedded in the
filename so the file is self-documenting in the Webflow asset library.

Example for slug `6-best-in-app-community-platforms-for-consumer-apps`:
```
6-best-in-app-community-platforms-for-consumer-apps_page-header_1578x888.webp
6-best-in-app-community-platforms-for-consumer-apps_thumbnail_724x408.webp
6-best-in-app-community-platforms-for-consumer-apps_mega-menu_502x283.webp
```

## Resize + convert with sips (macOS built-in)

`sips` resizes AND converts to WebP in a single pass.
Syntax: `sips -z <height> <width> -s format webp <input> --out <output>`

```bash
PNG="{absolute path to master PNG from user}"
SLUG="{cms slug, e.g. 6-best-in-app-community-platforms-for-consumer-apps}"
TMPDIR=$(mktemp -d)

# Validate: must be at least 1578 px wide
WIDTH=$(sips -g pixelWidth "$PNG" | awk '/pixelWidth/ {print $2}')
if [ "$WIDTH" -lt 1578 ]; then
  echo "ERROR: PNG is ${WIDTH}px wide — minimum 1578px required."
  exit 1
fi

# Resize to 3 sizes and convert to WebP
sips -z 888 1578 -s format webp "$PNG" --out "$TMPDIR/${SLUG}_page-header_1578x888.webp"
sips -z 408  724 -s format webp "$PNG" --out "$TMPDIR/${SLUG}_thumbnail_724x408.webp"
sips -z 283  502 -s format webp "$PNG" --out "$TMPDIR/${SLUG}_mega-menu_502x283.webp"

echo "Header:  $TMPDIR/${SLUG}_page-header_1578x888.webp"
echo "Grid:    $TMPDIR/${SLUG}_thumbnail_724x408.webp"
echo "Menu:    $TMPDIR/${SLUG}_mega-menu_502x283.webp"
```

Note on pixel rounding: the 3 target sizes are all approximately 16:9 but not exactly
(whole pixels only). `sips` stretches to exact dimensions. This is imperceptible and
expected — always work with whole pixels, never sub-pixel values.

## Upload to Webflow (via blog-publisher.py)

The Python script handles the full 3-step upload:
1. MD5 hash of file binary
2. `POST /v2/sites/{siteId}/assets` → S3 pre-signed URL + signing headers
3. POST WebP file to S3 as `image/webp`
4. `GET /v2/sites/{siteId}/assets/{id}` → retrieve `hostedUrl`

The script uses `Path(file).name` as the registered filename — the sips commands
above already produce the correct names, so pass them through unchanged.

The resulting CMS image objects:
```json
{
  "fileId": "<webflow-asset-id>",
  "url": "https://cdn.prod.website-files.com/66e2765d540e1939a89db4e3/..._page-header_1578x888.webp",
  "alt": null
}
```

Note: `alt` is `null` inside image objects — this matches all production posts.
The accessible description goes in the standalone `image-alt-text` PlainText field.

## Linux fallback (ImageMagick)

```bash
convert "$PNG" -resize 1578x888! -quality 90 "${SLUG}_page-header_1578x888.webp"
convert "$PNG" -resize 724x408!  -quality 90 "${SLUG}_thumbnail_724x408.webp"
convert "$PNG" -resize 502x283!  -quality 90 "${SLUG}_mega-menu_502x283.webp"
```
(`!` forces exact dimensions matching sips behaviour.)

## Troubleshooting

**PNG too small** — needs ≥ 1578 px wide. Ask for the full-resolution Figma export.

**S3 upload 403** — pre-signed URL expired (they expire within minutes). Re-run from the start.

**sips: unsupported format** — WebP output requires macOS 10.14+. Use ImageMagick fallback above.
