// Small CSS parser and serializer for the capture script.
// It keeps the rule text as written in the stylesheet (hex colours, clamp(), var() names),
// so what ends up in source.html is the site's own CSS and not a browser re-serialization.
// No AI calls. Only plain string handling.

/**
 * Parse CSS text into a flat list of nodes:
 *  { type: 'comment', text }
 *  { type: 'statement', text }                       // @import, @charset ...
 *  { type: 'rule', selector, body }                  // style rules, also @font-face, @page
 *  { type: 'keyframes', name, prelude, body }        // @keyframes name { ... }
 *  { type: 'group', prelude, children }              // @media, @supports, @container, @layer
 */
export function parseCss(text) {
  const nodes = [];
  let i = 0;
  const n = text.length;

  function skipWs() {
    while (i < n && /\s/.test(text[i])) i++;
  }

  // Reads until an unquoted, unparenthesised `{` or `;`. Returns the prelude text and the stop char.
  function readPrelude() {
    let start = i;
    let depth = 0;
    let quote = null;
    while (i < n) {
      const c = text[i];
      if (quote) {
        if (c === '\\') i++;
        else if (c === quote) quote = null;
      } else if (c === '"' || c === "'") quote = c;
      else if (c === '(') depth++;
      else if (c === ')') depth--;
      else if (c === '/' && text[i + 1] === '*') {
        const end = text.indexOf('*/', i + 2);
        i = end < 0 ? n : end + 2;
        continue;
      } else if (depth === 0 && (c === '{' || c === ';')) {
        return { prelude: text.slice(start, i).trim(), stop: c };
      }
      i++;
    }
    return { prelude: text.slice(start).trim(), stop: null };
  }

  // Reads a balanced block body after `{`, returns inner text and leaves i after `}`.
  function readBlock() {
    let depth = 1;
    let quote = null;
    const start = i;
    while (i < n) {
      const c = text[i];
      if (quote) {
        if (c === '\\') i++;
        else if (c === quote) quote = null;
      } else if (c === '"' || c === "'") quote = c;
      else if (c === '/' && text[i + 1] === '*') {
        const end = text.indexOf('*/', i + 2);
        i = end < 0 ? n : end + 2;
        continue;
      } else if (c === '{') depth++;
      else if (c === '}') {
        depth--;
        if (depth === 0) {
          const body = text.slice(start, i);
          i++;
          return body;
        }
      }
      i++;
    }
    return text.slice(start);
  }

  while (i < n) {
    skipWs();
    if (i >= n) break;
    if (text[i] === '/' && text[i + 1] === '*') {
      const end = text.indexOf('*/', i + 2);
      const stop = end < 0 ? n : end + 2;
      nodes.push({ type: 'comment', text: text.slice(i, stop) });
      i = stop;
      continue;
    }
    if (text[i] === '}') {
      i++;
      continue;
    }
    const { prelude, stop } = readPrelude();
    if (stop === ';') {
      i++;
      if (prelude) nodes.push({ type: 'statement', text: prelude + ';' });
      continue;
    }
    if (stop === null) break;
    i++; // past `{`
    const lower = prelude.toLowerCase();
    if (/^@(media|supports|container|layer|document)\b/.test(lower)) {
      const inner = readBlock();
      nodes.push({ type: 'group', prelude, children: parseCss(inner) });
    } else if (/^@(-webkit-)?keyframes\b/.test(lower)) {
      const body = readBlock();
      const name = prelude.replace(/^@(-webkit-)?keyframes\s+/i, '').trim();
      nodes.push({ type: 'keyframes', name, prelude, body });
    } else {
      const body = readBlock();
      nodes.push({ type: 'rule', selector: prelude, body: body.trim() });
    }
  }
  return nodes;
}

/** Split a selector list on top-level commas. */
export function splitSelectorList(selector) {
  const parts = [];
  let depth = 0;
  let quote = null;
  let start = 0;
  for (let i = 0; i < selector.length; i++) {
    const c = selector[i];
    if (quote) {
      if (c === '\\') i++;
      else if (c === quote) quote = null;
    } else if (c === '"' || c === "'") quote = c;
    else if (c === '(' || c === '[') depth++;
    else if (c === ')' || c === ']') depth--;
    else if (c === ',' && depth === 0) {
      parts.push(selector.slice(start, i).trim());
      start = i + 1;
    }
  }
  parts.push(selector.slice(start).trim());
  return parts.filter(Boolean);
}

/**
 * Remove state pseudo-classes and pseudo-elements so a selector can be tested with
 * element.matches() in a resting page. Structural pseudo-classes (:not, :nth-child, :first-child ...) stay.
 */
export function selectorForMatching(part) {
  let s = part
    // pseudo-elements, vendor pseudo-classes and state pseudo-classes
    .replace(
      /::?(?:-webkit-[\w-]+|-moz-[\w-]+|-ms-[\w-]+|hover|focus-visible|focus-within|focus|active|visited|link|any-link|checked|indeterminate|disabled|enabled|placeholder-shown|placeholder|autofill|valid|invalid|required|optional|read-only|read-write|target|before|after|first-letter|first-line|selection|backdrop|marker|file-selector-button|cue|part|fullscreen|default|in-range|out-of-range|user-invalid)(?:\([^()]*\))?/g,
      ''
    )
    .trim();
  // A part that was only a pseudo (":hover") or that now ends in a combinator: make it match anything.
  if (!s || /[>+~\s]$/.test(s)) s = (s + ' *').trim();
  return s;
}

/** Collect every selector part (deduplicated) from a node tree, for one matching round trip. */
export function collectSelectorParts(nodes, out = new Set()) {
  for (const node of nodes) {
    if (node.type === 'rule' && !node.selector.startsWith('@')) {
      for (const p of splitSelectorList(node.selector)) out.add(p);
    } else if (node.type === 'group') collectSelectorParts(node.children, out);
  }
  return out;
}

/**
 * Keep the rules that match. `matches` is a Map selectorPart -> boolean.
 * Also keeps @keyframes referenced by kept rules, and @media/@supports groups with at least one kept child.
 * Drops :root rules and @font-face rules (they go to tokens.css).
 */
export function filterRules(nodes, matches) {
  const kept = [];
  const animationNames = new Set();

  function walk(list) {
    const out = [];
    for (const node of list) {
      if (node.type === 'rule') {
        if (node.selector.startsWith('@')) continue; // @font-face, @page
        const parts = splitSelectorList(node.selector);
        if (parts.every((p) => p.trim() === ':root' || p.trim() === 'html:root')) continue;
        if (parts.some((p) => matches.get(p))) {
          out.push(node);
          for (const m of node.body.matchAll(/animation(?:-name)?\s*:\s*([^;]+)/g)) {
            for (const token of m[1].split(/[\s,]+/)) {
              if (/^[A-Za-z_-][\w-]*$/.test(token)) animationNames.add(token);
            }
          }
        }
      } else if (node.type === 'group') {
        const children = walk(node.children);
        if (children.length) out.push({ ...node, children });
      }
    }
    return out;
  }

  kept.push(...walk(nodes));

  const keyframes = [];
  (function collect(list) {
    for (const node of list) {
      if (node.type === 'keyframes' && animationNames.has(node.name)) keyframes.push(node);
      else if (node.type === 'group') collect(node.children);
    }
  })(nodes);

  return { rules: kept, keyframes };
}

/** Serialize nodes back to CSS text, one rule per line, groups indented. */
export function serialize(nodes, indent = '') {
  const lines = [];
  for (const node of nodes) {
    if (node.type === 'comment') lines.push(indent + node.text);
    else if (node.type === 'statement') lines.push(indent + node.text);
    else if (node.type === 'rule') lines.push(`${indent}${node.selector} { ${node.body} }`);
    else if (node.type === 'keyframes') lines.push(`${indent}${node.prelude} {${node.body}}`);
    else if (node.type === 'group') {
      lines.push(`${indent}${node.prelude} {`);
      lines.push(serialize(node.children, indent + '  '));
      lines.push(`${indent}}`);
    }
  }
  return lines.join('\n');
}

/** Rewrite references to Webflow "deleted" variables to their live equivalent. */
export function rewriteDeletedVars(cssText, map) {
  return cssText.replace(/var\(\s*(--[\w-]+)\\<deleted\\\|[^)]*?\\>\s*\)/g, (whole, name) => {
    if (map[name]) return map[name];
    return whole;
  });
}

/** Parse the :root block of a stylesheet into [{name, value, deleted}] in source order. */
export function parseRootVariables(cssText) {
  const out = [];
  for (const m of cssText.matchAll(/:root\s*\{([^}]*)\}/g)) {
    for (const decl of m[1].split(';')) {
      const idx = decl.indexOf(':');
      if (idx < 0) continue;
      const rawName = decl.slice(0, idx).trim();
      const value = decl.slice(idx + 1).trim();
      if (!rawName.startsWith('--')) continue;
      const deleted = rawName.includes('<deleted');
      const name = rawName.replace(/\\<deleted\\\|.*$/, '');
      out.push({ name, value, deleted, rawName });
    }
  }
  return out;
}
