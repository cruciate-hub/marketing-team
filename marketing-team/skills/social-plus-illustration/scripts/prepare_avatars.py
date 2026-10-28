#!/usr/bin/env python3
"""Prepare avatar photos from the Untitled UI avatars library for social.plus illustrations.

Input: PNG screenshots of `_Avatar image` instances from the library's neutral-grey rows
(320x380: photo on top, name and credit underneath), one file per person, e.g. avatars_raw/ava.png.
Output: avatars/<name>.jpg, 320x320 — the person cut out of the grey background and graded
dark, cool and slightly desaturated onto a dark ground — plus avatars_sheet.png for a visual check.

Usage: python3 prepare_avatars.py avatars_raw/ avatars/ [--hair-fix name1,name2] [--model birefnet-portrait]
Needs: pip install rembg pillow numpy scipy  (rembg downloads the u2net_human_seg model on first run)
See references/avatar-library.md.
"""
import argparse, os
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from scipy.ndimage import binary_fill_holes

S = 320               # photo is the top 320x320 of the 320x380 instance
BG = 224.0            # the library's neutral grey background (#E0E0E0)
GRADE = dict(saturation=0.62, brightness=0.84, contrast=1.06, cool=(70, 90, 150), cool_mix=0.07)

def ground():
    """#1A1A1A with a soft #343437 lift at the upper left."""
    g = Image.new('RGB', (S, S), (26, 26, 26))
    m = Image.new('L', (S, S), 0)
    ImageDraw.Draw(m).ellipse((-60, -80, 300, 260), fill=255)
    g.paste(Image.new('RGB', (S, S), (52, 52, 55)), (0, 0), m.filter(ImageFilter.GaussianBlur(70)))
    return g

def to_l(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8'))

def to_f(im):
    return np.asarray(im).astype(float) / 255

def prepare(src, session, hair_fix):
    from rembg import remove
    im = Image.open(src).convert('RGB')
    if im.size != (S, 380) and im.size != (S, S):
        im = im.resize((S, round(im.height * S / im.width)), Image.LANCZOS)
    im = im.crop((0, 0, S, S))
    a = to_f(remove(im, session=session, post_process_mask=False).getchannel('A'))
    # close holes inside the person (skin highlights read as background)
    a = np.where(binary_fill_holes(a > 0.5) & (a < 0.5), 1.0, a)
    px = np.asarray(im).astype(float)
    dist = np.sqrt(((px - BG) ** 2).sum(-1))
    sat = px.max(-1) - px.min(-1)
    if hair_fix:
        # grey showing through curls: near the outline, upper part of the photo only
        yy = np.arange(S)[:, None] * np.ones((1, S))
        upper = np.clip((230 - yy) / 40, 0, 1)
        band = to_f(to_l(a < 0.5).filter(ImageFilter.MaxFilter(25)))
        a = a * (1 - np.clip(1 - (dist - 6) / 22, 0, 1) * (sat < 14) * band * upper)
    # light fringe along the outline
    edge = to_f(to_l(a < 0.5).filter(ImageFilter.MaxFilter(5)))
    a = a * (1 - np.clip(1 - (dist - 10) / 45, 0, 1) * (sat < 16) * edge)
    alpha = to_l(a).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    rgb = ImageEnhance.Color(im).enhance(GRADE['saturation'])
    rgb = ImageEnhance.Brightness(rgb).enhance(GRADE['brightness'])
    rgb = ImageEnhance.Contrast(rgb).enhance(GRADE['contrast'])
    rgb = Image.blend(rgb, Image.new('RGB', (S, S), GRADE['cool']), GRADE['cool_mix'])
    out = ground()
    out.paste(rgb, (0, 0), alpha)
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument('src_dir'); p.add_argument('out_dir')
    p.add_argument('--hair-fix', default='', help='comma-separated names (file stems) with curly or loose hair')
    p.add_argument('--model', default='u2net_human_seg', help='rembg model; birefnet-portrait for hair the default leaves grey in (about 14 GB of memory)')
    o = p.parse_args()
    from rembg import new_session
    session = new_session(o.model)
    hair = {n.strip() for n in o.hair_fix.split(',') if n.strip()}
    os.makedirs(o.out_dir, exist_ok=True)
    names = sorted(os.path.splitext(f)[0] for f in os.listdir(o.src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')))
    files = {os.path.splitext(f)[0]: f for f in os.listdir(o.src_dir)}
    done = []
    for n in names:
        out = prepare(os.path.join(o.src_dir, files[n]), session, n in hair)
        dst = os.path.join(o.out_dir, f'{n}.jpg')
        out.save(dst, quality=90)
        done.append((n, out)); print(dst)
    if done:
        cols = min(4, len(done)); rows = (len(done) + cols - 1) // cols
        sheet = Image.new('RGB', (10 + cols * (S + 10), 10 + rows * (S + 10)), (17, 17, 17))
        for i, (_, im) in enumerate(done):
            sheet.paste(im, (10 + (i % cols) * (S + 10), 10 + (i // cols) * (S + 10)))
        sheet.save(os.path.join(o.out_dir, 'avatars_sheet.png'))
        print(os.path.join(o.out_dir, 'avatars_sheet.png'))

if __name__ == '__main__':
    main()
