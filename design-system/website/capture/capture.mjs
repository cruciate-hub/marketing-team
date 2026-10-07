#!/usr/bin/env node
// Captures sections of the live social.plus website for the website design system.
//
// For every section in capture.config.json it writes (inside sections/<folder>/, where the
// section id is `<folder>` or `<folder>--<variant>`; a variant's files get the `--<variant>` suffix):
//   source[--variant].html   self-contained HTML + the stylesheet rules that match the section
//   styles[--variant].css    the same rules without the HTML
//   desktop[--variant].png   screenshot at 1440 wide
//   mobile[--variant].png    screenshot at 390 wide
//   section.md               header + template, only when the file does not exist yet
//                            (otherwise section.generated.md, for comparison; default variant only)
// For every snippet it writes raw/snippets/<id>.html and .css (input for foundations.mjs).
// Plus tokens.css, tokens.json, sections/index.html (gallery, see gallery.mjs) and a tokens diff in README.md.
//
// Read-only towards the live site. Analytics and consent requests are blocked. No AI calls.
// Run: node capture.mjs [--only <section id>] [--page <page id>] [--config capture.config.json]

import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import prettier from 'prettier';
import {
  parseCss,
  collectSelectorParts,
  filterRules,
  serialize,
  rewriteDeletedVars,
  parseRootVariables,
} from './css-rules.mjs';
import { writeGallery } from './gallery.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const argValue = (flag) => {
  const i = args.indexOf(flag);
  return i >= 0 ? args[i + 1] : undefined;
};
const configPath = path.resolve(here, argValue('--config') || 'capture.config.json');
const only = argValue('--only');
const onlyPage = argValue('--page');
const config = JSON.parse(await fs.readFile(configPath, 'utf8'));
const today = new Date().toISOString().slice(0, 10);

const out = config.output;
const sectionsDir = path.resolve(here, out.sectionsDir);
const rawDir = path.resolve(here, out.rawDir);
const cssCacheDir = path.join(rawDir, 'css');
const snippetsDir = path.join(rawDir, 'snippets');
await fs.mkdir(sectionsDir, { recursive: true });
await fs.mkdir(cssCacheDir, { recursive: true });
await fs.mkdir(snippetsDir, { recursive: true });

const log = (...m) => console.log(...m);

/** Folder and file suffix for a section id: `11-two-column--image-left` -> { dir: '11-two-column', suffix: '--image-left' }. */
export function splitId(id) {
  const i = id.indexOf('--');
  if (i < 0) return { dir: id, suffix: '', variantId: '' };
  return { dir: id.slice(0, i), suffix: id.slice(i), variantId: id.slice(i + 2) };
}

const sections = config.sections.filter((s) => (!only || s.id === only) && (!onlyPage || s.page === onlyPage));
const snippets = (config.snippets || []).filter((s) => !only && (!onlyPage || s.page === onlyPage));
if (!sections.length && !snippets.length) throw new Error(`Nothing matches --only ${only} / --page ${onlyPage}`);

// ---------------------------------------------------------------------------------------------
// Browser setup (step A)
// ---------------------------------------------------------------------------------------------
const browser = await chromium.launch();

async function newContext(kind) {
  const vp = config.viewports[kind];
  const mobile = kind === 'mobile';
  const ctx = await browser.newContext({
    viewport: vp,
    deviceScaleFactor: config.browser.deviceScaleFactor,
    locale: config.browser.locale,
    timezoneId: config.browser.timezoneId,
    isMobile: mobile,
    hasTouch: mobile,
    userAgent: mobile ? config.browser.mobileUserAgent : undefined,
    reducedMotion: 'reduce',
    colorScheme: 'dark',
  });
  const blocked = config.blockRequests;
  await ctx.route('**/*', (route) => {
    const url = route.request().url();
    if (blocked.some((b) => url.includes(b))) return route.abort();
    return route.continue();
  });
  await ctx.addInitScript(() => {
    document.documentElement.classList.add('sp-annc-off');
  });
  return ctx;
}

// ---------------------------------------------------------------------------------------------
// Page load + settle (steps B and C), runs in the browser
// ---------------------------------------------------------------------------------------------
async function loadAndSettle(page, url, settle) {
  await page.goto(url, { waitUntil: 'networkidle', timeout: 90000 }).catch(async (e) => {
    log(`  (networkidle not reached: ${e.message.split('\n')[0]}; continuing with load)`);
    await page.waitForLoadState('load');
  });
  await page.emulateMedia({ reducedMotion: 'reduce', colorScheme: 'dark' });
  const noMotion = await page.addStyleTag({
    content:
      '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important}',
  });
  await noMotion.evaluate((e) => e.setAttribute('data-capture-injected', ''));
  await page
    .waitForFunction(() => window.Webflow && window.gsap && window.ScrollTrigger, null, { timeout: 10000 })
    .catch(() => log('  (GSAP or Webflow not found within 10 s, continuing)'));

  // B2: scroll the whole page down and back up (lazy images, IntersectionObserver, ScrollTrigger).
  await page.evaluate(async ({ step, pause }) => {
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
    const h = () => document.documentElement.scrollHeight;
    for (let y = 0; y < h(); y += step) {
      window.scrollTo(0, y);
      await sleep(pause);
    }
    window.scrollTo(0, h());
    await sleep(pause);
    for (let y = h(); y > 0; y -= step) {
      window.scrollTo(0, y);
      await sleep(pause / 2);
    }
    window.scrollTo(0, 0);
    await sleep(300);
  }, { step: settle.scrollStep, pause: settle.scrollPauseMs });

  // C1: images eager, largest srcset candidate as src, wait for them.
  const failedImages = await page.evaluate(async (timeout) => {
    const imgs = [...document.images];
    for (const img of imgs) {
      img.loading = 'eager';
      const srcset = img.getAttribute('srcset');
      if (srcset) {
        let best = null;
        for (const cand of srcset.split(',')) {
          const [u, d] = cand.trim().split(/\s+/);
          const w = d && d.endsWith('w') ? parseFloat(d) : 0;
          if (!best || w > best.w) best = { u, w };
        }
        if (best && best.u) img.src = best.u;
        img.removeAttribute('srcset');
        img.removeAttribute('sizes');
      }
    }
    const waitOne = (img) =>
      new Promise((resolve) => {
        if (img.complete && img.naturalWidth > 0) return resolve(null);
        const done = () => resolve(img.complete && img.naturalWidth > 0 ? null : img.currentSrc || img.src);
        img.addEventListener('load', done, { once: true });
        img.addEventListener('error', done, { once: true });
        setTimeout(() => resolve('timeout: ' + (img.currentSrc || img.src)), timeout);
      });
    const results = await Promise.all(imgs.map(waitOne));
    return results.filter(Boolean);
  }, settle.imageTimeoutMs);
  if (failedImages.length) log('  images that did not load:', failedImages.slice(0, 5));
  await page.evaluate(() => document.fonts.ready);

  // C2: GSAP to its end state, then stop it so nothing re-applies on later scrolls;
  //     remove the inline styles the scripts left behind (opacity, transform, translate, clip-path, visibility, height).
  await page.evaluate(({ keepOn, unwrap, removeClasses, removeFromPage }) => {
    try {
      if (window.ScrollTrigger) {
        window.ScrollTrigger.getAll().forEach((t) => {
          try {
            t.scroll(t.end);
            t.update();
          } catch {}
        });
      }
      if (window.gsap) {
        window.gsap.globalTimeline.progress(1);
        window.gsap.globalTimeline.getChildren(true, true, true).forEach((t) => t.kill());
      }
      if (window.ScrollTrigger) window.ScrollTrigger.getAll().forEach((t) => t.kill(false));
    } catch (e) {
      console.warn('gsap settle', e);
    }
    const keep = keepOn.join(',');
    for (const el of document.querySelectorAll('body [style]')) {
      if (keep && el.matches(keep)) continue;
      el.removeAttribute('style');
    }
    // videos: show the poster frame, do not play
    for (const v of document.querySelectorAll('video')) {
      try {
        v.pause();
        v.autoplay = false;
      } catch {}
    }
    // C3: hero word spans (other pages) -> plain text
    for (const sel of unwrap) {
      for (const el of document.querySelectorAll(sel)) el.replaceWith(document.createTextNode(el.textContent));
    }
    for (const cls of removeClasses) {
      for (const el of document.querySelectorAll('.' + cls)) el.classList.remove(cls);
    }
    for (const sel of removeFromPage) {
      for (const el of document.querySelectorAll(sel)) el.remove();
    }
    document.querySelectorAll('.w-richtext').forEach((el) => el.normalize());
  }, {
    keepOn: settle.keepInlineStyleOn,
    unwrap: settle.unwrapSelectors,
    removeClasses: settle.removeClasses,
    removeFromPage: settle.removeFromPage,
  });
}

// Resolve each section to exactly one element and tag it with data-capture-id.
async function markSections(page, pageSections) {
  const problems = await page.evaluate((list) => {
    const norm = (s) => (s || '').replace(/\s+/g, ' ').trim();
    const problems = [];
    const found = [];
    for (const s of list) {
      let matches = [];
      if (s.selector) {
        matches = [...document.querySelectorAll(s.selector)];
        if (s.containsText) matches = matches.filter((m) => norm(m.textContent).includes(s.containsText));
        if (typeof s.selectorIndex === 'number') matches = matches[s.selectorIndex] ? [matches[s.selectorIndex]] : [];
      } else if (s.headingText) {
        const set = new Set();
        for (const h of document.querySelectorAll(s.headingSelector || 'h1, h2')) {
          if (norm(h.textContent).includes(s.headingText)) {
            const sec = h.closest(s.closest || 'section');
            if (sec) set.add(sec);
          }
        }
        matches = [...set];
      }
      if (matches.length !== 1) {
        problems.push(`${s.id}: ${matches.length} matches for ${s.selector || 'heading "' + s.headingText + '"'}`);
        continue;
      }
      matches[0].setAttribute('data-capture-id', s.id);
      found.push(`${s.id}: <${matches[0].tagName.toLowerCase()}.${[...matches[0].classList].join('.')}> "${norm(matches[0].textContent).slice(0, 60)}"`);
      if (s.screenshotSelector) {
        const shot = matches[0].matches(s.screenshotSelector) ? matches[0] : document.querySelector(s.screenshotSelector);
        if (shot) shot.setAttribute('data-capture-shot', s.id);
        else problems.push(`${s.id}: screenshotSelector ${s.screenshotSelector} not found`);
      }
    }
    return { problems, found };
  }, pageSections);
  for (const f of problems.found) log('    ' + f);
  if (problems.problems.length) throw new Error('Section resolution failed:\n  ' + problems.problems.join('\n  '));
}

async function markSnippets(page, pageSnippets) {
  const problems = await page.evaluate((list) => {
    const problems = [];
    for (const s of list) {
      const all = [...document.querySelectorAll(s.selector)];
      let el = all[s.index || 0];
      if (el && s.inner) el = el.querySelector(s.inner) || el;
      if (!el) {
        problems.push(`snippet ${s.id}: ${all.length} matches for ${s.selector}, index ${s.index || 0} missing`);
        continue;
      }
      el.setAttribute('data-capture-id', 'snippet:' + s.id);
    }
    return problems;
  }, pageSnippets);
  if (problems.length) log('  ' + problems.join('\n  '));
}

async function injectStaticCss(page, pageSections) {
  const css = pageSections
    .filter((s) => s.staticCss)
    .map((s) => `/* ${s.id} */\n${s.staticCss}`)
    .join('\n');
  if (css) {
    const h = await page.addStyleTag({ content: css });
    await h.evaluate((e) => e.setAttribute('data-capture-injected', ''));
  }
}

// ---------------------------------------------------------------------------------------------
// Per section: HTML clean (step E), runs in the browser on a clone
// ---------------------------------------------------------------------------------------------
async function extractHtml(page, captureId, clean, unhide) {
  return page.evaluate(({ id, clean, unhide }) => {
    const src = document.querySelector(`[data-capture-id="${CSS.escape(id)}"]`);
    if (!src) return '';
    const el = src.cloneNode(true);
    el.removeAttribute('data-capture-id');
    el.querySelectorAll('[data-capture-id],[data-capture-shot]').forEach((e) => {
      e.removeAttribute('data-capture-id');
      e.removeAttribute('data-capture-shot');
    });
    el.removeAttribute('data-capture-shot');

    for (const sel of clean.removeSelectors) el.querySelectorAll(sel).forEach((e) => e.remove());
    for (const sel of unhide || []) {
      el.querySelectorAll(sel).forEach((e) => {
        e.hidden = false;
        e.removeAttribute('hidden');
      });
    }
    const idRe = new RegExp(clean.removeIdPattern);
    const keepStyle = ['input[type=checkbox]', 'input[type=radio]'].join(',');
    const walk = [el, ...el.querySelectorAll('*')];
    for (const node of walk) {
      for (const attr of [...node.attributes]) {
        const name = attr.name;
        if (clean.removeAttributes.includes(name)) {
          node.removeAttribute(name);
          continue;
        }
        if (clean.removeAttributePrefixes.some((p) => name.startsWith(p))) {
          node.removeAttribute(name);
          continue;
        }
        if (name === 'style' && !node.matches(keepStyle)) node.removeAttribute(name);
        if (name === 'id' && idRe.test(attr.value)) node.removeAttribute('id');
        if (name === 'tabindex' && attr.value === '-1' && !node.matches('a,button,input,select,textarea,[role=button]'))
          node.removeAttribute('tabindex');
      }
      for (const cls of clean.removeClasses) node.classList.remove(cls);
      if (node.hasAttribute('class') && !node.getAttribute('class').trim()) node.removeAttribute('class');
      // absolute links and image sources
      for (const attrName of ['href', 'src', 'poster']) {
        const v = node.getAttribute(attrName);
        if (v && !v.startsWith('#') && !/^(https?:|data:|mailto:|tel:)/.test(v)) {
          try {
            node.setAttribute(attrName, new URL(v, location.href).href);
          } catch {}
        }
      }
      // videos: keep the poster, do not autoplay in the copy
      if (node.tagName === 'VIDEO') {
        node.removeAttribute('autoplay');
        node.setAttribute('preload', 'metadata');
        if (node.querySelector('source[src^="blob:"]')) node.querySelectorAll('source').forEach((s) => s.remove());
      }
    }
    return el.outerHTML;
  }, { id: captureId, clean, unhide });
}

// ---------------------------------------------------------------------------------------------
// Per section: matching stylesheet rules (step F)
// ---------------------------------------------------------------------------------------------
async function matchSelectors(page, captureId, parts, alwaysKeep) {
  const results = await page.evaluate(({ id, parts, alwaysKeep }) => {
    const el = document.querySelector(`[data-capture-id="${CSS.escape(id)}"]`);
    // same cleanup as css-rules.mjs selectorForMatching, done here so one round trip carries 10k selectors
    const strip = (part) => {
      let s = part
        .replace(
          /::?(?:-webkit-[\w-]+|-moz-[\w-]+|-ms-[\w-]+|hover|focus-visible|focus-within|focus|active|visited|link|any-link|checked|indeterminate|disabled|enabled|placeholder-shown|placeholder|autofill|valid|invalid|required|optional|read-only|read-write|target|before|after|first-letter|first-line|selection|backdrop|marker|file-selector-button|cue|part|fullscreen|default|in-range|out-of-range|user-invalid)(?:\([^()]*\))?/g,
          ''
        )
        .trim();
      if (!s || /[>+~\s]$/.test(s)) s = (s + ' *').trim();
      return s;
    };
    return parts.map((p) => {
      if (alwaysKeep.includes(p)) return true;
      const probe = strip(p);
      if (alwaysKeep.includes(probe)) return true;
      try {
        return el.matches(probe) || !!el.querySelector(probe);
      } catch {
        return false;
      }
    });
  }, { id: captureId, parts, alwaysKeep });
  const map = new Map();
  parts.forEach((p, i) => map.set(p, results[i]));
  return map;
}

function filterInlineStyleBlocks(html, dropContaining, deletedMap) {
  return html.replace(/<style([^>]*)>([\s\S]*?)<\/style>/g, (whole, attrs, css) => {
    const nodes = parseCss(css);
    const keepNode = (node) => {
      if (node.type === 'rule') return !dropContaining.some((d) => node.selector.includes(d));
      if (node.type === 'keyframes') return !dropContaining.some((d) => node.name.includes(d));
      if (node.type === 'group') {
        node.children = node.children.filter(keepNode);
        return node.children.length > 0;
      }
      if (node.type === 'comment') return !dropContaining.some((d) => node.text.toLowerCase().includes(d));
      return true;
    };
    const kept = nodes.filter(keepNode);
    return `<style${attrs}>\n${rewriteDeletedVars(serialize(kept), deletedMap)}\n</style>`;
  });
}

// ---------------------------------------------------------------------------------------------
// Tokens (step F5)
// ---------------------------------------------------------------------------------------------
function buildTokens(optCss, sharedCss) {
  const vars = parseRootVariables(optCss);
  const live = vars.filter((v) => !v.deleted);
  const deleted = vars.filter((v) => v.deleted);
  const fontFace = parseCss(sharedCss).find(
    (n) => n.type === 'rule' && n.selector === '@font-face' && /font-family:\s*Figtree/i.test(n.body)
  );
  let fontFaceCss = '';
  if (fontFace) {
    const src = fontFace.body.match(/src:\s*([^;]+)/);
    const fallback = `url(${out.fontFallbackFile}) format("woff2")`;
    const body = src ? fontFace.body.replace(src[0], `src: ${src[1].trim()}, ${fallback}`) : fontFace.body;
    fontFaceCss = `@font-face { ${body.replace(/;?$/, ';')} }`;
  }
  const extra = Object.entries(config.tokens.extraRootDeclarations || {})
    .map(([k, v]) => `  ${k}: ${v};`)
    .join('\n');
  const css = [
    `/* social.plus website tokens.`,
    `   Source: the :root block of the live Webflow stylesheet, captured ${today} by capture/capture.mjs.`,
    `   ${vars.length} variables in the stylesheet; ${deleted.length} Webflow "deleted" leftovers dropped; ${live.length} kept.`,
    `   Change values in Webflow, then re-run the capture. Do not edit by hand. */`,
    fontFaceCss,
    `:root {`,
    extra,
    ...live.map((v) => `  ${v.name}: ${v.value};`),
    `}`,
    '',
  ]
    .filter((l) => l !== undefined)
    .join('\n');
  return { css, live, deleted };
}

async function readWebsiteDoc() {
  const file = path.resolve(here, out.websiteTokensDoc);
  let text = '';
  try {
    text = await fs.readFile(file, 'utf8');
  } catch {
    return { entries: new Map(), file };
  }
  const entries = new Map();
  for (const line of text.split('\n')) {
    if (!line.trim().startsWith('|')) {
      for (const m of line.matchAll(/`(--[\w-]+)`\s*=?\s*`([^`]+)`/g)) {
        if (!entries.has(m[1])) entries.set(m[1], { value: m[2], use: '' });
      }
      continue;
    }
    const cells = line.split('|').slice(1, -1).map((c) => c.trim());
    const nameIdx = cells.findIndex((c) => /^`--[\w-]+`$/.test(c));
    if (nameIdx < 0) continue;
    const name = cells[nameIdx].replace(/`/g, '');
    const valueCell = cells.slice(nameIdx + 1).find((c) => /^`[^`]+`$/.test(c));
    if (!valueCell) continue;
    const value = valueCell.replace(/`/g, '');
    let use = '';
    if (/^H[1-6]$/.test(cells[0])) use = `${cells[0]} heading size (${cells[cells.length - 1]})`;
    else {
      const rest = cells.slice(nameIdx + 1).filter((c) => c !== valueCell);
      use = rest[rest.length - 1] || '';
    }
    entries.set(name, { value, use });
  }
  return { entries, file };
}

function normalizeColor(v, liveByName) {
  let s = v.trim().toLowerCase();
  for (let guard = 0; guard < 5 && /^var\(/.test(s); guard++) {
    const m = s.match(/^var\((--[\w-]+)\)$/);
    if (!m || !liveByName.get(m[1])) break;
    s = liveByName.get(m[1]).toLowerCase();
  }
  const named = { white: '#ffffff', whitesmoke: '#f5f5f5', black: '#000000', transparent: 'rgba(0,0,0,0)' };
  if (named[s]) s = named[s];
  if (/^#[0-9a-f]{3,4}$/.test(s)) s = '#' + s.slice(1).split('').map((c) => c + c).join('');
  if (/^#[0-9a-f]{8}$/.test(s)) {
    const r = parseInt(s.slice(1, 3), 16), g = parseInt(s.slice(3, 5), 16), b = parseInt(s.slice(5, 7), 16);
    const a = Math.round((parseInt(s.slice(7, 9), 16) / 255) * 100) / 100;
    s = `rgba(${r},${g},${b},${a})`;
  }
  return s.replace(/\s+/g, '').replace(/(^|[^\d.])0\./g, '$1.');
}

function tokensDiff(live, doc) {
  const aliases = config.tokens.nameAliases || {};
  const liveByName = new Map(live.map((v) => [v.name, v.value]));
  const docByLiveName = new Map();
  for (const [name, entry] of doc.entries) docByLiveName.set(aliases[name] || name, { ...entry, docName: name });
  const lines = [];
  const differs = [];
  for (const v of live) {
    const d = docByLiveName.get(v.name);
    if (!d) {
      lines.push(`| \`${v.name}\` | \`${v.value}\` | not in website.md | add it |`);
      continue;
    }
    if (normalizeColor(v.value, liveByName) !== normalizeColor(d.value, liveByName)) {
      differs.push(`| \`${v.name}\` | \`${v.value}\` | \`${d.value}\` | values differ |`);
    }
  }
  for (const [liveName, d] of docByLiveName) {
    if (!liveByName.has(liveName)) lines.push(`| \`${d.docName}\` | not on the live site | \`${d.value}\` | remove or check |`);
  }
  const same = live.length - differs.length - lines.filter((l) => l.includes('not in website.md')).length;
  const header = [
    `Tokens: ${live.length} live variables; ${same} match website.md; ${differs.length} differ; ${lines.filter((l) => l.includes('not in website.md')).length} are new; ${lines.filter((l) => l.includes('not on the live site')).length} are in the doc only.`,
    '',
    '| Variable | Live value | website.md | Note |',
    '|---|---|---|---|',
  ];
  return [...header, ...differs, ...lines].join('\n');
}

// ---------------------------------------------------------------------------------------------
// Writers
// ---------------------------------------------------------------------------------------------
function sectionMdHeader(section, page) {
  const title = `${section.number} · ${section.title}`;
  return [
    `# ${title}`,
    '',
    `- Status: draft (${today}) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)`,
    `- Source: ${page.url}, ${section.headingText ? `section "${section.headingText}…"` : `\`${section.selector}\``}`,
    `- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css`,
    `- Variant captured: ${section.variant || 'TO CHECK'}`,
    `- Captured on ${today} from ${page.url} by capture/capture.mjs`,
  ].join('\n');
}

const sectionMdTemplate = `
## Use it when
TO CHECK

## Don't use it when
TO CHECK

## Content slots
- TO CHECK

## Allowed variations
- TO CHECK

## Not allowed
- TO CHECK

## Accessibility and mobile
- TO CHECK

## Webflow note
- Captured from the live Webflow site; class names are not a concern.
`;

async function updateReadmeDiff(diffText) {
  const file = path.resolve(here, out.readmeDiffFile);
  const start = '<!-- tokens-diff:start -->';
  const end = '<!-- tokens-diff:end -->';
  let text = '';
  try {
    text = await fs.readFile(file, 'utf8');
  } catch {
    text = `# capture\n\n${start}\n${end}\n`;
  }
  const block = `${start}\n_Generated ${today} by capture.mjs. Live \`:root\` against \`design-system/website.md\`._\n\n${diffText}\n${end}`;
  if (text.includes(start) && text.includes(end)) {
    text = text.slice(0, text.indexOf(start)) + block + text.slice(text.indexOf(end) + end.length);
  } else text += `\n${block}\n`;
  await fs.writeFile(file, text);
}

// ---------------------------------------------------------------------------------------------
// Stylesheets: the shared sheet once, the per-page sheet per page (Webflow emits one per page)
// ---------------------------------------------------------------------------------------------
const sheetCache = new Map(); // url -> { url, text, nodes, parts }
async function loadSheet(url) {
  if (sheetCache.has(url)) return sheetCache.get(url);
  const name = path.basename(new URL(url).pathname);
  const file = path.join(cssCacheDir, name);
  let text;
  try {
    text = await fs.readFile(file, 'utf8');
  } catch {
    const r = await fetch(url);
    if (!r.ok) throw new Error(`fetch ${url}: ${r.status}`);
    text = await r.text();
    await fs.writeFile(file, text);
  }
  const nodes = parseCss(text);
  const sheet = { url, name, text, nodes, parts: [...collectSelectorParts(nodes)] };
  sheetCache.set(url, sheet);
  return sheet;
}

async function pageSheets(page) {
  const hrefs = await page.evaluate(() =>
    [...document.querySelectorAll('link[rel=stylesheet]')].map((l) => l.href).filter((h) => /webflow/.test(h))
  );
  const shared = hrefs.find((h) => /\.shared\./.test(h));
  const opt = hrefs.find((h) => !/\.shared\./.test(h));
  if (!shared || !opt) throw new Error('Could not find both Webflow stylesheets in the page: ' + hrefs.join(', '));
  return { shared: await loadSheet(shared), opt: await loadSheet(opt) };
}

// Page <style> embeds outside the section (Webflow custom code in the head, body or other embeds, for example the
// rich-text table styling): parsed like a stylesheet, only the rules that match the section are kept.
async function pageEmbedNodes(page, captureId) {
  const text = await page.evaluate((id) => {
    const el = document.querySelector(`[data-capture-id="${CSS.escape(id)}"]`);
    return [...document.querySelectorAll('style')]
      .filter((s) => !(el && el.contains(s)) && !s.hasAttribute('data-capture-injected') && s.id !== 'capture-hide-chrome')
      .map((s) => s.textContent)
      .join('\n');
  }, captureId);
  const drop = config.clean.dropInlineCssSelectorsContaining;
  const keep = (node) => {
    if (node.type === 'rule') return !drop.some((d) => node.selector.includes(d));
    if (node.type === 'group') {
      node.children = node.children.filter(keep);
      return node.children.length > 0;
    }
    return node.type !== 'comment';
  };
  return parseCss(text).filter(keep);
}

async function matchedCss(page, captureId, sheets, staticCss) {
  const embedNodes = await pageEmbedNodes(page, captureId);
  const embedParts = [...collectSelectorParts(embedNodes)];
  const parts = [...new Set([...sheets.shared.parts, ...sheets.opt.parts, ...embedParts])];
  const matches = await matchSelectors(page, captureId, parts, config.clean.alwaysKeepSelectors);
  const sharedKept = filterRules(sheets.shared.nodes, matches);
  const optKept = filterRules(sheets.opt.nodes, matches);
  const embedKept = filterRules(embedNodes, matches);
  const cssParts = [
    `/* copied from ${sheets.shared.name}, ${today} (Webflow base styles that this section uses) */`,
    serialize(sharedKept.rules),
    serialize(sharedKept.keyframes),
    `/* copied from ${sheets.opt.name}, ${today} (site styles that match this section; tokens kept as var(--…), see tokens.css) */`,
    serialize(optKept.rules),
    serialize(optKept.keyframes),
  ];
  if (embedKept.rules.length)
    cssParts.push(`/* copied from the page's own <style> embeds outside the section, ${today} (rules that match this section) */`, serialize(embedKept.rules), serialize(embedKept.keyframes));
  if (staticCss) cssParts.push(`/* static state, added by the capture */`, staticCss);
  return {
    css: rewriteDeletedVars(cssParts.filter(Boolean).join('\n'), config.clean.deletedVariableMap),
    counts: { shared: sharedKept.rules.length, site: optKept.rules.length, embed: embedKept.rules.length },
  };
}

// ---------------------------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------------------------
const results = [];
let tokenSheets = null;

for (const pageCfg of config.pages) {
  const pageSections = sections.filter((s) => s.page === pageCfg.id);
  const pageSnippets = snippets.filter((s) => s.page === pageCfg.id);
  if (!pageSections.length && !pageSnippets.length) continue;
  log(`\nPage ${pageCfg.url} (${pageSections.length} sections, ${pageSnippets.length} snippets)`);

  const contexts = {};
  const pages = {};
  for (const kind of ['desktop', 'mobile']) {
    contexts[kind] = await newContext(kind);
    pages[kind] = await contexts[kind].newPage();
    log(`  ${kind}: load + settle`);
    await loadAndSettle(pages[kind], pageCfg.url, config.settle);
    await markSections(pages[kind], pageSections);
    await markSnippets(pages[kind], pageSnippets);
    await injectStaticCss(pages[kind], pageSections);
    await pages[kind].screenshot({ path: path.join(rawDir, `${pageCfg.id}-${kind}.png`), fullPage: true }).catch((e) => log('  full-page screenshot failed: ' + e.message.split('\n')[0]));
    const fullHtml = await pages[kind].evaluate(() => '<!doctype html>\n' + document.documentElement.outerHTML);
    await fs.writeFile(path.join(rawDir, `${pageCfg.id}-${kind}.html`), fullHtml);
  }

  const sheets = await pageSheets(pages.desktop);
  if (!tokenSheets) tokenSheets = sheets;
  log(`  stylesheets: ${sheets.shared.name} (${sheets.shared.text.length} B), ${sheets.opt.name} (${sheets.opt.text.length} B)`);

  for (const section of pageSections) {
    log(`  section ${section.id}`);
    const { dir: folder, suffix } = splitId(section.id);
    const dir = path.join(sectionsDir, folder);
    await fs.mkdir(dir, { recursive: true });

    // D3: screenshots. Sticky chrome (nav, sub-nav) is hidden while other sections are shot, so it does not overlap them.
    const isChrome = !!section.chrome;
    for (const kind of ['desktop', 'mobile']) {
      const page = pages[kind];
      await page.evaluate(({ hide, sels }) => {
        let st = document.getElementById('capture-hide-chrome');
        if (!st) {
          st = document.createElement('style');
          st.id = 'capture-hide-chrome';
          document.head.appendChild(st);
        }
        st.textContent = hide && sels.length ? `${sels.join(',')}{visibility:hidden !important}` : '';
      }, { hide: !isChrome, sels: config.settle.chromeSelectors || [] });
      const shotSel = section.screenshotSelector
        ? `[data-capture-shot="${section.id}"]`
        : `[data-capture-id="${section.id}"]`;
      const loc = page.locator(shotSel).first();
      await loc.scrollIntoViewIfNeeded();
      await page.waitForTimeout(300);
      await loc.screenshot({ path: path.join(dir, `${kind}${suffix}.png`), type: 'png', animations: 'disabled', timeout: 60000 });
    }

    // D4 + E: HTML
    let html = await extractHtml(pages.desktop, section.id, config.clean, section.unhideInHtml);
    html = filterInlineStyleBlocks(html, config.clean.dropInlineCssSelectorsContaining, config.clean.deletedVariableMap);

    // F: matching rules
    const { css: sectionCss, counts } = await matchedCss(pages.desktop, section.id, sheets, section.staticCss);

    const tokensRel = path.relative(dir, path.resolve(here, out.tokensCss)).split(path.sep).join('/');
    const comments = [
      `<!-- ${section.number} ${section.title}. Captured ${today} from ${pageCfg.url} by design-system/website/capture/capture.mjs. Images are the site's own CDN files. -->`,
      section.comment ? `<!-- ${section.comment} -->` : '',
    ]
      .filter(Boolean)
      .join('\n');
    const doc = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${section.number} · ${section.title} · social.plus website section</title>
<link rel="stylesheet" href="${tokensRel}">
<style>
${sectionCss}
</style>
</head>
<body>
${comments}
${html}
</body>
</html>
`;
    let pretty = doc;
    try {
      pretty = await prettier.format(doc, { parser: 'html', printWidth: 120, htmlWhitespaceSensitivity: 'css' });
    } catch (e) {
      log(`  prettier failed for ${section.id}: ${e.message.split('\n')[0]}; writing unformatted`);
    }
    await fs.writeFile(path.join(dir, `source${suffix}.html`), pretty);
    let prettyCss = sectionCss;
    try {
      prettyCss = await prettier.format(sectionCss, { parser: 'css', printWidth: 120 });
    } catch {}
    await fs.writeFile(path.join(dir, `styles${suffix}.css`), prettyCss);

    // section.md: never overwrite a hand-written one; only the default variant writes the template
    if (!suffix) {
      const mdPath = path.join(dir, 'section.md');
      const header = sectionMdHeader(section, pageCfg);
      const exists = await fs
        .access(mdPath)
        .then(() => true)
        .catch(() => false);
      if (!exists) await fs.writeFile(mdPath, header + '\n' + sectionMdTemplate);
      else await fs.writeFile(path.join(dir, 'section.generated.md'), header + '\n');
    }

    log(`    rules kept: shared ${counts.shared}, site ${counts.site}, page embeds ${counts.embed}; html ${html.length} B`);
    results.push({ section, page: pageCfg, dir });
  }

  for (const snip of pageSnippets) {
    const captureId = 'snippet:' + snip.id;
    let html = await extractHtml(pages.desktop, captureId, config.clean, snip.unhideInHtml);
    if (!html) {
      log(`  snippet ${snip.id}: not found, skipped`);
      continue;
    }
    html = filterInlineStyleBlocks(html, config.clean.dropInlineCssSelectorsContaining, config.clean.deletedVariableMap);
    const { css, counts } = await matchedCss(pages.desktop, captureId, sheets, '');
    await fs.writeFile(path.join(snippetsDir, `${snip.id}.html`), html);
    await fs.writeFile(path.join(snippetsDir, `${snip.id}.css`), css);
    await fs.writeFile(
      path.join(snippetsDir, `${snip.id}.json`),
      JSON.stringify({ id: snip.id, page: pageCfg.url, selector: snip.selector, index: snip.index || 0, captured: today }, null, 2)
    );
    log(`  snippet ${snip.id}: html ${html.length} B, rules ${counts.shared + counts.site}`);
  }

  for (const kind of ['desktop', 'mobile']) await contexts[kind].close();
  await new Promise((r) => setTimeout(r, config.browser.pauseBetweenPagesMs || 1000));
}

// Tokens (from the first page captured; the :root block is the same in every per-page sheet)
if (tokenSheets && !only) {
  const { css, live, deleted } = buildTokens(tokenSheets.opt.text, tokenSheets.shared.text);
  await fs.writeFile(path.resolve(here, out.tokensCss), css);
  const doc = await readWebsiteDoc();
  const aliases = config.tokens.nameAliases || {};
  const docByLive = new Map();
  for (const [n, e] of doc.entries) docByLive.set(aliases[n] || n, e);
  const json = live.map((v) => ({ name: v.name, value: v.value, use: docByLive.get(v.name)?.use || '' }));
  await fs.writeFile(
    path.resolve(here, out.tokensJson),
    JSON.stringify({ source: tokenSheets.opt.url, captured: today, dropped: deleted.map((d) => d.rawName), tokens: json }, null, 2) + '\n'
  );
  const diff = tokensDiff(live, doc);
  await updateReadmeDiff(diff);
  log(`\n${diff}`);
  log(`\ntokens: ${live.length} live, ${deleted.length} deleted leftovers dropped`);
}

if (!only && !onlyPage) {
  const gallery = await writeGallery(config, here);
  log(`gallery: ${gallery}`);
}

await browser.close();
log('\nDone.');
