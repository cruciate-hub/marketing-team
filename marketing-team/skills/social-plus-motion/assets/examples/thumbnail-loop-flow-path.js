const HTML = "<div id=\"w\" style=\"position:absolute;inset:0;overflow:hidden;background:#111111;font-family:figtree,Arial,sans-serif\">\n<div id=\"glow\" style=\"position:absolute;inset:0;background:radial-gradient(ellipse 520px 360px at 1360px 760px, rgba(59,65,236,0.42) 0%, rgba(59,65,236,0) 70%)\"></div>\n\n<svg aria-hidden=\"true\" width=\"1578\" height=\"888\" viewBox=\"0 0 1578 888\" style=\"position: absolute; left: 0; top: 0\">\n<path id=\"p1\" d=\"M380 300 C 470 420, 470 420, 600 430\" fill=\"none\" stroke=\"#414347\" stroke-width=\"5\" stroke-dasharray=\"4 16\" stroke-linecap=\"round\"></path>\n<path id=\"p2\" d=\"M1050 560 C 1110 640, 1090 690, 1160 720\" fill=\"none\" stroke=\"#414347\" stroke-width=\"5\" stroke-dasharray=\"4 16\" stroke-linecap=\"round\"></path>\n</svg>\n\n<div id=\"post\" style=\"position: absolute; left: -90px; top: -70px; width: 560px; height: 380px; box-sizing: border-box; border-radius: 40px; background: #1C1C1E; border: 2px solid #29292B; padding: 120px 48px 40px 140px; display: flex; flex-direction: column; gap: 22px; transform: rotate(-4deg)\">\n<div style=\"display: flex; align-items: center; gap: 18px\"><div style=\"width: 64px; height: 64px; border-radius: 999px; background: linear-gradient(160deg, #939497, #414347)\"></div><div style=\"width: 160px; height: 16px; border-radius: 8px; background: #939497\"></div></div>\n<div style=\"width: 300px; height: 16px; border-radius: 8px; background: #414347\"></div>\n<div style=\"display: flex; gap: 12px\"><div style=\"height: 50px; width: 104px; border-radius: 999px; background: #29292B; display: flex; align-items: center; justify-content: center\"><svg aria-hidden=\"true\" width=\"26\" height=\"26\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#B3B3B3\" stroke-width=\"2.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z\"/></svg></div><div style=\"height: 50px; width: 104px; border-radius: 999px; background: #29292B; display: flex; align-items: center; justify-content: center\"><svg aria-hidden=\"true\" width=\"26\" height=\"26\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#B3B3B3\" stroke-width=\"2.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M21 11.5a8.4 8.4 0 0 1-12.2 7.5L3 21l2-5.6A8.4 8.4 0 1 1 21 11.5z\"/></svg></div></div>\n</div>\n\n<div id=\"prod\" style=\"position: absolute; left: 560px; top: 170px; width: 520px; height: 600px; box-sizing: border-box; border-radius: 48px; background: #202022; border: 2px solid #343437; padding: 28px; display: flex; flex-direction: column; gap: 26px; box-shadow: 0 50px 140px rgba(0,0,0,0.65); transform: rotate(3deg)\">\n<div style=\"position: relative; height: 330px; flex: none; border-radius: 30px; background: linear-gradient(170deg, #29292B, #1A1A1A); overflow: hidden\">\n<div style=\"position: absolute; left: 120px; top: 60px; width: 240px; height: 240px; border-radius: 999px; background: radial-gradient(circle at 38% 32%, #4A4B50 0%, #29292B 60%, #1C1C1E 100%)\"></div>\n<div id=\"chip\" style=\"position: absolute; left: 22px; top: 22px; transform-origin: 30px 28px; display: flex; align-items: center; gap: 10px; height: 56px; padding: 0 18px 0 8px; border-radius: 999px; background: rgba(17,17,17,0.75)\"><div style=\"width: 40px; height: 40px; border-radius: 999px; background: linear-gradient(160deg, #939497, #414347)\"></div><div style=\"width: 80px; height: 12px; border-radius: 6px; background: #939497\"></div></div>\n</div>\n<div style=\"width: 340px; height: 24px; border-radius: 12px; background: #939497; margin-left: 8px\"></div>\n<div style=\"width: 150px; height: 24px; border-radius: 12px; background: #414347; margin-left: 8px\"></div>\n</div>\n\n<div style=\"position: absolute; left: 1090px; top: 690px; width: 620px; height: 140px\"><div id=\"ring\" style=\"position: absolute; inset: 0; border-radius: 999px; border: 4px solid #6F89FC; opacity: 0\"></div><div id=\"btn\" style=\"position: absolute; left: 0; top: 0; width: 620px; height: 140px; border-radius: 999px; background: #3B41EC; display: flex; align-items: center; gap: 24px; padding-left: 56px; box-sizing: border-box; box-shadow: 0 30px 80px rgba(59,65,236,0.3)\"><svg aria-hidden=\"true\" width=\"56\" height=\"56\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#FFFFFF\" stroke-width=\"2.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><circle cx=\"9\" cy=\"20\" r=\"1.5\"/><circle cx=\"18\" cy=\"20\" r=\"1.5\"/><path d=\"M2 3h3l2.6 12.2a2 2 0 0 0 2 1.6h8.6a2 2 0 0 0 2-1.5L22 8H6\"/></svg><span style=\"font-size: 52px; font-weight: 600; letter-spacing: -0.015em; color: #FFFFFF; white-space: nowrap\">Add to cart</span></div>\n</div>\n<div style=\"position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse 980px 620px at 789px 444px, rgba(0,0,0,0) 50%, rgba(0,0,0,0.75) 100%)\"></div>\n</div>";
// social.plus blog header loop — "E-commerce personalization & the role social features play", concept B (flow/path)
const L = 6, W = 1578, H = 888;
let el = {}, pat;
window.CUT = {
  width: W, height: H, fps: 30, duration: L, background: '#111111',
  chapters: [{ t: 0, label: 'Loop' }],
  async init(kit) {
    const root = kit.h(HTML);
    kit.stage.appendChild(root);
    ['glow','p1','p2','post','prod','chip','ring','btn'].forEach(id => el[id] = root.querySelector('#' + id));
    const S = 512, tile = document.createElement('canvas'); tile.width = S; tile.height = S;
    const g = tile.getContext('2d'), img = g.createImageData(S, S), rnd = kit.rng(42);
    for (let i = 0; i < S * S; i++) {
      const n = (rnd() + rnd() + rnd() - 1.5) / 1.5;
      const v = n > 0 ? 255 : 0;
      img.data[i*4] = v; img.data[i*4+1] = v; img.data[i*4+2] = v;
      img.data[i*4+3] = Math.min(255, Math.abs(n) * 255 * 0.15);
    }
    g.putImageData(img, 0, 0);
    pat = kit.fx.createPattern(tile, 'repeat');
  },
  render(t, kit) {
    const p = 2 * Math.PI * t / L;
    // dots travel along both paths toward the cart (6 dash periods per loop = seamless)
    const off = (-(t / L) * 120).toFixed(2);
    el.p1.setAttribute('stroke-dashoffset', off);
    el.p2.setAttribute('stroke-dashoffset', off);
    // cards float and tilt slightly
    el.post.style.transform = `rotate(${(-4 + 0.6 * Math.sin(p)).toFixed(3)}deg) translateY(${(5 * Math.sin(p + 1)).toFixed(2)}px)`;
    el.prod.style.transform = `rotate(${(3 + 0.5 * Math.sin(p + 2)).toFixed(3)}deg) translateY(${(-7 * Math.sin(p)).toFixed(2)}px)`;
    el.glow.style.opacity = (0.85 + 0.15 * Math.sin(p)).toFixed(3);
    // every 3 s: the friend chip pops, then the cart button is pressed and rings
    const lt = t % 3;
    const chipBump = Math.exp(-Math.pow((lt - 0.5) / 0.18, 2));
    el.chip.style.transform = `scale(${(1 + 0.08 * chipBump).toFixed(4)})`;
    const press = Math.exp(-Math.pow((lt - 1.4) / 0.16, 2));
    el.btn.style.transform = `scale(${(1 - 0.03 * press).toFixed(4)})`;
    const u = kit.clamp01((lt - 1.4) / 1.4);
    const on = lt >= 1.4 && lt < 2.8;
    el.ring.style.opacity = on ? (0.7 * (1 - u)).toFixed(3) : '0';
    el.ring.style.transform = `scale(${(1 + 0.12 * kit.eo(u)).toFixed(4)}, ${(1 + 0.4 * kit.eo(u)).toFixed(4)})`;
    // grain boils 12x per second (calibrated to match the static)
    const GF = (typeof window !== 'undefined' && window.GRAIN_FPS) || 12;
    const fi = Math.floor(t * GF) % (GF * L);
    const r = kit.rng(fi + 1), ox = Math.floor(r() * 512), oy = Math.floor(r() * 512);
    const ctx = kit.fx; ctx.save(); ctx.translate(-ox, -oy); ctx.fillStyle = pat; ctx.fillRect(ox, oy, W, H); ctx.restore();
  }
};
