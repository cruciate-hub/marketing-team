#!/usr/bin/env python3
"""Render a social.plus thumbnail motion cut (window.CUT) to animated WebP.

Usage:
  python3 render_webp.py cut.js --font figtree.woff2 [--mono-font geist-mono.woff2] --out out/ [--widths 1578 724 502]
                         [--fps 15] [--grain-fps 12] [--quality 72] [--name header]

Needs: playwright (python) with Chromium, ffmpeg with libwebp_anim.
The harness is a minimal stand-in for the Motion player's kit: stage, fx, css, h, esc, rng, clamp01, eo.
"""
import argparse, asyncio, os, shutil, subprocess, tempfile

HTML = """<!doctype html><html><head><meta charset="utf-8">
<style>@font-face{font-family:figtree;src:url(figtree.woff2) format("woff2");font-weight:300 900}
@font-face{font-family:"geist-mono";src:url(geist-mono.woff2) format("woff2");font-weight:100 900}
html,body{margin:0;background:#111}
#stage{position:absolute;left:0;top:0;overflow:hidden}
#fx{position:absolute;left:0;top:0;z-index:99}</style></head>
<body><div id="stage"></div><canvas id="fx"></canvas>
<script>
window.GRAIN_FPS=%(gfps)d;
function mulberry(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const stage=document.getElementById('stage');const cv=document.getElementById('fx');const fx=cv.getContext('2d');
window.kit={stage,fx,
 css(t){const s=document.createElement('style');s.textContent=t;stage.appendChild(s)},
 h(html){const d=document.createElement('div');d.innerHTML=html.trim();return d.firstElementChild},
 esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))},
 rng(seed){return mulberry(seed*2654435761)},clamp01:x=>Math.max(0,Math.min(1,x)),eo:x=>1-Math.pow(1-x,3)};
</script><script src="cut.js"></script>
<script>
window.ready=(async()=>{const W=CUT.width,H=CUT.height;kit.W=W;kit.H=H;
 stage.style.width=W+'px';stage.style.height=H+'px';cv.width=W;cv.height=H;
 await document.fonts.load('600 52px figtree');await document.fonts.load('500 24px figtree');
 await CUT.init(kit);return {W,H,D:CUT.duration}})();
window.frame=t=>{fx.clearRect(0,0,CUT.width,CUT.height);CUT.render(t,kit)};
</script></body></html>"""

async def shoot(work, fps):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 4096, 'height': 4096})
        await pg.goto('file://' + os.path.join(work, 'index.html'))
        info = await pg.evaluate('window.ready')
        W, H, D = info['W'], info['H'], info['D']
        n = round(D * fps)
        os.makedirs(os.path.join(work, 'frames'), exist_ok=True)
        for i in range(n):
            await pg.evaluate(f'window.frame({i / fps})')
            await pg.screenshot(path=os.path.join(work, 'frames', f'f_{i:04d}.png'),
                                clip={'x': 0, 'y': 0, 'width': W, 'height': H})
        await b.close()
    return W, n

def main():
    a = argparse.ArgumentParser()
    a.add_argument('cut'); a.add_argument('--font', required=True); a.add_argument('--mono-font', default=None); a.add_argument('--out', default='out')
    a.add_argument('--widths', type=int, nargs='+', default=[1578, 724, 502])
    a.add_argument('--fps', type=int, default=15); a.add_argument('--grain-fps', type=int, default=12)
    a.add_argument('--quality', type=int, default=72); a.add_argument('--name', default='thumbnail')
    o = a.parse_args()
    work = tempfile.mkdtemp(prefix='sp_thumb_')
    shutil.copy(o.cut, os.path.join(work, 'cut.js'))
    shutil.copy(o.font, os.path.join(work, 'figtree.woff2'))
    if o.mono_font: shutil.copy(o.mono_font, os.path.join(work, 'geist-mono.woff2'))
    open(os.path.join(work, 'index.html'), 'w').write(HTML % {'gfps': o.grain_fps})
    W, n = asyncio.run(shoot(work, o.fps))
    os.makedirs(o.out, exist_ok=True)
    for w in o.widths:
        dst = os.path.join(o.out, f'{o.name}-{w}.webp')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(o.fps),
                        '-i', os.path.join(work, 'frames', 'f_%04d.png'),
                        '-vf', f'scale={w}:-2:flags=lanczos', '-c:v', 'libwebp_anim', '-lossless', '0',
                        '-q:v', str(o.quality), '-compression_level', '6', '-loop', '0', dst], check=True)
        print(f'{dst}  {os.path.getsize(dst) / 1024:.0f} KB')
    print(f'frames: {n} in {work}/frames (first frame = still preview)')

if __name__ == '__main__':
    main()
