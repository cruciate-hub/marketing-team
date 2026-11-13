const { seg, eo, TextFx } = kit;
// Optional closing card: one approved customer quote (never a placeholder in a finished film).
// who: "Name, Title\nCompany" (two lines).
kit.scene('quote', {
  init(kit) {
    const q = SP.cfg(kit).quote, g = SP.geo(kit), b = g.quote;
    kit.stage.append(kit.h('<div class="ground"></div>'));
    this.glow = kit.h('<div class="glow" style="left:' + g.W / 2 + 'px;top:' + g.quoteGlowY + 'px"></div>');
    const w = kit.h('<div class="words" style="left:' + b.left + 'px;top:' + b.top + 'px;width:' + b.width + 'px;gap:30px">' +
      '<div class="hero quote-mark" style="font-size:240px;line-height:.8;height:150px;color:var(--accent)">“</div>' +
      '<p class="hero quote-text" style="font-size:64px;line-height:1.25"></p>' +
      '<p class="sub quote-who" style="font-size:40px;white-space:pre-line"></p></div>');
    this.mark = w.querySelector('.quote-mark');
    this.text = w.querySelector('.quote-text');
    this.who = w.querySelector('.quote-who');
    this.text.textContent = q.text;
    this.who.textContent = q.who;
    // a long quote: smaller type so it stays inside the frame
    if (q.text.length > 140) this.text.style.fontSize = Math.max(48, 64 * Math.sqrt(140 / q.text.length)) + 'px';
    this.w = w; this.S = g.S;
    w.style.transformOrigin = '50% 0';
    kit.stage.append(this.glow, w);
  },
  render(t, kit) {
    this.glow.style.opacity = 0.45 * eo(seg(t, 0, 0.8));
    this.glow.style.transform = 'scale(' + kit.breathe(t, 0.03, 3.4) + ')';
    const m = eo(seg(t, 0, 0.5));
    this.mark.style.opacity = m;
    this.mark.style.transform = 'translateY(' + (1 - m) * 30 + 'px)';
    TextFx.fadeFromRight(this.text, t, 0.3, { stagger: 0.07, dur: 0.5, dx: 26 });
    const p = eo(seg(t, 1.9, 2.4));
    this.who.style.opacity = p;
    this.who.style.transform = 'translateY(' + (1 - p) * 20 + 'px)';
    this.w.style.transform = 'translateY(' + (-2 * t) + 'px) scale(' + this.S + ')';
  },
});
