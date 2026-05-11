# social.plus Imagery Style

social.plus uses two distinct imagery modes: **product illustrations** for in-product and documentation contexts, and **photography** for marketing and campaign contexts. The two modes are never mixed in the same layout.

---

## Product Illustrations

Used in: feature sections, documentation, empty states, onboarding, product marketing pages.

### Style

**3D object-based.** Illustrations are rendered with depth, layering, and perspective — not flat or hand-drawn. Objects have weight and dimension. Think chip stacks, layered cards, floating UI panels.

**UI-metaphor driven.** Illustrations communicate product concepts through recognisable UI elements — toggles, cards, toolbars, icons, SDK logos — rather than abstract shapes or human figures.

**One concept per illustration.** Each piece communicates a single idea. No visual clutter. The composition is sparse and confident.

### Colour rules

- **Dark background always.** Illustration backgrounds use the elevation surface palette — `#111111`, `#1e1e1e`, or `#272727`. Never white or light backgrounds.
- **Blue is the sole accent colour.** Ultramarine (`#3B41EC`) and the brand blue range are the only colours that appear as accents in product illustrations. Pink, orange, and yellow do not appear — those are reserved for marketing gradients and the logo.
- **Greyscale supporting elements.** All secondary and background objects are rendered in muted dark greys. This creates clear focal hierarchy: one blue focal point, everything else recedes.
- **Soft blue glow.** The primary focal element carries a subtle luminous halo — a soft `glow-ultramarine` or `glow-blue` applied to the key object. Never harsh or neon.

### Shape and form

- **Generous border radius.** All containers, cards, and UI elements use large rounding (radius-4 to radius-6 range), consistent with the design system.
- **Layering and depth.** Multiple planes are stacked with perspective offsets to imply depth. Front elements are fully rendered; receding elements become more muted and smaller.
- **Icon-centric composition.** A Material Symbol or product icon often anchors the centre of the composition, rendered at large scale (40–48px optical size) inside a rounded dark container with a blue accent.

### What to avoid

- No human figures or faces in product illustrations
- No gradients other than blue tones (no pink/orange/yellow in illustration contexts)
- No white or light backgrounds
- No flat 2D icon sheets — always have dimension and depth
- No more than one accent colour per illustration

---

## Photography

Used in: marketing campaigns, landing page heroes, blog posts, social media, event materials.

### Subject matter

A mix of:
- **People in authentic collaboration** — diverse individuals working together, in conversation, or engaged with technology. Candid over staged. Real moments over stock-photo setups.
- **Technology environments** — developer workspaces, screens, infrastructure, abstract tech contexts.

### Treatment

- **Dark and high-contrast.** Photos should skew dark — underexposed backgrounds, strong subject lighting. Avoid bright, airy, or pastel photography.
- **Colour grading.** Apply a cool, slightly desaturated grade with a subtle blue shift in shadows. This keeps photography consistent with the dark-first brand palette.
- **Brand colour overlays.** When photography is used behind text or in hero sections, apply a dark overlay (`rgba(17,17,17,0.5–0.7)`) to ensure legibility and reinforce the dark brand aesthetic. Brand gradient overlays (blue) may be used for campaign moments.
- **Avoid warm tones.** Warm-graded, golden-hour, or heavily orange-tinted photography feels off-brand. Keep the palette cool and grounded.

### People guidelines

- Show **diverse, real-feeling people** — a range of ages, backgrounds, and roles
- Capture **moments of connection** — conversation, collaboration, shared focus
- Avoid **generic stock imagery** — no handshakes, forced smiles at cameras, or office clichés
- Subjects should feel **engaged and purposeful**, not posed

### What to avoid

- Bright, high-key, or light-background photography
- Warm colour grades (orange, yellow, golden tones)
- Generic stock photo clichés
- Photography in contexts where product illustrations are specified

---

## Decorative Visuals

Used in: hero section backgrounds, section dividers, empty states, loading screens.

Decorative visuals are abstract and use the brand palette directly:

- **Gradient abstracts** — Brand Blue or Brand Pink gradients rendered as soft, blurred shapes or noise textures on a dark background. Low opacity, never overwhelming the content above.
- **Geometric shapes** — Simple rounded rectangles and circles using brand colours at 5–15% opacity, layered to create subtle depth behind content.
- **Pure dark with subtle texture** — Fine grain noise or a very subtle dot grid on `#111111`. Used when no colour is appropriate (developer docs, data-heavy pages).

**Rule:** Decorative visuals always sit behind content and never compete with it. They provide atmosphere, not information.

---

## Summary: Which mode to use

| Context | Mode |
|---------|------|
| Feature section on product/marketing page | Product illustration |
| Documentation or help centre | Product illustration |
| Empty states and onboarding | Product illustration |
| Hero section of marketing page | Photography or gradient abstract |
| Blog post header | Photography |
| Section divider / background texture | Decorative visual |
| Email header | Gradient abstract or product illustration |
