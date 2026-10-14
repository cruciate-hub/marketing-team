# Treatments: when to use grain

Grain is not part of the core style. It is the **editorial treatment**: it signals "story, opinion, explainer". Clean (no grain) signals "product, brand, interface".

| Surface | Treatment | Notes |
|---|---|---|
| Blog headers and thumbnails | **Grain** | blog-thumbnails skill |
| Answer-page and glossary images | **Grain** | editorial content |
| Reels, shorts, carousels built from a blog post or in Vox/explainer style | **Grain** | social-plus-motion, explainer mode |
| Social posts quoting or promoting an article | **Grain** | |
| Website hero, feature and section illustrations | Clean | |
| Product/feature announcements, release visuals | Clean | |
| Ads (paid social, display) | Clean by default | grain only if the ad promotes a piece of editorial content |
| Sales/pitch decks, one-pagers, email headers | Clean | |
| Event and webinar graphics | Clean | unless built from an article |

If unsure, ask: "Is this telling a story from content, or presenting the product?" Story → grain. Product → clean.

## Grain specs (editorial)

- **Static**: grain covers background and foreground alike (two SVG `feTurbulence` layers: fractalNoise 0.7 / 3 octaves, `overlay`, opacity 0.9; fractalNoise 1.4 / 2 octaves, `soft-light`, ≈0.75). In `assets/shell.dc.html` set the `grain` prop default to 0.9.
- **Smaller exports**: grain is drawn at device pixels, so the same setting reads heavier on a small image. Scale it down with the width — strength × (width / design width)^0.75 (blog-thumbnails' export script does this).
- **Motion**: grain drawn on the fx canvas with alpha factor 0.15, boiling 12×/s (see social-plus-motion). Compare a frame with the static before delivering.
- Tried and rejected (October 2026): grain only behind the foreground, and a grainy spray-paint glow. Keep grain uniform over the whole image and the glow soft.

## Clean specs

Same everything, grain off. Without grain, add depth with the single soft drop shadow on the focal object and one-step tonal surfaces; keep the vignette.

## Sizes by surface

Blog: header 1578×888, grid thumbnail 724×408, mega-menu 502×283, all WebP with exact sizes (details in blog-thumbnails) · answer page 1240×840 · glossary 1578×888 · Instagram post 1080×1350 · Instagram/TikTok reel and story 1080×1920 · LinkedIn post 1200×1200 or 1200×627 · X/Twitter 1600×900 · OG image 1200×630. Website illustrations: ask for the slot size, or design at 2× of the container.
