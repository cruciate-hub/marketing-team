#!/usr/bin/env python3
"""Build a customer showcase film's store documents from showcase.json and the template.

Usage: MT_REPO=<clone> python3 build_film.py showcase.json OUT_DIR
(OUT_DIR = the folder prep_clips.py wrote; run prep first.)

Writes:
  OUT_DIR/assets/  Figtree-500.woff2, Figtree-700.woff2, icon.webp (+ prep's clips and stills)
  OUT_DIR/film/docs/<collection>/<doc_id>.json   one store document each
  OUT_DIR/film/batch.json    the ArtifactData batch: film/meta first, modules, film/script last
  OUT_DIR/film/uploads.json  the asset files to upload: name, local path, mime, w, h
Needs Pillow and fontTools (+ brotli); Playwright only for an SVG app icon.
"""
import io, json, os, re, sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, '..', 'template')
SP_LOGO = 'design-system/assets/media/66fe6169153dc88a03557da6_29a5aaff9e31043f2175762ac854a9e5_logo.svg'
FIGTREE = 'design-system/figtree.woff2'
INTRO, LOCKUP, LOCKUP_END = 4.2, 3.3, 4.5
LOOK = ("social.plus customer showcase (customer-showcase-video skill): dark social.plus ground with one soft blue glow, "
        "a still, front-on phone playing the customer's real app recordings, Figtree labels above the phone as one "
        "vertically centred block, an app-launch from the customer's app icon into the phone, in-app slides between "
        "features, one highlight per feature (the screen dims except the part that matters; the UI is never cropped "
        "or zoomed), the official social.plus logo x the customer's wordmark side by side, optional approved quote.")


def die(msg):
    sys.exit('build_film: ' + msg)


def tpl(name):
    return open(os.path.join(TPL, name), encoding='utf-8').read()


def prefix_ids(svg, p):
    ids = re.findall(r'\bid="([^"]+)"', svg)
    for i in sorted(set(ids), key=len, reverse=True):
        svg = svg.replace(f'id="{i}"', f'id="{p}{i}"').replace(f'url(#{i})', f'url(#{p}{i})').replace(f'href="#{i}"', f'href="#{p}{i}"')
    return svg


def clean_svg(svg):
    svg = svg[svg.index('<svg'):]
    svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S)
    svg = re.sub(r'>\s+<', '><', svg).strip()
    return svg


def svg_aspect(svg):
    m = re.search(r'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', svg)
    if m:
        return float(m.group(1)) / float(m.group(2))
    w, h = re.search(r'\bwidth="([\d.]+)', svg), re.search(r'\bheight="([\d.]+)', svg)
    if w and h:
        return float(w.group(1)) / float(h.group(1))
    die('the wordmark SVG has no viewBox or width/height')


def static_figtree(repo, out):
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    from fontTools import subset
    for wght in (500, 700):
        f = TTFont(os.path.join(repo, FIGTREE))
        inst = instancer.instantiateVariableFont(f, {'wght': wght})
        opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = ['*']
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=list(range(0x20, 0x7F)) + [0xA0, 0xA9, 0xAE, 0xD7, 0x2013, 0x2014, 0x2018, 0x2019,
                                                          0x201C, 0x201D, 0x2022, 0x2026, 0x20AC, 0x2122]
                     + list(range(0xC0, 0x100)))
        sub.subset(inst)
        inst.flavor = 'woff2'
        inst.save(os.path.join(out, f'Figtree-{wght}.woff2'))


def icon_webp(src, dst):
    if src.lower().endswith('.svg'):
        from playwright.sync_api import sync_playwright
        svg = open(src, encoding='utf-8').read()
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1024, 'height': 1024})
            pg.set_content('<style>html,body{margin:0}svg{width:1024px;height:1024px;display:block}</style>' + clean_svg(svg))
            png = pg.screenshot(); b.close()
        im = Image.open(io.BytesIO(png))
    else:
        im = Image.open(src)
    im = im.convert('RGB')
    if abs(im.width - im.height) > 2:
        die('the app icon must be square (the App Store / Play Store icon, 1024 x 1024)')
    im.resize((600, 600), Image.LANCZOS).save(dst, quality=92)


def main():
    cfg_path, out = sys.argv[1], sys.argv[2]
    repo = os.environ.get('MT_REPO', '/tmp/cruciate-hub-marketing-team')
    base = os.path.dirname(os.path.abspath(cfg_path))
    rel = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    cfg = json.load(open(cfg_path))
    feats = cfg.get('features', [])
    if not 2 <= len(feats) <= 5:
        die('a showcase has 2 to 5 features')
    for f in feats:
        for k in ('id', 'title', 'line', 'clip', 'dur'):
            if k not in f:
                die(f'feature {f.get("id")} has no "{k}" (run prep_clips.py first)')
        if not re.fullmatch(r'f[1-9]', f['id']):
            die('feature ids are f1, f2, ...')
        fo = f.get('focus') or {}
        if 't' not in fo or len(fo.get('rect', [])) != 5:
            die(f'feature {f["id"]} needs focus.t and focus.rect [x, y, w, h, radius] in clip pixels')
    assets = f'{out}/assets'
    os.makedirs(assets, exist_ok=True)

    # brand files: Figtree statics and the official social.plus logo, both from the design system
    static_figtree(repo, assets)
    sp = clean_svg(open(os.path.join(repo, SP_LOGO), encoding='utf-8').read())
    sp = re.sub(r'\s(id|data-name)="Layer_1"', '', sp).replace(' data-name="Layer 1"', '')
    sp = prefix_ids(sp.replace(' xmlns:xlink="http://www.w3.org/1999/xlink"', ''), 'spl-')
    sp = sp.replace('<svg ', '<svg style="display:block;width:100%;height:100%" ', 1)

    # customer files
    icon_webp(rel(cfg['iconSrc']), f'{assets}/icon.webp')
    wm = prefix_ids(clean_svg(open(rel(cfg['wordmarkSrc']), encoding='utf-8').read()), 'cwm-')
    asp = svg_aspect(wm)
    lk = dict(cfg.get('lockup') or {})
    h = float(lk.get('wordmarkH', 48))
    w = h * asp
    if w > 320:
        w, h = 320.0, 320.0 / asp
    lockup = {'wordmarkW': round(w, 2), 'wordmarkH': round(h, 2), 'wordmarkDy': float(lk.get('wordmarkDy', 0))}

    quote = cfg.get('quote')
    if quote and (not quote.get('text') or not quote.get('who')):
        die('quote needs "text" and "who" (name, title, company), and must be approved')
    aspect = cfg.get('aspect', '9:16')
    if aspect not in ('9:16', '16:9'):
        die('aspect is "9:16" (default) or "16:9"')
    wide = aspect == '16:9'
    runtime = {
        'aspect': aspect, 'customer': cfg['customer'], 'headline': cfg.get('headline') or None, 'icon': 'icon.webp', 'lockup': lockup, 'quote': quote or None,
        'features': [{k: f[k] for k in ('id', 'title', 'line', 'clip', 'clipW', 'trim', 'focus') if k in f} for f in feats],
    }

    intro_name = (cfg.get('headline') or f'{cfg["customer"]} is live / with social.plus').replace('*', '').replace(' / ', ' ')
    scenes = [{'id': 'intro', 'name': intro_name, 'dur': INTRO,
               'desc': 'The app icon lands with the headline, pulses twice, then opens into the phone.'}]
    for f in feats:
        scenes.append({'id': f['id'], 'name': f['title'], 'dur': f['dur'], 'desc': f'{f["title"]}: {f["line"]}. One highlight.'})
    scenes.append({'id': 'lockup', 'name': 'Logo lockup', 'dur': LOCKUP if quote else LOCKUP_END,
                   'desc': f'The official social.plus logo x {cfg["customer"]}, side by side.'})
    if quote:
        words = len(quote['text'].split())
        scenes.append({'id': 'quote', 'name': 'Customer quote', 'dur': round(max(5.3, 2.4 + words / 3.0), 1),
                       'desc': 'The approved customer quote.'})
    scenes_json = {'v': 1, 'stage': 'final', 'look': LOOK, 'palettes': [['#111111', '#0253F7', '#FFFFFF', '#6E9BFF']],
                   'theirs': 1, 'width': 1920 if wide else 1080, 'height': 1080 if wide else 1920, 'fps': 30, 'background': '#111111',
                   'fonts': {'sans': 'plus-jakarta-sans'}, 'scenes': scenes}

    modules = {
        'base.css': ('css', tpl('base.css') + ('\n' + tpl('base-wide.css') if wide else '')),
        'shared.js': ('js', tpl('shared.js')),
        'showcase.json': ('json', json.dumps(runtime, ensure_ascii=False, indent=1)),
        'wordmark.html': ('html', wm),
        'scene-intro.js': ('js', tpl('scene-intro.js')),
        'scene-lockup.js': ('js', tpl('scene-lockup.js').replace("/*@SP_LOGO@*/''", json.dumps(sp))),
        'score.js': ('js', tpl('score.js')),
        'scenes.json': ('json', json.dumps(scenes_json, ensure_ascii=False, separators=(',', ':'))),
    }
    for f in feats:
        modules[f'scene-{f["id"]}.js'] = ('js', f"kit.scene('{f['id']}', SP.feature('{f['id']}'));\n")
    if quote:
        modules['scene-quote.js'] = ('js', tpl('scene-quote.js'))
    if '/*@SP_LOGO@*/' in modules['scene-lockup.js'][1]:
        die('the social.plus logo was not inlined')

    docs = f'{out}/film/docs'
    writes = []

    def put(coll, doc_id, data):
        os.makedirs(f'{docs}/{coll}', exist_ok=True)
        p = os.path.abspath(f'{docs}/{coll}/{doc_id}.json')
        json.dump(data, open(p, 'w'), ensure_ascii=False)
        writes.append({'op': 'set', 'collection': coll, 'doc_id': doc_id, 'file_path': p})

    title = cfg.get('title') or f'{cfg["customer"]} x social.plus showcase'
    put('film', 'meta', {'v': 1, 'title': title, 'updatedAt': cfg.get('updatedAt', '')})
    for name, (kind, text) in modules.items():
        if len(text.encode()) > 200 * 1024:
            die(f'{name} is over 200 KiB')
        put('modules', name, {'kind': kind, 'text': text})
    put('film', 'script', {'code': 'window.CUT = kit.scenes();'})
    json.dump(writes, open(f'{out}/film/batch.json', 'w'), indent=1)

    uploads = []

    def up(name, mime, wh=None):
        p = os.path.abspath(f'{assets}/{name}')
        if not os.path.exists(p):
            die(f'missing asset {p}')
        e = {'name': name, 'path': p, 'mime': mime}
        if wh:
            e['w'], e['h'] = wh
        uploads.append(e)

    up('Figtree-500.woff2', 'font/woff2'); up('Figtree-700.woff2', 'font/woff2')
    up('icon.webp', 'image/webp', (600, 600))
    for f in feats:
        wh = (f.get('clipW'), f.get('clipH'))
        up(f['clip'], 'video/mp4', wh)
        up(f'{f["id"]}-last.webp', 'image/webp', wh)
    up(f'{feats[0]["id"]}-first.webp', 'image/webp', (feats[0].get('clipW'), feats[0].get('clipH')))
    json.dump(uploads, open(f'{out}/film/uploads.json', 'w'), indent=1)
    total = INTRO + sum(f['dur'] for f in feats) + (LOCKUP if quote else LOCKUP_END) + (scenes[-1]['dur'] if quote else 0)
    print(json.dumps({'film_seconds': round(total, 1), 'scenes': [(s['id'], s['dur']) for s in scenes],
                      'documents': len(writes), 'uploads': len(uploads)}, indent=1))


if __name__ == '__main__':
    main()
