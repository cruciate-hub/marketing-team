#!/usr/bin/env python3
"""
resize_blog_images.py — Resize a master image into the exact WebP sizes the
social.plus Blog collection requires.

Usage:
    python3 scripts/resize_blog_images.py <master.png|webp> <slug> <outdir> [--inline img1 img2 ...]

Outputs into <outdir>:
    {slug}_page-header_1578x888.webp
    {slug}_thumbnail_724x408.webp
    {slug}_mega-menu_502x283.webp
    {slug}_img-N_1578x888.webp        (one per --inline file, in order)

Why this exists:
- The Blog collection's image fields enforce EXACT dimensions (min=max validation:
  1578x888 / 724x408 / 502x283) — the API rejects anything else, so resizes must be exact.
- macOS `sips` cannot write WebP ("Can't write format: org.webmproject.webp") and ffmpeg
  is often built without libwebp. Pillow is the path that works everywhere Python does.

Dependency: Pillow. Check with `python3 -c "import PIL"`. If missing, install it in a
venv or with `python3 -m pip install --break-system-packages Pillow` (macOS's system
Python blocks plain pip installs).

Accepts PNG or WebP input (some designers ship only a `*_page-header.webp` master —
deriving the smaller sizes from it is fine). Input must be ≥ 1578 px wide and ~16:9;
both are validated. Exits non-zero on any failure.
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required for image resizing.", file=sys.stderr)
    print('  Check:   python3 -c "import PIL"', file=sys.stderr)
    print("  Install: python3 -m pip install --break-system-packages Pillow  (or use a venv)",
          file=sys.stderr)
    sys.exit(1)

HERO_SIZES = [(1578, 888, "page-header"), (724, 408, "thumbnail"), (502, 283, "mega-menu")]
INLINE_SIZE = (1578, 888)


def convert(src: Path, out: Path, size: tuple) -> None:
    img = Image.open(src).convert("RGB")
    img.resize(size, Image.LANCZOS).save(out, "WEBP", quality=90)
    print(f"  ✓ {out.name}  ({size[0]}x{size[1]})", file=sys.stderr)


def main() -> None:
    args = sys.argv[1:]
    if "--inline" in args:
        i = args.index("--inline")
        positional, inline = args[:i], args[i + 1:]
    else:
        positional, inline = args, []
    if len(positional) != 3:
        print("Usage: python3 resize_blog_images.py <master> <slug> <outdir> [--inline img1 ...]",
              file=sys.stderr)
        sys.exit(1)

    master, slug, outdir = Path(positional[0]), positional[1], Path(positional[2])
    outdir.mkdir(parents=True, exist_ok=True)

    for p in [master] + [Path(x) for x in inline]:
        if not p.exists():
            print(f"ERROR: File not found: {p}", file=sys.stderr)
            sys.exit(1)

    # Validate the master: wide enough, and ~16:9 (resize stretches to exact target
    # dimensions, so a non-16:9 source would come out visibly distorted).
    with Image.open(master) as im:
        w, h = im.size
    if w < 1578:
        print(f"ERROR: master is {w}px wide — need ≥ 1578px. Ask for the full-resolution export.",
              file=sys.stderr)
        sys.exit(1)
    if abs(w / h - 16 / 9) > 0.02:
        print(f"ERROR: master is {w}x{h} (ratio {w/h:.3f}) — must be ~16:9 ({16/9:.3f}) or the "
              f"resize will distort it.", file=sys.stderr)
        sys.exit(1)

    print(f"Master: {master.name} ({w}x{h})", file=sys.stderr)
    for tw, th, variant in HERO_SIZES:
        convert(master, outdir / f"{slug}_{variant}_{tw}x{th}.webp", (tw, th))

    for n, src in enumerate(inline, start=1):
        convert(Path(src), outdir / f"{slug}_img-{n}_{INLINE_SIZE[0]}x{INLINE_SIZE[1]}.webp",
                INLINE_SIZE)

    print(f"\n✓ {3 + len(inline)} WebP files in {outdir}", file=sys.stderr)


if __name__ == "__main__":
    main()
