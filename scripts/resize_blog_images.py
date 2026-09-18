#!/usr/bin/env python3
"""
resize_blog_images.py — thin wrapper: resize a master image into the Blog collection's
exact WebP sizes via the shared scripts/resize_images.py (sizes come from
webflow-publisher/collections/blog.json, not from this file).

Usage (unchanged):
    python3 scripts/resize_blog_images.py <master.png|webp> <slug> <outdir> [--inline img1.png img2.png ...]

Outputs into <outdir>:
    {slug}_page-header_1578x888.webp
    {slug}_thumbnail_724x408.webp
    {slug}_mega-menu_502x283.webp
    {slug}_img-N_1578x888.webp        (one per --inline file, in order)

Dependency: Pillow (the shared helper checks and prints the install command if missing).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HELPER = Path(__file__).resolve().parent / "resize_images.py"

if __name__ == "__main__":
    argv = sys.argv[1:]
    if not any(a in ("--collection", "--field-map") for a in argv):
        # Insert before --inline so argparse's nargs='*' for --inline is not disturbed.
        idx = argv.index("--inline") if "--inline" in argv else len(argv)
        argv = argv[:idx] + ["--collection", "blog"] + argv[idx:]
    os.execv(sys.executable, [sys.executable, str(HELPER), *argv])
