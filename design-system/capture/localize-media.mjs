#!/usr/bin/env node
// Makes the captured HTML and CSS self-contained for images: every image, SVG and Lottie file that
// sections/**/source*.html, sections/**/styles*.css, foundations/*/preview.html and foundations/*/styles.css
// reference on the site's CDN is copied, as served, into design-system/assets/media/ (original Webflow file
// name, URL-decoded), and the reference is rewritten to the relative path, so the files open with no network.
//
// Videos are not copied (team decision, 7 October 2026): a <video> loses its CDN src and gets a poster made
// from the video's first frame (assets/media/<name>-still.jpg, extracted with ffmpeg from a temporary download),
// so the section shows the still the live page shows before the video plays. Without ffmpeg on PATH the video
// keeps no src and no poster, and the run says so.
//
// capture.mjs and foundations.mjs run this at the end; standalone: node localize-media.mjs [--prune] [--refresh]
//   --prune    delete files in assets/media/ that nothing references any more
//   --refresh  download every referenced file again (otherwise a file already on disk is kept)
// SVGs that colour their shapes in a <style> block get those colours moved onto the shapes as attributes
// (inlineSvgStyles), because Claude Design strips <style> from uploaded SVGs and the shapes then render black.
// The manifest capture/media.json records where every file came from. Read-only towards the CDN (one GET per
// file, one at a time, a pause between them). No AI calls.

import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import prettier from 'prettier';

const here = path.dirname(fileURLToPath(import.meta.url));
const config = JSON.parse(await fs.readFile(path.resolve(here, 'capture.config.json'), 'utf8'));
const out = config.output;
const mediaCfg = config.media || {};
const mediaDir = path.resolve(here, out.mediaDir || '../assets/media');
const manifestFile = path.resolve(here, out.mediaManifest || 'media.json');
const scanDirs = [path.resolve(here, out.sectionsDir || '../sections'), path.resolve(here, out.foundationsDir || '../foundations')];
const hosts = mediaCfg.hosts || ['cdn.prod.website-files.com'];
const videoExt = new Set((mediaCfg.videoExtensions || ['.mp4', '.webm', '.mov', '.m4v', '.ogv']).map((e) => e.toLowerCase()));
const userAgent = mediaCfg.userAgent || 'marketing-team design-system capture (read-only; https://github.com/cruciate-hub/marketing-team)';
const pauseMs = mediaCfg.pauseBetweenDownloadsMs ?? 150;
const today = new Date().toISOString().slice(0, 10);

const hostRe = hosts.map((h) => h.replace(/\./g, '\\.')).join('|');
const URL_RE = new RegExp(`https?://(?:${hostRe})/[^\\s"'()<>,]+`, 'g');
const isCdn = (u) => new RegExp(`^https?://(?:${hostRe})/`).test(u);
const OLD_COMMENT = "Images are the site's own CDN files.";
export const MEDIA_COMMENT = 'Images are copies of the site\'s own files in design-system/assets/media/ (capture/localize-media.mjs); videos are not copied, a <video> shows its first frame as poster.';

const log = (...m) => console.log(...m);
const posix = (p) => p.split(path.sep).join('/');

// The file name on disk: the last path segment, URL-decoded (Webflow names are "<24 hex>_<original name>", unique
// per asset), never a path, never a dotfile. The query string is dropped.
function localName(url) {
  let seg = new URL(url).pathname;
  try {
    seg = decodeURIComponent(seg);
  } catch {}
  seg = seg.split('/').filter(Boolean).pop() || 'file';
  seg = seg.replace(/[\\/\0]/g, '_').replace(/^\.+/, '_').trim();
  return seg;
}
const extOf = (name) => path.extname(name).toLowerCase();
const isVideo = (url) => videoExt.has(extOf(new URL(url).pathname));
// How the name is written in HTML and CSS: percent-encoded, with the characters that break an unquoted url() too.
const encodeName = (name) => encodeURIComponent(name).replace(/[!'()*]/g, (c) => '%' + c.charCodeAt(0).toString(16).toUpperCase());
const shortHash = (s) => createHash('sha1').update(s).digest('hex').slice(0, 8);

async function exists(p) {
  return fs
    .access(p)
    .then(() => true)
    .catch(() => false);
}

async function readManifest() {
  try {
    const m = JSON.parse(await fs.readFile(manifestFile, 'utf8'));
    return { files: m.files || {}, videos: m.videos || {} };
  } catch {
    return { files: {}, videos: {} };
  }
}

async function writeManifest(m) {
  const sortObj = (o) => Object.fromEntries(Object.keys(o).sort().map((k) => [k, o[k]]));
  const doc = {
    note: 'Written by capture/localize-media.mjs. files: every file in design-system/assets/media/ and the CDN URL it was copied from, as served. videos: not copied (team decision); still = the first frame, used as the poster.',
    generated: today,
    files: sortObj(m.files),
    videos: sortObj(m.videos),
  };
  await fs.writeFile(manifestFile, JSON.stringify(doc, null, 2) + '\n');
}

// Claude Design strips the <style> block from every SVG it uploads, so an SVG that colours its shapes through
// classes (.cls-1 { fill: #fff }) renders black there: the social.plus logo did on 7 October 2026. This moves each
// class rule onto the elements as presentation attributes (fill, stroke, opacity …; anything else into style="…")
// and drops the <style> block. Only plain class selectors are handled; any other selector leaves the file as it is
// and is reported. Returns the new text, or null when there is nothing to change or it cannot be done safely.
const PRESENTATION = new Set(['fill', 'fill-opacity', 'fill-rule', 'stroke', 'stroke-width', 'stroke-opacity', 'stroke-linecap', 'stroke-linejoin', 'stroke-miterlimit', 'stroke-dasharray', 'stroke-dashoffset', 'opacity', 'clip-rule', 'display', 'visibility', 'stop-color', 'stop-opacity']);
export function inlineSvgStyles(svg) {
  const blocks = [...svg.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)];
  if (!blocks.length) return null;
  const rules = new Map(); // class -> [[prop, value], …] in source order
  for (const [, css] of blocks) {
    for (const [, sel, body] of css.replace(/\/\*[\s\S]*?\*\//g, '').matchAll(/([^{}]+)\{([^{}]*)\}/g)) {
      const classes = sel.split(',').map((s) => s.trim());
      if (!classes.every((c) => /^\.[\w-]+$/.test(c))) return null;
      const decls = body.split(';').map((d) => d.split(':').map((x) => x.trim())).filter(([p, v]) => p && v);
      for (const c of classes) rules.set(c.slice(1), [...(rules.get(c.slice(1)) || []), ...decls]);
    }
  }
  let out = svg.replace(/\s*<style[^>]*>[\s\S]*?<\/style>/g, '');
  out = out.replace(/<([\w:-]+)([^<>]*?)\sclass="([^"]*)"([^<>]*?)(\/?)>/g, (all, tag, before, cls, after, slash) => {
    const props = new Map();
    for (const c of cls.split(/\s+/).filter(Boolean)) for (const [p, v] of rules.get(c) || []) props.set(p, v);
    let attrs = before + after;
    const style = [];
    for (const [p, v] of props) {
      if (PRESENTATION.has(p)) {
        if (!new RegExp(`\\s${p}="`).test(attrs)) attrs += ` ${p}="${v}"`;
      } else style.push(`${p}:${v}`);
    }
    if (style.length) attrs += ` style="${style.join(';')}"`;
    return `<${tag}${attrs}${slash}>`;
  });
  return out;
}

async function inlineSvgFiles(stats) {
  for (const n of (await fs.readdir(mediaDir)).filter((n) => extOf(n) === '.svg')) {
    const file = path.join(mediaDir, n);
    const text = await fs.readFile(file, 'utf8');
    if (!text.includes('<style')) continue;
    const fixed = inlineSvgStyles(text);
    if (fixed === null) {
      stats.svgSkipped.push(n);
      continue;
    }
    await fs.writeFile(file, fixed);
    stats.svgInlined++;
    log(`  colours inlined ${n}`);
  }
}

async function download(url, dest) {
  let lastErr;
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const res = await fetch(url, { headers: { 'user-agent': userAgent, accept: '*/*' }, signal: AbortSignal.timeout(60000), redirect: 'follow' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const buf = Buffer.from(await res.arrayBuffer());
      if (!buf.length) throw new Error('empty response');
      await fs.writeFile(dest + '.part', buf);
      await fs.rename(dest + '.part', dest);
      return buf.length;
    } catch (e) {
      lastErr = e;
      await fs.rm(dest + '.part', { force: true });
      if (attempt < 3) await new Promise((r) => setTimeout(r, 1000 * attempt));
    }
  }
  throw lastErr;
}

function findFfmpeg() {
  const r = spawnSync('ffmpeg', ['-version'], { encoding: 'utf8' });
  return r.status === 0 ? 'ffmpeg' : null;
}

// First frame of a video as a JPEG poster. The video is downloaded to a temporary folder and deleted again.
async function makeStill(url, stillPath, ffmpeg) {
  const tmp = await fs.mkdtemp(path.join(os.tmpdir(), 'ds-video-'));
  try {
    const videoFile = path.join(tmp, 'video' + extOf(new URL(url).pathname));
    await download(url, videoFile);
    const r = spawnSync(ffmpeg, ['-v', 'error', '-y', '-i', videoFile, '-frames:v', '1', '-c:v', 'mjpeg', '-q:v', '3', stillPath], { encoding: 'utf8' });
    if (r.status !== 0) throw new Error('ffmpeg: ' + (r.stderr || '').trim().split('\n')[0]);
    return (await fs.stat(stillPath)).size;
  } finally {
    await fs.rm(tmp, { recursive: true, force: true });
  }
}

async function listFiles(dir, re, acc = []) {
  let entries = [];
  try {
    entries = await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return acc;
  }
  for (const e of entries) {
    if (e.name.startsWith('.') || e.name === 'node_modules') continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) await listFiles(p, re, acc);
    else if (re.test(e.name)) acc.push(p);
  }
  return acc;
}

export async function localizeMedia({ prune = false, refresh = false } = {}) {
  await fs.mkdir(mediaDir, { recursive: true });
  const manifest = await readManifest();
  const byUrl = new Map(Object.entries(manifest.files).map(([name, f]) => [f.url, name]));
  const files = (await Promise.all(scanDirs.map((d) => listFiles(d, /\.(html|css)$/)))).flat().sort();
  const stats = { files: 0, rewritten: 0, downloaded: 0, kept: 0, failed: [], videos: 0, stills: 0, noStill: [], svgInlined: 0, svgSkipped: [] };
  let ffmpeg;

  // the local name for a CDN URL: reuse the manifest's, else the decoded Webflow name (with a hash suffix on a clash)
  const nameFor = (url) => {
    if (byUrl.has(url)) return byUrl.get(url);
    let name = localName(url);
    if (manifest.files[name] && manifest.files[name].url !== url) {
      const ext = extOf(name);
      name = name.slice(0, name.length - ext.length) + '-' + shortHash(url) + ext;
    }
    return name;
  };

  const fetched = new Map(); // url -> local name | null (failed) for this run
  async function ensureFile(url) {
    if (fetched.has(url)) return fetched.get(url);
    const name = nameFor(url);
    const dest = path.join(mediaDir, name);
    if (!refresh && (await exists(dest)) && manifest.files[name]?.url === url) {
      stats.kept++;
    } else {
      try {
        const bytes = await download(url, dest);
        manifest.files[name] = { url, bytes, type: extOf(name) === '.json' ? 'lottie' : 'image', copied: today };
        byUrl.set(url, name);
        stats.downloaded++;
        log(`  copied ${name} (${(bytes / 1024).toFixed(1)} kB)`);
        await new Promise((r) => setTimeout(r, pauseMs));
      } catch (e) {
        stats.failed.push(`${url}: ${e.message}`);
        fetched.set(url, null);
        return null;
      }
    }
    fetched.set(url, name);
    return name;
  }

  async function ensureStill(url) {
    if (fetched.has(url)) return fetched.get(url);
    const videoName = localName(url);
    const ext = extOf(videoName);
    const stillName = videoName.slice(0, videoName.length - ext.length) + '-still.jpg';
    const dest = path.join(mediaDir, stillName);
    stats.videos++;
    if (!refresh && (await exists(dest)) && manifest.videos[videoName]?.url === url) {
      stats.kept++;
    } else {
      ffmpeg ??= findFfmpeg();
      if (!ffmpeg) {
        stats.noStill.push(`${videoName}: ffmpeg not found, no poster made`);
        manifest.videos[videoName] = { url, copied: false, still: null };
        fetched.set(url, null);
        return null;
      }
      try {
        const bytes = await makeStill(url, dest, ffmpeg);
        manifest.files[stillName] = { url, bytes, type: 'still', copied: today, note: 'first frame of the video, made with ffmpeg; the video itself is not in the repo' };
        manifest.videos[videoName] = { url, copied: false, still: stillName };
        stats.stills++;
        log(`  still ${stillName} from ${videoName} (${(bytes / 1024).toFixed(1)} kB)`);
      } catch (e) {
        stats.noStill.push(`${videoName}: ${e.message}`);
        manifest.videos[videoName] = { url, copied: false, still: null };
        fetched.set(url, null);
        return null;
      }
    }
    fetched.set(url, stillName);
    return stillName;
  }

  for (const file of files) {
    const original = await fs.readFile(file, 'utf8');
    if (!original.match(URL_RE) && !original.includes(OLD_COMMENT)) continue;
    stats.files++;
    const rel = posix(path.relative(path.dirname(file), mediaDir));
    const localRef = (name) => `${rel}/${encodeName(name)}`;
    let text = original;
    let changed = 0;

    // 1. videos: drop the CDN src, add the first-frame poster, say so in a comment
    if (file.endsWith('.html')) {
      const videoTags = [...text.matchAll(/<video\b[^>]*>/g)].map((m) => m[0]);
      for (const tag of videoTags) {
        const m = tag.match(/\ssrc="([^"]+)"/);
        if (!m || !isCdn(m[1]) || !isVideo(m[1])) continue;
        const url = m[1];
        const still = await ensureStill(url);
        let newTag = tag.replace(m[0], '');
        if (still && !/\sposter=/.test(newTag)) newTag = newTag.replace(/^<video\b/, `<video poster="${localRef(still)}"`);
        const note = `<!-- The live section plays the video ${localName(url)} (not in the repo: team decision, 7 October 2026); ${still ? 'the poster is its first frame' : 'no poster could be made (ffmpeg missing)'}. -->\n`;
        text = text.replace(tag, note + newTag);
        changed++;
      }
      // <source src="…mp4"> inside a video: remove the element
      text = text.replace(/<source\b[^>]*\ssrc="([^"]+)"[^>]*>(?:<\/source>)?/g, (whole, src) => {
        const hit = isCdn(src) && isVideo(src);
        if (hit) changed++;
        return hit ? '' : whole;
      });
    }

    // 2. images, SVG, Lottie JSON: copy and rewrite (src, poster, data-src, href, CSS url(), inline styles alike)
    const urls = [...new Set(text.match(URL_RE) || [])];
    for (const url of urls) {
      if (isVideo(url)) continue; // a video URL anywhere else stays untouched and is reported below
      const name = await ensureFile(url);
      if (!name) continue;
      const ref = localRef(name);
      text = text.split(url).join(ref);
      changed++;
    }
    text = text.split(OLD_COMMENT).join(MEDIA_COMMENT);
    const left = (text.match(URL_RE) || []).filter((u) => isVideo(u));
    if (left.length) stats.failed.push(`${posix(path.relative(path.resolve(here, '..'), file))}: video URL left in place (not a <video src>): ${left.join(', ')}`);
    if (text !== original) {
      // the same formatting capture.mjs and foundations.mjs use, so the diff is only the media change
      try {
        text = await prettier.format(text, file.endsWith('.css') ? { parser: 'css', printWidth: 120 } : { parser: 'html', printWidth: 120, htmlWhitespaceSensitivity: 'css' });
      } catch {}
      await fs.writeFile(file, text);
      stats.rewritten++;
    }
  }

  // 3. unreferenced files in assets/media
  const referenced = new Set();
  for (const file of files) {
    const text = await fs.readFile(file, 'utf8');
    for (const m of text.matchAll(/assets\/media\/([^\s"')<>]+)/g)) {
      try {
        referenced.add(decodeURIComponent(m[1]));
      } catch {
        referenced.add(m[1]);
      }
    }
  }
  await inlineSvgFiles(stats);
  const onDisk = (await fs.readdir(mediaDir)).filter((n) => !n.startsWith('.'));
  const unreferenced = onDisk.filter((n) => !referenced.has(n));
  if (prune) {
    for (const n of unreferenced) {
      await fs.rm(path.join(mediaDir, n), { force: true });
      delete manifest.files[n];
      log(`  pruned ${n}`);
    }
  }
  for (const n of Object.keys(manifest.files)) if (!(await exists(path.join(mediaDir, n)))) delete manifest.files[n];
  await writeManifest(manifest);

  const total = (await Promise.all((await fs.readdir(mediaDir)).map((n) => fs.stat(path.join(mediaDir, n)).then((s) => s.size)))).reduce((a, b) => a + b, 0);
  log(
    `media: ${stats.files} files scanned, ${stats.rewritten} rewritten; ${stats.downloaded} copied, ${stats.kept} already there, ${stats.failed.length} failed; ` +
      `${stats.videos} video references, ${stats.stills} stills made; ${stats.svgInlined} SVGs with colours inlined; ${(await fs.readdir(mediaDir)).length} files in ${posix(path.relative(path.resolve(here, '..'), mediaDir))} (${(total / 1e6).toFixed(1)} MB)` +
      (unreferenced.length ? `; ${unreferenced.length} unreferenced${prune ? ' (pruned)' : ' (run with --prune to delete)'}: ${unreferenced.join(', ')}` : '')
  );
  for (const f of stats.failed) log(`  FAILED ${f}`);
  for (const f of stats.noStill) log(`  NO STILL ${f}`);
  for (const f of stats.svgSkipped) log(`  SVG <style> NOT INLINED (selector other than a class; Claude Design will strip it) ${f}`);
  return stats;
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const args = process.argv.slice(2);
  const stats = await localizeMedia({ prune: args.includes('--prune'), refresh: args.includes('--refresh') });
  process.exitCode = stats.failed.length || stats.noStill.length || stats.svgSkipped.length ? 1 : 0;
}
