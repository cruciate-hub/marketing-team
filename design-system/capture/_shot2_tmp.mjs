import { chromium } from 'playwright';
const [,, out, sel, ...files] = process.argv;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
for (const f of files) { await p.goto('file://' + f); await p.waitForTimeout(600);
  const name=f.split('/').pop().replace('.html','');
  if (sel==='full') await p.screenshot({ path: `${out}/${name}.png`, fullPage: true });
  else { const el = await p.$(sel); await el.screenshot({ path: `${out}/${name}-${sel.replace(/[^a-z]/g,'')}.png` }); } }
await b.close();
