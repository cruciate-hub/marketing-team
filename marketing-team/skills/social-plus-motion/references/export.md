# Export

- **MP4**: the Motion page's Export button (for reels and anything with sound).
- **Animated WebP** (web loops): `scripts/render_webp.py cut.js --font <figtree.woff2> [--mono-font <geist-mono.woff2>] --out out/ --widths 724 502 --fps 15 --grain-fps 12`. Renders in headless Chromium with a minimal stand-in kit (`stage, fx, css, h, esc, rng, clamp01, eo`); if a cut uses more of the kit, extend the harness or export MP4 and convert.
- **GIF** (email, Slack): from the MP4 via the video-to-gif-and-webp skill; 10–12 fps, ≤750px wide, under ~500 KB.

## Grain vs file size (6 s loop, 15 fps)

Boiling grain changes every pixel every frame, so animated WebP gets heavy: 1578px at 12 boils/s ≈ 11.5 MB, at 3/s ≈ 4 MB; 724px ≈ 480 KB / 300 KB. Use a static image for full-size headers and animated WebP at 724/502 for grids; for a full-size animated header use `--grain-fps 3` or a static grain layer.
