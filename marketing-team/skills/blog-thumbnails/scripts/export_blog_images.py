#!/usr/bin/env python3
"""Export a blog-thumbnail artboard (.dc.html from the Design canvas) to the three WebP files
the Webflow blog collection requires — exact sizes, exact names:

  {slug}_page-header_1578x888.webp   (field image-page-header)
  {slug}_thumbnail_724x408.webp      (field grid-thumbnail)
  {slug}_mega-menu_502x283.webp      (field thumbnail-mega-menu)

The CMS validates min=max on each field: any other size or format is rejected.

Usage: python3 export_blog_images.py Concept2.dc.html --slug my-post-slug \
         --fonts <dir with figtree.woff2, geist-mono.woff2> [--assets <dir of <blob id>.svg|png>] [--grain 0.9] [--glow 0.8] [--out out/]
Needs playwright (chromium) and Pillow.
"""
import argparse, asyncio, base64, os, re
from PIL import Image, ImageOps

SIZES = [('page-header', 1578, 888), ('thumbnail', 724, 408), ('mega-menu', 502, 283)]
# Grain is drawn at device pixels, so on a smaller image the same grain covers a larger share of
# every shape and reads heavier. Scale its strength down with the image: (w / 1578) ** GRAIN_FALLOFF.
GRAIN_FALLOFF = 0.75

def build_html(src, fonts, grain, glow, assets=None):
    s = open(src, encoding='utf-8').read()
    vals = {'grainOpacity': grain, 'grainFine': min(1, grain * 0.85), 'glowOpacity': glow}
    def hole(m):
        k = m.group(1).strip()
        if k not in vals: raise SystemExit(f'unknown template value {{{{{k}}}}} — add it to vals')
        return f'{vals[k]:.3f}'
    s = re.sub(r'\{\{\s*([A-Za-z_][\w.]*)\s*\}\}', hole, s)
    body = s.split('<x-dc>')[1].split('</x-dc>')[0].replace('<helmet>', '').replace('</helmet>', '')
    body = re.sub(r'@font-face\{[^}]*\}', '', body)
    # logos and other uploaded assets: /_blob/<id> -> data URI from a local folder (files named <id>.<ext>)
    mimes = {'.svg': 'image/svg+xml', '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}
    def blob(m):
        bid = m.group(1)
        if assets:
            for fn in os.listdir(assets):
                stem, ext = os.path.splitext(fn)
                if stem == bid and ext.lower() in mimes:
                    data = base64.b64encode(open(os.path.join(assets, fn), 'rb').read()).decode()
                    return f'data:{mimes[ext.lower()]};base64,{data}'
        raise SystemExit(f'asset /_blob/{bid} not found — read it from the canvas (Artifact read, path=<id>) into --assets')
    body = re.sub(r'/_blob/([0-9a-f]{32})', blob, body)
    face = ''
    for fam, fn in [('Figtree', 'figtree.woff2'), ('Geist Mono', 'geist-mono.woff2')]:
        p = os.path.join(fonts, fn)
        if os.path.exists(p):
            b64 = base64.b64encode(open(p, 'rb').read()).decode()
            face += f'@font-face{{font-family:"{fam}";src:url(data:font/woff2;base64,{b64}) format("woff2");font-weight:100 900}}'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{face}html,body{{margin:0;background:#111}}</style></head><body>{body}</body></html>'

async def shoot(jobs):
    """Render each size natively (CSS zoom), so grain and type stay crisp instead of being
    averaged away by downscaling a 1578px render."""
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for html_path, (w, h), png in jobs:
            pg = await b.new_page(viewport={'width': w, 'height': h})
            await pg.goto('file://' + os.path.abspath(html_path))
            await pg.evaluate(f'document.body.style.zoom = "{w / 1578:.6f}"')
            await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=png, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
            await pg.close()
        await b.close()

def main():
    a = argparse.ArgumentParser()
    a.add_argument('artboard'); a.add_argument('--slug', required=True); a.add_argument('--fonts', required=True)
    a.add_argument('--grain', type=float, default=0.9); a.add_argument('--glow', type=float, default=0.8)
    a.add_argument('--out', default='out'); a.add_argument('--quality', type=int, default=88)
    a.add_argument('--inline', type=int, help='export an in-blog image instead: writes {slug}_img-N_1578x888.webp only')
    a.add_argument('--assets', help='folder with uploaded assets (logos) named <blob id>.<ext>')
    a.add_argument('--grain-falloff', type=float, default=GRAIN_FALLOFF, help='0 = same grain at every size; higher = lighter grain on small sizes')
    o = a.parse_args()
    os.makedirs(o.out, exist_ok=True)
    sizes = [(f'img-{o.inline}', 1578, 888)] if o.inline else SIZES
    jobs = []
    for variant, w, h in sizes:
        g = o.grain * (w / 1578) ** o.grain_falloff
        html = os.path.join(o.out, f'_{variant}.html')
        open(html, 'w', encoding='utf-8').write(build_html(o.artboard, o.fonts, g, o.glow, o.assets))
        jobs.append((html, (w, h), os.path.join(o.out, f'_{variant}.png')))
    asyncio.run(shoot(jobs))
    for html, _, _ in jobs: os.remove(html)
    for (variant, w, h), (_, _, png) in zip(sizes, jobs):
        im = Image.open(png).convert('RGB')
        if im.size != (w, h): im = ImageOps.fit(im, (w, h), Image.LANCZOS)
        os.remove(png)
        dst = os.path.join(o.out, f'{o.slug}_{variant}_{w}x{h}.webp')
        im.save(dst, 'WEBP', quality=o.quality, method=6)
        chk = Image.open(dst); assert chk.size == (w, h) and chk.format == 'WEBP'
        print(f'{dst}  {chk.size[0]}x{chk.size[1]}  {os.path.getsize(dst)//1024} KB')

if __name__ == '__main__':
    main()
