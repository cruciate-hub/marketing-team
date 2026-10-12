#!/usr/bin/env python3
"""Checks that the Claude Design page "social.plus" and this folder hold the same design system.

Give it a local copy of the page's project/ folder (read the page's files with Claude: SKILL.md, index.html and
everything under project/ except the generated api/, tokens.css and manifest.json). It compares every file the page
shows with its source here, as claude-design/SYNC.md maps them, and prints MATCH or DIFF per file. Exit code 1 when
anything differs. Run it before a re-sync from GitHub and after bringing a change made in Claude Design back here.

Run: python3 claude-design-check.py /path/to/copy/project
No network, no AI calls.
"""
import json, os, re, sys, urllib.parse
from pathlib import Path

root = Path(__file__).resolve().parent.parent  # design-system/
cd = root / 'claude-design'
page = Path(sys.argv[1]) if len(sys.argv) > 1 else None
if not page or not (page / 'design-system.json').is_file():
    sys.exit('usage: python3 claude-design-check.py <copy of the page>/project')

# The brand-book sections the page shows, and their file here (copied as they are).
DOCS = {
    '01-colors.md': 'foundations/colors/foundation.md',
    '02-typography.md': 'foundations/typography/foundation.md',
    '03-spacing.md': 'foundations/spacing/foundation.md',
    '03b-grid-and-frame.md': 'foundations/grid-and-frame/foundation.md',
    '04-shadows-and-radius.md': 'foundations/shadows-and-radius/foundation.md',
    '05-logo.md': 'foundations/logo/foundation.md',
    '06-icons.md': 'foundations/icons/foundation.md',
    '07-imagery.md': 'foundations/imagery/foundation.md',
    '08-accessibility.md': 'foundations/accessibility/foundation.md',
    '09-sections.md': 'sections/README.md',
    '10-recipes.md': 'claude-design/10-recipes.md',
    '11-taste.md': 'taste.md',
    '12-proposals.md': 'claude-design/12-proposals.md',
    'tokens.json': 'claude-design/tokens.json',
    'components/bundle.css': 'claude-design/components/bundle.css',
    'components/framed.css': 'sections/framed/framed.css',
    'fonts/figtree.woff2': 'figtree.woff2',
    'fonts/geist-mono.woff2': 'geist-mono.woff2',
    'assets/Logos/README.md': 'claude-design/assets/Logos/README.md',
    'assets/media/README.md': 'claude-design/assets/media/README.md',
    'assets/third-party/README.md': 'claude-design/assets/third-party/README.md',
    'assets/media/611e684cb5fcc8846ebc30dc_explosion.json': 'assets/media/611e684cb5fcc8846ebc30dc_explosion.json',
}
GENERATED = '## Consuming this system (generated — do not edit)'
results = []


def report(status, what, note=''):
    results.append(status)
    print(f'{status:5} {what}{"  (" + note + ")" if note else ""}')


def blob_free(text):
    """Asset references differ only in where the file lives: /_blob/<id> on the page, ../../assets/<group>/<file> here."""
    text = re.sub(r'/_blob/[0-9a-f]{32}', '/_blob/ASSET', text)
    return text


def as_page_preview(source):
    """What the sync does to a source file: drop the tokens.css link (the page preloads its tokens) and point the
    images at the page's asset store. Lottie JSON stays a file."""
    lines = [l for l in source.split('\n') if not re.fullmatch(r'\s*<link rel="stylesheet" href="(\.\./)+tokens\.css"\s*/?>\s*', l)]
    text = '\n'.join(lines)
    return re.sub(r'(?:\.\./)+assets/(?:media|third-party)/([^"\')\s]+)',
                  lambda m: m.group(0) if m.group(1).endswith('.json') else '/_blob/ASSET', text)


# 1. Brand book, tokens, fonts, asset notes: the same bytes.
for p, src in DOCS.items():
    a, b = page / p, root / src
    if not a.exists() and not b.exists():
        continue
    if not a.exists() or not b.exists():
        report('DIFF', p, f'missing {"on the page" if not a.exists() else "here: " + src}')
    else:
        report('MATCH' if a.read_bytes() == b.read_bytes() else 'DIFF', p, src)

# 2. The page README: its authored part is claude-design/README.md; the page appends the generated index.
readme = (page / 'README.md').read_text()
authored = readme.split(GENERATED)[0]
report('MATCH' if authored == (cd / 'README.md').read_text() else 'DIFF', 'README.md', 'claude-design/README.md (authored part)')

# 3. Cards: the first line from cards.json, the body from its source.
cards = json.loads((cd / 'cards.json').read_text())
on_page = {c for c in os.listdir(page / 'components') if (page / 'components' / c / 'preview.html').is_file()}
for c in sorted(set(cards['cards']) | on_page):
    prev = page / 'components' / c / 'preview.html'
    if c not in cards['cards']:
        report('DIFF', f'components/{c}/preview.html', 'a card on the page that cards.json does not list')
        continue
    if not prev.is_file():
        report('DIFF', f'components/{c}/preview.html', 'listed in cards.json, not on the page')
        continue
    first, body = prev.read_text().split('\n', 1)
    if first != cards['cards'][c]:
        report('DIFF', f'components/{c}/preview.html', f'card line: page {first!r}, cards.json {cards["cards"][c]!r}')
        continue
    mirror = cd / 'components' / c / 'preview.html'
    src = cards['sources'].get(c)
    if mirror.is_file():
        ok = blob_free(body) == blob_free(mirror.read_text().split('\n', 1)[1])
        report('MATCH' if ok else 'DIFF', f'components/{c}/preview.html', str(mirror.relative_to(root)))
    elif src and (root.parent / src).is_file():
        ok = blob_free(body) == as_page_preview((root.parent / src).read_text())
        report('MATCH' if ok else 'DIFF', f'components/{c}/preview.html', src.replace('design-system/', ''))
    else:
        report('DIFF', f'components/{c}/preview.html', 'no source in cards.json')
for c in cards['notShown']:
    if (page / 'components' / c / 'preview.html').is_file():
        report('DIFF', f'components/{c}/preview.html', 'on the page, but cards.json lists it as not shown')

# 4. Card notes: page-written ones are mirrored in claude-design/components/; the others carry their section.md or
#    foundation.md (without its title line).
for c in sorted(os.listdir(page / 'components')):
    note = page / 'components' / c / 'README.md'
    if not note.is_file():
        continue
    mirror = cd / 'components' / c / 'README.md'
    if mirror.is_file():
        report('MATCH' if note.read_bytes() == mirror.read_bytes() else 'DIFF', f'components/{c}/README.md', str(mirror.relative_to(root)))
        continue
    src = cards['sources'].get(c, '')
    folder = (root.parent / src).parent
    md = folder / ('section.md' if (folder / 'section.md').is_file() else 'foundation.md')
    if not md.is_file():
        report('DIFF', f'components/{c}/README.md', 'no mirror and no section.md or foundation.md')
        continue
    body = '\n'.join(md.read_text().split('\n')[1:]).strip()
    report('MATCH' if body in note.read_text() else 'DIFF', f'components/{c}/README.md', str(md.relative_to(root)))

# 5. Anything else on the page that this check does not know.
known = set(DOCS) | {'README.md', 'design-system.json', 'tokens.css', 'manifest.json'}
for f in sorted(page.rglob('*')):
    rel = f.relative_to(page).as_posix()
    if f.is_dir() or rel in known or rel.startswith(('api/', 'components/')):
        continue
    report('DIFF', rel, 'a page file this check does not map: add it to SYNC.md and DOCS')

diffs = results.count('DIFF')
print(f'\n{results.count("MATCH")} match, {diffs} differ')
sys.exit(1 if diffs else 0)
