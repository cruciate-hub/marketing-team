#!/usr/bin/env python3
"""
resize_images.py — resize a master image into the exact WebP sizes a Webflow collection's
image fields require. Sizes come from the collection's field map — each content-type
skill's own webflow-fields.json (schema documented in webflow-publisher/field-map-schema.md)
— never from this file.

Usage:
    python3 scripts/resize_images.py <master.png|webp> <slug> <outdir> --collection <name> \
        [--inline img1.png img2.png ...]

Outputs into <outdir>, one per `images[]` entry in the field map plus one per --inline file:
    {slug}_{variant}_{width}x{height}.webp          e.g. {slug}_page-header_1578x888.webp
    {slug}_{inline-variant}-N_{width}x{height}.webp e.g. {slug}_img-1_1578x888.webp

Why this exists:
- The CMS image fields enforce EXACT dimensions (min=max validation) — the API rejects
  anything else, so resizes must be exact.
- macOS `sips` cannot write WebP ("Can't write format: org.webmproject.webp") and ffmpeg is
  often built without libwebp. Pillow is the path that works everywhere Python does.

Dependency: Pillow. Check with `python3 -c "import PIL"`. If missing, install it in a venv
or with `python3 -m pip install --break-system-packages Pillow` (macOS's system Python
blocks plain pip installs).

Accepts PNG or WebP input (some designers ship only a `*_page-header.webp` master —
deriving the smaller sizes from it is fine). The master must be at least as wide as the
largest target and match the targets' aspect ratio (validated, so nothing is distorted).
Exits non-zero on any failure.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from webflow_fieldmap import FieldMapError, load_field_map  # noqa: E402

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required for image resizing.", file=sys.stderr)
    print('  Check:   python3 -c "import PIL"', file=sys.stderr)
    print("  Install: python3 -m pip install --break-system-packages Pillow  (or use a venv)",
          file=sys.stderr)
    sys.exit(1)


def convert(src: Path, out: Path, size: tuple) -> None:
    img = Image.open(src).convert("RGB")
    img.resize(size, Image.LANCZOS).save(out, "WEBP", quality=90)
    print(f"  ✓ {out.name}  ({size[0]}x{size[1]})", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser(description="Master image → exact WebP sizes for a collection")
    ap.add_argument("master")
    ap.add_argument("slug")
    ap.add_argument("outdir")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--collection")
    g.add_argument("--field-map")
    ap.add_argument("--inline", nargs="*", default=[])
    args = ap.parse_args()

    try:
        fm = load_field_map(args.collection or args.field_map)
    except FieldMapError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    specs = fm.get("images", [])
    inline_spec = fm.get("inline_images")
    if not specs and not (args.inline and inline_spec):
        print(f"ERROR: collection '{fm['_name']}' declares no image fields"
              + (" (and no inline_images)" if args.inline else "") + " — nothing to resize.", file=sys.stderr)
        sys.exit(1)
    if args.inline and not inline_spec:
        print(f"ERROR: collection '{fm['_name']}' declares no inline_images; drop --inline.", file=sys.stderr)
        sys.exit(1)

    master, slug, outdir = Path(args.master), args.slug, Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for p in [master] + [Path(x) for x in args.inline]:
        if not p.exists():
            print(f"ERROR: File not found: {p}", file=sys.stderr)
            sys.exit(1)

    # Validate the master: wide enough for the largest target, and the right aspect ratio
    # (resize stretches to exact target dimensions, so a mismatched source would distort).
    targets = [(s["width"], s["height"]) for s in specs] or [(inline_spec["width"], inline_spec["height"])]
    max_w = max(w for w, _ in targets)
    ratio = targets[0][0] / targets[0][1]
    with Image.open(master) as im:
        w, h = im.size
    if w < max_w:
        print(f"ERROR: master is {w}px wide — need ≥ {max_w}px. Ask for the full-resolution export.",
              file=sys.stderr)
        sys.exit(1)
    if abs(w / h - ratio) > 0.02:
        print(f"ERROR: master is {w}x{h} (ratio {w/h:.3f}) — must be ~{ratio:.3f} "
              f"({targets[0][0]}:{targets[0][1]}) or the resize will distort it.", file=sys.stderr)
        sys.exit(1)

    print(f"Master: {master.name} ({w}x{h}) → collection '{fm['_name']}'", file=sys.stderr)
    for s in specs:
        convert(master, outdir / f"{slug}_{s['variant']}_{s['width']}x{s['height']}.webp",
                (s["width"], s["height"]))

    for n, src in enumerate(args.inline, start=1):
        convert(Path(src),
                outdir / f"{slug}_{inline_spec['variant']}-{n}_{inline_spec['width']}x{inline_spec['height']}.webp",
                (inline_spec["width"], inline_spec["height"]))

    print(f"\n✓ {len(specs) + len(args.inline)} WebP files in {outdir}", file=sys.stderr)


if __name__ == "__main__":
    main()
