# social.plus Typography System

Source of truth: Figma file node `131:3822`
https://www.figma.com/design/nDIDa7goXwKlqGWdKKlbIX/2026-Website-Visuals?node-id=131-3822

---

## Typefaces

### Primary: Figtree
**All social.plus communications use Figtree as the primary typeface.**

- Type: Geometric sans-serif
- Available: Free on Google Fonts (https://fonts.google.com/specimen/Figtree)
- Download link is included in the Figma brand site under Typography > Download > Font Family
- Weights available: Light (300), Regular (400), Medium (500), SemiBold (600), Bold (700), ExtraBold (800), Black (900)

Figtree is warm, readable, and confident — a perfect match for social.plus's direct
yet human brand personality.

### Safe fallback (email / system contexts)
Where custom fonts cannot be loaded (plain HTML email, Office documents):
`font-family: 'Figtree', 'Inter', sans-serif;`

---

## Type Scale

The following scale is derived from the Figma brand site:

| Style name | Size | Weight | Line height | Use |
|------------|------|--------|-------------|-----|
| H1 / Display | 48px | Bold (700) | 1.4 | Page titles, hero headlines |
| H2 | 32px | Bold (700) | 1.4 | Section headings |
| H3 | 24px | Bold (700) | 1.4 | Sub-section headings, card titles |
| H4 / H6 | 20px | Bold (700) | 1.4 | Small headings, nav labels |
| Body Large | 16px | Regular (400) | 1.5 | Body text, descriptions |
| Body Medium | 16px | Medium (500) | 1.5 | Emphasis within body, labels |
| Body Small | 14px | Medium (500) | 1.25 | Captions, secondary info |
| Label / Eyebrow | 12px | Bold (700) | 1 | All-caps section labels, UI eyebrows, table headers, token labels — 0.1em letter-spacing |
| Caption | 12px | Regular (400) | 1.5 | Fine print, timestamps |

**Minimum font size: 12px.** Never use 11px, 10px, or smaller in any UI context. The 12px step satisfies the 4pt grid and remains legible at standard screen densities.

---

## Typesetting Principles

**Leading (line height):** Headings use 1.4× line height. Body text uses 1.5×.
Tight line heights (1.2–1.3) should be reserved for very large display type only.

**Tracking (letter spacing):** Use 0 tracking for body text. All-caps labels and
nav items use slight tracking (0.05–0.1em) to aid readability. Never use wide
tracking on lowercase body copy.

**Kerning:** Use optical kerning on headlines and large display text. Metric kerning
is fine for body copy.

**Hierarchy:** On any given screen or page, limit yourself to 3 type sizes maximum.
The hierarchy should be immediately legible — the most important information should
be the largest and boldest.

**Uppercase:** Navigation labels and badges use UPPERCASE with Figtree Bold or Medium.
Body copy is never all-caps. Headlines are sentence case or title case.

---

## Colour on Text

Colour tokens below reference primitives from `colors-palette.md`.

- **Primary text on dark:** White (`neutral-white` / `#FFFFFF`)
- **Secondary text on dark:** `slate-300` (`#D3D3D3`) for subtle, `slate-400` (`#A3A3A3`) for muted
- **On light backgrounds:** Use `slate-950` (`#111111`) for primary text
- **Body text on light:** `slate-700` (`#404040`)
- **Secondary text on light:** `slate-500` (`#727272`)
- **Muted text on light:** `slate-400` (`#A3A3A3`)
- **Links and CTAs:** `ultramarine-600` (`#3B41EC`) on light backgrounds; white with underline on dark

---

## Typography in Email

Because email clients have inconsistent font rendering:
- Specify `font-family: 'Figtree', 'Inter', Arial, sans-serif;` in all email CSS
- Use web-safe fallbacks (Arial or Helvetica) as tertiary fallbacks
- Bold text should use `font-weight: 700` not just `font-weight: bold` for consistency
---

## Typography in Social Media

- **LinkedIn:** Figtree is not rendered natively in LinkedIn posts (all text is platform-rendered).
  Write copy that is powerful even in the default LinkedIn font. Emojis can add visual
  weight and break up long text.
- **Instagram:** Text overlaid on images should use Figtree Bold at a size large enough
  to be legible at mobile thumbnail size (approximately 24px+ in a 1080×1080 frame).
- **Twitter/X:** Character limits apply. Write punchy, direct copy. Headlines over body copy.
