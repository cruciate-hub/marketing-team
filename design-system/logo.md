# social.plus Logo Guidelines

Source: canonical design system HTML

---

## SVG Logo Data

When generating HTML, emails, or any output that needs to embed the logo as inline SVG,
use the following verified vector data directly.

### Full Name Logo (icon + wordmark) - colour on dark

The wordmark paths use `fill: #111` which renders as black - swap to `fill: #ffffff` for
use on dark backgrounds (e.g. brand emails).

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

### Icon Mark Only - colour

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

---

## The Logo Concept

The social.plus logo embodies **limitless connection**. By intersecting fluid shapes,
the mark reveals a central plus sign integrated with a subtle chat bubble - symbolising
the core of the communication platform. The vibrant, multi-coloured palette reflects
the diverse range of opportunities and creative possibilities within the community.

---

## Logo Variants

### 1. Full Name Logo (Primary)
The main logo: the social.plus icon mark + "social.plus" wordmark side by side.
- **Colour version** (default): Multi-colour icon on dark or white backgrounds
- **White version**: All-white for use on dark/coloured backgrounds
- **Black version** (monochrome): For single-colour print, embossing, or reverse situations

### 2. Icon Logo (Secondary)
The icon mark alone, without the wordmark. Use when:
- Space is very limited (e.g., favicons, social profile pictures, app icons)
- The brand is already established in context and the wordmark is redundant
- Available in: Colour, White, Black monochrome

Available colour variations of the icon: standard colour, white, black, and additional
mono variations.

---

## Clearspace Rules

The logo requires protected clear space on all sides. This space keeps the logo
visually separate from other elements and prevents visual clutter.

**Clearspace rule:** Maintain a minimum clear space equal to the height of the icon
mark on all four sides of the logo (both the full name logo and icon logo).

Never crowd the logo. If a layout is tight, use the icon mark instead of reducing
the full name logo below its minimum size.

---

## Logo on Backgrounds

| Background | Recommended logo treatment |
|------------|---------------------------|
| Brand Black (`#111`) | Colour logo or White logo |
| White / Light | Colour logo or Black logo |
| Brand Blue Gradient | White logo |
| Brand Pink Gradient | White logo |
| Dark photography | White logo |
| Light photography | Black logo or Colour logo (test for legibility) |
| Gradient white | Colour logo |
| Gradient black | White logo |

**Rule of thumb:** On any dark or highly saturated background, use the white logo.
On light backgrounds, use the colour logo or black logo. Never place the colour logo
on a busy or clashing coloured background.

**Never use the logo (full wordmark or icon mark) on Ultramarine (`#3B41EC`).** The blue gradient arm of the icon mark becomes invisible against Ultramarine, and the dark navy centre shape loses all definition. Approved backgrounds: Brand Black, dark surfaces (Surface 1–3), white, and light grey.

---

## Monochrome Usage

The monochrome (single colour) logo is used when:
- Printing in a single ink colour
- Embossing, debossing, or engraving
- Watermarks
- Situations where colour reproduction is not possible or reliable

Available monochrome sets: Black set and White set.

---

## Partnerships / Co-branding

When displaying the social.plus logo alongside a partner's logo:
- Use the full name logo paired with the partner's full logo
- OR use the icon logo paired with the partner's icon/mark
- Maintain equal visual weight between logos
- Separate logos with sufficient space (do not overlap)
- Downloadable partnership templates are available in Figma

---

## Logo Donts

Never:
- Stretch, skew, or distort the logo in any dimension
- Rotate the logo
- Apply drop shadows or glows to the logo
- Place the logo on a background colour that reduces legibility
- Redraw or recreate the logo from scratch - always use official files
- Change the logo's internal colour arrangement
- Add text or elements inside the clearspace zone
- Use a low-resolution version of the logo
- **Place the icon mark on an Ultramarine (#3B41EC) background** - the blue gradient arm becomes invisible against Ultramarine, and the dark navy centre shape (#27265E) loses all definition. The icon mark is approved for use on: Brand Black (#111111), dark surfaces (Surface 1–3), and light/white backgrounds only.

---

## Logo in Written Copy

When referring to the brand name in text:
- Write **social.plus** (lowercase 's', lowercase 'p', dot between them)
- Do not write Social.Plus, Social Plus, social plus, or SocialPlus
- In email subject lines or headings where title case is used, keep it: **social.plus** (the brand name is always lowercase)
