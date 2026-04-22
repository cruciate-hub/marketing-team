# social.plus — Main Brain

This is the master router for all social.plus marketing content. Every skill fetches this file alongside its domain-specific router to get cross-domain awareness, precedence rules, and the compliance check.

All reference files are hosted at:
`https://github.com/cruciate-hub/marketing-team/blob/main/`

**Warning:** Always use `github.com/.../blob/...` URLs when fetching. Never convert to `raw.githubusercontent.com` or `api.github.com` — both are blocked by network egress restrictions and will fail.

## Cross-domain routing

Most tasks need references from more than one domain. Use this table to determine which routers to fetch:

| Task type | Fetch these routers |
|---|---|
| Written content (articles, blog posts, scripts, copy) | `messaging/brain.md` |
| Visual output (HTML, CSS, components, decks, emails) | `messaging/brain.md` + `design-system/brain.md` |
| Social media posts | `messaging/brain.md` + `design-system/brain.md` — brain.md routes to `social-posts.md` for platform specs |
| HTML emails / newsletters | **Use the newsletters skill** (see Available Skills below). It fetches `messaging/brain.md`, `design-system/colors-palette.md`, `design-system/colors-usage.md`, and all email template files automatically. |
| UI copy (buttons, errors, tooltips, empty states) | `messaging/brain.md` — brain.md routes to `ui-micro-copy.md` |
| Website audit or content analysis | `website/pages-*.json` (10 files, pick relevant ones) + `messaging/brain.md` |
| Competitive content (comparisons, differentiators) | `messaging/brain.md` — ensure both `positioning.md` and `value-story.md` are loaded |
| AEO answer articles (/answers/ collection) | `skills/skills/aeo-content/SKILL.md` + `messaging/brain.md` |

If your skill's SKILL.md already specifies which domain router to fetch, follow that. Use this table to decide whether you also need the *other* domain router.

## Available skills

Skills are pre-built instruction sets for recurring task types. When a task matches, fetch the skill's SKILL.md first and follow it — it handles all routing and generation steps.

| Skill | Trigger | SKILL.md |
|---|---|---|
| **newsletters** | Any email HTML output — product update emails, feature launch announcements, campaign emails, newsletters | `skills/skills/newsletters/SKILL.md` |
| **brand-messaging** | Marketing copy, website copy, landing pages, press releases, pitch materials, taglines, brand voice questions | `skills/skills/brand-messaging/SKILL.md` |
| **blog-seo-content** | Blog posts, thought leadership articles, SEO content, pillar pages, comparison articles, how-to guides | `skills/skills/blog-seo-content/SKILL.md` |
| **social-media** | LinkedIn posts, Instagram captions, X posts, social media campaigns, content calendars | `skills/skills/social-media/SKILL.md` |
| **campaign-copy** | Google Ads, LinkedIn Ads, Meta Ads, display ad copy, campaign landing pages, A/B test variants | `skills/skills/campaign-copy/SKILL.md` |
| **case-study** | Customer stories, case studies, success stories, testimonial write-ups, Webflow customer story CMS items | `skills/skills/case-study/SKILL.md` |
| **design-system** | CSS, HTML styling, Webflow components, brand colors, typography, spacing, design tokens, dark mode | `skills/skills/design-system/SKILL.md` |
| **site-intelligence** | Query, audit, or analyze website content — what pages say, messaging consistency, gaps, competitive comparisons | `skills/skills/site-intelligence/SKILL.md` |
| **product-update-vs-website** | Compare a product release or changelog against the website to find pages that need updating | `skills/skills/product-update-vs-website/SKILL.md` |
| **link-building-vetter** | Vet incoming ABC link exchange requests — score anchors, text mods, and article eligibility, then draft response emails | `skills/skills/link-building-vetter/SKILL.md` |
| **backlink-placement-finder** | Find contextually relevant backlink placement opportunities on partner sites and draft request emails | `skills/skills/backlink-placement-finder/SKILL.md` |
| **aeo-content** | AEO answer articles for /answers/ collection, AI-optimized reference content for AI search engines | `skills/skills/aeo-content/SKILL.md` |

Fetch skill files using the same `github.com/.../blob/...` URL pattern as all other files.

## Precedence rules

When two reference files give guidance on the same topic, the more specific file wins:

- **UI copy tasks:** `ui-micro-copy.md` overrides `tone.md` for voice, style, and capitalisation.
- **Social media tasks:** `social-posts.md` overrides `tone.md` for platform-specific tone, format, and structure.
- **Email tasks:** `emails/emails.md` overrides `tone.md` for email-specific structure, subject lines, and CTAs.
- **Design tokens always win.** If `colors-palette.md` or `colors-usage.md` specifies a hex value, use it exactly — never approximate or substitute.
- **Terminology is always law.** `terminology.md` is never overridden by any file. Approved terms and forbidden terms apply everywhere, in every context, no exceptions.

## Compliance check

Before delivering ANY content to the user, run this check:

1. **Terminology.** Re-read `terminology.md` (you already fetched it). Scan your output for forbidden terms. Common violations: "social network", "forum", "chat tool", "plug and play" (forbidden outside dev docs), growth guarantees.
2. **Tone.** Compare your output against `tone.md`. Does it sound like the social.plus brand — or like default Claude? If you can't tell the difference, it's default Claude. Rewrite.
3. **Claims.** You did not invent any statistics, customer names, quotes, features, or performance claims. If it's not in the fetched reference files, don't state it as fact.
4. **Design tokens.** If your output includes visual styling (CSS, HTML, color references), confirm every value matches the design system files exactly. No eyeballing.
5. **Precedence.** If you loaded multiple files that cover the same topic, confirm you followed the precedence rules above.

If any check fails, fix the output before delivering. Do not flag the issue and deliver anyway — fix it.
