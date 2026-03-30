# social.plus Email — Assembly Orders

How to assemble components into complete emails. Use alongside the spec and components files.

---

## Assembly Order: Monthly Product Update

Stack components in this exact order:

1. **Base Template Shell** (wraps everything)
2. **Preheader** (hidden preview text + "View in browser")
3. **Header** (logo + "Explore All Updates" button)
4. **Intro Text** (opening remark from the doc)
5. **Hero Image** (monthly product update graphic)
6. **Body Intro** (contextual paragraph setting up the features)
7. **Tier 1 Feature(s)** — if present
8. **Tier 2 Feature(s)** — if present, separated by Dividers
9. **Tier 3 Feature Rows** — if present, alternating zigzag direction
10. **Tier 4 List** — if present
11. **Closing Text** (from the doc's closing remarks)
12. **Footer** (with social icons + unsubscribe)

Not every tier needs to be present. Include only the tiers that appear in the source doc.

---

## Assembly Order: Feature Launch Announcement

For single-feature launch emails (e.g., "Events is now live"). Use when the source focuses on one major feature with sub-features.

1. **Base Template Shell** (wraps everything)
2. **Preheader** (hidden preview text + "View in browser")
3. **Header** (logo + CTA button — e.g., "Visit Website")
4. **Hero Image** (full-width feature launch graphic, 750×425)
5. **Feature Title** — centered H1 heading with the launch headline
6. **Feature Description** — 1-2 paragraphs explaining the feature
7. **Section Heading** — e.g., "What's included" (centered H2, `font-size:22px; font-weight:700`)
8. **Tier 3 Feature Rows** — zigzag layout for sub-features (alternating image/text direction)
9. **CTA Button** — primary filled button (e.g., "See full announcement")
10. **Closing Text** (semi-bold, centered)
11. **Footer** (with social icons + unsubscribe)

Key differences from Monthly Product Update: no tiers 1/2/4, no Body Intro, the Hero acts as the launch visual, all sub-features use Tier 3 zigzag layout.

---

## Checklist Before Delivery

- [ ] All copy follows terminology.md rules
- [ ] Tone matches tone.md guidelines
- [ ] All colors are hardcoded hex from brand palette
- [ ] Table-based layout with `role="presentation"` throughout
- [ ] Embedded `<style>` block present (not all-inline)
- [ ] Single responsive breakpoint at 789px
- [ ] Outlook conditional comments in `<head>`
- [ ] iOS blue link fix and Android center fix present
- [ ] `{$unsubscribe}` in footer (mandatory)
- [ ] `{$url}` in preheader "View in browser" link
- [ ] `{$preferences}` in footer
- [ ] All images have alt text
- [ ] Image placeholders use `placehold.co` with correct dimensions and labels
- [ ] 750px max content width
- [ ] VML fallback on primary CTA button
- [ ] Module color badges applied where tags are present
- [ ] Preheader text matches email subject/purpose
- [ ] Feature images use `class="img-rounded"` with inline `border-radius:16px` fallback
- [ ] Closing text uses `font-weight:600`
- [ ] Dark mode meta tags present
- [ ] Dark mode `@media (prefers-color-scheme: dark)` block with all class overrides
- [ ] `[data-ogsc]` and `[data-ogsb]` Outlook dark mode selectors present
- [ ] All wrapper tables have `class="body-bg"`
- [ ] All container tables have `class="container-bg"`
- [ ] Text elements have dark mode classes (`text-dark`, `text-body`, `text-secondary`)
- [ ] Brand links have `class="link-brand"`
- [ ] Logo swap: both `logo-light` and `logo-dark` images in header
- [ ] Footer table has `class="footer-border"`
- [ ] `<body>` tag has `class="body-bg"`
