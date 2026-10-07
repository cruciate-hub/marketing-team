#!/usr/bin/env node
// Builds the foundation previews in foundations/<name>/ from the snippets that capture.mjs saved in
// raw/snippets/ (live HTML + the stylesheet rules that match it) and from tokens.json.
//
// For every foundation it writes preview.html (self-contained, links ../../tokens.css) and styles.css.
// foundation.md is written by hand and never overwritten (a template is written when it is missing).
// Screenshots (desktop.png, mobile.png) are taken by verify.mjs.
//
// No AI calls. Headless Chromium is used only to assemble the DOM and to measure computed sizes
// (nothing is fetched from the live site; images in the previews point to the site's CDN).
// Run after capture.mjs: node foundations.mjs [--only <foundation id>]

import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import prettier from 'prettier';
import { parseCss, serialize, splitSelectorList } from './css-rules.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const only = args.includes('--only') ? args[args.indexOf('--only') + 1] : undefined;
const config = JSON.parse(await fs.readFile(path.resolve(here, 'capture.config.json'), 'utf8'));
const out = config.output;
const foundationsDir = path.resolve(here, out.foundationsDir || '../foundations');
const snippetsDir = path.resolve(here, out.rawDir, 'snippets');
const tokensJsonPath = path.resolve(here, out.tokensJson);
const tokensCssPath = path.resolve(here, out.tokensCss);
const today = new Date().toISOString().slice(0, 10);
await fs.mkdir(foundationsDir, { recursive: true });

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');

// ---------------------------------------------------------------------------------------------
// Snippets
// ---------------------------------------------------------------------------------------------
async function readSnippet(id) {
  try {
    const html = await fs.readFile(path.join(snippetsDir, `${id}.html`), 'utf8');
    const css = await fs.readFile(path.join(snippetsDir, `${id}.css`), 'utf8');
    const meta = JSON.parse(await fs.readFile(path.join(snippetsDir, `${id}.json`), 'utf8'));
    return { id, html, css, meta };
  } catch {
    console.log(`  snippet ${id} missing (run capture.mjs first); skipped`);
    return null;
  }
}

/** Merge several CSS texts: one copy of every identical rule, in first-seen order; @media groups merged per prelude. */
function mergeCss(texts) {
  const seen = new Set();
  const top = [];
  const groups = new Map();
  const keyOf = (n) => (n.type === 'rule' ? `${n.selector}{${n.body}}` : n.type === 'keyframes' ? `@k ${n.prelude}{${n.body}}` : n.type === 'comment' ? '' : n.text);
  const add = (nodes, target) => {
    for (const n of nodes) {
      if (n.type === 'comment') continue;
      if (n.type === 'group') {
        if (!groups.has(n.prelude)) {
          const g = { type: 'group', prelude: n.prelude, children: [] };
          groups.set(n.prelude, g);
          top.push(g);
        }
        add(n.children, groups.get(n.prelude).children);
        continue;
      }
      const k = n.prelude ? `${target === top ? '' : 'g:'}${keyOf(n)}` : keyOf(n);
      if (!k || seen.has(k)) continue;
      seen.add(k);
      target.push(n);
    }
  };
  for (const t of texts) add(parseCss(t), top);
  return serialize(top);
}

/** Duplicate :hover / :active / :focus-visible rules as .sim-hover / .sim-active / .sim-focus so states can be shown statically. */
function stateRules(cssText) {
  const nodes = parseCss(cssText);
  const outNodes = [];
  const walk = (list, target) => {
    for (const n of list) {
      if (n.type === 'rule' && /:(hover|active|focus-visible|focus)\b/.test(n.selector)) {
        const parts = splitSelectorList(n.selector).filter((p) => /:(hover|active|focus-visible|focus)\b/.test(p));
        const mapped = parts.map((p) =>
          p
            .replace(/:hover\b/g, '.sim-hover')
            .replace(/:active\b/g, '.sim-active')
            .replace(/:focus-visible\b/g, '.sim-focus')
            .replace(/:focus\b/g, '.sim-focus')
        );
        target.push({ type: 'rule', selector: mapped.join(', '), body: n.body });
      } else if (n.type === 'group') {
        const children = [];
        walk(n.children, children);
        if (children.length) target.push({ type: 'group', prelude: n.prelude, children });
      }
    }
  };
  walk(nodes, outNodes);
  return serialize(outNodes);
}

// ---------------------------------------------------------------------------------------------
// Preview chrome (the fx-* classes are the preview's own; the samples use the site's classes)
// ---------------------------------------------------------------------------------------------
const previewCss = `
/* preview chrome (not part of the site) */
body { margin: 0; background: var(--social--dark); color: var(--text--text-color-grey-light); font-family: var(--font--figtree); }
.fx-page { max-width: 80rem; margin: 0 auto; padding: 2rem 2.5rem 5rem; }
.fx-sample .add-ons_image-wrapper { display: none; } /* preview: the accordion item's image column is shown in section 17 */
.fx-head { border-bottom: 1px solid var(--border--border-dark); padding-bottom: 1rem; margin-bottom: 2rem; }
.fx-head h1 { font-size: 1.5rem; margin: 0 0 .25rem; background: none; -webkit-text-fill-color: var(--main--white); color: var(--main--white); letter-spacing: 0; }
.fx-head p { margin: 0; color: var(--text--text-color-grey-light); font-size: .95rem; max-width: 60rem; }
.fx-block { margin: 0 0 2.5rem; }
.fx-label { font-size: .875rem; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; color: var(--text--text-color-grey-medium); margin: 0 0 .5rem; background: none; -webkit-text-fill-color: var(--text--text-color-grey-medium); }
.fx-note { font-size: .875rem; color: var(--text--text-color-grey-light); margin: 0 0 1rem; max-width: 60rem; }
.fx-sample { border: 1px dashed var(--border--border-hover); border-radius: .5rem; padding: 1.5rem; overflow: hidden; }
.fx-sample.fx-tight { padding: 1rem; }
.fx-sample.fx-light { background: var(--main--white); color: var(--text--text-color-dark); }
.fx-row { display: flex; flex-wrap: wrap; gap: 1.5rem 2rem; align-items: center; }
.fx-col { display: flex; flex-direction: column; gap: 1rem; align-items: flex-start; }
.fx-item { display: flex; flex-direction: column; gap: .5rem; align-items: flex-start; }
.fx-cap { font-size: .75rem; color: var(--text--text-color-grey-medium); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.fx-measure { display: block; font-size: .75rem; line-height: 1.3; color: var(--text--text-color-grey-medium); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-weight: 400; letter-spacing: 0; text-transform: none; margin: 1.25rem 0 .25rem; background: none; -webkit-text-fill-color: var(--text--text-color-grey-medium); }
.fx-measure:first-child { margin-top: 0; }
.fx-swatches { display: grid; grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr)); gap: 1rem; }
.fx-swatch { border: 1px solid var(--border--border-dark); border-radius: .5rem; overflow: hidden; background: var(--social--dark-gray-background); }
.fx-swatch-color { height: 4.5rem; border-bottom: 1px solid var(--border--border-dark); }
.fx-swatch-text { padding: .6rem .75rem .75rem; font-size: .8rem; line-height: 1.4; }
.fx-swatch-text code { display: block; color: var(--main--white); font-size: .78rem; word-break: break-all; }
.fx-swatch-text .fx-val { color: var(--text--text-color-grey-light); }
.fx-swatch-text .fx-use { color: var(--text--text-color-grey-medium); }
.fx-grid-3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1.5rem; align-items: start; }
.fx-grid-2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1.5rem; align-items: start; }
.fx-max-m { max-width: 47.5rem; }
.fx-box { background: var(--social--blue-transparent); outline: 1px dashed var(--social--main-blue); }
.fx-box-inner { background: var(--social--dark-gray-background); border: 1px solid var(--border--border-hover); padding: .25rem .5rem; font-size: .8rem; color: var(--text--text-color-grey-light); }
.fx-container-demo { background: var(--social--blue-transparent); outline: 1px dashed var(--social--main-blue); padding: .5rem; margin-bottom: .75rem; text-align: center; font-size: .8rem; color: var(--text--text-color-grey-light); }
.fx-table { border-collapse: collapse; font-size: .85rem; width: 100%; max-width: 60rem; }
.fx-table th, .fx-table td { text-align: left; padding: .4rem .6rem; border-bottom: 1px solid var(--border--border-dark); vertical-align: top; }
.fx-table th { color: var(--text--text-color-grey-medium); font-weight: 600; }
.fx-table td { color: var(--text--text-color-grey-light); }
.fx-table code { color: var(--main--white); }
@media (max-width: 991px) { .fx-grid-3 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 767px) { .fx-page { padding: 1.5rem 1rem 3rem; } .fx-grid-3, .fx-grid-2 { grid-template-columns: 1fr; } .fx-sample { padding: 1rem; } }
`;

function block(label, note, sampleHtml, extraClass = '') {
  return `<section class="fx-block"><h2 class="fx-label">${esc(label)}</h2>${note ? `<p class="fx-note">${note}</p>` : ''}<div class="fx-sample ${extraClass}">${sampleHtml}</div></section>`;
}

function page(title, lead, bodyHtml, css) {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)} · social.plus website foundations</title>
<link rel="stylesheet" href="../../tokens.css">
<style>
${css}
</style>
</head>
<body>
<!-- Foundation preview built ${today} by design-system/capture/foundations.mjs from live site snippets (see foundation.md). Images are the site's own CDN files. -->
<main class="fx-page">
  <header class="fx-head"><h1>${esc(title)}</h1><p>${lead}</p></header>
${bodyHtml}
</main>
</body>
</html>
`;
}

// ---------------------------------------------------------------------------------------------
// Foundation builders. Each returns { title, lead, body, css, measure? }
// ---------------------------------------------------------------------------------------------
const tokens = JSON.parse(await fs.readFile(tokensJsonPath, 'utf8'));

const tokenUse = {
  '--social--dark': 'page background; same value as --text--text-color-dark',
  '--social--dark-gray-background': 'raised dark surface: cards v2/v3/plain, secondary button fill',
  '--social--dark-card': 'dark card (3 rules)',
  '--secondary--menu-bg': 'nav bar and nav sheet background',
  '--social--grey': 'dark card / panel; card-v1 gradient start',
  '--social--light-grey': 'dark subtle fill',
  '--social--dark-pill': 'dark pill (1 rule)',
  '--social--grey-background': 'light section background (.bg-color_grey, .background-color_grey-6)',
  '--main--whitesmoke': 'tag background',
  '--main--white': 'headings and white text on dark; light surfaces',
  '--main--transparant': 'transparent (spelled "transparant" on the site)',
  '--social--main-blue': 'the action blue: primary button, tags, icons; --gradient--dark-blue aliases it',
  '--social--button-hover': 'primary button hover; second stop of the button gradient',
  '--social--button-pressed': 'primary button pressed',
  '--social--blue-transparent': 'tinted blue background',
  '--gradient--light-blue': 'gradient stop (announcement bar, heroes)',
  '--gradient--medium-blue': 'links and superscripts: the second blue next to --social--main-blue',
  '--gradient--dark-blue': 'alias of --social--main-blue',
  '--text--text-color-grey-light': 'body copy on dark',
  '--text--text-color-grey-lighter': 'h1 gradient end (1 rule)',
  '--text--text-color-grey-mid': '1 rule only',
  '--text--text-color-grey-medium': 'muted text (nav, footer, captions); 3.9:1 on #111',
  '--text--text-color-grey-muted': 'defined, unused on the live site',
  '--text--text-color-grey-dark': 'secondary text on light',
  '--text--text-color-dark': 'text on light; same value as --social--dark',
  '--border--border-dark': 'dark divider and card border',
  '--border--border-hover': 'hover border, sub-nav border',
  '--border--border-dark-grey': 'secondary button outline',
  '--border--border-med-grey': 'light-mode input and card border',
  '--border--border-light-grey': 'the .divider line (light grey on a dark site)',
  '--secondary--green': 'accent and status, never a CTA',
  '--secondary--yellow': 'accent and status, never a CTA',
  '--secondary--red': 'accent and status, never a CTA',
  '--secondary--orange': 'accent and status, never a CTA',
  '--secondary--purple': 'accent and status, never a CTA',
  '--secondary--pink': 'accent and status, never a CTA',
  '--font--figtree': 'the font stack',
  '--cta-button_icon-size': 'size of the button arrow',
  '--_typography---h1-font-size': 'h1 and .h1-font-size',
  '--_typography---h2-font-size': 'h2 and .h2-font-size',
  '--_typography---h3-font-size': 'h3 and .h3-font-size',
  '--_typography---h4-font-size': 'h4 and .h4-font-size',
  '--_typography---h5-font-size': 'h5 and .h5-font-size',
  '--_typography---h6-font-size': 'h6 and .h6-font-size',
};

function colorsFoundation() {
  const groups = [
    ['Surfaces', ['--social--dark', '--social--dark-gray-background', '--social--dark-card', '--secondary--menu-bg', '--social--grey', '--social--light-grey', '--social--dark-pill', '--social--grey-background', '--main--whitesmoke', '--main--white', '--main--transparant']],
    ['Blue (actions, links, gradients)', ['--social--main-blue', '--social--button-hover', '--social--button-pressed', '--social--blue-transparent', '--gradient--light-blue', '--gradient--medium-blue', '--gradient--dark-blue']],
    ['Text', ['--main--white', '--text--text-color-grey-light', '--text--text-color-grey-lighter', '--text--text-color-grey-mid', '--text--text-color-grey-medium', '--text--text-color-grey-muted', '--text--text-color-grey-dark', '--text--text-color-dark']],
    ['Borders', ['--border--border-dark', '--border--border-hover', '--border--border-dark-grey', '--border--border-med-grey', '--border--border-light-grey']],
    ['Secondary accents', ['--secondary--green', '--secondary--yellow', '--secondary--red', '--secondary--orange', '--secondary--purple', '--secondary--pink']],
  ];
  const byName = new Map(tokens.tokens.map((t) => [t.name, t]));
  const body = groups
    .map(([label, names]) => {
      const cards = names
        .filter((n) => byName.has(n))
        .map((n) => {
          const t = byName.get(n);
          return `<div class="fx-swatch"><div class="fx-swatch-color" style="background: var(${n})"></div><div class="fx-swatch-text"><code>${esc(n)}</code><span class="fx-val">${esc(t.value)}</span><br><span class="fx-use">${esc(tokenUse[n] || t.use || '')}</span></div></div>`;
        })
        .join('');
      return `<section class="fx-block"><h2 class="fx-label">${esc(label)}</h2><div class="fx-swatches">${cards}</div></section>`;
    })
    .join('\n');
  const offToken = [
    ['#141414', 'radial-gradient start of .c-radial-gradient sections'],
    ['#1b1b1b', 'input field background (.input-field, page embeds)'],
    ['#dc3545', 'form error text'],
    ['#3ccb7f on #093a20', '.tag.c-new'],
    ['#14152c', 'industry hero'],
    ['#12141914 / #12141929', 'the recurring card shadow (0 16px 2rem)'],
    ['#3b41ec73 / #3b41ec2e / #3b41ec1a', 'blue glows on the AI pages'],
  ]
    .map(([v, u]) => `<tr><td><code>${esc(v)}</code></td><td>${esc(u)}</td></tr>`)
    .join('');
  const other = tokens.tokens
    .filter((t) => !groups.some(([, names]) => names.includes(t.name)))
    .map((t) => `<tr><td><code>${esc(t.name)}</code></td><td>${esc(t.value)}</td><td>${esc(tokenUse[t.name] || t.use || '')}</td></tr>`)
    .join('');
  const tables = `<section class="fx-block"><h2 class="fx-label">Non-colour tokens</h2><table class="fx-table"><tr><th>Token</th><th>Value</th><th>Use</th></tr>${other}</table></section>
<section class="fx-block"><h2 class="fx-label">Colours regular sections use that are not tokens (as-is today)</h2><p class="fx-note">Listed so nobody mistakes them for tokens. The audit counted 192 off-token colour values in the stylesheets; these are the ones recurring sections depend on.</p><table class="fx-table"><tr><th>Value</th><th>Where</th></tr>${offToken}</table></section>`;
  return {
    title: 'Colors',
    lead: `The ${tokens.tokens.length} live Webflow variables (General and Typography collections) as captured ${tokens.captured}; swatches read their colour from tokens.css. Inline style on the swatches is the preview's own.`,
    body: body + tables,
    css: '',
    allowInlineStyle: true,
  };
}

const typeSelectors = [
  ['h1', 'h1'], ['h2', 'h2'], ['h3', 'h3'], ['h4', 'h4'], ['h5', 'h5'], ['h6', 'h6'],
  ['.h1-font-size', '.h1-font-size'], ['.h2-font-size', '.h2-font-size'], ['.h3-font-size', '.h3-font-size'], ['.h4-font-size', '.h4-font-size'], ['.h5-font-size', '.h5-font-size'], ['.h6-font-size', '.h6-font-size'],
  ['.heading-small', '.heading-small'], ['.heading-xsmall', '.heading-xsmall'],
  ['p', 'p:not([class])'], ['.enlarged-paragraph', '.enlarged-paragraph'], ['.text-size-tiny', '.text-size-tiny'], ['.text-size-small', '.text-size-small'], ['.superscript', '.superscript'],
  ['a', 'a:not([class])'], ['blockquote', 'blockquote'], ['li', 'li'],
];

async function snippetsFoundation(def) {
  const parts = [];
  const cssTexts = [];
  for (const s of def.blocks) {
    const snip = await readSnippet(s.snippet);
    if (!snip) continue;
    cssTexts.push(snip.css);
    const html = s.wrap ? s.wrap(snip.html) : snip.html;
    parts.push(block(s.label, s.note || '', html, s.cls || ''));
  }
  if (def.extraBlocks) parts.push(...def.extraBlocks);
  return { title: def.title, lead: def.lead, body: parts.join('\n'), css: mergeCss(cssTexts), measure: def.measure, prepare: def.prepare, states: def.states };
}

const defs = [
  {
    id: 'colors',
    build: async () => colorsFoundation(),
  },
  {
    id: 'typography',
    build: () =>
      snippetsFoundation({
        title: 'Typography',
        lead: 'Figtree (variable font, 300 to 900). Samples are the style guide\'s own markup; the grey labels show the computed size, line height, weight and letter spacing measured at 1440 and at 390 px wide.',
        measure: typeSelectors,
        blocks: [
          { snippet: 'sg-heading-tags', label: 'Heading tags h1 to h6', note: 'Sizes come from the six typography tokens (clamp() for h1 to h4). h1 carries a radial gradient text fill. Note: h1 and h2 are the same size on desktop.' },
          { snippet: 'sg-heading-classes', label: 'Heading classes .h1-font-size to .h6-font-size, .heading-small, .heading-xsmall', note: 'Same tokens on a div. The mobile sizes of the classes differ from the tags (see foundation.md).' },
          { snippet: 'sg-other-tags', label: 'Body, paragraph, link, blockquote, lists' },
          { snippet: 'sg-text-classes', label: 'Text classes: .enlarged-paragraph, .text-size-tiny, .superscript and more' },
          { snippet: 'sg-text-weights', label: 'Weights: .text-weight-medium, .text-weight-bold' },
          { snippet: 'sg-text-alignments', label: 'Alignment: .text-align-left, .text-align-center' },
          { snippet: 'sg-text-colors', label: 'Text colours: .text-color-dark, -grey-dark, -grey-medium, -grey-light, -white' },
        ],
      }),
  },
  {
    id: 'spacing',
    build: () =>
      snippetsFoundation({
        title: 'Spacing and containers',
        lead: 'The five named steps (xs .3rem, s .625rem, m 1.5rem, l 3.125rem, xl 6rem), the four containers, and the rhythm every page relies on: .section.padding_y (5rem, 3rem under 480px) and .page-padding (2.5rem, 1.5rem under 992px, 1rem under 480px).',
        blocks: [
          { snippet: 'sg-padding', label: 'Padding classes (.padding_xs … .padding_l, with -top/-left variants)', note: 'Each sample is the style guide\'s own block; the outline shows the padded box.' },
          { snippet: 'sg-margin', label: 'Margin classes (.margin_xs … .margin_l, .margin-bottom_xl)' },
          { snippet: 'sg-containers', label: 'Containers: .container-large 80rem, .container-medium-large 65rem, .container-medium 47.5rem, .container-small 30rem', note: 'The style guide labels .container-medium-large as 60rem / 960px; the CSS says 65rem = 1040px.' },
        ],
        extraBlocks: [
          block(
            'Section rhythm and page gutter (as the pages use them)',
            'Every page section is <code>section.section.padding_y</code> inside <code>.page-padding</code> and a container. Shown with the preview\'s own outlines.',
            `<div class="fx-box"><section class="section padding_y" style="outline:1px dashed var(--secondary--green)"><div class="page-padding" style="outline:1px dashed var(--secondary--yellow)"><div class="container-large"><div class="fx-box-inner">container-large · .page-padding 2.5rem each side (yellow) · .section.padding_y 5rem top and bottom (green)</div></div></div></section></div>
<div class="fx-box" style="margin-top:1rem"><div class="grid-2"><div class="fx-box-inner">.grid-2 column 1</div><div class="fx-box-inner">.grid-2 column 2 (4rem gap)</div></div></div>
<div class="fx-box" style="margin-top:1rem"><div class="grid-3"><div class="fx-box-inner">.grid-3</div><div class="fx-box-inner">.grid-3</div><div class="fx-box-inner">.grid-3 (2 columns under 992px, 1 under 480px)</div></div></div>`
          ),
        ],
      }),
  },
  {
    id: 'buttons',
    states: true,
    build: () =>
      snippetsFoundation({
        title: 'Buttons',
        lead: 'The three button styles of the style guide (primary .cta-button, secondary .cta-button.c-grey, text link .text-link in white and blue) plus the form submit button .button that every form uses. Hover and pressed are shown statically: the :hover and :active rules are copied onto .sim-hover and .sim-active.',
        blocks: [
          { snippet: 'sg-buttons', label: 'Style guide buttons (as on /styleguide)', note: 'Primary, secondary and the two text links.' },
          { snippet: 'button-primary', label: 'Primary .cta-button: default, hover, pressed', cls: 'fx-states' },
          { snippet: 'button-secondary', label: 'Secondary .cta-button.c-grey: default, hover, pressed', cls: 'fx-states' },
          { snippet: 'button-text-link', label: 'Text link .text-link: default, hover', cls: 'fx-states' },
          { snippet: 'button-submit', label: 'Form submit input.button.is-full-width: default, hover', cls: 'fx-states' },
          { snippet: 'button-submit-newsletter', label: 'Form submit input.button (newsletter): default, hover', cls: 'fx-states' },
        ],
      }),
  },
  {
    id: 'cards',
    build: () =>
      snippetsFoundation({
        title: 'Cards',
        lead: 'The four card styles as they are today: card-v1 (bordered gradient, the style guide card), card-v2 (compact icon card), card-v3 (icon card with more padding and a larger heading) and card-plain, plus the thumbnail card of every listing and the customer story card.',
        blocks: [
          { snippet: 'sg-card', label: 'card-v1 (style guide sample)', note: '1px --border--border-dark border, radial gradient --social--grey to --social--dark-gray-background, radius .5rem, padding 2.5rem; icon 48px blue circle; h3.h5-font-size; p.text-size-small; text link footer.' },
          { snippet: 'card-v1-page', label: 'card-v1 on a page (/social/uikit)', wrap: (h) => `<div class="fx-grid-3">${h}</div>` },
          { snippet: 'card-v2', label: 'card-v2 (/industry/gaming)', note: 'bg #1a1a1a, no border, radius .5rem, padding 1rem; icon 72px; heading 20px.', wrap: (h) => `<div class="fx-grid-3">${h}</div>` },
          { snippet: 'card-v3', label: 'card-v3 (/use-case/1-1-chat)', note: 'bg #1a1a1a, radius .5rem, padding 2rem; heading 28px.', wrap: (h) => `<div class="fx-grid-3">${h}</div>` },
          { snippet: 'card-v3-docs', label: 'card-v3 link card with checklist (release notes, tutorials)', wrap: (h) => `<div class="fx-grid-3">${h}</div>` },
          { snippet: 'card-plain', label: 'card-plain (/industry/gaming)', note: 'bg #1a1a1a, radius .5rem, padding 2rem; heading 20px, text 16px.', wrap: (h) => `<div class="fx-grid-2">${h}</div>` },
          { snippet: 'thumbnail-card', label: 'Thumbnail card (blog, news, product updates, tutorials)', note: 'Image with 16px radius, tags above the title, author row.', wrap: (h) => `<div class="fx-grid-3">${h}</div>` },
          { snippet: 'story-card', label: 'Customer story card (customer story strip)', wrap: (h) => `<div class="fx-grid-3">${h}</div>` },
        ],
      }),
  },
  {
    id: 'rich-text',
    build: () =>
      snippetsFoundation({
        title: 'Rich text (article body)',
        lead: 'The rich-text styles as they are today: .rich-text (blog, glossary, answers via .answers_rich-text, tutorials), .product-update_rich-text (product updates, release notes) and the plain .w-richtext. Long bodies are trimmed to their first elements; the markup is the live page\'s.',
        prepare: 'richtext',
        blocks: [
          { snippet: 'sg-rich-text', label: '.rich-text (style guide sample)' },
          { snippet: 'rich-text-blog', label: '.rich-text.c-blog (a blog post)' },
          { snippet: 'rich-text-glossary', label: '.rich-text (a glossary entry)' },
          { snippet: 'rich-text-answer', label: '.answers_rich-text (an answer page)' },
          { snippet: 'sg-rich-text-product-update', label: '.product-update_rich-text (style guide sample)' },
          { snippet: 'rich-text-product-update', label: '.product-update_rich-text (a release note)' },
        ],
      }),
  },
  {
    id: 'form-inputs',
    states: true,
    build: () =>
      snippetsFoundation({
        title: 'Form inputs',
        lead: 'The contact form (text fields .input-field, selects .input-field_select, textarea .input-field.c-area, custom checkbox, submit .button) and the newsletter form of the footer. Forms post to the site\'s form endpoint on the live site; actions, hidden fields and anti-bot attributes are removed here. The .input-field style comes from page embeds on the live site, not from the stylesheet (see foundation.md).',
        blocks: [
          { snippet: 'form-contact', label: 'Contact form (/contact/contact-sales)', wrap: (h) => `<div class="fx-max-m">${h}</div>` },
          { snippet: 'form-newsletter', label: 'Newsletter form (footer)', wrap: (h) => `<div class="fx-max-m">${h}</div>` },
        ],
      }),
  },
  {
    id: 'tags',
    build: () =>
      snippetsFoundation({
        title: 'Tags',
        lead: 'The .tag pill and its variants as used on the site: default (blog thumbnails), .c-dark (release note tags), .c-new ("New" badge), .c-nav-webinar ("Webinar" label in the nav); plus the "We\'re hiring" alert of the footer and nav, which is its own class .nav-hiring-alert, not a .tag.',
        blocks: [
          { snippet: 'tag-blog', label: '.tag (blog)', cls: 'fx-tight', wrap: (h) => `<div class="fx-row">${h}</div>` },
          { snippet: 'tag-dark', label: '.tag.c-dark (release notes)', cls: 'fx-tight', wrap: (h) => `<div class="fx-row">${h}</div>` },
          { snippet: 'tag-new', label: '.tag.c-new', cls: 'fx-tight', wrap: (h) => `<div class="fx-row">${h}</div>` },
          { snippet: 'tag-nav', label: '.nav-hiring-alert.c-footer ("We\'re hiring", footer and nav; not a .tag)', cls: 'fx-tight', wrap: (h) => `<div class="fx-row">${h}</div>` },
        ],
      }),
  },
  {
    id: 'accordion-row',
    build: () =>
      snippetsFoundation({
        title: 'Accordion row',
        lead: 'The two accordion families: the FAQ row (.accordion_item: question, chevron, answer; 1px --border--border-dark bottom line) and the feature accordion item (.add-ons_accordion-item, used next to an image). The open and close animation is a Webflow interaction; here the FAQ answer is open.',
        blocks: [
          { snippet: 'accordion-faq', label: 'FAQ row .accordion_item (open)', wrap: (h) => `<div class="fx-max-m">${h}</div>` },
          { snippet: 'accordion-addons', label: 'Feature accordion item .add-ons_accordion-item (open; its image column is hidden here, see section 17)', wrap: (h) => `<div class="fx-max-m">${h}</div>` },
        ],
      }),
  },
  {
    id: 'dividers',
    build: () =>
      snippetsFoundation({
        title: 'Dividers',
        lead: 'The .divider line (1px --border--border-light-grey, a light grey line on a dark site) and the text divider of the logo wall (.text-divider: a superscript between two fading lines, .divider.c-divider).',
        blocks: [
          { snippet: 'sg-divider', label: '.divider (style guide)' },
          { snippet: 'superscript-divider', label: '.text-divider with .superscript.c-divider (logo wall)' },
        ],
      }),
  },
  {
    id: 'imagery',
    build: () =>
      snippetsFoundation({
        title: 'Imagery',
        lead: 'The image shapes of the site. Ratio classes of the style guide: .image-16-9, .image-2-1, .image-3-1, .image-4-3, .image-3-2 (max-width 100%, aspect-ratio, 16px radius; .image-4-3 has no radius). Pages mostly use .image-square_radius, .image-fw-radius and .image-3-2. The style guide shows Webflow placeholders; here each class gets one site image (the gaming industry hero cover) so the ratio and radius are visible. The style rules for illustrations, photography and blog headers are in foundation.md.',
        blocks: [{ snippet: 'sg-images', label: 'Image ratio classes (style guide samples, one site image per class)', wrap: (h) => h.replace(/src="[^"]*placeholder[^"]*"/g, 'src="https://cdn.prod.website-files.com/66e2765d540e1939a89db4bb/6967c8810ef78c60a1c8b274_Hero%20Cover%20-%20Gaming.webp"').replace(/<img /g, '<img style="margin-bottom:1rem;display:block" ') }],
      }),
  },
];

// ---------------------------------------------------------------------------------------------
// Assemble in a browser: trim rich text, add state rows, measure type, serialize
// ---------------------------------------------------------------------------------------------
const browser = await chromium.launch();

async function assemble(def, built) {
  const stateCss = built.states ? stateRules(built.css) : '';
  const css = [built.css, stateCss ? '/* static states for the preview: :hover -> .sim-hover, :active -> .sim-active */\n' + stateCss : '', previewCss].filter(Boolean).join('\n');
  const html = page(built.title, built.lead, built.body, css);
  const tmpDir = path.join(foundationsDir, def.id);
  await fs.mkdir(tmpDir, { recursive: true });
  const tmp = path.join(tmpDir, '.assemble.html');
  await fs.writeFile(tmp, html);

  const measurements = {};
  for (const kind of ['desktop', 'mobile']) {
    const vp = config.viewports[kind];
    const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1, isMobile: kind === 'mobile', hasTouch: kind === 'mobile', colorScheme: 'dark', reducedMotion: 'reduce' });
    const pg = await ctx.newPage();
    await pg.route('**/*', (route) => (route.request().url().startsWith('file:') || /cdn\.prod\.website-files\.com|fonts\./.test(route.request().url()) ? route.continue() : route.abort()));
    await pg.goto(pathToFileURL(tmp).href, { waitUntil: 'load' });
    await pg.evaluate(() => document.fonts.ready);
    if (built.measure) {
      measurements[kind] = await pg.evaluate((selectors) => {
        const outm = {};
        for (const [label, sel] of selectors) {
          const el = [...document.querySelectorAll('.fx-sample ' + sel)].find((e) => !e.closest('.fx-measure') && !e.classList.contains('fx-cap'));
          if (!el) continue;
          const cs = getComputedStyle(el);
          outm[label] = `${parseFloat(cs.fontSize).toFixed(1).replace(/\.0$/, '')}px / ${parseFloat(cs.lineHeight).toFixed(1).replace(/\.0$/, '')}px · ${cs.fontWeight} · ${cs.letterSpacing === 'normal' ? '0' : parseFloat(cs.letterSpacing).toFixed(2) + 'px'} · ${cs.color}`;
        }
        return outm;
      }, built.measure);
    }
    if (kind === 'mobile') {
      // final DOM: do the edits once, at the end, and read back the HTML
      const finalHtml = await pg.evaluate(
        ({ prepare, states, measure, measurements, selectors }) => {
          const samples = [...document.querySelectorAll('.fx-sample')];
          // rich text: keep the first elements so every style shows once
          if (prepare === 'richtext') {
            for (const s of samples) {
              const rt = s.querySelector('.w-richtext, [class*="rich-text"]');
              if (!rt) continue;
              const kids = [...rt.children];
              const seen = {};
              let kept = 0;
              for (const k of kids) {
                const tag = k.tagName.toLowerCase();
                seen[tag] = (seen[tag] || 0) + 1;
                const keep = kept < 18 && seen[tag] <= (tag === 'p' ? 4 : 2);
                if (!keep) k.remove();
                else kept++;
              }
            }
          }
          // states: clone the sample three times (default, hover, pressed)
          if (states) {
            for (const s of samples) {
              if (!s.classList.contains('fx-states')) continue;
              const inner = s.innerHTML;
              const isTextLink = !!s.querySelector('.text-link') || !!s.querySelector('input.button');
              const rows = [['default', ''], ['hover', 'sim-hover']];
              if (!isTextLink) rows.push(['pressed', 'sim-active']);
              s.innerHTML = '';
              const row = document.createElement('div');
              row.className = 'fx-row';
              for (const [name, cls] of rows) {
                const item = document.createElement('div');
                item.className = 'fx-item';
                const holder = document.createElement('div');
                holder.innerHTML = inner;
                const target = holder.firstElementChild;
                if (cls && target) {
                  target.classList.add(cls);
                  if (cls === 'sim-hover') target.querySelectorAll('.cta-border_rotate').forEach((e) => e.classList.add('sim-hover'));
                }
                const cap = document.createElement('span');
                cap.className = 'fx-cap';
                cap.textContent = name;
                item.appendChild(holder.firstElementChild);
                item.appendChild(cap);
                row.appendChild(item);
              }
              s.appendChild(row);
            }
          }
          // type measurements as labels before each measured element
          if (measure) {
            for (const [label, sel] of selectors) {
              const el = [...document.querySelectorAll('.fx-sample ' + sel)].find((e) => !e.closest('.fx-measure') && !e.classList.contains('fx-cap'));
              if (!el) continue;
              const d = measurements.desktop?.[label];
              const m = measurements.mobile?.[label];
              if (!d) continue;
              const tag = document.createElement('span');
              tag.className = 'fx-measure';
              tag.textContent = `${label} — 1440: ${d}${m && m !== d ? ` — 390: ${m}` : ' — 390: same'}`;
              el.parentNode.insertBefore(tag, el);
            }
          }
          // links in samples go nowhere in a preview
          document.querySelectorAll('.fx-sample a[href]').forEach((a) => a.setAttribute('href', a.getAttribute('href').startsWith('http') ? a.getAttribute('href') : '#'));
          return '<!doctype html>\n' + document.documentElement.outerHTML;
        },
        { prepare: built.prepare || '', states: !!built.states, measure: !!built.measure, measurements, selectors: built.measure || [] }
      );
      await ctx.close();
      await fs.unlink(tmp).catch(() => {});
      return finalHtml;
    }
    await ctx.close();
  }
}

async function writeFoundation(def) {
  console.log(`foundation ${def.id}`);
  const built = await def.build();
  built.states = built.states ?? def.states;
  const finalHtml = await assemble(def, built);
  const dir = path.join(foundationsDir, def.id);
  let pretty = finalHtml;
  try {
    pretty = await prettier.format(finalHtml, { parser: 'html', printWidth: 120, htmlWhitespaceSensitivity: 'css' });
  } catch (e) {
    console.log(`  prettier failed: ${e.message.split('\n')[0]}`);
  }
  await fs.writeFile(path.join(dir, 'preview.html'), pretty);
  const styleOnly = pretty.match(/<style>([\s\S]*?)<\/style>/);
  let css = styleOnly ? styleOnly[1] : '';
  try {
    css = await prettier.format(css, { parser: 'css', printWidth: 120 });
  } catch {}
  await fs.writeFile(path.join(dir, 'styles.css'), `/* ${built.title}: the stylesheet rules that match the preview, copied from the live site (tokens as var(--…), see ../../tokens.css), plus the preview's own fx-* chrome. Generated ${today}. */\n` + css);
  const mdPath = path.join(dir, 'foundation.md');
  if (!(await fs.access(mdPath).then(() => true).catch(() => false))) {
    await fs.writeFile(mdPath, `# ${built.title}\n\n${built.lead}\n\n- Status: draft (${today}) · Source: live site snippets, see capture/capture.config.json (snippets)\n- Preview: preview.html · Screenshots: desktop.png, mobile.png (verify.mjs)\n\n## Values as measured\n- TO CHECK\n\n## Known inconsistencies (as-is, no decision applied)\n- TO CHECK\n`);
  }
}

for (const def of defs) {
  if (only && def.id !== only) continue;
  await writeFoundation(def);
}
await browser.close();
console.log('Done.');
