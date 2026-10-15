// social.plus blog thumbnail — motion template (Motion artifact type, film with no scene list).
// Concept C of "Push Notifications Have Hit a Ceiling": wall of push pills + one social post with a blue Reply.
// To adapt: change the wall generator (texts, widths, unit markup) and the post markup; keep render() motion + grain.
const L = 6;
const W = 1578, H = 888;
let rows = [], post, glow, ring, btn, pat;

window.CUT = {
  width: W, height: H, fps: 30, duration: L, background: '#111111',
  chapters: [{ t: 0, label: 'Loop' }],
  async init(kit) {
    kit.css(`
      #w{position:absolute;inset:0;overflow:hidden;background:#111111;font-family:figtree,Arial,sans-serif}
      .row{position:absolute;left:0;height:64px;width:${W}px}
      .pill{position:absolute;top:0;height:64px;box-sizing:border-box;border-radius:32px;background:#1A1A1A;border:2px solid #202022;display:flex;align-items:center;gap:16px;padding:0 14px}
      .ic{width:38px;height:38px;border-radius:12px;background:#29292B;flex:none}
      .bar{height:10px;border-radius:5px;background:#29292B}
      .tx{font-size:24px;font-weight:500;color:#414347;white-space:nowrap}
      .layer{position:absolute;inset:0}
      .post{position:absolute;left:470px;top:330px;width:1300px;height:720px;box-sizing:border-box;border-radius:52px;background:#202022;border:2px solid #343437;padding:60px 64px;display:flex;flex-direction:column;gap:40px;box-shadow:0 40px 120px rgba(0,0,0,0.6)}
      .b{border-radius:11px}
    `);
    const texts = { '1-1': 'We miss you', '2-2': 'Your cart is waiting', '0-3': "Don't miss out", '4-0': 'Last chance' };
    const widths = [380, 300, 440, 340, 400, 320];
    let wall = '';
    for (let r = 0; r < 10; r++) {
      let x = (r % 2 === 0) ? -120 : -300;
      const dy = Math.abs(r - 2.5);
      const o = Math.max(0.25, 1 - dy * 0.12);
      let pills = '';
      for (let c = 0; x < 1700; c++) {
        let wd = widths[(r * 3 + c) % widths.length];
        const t = texts[r + '-' + c];
        if (t) wd = Math.max(wd, t.length * 13 + 90);
        const inner = t ? `<span class="tx">${kit.esc(t)}</span>` : `<div class="bar" style="width:${Math.max(60, wd - 130)}px"></div>`;
        pills += `<div class="pill" style="left:${x}px;width:${wd}px"><div class="ic"></div>${inner}</div>`;
        x += wd + 20;
      }
      wall += `<div class="row" style="top:${-30 + r * 92}px;opacity:${o}">${pills}</div>`;
    }
    const heart = '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#B3B3B3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/></svg>';
    const bubble = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-12.2 7.5L3 21l2-5.6A8.4 8.4 0 1 1 21 11.5z"/></svg>';
    const smile = '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#B3B3B3" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M8.5 14.5a4.5 4.5 0 0 0 7 0M9 9.5h.01M15 9.5h.01"/></svg>';
    const root = kit.h(`<div id="w">
      <div class="layer" id="wall">${wall}</div>
      <div class="layer" style="background:radial-gradient(ellipse 900px 520px at 1050px 640px, rgba(17,17,17,0.85) 0%, rgba(17,17,17,0) 75%)"></div>
      <div class="layer" id="glow" style="background:radial-gradient(ellipse 520px 360px at 820px 860px, rgba(59,65,236,0.45) 0%, rgba(59,65,236,0) 70%)"></div>
      <div class="post" id="post">
        <div style="display:flex;align-items:center;gap:28px">
          <div style="width:112px;height:112px;border-radius:999px;background:linear-gradient(160deg,#939497,#414347);border:4px solid #29292B;box-sizing:border-box;flex:none"></div>
          <div style="display:flex;flex-direction:column;gap:14px">
            <span style="font-size:52px;font-weight:600;letter-spacing:-0.015em;line-height:1.1;color:#FFFFFF">Emily Carter</span>
            <div style="width:170px;height:14px;border-radius:7px;background:#414347"></div>
          </div>
        </div>
        <div style="display:flex;flex-direction:column;gap:20px">
          <div class="b" style="width:900px;height:22px;background:#939497"></div>
          <div class="b" style="width:760px;height:22px;background:#939497"></div>
          <div class="b" style="width:520px;height:22px;background:#414347"></div>
        </div>
        <div style="display:flex;align-items:center;gap:16px;margin-top:12px">
          <div style="position:relative">
            <div id="ring" style="position:absolute;inset:0;border-radius:999px;border:3px solid #6F89FC;opacity:0"></div>
            <div id="btn" style="position:relative;height:80px;padding:0 40px 0 32px;border-radius:999px;background:#3B41EC;display:flex;align-items:center;gap:14px">${bubble}<span style="font-size:34px;font-weight:500;color:#FFFFFF">Reply</span></div>
          </div>
          <div style="height:80px;width:150px;border-radius:999px;background:#29292B;display:flex;align-items:center;justify-content:center;gap:14px">${heart}<div style="width:36px;height:12px;border-radius:6px;background:#414347"></div></div>
          <div style="height:80px;width:80px;border-radius:999px;background:#29292B;display:flex;align-items:center;justify-content:center">${smile}</div>
        </div>
      </div>
      <div class="layer" style="background:radial-gradient(ellipse 980px 620px at 789px 444px, rgba(0,0,0,0) 50%, rgba(0,0,0,0.75) 100%)"></div>
    </div>`);
    kit.stage.appendChild(root);
    rows = Array.from(root.querySelectorAll('.row'));
    post = root.querySelector('#post'); glow = root.querySelector('#glow');
    ring = root.querySelector('#ring'); btn = root.querySelector('#btn');

    // grain tile
    const S = 512, tile = document.createElement('canvas');
    tile.width = S; tile.height = S;
    const g = tile.getContext('2d'), img = g.createImageData(S, S), rnd = kit.rng(42);
    for (let i = 0; i < S * S; i++) {
      const n = (rnd() + rnd() + rnd() - 1.5) / 1.5;
      const a = Math.min(255, Math.abs(n) * 255 * 0.15);
      const v = n > 0 ? 255 : 0;
      img.data[i * 4] = v; img.data[i * 4 + 1] = v; img.data[i * 4 + 2] = v; img.data[i * 4 + 3] = a;
    }
    g.putImageData(img, 0, 0);
    pat = kit.fx.createPattern(tile, 'repeat');
  },
  render(t, kit) {
    const p = 2 * Math.PI * t / L;
    rows.forEach((el, r) => {
      const y = 7 * Math.sin(p + r * 0.55);
      const x = (r % 2 ? 1 : -1) * 14 * Math.sin(p + r * 1.1);
      el.style.transform = `translate(${x.toFixed(2)}px,${y.toFixed(2)}px)`;
    });
    post.style.transform = `translateY(${(-6 * Math.sin(p)).toFixed(2)}px)`;
    glow.style.opacity = (0.82 + 0.15 * Math.sin(p)).toFixed(3);

    const lt = t % 3;
    const u = kit.clamp01((lt - 0.35) / 1.5);
    const active = lt >= 0.35 && lt < 1.85;
    ring.style.opacity = active ? (0.7 * (1 - u)).toFixed(3) : '0';
    ring.style.transform = `scale(${(1 + 0.32 * kit.eo(u)).toFixed(4)})`;
    const bump = Math.exp(-Math.pow((lt - 0.35) / 0.16, 2));
    btn.style.transform = `scale(${(1 + 0.035 * bump).toFixed(4)})`;

    const GF = (typeof window !== 'undefined' && window.GRAIN_FPS) || 12; // grain boils per second
    const fi = Math.floor(t * GF) % (GF * L);
    const r = kit.rng(fi + 1);
    const ox = Math.floor(r() * 512), oy = Math.floor(r() * 512);
    const ctx = kit.fx;
    ctx.save();
    ctx.translate(-ox, -oy);
    ctx.fillStyle = pat;
    ctx.fillRect(ox, oy, W, H);
    ctx.restore();
  }
};
