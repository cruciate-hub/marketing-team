#!/usr/bin/env python3
"""Render stills of a built showcase film locally, to check it before it goes into the Motion film.

Usage: python3 preview.py OUT_DIR [scene:t,t,...] ...      (times in seconds within the scene)
       python3 preview.py OUT_DIR --key                        (the moments worth looking at)
Writes OUT_DIR/review/still_<scene>_<t>.png and a contact sheet OUT_DIR/review/stills.png.
Runs the film's own modules in Chromium with a small stand-in for the Motion kit (the player itself
is not needed). Needs Playwright (Chromium) and Pillow.
"""
import asyncio, glob, json, os, sys
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw

SHIM = r"""
window.__scenes = {};
function makeKit(start, dur) {
  const clamp01 = (x) => Math.max(0, Math.min(1, x));
  const kit = {
    start, dur, W: window.__W, H: window.__H, stage: document.getElementById('stage'),
    clamp01, seg: (t, a, b) => clamp01((t - a) / (b - a)), lerp: (a, b, p) => a + (b - a) * p,
    eo: (x) => 1 - Math.pow(1 - x, 3), ei: (x) => x * x * x,
    eio: (x) => x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
    eox: (x) => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x),
    eob: (x, o = 1.4) => 1 + (o + 1) * Math.pow(x - 1, 3) + o * Math.pow(x - 1, 2),
    breathe: (t, amt = 0.012, period = 3.2) => 1 + amt * Math.sin(2 * Math.PI * t / period),
    h: (html) => { const tp = document.createElement('template'); tp.innerHTML = html.trim(); return tp.content.firstElementChild; },
    video: (name, o = {}) => { const v = document.createElement('video'); v.muted = true; v.preload = 'auto';
      v.src = 'assets/' + name; v.dataset.start = start + (o.start || 0); return v; },
    seek: (v, s) => { v.dataset.seek = s; },
    module: (n) => window.__mods[n], json: (n) => JSON.parse(window.__mods[n]),
    assets: { url: (n) => 'assets/' + n },
    scene: (id, def) => { window.__scenes[id] = def; },
    score: () => {},
    TextFx: { fadeFromRight: (el, t, t0, o = {}) => {
      if (!el.__w) { const ws = el.textContent.split(' '); el.textContent = ''; el.__w = ws.map((w, i) => {
        const s = document.createElement('span'); s.style.display = 'inline-block'; s.textContent = w; el.append(s); if (i < ws.length - 1) el.append(' '); return s; }); }
      const st = o.stagger || 0.11, d = o.dur || 0.5, dx = o.dx || 26;
      el.__w.forEach((s, i) => { const p = clamp01((t - t0 - i * st) / d), e = 1 - Math.pow(1 - p, 3); s.style.opacity = e; s.style.transform = 'translateX(' + (1 - e) * dx + 'px)'; });
    } },
  };
  return kit;
}
"""


async def main():
    out = sys.argv[1]
    mods = {os.path.basename(p)[:-5]: json.load(open(p))['text'] for p in glob.glob(f'{out}/film/docs/modules/*.json')}
    sc = json.loads(mods['scenes.json'])
    starts, acc = {}, 0.0
    for s in sc['scenes']:
        starts[s['id']] = (acc, s['dur']); acc += s['dur']
    jobs = []
    if sys.argv[2:] == ['--key']:
        cfg = json.loads(mods['showcase.json'])
        jobs += [('intro', 0.0), ('intro', 1.6), ('intro', 3.6)]
        for f in cfg['features']:
            d = starts[f['id']][1]
            jobs += [(f['id'], 0.2), (f['id'], 1.0), (f['id'], round(f['focus']['t'] + 0.7, 2)), (f['id'], round(d - 0.05, 2))]
        jobs += [('lockup', 0.5), ('lockup', 2.0)]
        if 'quote' in starts:
            jobs += [('quote', 3.5)]
    else:
        for a in sys.argv[2:]:
            s, ts = a.split(':'); jobs += [(s, float(x)) for x in ts.split(',')]
    os.makedirs(f'{out}/review', exist_ok=True)
    css = mods['base.css']
    sj = json.loads(mods['scenes.json']); SW, SH = sj.get('width', 1080), sj.get('height', 1920)
    tw, th = (270, 480) if SH > SW else (480, 270)
    page = f"""<!doctype html><html><head><style>
@font-face {{ font-family:'Figtree-500'; src:url(assets/Figtree-500.woff2); }}
@font-face {{ font-family:'Figtree-700'; src:url(assets/Figtree-700.woff2); }}
html,body{{margin:0;background:#000}} #stage{{position:absolute;left:0;top:0;width:{SW}px;height:{SH}px;overflow:hidden;background:#111}}
{css}</style></head><body><div id="stage"></div><script>window.__W={SW};window.__H={SH};{SHIM}; window.__mods = {json.dumps(mods)};</script></body></html>"""
    open(f'{out}/preview.html', 'w').write(page)
    shots = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': SW, 'height': SH})
        pg.on('pageerror', lambda e: print('PAGE ERROR:', e))
        pg.on('console', lambda m: m.type in ('error', 'warning') and print('console:', m.text))
        await pg.goto('file://' + os.path.abspath(f'{out}/preview.html'))
        await pg.evaluate("Promise.all([document.fonts.load('96px Figtree-700'), document.fonts.load('42px Figtree-500')])")
        for sid, t in jobs:
            st, du = starts[sid]
            mod = 'scene-' + sid + '.js'
            await pg.evaluate("""async ([shared, code, sid, st, du, t]) => {
              const stage = document.getElementById('stage'); stage.innerHTML = ''; window.SP = undefined;
              const kit = makeKit(st, du);
              new Function('kit', shared)(kit); new Function('kit', code)(kit);
              const s = window.__scenes[sid]; await s.init.call(s, kit); s.render.call(s, t, kit);
              const vids = [...stage.querySelectorAll('video')];
              await Promise.all(vids.map(v => new Promise(res => {
                const go = () => { const lt = v.dataset.seek !== undefined ? +v.dataset.seek : (st + t) - (+v.dataset.start);
                  v.addEventListener('seeked', res, { once: true }); v.currentTime = Math.max(0, Math.min(v.duration - 0.001, lt)) + 0.0005; };
                if (v.readyState >= 1) go(); else v.addEventListener('loadedmetadata', go, { once: true });
                v.addEventListener('error', res, { once: true }); })));
              await Promise.all([...stage.querySelectorAll('img')].map(i => i.decode().catch(() => {})));
            }""", [mods['shared.js'], mods[mod], sid, st, du, t])
            await pg.wait_for_timeout(80)
            f = f'{out}/review/still_{sid}_{t:05.2f}.png'
            await pg.screenshot(path=f); shots.append((f, f'{sid} {t:.2f}s'))
        await b.close()
    cols = min(6, len(shots)); rows = (len(shots) + cols - 1) // cols
    cols = min(6 if SH > SW else 4, len(shots)); rows = (len(shots) + cols - 1) // cols
    W = Image.new('RGB', (cols * (tw + 10), rows * (th + 40)), (40, 40, 40)); d = ImageDraw.Draw(W)
    for i, (f, lab) in enumerate(shots):
        x, y = (i % cols) * (tw + 10), (i // cols) * (th + 40)
        W.paste(Image.open(f).resize((tw, th)), (x + 5, y + 30)); d.text((x + 8, y + 8), lab, fill=(255, 220, 0))
    W.save(f'{out}/review/stills.png')
    print(f'{out}/review/stills.png', len(shots), 'stills')


if __name__ == '__main__':
    asyncio.run(main())
