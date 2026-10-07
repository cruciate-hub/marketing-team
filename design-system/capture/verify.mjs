#!/usr/bin/env node
// Opens every captured sections/<folder>/source[--variant].html at 1440 and 390 wide, screenshots it, and compares it
// with the live screenshots (desktop[--variant].png, mobile[--variant].png). Also opens every foundations/<name>/preview.html,
// checks it and writes its desktop.png and mobile.png (there is no live screenshot to compare a preview with).
// Writes the comparison images to raw/verify/ and a markdown table (raw/verify/report.md) for capture/README.md.
// Checks: file loads, no sideways scroll, no broken images, no leftover <script>/tracking attributes, size and pixel difference.
// No AI calls. Run after capture.mjs and foundations.mjs: node verify.mjs [--only <id>[,<id>…]]
// With --only the report table is merged into the previous raw/verify/report.md (rows replaced by id).

import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { PNG } from 'pngjs';
import pixelmatch from 'pixelmatch';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const onlyList = args.includes('--only') ? args[args.indexOf('--only') + 1].split(',') : null;
const wanted = (id) => !onlyList || onlyList.includes(id);
const config = JSON.parse(await fs.readFile(path.resolve(here, 'capture.config.json'), 'utf8'));
const sectionsDir = path.resolve(here, config.output.sectionsDir);
const foundationsDir = path.resolve(here, config.output.foundationsDir || '../foundations');
const verifyDir = path.resolve(here, config.output.rawDir, 'verify');
await fs.mkdir(verifyDir, { recursive: true });

function splitId(id) {
  const i = id.indexOf('--');
  if (i < 0) return { dir: id, suffix: '' };
  return { dir: id.slice(0, i), suffix: id.slice(i) };
}

const browser = await chromium.launch();
const rows = [];

// Compare two PNGs on their shared area (both at 2x), returns % of differing pixels and the height delta.
function compare(liveBuf, ownBuf) {
  const a = PNG.sync.read(liveBuf);
  const b = PNG.sync.read(ownBuf);
  const w = Math.min(a.width, b.width);
  const h = Math.min(a.height, b.height);
  const crop = (img) => {
    const out = new PNG({ width: w, height: h });
    for (let y = 0; y < h; y++) img.data.copy(out.data, y * w * 4, y * img.width * 4, y * img.width * 4 + w * 4);
    return out;
  };
  const diff = new PNG({ width: w, height: h });
  const n = pixelmatch(crop(a).data, crop(b).data, diff.data, w, h, { threshold: 0.15, includeAA: true });
  return { pct: ((n / (w * h)) * 100).toFixed(1), heightDelta: b.height - a.height, widthDelta: b.width - a.width, diffPng: PNG.sync.write(diff) };
}

function leftoversIn(html) {
  const leftovers = [];
  if (/<script\b/i.test(html)) leftovers.push('<script>');
  if (/<iframe\b/i.test(html)) leftovers.push('<iframe>');
  for (const bad of ['data-w-id', 'optibase', 'gtm-', 'iubenda', 'usebasin', 'turnstile', 'recaptcha', 'analytics.js', 'googletagmanager', 'clickcease', 'data-turnstile', 'hotjar', 'apollo.io']) {
    if (html.toLowerCase().includes(bad)) leftovers.push(bad);
  }
  if (/\sdata-wf-[\w-]*=/.test(html)) leftovers.push('data-wf-* attribute');
  const imgNotCdn = [...html.matchAll(/<img[^>]*\ssrc="([^"]+)"/g)].map((m) => m[1]).filter((u) => !/^https:\/\//.test(u));
  if (imgNotCdn.length) leftovers.push(`${imgNotCdn.length} non-absolute img src`);
  return leftovers;
}

async function openAndCheck(file, kind, shotPath, screenshotSelector) {
  const vp = config.viewports[kind];
  const ctx = await browser.newContext({
    viewport: vp,
    deviceScaleFactor: config.browser.deviceScaleFactor,
    isMobile: kind === 'mobile',
    hasTouch: kind === 'mobile',
    reducedMotion: 'reduce',
    colorScheme: 'dark',
  });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('requestfailed', (r) => errors.push('request failed: ' + r.url().slice(0, 80)));
  await page.goto(pathToFileURL(file).href, { waitUntil: 'networkidle', timeout: 90000 }).catch(() => page.waitForLoadState('load'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  const info = await page.evaluate(() => ({
    scrollW: document.documentElement.scrollWidth,
    innerW: window.innerWidth,
    font: getComputedStyle(document.body).fontFamily,
    brokenImgs: [...document.images].filter((i) => !(i.complete && (i.naturalWidth > 0 || /\.svg(\?|$)/.test(i.src)))).map((i) => i.src.slice(0, 80)),
  }));
  const target = page.locator(screenshotSelector || 'body > *:not(style):not(script)').first();
  const own = await target.screenshot({ path: shotPath, type: 'png', animations: 'disabled', timeout: 90000 });
  await ctx.close();
  return { own, sideways: info.scrollW > info.innerW ? `${info.scrollW}>${info.innerW}` : 'no', brokenImgs: info.brokenImgs, errors: errors.filter((e) => !/request failed/.test(e)), font: info.font };
}

function verdict(row) {
  const d = row.viewports.desktop;
  const m = row.viewports.mobile;
  const broken = row.leftovers.length || d.brokenImgs.length || m.brokenImgs.length || m.sideways !== 'no' || d.sideways !== 'no';
  if (broken) return 'broken';
  if (row.kind === 'foundation') return 'OK';
  const pct = Math.max(parseFloat(d.pct), parseFloat(m.pct));
  const hd = Math.max(Math.abs(d.heightDelta), Math.abs(m.heightDelta));
  if (row.knownDifference && pct <= 6) return 'minor';
  if (pct > 25 || hd > 400) return 'broken';
  if (pct > 4 || hd > 4) return 'minor';
  return 'OK';
}

// Sections (every entry of the config, variants included)
for (const section of config.sections) {
  if (!wanted(section.id)) continue;
  const { dir: folder, suffix } = splitId(section.id);
  const dir = path.join(sectionsDir, folder);
  const file = path.join(dir, `source${suffix}.html`);
  let html;
  try {
    html = await fs.readFile(file, 'utf8');
  } catch {
    console.log(`${section.id}: no source${suffix}.html (not captured)`);
    continue;
  }
  const row = { id: section.id, kind: 'section', knownDifference: section.knownDifference, title: `${section.number} ${section.title}${suffix ? ` (${suffix.slice(2)})` : ''}`, leftovers: leftoversIn(html), viewports: {} };
  for (const kind of ['desktop', 'mobile']) {
    const shotPath = path.join(verifyDir, `${section.id.replace(/\//g, '-')}-${kind}.png`);
    const r = await openAndCheck(file, kind, shotPath, section.screenshotSelector);
    const live = await fs.readFile(path.join(dir, `${kind}${suffix}.png`));
    const cmp = compare(live, r.own);
    await fs.writeFile(path.join(verifyDir, `${section.id.replace(/\//g, '-')}-${kind}-diff.png`), cmp.diffPng);
    row.viewports[kind] = {
      sideways: r.sideways,
      pct: cmp.pct,
      heightDelta: Math.round(cmp.heightDelta / config.browser.deviceScaleFactor),
      widthDelta: Math.round(cmp.widthDelta / config.browser.deviceScaleFactor),
      brokenImgs: r.brokenImgs,
      errors: r.errors,
      font: r.font,
    };
  }
  row.result = verdict(row);
  rows.push(row);
  const d = row.viewports.desktop;
  const m = row.viewports.mobile;
  console.log(
    `${row.title.padEnd(44)} ${row.result.padEnd(7)} desktop ${d.pct}% h${d.heightDelta >= 0 ? '+' : ''}${d.heightDelta}px | mobile ${m.pct}% h${m.heightDelta >= 0 ? '+' : ''}${m.heightDelta}px sideways ${m.sideways}` +
      (row.leftovers.length ? ` | leftovers: ${row.leftovers.join(', ')}` : '') +
      (d.brokenImgs.length || m.brokenImgs.length ? ` | broken images: ${d.brokenImgs.length + m.brokenImgs.length}` : '') +
      (d.errors.length || m.errors.length ? ` | errors: ${[...d.errors, ...m.errors].slice(0, 3).join('; ')}` : '')
  );
}

// Foundations: check and screenshot (the screenshots are the preview's own, used by the gallery)
let foundationNames = [];
try {
  foundationNames = (await fs.readdir(foundationsDir)).sort();
} catch {}
for (const name of foundationNames) {
  if (!wanted(name) && !wanted('foundations/' + name)) continue;
  const dir = path.join(foundationsDir, name);
  const file = path.join(dir, 'preview.html');
  let html;
  try {
    html = await fs.readFile(file, 'utf8');
  } catch {
    continue;
  }
  const row = { id: `foundations/${name}`, kind: 'foundation', title: `Foundation: ${name}`, leftovers: leftoversIn(html), viewports: {} };
  for (const kind of ['desktop', 'mobile']) {
    const r = await openAndCheck(file, kind, path.join(dir, `${kind}.png`), 'main.fx-page');
    row.viewports[kind] = { sideways: r.sideways, pct: '–', heightDelta: 0, widthDelta: 0, brokenImgs: r.brokenImgs, errors: r.errors, font: r.font };
  }
  row.result = verdict(row);
  rows.push(row);
  const m = row.viewports.mobile;
  console.log(`${row.title.padEnd(44)} ${row.result.padEnd(7)} sideways ${m.sideways}` + (row.leftovers.length ? ` | leftovers: ${row.leftovers.join(', ')}` : '') + (m.brokenImgs.length ? ` | broken images: ${m.brokenImgs.length}` : ''));
}

// with --only: keep the previous rows for everything not re-checked
if (onlyList) {
  try {
    const prev = await fs.readFile(path.join(verifyDir, 'rows.json'), 'utf8');
    const prevRows = JSON.parse(prev).filter((r) => !rows.some((n) => n.id === r.id));
    rows.unshift(...prevRows);
    const order = [...config.sections.map((s) => s.id), ...foundationNames.map((n) => 'foundations/' + n)];
    rows.sort((a, b) => order.indexOf(a.id) - order.indexOf(b.id));
  } catch {}
}
await fs.writeFile(path.join(verifyDir, 'rows.json'), JSON.stringify(rows, null, 1));

const table = [
  '| Item | Result | Desktop: pixels differing, height delta | Mobile: pixels differing, height delta, sideways scroll | Leftovers / broken images |',
  '|---|---|---|---|---|',
  ...rows.map((r) => {
    const d = r.viewports.desktop;
    const m = r.viewports.mobile;
    const extra = [r.leftovers.length ? r.leftovers.join(', ') : '', d.brokenImgs.length + m.brokenImgs.length ? `${d.brokenImgs.length + m.brokenImgs.length} broken images` : ''].filter(Boolean).join('; ');
    const fmt = (v) => (r.kind === 'foundation' ? '–' : `${v.pct}%, ${v.heightDelta >= 0 ? '+' : ''}${v.heightDelta}px`);
    const note = r.knownDifference ? `by design: ${r.knownDifference}` : '';
    return `| ${r.title} | ${r.result} | ${fmt(d)} | ${fmt(m)}${r.kind === 'foundation' ? '' : ','} ${m.sideways === 'no' ? 'no sideways scroll' : 'SIDEWAYS ' + m.sideways} | ${[extra, note].filter(Boolean).join('; ') || 'none'} |`;
  }),
].join('\n');
const counts = rows.reduce((a, r) => ((a[r.result] = (a[r.result] || 0) + 1), a), {});
const summary = `${rows.length} items checked: ${counts.OK || 0} OK, ${counts.minor || 0} minor, ${counts.broken || 0} broken.`;
await fs.writeFile(path.join(verifyDir, 'report.md'), `${summary}\n\n${table}\n`);
console.log('\n' + summary + '\n\n' + table);
console.log(`\nScreenshots and diff images: ${verifyDir}`);
await browser.close();
