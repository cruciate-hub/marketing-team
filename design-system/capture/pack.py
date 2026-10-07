#!/usr/bin/env python3
"""Assembles the upload pack for Claude Design from design-system/ (the parent folder) and zips it.

Copies tokens.css, tokens.json, figtree.woff2, assets/media/ (the site images the previews use), foundations/ and
sections/ (without the gallery index.html, .gitignore, proposals and generated comparison files), writes README.md
from pack-README.md, and scales every
screenshot to 1x (half of the captured 2x) and a 256-colour palette so the zip stays small. No AI calls, no network.

Run: python3 pack.py [--out /path/to/folder] [--scale 0.5]
"""
import argparse, os, shutil, sys, zipfile
from pathlib import Path
from PIL import Image

here = Path(__file__).resolve().parent
root = here.parent  # design-system/
ap = argparse.ArgumentParser()
ap.add_argument('--out', default=str(Path.home() / 'Downloads' / 'socialplus-website-design-system'))
ap.add_argument('--scale', type=float, default=0.5)
args = ap.parse_args()
out = Path(args.out)
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)

SKIP_NAMES = {'index.html', '.gitignore', 'section.generated.md', '.DS_Store', '.assemble.html'}
SKIP_DIRS = {'proposals'}


def copy_tree(src: Path, dst: Path):
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel = Path(root).relative_to(src)
        (dst / rel).mkdir(parents=True, exist_ok=True)
        for f in files:
            if f in SKIP_NAMES:
                continue
            s = Path(root) / f
            d = dst / rel / f
            if f.endswith('.png') and args.scale != 1:
                im = Image.open(s)
                w, h = im.size
                im = im.resize((max(1, round(w * args.scale)), max(1, round(h * args.scale))), Image.LANCZOS).convert('RGB')
                # 256-colour palette with dithering: about a third of the size, fine for reference screenshots
                im = im.quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
                im.save(d, optimize=True)
            else:
                shutil.copy2(s, d)


for name in ['tokens.css', 'tokens.json', 'figtree.woff2']:
    shutil.copy2(root / name, out / name)
copy_tree(root / 'assets', out / 'assets')  # assets/media: the images as served by the site's CDN, copied as-is
copy_tree(root / 'foundations', out / 'foundations')
copy_tree(root / 'sections', out / 'sections')
shutil.copy2(here / 'pack-README.md', out / 'README.md')

zip_path = out.with_suffix('.zip')
if zip_path.exists():
    zip_path.unlink()
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(out):
        for f in sorted(files):
            p = Path(root) / f
            z.write(p, p.relative_to(out.parent))

total = sum(p.stat().st_size for p in out.rglob('*') if p.is_file())
print(f'pack: {out} ({total / 1e6:.1f} MB, {sum(1 for _ in out.rglob("*") if _.is_file())} files)')
print(f'zip:  {zip_path} ({zip_path.stat().st_size / 1e6:.1f} MB)')
