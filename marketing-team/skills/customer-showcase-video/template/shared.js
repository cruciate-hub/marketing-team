// customer-showcase-video template. Fixed: never edit per customer. Everything that changes
// lives in modules/showcase.json (written by scripts/build_film.py).
window.SP = {
  // Stage 1080 x 1920. The feature label and the phone sit as one block centred vertically:
  // label 239-383, phone 435-1681, screen 560 x 1214 at (260, 451).
  // 16:9 (aspect "16:9" in showcase.json; base-wide.css overrides the CSS to match): stage 1920 x 1080,
  // the reel's layout scaled by S = 2/3 and centred, so the wider frame only adds space at the sides:
  // label 59-155, phone 190-1021, screen 373 x 809 at (774, 201).
  G: { SW: 560, SH: 1214, PT: 435, PH: 1246, CY: 1058, ST: 451 },
  geo(kit) {
    if (SP._g) return SP._g;
    const wide = SP.cfg(kit).aspect === '16:9';
    return (SP._g = wide
      ? { wide, S: 2 / 3, W: 1920, H: 1080, SW: 373, SH: 809, ST: 201, SR: 35, PB: 11, CX: 960, glowY: 633,
          introY: 405, introIcon: 200, introR: 45, hero: 64, words: { left: 660, width: 600 }, lockCy: 540,
          quote: { left: 540, top: 234, width: 840 }, quoteGlowY: 451 }
      : { wide, S: 1, W: 1080, H: 1920, SW: 560, SH: 1214, ST: 451, SR: 53, PB: 16, CX: 540, glowY: 1100,
          introY: 808, introIcon: 300, introR: 67, hero: 96, words: { left: 90, width: 900 }, lockCy: 960,
          quote: { left: 120, top: 500, width: 840 }, quoteGlowY: 820 });
  },

  cfg(kit) { return SP._c || (SP._c = kit.json('showcase.json')); },
  feat(kit, id) { return SP.cfg(kit).features.find((f) => f.id === id); },

  // The flat front-on phone playing one feature's clip; same place in every scene.
  phone(kit, clip, start) {
    const phone = kit.h('<div class="phone"><div class="screen"></div></div>');
    const screen = phone.querySelector('.screen');
    const video = kit.video(clip, { start: start || 0 });
    screen.append(video);
    kit.stage.append(phone);
    return { phone, screen, video };
  },

  // A held screen as a picture, laid exactly like a clip (pictures always export; held clips may not).
  still(kit, name) {
    const g = SP.geo(kit);
    const img = kit.h('<img alt="" style="position:absolute;left:0;top:0;width:' + g.SW + 'px;height:' + g.SH + 'px;object-fit:cover;display:block">');
    img.src = kit.assets.url(name);
    return img;
  },

  // Feature title and one benefit line, directly above the phone.
  label(kit, title, sub) {
    const w = kit.h('<div class="words label"><h2 class="line"></h2><p class="sub"></p></div>');
    w.firstChild.textContent = title; w.lastChild.textContent = sub;
    kit.stage.append(w);
    return w;
  },

  // The highlight: everything on the screen except one part dims for about a second.
  spot(kit, screen) {
    const el = kit.h('<div style="position:absolute;pointer-events:none;display:none"></div>');
    screen.append(el);
    return el;
  },
  // r = [x, y, w, h, radius] in clip pixels; k = screen px per clip px. In 0.3 s, held 0.9 s, out 0.3 s.
  focus(kit, el, t, t0, r, k) {
    const { seg, eo, eio } = kit;
    const a = eio(seg(t, t0, t0 + 0.3)) * (1 - eio(seg(t, t0 + 1.2, t0 + 1.5)));
    el.style.display = a > 0 ? 'block' : 'none';
    if (!(a > 0)) return;
    const pad = 6 + 12 * (1 - eo(seg(t, t0, t0 + 0.6)));
    el.style.left = (r[0] * k - pad) + 'px';
    el.style.top = (r[1] * k - pad) + 'px';
    el.style.width = (r[2] * k + 2 * pad) + 'px';
    el.style.height = (r[3] * k + 2 * pad) + 'px';
    el.style.borderRadius = (r[4] * k + pad) + 'px';
    el.style.boxShadow = '0 0 0 1800px rgba(0,0,0,' + (0.55 * a).toFixed(3) + ')';
  },

  // One feature scene. The first comes out of the app-launch; each later one slides in over the
  // previous feature's last frame; the last fades out in place before the logos.
  feature(id) {
    return {
      init(kit) {
        const c = SP.cfg(kit), i = c.features.findIndex((f) => f.id === id), f = c.features[i];
        this.f = f; this.i = i; this.last = i === c.features.length - 1;
        kit.stage.append(kit.h('<div class="ground"></div>'));
        const g = SP.geo(kit);
        this.glow = kit.h('<div class="glow" style="left:' + g.CX + 'px;top:' + g.glowY + 'px"></div>');
        kit.stage.append(this.glow);
        this.p = SP.phone(kit, f.clip, -(f.trim || 0));
        if (i > 0) { this.prev = SP.still(kit, c.features[i - 1].id + '-last.webp'); this.p.screen.prepend(this.prev); }
        this.spot = SP.spot(kit, this.p.screen);
        this.label = SP.label(kit, f.title, f.line);
        this.kids = [...this.label.children];
      },
      render(t, kit) {
        const { seg, eo, eio } = kit, f = this.f, D = kit.dur, W = SP.geo(kit).SW, T = kit.start + t;
        const fade = this.last ? eio(seg(t, D - 1.1, D - 0.1)) : 0;
        this.glow.style.opacity = (0.65 + 0.08 * Math.sin(T * 1.1)) * (1 - fade);
        this.glow.style.transform = 'scale(1.12)';
        if (f.focus) SP.focus(kit, this.spot, t, f.focus.t, f.focus.rect, W / (f.clipW || 392));
        this.p.phone.style.opacity = 1 - fade;
        if (this.prev) {
          const s = eio(seg(t, 0, 0.45));
          this.prev.style.left = (-W * s) + 'px';
          this.prev.style.opacity = s < 1 ? 1 : 0;
          this.p.video.style.left = (W * (1 - s)) + 'px';
        }
        // title, then benefit line, from below; quick exit before the next scene
        const out = this.last ? eio(seg(t, D - 1.4, D - 1.1)) : eio(seg(t, D - 0.35, D - 0.05));
        const d0 = this.i === 0 ? 0 : 0.3;
        this.kids.forEach((el, k) => {
          const p = eo(seg(t, d0 + k * 0.15, d0 + 0.45 + k * 0.15));
          el.style.opacity = p * (1 - out);
          el.style.transform = 'translateY(' + ((1 - p) * 28 - out * 16) + 'px)';
        });
      },
    };
  },
};
