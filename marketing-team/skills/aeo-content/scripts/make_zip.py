#!/usr/bin/env python3
"""
Bundle the batch's `.docx` files into a timestamped zip.

Used in Phase D of the AEO batch workflow. By default it zips every `.docx`
file in `outputs/` and writes `outputs/aeo-batch-YYYY-MM-DD.zip`. Customize
with --out and --files.

Usage:
    python scripts/make_zip.py
    python scripts/make_zip.py --out outputs/custom-name.zip
    python scripts/make_zip.py --files outputs/a.docx outputs/b.docx

Exit codes:
    0 — zip written
    1 — no `.docx` files found (nothing to zip)
    2 — usage or I/O error
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
import zipfile
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description="Zip AEO batch .docx files")
    p.add_argument(
        "--out",
        type=Path,
        help="Output zip path (default: outputs/aeo-batch-YYYY-MM-DD.zip)",
    )
    p.add_argument(
        "--dir",
        type=Path,
        default=Path("outputs"),
        help="Directory to scan for .docx files (default: outputs/)",
    )
    p.add_argument(
        "--files",
        nargs="+",
        type=Path,
        help="Specific files to zip (overrides --dir scan)",
    )
    args = p.parse_args()

    if args.files:
        files = [f for f in args.files if f.exists()]
        missing = [str(f) for f in args.files if not f.exists()]
        if missing:
            print(f"missing files: {missing}", file=sys.stderr)
            return 2
    else:
        if not args.dir.exists():
            print(f"directory not found: {args.dir}", file=sys.stderr)
            return 2
        files = sorted(args.dir.glob("*.docx"))

    if not files:
        print("no .docx files to zip", file=sys.stderr)
        return 1

    if args.out is None:
        date = _dt.date.today().isoformat()
        args.out = args.dir / f"aeo-batch-{date}.zip"

    args.out.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, arcname=f.name)

    # Report.
    print(f"wrote {args.out}")
    for f in files:
        size_kb = f.stat().st_size / 1024
        print(f"  included {f.name} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
