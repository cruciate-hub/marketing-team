---
name: newsletters
description: >
  Generate MailerLite-compatible responsive HTML marketing emails for social.plus.
  This skill handles ALL email HTML output — two types:
  (1) Product/feature/release emails: product update emails, feature announcement emails,
  monthly release emails, release notes, "what's new" emails, or when the user pastes
  content from a product update doc or shares a Google Doc with release notes.
  (2) General marketing emails: campaign emails, one-off announcements, promotional emails,
  outreach emails, or any email that is NOT about a product update or feature release.
  Trigger on phrases like "create an email", "write a newsletter", "email HTML",
  "MailerLite email", "campaign email", "product update email", "monthly update email",
  "feature announcement email", "email template", "newsletter HTML".
  Do NOT use brand-messaging for emails — this skill handles both copy and HTML.
---

# social.plus Email HTML Generator

Generate MailerLite-compatible responsive HTML emails. This skill handles two distinct email types — determine which one applies before proceeding.

## How to fetch reference files

<!-- FETCH-BLOCK:START v1 -->
Fetch reference files ONLY with `curl` from `raw.githubusercontent.com`, using these exact flags:

    curl -fsSL --max-time 30 --connect-timeout 10 --retry 2 --retry-delay 1 \
      https://raw.githubusercontent.com/cruciate-hub/marketing-team/main/<path>

The repo is public — no authentication required. When fetching multiple files in one step, run the curl commands in parallel (single Bash message, multiple commands) — do not serialise.

Validate every response before using it:
- Markdown files must start with `#` (a leading heading line)
- JSON files must start with `{` or `[`
- HTML files must start with `<`
- Content must be non-empty

If any fetch fails (non-zero exit, empty output, or content that fails the above check):
- Do NOT reconstruct the file from memory or training data.
- Do NOT fall back to WebFetch or any other tool.
- Stop immediately and respond with exactly this line:

  `Fetch failed: <path>. Please check your network connection and rerun.`
<!-- FETCH-BLOCK:END v1 -->

## Step 0: Fetch the main brain

Fetch `brain.md` for cross-domain routing, precedence rules, and the compliance check you must run before delivering.

## Step 1: Fetch brand guidelines

Fetch `messaging/brain.md` to get the messaging router.

Follow its "Any content task" routing to fetch `terminology.md` and `tone.md`. For email subject lines and body copy, also check if "Short-form content" routing applies.

Fetch the color system directly (emails need hex values, not CSS variables):

- `design-system/colors-palette.md`
- `design-system/colors-usage.md`

## Step 2: Fetch the email template references

Fetch all five — they work together:

- `emails/product-update-newsletter-spec.md`
- `emails/product-update-newsletter-structure.md`
- `emails/product-update-newsletter-blocks.md`
- `emails/product-update-newsletter-assembly.md`
- `emails/emails.md`

- `product-update-newsletter-spec.md` — MailerLite technical requirements, brand colors, typography, merge tags, image placeholder convention
- `product-update-newsletter-structure.md` — HTML for: base shell, preheader, header, intro text, hero image
- `product-update-newsletter-blocks.md` — HTML for: tiers 1-4, divider, CTA button, closing text, footer. Follow both components files exactly when generating HTML.
- `product-update-newsletter-assembly.md` — assembly orders for both email types and the pre-delivery checklist
- `emails.md` — email content strategy: subject line rules, body structure, CTA best practices, email type guidelines

## Step 3: Determine email type

Identify which of the two email types applies based on the user's request or source document:

### Type A — Product / Feature / Release email
Use when: the user shares a product update doc, release notes, a Google Doc with feature tiers, or asks for a "what's new", "feature launch", or "release note" email.

- **Monthly Product Update** — Multiple features across tiers, subject line pattern "What's New in [month year]", has Newsletter section with tiered features. Use the "Assembly Order: Monthly Product Update" from `product-update-newsletter-assembly.md`.
- **Feature Launch Announcement** — Single major feature with sub-features, subject line focuses on one launch (e.g., "Events is now live"), no tier structure. Use the "Assembly Order: Feature Launch Announcement" from `product-update-newsletter-assembly.md`.

→ Continue to Step 4.

### Type B — General marketing email
Use when: the user asks for a campaign email, one-off announcement, promotional email, or any email not tied to a product update or feature release.

- Fetch the base HTML template at `emails/product-update-newsletter-examples/email-template.html`.
- Fetch `messaging/boilerplates.md` for standardized descriptions and elevator pitches — use these as starting points for body copy.
- Apply `terminology.md` and `tone.md` for copy.
- Apply `colors-palette.md` and `colors-usage.md` for all color values (hex only — no CSS variables).
- Follow the email content guidelines in `emails.md` for body structure and CTA.
- **Subject line rules (mandatory):**
  - 40–50 characters maximum
  - Lead with the value or hook — front-load the most important word
  - No spam trigger words ("FREE", "Act now", all-caps, multiple exclamation marks)
  - One emoji max, only if it adds meaning
- Output complete HTML ready to paste into MailerLite.

→ Skip to Step 6 after generating the HTML.

## Step 4: Parse the input

The source document is typically a Google Doc (or pasted text from one).

### For Monthly Product Updates:

The Newsletter section uses a **tiered feature system**:

- **Tier 1** — Lead feature. Has: title, full description, image placeholder, "Learn more" CTA link.
- **Tier 2** — Secondary features. Has: title, product module tag, full description, image placeholder, "Learn more" CTA link.
- **Tier 3** — Smaller features. Has: title, product module tag, image placeholder, short description (max 280 chars), documentation link.
- **Tier 4** — Brief mentions. Has: product module tag, title only. No images, no descriptions.

The doc also contains Website, Video, and Product Activation sections — **ignore everything outside the Newsletter section.**

If the user shares a Google Doc link, use the google_drive_fetch tool to read it. If they paste text, parse it directly.

Extract from the Newsletter section:
1. The subject line (from the heading pattern "What's New in [month year]: [highlights]")
2. The opening remark paragraph
3. Each tiered feature with its title, description, module tag, image reference, and link
4. The closing remark

### For Feature Launch Announcements:

Extract:
1. The subject line (feature launch headline)
2. The hero image description
3. The feature title and description
4. Sub-features (each with: title, short description, image reference)
5. CTA link (full announcement page)
6. The closing remark

## Step 5: Generate the HTML

Follow all patterns from the email template reference file. Use the correct assembly order for the email type.

Key requirements:

- Use embedded `<style>` block for CSS — MailerLite's automatic CSS inliner converts it to inline styles, preserving only `@media` queries for responsive behavior
- Single responsive breakpoint: `@media all and (max-width:789px)` (750px content + scrollbar buffer)
- Outlook conditional comments for font-family and PixelsPerInch
- iOS blue link fix (`a[x-apple-data-detectors]`) and Android center fix
- `role="presentation"` on all layout tables
- 750px max content width
- Inter font with system fallbacks
- Brand colors as hardcoded hex values (not CSS custom properties — email clients don't support them)
- Per-module color accents for category badges
- MailerLite merge tags: `{$unsubscribe}`, `{$url}`, `{$preferences}`
- Visible `placehold.co` placeholder images with labeled colored boxes at correct dimensions (see reference file for format)
- Map tiers to the correct layout components from the reference file
- Feature images use `.img-rounded` CSS class (`border-radius:16px` desktop, `12px` mobile) — never bake border-radius into images
- Closing text uses `font-weight:600` (semi-bold)
- Dark mode support: include `<meta name="color-scheme" content="light dark">` and `<meta name="supported-color-schemes" content="light dark">` meta tags, `:root { color-scheme: light dark; }`, `@media (prefers-color-scheme: dark)` block with all override classes, plus `[data-ogsc]` and `[data-ogsb]` Outlook selectors
- Dark mode CSS classes on all HTML elements: `body-bg` on wrapper tables and body, `container-bg` on content tables, `text-dark`/`text-body`/`text-secondary` on text, `link-brand` on links, `footer-border` on footer table, `preheader-ghost` on hidden preheader
- Logo swap: include both `logo-light` (default dark logo) and `logo-dark` (white logo, hidden by default) images in header, wrapped in MSO conditional comments

## Step 6: Run compliance check and deliver

Run the compliance check from `brain.md` before delivering. Pay special attention to terminology in email subject lines and CTAs — these are high-visibility.

Output the complete HTML in a single code block. If the email is long, also save it as an `.html` file so the user can preview it in a browser before pasting into MailerLite.

Remind the user to:
1. Paste the HTML into MailerLite's custom HTML editor
2. Upload screenshots to MailerLite's media library, then replace each `placehold.co` URL with the MailerLite CDN URL — the colored placeholder boxes show exactly which image goes where
3. **Export all images as flat rectangles** — no border-radius, no borders, no shadows baked in. The HTML applies border-radius via CSS.
4. **Upload a white version of the social.plus logo** to MailerLite and replace `REPLACE_WITH_WHITE_LOGO.png` in the header with the actual MailerLite CDN URL (needed for dark mode logo swap)
5. Preview in MailerLite using Preview and Test before sending — check both light and dark mode rendering
6. Enable "Automatic CSS inline" in MailerLite's Settings tab
