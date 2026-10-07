#!/usr/bin/env node
// Writes sections/index.html: a gallery of every foundation preview and every captured section
// (desktop and mobile screenshots, links to the files). Reads capture.config.json and the folders on disk.
// No AI calls. Run: node gallery.mjs (capture.mjs also calls it at the end of a full run).

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));

function splitId(id) {
  const i = id.indexOf('--');
  if (i < 0) return { dir: id, suffix: '', variantId: '' };
  return { dir: id.slice(0, i), suffix: id.slice(i), variantId: id.slice(i + 2) };
}

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');

async function exists(p) {
  return fs
    .access(p)
    .then(() => true)
    .catch(() => false);
}

/** First line after `# ` in a markdown file, and the "Variant captured" line, for the card text. */
async function readMdTitle(file) {
  try {
    const text = await fs.readFile(file, 'utf8');
    const m = text.match(/^#\s+(.+)$/m);
    const lead = text.split('\n').find((l) => l.trim() && !l.startsWith('#') && !l.startsWith('-') && !l.startsWith('|'));
    return { title: m ? m[1].trim() : '', lead: (lead || '').trim() };
  } catch {
    return { title: '', lead: '' };
  }
}

export async function writeGallery(config, baseDir = here) {
  const out = config.output;
  const galleryFile = path.resolve(baseDir, out.galleryFile);
  const galleryDir = path.dirname(galleryFile);
  const sectionsDir = path.resolve(baseDir, out.sectionsDir);
  const foundationsDir = path.resolve(baseDir, out.foundationsDir || '../foundations');
  const tokensRel = path.relative(galleryDir, path.resolve(baseDir, out.tokensCss)).split(path.sep).join('/');
  const rel = (p) => path.relative(galleryDir, p).split(path.sep).join('/');
  const today = new Date().toISOString().slice(0, 10);

  // Foundations: every folder with preview.html
  const foundations = [];
  try {
    for (const name of (await fs.readdir(foundationsDir)).sort()) {
      const dir = path.join(foundationsDir, name);
      if (!(await exists(path.join(dir, 'preview.html')))) continue;
      const md = await readMdTitle(path.join(dir, 'foundation.md'));
      foundations.push({ name, dir, title: md.title || name, lead: md.lead });
    }
  } catch {}

  // Sections grouped by folder, in config order
  const groups = new Map();
  for (const s of config.sections) {
    const { dir: folder, variantId } = splitId(s.id);
    if (!groups.has(folder)) groups.set(folder, { folder, number: s.number, title: s.title, page: config.pages.find((p) => p.id === s.page), variants: [] });
    const g = groups.get(folder);
    g.variants.push({ ...s, variantId, suffix: variantId ? `--${variantId}` : '', page: config.pages.find((p) => p.id === s.page) });
  }

  const families = [
    ['Global chrome', (f) => f.startsWith('global/')],
    ['Heroes', (f) => /^0\d-/.test(f)],
    ['Content sections', (f) => /^[12]\d-/.test(f)],
    ['Listings', (f) => /^3\d-/.test(f)],
    ['Articles', (f) => /^4\d-/.test(f)],
    ['/vs/ family', (f) => /^5\d-/.test(f)],
    ['Pricing family', (f) => /^6\d-/.test(f)],
  ];

  const anchor = (s) => s.replace(/[^a-z0-9]+/gi, '-');

  const foundationCards = foundations
    .map((f) => {
      const d = rel(f.dir);
      return `
    <article class="card" id="f-${anchor(f.name)}">
      <header>
        <h3>${esc(f.title)}</h3>
        <p class="meta">${esc(f.lead)} · <a href="${d}/preview.html">preview.html</a> · <a href="${d}/foundation.md">foundation.md</a></p>
      </header>
      <div class="shots">
        <figure class="desktop"><img src="${d}/desktop.png" alt="${esc(f.title)}, desktop" loading="lazy"><figcaption>1440</figcaption></figure>
        <figure class="mobile"><img src="${d}/mobile.png" alt="${esc(f.title)}, mobile" loading="lazy"><figcaption>390</figcaption></figure>
      </div>
    </article>`;
    })
    .join('\n');

  const sectionCards = [];
  const toc = [];
  for (const [familyName, test] of families) {
    const list = [...groups.values()].filter((g) => test(g.folder));
    if (!list.length) continue;
    sectionCards.push(`<h2 class="family" id="${anchor(familyName)}">${esc(familyName)}</h2>`);
    for (const g of list) {
      const dir = rel(path.join(sectionsDir, g.folder));
      toc.push(`<a href="#${anchor(g.folder)}">${esc(g.number)} ${esc(g.title)}</a>`);
      const variantBlocks = g.variants
        .map(
          (v) => `
      <div class="variant">
        <p class="meta"><strong>${esc(v.variantId ? v.title : 'Default')}</strong> · ${esc(v.variant || '')} · <a href="${dir}/source${v.suffix}.html">source${v.suffix}.html</a> · <a href="${dir}/styles${v.suffix}.css">styles${v.suffix}.css</a> · <a href="${v.page?.url || '#'}" rel="noopener">live page</a></p>
        <div class="shots">
          <figure class="desktop"><img src="${dir}/desktop${v.suffix}.png" alt="${esc(v.title)}, desktop" loading="lazy"><figcaption>1440</figcaption></figure>
          <figure class="mobile"><img src="${dir}/mobile${v.suffix}.png" alt="${esc(v.title)}, mobile" loading="lazy"><figcaption>390</figcaption></figure>
        </div>
      </div>`
        )
        .join('\n');
      sectionCards.push(`
    <article class="card" id="${anchor(g.folder)}">
      <header>
        <h3><span class="num">${esc(g.number)}</span> ${esc(g.title)} <span class="folder">${esc(g.folder)}/</span></h3>
        <p class="meta"><a href="${dir}/section.md">section.md</a> · ${g.variants.length} variant${g.variants.length > 1 ? 's' : ''}</p>
      </header>
      ${variantBlocks}
    </article>`);
    }
  }

  const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>social.plus website design system: gallery</title>
<link rel="stylesheet" href="${tokensRel}">
<style>
  body { margin: 0; background: var(--social--dark); color: var(--main--white); font-family: var(--font--figtree); }
  .wrap { max-width: 80rem; margin: 0 auto; padding: 2rem 1rem 4rem; }
  h1 { font-size: 1.75rem; margin: 0 0 .25rem; }
  h2.family { font-size: 1.25rem; margin: 2.5rem 0 1rem; padding-top: 1rem; border-top: 1px solid var(--border--border-dark); color: var(--text--text-color-grey-light); }
  .lead, .meta { color: var(--text--text-color-grey-light); }
  .lead { margin: 0 0 2rem; }
  nav.toc { display: flex; flex-wrap: wrap; gap: .5rem 1rem; margin-bottom: 2rem; font-size: .875rem; }
  a { color: var(--main--white); }
  .card { border: 1px solid var(--border--border-dark); border-radius: .75rem; padding: 1.25rem; margin-bottom: 1.5rem; background: var(--social--dark-gray-background); }
  .card h3 { margin: 0 0 .25rem; font-size: 1.125rem; }
  .num { color: var(--social--main-blue); margin-right: .5rem; }
  .folder { color: var(--text--text-color-grey-medium); font-weight: 400; font-size: .875rem; margin-left: .5rem; }
  .meta { margin: 0 0 1rem; font-size: .875rem; }
  .variant { border-top: 1px dashed var(--border--border-hover); padding-top: .75rem; margin-top: .75rem; }
  .shots { display: grid; grid-template-columns: minmax(0, 3.7fr) minmax(0, 1fr); gap: 1rem; align-items: start; }
  figure { margin: 0; }
  figure img { width: 100%; height: auto; display: block; border-radius: .5rem; border: 1px solid var(--border--border-dark); background: var(--social--dark); }
  figcaption { color: var(--text--text-color-grey-medium); font-size: .75rem; margin-top: .25rem; }
  @media (max-width: 767px) { .shots { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="wrap">
  <h1>social.plus website design system</h1>
  <p class="lead">Foundations and sections captured ${today} from the live site by <code>capture/capture.mjs</code>. Each card: desktop (1440) and mobile (390) screenshot, with links to the self-contained HTML and the notes. See <a href="README.md">README.md</a> for the rule and the index.</p>
  <nav class="toc"><a href="#foundations">Foundations</a> ${toc.join('\n')}</nav>
  <h2 class="family" id="foundations">Foundations</h2>
${foundationCards || '<p class="meta">No foundation previews yet (run foundations.mjs, then verify.mjs for the screenshots).</p>'}
${sectionCards.join('\n')}
</div>
</body>
</html>
`;
  await fs.writeFile(galleryFile, html);
  return galleryFile;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const config = JSON.parse(await fs.readFile(path.resolve(here, 'capture.config.json'), 'utf8'));
  console.log('gallery:', await writeGallery(config, here));
}
