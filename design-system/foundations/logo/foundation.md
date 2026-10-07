# Logo

The social.plus logo: full logo (icon mark + wordmark) and icon mark, in colour and in monochrome, with the clear-space rule and the backgrounds it may sit on. The vector data is below so HTML can embed it inline; the colour files are `assets/social-plus-logo.svg` and `assets/social-plus-icon.svg` at the repository root (`$MT_REPO/assets/`, not under `design-system/`). The white and black mono sets are not in the repository (TO CHECK: Figma or the brand kit); until then make them from the inline SVG as described below.

- Status: draft (2026-10-07), moved from the former `design-system/logo.md` (brand guidelines) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: the official logo files (`$MT_REPO/assets/social-plus-logo.svg`, `assets/social-plus-icon.svg`) and the brand guidelines; on the live site the nav and footer show the logo as a CDN image in a `.nav-logo_img` box of 10.5rem × 2.5rem (9.5rem wide on phones) and a `.logo-footer` box of 10rem × 2.5rem (captured CSS, G1 and G5)
- Preview: preview.html (hand-made, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Not produced by capture/: the preview is written by hand and survives re-runs

## The mark

Intersecting rounded shapes reveal a plus sign and a chat bubble: connection at the centre of the platform. The warm arm (pink to orange to yellow) and the blue arm (medium blue to main blue to light blue) meet in a navy centre (`#27265E`, the same value as `--social--button-pressed`). The gradient stops of the mark are part of the artwork, not website tokens: the orange in the mark is `#F66005` while the site's `--secondary--orange` is `#FF6937`.

## Variants

| Variant | Use |
|---|---|
| Full logo, colour, white wordmark | Default on dark pages and dark sections |
| Full logo, colour, dark wordmark (`#111`) | Light backgrounds: white, `--main--whitesmoke`, `--social--grey-background` |
| Full logo, white mono | Dark photography, gradients, busy or saturated backgrounds, single-ink print |
| Full logo, black mono | Light photography (or the colour logo, tested for legibility), light single-ink print, embossing, watermarks |
| Icon mark (colour, white, black) | Favicons, profile pictures, app icons, layouts too tight for the full logo |

## Rules

- Clear space: the height of the icon mark (x) on all four sides. Nothing enters that zone.
- Minimum size: TO CHECK (the former brand file set none; the smallest live use is the 2.5rem = 40px nav box). Until decided, do not set the full logo smaller than the nav shows it.
- When the layout is tight, switch to the icon mark; never shrink the full logo below its minimum.
- Never on `--social--main-blue` (#3B41EC): the blue arm disappears and the navy centre loses its shape. Approved backgrounds: `--social--dark` and the dark surfaces, white and the light greys, photography with the mono logo.
- Light photography: black mono or the colour logo, tested for legibility; dark photography: white mono. On any dark or saturated background, the white mono logo.
- Monochrome is for single-ink print, embossing and engraving, watermarks, and wherever colour reproduction is not reliable.
- Never stretch, rotate, recolour, redraw, add a shadow or a glow, or change the colour arrangement. Use the files, never a low-resolution copy (the live nav does, see Known inconsistencies).
- Co-branding: full logo next to the partner's full logo, or mark next to mark; equal visual weight, clear separation, no overlap. The partnership templates are in Figma.
- In writing the name is always `social.plus`, lowercase, also at the start of a sentence and in title-case headings; never Social.Plus, Social Plus, social plus or SocialPlus (see `messaging/terminology.md`).

## On the website

The website (dark) uses the full logo in colour with the **white** wordmark: `assets/media/66fe6169153dc88a03557da6_29a5aaff9e31043f2175762ac854a9e5_logo.svg`, as the nav (G1) and the footer (G5) show it. Use that file as it is; never the `#111` wordmark on a dark page. A logo that renders black on a dark page is a bug: the file lost its colours (see Known inconsistencies).

## Inline SVG

Full logo, colour. The wordmark paths use `fill="#111"` (light backgrounds); use `fill="#ffffff"` on dark backgrounds. Rename the gradient ids when two logos share a page.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2255.26 389.98">
  <defs>
    <linearGradient id="sp-g1" x1="125.8" y1="60.75" x2="307.71" y2="270.34" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#f568f0"/>
      <stop offset=".516" stop-color="#f66005"/>
      <stop offset="1" stop-color="#f7c506"/>
    </linearGradient>
    <linearGradient id="sp-g2" x1="62.83" y1="116.6" x2="247.38" y2="334.1" gradientUnits="userSpaceOnUse">
      <stop offset=".097" stop-color="#3769ec"/>
      <stop offset=".469" stop-color="#3b41ec"/>
      <stop offset=".910" stop-color="#45a5ed"/>
    </linearGradient>
  </defs>
  <!-- Icon mark -->
  <path fill="url(#sp-g1)" d="M324.98,129.99h-65v-65C259.99,29.1,230.89,0,194.99,0h0C159.09,0,129.99,29.1,129.99,65v194.99h194.99c35.9,0,65-29.1,65-65h0C389.98,159.09,360.88,129.99,324.98,129.99Z"/>
  <path fill="url(#sp-g2)" d="M129.99,129.99l-65,0C29.1,129.99,0,159.09,0,194.99v0c0,35.9,29.1,65,65,65l65,0v65c0,35.9,29.1,65,65,65h0c35.9,0,65-29.1,65-65l0-65v-62.59c0-37.23-30.18-67.4-67.4-67.4H129.99Z"/>
  <path fill="#27265e" d="M194.99,129.99h0c35.87,0,65,29.12,65,65v0c0,35.87-29.12,65-65,65h-65v-65C129.99,159.12,159.12,129.99,194.99,129.99Z"/>
  <!-- Wordmark (use fill="#ffffff" on dark backgrounds) -->
  <path fill="#111" d="M496.73,254.17c-5.41-10.83.36-18.77,11.55-21.65l11.19-2.53c9.74-2.53,14.07,2.17,21.65,9.74,6.5,7.22,16.24,10.83,27.79,10.83,14.07,0,23.82-6.5,23.82-16.24,0-7.94-5.41-11.91-17.32-16.24l-22.74-7.94c-19.13-6.14-52.33-20.21-52.33-53.77,0-34.65,28.87-58.46,68.93-58.46,23.82,0,45.47,7.58,59.19,28.15,7.22,10.47,1.8,19.85-10.1,22.74l-10.1,2.53c-9.38,2.53-14.44-.72-20.93-6.86-5.05-5.05-11.55-6.86-18.04-6.86-11.55,0-18.77,7.22-18.77,15.88,0,7.94,7.22,11.91,16.96,15.16l23.1,8.66c38.25,12.63,51.97,33.2,52.69,55.94,0,38.98-34.65,58.1-74.7,58.1-32.84,0-59.55-12.27-71.82-37.17Z"/>
  <path fill="#111" d="M664.18,194.63c0-53.41,44.03-96.72,102.85-96.72,58.82,0,102.85,43.31,102.85,96.72s-44.03,96.72-102.85,96.72c-58.82,0-102.85-42.95-102.85-96.72ZM816.83,194.99c0-29.23-22.01-51.61-49.8-51.61-28.15,0-49.8,22.37-49.8,51.61,0,28.87,21.65,51.25,49.8,51.25,27.79,0,49.8-22.37,49.8-51.25Z"/>
  <path fill="#111" d="M891.17,195.71c0-54.13,41.5-97.8,106.82-97.8,17.68,0,38.98,3.97,58.82,15.52,9.74,6.13,10.1,15.52,3.25,24.54l-5.77,7.22c-6.86,8.66-14.07,9.02-24.54,4.33-11.91-5.77-23.46-6.5-28.51-6.5-31.4,0-54.13,21.29-54.13,51.61s22.74,51.61,54.13,51.61c5.05,0,16.6-.72,28.51-6.5,10.47-4.69,18.04-4.33,24.54,4.33l5.77,7.22c6.86,9.02,5.41,19.49-6.5,25.98-18.4,10.47-38.61,14.07-55.58,14.07-64.6,0-106.82-42.58-106.82-95.63Z"/>
  <path fill="#111" d="M1095.07,51c0-16.6,11.91-29.23,33.56-29.23,21.29,0,33.56,12.63,33.56,29.23,0,16.24-12.99,28.87-33.56,28.87-20.57,0-33.56-12.63-33.56-28.87ZM1100.85,270.05V119.2c0-11.19,6.14-17.32,17.32-17.32h20.93c11.19,0,17.68,6.13,17.68,17.32v150.85c0,11.19-6.5,17.32-17.68,17.32h-20.93c-11.19,0-17.32-6.14-17.32-17.32Z"/>
  <path fill="#111" d="M1190.71,194.63c0-54.49,37.17-96.72,89.14-96.72,24.54,0,46.19,9.38,59.55,30.31v-9.02c0-11.19,6.13-17.32,17.32-17.32h21.29c11.19,0,17.32,6.13,17.32,17.32v150.85c0,11.19-6.14,17.32-17.32,17.32h-21.29c-11.19,0-17.32-6.14-17.32-17.32v-8.66c-13.35,20.57-35.01,29.95-59.55,29.95-51.97,0-89.14-41.86-89.14-96.72ZM1340.11,194.63c0-29.59-18.77-51.97-47.28-51.97-29.23,0-46.19,23.46-46.19,51.97,0,28.87,16.96,51.97,46.19,51.97,28.51,0,47.28-22.37,47.28-51.97Z"/>
  <path fill="#111" d="M1440.8,270.05V43.78c0-11.19,6.14-17.32,17.32-17.32h20.93c11.19,0,17.68,6.13,17.68,17.32v226.28c0,11.19-6.5,17.32-17.68,17.32h-20.93c-11.19,0-17.32-6.14-17.32-17.32Z"/>
  <path fill="#111" d="M1531.48,269.69c0-11.91,9.38-21.65,21.65-21.65,12.27,0,21.65,9.74,21.65,21.65,0,12.27-9.38,21.65-21.65,21.65-12.27,0-21.65-9.38-21.65-21.65Z"/>
  <path fill="#111" d="M1606.03,358.47V117.04c0-6.14,3.61-9.74,9.38-9.74h8.3c6.14,0,9.74,3.61,9.74,9.74v25.62c16.24-27.07,41.86-39.34,70.37-39.34,54.85,0,90.22,42.22,90.22,94.19,0,51.25-34.65,93.83-89.86,93.83-29.23,0-54.85-12.63-70.73-39.34v106.46c0,6.14-3.61,9.74-9.74,9.74h-8.3c-5.77,0-9.38-3.61-9.38-9.74ZM1766.26,197.52c0-38.25-24.18-69.65-65.32-69.65-39.7,0-67.85,29.23-68.21,69.65.36,39.7,27.79,69.29,68.21,69.29,41.86,0,65.32-31.76,65.32-69.29Z"/>
  <path fill="#111" d="M1839.88,277.63V36.2c0-6.14,3.61-9.74,9.74-9.74h8.3c5.77,0,9.38,3.61,9.38,9.74v241.43c0,6.14-3.61,9.74-9.38,9.74h-8.3c-6.13,0-9.74-3.61-9.74-9.74Z"/>
  <path fill="#111" d="M1923.6,209.79v-92.75c0-5.77,3.61-9.74,9.74-9.74h8.3c6.14,0,9.74,3.61,9.74,9.74v92.75c0,43.31,22.74,57.02,45.47,57.02,19.85,0,60.63-14.07,60.99-72.18v-77.59c0-6.14,3.61-9.74,9.74-9.74h8.3c6.14,0,9.74,3.61,9.74,9.74v160.59c0,6.14-3.61,9.74-9.74,9.74h-8.3c-6.13,0-9.74-3.61-9.74-9.74v-28.51c-9.38,28.51-36.09,42.22-62.79,42.22-38.25,0-71.46-22.37-71.46-81.56Z"/>
  <path fill="#111" d="M2130.39,257.78c-3.61-6.14-.36-10.47,5.77-12.27l6.5-1.8c5.41-1.44,8.66.72,12.27,5.41,7.22,11.19,21.65,18.4,38.25,18.4,20.21,0,35.73-11.91,35.73-28.87,0-13.71-10.1-22.01-25.26-27.07l-25.62-8.3c-25.98-7.94-42.95-22.37-42.95-47.64,0-28.51,22.37-52.33,57.74-52.33,20.57,0,41.14,8.3,52.33,29.59,3.25,6.14,0,10.83-6.5,12.27l-5.77,1.44c-5.41,1.44-8.66-.72-12.27-5.77-6.5-9.38-16.96-13.71-27.07-13.71-19.85,0-31.76,13.35-31.76,27.79,0,14.8,12.63,22.01,24.9,25.98l26.71,8.66c32.12,9.74,41.86,29.59,41.86,49.44,0,32.84-28.87,52.33-62.43,52.33-27.07,0-51.25-11.91-62.43-33.56Z"/>
</svg>
```

Icon mark, colour:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 390 390">
  <defs>
    <linearGradient id="sp-icon-g1" x1="125.8" y1="60.75" x2="307.71" y2="270.34" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#f568f0"/>
      <stop offset=".516" stop-color="#f66005"/>
      <stop offset="1" stop-color="#f7c506"/>
    </linearGradient>
    <linearGradient id="sp-icon-g2" x1="62.83" y1="116.6" x2="247.38" y2="334.1" gradientUnits="userSpaceOnUse">
      <stop offset=".097" stop-color="#3769ec"/>
      <stop offset=".469" stop-color="#3b41ec"/>
      <stop offset=".910" stop-color="#45a5ed"/>
    </linearGradient>
  </defs>
  <path fill="url(#sp-icon-g1)" d="M324.98,129.99h-65v-65C259.99,29.1,230.89,0,194.99,0h0C159.09,0,129.99,29.1,129.99,65v194.99h194.99c35.9,0,65-29.1,65-65h0C389.98,159.09,360.88,129.99,324.98,129.99Z"/>
  <path fill="url(#sp-icon-g2)" d="M129.99,129.99l-65,0C29.1,129.99,0,159.09,0,194.99v0c0,35.9,29.1,65,65,65l65,0v65c0,35.9,29.1,65,65,65h0c35.9,0,65-29.1,65-65l0-65v-62.59c0-37.23-30.18-67.4-67.4-67.4H129.99Z"/>
  <path fill="#27265e" d="M194.99,129.99h0c35.87,0,65,29.12,65,65v0c0,35.87-29.12,65-65,65h-65v-65C129.99,159.12,159.12,129.99,194.99,129.99Z"/>
</svg>
```

For the white mono version replace every `fill="url(#…)"`, `fill="#27265e"` and `fill="#111"` with `fill="#ffffff"`; for black mono with `fill="#111111"`.

## Known inconsistencies (as-is, no decision applied)
- The live nav shows the logo as a raster CDN image, not the SVG; the footer uses a second copy with alt text "SocialPlus logo" (the name is written social.plus)
- The X (Twitter) footer icon title still says "Social+" (see the icons foundation)
- The site's logo file set its colours in a `<style>` block. Claude Design strips `<style>` from uploaded SVGs, so the first page built there (7 October 2026) showed the logo all black. Since 13.57 the copy in `assets/media/` carries its colours on the shapes (`capture/localize-media.mjs` does this on every capture run)
