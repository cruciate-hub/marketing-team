#!/usr/bin/env python3
"""Makes the committed screenshots small before they go into the (public) repo.

Every PNG under ../sections and ../foundations wider than 1440 px (desktop) or 390 px (mobile) is scaled down to
that width (the capture takes them at 2x), and every PNG is stored with a 256-colour palette. The full-size 2x
captures stay in capture/raw/ (gitignored) and can always be regenerated with capture.mjs.
Run after every capture, before committing: python3 compact-screenshots.py
No AI calls, no network.
"""
from pathlib import Path
from PIL import Image

website = Path(__file__).resolve().parent.parent
before = after = 0
for folder in ('sections', 'foundations'):
    for p in sorted((website / folder).rglob('*.png')):
        before += p.stat().st_size
        im = Image.open(p)
        target = 390 if 'mobile' in p.name else 1440
        w, h = im.size
        if im.mode == 'P' and w <= target:
            after += p.stat().st_size
            continue  # already compact
        if w > target:
            im = im.resize((target, round(h * target / w)), Image.LANCZOS)
        im = im.convert('RGB').quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
        im.save(p, optimize=True)
        after += p.stat().st_size
print(f'screenshots: {before/1e6:.1f} MB -> {after/1e6:.1f} MB')
