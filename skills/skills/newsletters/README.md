# Newsletters

Claude skill for generating MailerLite-compatible responsive HTML marketing emails for social.plus.

Handles ALL email HTML output — both product/feature/release emails (Monthly Product Updates, Feature Launch Announcements) and general marketing emails (campaigns, announcements, promotions, outreach). Copy + HTML together in one skill; no hand-off needed.

## What it does

- Fetches terminology, tone, and color palette (hex values, not CSS variables — email clients don't support custom properties).
- Fetches the full email template reference stack: spec, structure, blocks, assembly orders, and content strategy.
- Determines email type from the input (product update doc → Type A; campaign brief → Type B) and applies the right assembly order.
- For product emails, parses the Newsletter section of a Google Doc and extracts tiered features (Tier 1 → Tier 4).
- Generates MailerLite-ready HTML with embedded `<style>`, responsive breakpoint, Outlook conditional comments, iOS blue-link fix, dark mode support, logo swap, and placeholder images at correct dimensions.
- Runs the compliance check before delivering, with special attention to terminology in subject lines and CTAs.

## When it triggers

Any email HTML generation request. Trigger phrases include "create an email", "write a newsletter", "email HTML", "MailerLite email", "campaign email", "product update email", "monthly update email", "feature announcement email", "email template", "newsletter HTML", or pasted content from a product update doc / Google Doc with release notes.

Do not use `brand-messaging` for emails — this skill handles both copy and HTML with format-specific requirements that `brand-messaging` doesn't load.

## Two email types

### Type A — Product / Feature / Release email
Triggered by product update docs, release notes, Google Docs with feature tiers, or requests for "what's new" / "feature launch" / "release note" emails.

- **Monthly Product Update** — multiple features across tiers, subject line pattern "What's New in [month year]", Newsletter section with tiered features. Uses "Assembly Order: Monthly Product Update" from `product-update-newsletter-assembly.md`.
- **Feature Launch Announcement** — single major feature with sub-features, subject line focuses on one launch, no tier structure. Uses "Assembly Order: Feature Launch Announcement".

### Type B — General marketing email
Campaign emails, one-off announcements, promotional emails, outreach emails, or anything not tied to a product release. Uses the base HTML template plus boilerplates and content guidelines.

Subject line rules (mandatory):
- 40–50 characters maximum
- Lead with the value or hook — front-load the most important word
- No spam trigger words ("FREE", "Act now", all-caps, multiple exclamation marks)
- One emoji max, only if it adds meaning

## Workflow

1. Fetch `brain.md` (main brain).
2. Fetch `messaging/brain.md`. Follow "Any content task" routing for `terminology.md` + `tone.md`. Check if "Short-form content" applies for subject lines.
3. Fetch color files directly: `design-system/colors-palette.md`, `design-system/colors-usage.md`.
4. Fetch the email template stack: spec, structure, blocks, assembly, and `emails.md`.
5. Determine email type. Parse the input (Google Doc via `google_drive_fetch`, or pasted text).
6. Generate HTML following the correct assembly order.
7. Run the compliance check from `brain.md`.
8. Deliver complete HTML in a single code block. Save as `.html` if long enough to warrant browser preview before MailerLite.

## Tier system (Monthly Product Updates)

| Tier | Contains | Image | Description |
|---|---|---|---|
| Tier 1 | Lead feature | Placeholder | Title + full description + "Learn more" CTA |
| Tier 2 | Secondary features | Placeholder | Title + module tag + full description + "Learn more" |
| Tier 3 | Smaller features | Placeholder | Title + module tag + short description (≤280 chars) + docs link |
| Tier 4 | Brief mentions | None | Module tag + title only |

**Ignore everything outside the Newsletter section** of the product update doc (Website, Video, Product Activation sections are out of scope).

## HTML requirements

- Embedded `<style>` block — MailerLite's CSS inliner converts it to inline styles, preserving only `@media` queries.
- Single responsive breakpoint: `@media all and (max-width:789px)` (750px content + scrollbar buffer).
- Outlook conditional comments for font-family and PixelsPerInch.
- iOS blue link fix (`a[x-apple-data-detectors]`) and Android center fix.
- `role="presentation"` on all layout tables.
- 750px max content width.
- Inter font with system fallbacks.
- Brand colors as hardcoded hex values — no CSS custom properties.
- Per-module color accents for category badges.
- MailerLite merge tags: `{$unsubscribe}`, `{$url}`, `{$preferences}`.
- Visible `placehold.co` placeholder images at correct dimensions with labeled colored boxes.
- Feature images use `.img-rounded` CSS class (`border-radius:16px` desktop, `12px` mobile) — never bake border-radius into the image.
- Closing text uses `font-weight:600` (semi-bold).

### Dark mode support
- `<meta name="color-scheme" content="light dark">` and `<meta name="supported-color-schemes" content="light dark">`.
- `:root { color-scheme: light dark; }`.
- `@media (prefers-color-scheme: dark)` block with all override classes.
- `[data-ogsc]` and `[data-ogsb]` Outlook selectors.
- Dark mode CSS classes: `body-bg` on wrapper tables and body, `container-bg` on content tables, `text-dark`/`text-body`/`text-secondary` on text, `link-brand` on links, `footer-border` on footer table, `preheader-ghost` on hidden preheader.
- Logo swap: include both `logo-light` (default dark logo) and `logo-dark` (white logo, hidden by default) images in the header, wrapped in MSO conditional comments.

## Files

```
newsletters/
├── SKILL.md                          Skill entry point — workflow, type detection, HTML requirements
└── README.md                         This file
```

All email templates, specs, and guidelines live in the repo root's `emails/` folder and are fetched at runtime.

## Delivery reminders for the user

1. Paste the HTML into MailerLite's custom HTML editor.
2. Upload screenshots to MailerLite's media library; replace each `placehold.co` URL with the MailerLite CDN URL.
3. **Export images as flat rectangles** — no border-radius, no borders, no shadows baked in. The HTML applies border-radius via CSS.
4. Upload a white version of the social.plus logo to MailerLite and replace `REPLACE_WITH_WHITE_LOGO.png` in the header with the actual CDN URL (needed for dark mode logo swap).
5. Preview in MailerLite using Preview and Test — check both light and dark mode rendering.
6. Enable "Automatic CSS inline" in MailerLite's Settings tab.

## URL format

All reference files are loaded from a shallow clone of this repo (`git clone --depth 1`) into `$MT_REPO`. The canonical fetch block at the top of each SKILL.md handles the clone; skills then read files with `cat "$MT_REPO/<path>"`.
