const { seg, eo, eio, eob, lerp } = kit;
// The customer's app icon lands with "<Customer> is live / with social.plus" (or the film's own
// headline: "/" breaks the line, *word* is the accent word), pulses twice,
// then opens into the phone (app launch) onto the first feature's first frame.
kit.scene('intro', {
  init(kit) {
    const c = SP.cfg(kit), g = SP.geo(kit);
    kit.stage.append(kit.h('<div class="ground"></div>'));
    this.glow = kit.h('<div class="glow"></div>');
    this.r1 = kit.h('<div class="ring"></div>');
    this.r2 = kit.h('<div class="ring"></div>');
    this.frame = kit.h('<div class="phone" style="transform:none"></div>');
    this.tile = kit.h('<div class="tile"></div>');
    this.vid = kit.h('<img alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block">');
    this.vid.src = kit.assets.url(c.features[0].id + '-first.webp');
    this.icon = kit.h('<img alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block">');
    this.icon.src = kit.assets.url(c.icon);
    this.tile.append(this.vid, this.icon);
    const words = kit.h('<div class="words" style="left:' + g.words.left + 'px;top:' + (g.introY + g.introIcon / 2 + 80 * g.S) + 'px;width:' + g.words.width + 'px;gap:8px"></div>');
    const head = c.headline || (c.customer + ' is *live* / with social.plus');
    const lines = head.split('/').map((l) => l.trim().split(/\s+/));
    this.w = [];
    const hs = lines.map((line) => {
      const h = kit.h('<h2 class="hero" style="white-space:nowrap"></h2>');
      line.forEach((s, i) => {
        const sp = kit.h('<span style="display:inline-block"></span>');
        const hl = /^\*.+\*$/.test(s);
        sp.textContent = hl ? s.slice(1, -1) : s;
        if (hl) sp.className = 'hl';
        if (i) h.append(' ');
        h.append(sp); this.w.push(sp);
      });
      words.append(h);
      return h;
    });
    kit.stage.append(this.glow, this.r1, this.r2, this.frame, this.tile, words);
    // a long name: shrink the headline to fit
    const widest = Math.max.apply(null, hs.map((h) => h.offsetWidth)), fit = g.words.width;
    if (widest > fit) hs.forEach((h) => { h.style.fontSize = (g.hero * fit / widest) + 'px'; });
  },
  render(t, kit) {
    const G = SP.geo(kit), INTRO_ICON = G.introIcon, INTRO_R = G.introR, INTRO_Y = G.introY;
    const m = eio(seg(t, 3.0, 4.2)); // app launch: icon -> phone screen
    const ga = eo(seg(t, -0.6, 1.0)) * (0.82 + 0.18 * Math.sin(t * 3.2)) * (1 - 0.35 * m);
    this.glow.style.opacity = ga;
    this.glow.style.top = lerp(INTRO_Y, G.glowY, m) + 'px';
    this.glow.style.left = lerp(G.W / 2, G.CX, m) + 'px';
    this.glow.style.transform = 'scale(' + (1 + 0.05 * Math.sin(t * 2.2) + 0.12 * m) + ')';
    // two soft "live" pulses in the icon's own squircle shape
    [[this.r1, 1.3], [this.r2, 1.9]].forEach(([el, t0]) => {
      const p = seg(t, t0, t0 + 1.4);
      const d = 170 * G.S * eo(p), sz = INTRO_ICON + 2 * d;
      el.style.cssText = 'left:' + (G.W / 2 - sz / 2) + 'px;top:' + (INTRO_Y - sz / 2) + 'px;width:' + sz + 'px;height:' + sz +
        'px;border-radius:' + (INTRO_R + 0.9 * d) + 'px;opacity:' + (p > 0 && p < 1 ? (1 - p) * 0.45 : 0);
    });
    // icon lands with a small settle, then grows into the phone screen
    const a = seg(t, -0.6, 0.45);
    const sc = 0.9 + 0.1 * eob(a, 1.5);
    const w = lerp(INTRO_ICON * sc, G.SW, m), h = lerp(INTRO_ICON * sc, G.SH, m);
    const cy = lerp(INTRO_Y, G.ST + G.SH / 2, m), r = lerp(INTRO_R * sc, G.SR, m);
    const x = lerp(G.W / 2, G.CX, m) - w / 2, y = cy - h / 2;
    const ts = this.tile.style;
    ts.left = x + 'px'; ts.top = y + 'px'; ts.width = w + 'px'; ts.height = h + 'px';
    ts.borderRadius = r + 'px'; ts.opacity = eo(a);
    const ba = eio(seg(m, 0.45, 1)), b = G.PB * ba;
    ts.boxShadow = '0 30px 90px rgba(0,0,0,' + (0.5 * (1 - ba)) + ')';
    this.icon.style.opacity = 1 - eio(seg(m, 0, 0.45));
    this.vid.style.opacity = eio(seg(m, 0.3, 0.8));
    const fs = this.frame.style;
    fs.left = (x - b) + 'px'; fs.top = (y - b) + 'px'; fs.width = (w + 2 * b) + 'px'; fs.height = (h + 2 * b) + 'px';
    fs.borderRadius = (r + b) + 'px'; fs.opacity = ba;
    // headline word by word from below; leaves upward before the launch
    const out = eio(seg(t, 2.8, 3.15));
    this.w.forEach((el, i) => {
      const p = eo(seg(t, 0.35 + i * 0.11, 0.85 + i * 0.11));
      el.style.opacity = p * (1 - out);
      el.style.transform = 'translateY(' + ((1 - p) * 34 - out * 24) + 'px)';
    });
  },
});
