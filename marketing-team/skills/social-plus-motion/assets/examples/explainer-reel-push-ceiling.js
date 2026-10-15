// social.plus reel v2 — one continuous world, Vox-style camera storytelling. 1080×1920, 30 s.
const W = 1080, H = 1920, D = 30;
const cl = x => Math.max(0, Math.min(1, x));
const seg = (t, a, b) => cl((t - a) / (b - a));
const eo = x => 1 - Math.pow(1 - x, 3);
const eio = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const eox = x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x);
const eob = (x, s = 1.5) => x <= 0 ? 0 : 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2);
const lerp = (a, b, p) => a + (b - a) * p;
const $ = {}; let pat;

// ---------- world layout ----------
const PH = { x: 90, y: 100, w: 900, h: 1760 };                  // phone
const CEIL = PH.y + 430;                                          // ceiling line (world y)
const HTS = [14, 24, 40, 64, 96, 124, 124, 124];
const NTOP = []; { let y = CEIL + 14; HTS.forEach(h => { NTOP.push(y); y += h + 10; }); }
const DOC = { x: 1500, y: 200, w: 1000, h: 1500 };
const L1 = { x: DOC.x + 70, y: DOC.y + 470 }, L2 = { x: DOC.x + 70, y: DOC.y + 1010 };
const PL = { x: 2800, y: 0 };
const HERO = { x: 2890, y: 860, w: 900, h: 240 };
const HC = { x: HERO.x + HERO.w / 2, y: HERO.y + HERO.h / 2 };
const DOT = { x: HERO.x + HERO.w - 64, y: HERO.y + 120 };
const NET = [[-1500, -1150], [0, -1300], [1450, -1050], [-1700, 250], [1650, 300], [-1300, 1350], [150, 1480], [1500, 1450]];

// ---------- camera keys (world centre cx,cy and zoom z) ----------
const CAM = [
  { t: 0.0, cx: 380, cy: NTOP[7] + 62, z: 2.3 },
  { t: 1.5, cx: 400, cy: NTOP[7] + 40, z: 2.15 },
  { t: 2.7, cx: 540, cy: 870, z: 0.98, e: eio },
  { t: 3.95, cx: 540, cy: 840, z: 1.04 },
  { t: 4.45, cx: L1.x + 395, cy: L1.y + 30, z: 1.16, e: eox },        // whip to the report
  { t: 6.7, cx: L1.x + 405, cy: L1.y + 60, z: 1.22 },
  { t: 7.3, cx: L2.x + 395, cy: L2.y + 30, z: 1.18, e: eio },
  { t: 8.9, cx: L2.x + 405, cy: L2.y + 50, z: 1.24 },
  { t: 9.45, cx: PL.x + 540, cy: 960, z: 1.0, e: eox },               // whip to the sorting plane
  { t: 13.5, cx: PL.x + 540, cy: 940, z: 1.1 },
  { t: 14.3, cx: HC.x, cy: HC.y + 30, z: 1.12, e: eio },             // push into the person
  { t: 18.5, cx: HC.x, cy: HC.y + 45, z: 1.16 },
  { t: 20.3, cx: HC.x, cy: HC.y + 200, z: 0.42, e: eio },             // pull back: the network
  { t: 24.5, cx: HC.x + 60, cy: HC.y + 160, z: 0.47 },
  { t: 25.5, cx: DOT.x, cy: DOT.y, z: 7.0, e: x => eio(x) },           // dive into the blue dot
  { t: 30, cx: DOT.x, cy: DOT.y, z: 7.0 },
];
function cam(t) {
  let i = 0; while (i < CAM.length - 2 && t >= CAM[i + 1].t) i++;
  const a = CAM[i], b = CAM[i + 1];
  const p = (b.e || (x => x))(seg(t, a.t, b.t));
  return { cx: lerp(a.cx, b.cx, p), cy: lerp(a.cy, b.cy, p), z: Math.exp(lerp(Math.log(a.z), Math.log(b.z), p)) };
}
const proj = (c, x, y) => [W / 2 + (x - c.cx) * c.z, H / 2 + (y - c.cy) * c.z];

// ---------- markup helpers ----------
const ICON = {
  heart: '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
  bubble: '<path d="M21 11.5a8.4 8.4 0 0 1-12.2 7.5L3 21l2-5.6A8.4 8.4 0 1 1 21 11.5z"/>',
  at: '<circle cx="12" cy="12" r="4"/><path d="M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-4 8"/>',
  userplus: '<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0"/><path d="M19 8v6M16 11h6"/>',
  tag: '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8" r="1.4"/>',
};
const ic = (n, c, s, f = 'none') => `<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="${f}" stroke="${c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">${ICON[n]}</svg>`;
const AV = 'linear-gradient(160deg,#939497,#414347)';
const bars = (a, b) => `<div style="display:flex;flex-direction:column;gap:14px"><div class="bar" style="width:${a}px;height:16px;background:#939497"></div><div class="bar" style="width:${b}px;height:14px;background:#414347"></div></div>`;
const brand = s => `<div style="width:${s}px;height:${s}px;border-radius:${s * .28}px;background:#29292B;flex:none;display:flex;align-items:center;justify-content:center">${ic('tag', '#414347', s * .45)}</div>`;
const face = (s, g = AV) => `<div style="width:${s}px;height:${s}px;border-radius:999px;background:${g};flex:none"></div>`;
const at = (x, y, w, h, extra = '') => `position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;${extra}`;

window.CUT = {
  width: W, height: H, fps: 30, duration: D, background: '#111111',
  chapters: [
    { t: 0, label: 'Push has hit a ceiling' }, { t: 4, label: 'Half never opt in' },
    { t: 9, label: 'The OS decides' }, { t: 13.5, label: 'People get through' },
    { t: 18.5, label: 'Community and retention' }, { t: 25, label: 'Build for people' },
  ],
  async init(kit) {
    kit.css(`
      #w{position:absolute;inset:0;overflow:hidden;background:#111111;font-family:figtree,Arial,sans-serif;color:#fff}
      #cam{position:absolute;left:0;top:0;width:10px;height:10px;transform-origin:0 0}
      .bar{border-radius:999px}
      .card{position:absolute;box-sizing:border-box;border-radius:44px;background:#202022;border:2px solid #29292B;display:flex;align-items:center;gap:28px;padding:0 36px}
      .mono{font-family:geist-mono,ui-monospace,monospace}
      .tx{position:absolute;font-weight:600;letter-spacing:-0.025em;line-height:1.02;white-space:nowrap}
      .w{display:inline-block;margin-right:.24em}
      .ann{position:absolute;font-size:36px;color:#D0D0D1;white-space:nowrap;padding:8px 16px;border-radius:12px;background:rgba(17,17,17,.82);border:2px solid #29292B}
      .src{position:absolute;left:90px;top:1420px;font-size:28px;color:#B3B3B3;padding:14px 22px;border-radius:14px;background:rgba(17,17,17,.88);border:2px solid #343437;white-space:nowrap}
      .scrim{position:absolute;left:0;width:1080px;pointer-events:none}
    `);
    // phone + pile
    let pile = '';
    HTS.forEach((h, i) => {
      const lab = i === 7 ? '<span style="font-size:40px;font-weight:500;color:#939497">We miss you</span>' : i === 5 ? '<span style="font-size:36px;font-weight:500;color:#414347">Last chance</span>' : bars(240 + i * 12, 380);
      pile += `<div id="p${i}" class="card" style="left:${PH.x + 70}px;top:${NTOP[i]}px;width:760px;height:${h}px;${h < 96 ? 'padding:0;background:#1A1A1A;border-radius:' + Math.min(44, h / 2) + 'px' : ''}">${h >= 96 ? brand(70) + lab : ''}</div>`;
    });
    const phone = `<div style="${at(PH.x, PH.y, PH.w, PH.h, 'box-sizing:border-box;border-radius:130px;background:#1A1A1A;border:3px solid #343437')}"></div>
      <div style="${at(PH.x + 300, PH.y + 120, 300, 22, 'border-radius:999px;background:#29292B')}"></div>
      <div style="${at(PH.x + 240, PH.y + 210, 420, 120, 'border-radius:28px;background:#1A1A1A')}"></div>
      <div id="ceil" style="${at(0, CEIL, 1080, 0, 'border-top:5px dashed #666666;transform-origin:0 0')}"></div>${pile}`;
    // report document
    const para = (y, ws) => `<div style="position:absolute;left:70px;top:${y}px;display:flex;flex-direction:column;gap:18px">${ws.map(w => `<div class="bar" style="width:${w}px;height:16px;background:#343437"></div>`).join('')}</div>`;
    const hl = (id, y, txt) => `<div style="position:absolute;left:60px;top:${y - 10}px;height:76px;display:flex;align-items:center;padding:0 16px">
        <div id="${id}bg" style="position:absolute;inset:0;border-radius:10px;background:#3B41EC;transform-origin:0 50%"></div>
        <span id="${id}tx" style="position:relative;font-size:38px;font-weight:600;white-space:nowrap">${txt}</span></div>`;
    const doc = `<div style="${at(DOC.x, DOC.y, DOC.w, DOC.h, 'box-sizing:border-box;border-radius:28px;background:#1A1A1A;border:2px solid #29292B;transform:rotate(-3deg)')}">
      <div class="mono" style="position:absolute;left:70px;top:70px;font-size:26px;color:#939497">PUSH NOTIFICATION BENCHMARKS · 2026</div>
      <div class="bar" style="position:absolute;left:70px;top:140px;width:640px;height:34px;background:#939497"></div>
      ${para(240, [820, 780, 840, 520])}${hl('h1', 470, 'Median opt-in: 53.3% Android, 48.85% iOS')}
      ${para(600, [800, 840, 760, 820, 600, 810, 420])}${hl('h2', 1010, 'iOS opens: down 13.71% year over year')}
      ${para(1140, [820, 760, 800, 500])}</div>`;
    // sorting plane
    const PERSON = new Set([0, 3, 4, 7, 9, 10]);
    let tiles = '';
    for (let i = 0; i < 12; i++) {
      const per = PERSON.has(i);
      tiles += `<div id="t${i}" class="card" style="left:0;top:0;width:420px;height:150px;padding:0 26px;gap:20px;border-radius:36px">${per ? face(84) : brand(84)}${bars(150 + (i % 3) * 30, 220)}</div>`;
    }
    const plane = `<div id="planeWrap" style="${at(PL.x, PL.y, 1080, 1920, 'perspective:1700px')}">
      <div id="plane" style="${at(90, 340, 900, 1240, 'transform:rotateX(48deg) rotateZ(-10deg);transform-style:preserve-3d')}">
        <div style="${at(470, 700, 430, 520, 'border-radius:40px;background:#1A1A1A;border:2px dashed #343437;box-sizing:border-box')}"></div>
        <div class="mono" style="position:absolute;left:500px;top:640px;font-size:34px;color:#939497">SILENCED</div>
        ${tiles}</div></div>`;
    // hero + follow-ups
    const hero = `<div id="hero" class="card" style="left:${HERO.x}px;top:${HERO.y}px;width:${HERO.w}px;height:${HERO.h}px;border-color:#343437;background:#202022;transform-origin:50% 100%">
        ${face(112)}<div style="display:flex;flex-direction:column;gap:6px"><span style="font-size:48px;font-weight:600;white-space:nowrap">Ana <span style="font-weight:500;color:#B3B3B3">replied to</span></span><span id="yc" style="font-size:48px;font-weight:500;color:#B3B3B3">your comment</span></div>
        <div style="margin-left:auto;width:36px;height:36px;border-radius:999px;background:#3B41EC;flex:none"></div></div>
      <div id="ring" style="${at(HERO.x, HERO.y, HERO.w, HERO.h, 'box-sizing:border-box;border-radius:44px;border:5px solid #6F89FC;opacity:0')}"></div>
      <div id="f1" class="card" style="left:${HERO.x}px;top:${HERO.y + 280}px;width:${HERO.w}px;height:140px"><div style="width:84px;height:84px;border-radius:999px;background:#29292B;display:flex;align-items:center;justify-content:center;flex:none">${ic('at', '#B3B3B3', 42)}</div>${bars(300, 420)}</div>
      <div id="f2" class="card" style="left:${HERO.x}px;top:${HERO.y + 440}px;width:${HERO.w}px;height:140px"><div style="width:84px;height:84px;border-radius:999px;background:#29292B;display:flex;align-items:center;justify-content:center;flex:none">${ic('userplus', '#B3B3B3', 42)}</div>${bars(260, 380)}</div>`;
    // network
    let lines = '', posts = '';
    NET.forEach(([dx, dy], i) => {
      const x = HC.x + dx, y = HC.y + dy;
      lines += `<line id="ln${i}" x1="${HC.x}" y1="${HC.y}" x2="${x}" y2="${y}" stroke="#343437" stroke-width="5" stroke-dasharray="2 18" stroke-linecap="round"/>`;
      if (i > 0) { const [px, py] = NET[i - 1]; lines += `<line id="lm${i}" x1="${HC.x + px}" y1="${HC.y + py}" x2="${x}" y2="${y}" stroke="#29292B" stroke-width="4"/>`; }
      posts += `<div id="n${i}" style="${at(x - 380, y - 230, 760, 460, 'box-sizing:border-box;border-radius:48px;background:#202022;border:2px solid #343437;padding:44px;display:flex;flex-direction:column;gap:26px')}">
        <div style="display:flex;align-items:center;gap:20px">${face(84)}${bars(200, 120)}</div>
        <div class="bar" style="width:${520 + (i % 3) * 40}px;height:18px;background:#414347"></div>
        <div style="display:flex;gap:14px;margin-top:auto"><div id="nr${i}" style="height:72px;padding:0 24px;border-radius:999px;background:#29292B;display:flex;align-items:center;gap:12px">${ic('heart', '#B3B3B3', 34, '#B3B3B3')}<div class="bar" style="width:40px;height:14px;background:#939497"></div></div>
        <div id="nc${i}" style="height:72px;padding:0 24px;border-radius:999px;background:#29292B;display:flex;align-items:center;gap:12px">${ic('bubble', '#B3B3B3', 34)}<div class="bar" style="width:30px;height:14px;background:#939497"></div></div></div></div>`;
    });
    const net = `<svg id="netsvg" width="6000" height="6000" style="position:absolute;left:0;top:0;overflow:visible">${lines}</svg>${posts}`;

    const root = kit.h(`<div id="w">
      <div id="glow" style="position:absolute;inset:0"></div>
      <div id="cam"><div id="worldA">${phone}</div><div id="worldB">${doc}</div><div id="worldC">${plane}</div><div id="worldN">${net}</div><div id="worldD">${hero}</div></div>
      <div id="scrimB" class="scrim" style="top:1000px;height:920px;background:linear-gradient(180deg,rgba(17,17,17,0) 0%,rgba(17,17,17,.9) 22%,rgba(17,17,17,.94) 100%)"></div>
      <div id="T1a" class="tx" style="font-size:150px">Push</div>
      <div id="T1b" class="tx" style="font-size:96px">has hit a ceiling.</div>
      <div id="T2a" class="tx" style="font-size:100px;line-height:1.06;white-space:normal;width:860px">Half your users never opt in.</div>
      <div id="T2b" class="tx" style="font-size:100px;line-height:1.06;white-space:normal;width:860px">The rest open less.</div>
      <div id="T3" class="tx" style="font-size:118px;line-height:1.02;text-align:right;white-space:normal;width:900px">The OS decides what gets through.</div>
      <svg id="annsvg" width="${W}" height="${H}" style="position:absolute;left:0;top:0;overflow:visible"><path id="a1p" fill="none" stroke="#D0D0D1" stroke-width="3"/><path id="a2p" fill="none" stroke="#D0D0D1" stroke-width="3"/><circle id="a1c" r="9" fill="#D0D0D1"/><circle id="a2c" r="9" fill="#D0D0D1"/></svg>
      <div id="A1" class="ann mono">a person</div>
      <div id="A2" class="ann mono">about you</div>
      <div id="T4" class="tx" style="font-size:124px;line-height:1.02;white-space:normal;width:900px">People get through.</div>
      <div id="T5" class="tx" style="font-size:200px;transform-origin:0 100%">+10–35%</div>
      <div id="T5c" class="tx" style="font-size:52px;font-weight:500;color:#D0D0D1">retention with community</div>
      <div id="S1" class="mono src">Source: Airship push benchmarks 2026</div>
      <div id="S5" class="mono src">Source: social.plus platform data</div>
      <div id="end" style="position:absolute;inset:0">
        <div id="E1" class="tx" style="left:90px;top:560px;font-size:170px;white-space:normal;width:900px">Build for people.</div>
        <div id="EU" style="position:absolute;left:96px;top:940px;width:610px;height:20px;border-radius:999px;background:#3B41EC;transform-origin:0 50%"></div>
        <div id="E2" class="tx" style="left:90px;top:1220px;font-size:66px;letter-spacing:-0.02em">social.plus</div>
      </div>
      <div style="position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse 760px 1200px at 540px 960px, rgba(0,0,0,0) 55%, rgba(0,0,0,.72) 100%)"></div>
    </div>`);
    kit.stage.appendChild(root);
    root.querySelectorAll('[id]').forEach(e => $[e.id] = e);
    ['T1b', 'T2a', 'T2b', 'T3', 'T4', 'E1'].forEach(id => {
      const words = $[id].textContent.split(' ');
      $[id].innerHTML = words.map(w => `<span class="w">${w}</span>`).join('');
      $[id].words = Array.from($[id].children);
    });
    const S = 512, tile = document.createElement('canvas'); tile.width = S; tile.height = S;
    const g = tile.getContext('2d'), img = g.createImageData(S, S), rnd = kit.rng(42);
    for (let i = 0; i < S * S; i++) {
      const n = (rnd() + rnd() + rnd() - 1.5) / 1.5, v = n > 0 ? 255 : 0;
      img.data[i * 4] = v; img.data[i * 4 + 1] = v; img.data[i * 4 + 2] = v; img.data[i * 4 + 3] = Math.min(255, Math.abs(n) * 255 * 0.15);
    }
    g.putImageData(img, 0, 0); pat = kit.fx.createPattern(tile, 'repeat');
  },

  render(t, kit) {
    const c = cam(t);
    $.cam.style.transform = `translate(${(W / 2 - c.cx * c.z).toFixed(2)}px,${(H / 2 - c.cy * c.z).toFixed(2)}px) scale(${c.z.toFixed(4)})`;
    const op = (el, v) => { el.style.opacity = cl(v).toFixed(3); el.style.visibility = v <= 0.001 ? 'hidden' : 'visible'; };
    const words = (el, t0, out, st = .08, dy = 50) => { const q = seg(t, out - .3, out); el.words.forEach((w, j) => { const p = eo(seg(t, t0 + j * st, t0 + j * st + .45)); w.style.opacity = (p * (1 - q)).toFixed(3); w.style.transform = `translateY(${((1 - p) * dy - q * 30).toFixed(1)}px)`; }); op(el, t > t0 - .1 && t < out ? 1 : 0); };
    const place = (el, x, y) => { el.style.left = x.toFixed(1) + 'px'; el.style.top = y.toFixed(1) + 'px'; };

    // ---- world visibility ----
    op($.worldA, 1 - seg(t, 4.3, 4.6));
    op($.worldB, seg(t, 3.9, 4.2) * (1 - seg(t, 9.2, 9.5)));
    op($.worldC, seg(t, 8.9, 9.2) * (1 - .8 * seg(t, 13.4, 14.0)) * (1 - seg(t, 18.6, 19.2)));
    op($.worldD, seg(t, 13.5, 13.7) * (1 - seg(t, 25.3, 25.6)));
    op($.worldN, seg(t, 18.7, 18.9) * (1 - seg(t, 24.9, 25.3)));

    // ---- A: the pile under the ceiling ----
    $.ceil.style.transform = `scaleX(${eio(seg(t, 1.9, 2.6)).toFixed(3)})`;
    HTS.forEach((h, i) => {
      if (i === 7) { $.p7.style.transform = `translateY(${(Math.sin(t * 2.2) * 2).toFixed(1)}px)`; return; }
      const tin = 1.6 + (6 - i) * .17, p = seg(t, tin, tin + .5);
      op($['p' + i], cl(p * 3));
      $['p' + i].style.transform = `translateY(${((1 - eob(p, 1.1)) * 1100).toFixed(1)}px)`;
    });
    // T1: "Push" big over the close-up, then label riding the ceiling line
    const pA = eo(seg(t, .25, .7));
    op($.T1a, pA * (1 - seg(t, 3.7, 4.0)));
    const [, ceilY] = proj(c, 0, CEIL);
    place($.T1a, 90, lerp(330, ceilY - 310, eio(seg(t, 1.6, 2.7))));
    $.T1a.style.transform = `translateY(${((1 - pA) * 60).toFixed(1)}px)`;
    words($.T1b, 2.55, 4.0, .07, 30); place($.T1b, 90, ceilY - 140);

    // ---- B: the report, highlighter marks ----
    const h1 = eio(seg(t, 4.9, 5.4)), h2 = eio(seg(t, 7.5, 8.0)), h1off = seg(t, 7.3, 7.6);
    $.h1bg.style.transform = `scaleX(${h1.toFixed(3)})`; $.h1bg.style.background = h1off > 0 ? `rgba(52,52,55,${(.4 + .6 * h1off).toFixed(2)})` : '#3B41EC';
    $.h1bg.style.opacity = (1 - h1off * .3).toFixed(3);
    $.h2bg.style.transform = `scaleX(${h2.toFixed(3)})`;
    $.h2tx.style.color = h2 > .5 ? '#FFFFFF' : '#666666'; $.h1tx.style.color = h1 > .5 ? '#FFFFFF' : '#666666';
    words($.T2a, 5.2, 7.4); place($.T2a, 90, 1160);
    words($.T2b, 7.9, 9.3); place($.T2b, 90, 1160);
    op($.S1, seg(t, 5.0, 5.4) * (1 - seg(t, 9.0, 9.3)));
    op($.scrimB, seg(t, 4.6, 5.0) * (1 - seg(t, 9.1, 9.4)) + seg(t, 21.0, 21.4) * (1 - seg(t, 24.6, 24.9)));

    // ---- C: the sorting plane ----
    const PERSON = [0, 3, 4, 7, 9, 10], PROMO = [1, 2, 5, 6, 8, 11];
    const ps = eio(seg(t, 10.3, 11.7));
    for (let i = 0; i < 12; i++) {
      const sx = (i % 2) * 470, sy = Math.floor(i / 2) * 190;
      let ex, ey, o = 1;
      const pi = PERSON.indexOf(i);
      if (pi >= 0) { ex = 0; ey = pi * 190; }
      else { const k = PROMO.indexOf(i); ex = 470 + k * 3; ey = 760 + k * 14; o = .9 - k * .1; }
      const lift = pi >= 0 ? Math.sin(ps * Math.PI) * -40 : 0;
      const el = $['t' + i];
      el.style.transform = `translate(${lerp(sx, ex, ps).toFixed(1)}px,${(lerp(sy, ey, ps) + lift).toFixed(1)}px)`;
      el.style.opacity = lerp(1, o, ps).toFixed(3);
      el.style.zIndex = pi >= 0 ? 20 : 10 - PROMO.indexOf(i);
    }
    $.plane.style.transform = `rotateX(${(48 + 3 * Math.sin(t * .8)).toFixed(2)}deg) rotateZ(${(-10 + 2 * seg(t, 9.3, 13.5)).toFixed(2)}deg)`;
    words($.T3, 9.75, 13.5, .07); place($.T3, 90, 250);

    // ---- D: the person ----
    const fl = eob(seg(t, 13.55, 14.3), 1.2);
    $.hero.style.transform = `perspective(1400px) rotateX(${((1 - fl) * 75).toFixed(2)}deg)`;
    const u = seg(t, 14.4, 15.6);
    op($.ring, t > 14.4 && t < 15.6 ? .85 * (1 - u) : 0);
    $.ring.style.transform = `scale(${(1 + .05 * eo(u)).toFixed(4)},${(1 + .2 * eo(u)).toFixed(4)})`;
    [['f1', 16.9], ['f2', 17.25]].forEach(([id, a]) => { const p = eo(seg(t, a, a + .45)); op($[id], p); $[id].style.transform = `translateY(${((1 - p) * 80).toFixed(1)}px)`; });
    // annotations (screen space, pinned to world points)
    const ann = (lab, path, dotEl, wx, wy, lx, ly, a, b) => {
      const [px, py] = proj(c, wx, wy);
      const p = eo(seg(t, a, a + .4)), q = seg(t, b - .3, b);
      const ex = lerp(px, lx + 40, p), ey = lerp(py, ly + 58, p);
      path.setAttribute('d', `M${px.toFixed(1)} ${py.toFixed(1)} Q ${((px + ex) / 2 - 30).toFixed(1)} ${((py + ey) / 2).toFixed(1)} ${ex.toFixed(1)} ${ey.toFixed(1)}`);
      dotEl.setAttribute('cx', px.toFixed(1)); dotEl.setAttribute('cy', py.toFixed(1));
      const v = p * (1 - q); path.style.opacity = dotEl.style.opacity = v.toFixed(3);
      op(lab, seg(t, a + .25, a + .5) * (1 - q)); place(lab, lx, ly);
    };
    ann($.A1, $.a1p, $.a1c, HERO.x + 92, HERO.y + 120, 90, 640, 15.0, 18.4);
    ann($.A2, $.a2p, $.a2c, HERO.x + 430, HERO.y + 176, 560, 640, 15.5, 18.4);
    words($.T4, 16.3, 18.6, .09); place($.T4, 90, 290);

    // ---- E: the network ----
    NET.forEach((_, i) => {
      const a = 18.9 + i * .16, p = seg(t, a, a + .45);
      op($['n' + i], cl(p * 2));
      $['n' + i].style.transform = `scale(${(.7 + .3 * eob(p, 1.6)).toFixed(3)})`;
      $['ln' + i].style.opacity = seg(t, a - .1, a + .3).toFixed(3);
      $['ln' + i].setAttribute('stroke-dashoffset', (-t * 40).toFixed(1));
      if ($['lm' + i]) $['lm' + i].style.opacity = (.8 * seg(t, a + .2, a + .6)).toFixed(3);
      const r = 20.6 + ((i * 5) % 8) * .3;
      ['nr', 'nc'].forEach((k, j) => { const q = seg(t, r + j * .2, r + j * .2 + .3); $[k + i].style.transform = `scale(${(q <= 0 ? 1 : 1 + .25 * Math.sin(q * Math.PI)).toFixed(3)})`; });
    });
    const sl = seg(t, 21.2, 21.55);
    op($.T5, sl * (1 - seg(t, 24.6, 24.9)));
    $.T5.style.transform = `rotate(-4deg) scale(${lerp(1.6, 1, eo(sl)).toFixed(3)})`;
    place($.T5, 84, 1000);
    op($.T5c, seg(t, 21.7, 22.1) * (1 - seg(t, 24.6, 24.9))); place($.T5c, 92, 1262);
    op($.S5, seg(t, 21.9, 22.3) * (1 - seg(t, 24.6, 24.9)));

    // ---- F: end ----
    op($.end, seg(t, 25.3, 25.6));
    words($.E1, 25.7, D + 1, .12, 60);
    $.EU.style.transform = `scaleX(${eio(seg(t, 26.7, 27.25)).toFixed(3)})`;
    const lp = eo(seg(t, 27.6, 28.1)); op($.E2, lp); $.E2.style.transform = `translateY(${((1 - lp) * 24).toFixed(1)}px)`;

    // glow sits under the one blue element of the moment
    let g = null;
    if (t > 4.9 && t < 9.3) { const L = t < 7.5 ? L1 : L2; g = proj(c, L.x + 430, L.y + 30); }
    else if (t > 13.6 && t < 25.3) g = proj(c, DOT.x, DOT.y);
    else if (t > 26.6) g = [420, 950];
    $.glow.style.background = g ? `radial-gradient(ellipse 520px 400px at ${g[0].toFixed(0)}px ${g[1].toFixed(0)}px, rgba(59,65,236,.4) 0%, rgba(59,65,236,0) 70%)` : 'none';

    // grain
    const fi = Math.floor(t * 12), r = kit.rng(fi + 1), ox = Math.floor(r() * 512), oy = Math.floor(r() * 512);
    const ctx = kit.fx; ctx.save(); ctx.translate(-ox, -oy); ctx.fillStyle = pat; ctx.fillRect(ox, oy, W, H); ctx.restore();
  },

  score(S) {
    // Foley only, quiet, leaving room for the voiceover.
    S.fx('pop', .3, { vel: 26 });
    S.fx('whoosh', 1.7, { dur: .9, vel: 20, into: 1 });
    for (let i = 6; i >= 0; i--) S.fx('pop', 1.6 + (6 - i) * .17 + .4, { vel: 16 + (6 - i) * 2, pitch: -6 + (6 - i) });
    S.fx('thud', 2.75, { vel: 32 });
    S.fx('whoosh', 3.95, { dur: .5, vel: 30 });
    S.fx('roll', 4.9, { dur: .5, vel: 18 });
    S.fx('whoosh', 6.75, { dur: .55, vel: 16 });
    S.fx('roll', 7.5, { dur: .5, vel: 18 });
    S.fx('whoosh', 8.95, { dur: .5, vel: 30 });
    S.fx('whoosh', 10.3, { dur: 1.4, vel: 18 });
    S.fx('thud', 11.7, { vel: 24 });
    S.fx('whoosh', 13.5, { dur: .8, vel: 20, into: 1 });
    S.fx('chime', 14.4, { vel: 34 });
    S.fx('click', 15.05, { vel: 20 }); S.fx('click', 15.55, { vel: 20 });
    S.fx('pop', 16.95, { vel: 20 }); S.fx('pop', 17.3, { vel: 20, pitch: 2 });
    S.fx('whoosh', 18.5, { dur: 1.6, vel: 22 });
    for (let i = 0; i < 8; i++) S.fx('pop', 18.9 + i * .16 + .1, { vel: 14 + i, pitch: i - 2 });
    S.fx('thud', 21.25, { vel: 40 });
    S.fx('revswell', 25.4, { dur: .9, vel: 24 });
    S.fx('ding', 26.75, { vel: 30 });
    S.fx('sparkle', 27.65, { vel: 20 });
    S.master({ gain: -8, fadeOut: .8 });
  },
};
