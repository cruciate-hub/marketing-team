# social.plus — Main Brain

This is the master router for all social.plus marketing content. Every skill loads this file alongside its domain-specific router to get cross-domain awareness, precedence rules, and the compliance check.

All reference files live in the public `cruciate-hub/marketing-team` GitHub repo. Skills load them via the canonical fetch block at the top of each SKILL.md, which shallow-clones the repo to `$MT_REPO` (default `/tmp/cruciate-hub-marketing-team`) once per session and reads files with `cat`. Paths in this file are relative to the repo root — for example `messaging/brain.md` is at `$MT_REPO/messaging/brain.md`.

## Cross-domain routing

Most tasks need references from more than one domain. Use this table to determine which routers to load:

| Task type | Load these routers |
|---|---|
| Written content (general copy, scripts, captions, taglines, ad-hoc text without a dedicated skill) | `messaging/brain.md` |
| Visual output (HTML, CSS, components, decks) | `messaging/brain.md` + `design-system/brain.md` |
| Blog posts for social.plus/blog | `skills/skills/blog-seo-content/SKILL.md` + `messaging/brain.md` |
| Customer stories / case studies | `skills/skills/case-study/SKILL.md` + `messaging/brain.md` |
| HTML emails / newsletters | **Use the newsletters skill** (see Available Skills below). It loads `messaging/brain.md`, `design-system/colors-palette.md`, `design-system/colors-usage.md`, and all email template files automatically. |
| UI copy (buttons, errors, tooltips, empty states) | `messaging/brain.md` — brain.md routes to `ui-micro-copy.md` |
| Website audit or content analysis (what pages say, messaging consistency, content gaps) | `skills/skills/site-intelligence/SKILL.md` + `messaging/brain.md` |
| Competitive content (comparisons, differentiators) | `messaging/brain.md` — ensure both `positioning.md` and `value-story.md` are loaded |
| AEO answer articles (/answers/ collection) | `skills/skills/aeo-content/SKILL.md` + `messaging/brain.md` |
| Press releases (newswire, PR Newswire / Cision, embargoed announcements, product/funding/partnership announcements) | `skills/skills/press-release/SKILL.md` + `messaging/brain.md` |
| Legal documents for `/legal/` (MSA, DPA, SLA, Terms, Privacy, etc.) | `skills/skills/legal-docs-formatter/SKILL.md` + `messaging/brain.md` |

If your skill's SKILL.md already specifies which domain router to load, follow that. Use this table to decide whether you also need the *other* domain router.

## Available skills

Skills are pre-built instruction sets for recurring task types. When a task matches, load the skill's SKILL.md first and follow it — it handles all routing and generation steps.

| Skill | Trigger | SKILL.md |
|---|---|---|
| **newsletters** | Any email HTML output — product update emails, feature launch announcements, campaign emails, newsletters | `skills/skills/newsletters/SKILL.md` |
| **brand-messaging** | Marketing copy, website copy, landing pages, pitch materials, taglines, brand voice questions | `skills/skills/brand-messaging/SKILL.md` |
| **blog-seo-content** | Blog posts for social.plus/blog | `skills/skills/blog-seo-content/SKILL.md` |
| **press-release** | Newswire-ready press releases (PR Newswire / Cision), embargoed announcements, product/funding/partnership announcements | `skills/skills/press-release/SKILL.md` |
| **case-study** | Customer stories, case studies, success stories, testimonial write-ups, Webflow customer story CMS items | `skills/skills/case-study/SKILL.md` |
| **design-system** | CSS, HTML styling, Webflow components, brand colors, typography, spacing, design tokens, dark mode | `skills/skills/design-system/SKILL.md` |
| **site-intelligence** | Query, audit, or analyze website content — what pages say, messaging consistency, gaps, competitive comparisons | `skills/skills/site-intelligence/SKILL.md` |
| **product-update-vs-website** | Compare a product release or changelog against the website to find pages that need updating | `skills/skills/product-update-vs-website/SKILL.md` |
| **link-building-vetter** | Vet incoming ABC link exchange requests — score anchors, text mods, and article eligibility, then draft response emails | `skills/skills/link-building-vetter/SKILL.md` |
| **backlink-placement-finder** | Find contextually relevant backlink placement opportunities on partner sites and draft request emails | `skills/skills/backlink-placement-finder/SKILL.md` |
| **aeo-content** | AEO answer articles for /answers/ collection, AI-optimized reference content for AI search engines | `skills/skills/aeo-content/SKILL.md` |
| **internal-linking-strategist** | Suggest SEO-grounded internal links for new content (invoked by `blog-seo-content` and `aeo-content` as a pre-delivery step) or run a site-wide internal-linking audit | `skills/skills/internal-linking-strategist/SKILL.md` |
| **legal-docs-formatter** | Format legal documents (MSA, DPA, SLA, Terms, Privacy, etc.) into clean HTML ready to paste into a Webflow Rich Text Embed block on a 📜 Legals CMS item | `skills/skills/legal-docs-formatter/SKILL.md` |
| **svg-icon-transformer** | Transform raw SVG input into clean, accessible, inline-embed-ready icon markup; strips editor noise and applies accessibility defaults | `skills/skills/svg-icon-transformer/SKILL.md` |

Load skill files via the canonical fetch block, same as every other reference file.

## Precedence rules

When two reference files give guidance on the same topic, the more specific file wins:

- **UI copy tasks:** `ui-micro-copy.md` overrides `tone.md` for voice, style, and capitalisation.
- **Email tasks:** `emails/emails.md` overrides `tone.md` for email-specific structure, subject lines, and CTAs.
- **Design tokens always win.** If `colors-palette.md` or `colors-usage.md` specifies a hex value, use it exactly — never approximate or substitute.
- **Terminology is always law.** `terminology.md` is never overridden by any file. Approved terms and forbidden terms apply everywhere, in every context, no exceptions.
- **Dedicated skills win over brand-messaging.** When a request matches both `brand-messaging` and a more specific skill — `blog-seo-content`, `aeo-content`, `press-release`, `case-study`, `newsletters`, or `legal-docs-formatter` — route to the dedicated skill. brand-messaging is the fallback for content types without a dedicated skill.

## Compliance check

Before delivering ANY content to the user, run this check:

1. **Terminology.** Re-read `terminology.md` (you already loaded it). Scan your output for forbidden terms. Common violations: "social network", "forum", "chat tool", "plug and play" (forbidden outside dev docs), growth guarantees.
2. **Tone.** Compare your output against `tone.md`. Does it sound like the social.plus brand — or like default Claude? If you can't tell the difference, it's default Claude. Rewrite.
3. **Claims.** You did not invent any statistics, customer names, quotes, features, or performance claims. If it's not in the fetched reference files, don't state it as fact.
4. **Design tokens.** If your output includes visual styling (CSS, HTML, color references), confirm every value matches the design system files exactly. No eyeballing.
5. **Precedence.** If you loaded multiple files that cover the same topic, confirm you followed the precedence rules above.

If any check fails, fix the output before delivering. Do not flag the issue and deliver anyway — fix it.
