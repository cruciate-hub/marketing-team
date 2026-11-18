#!/usr/bin/env python3
"""Turn app screenshots into tap-through clips, for a customer who sends screenshots instead of recordings.

Usage: python3 screens_to_clips.py screens.json OUT_DIR

screens.json:
  {"src": "zip",                                  # folder with the screenshots (relative to screens.json)
   "clips": {
     "feed": [                                     # one clip per feature -> OUT_DIR/feed.mp4
       {"img": "home.png", "hold": 1.7, "tap": [168, 1190]},
       {"img": "feed.png", "in": "fade", "dur": 0.25, "hold": 1.7, "tap": [200, 465]},
       {"img": "post.png", "in": "push", "dur": 0.45, "hold": 3.1}
     ]}}

Each step holds one screenshot for `hold` seconds. From the second step on, `in` is how it arrives
(over `dur` seconds), like in-app navigation:
  fade    a cross-fade (a tab or a state change on the same screen)
  push    slides in from the right (opening a post, a group, a profile)
  scroll  the page scrolls up by `shift` px; `pin` px at the top (the app bar) stay put
  vslide  the content below `pin` slides up as one (a long page continuing)
`tap: [x, y]` shows a soft tap dot for the last 0.4 s of the hold, where the person taps to go on.
Coordinates are in clip pixels (585 x 1266): run once, read OUT_DIR/screens/grid_<name>.png and place them.

Screenshots are fitted to the phone without cropping the UI: scaled to 585 px wide, and a shorter
screen is padded at the top with its own top-row colour (it reads as the status bar). The clips are
then ready for prep_clips.py (set each feature's "src" to OUT_DIR/<name>.mp4).
Needs Pillow and ffmpeg.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw

FPS, W, H = 30, 585, 1266


def eio(x):
    x = min(1, max(0, x))
    return 4 * x * x * x if x < .5 else 1 - (-2 * x + 2) ** 3 / 2


def fit(path):
    im = Image.open(path).convert('RGB')
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    if im.height > H:  # taller than the phone: fit the height, pad the sides
        im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
        out = Image.new('RGB', (W, H), im.getpixel((0, H // 2)))
        out.paste(im, ((W - im.width) // 2, 0))
        return out
    out = Image.new('RGB', (W, H), im.getpixel((W // 2, 2)))
    out.paste(im, (0, H - im.height))
    return out


def grid(im, path):
    g = im.copy(); d = ImageDraw.Draw(g)
    for y in range(0, H, 50):
        d.line([(0, y), (W, y)], fill=(255, 0, 255) if y % 100 == 0 else (0, 200, 255)); d.text((2, y + 1), str(y), fill=(255, 0, 0))
    for x in range(0, W, 50):
        d.line([(x, 0), (x, H)], fill=(255, 0, 255) if x % 100 == 0 else (0, 200, 255)); d.text((x + 1, 2), str(x), fill=(255, 0, 0))
    g.save(path)


def dot(fr, xy, a, s):
    if a <= 0:
        return fr
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); r = 22 * s; x, y = xy
    d.ellipse([x - r, y - r, x + r, y + r], fill=(110, 110, 110, int(110 * a)), outline=(255, 255, 255, int(150 * a)), width=2)
    return Image.alpha_composite(fr.convert('RGBA'), ov).convert('RGB')


def frame(IA, IB, s, e):
    m = s['in']
    if m == 'fade':
        return Image.blend(IA, IB, e)
    if m == 'push':
        fr = Image.new('RGB', (W, H)); dx = int(W * e); fr.paste(IA, (-dx, 0)); fr.paste(IB, (W - dx, 0)); return fr
    if m == 'scroll':
        sh, pin = s['shift'], s.get('pin', 0); o = int(sh * e)
        strip = Image.new('RGB', (W, H + sh)); strip.paste(IA, (0, 0)); strip.paste(IB.crop((0, H - sh, W, H)), (0, H))
        fr = strip.crop((0, o, W, o + H))
        if pin:
            fr.paste(Image.blend(fr.crop((0, 0, W, pin)), IB.crop((0, 0, W, pin)), min(1, max(0, (e - .35) / .4))), (0, 0))
        return IB.copy() if e >= 1 else fr
    if m == 'vslide':
        pin = s['pin']; o = int((H - pin) * e); fr = Image.new('RGB', (W, H))
        fr.paste(IA.crop((0, pin, W, H)), (0, pin - o)); fr.paste(IB.crop((0, pin, W, H)), (0, H - o))
        fr.paste(Image.blend(IA.crop((0, 0, W, pin)), IB.crop((0, 0, W, pin)), e), (0, 0))
        return fr
    sys.exit(f'screens_to_clips: unknown transition "{m}"')


def render(name, steps, ims, out):
    segs, t = [], 0.0
    for i, s in enumerate(steps):
        if i:
            segs.append(('tr', t, t + s['dur'], steps[i - 1], s)); t += s['dur']
        segs.append(('hold', t, t + s['hold'], s, None)); t += s['hold']
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-vf', 'scale=584:1264', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', f'{out}/{name}.mp4'],
                         stdin=subprocess.PIPE)
    for f in range(round(t * FPS)):
        tt = f / FPS
        kind, a, b, A, B = next((sg for sg in segs if sg[1] <= tt < sg[2]), segs[-1])
        if kind == 'hold':
            fr = ims[A['img']].copy()
            if A.get('tap'):
                q = tt - (b - 0.4)
                al = 0 if q < 0 else (min(1, q / 0.08) if q < 0.3 else max(0, 1 - (q - 0.3) / 0.15))
                fr = dot(fr, A['tap'], al, 0.85 + 0.15 * min(1, max(0, q / 0.1)))
        else:
            fr = frame(ims[A['img']], ims[B['img']], B, eio((tt - a) / (b - a)))
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    print(f'{out}/{name}.mp4', round(t, 2), 's')


def main():
    cfg_path, out = sys.argv[1], sys.argv[2]
    cfg = json.load(open(cfg_path))
    src = os.path.join(os.path.dirname(os.path.abspath(cfg_path)), cfg.get('src', '.'))
    os.makedirs(f'{out}/screens', exist_ok=True)
    ims = {}
    for steps in cfg['clips'].values():
        for s in steps:
            if s['img'] not in ims:
                ims[s['img']] = fit(os.path.join(src, s['img']))
                base = os.path.splitext(s['img'])[0]
                ims[s['img']].save(f'{out}/screens/{base}.png'); grid(ims[s['img']], f'{out}/screens/grid_{base}.png')
    for name, steps in cfg['clips'].items():
        render(name, steps, ims, out)


if __name__ == '__main__':
    main()
