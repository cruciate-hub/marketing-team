# Image Pipeline — Resize + Upload

## Resize with sips (macOS built-in)

`sips` is available on every Mac without installing anything.
Syntax: `sips -z <height> <width> <input> --out <output>`

Given a master PNG at `$PNG` and article slug at `$SLUG`:

```bash
# Validate the input first
WIDTH=$(sips -g pixelWidth "$PNG" | awk '/pixelWidth/ {print $2}')
HEIGHT=$(sips -g pixelHeight "$PNG" | awk '/pixelHeight/ {print $2}')
echo "Input: ${WIDTH}×${HEIGHT}"

# Must be at least 1578 px wide. If not, stop and ask for a higher-res PNG.

# Resize to 3 sizes
TMPDIR=$(mktemp -d)
sips -z 888 1578 "$PNG" --out "$TMPDIR/${SLUG}-header.png"   # 1578×888  Page Header
sips -z 408  724 "$PNG" --out "$TMPDIR/${SLUG}-grid.png"     #  724×408  Grid Thumbnail
sips -z 283  502 "$PNG" --out "$TMPDIR/${SLUG}-menu.png"     #  502×283  Mega Menu

echo "Header:  $TMPDIR/${SLUG}-header.png"
echo "Grid:    $TMPDIR/${SLUG}-grid.png"
echo "Menu:    $TMPDIR/${SLUG}-menu.png"
```

Note: `sips -z` scales and crops to the exact dimensions. If the input PNG is not
16:9 (1.775 ratio), the result will be letterboxed or cropped. All images provided
by the designer should already be 16:9 — verify with:

```bash
python3 -c "w,h=$WIDTH,$HEIGHT; print('16:9' if abs(w/h - 16/9) < 0.01 else f'NOT 16:9 — ratio is {w/h:.3f}')"
```

## Upload to Webflow (via blog-publisher.py)

The Python script at `scripts/blog-publisher.py` handles the full 3-step upload:
1. MD5 hash of file binary
2. `POST /v2/sites/{siteId}/assets` → S3 pre-signed URL
3. POST file to S3 → asset goes live
4. `GET /v2/sites/{siteId}/assets/{id}` → retrieve `hostedUrl`

The script takes all 3 image paths as positional arguments alongside the fielddata JSON.
See `scripts/blog-publisher.py --help` (usage printed to stderr on wrong arg count).

## Troubleshooting

**"Input PNG too small"** — The master PNG must be ≥ 1578 px wide. Ask the designer
for the full-resolution export (not a screenshot or preview export).

**S3 upload 403** — The pre-signed URL has expired (they expire within minutes).
Re-run the full pipeline from the beginning to get a fresh URL.

**S3 upload 400 "InvalidArgument"** — The MD5 hash mismatch or the file was modified
after hashing. Re-run from the beginning.

**sips not found** — Only on macOS. If running on Linux, use ImageMagick instead:
```bash
convert "$PNG" -resize 1578x888^ -gravity Center -extent 1578x888 "${SLUG}-header.png"
convert "$PNG" -resize 724x408^  -gravity Center -extent 724x408  "${SLUG}-grid.png"
convert "$PNG" -resize 502x283^  -gravity Center -extent 502x283  "${SLUG}-menu.png"
```
