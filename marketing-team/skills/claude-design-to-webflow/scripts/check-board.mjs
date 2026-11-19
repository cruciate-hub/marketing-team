#!/usr/bin/env node
// Board-vs-staging check for a Claude Design -> Webflow build.
// Renders the board (.dc.html) and the staging page side by side at each width and reports
// PASS / FAIL / WARN / NOTE per check. Exit code 1 when anything FAILs.
//
//   node check-board.mjs --roles examples/pricing.roles.json --board /path/Board.dc.html \
//        --url https://<site>.webflow.io/<page> --out ./check-out [--widths 1440,800,390] \
//        [--new-css ".pricing-chat,.c-pricing"] [--inject-css "<css for the staging page>"]
//
// The roles file maps board selectors to staging selectors (written in the Map step); see
// examples/pricing.roles.json and ../references/check-board.md.
import { chromium } from 'playwright';
import { PNG } from 'pngjs';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const rolesFile = arg('roles');
if (!rolesFile) { console.error('Missing --roles <file>. See references/check-board.md.'); process.exit(2); }
const cfg = JSON.parse(fs.readFileSync(rolesFile, 'utf8'));
const board = path.resolve(arg('board', cfg.board || ''));
const url = arg('url', cfg.url);
const out = path.resolve(arg('out', './check-out'));
const widths = arg('widths', '1440,800,390').split(',').map(Number);
const newCss = (arg('new-css', (cfg.newCss || []).join(',')) || '').split(',').map(s => s.trim()).filter(Boolean);
const inject = arg('inject-css', '');
if (!fs.existsSync(board)) { console.error('Board file not found: ' + board); process.exit(2); }
if (!url) { console.error('Missing --url'); process.exit(2); }
fs.mkdirSync(out, { recursive: true });

const ROLES = cfg.roles;                 // { name: [boardSelector, stagingSelector] }
const KNOWN = cfg.known || [];           // [{ widths:[800], roles:'*'|[..], props:[..], why }]
const HIDE = cfg.hideCss || '#iubenda-cs-banner,.iubenda-cs-container{display:none!important}';
const KEYS = ['fontSize', 'lineHeight', 'fontWeight', 'letterSpacing', 'color', 'paddingTop', 'paddingBottom',
  'paddingLeft', 'paddingRight', 'backgroundColor', 'borderRadius', 'gap', 'borderTopWidth', 'borderBottomWidth'];
const LINE = cfg.lineColor || [32, 32, 34];   // frame line #202022
const results = [];
const meta = {};
const add = (status, check, detail = '') => results.push({ status, check, detail });
const isKnown = (w, role, prop) => KNOWN.find(k => (!k.widths || k.widths.includes(w))
  && (k.roles === '*' || (k.roles || []).includes(role)) && (k.props || []).includes(prop));

const chromePath = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome']
  .find(p => fs.existsSync(p));
const browser = await chromium.launch(chromePath ? { executablePath: chromePath } : {});

async function open(src, w) {
  const p = await browser.newPage({ viewport: { width: w, height: 900 } });
  const errors = [];
  p.on('pageerror', e => errors.push(e.message));
  const target = src === 'board' ? 'file://' + board : url + (url.includes('?') ? '&' : '?') + 'check=' + Date.now();
  await p.goto(target, { waitUntil: 'load' });
  await p.addStyleTag({ content: HIDE });
  if (src === 'board') {
    // A local board can't load its /_blob fonts: fall back to the same families from Google Fonts,
    // so text wraps and heights match. Images stay blank, which doesn't move the layout.
    const ok = await p.evaluate(async () => { try { await document.fonts.load('16px Figtree'); } catch { } return [...document.fonts].some(f => f.family.replace(/"/g, '') === 'Figtree' && f.status === 'loaded'); });
    if (!ok) {
      await p.addStyleTag({ url: 'https://fonts.googleapis.com/css2?family=Figtree:wght@300..900&family=Geist+Mono:wght@100..900&display=block' }).catch(() => {});
      await p.evaluate(async () => { await Promise.all(['400 16px Figtree', '600 16px Figtree', '500 12px "Geist Mono"'].map(f => document.fonts.load(f).catch(() => null))); });
      await p.waitForFunction(() => [...document.fonts].some(f => f.family.replace(/"/g, '') === 'Figtree' && f.status === 'loaded'), null, { timeout: 8000 }).catch(() => {});
      await p.waitForTimeout(300);
    }
    meta.fonts = await p.evaluate(() => [...document.fonts].some(f => f.family.replace(/"/g, '') === 'Figtree' && f.status === 'loaded'));
  }
  if (src === 'stage' && inject) await p.addStyleTag({ content: inject });
  // scroll through once so lazy content and scroll-triggered states settle
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); });
  await p.waitForTimeout(1200);
  return { p, errors };
}

const measure = (p, idx) => p.evaluate(([R, K, idx]) => {
  const o = {};
  for (const [k, sels] of Object.entries(R)) {
    const e = document.querySelector(sels[idx]);
    if (!e) { o[k] = null; continue; }
    const r = e.getBoundingClientRect(), c = getComputedStyle(e);
    const visible = r.width > 0 && r.height > 0 && c.display !== 'none' && c.visibility !== 'hidden';
    // text styles only mean something on an element that holds text itself
    const hasText = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) || /^(P|H[1-6]|SPAN|A|LABEL|LI|BUTTON)$/.test(e.tagName) && !!e.textContent.trim();
    const layout = /flex|grid/.test(c.display);
    let bg = c.backgroundColor, a = e;   // effective background: first non-transparent ancestor
    while (a && /rgba\(0, 0, 0, 0\)|transparent/.test(getComputedStyle(a).backgroundColor)) a = a.parentElement;
    if (a) bg = getComputedStyle(a).backgroundColor;
    o[k] = { visible, hasText, layout, x: Math.round(r.left), y: Math.round(r.top + scrollY), w: Math.round(r.width), h: Math.round(r.height),
      ...Object.fromEntries(K.map(x => [x, c[x]])), backgroundColor: bg };
  }
  return o;
}, [ROLES, KEYS, idx]);

const TEXT_KEYS = new Set(['fontSize', 'lineHeight', 'fontWeight', 'letterSpacing', 'color']);
const rgb = v => (v.match(/[\d.]+/g) || []).map(Number);
function differs(f, av, sv, a, s) {
  if (TEXT_KEYS.has(f) && !(a.hasText && s.hasText)) return false;
  if (f === 'letterSpacing') { av = av === 'normal' ? '0px' : av; sv = sv === 'normal' ? '0px' : sv; }
  if (/^border(Top|Bottom)Width$/.test(f)) return Math.abs(parseFloat(av) - parseFloat(sv)) > 0.5;   // a missing 1px line must fail
  if (f === 'gap') { if (!a.layout || !s.layout) return false; const g = v => Math.max(0, ...(v.match(/[\d.]+(?=px)/g) || ['0']).map(Number)); return Math.abs(g(av) - g(sv)) > (cfg.toleranceCss ?? 1.5); }
  if (/color/i.test(f)) {
    const x = rgb(av), y = rgb(sv); if (x.length < 3 || y.length < 3) return av !== sv;
    const ax = x[3] ?? 1, ay = y[3] ?? 1;
    if (ax === 0 && ay === 0) return false;
    return Math.abs(ax - ay) > 0.05 || x.slice(0, 3).some((v, i) => Math.abs(v - y[i]) > (cfg.toleranceColor ?? 4));
  }
  const n1 = parseFloat(av), n2 = parseFloat(sv);
  if (!isNaN(n1) && !isNaN(n2) && /px/.test(av + sv) && !/ /.test(av + sv)) return Math.abs(n1 - n2) > (cfg.toleranceCss ?? 1.5);
  return av !== sv;
}

// Frame lines: does a full-width-ish row of the frame-line colour sit at a section's top and bottom edge,
// and how many vertical frame lines run through the section? Checked per section role, on both renders.
function lineAt(png, y, x0, x1) {
  const { width: w, height: h, data } = png;
  for (let yy = Math.max(0, y - 3); yy <= Math.min(h - 1, y + 3); yy++) {
    let n = 0, t = 0;
    for (let x = Math.max(0, x0); x < Math.min(w, x1); x += 4) { t++; const i = (yy * w + x) * 4; if (near(data, i)) n++; }
    if (t && n > t * 0.6) return true;
  }
  return false;
}
function vlines(png, y0, y1) {
  const { width: w, height: h, data } = png; const cols = [];
  for (let x = 0; x < w; x++) { let n = 0, t = 0; for (let y = Math.max(0, y0 + 4); y < Math.min(h, y1 - 4); y += 4) { t++; if (near(data, (y * w + x) * 4)) n++; } if (t && n > t * 0.8) cols.push(x); }
  return cols.filter((x, k) => k === 0 || x - cols[k - 1] > 1).length;
}
const near = (d, i) => Math.abs(d[i] - LINE[0]) <= 4 && Math.abs(d[i + 1] - LINE[1]) <= 4 && Math.abs(d[i + 2] - LINE[2]) <= 4;
const SECTION_ROLES = cfg.sectionRoles || Object.keys(ROLES).filter(k => /^section/i.test(k));

for (const W of widths) {
  const m = {}, shots = {}; const pm = {};
  for (const [src, idx] of [['board', 0], ['stage', 1]]) {
    const { p, errors } = await open(src, W);
    m[src] = await measure(p, idx);
    pm[src] = await p.evaluate(() => ({ sw: document.scrollingElement.scrollWidth, iw: innerWidth }));
    shots[src] = path.join(out, `${src}-${W}.png`);
    await p.screenshot({ path: shots[src], fullPage: true });
    if (src === 'stage' && errors.length) add('WARN', `page errors @${W}`, errors.slice(0, 3).join(' | '));
    await p.close();
  }
  // 1. roles: presence, size, type and spacing
  for (const k of Object.keys(ROLES)) {
    const a = m.board[k], s = m.stage[k];
    if (!a) { add('FAIL', `role ${k} @${W}`, 'board selector matches nothing: fix the roles file'); continue; }
    if (!s) { add('FAIL', `role ${k} @${W}`, 'missing on staging'); continue; }
    if (a.visible !== s.visible) { add('FAIL', `role ${k} @${W}`, `visible on board ${a.visible}, on staging ${s.visible}`); continue; }
    if (!a.visible) continue;
    const fails = [], notes = [];
    for (const f of ['x', 'w', 'h']) if (Math.abs(a[f] - s[f]) > (cfg.tolerancePx ?? 3)) (isKnown(W, k, f) ? notes : fails).push(`${f} ${a[f]}→${s[f]}`);
    for (const f of KEYS) {
      if (/^border(Top|Bottom)Width$/.test(f) && SECTION_ROLES.includes(k)) continue;   // section lines: the frame-line checks own them (a shared line can sit on either section)
      const av = a[f], sv = s[f];
      if (differs(f, av, sv, a, s)) (isKnown(W, k, f) ? notes : fails).push(`${f} ${av}→${sv}`);
    }
    if (a.hasText !== s.hasText) notes.push('text styles not compared: one side is a wrapper, point the role at the text element');
    if (fails.length) add('FAIL', `role ${k} @${W}`, fails.join(' | '));
    else add('PASS', `role ${k} @${W}`);
    if (notes.length) add('NOTE', `role ${k} @${W} (known Webflow difference)`, notes.join(' | '));
  }
  // 2. frame lines per section: top edge, bottom edge, vertical lines
  const png = { board: PNG.sync.read(fs.readFileSync(shots.board)), stage: PNG.sync.read(fs.readFileSync(shots.stage)) };
  for (const k of SECTION_ROLES) {
    const a = m.board[k], s = m.stage[k];
    if (!a || !s || !a.visible || !s.visible) continue;
    for (const [edge, ya, ys] of [['top', a.y, s.y], ['bottom', a.y + a.h - 1, s.y + s.h - 1]]) {
      const hb = lineAt(png.board, ya, 0, png.board.width), hs = lineAt(png.stage, ys, 0, png.stage.width);
      if (hb && !hs) add('FAIL', `frame line ${edge} of ${k} @${W}`, 'board has a line here, staging does not');
      else if (!hb && hs) add('WARN', `frame line ${edge} of ${k} @${W}`, 'staging has a line the board does not');
      else add('PASS', `frame line ${edge} of ${k} @${W}`, hb ? 'line on both' : 'no line on either');
    }
    const vb = vlines(png.board, a.y, a.y + a.h), vs = vlines(png.stage, s.y, s.y + s.h);
    add(vs < vb ? 'FAIL' : 'PASS', `vertical frame lines in ${k} @${W}`, `board ${vb}, staging ${vs}`);
  }
  // 3. horizontal scroll
  add(pm.stage.sw > pm.stage.iw + 1 ? 'FAIL' : 'PASS', `horizontal scroll @${W}`, `scrollWidth ${pm.stage.sw}, viewport ${pm.stage.iw}`);
  if (meta.fonts === false) add('WARN', `board fonts @${W}`, 'Figtree did not load for the board: text sizes and heights are unreliable');
}

// 4. accessibility (axe, WCAG 2.x A/AA) + checks axe doesn't make, on staging at the first width
{
  const { p } = await open('stage', widths[0]);
  await p.addScriptTag({ content: fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8') });
  const scope = cfg.a11yScope || 'main';
  const axe = await p.evaluate(async (scope) => {
    const ctx = document.querySelector(scope) ? scope : document;
    const r = await window.axe.run(ctx, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] } });
    return r.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, t: v.nodes.slice(0, 3).map(n => n.target.join(' ')).join(' ; ') }));
  }, scope);
  if (!axe.length) add('PASS', 'accessibility (axe WCAG A/AA)', `scope ${scope}`);
  for (const v of axe) add(['serious', 'critical'].includes(v.impact) ? 'FAIL' : 'WARN', `accessibility: ${v.id} (${v.impact})`, `${v.n}× ${v.t}`);
  const extra = await p.evaluate((scope) => {
    const root = document.querySelector(scope) || document.body;
    const svgs = [...root.querySelectorAll('svg')].filter(s => s.getAttribute('role') !== 'img' && (s.getAttribute('aria-hidden') !== 'true' || s.getAttribute('focusable') !== 'false')).length;
    const ids = {}; let emptyIds = 0; document.querySelectorAll('[id]').forEach(e => { if (!e.id.trim()) { emptyIds++; return; } ids[e.id] = (ids[e.id] || 0) + 1; });
    const raw = [...root.querySelectorAll('[href]')].filter(e => !['A', 'LINK'].includes(e.tagName) && !e.closest('svg')).length;
    const relLink = [...document.querySelectorAll('a + link[rel]')].length;
    return { emptyIds, mains: document.querySelectorAll('main').length, svgs, dup: Object.entries(ids).filter(([, n]) => n > 1).map(([k, n]) => `${k}×${n}`), raw, relLink };
  }, scope);
  add(extra.mains === 1 ? 'PASS' : 'FAIL', 'one <main>', `found ${extra.mains}`);
  add(extra.svgs ? 'FAIL' : 'PASS', 'decorative SVGs have aria-hidden + focusable=false', extra.svgs ? `${extra.svgs} without` : '');
  add(extra.dup.length ? 'FAIL' : 'PASS', 'no duplicate ids', extra.dup.slice(0, 8).join(', '));
  if (extra.emptyIds) add('WARN', 'empty id attributes', `${extra.emptyIds} elements have id="" (Webflow writes these for some elements; harmless but invalid)`);
  add(extra.raw ? 'FAIL' : 'PASS', 'no raw href attributes on non-links (whtml leftovers)', extra.raw ? `${extra.raw} found` : '');
  add(extra.relLink ? 'FAIL' : 'PASS', 'no stray <link rel> after anchors (rel on a Webflow link)', extra.relLink ? `${extra.relLink} found` : '');

  // 5. internal links answer 200; external links are listed, never failed
  const links = await p.evaluate((scope) => [...new Set([...(document.querySelector(scope) || document.body).querySelectorAll('a[href]')].map(a => a.href))], scope);
  const origin = new URL(url).origin; const bad = [], ext = [];
  for (const h of links) {
    if (!/^https?:/.test(h)) continue;
    if (!h.startsWith(origin)) { ext.push(h); continue; }
    const r = await p.request.get(h.split('#')[0], { maxRedirects: 5 }).catch(() => null);
    if (!r || r.status() >= 400) bad.push(`${h} ${r ? r.status() : 'error'}`);
  }
  add(bad.length ? 'FAIL' : 'PASS', 'internal links answer < 400', bad.length ? bad.join(', ') : `${links.length - ext.length} checked`);
  if (ext.length) add('NOTE', 'external links (not checked)', ext.slice(0, 10).join(', '));

  // 6. new CSS is live: every listed class or rule text appears in the page's CSS
  if (newCss.length) {
    const css = await p.evaluate(async () => {
      let t = [...document.querySelectorAll('style')].map(s => s.textContent).join('\n');
      for (const l of document.querySelectorAll('link[rel=stylesheet]')) { try { t += await (await fetch(l.href, { cache: 'no-store' })).text(); } catch { } }
      return t;
    });
    const flat = css.replace(/\s+/g, '');
    const esc = x => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const missing = newCss.filter(c => { const n = c.replace(/\s+/g, ''); return /^\.[\w-]+$/.test(n) ? !new RegExp(esc(n) + '(?![\\w-])').test(flat) : !flat.includes(n); });
    add(missing.length ? 'FAIL' : 'PASS', 'new CSS is live on staging', missing.length ? `missing: ${missing.join(', ')} (stale CDN? republish and wait)` : `${newCss.length} found`);
  } else add('WARN', 'new CSS is live on staging', 'no --new-css given: list the classes or rules this build added');
  await p.close();
}
await browser.close();

// side-by-side images per width
for (const W of widths) {
  const a = PNG.sync.read(fs.readFileSync(path.join(out, `board-${W}.png`))), b = PNG.sync.read(fs.readFileSync(path.join(out, `stage-${W}.png`)));
  const h = Math.max(a.height, b.height), img = new PNG({ width: a.width + b.width + 16, height: h });
  img.data.fill(255);
  PNG.bitblt(a, img, 0, 0, a.width, a.height, 0, 0); PNG.bitblt(b, img, 0, 0, b.width, b.height, a.width + 16, 0);
  fs.writeFileSync(path.join(out, `side-by-side-${W}.png`), PNG.sync.write(img));
}

const order = { FAIL: 0, WARN: 1, NOTE: 2, PASS: 3 };
results.sort((x, y) => order[x.status] - order[y.status]);
const count = s => results.filter(r => r.status === s).length;
const summary = `FAIL ${count('FAIL')} · WARN ${count('WARN')} · NOTE ${count('NOTE')} · PASS ${count('PASS')}`;
const md = [`# Board check: ${path.basename(board)} vs ${url}`, '', `${new Date().toISOString()} · widths ${widths.join('/')}`, '', `**${summary}**`, '',
  ...results.map(r => `- **${r.status}** ${r.check}${r.detail ? ': ' + r.detail : ''}`), '',
  `Screenshots: ${widths.map(W => `side-by-side-${W}.png`).join(', ')}`].join('\n');
fs.writeFileSync(path.join(out, 'report.md'), md);
fs.writeFileSync(path.join(out, 'results.json'), JSON.stringify(results, null, 1));
console.log(md);
process.exit(count('FAIL') ? 1 : 0);
