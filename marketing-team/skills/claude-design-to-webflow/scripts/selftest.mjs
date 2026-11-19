#!/usr/bin/env node
// Proves check-board.mjs can fail: runs it once as a baseline, then with deliberate breakage injected
// into the staging page, and expects each breakage to turn a check that PASSed into a FAIL.
//   node selftest.mjs --roles examples/pricing.roles.json --board /path/Pricing.dc.html [--out ./selftest-out]
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const roles = path.resolve(arg('roles') || ''), board = path.resolve(arg('board') || ''), out = path.resolve(arg('out', './selftest-out'));
const here = path.dirname(fileURLToPath(import.meta.url));
const cfg = JSON.parse(fs.readFileSync(roles, 'utf8'));
const cases = cfg.selftest || [];
if (!cases.length) { console.error('The roles file has no "selftest" cases.'); process.exit(2); }
const run = (name, inject) => {
  const dir = path.join(out, name);
  fs.rmSync(dir, { recursive: true, force: true });   // never read a stale results.json
  const a = ['check-board.mjs', '--roles', roles, '--board', board, '--out', dir, '--widths', '1440'];
  if (inject) a.push('--inject-css', inject);
  const r = spawnSync(process.execPath, a, { cwd: here, stdio: 'ignore' });
  const f = path.join(dir, 'results.json');
  if (r.status > 1 || !fs.existsSync(f)) { console.error(`check-board.mjs did not finish for "${name}" (exit ${r.status})`); process.exit(2); }
  return JSON.parse(fs.readFileSync(f, 'utf8'));
};
const base = run('baseline');
const passed = new Set(base.filter(r => r.status === 'PASS').map(r => r.check));
let bad = 0;
for (const c of cases) {
  const res = run(c.name, c.inject);
  const caught = res.filter(r => r.status === 'FAIL' && passed.has(r.check) && new RegExp(c.expect).test(r.check));
  console.log(`${caught.length ? 'CAUGHT' : 'MISSED'}  ${c.name}${caught.length ? ': ' + caught.map(r => r.check).join(', ') : ` (expected a new FAIL matching /${c.expect}/)`}`);
  if (!caught.length) bad++;
}
console.log(bad ? `${bad} breakage(s) missed: the check is not trustworthy yet.` : 'All breakages caught.');
process.exit(bad ? 1 : 0);
