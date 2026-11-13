const { seg, eo, eio, eox } = kit;
// social.plus  x  customer, side by side, centred as one group on the frame's centre line.
// social.plus: the official logo for dark backgrounds (colour mark, white wordmark), inlined by
// build_film.py from the design system, never redrawn. The customer's white wordmark comes from
// modules/wordmark.html. The gap on each side of the x is the social.plus logo's clear space.
// The x draws first; both logos then slide out from behind it, each in its own mask.
const LOCK_SP = /*@SP_LOGO@*/'';
const LOCK = { spH: 64, gap: 64, x: 38, cy: 960 };
kit.scene('lockup', {
  init(kit) {
    const g = SP.geo(kit), L = Object.assign({}, LOCK, { cy: g.lockCy }), c = SP.cfg(kit).lockup, CX = g.W / 2, spW = L.spH * 2255.26 / 389.98, cw = c.wordmarkW, ch = c.wordmarkH;
    const x0 = CX - (spW + 2 * L.gap + L.x + cw) / 2, xc = x0 + spW + L.gap + L.x / 2;
    kit.stage.append(kit.h('<div class="ground"></div>'));
    this.glow = kit.h('<div class="glow" style="left:' + CX + 'px;top:' + L.cy + 'px"></div>');
    this.group = kit.h('<div style="position:absolute;inset:0;transform-origin:' + CX + 'px ' + L.cy + 'px"></div>');
    const spMask = kit.h('<div style="position:absolute;overflow:hidden;left:' + (x0 - 24) + 'px;top:' + (L.cy - 80) + 'px;width:' + (spW + 24) + 'px;height:160px"></div>');
    this.sp = kit.h('<div style="position:absolute;left:24px;top:' + (80 - L.spH / 2) + 'px;width:' + spW + 'px;height:' + L.spH + 'px">' + LOCK_SP + '</div>');
    spMask.append(this.sp);
    this.spW = spW;
    this.x = kit.h('<svg viewBox="0 0 40 40" style="position:absolute;overflow:visible;left:' + (xc - L.x / 2) + 'px;top:' + (L.cy - L.x / 2) + 'px;width:' + L.x + 'px;height:' + L.x + 'px">' +
      '<path d="M4 4 L36 36" pathLength="1" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" fill="none" stroke-dasharray="1 1"/>' +
      '<path d="M36 4 L4 36" pathLength="1" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" fill="none" stroke-dasharray="1 1"/></svg>');
    this.strokes = [...this.x.querySelectorAll('path')];
    const cmMask = kit.h('<div style="position:absolute;overflow:hidden;left:' + (xc + L.x / 2 + L.gap) + 'px;top:' + (L.cy - 80) + 'px;width:' + (cw + 24) + 'px;height:160px"></div>');
    this.cm = kit.h('<div style="position:absolute;left:0;top:' + (80 - ch / 2 + (c.wordmarkDy || 0)) + 'px;width:' + cw + 'px;height:' + ch + 'px">' + kit.module('wordmark.html') + '</div>');
    const svg = this.cm.querySelector('svg');
    if (svg) { svg.setAttribute('width', '100%'); svg.setAttribute('height', '100%'); svg.style.display = 'block'; }
    cmMask.append(this.cm);
    this.cw = cw;
    this.group.append(spMask, this.x, cmMask);
    kit.stage.append(this.glow, this.group);
  },
  render(t, kit) {
    const out = eio(seg(t, 2.95, 3.3));
    this.glow.style.opacity = 0.75 * eo(seg(t, 0, 0.7)) * (1 - out);
    this.glow.style.transform = 'scale(' + kit.breathe(t, 0.03, 3) + ')';
    this.strokes.forEach((el, i) => {
      el.style.strokeDashoffset = 1 - eo(seg(t, i * 0.1, 0.32 + i * 0.1));
    });
    // both logos slide out from behind the x, landing on the music's downbeat
    const p = eox(seg(t, 0.22, 1.15)), a = eo(seg(t, 0.22, 0.5));
    this.sp.style.transform = 'translateX(' + (1 - p) * (this.spW + 30) + 'px)';
    this.sp.style.opacity = a;
    this.cm.style.transform = 'translateX(' + -(1 - p) * (this.cw + 30) + 'px)';
    this.cm.style.opacity = a;
    // slow creep while it holds, then fade (to the quote, or the film's end)
    this.group.style.transform = 'scale(' + SP.geo(kit).S * (1 + 0.022 * seg(t, 0, 3.3)) + ')';
    this.group.style.opacity = 1 - (SP.cfg(kit).quote ? out : 0);
    if (!SP.cfg(kit).quote) this.glow.style.opacity = 0.75 * eo(seg(t, 0, 0.7));
  },
});
