#!/usr/bin/env python3
"""Render chosen frames of a window.CUT film and lay them out with platform safe-zone guides.

Usage: python3 contact_sheet.py cut.js --font figtree.woff2 [--mono-font geist-mono.woff2]
         --times 0.8 3.2 6.6 ... [--guides reels|none] [--out sheet.png]
The film's own width/height are used. 'reels' guides: top 250, bottom 420, right icon rail.
"""
import argparse, asyncio, os, shutil, tempfile, sys
sys.path.insert(0, os.path.dirname(__file__))
from render_webp import HTML

async def shoot(work, times):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 4096, 'height': 4096})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://' + os.path.join(work, 'index.html'))
        info = await pg.evaluate('window.ready')
        paths = []
        for t in times:
            await pg.evaluate(f'window.frame({t})')
            path = os.path.join(work, f'f_{t}.png'); paths.append(path)
            await pg.screenshot(path=path, clip={'x': 0, 'y': 0, 'width': info['W'], 'height': info['H']})
        await b.close()
    if errs: print('page errors:', errs)
    return info, paths

def main():
    a = argparse.ArgumentParser()
    a.add_argument('cut'); a.add_argument('--font', required=True); a.add_argument('--mono-font')
    a.add_argument('--times', type=float, nargs='+', required=True)
    a.add_argument('--guides', default='reels'); a.add_argument('--out', default='sheet.png')
    o = a.parse_args()
    work = tempfile.mkdtemp(prefix='sp_sheet_')
    shutil.copy(o.cut, os.path.join(work, 'cut.js')); shutil.copy(o.font, os.path.join(work, 'figtree.woff2'))
    if o.mono_font: shutil.copy(o.mono_font, os.path.join(work, 'geist-mono.woff2'))
    open(os.path.join(work, 'index.html'), 'w').write(HTML % {'gfps': 12})
    info, paths = asyncio.run(shoot(work, o.times))
    from PIL import Image, ImageDraw
    W, H = info['W'], info['H']; tw = 300; th = int(H * tw / W)
    sheet = Image.new('RGB', ((tw + 10) * len(paths), th + 30), (60, 60, 60)); d0 = ImageDraw.Draw(sheet)
    for i, (t, pth) in enumerate(zip(o.times, paths)):
        im = Image.open(pth).convert('RGB'); d = ImageDraw.Draw(im)
        if o.guides == 'reels' and H > W:
            d.rectangle([0, 250, W - 1, H - 420], outline=(255, 60, 60), width=4)
            d.rectangle([W - 120, int(H * .52), W - 1, H - 420], outline=(255, 160, 0), width=4)
        sheet.paste(im.resize((tw, th)), (i * (tw + 10), 30)); d0.text((i * (tw + 10) + 6, 8), f't={t}s', fill=(230, 230, 230))
    sheet.save(o.out); print(o.out)

if __name__ == '__main__':
    main()
