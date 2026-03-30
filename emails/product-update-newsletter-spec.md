# social.plus Email — Technical Spec

MailerLite requirements, brand colors, typography, and merge tags. Fetch this alongside the components and assembly files.

---

## MailerLite Technical Requirements

**CSS strategy:** Use an embedded `<style>` block in `<head>`. MailerLite's automatic CSS inliner converts embedded styles to inline, preserving only `@media` queries. Enable "Automatic CSS inline" in the Settings tab when editing.

**Responsive approach:** Use a single `@media all and (max-width:789px)` breakpoint (750px content width + scrollbar buffer). Define responsive utility classes (`.container`, `.row`, `.mobile-stack`, `.mobile-hide`) that override fixed widths on small screens.

**Layout:** Table-based only. Use `<table>`, `<tr>`, `<td>` with `role="presentation"` for accessibility. Never rely on `<div>` for structural layout.

**Outlook support:** Include conditional comments for `<!--[if mso]>` to force font-family and set PixelsPerInch to 96. Use VML `<v:roundrect>` fallback for rounded buttons.

**Device fixes:**
- iOS: `a[x-apple-data-detectors]` to prevent blue link styling
- Android: `div[style*="margin: 16px 0"]` center fix
- Meta tags: `format-detection` to prevent auto-linking phone numbers/dates

**Width:** 750px max content width. Collapses to 100% on mobile via media queries.

**Images:** Always set explicit `width` attribute, use `style="display:block;"`, include meaningful `alt` text.

**Footer requirements:** Must include visible `{$unsubscribe}` link (mandatory for MailerLite delivery). Should include `{$preferences}` link.

---

## Brand Colors for Email

Hardcoded hex values only — email clients do not support CSS custom properties.

| Role | Light Hex | Dark Hex | Usage |
|------|-----------|----------|-------|
| Brand Blue | `#3b41ec` | `#7b7fff` | CTA buttons, header button border, links |
| Blue Hover | `#272b9d` | — | Button hover (in `<style>` block only) |
| Page Background | `#f5f5f5` | `#1a1a1a` | `<body>` and outer wrapper |
| Content Background | `#ffffff` | `#2d2d2d` | Content area cells |
| Alt Section Background | `#f9f9f9` | `#2d2d2d` | Tier 3 feature section, divider areas |
| Footer Background | `#ffffff` | `#2d2d2d` | Footer (with top border) |
| Heading Text | `#111111` | `#f0f0f0` | Headings, footer brand name |
| Body Text | `#414347` | `#e0e0e0` | Paragraph text |
| Secondary Text | `#717275` | `#a0a0a3` | Module tags, preheader, captions, footer text |
| Muted Text | `#b3b3b3` | `#555555` | Footer separator pipe |
| White | `#ffffff` | — | Button text, social icon text (X) |
| Border | `#e7e7e7` | `#444444` | Divider lines, footer top border |
| Footer Link | `#3b41ec` | `#7b7fff` | Unsubscribe/preferences links |

---

## Module Color Accents

Each product module has a background/text color pair used for category badges. Apply as a small inline badge next to feature headings when the module tag is present.

| Module | Background | Text/Accent |
|--------|-----------|-------------|
| Console | `#e8deff` | `#c5aaff` |
| UI Kit | `#fff4d9` | `#f7c506` |
| Chat | `#e8f9f5` | `#1dc497` |
| Video | `#fff4d9` | `#ffd500` |
| Analytics | `#8abfff` | `#222222` |
| Social | `#ffe9ed` | `#ff456b` |
| Flutter | `#fff1f0` | `#ff5a36` |
| React Native | `#d6ede2` | `#084c41` |

Badge HTML pattern:
```html
<span style="display:inline-block; padding:2px 8px; border-radius:4px; background-color:MODULE_BG; color:MODULE_TEXT; font-size:12px; font-weight:600; line-height:18px; margin-left:8px; vertical-align:middle;">Module Name</span>
```

---

## Typography

```
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
```

| Element | Size | Weight | Color | Line-height |
|---------|------|--------|-------|-------------|
| H1 (email title) | 28px | 700 | `#111111` | 36px |
| H2 (section heading) | 22px | 700 | `#111111` | 30px |
| H3 (feature name) | 18px | 700 | `#111111` | 26px |
| Module tag label | 13px | 600 | `#717275` | 18px |
| Body text | 16px | 400 | `#414347` | 26px |
| Small text | 14px | 400 | `#717275` | 22px |
| Button text | 16px | 600 | `#ffffff` | 20px |
| Outlined button | 14px | 600 | `#3b41ec` | 20px |
| Footer heading | 16px | 700 | `#111111` | 24px |
| Footer text | 14px | 400 | `#717275` | 22px |

---

## MailerLite Merge Tags

| Tag | Purpose | Required? |
|-----|---------|-----------|
| `{$unsubscribe}` | Unsubscribe URL | Yes (mandatory) |
| `{$preferences}` | Update preferences URL | Recommended |
| `{$url}` | View-in-browser URL | Recommended |
| `{$name}` | Subscriber's first name | Optional |
| `{$email}` | Subscriber's email | Optional |

---

## Image Placeholder Convention

Use visible `placehold.co` placeholder images so Bam can visually identify and swap each image in MailerLite's media manager after pasting the HTML.

**Format:** `https://placehold.co/{WIDTH}x{HEIGHT}/{BG_HEX}/{TEXT_HEX}?text={LABEL}`

| Slot | Dimensions | Example URL |
|------|-----------|-------------|
| Hero image | 750×425 | `https://placehold.co/750x425/e8eaff/3b41ec?text=HERO+IMAGE` |
| Tier 1 feature | 750×425 | `https://placehold.co/750x425/e8eaff/3b41ec?text=FEATURE+NAME` |
| Tier 2 feature | 670×385 | `https://placehold.co/670x385/e8eaff/3b41ec?text=FEATURE+NAME` |
| Tier 3 feature | 315×210 | `https://placehold.co/315x210/e8eaff/3b41ec?text=FEATURE+NAME` |

- Replace `FEATURE+NAME` with the actual feature name (spaces as `+`)
- Use `e8eaff` background with `3b41ec` text for all placeholders
- Always include meaningful `alt` text
- Logo URL (hardcoded): `https://storage.mlcdn.com/account_image/958330/0OpCmydxj01SEFXO54Jr1WOrPLK15IhrfL3CzQdj.png`

---

## Image Preparation

**Critical rule: all images must be exported as flat rectangles — no border-radius, no borders, no shadows baked into the image file.** The HTML applies `border-radius: 16px` on desktop and `12px` on mobile via the `.img-rounded` CSS class.

Dimensions: 750×425 for hero/Tier 1, 670×385 for Tier 2, 315×210 for Tier 3. Full-width images (hero, Tier 1) have no border-radius. Only Tier 2 and Tier 3 get rounded corners.
