# social.plus — Main Brain

This is the master router for all social.plus marketing content. Most skills load this file alongside their domain-specific router to get cross-domain awareness, precedence rules, and the compliance check.

All reference files live in the public `cruciate-hub/marketing-team` GitHub repo. Skills load them via the canonical fetch block at the top of each SKILL.md, which shallow-clones the repo to `$MT_REPO` (default `/tmp/cruciate-hub-marketing-team`) once per session and reads files with `cat`. Paths in this file are relative to the repo root — for example `messaging/brain.md` is at `$MT_REPO/messaging/brain.md`.

## Cross-domain routing

Most tasks need references from more than one domain. Use this table to determine which routers to load:

| Task type | Load these routers |
|---|---|
| Written content (general copy, scripts, captions, taglines, ad-hoc text without a dedicated skill) | `messaging/brain.md` |
| Visual output (HTML, CSS, components, decks) | `messaging/brain.md` + `design-system/brain.md` |
| Blog posts for social.plus/blog (any topic — product features, industry trends, opinion, listicles) | `marketing-team/skills/blog-seo-content/SKILL.md` + `messaging/brain.md` |
| Customer stories / case studies | `marketing-team/skills/case-study/SKILL.md` + `messaging/brain.md` |
| HTML emails / newsletters | **Use the newsletters skill** (see Available Skills below). It loads `messaging/brain.md`, `design-system/colors-palette.md`, `design-system/colors-usage.md`, and all email template files automatically. |
| UI copy (buttons, errors, tooltips, empty states) | `messaging/brain.md` — brain.md routes to `ui-micro-copy.md` |
| Website audit or content analysis (what pages say, messaging consistency, content gaps) | `marketing-team/skills/site-intelligence/SKILL.md` + `messaging/brain.md` |
| Competitive content (comparisons, differentiators) | `messaging/brain.md` — ensure both `positioning.md` and `value-story.md` are loaded |
| AEO answer articles (/answers/ collection) | `marketing-team/skills/aeo-content/SKILL.md` + `messaging/brain.md` |
| Press releases (newswire, PR Newswire / Cision, embargoed announcements, product/funding/partnership announcements) | `marketing-team/skills/press-release/SKILL.md` + `messaging/brain.md` |
| Legal documents for `/legal/` (MSA, DPA, SLA, Terms, Privacy, etc.) | `marketing-team/skills/legal-docs-formatter/SKILL.md` + `messaging/brain.md` |

If your skill's SKILL.md already specifies which domain router to load, follow that. Use this table to decide whether you also need the *other* domain router.

## Available skills

Skills are pre-built instruction sets for recurring task types. When a task matches, load the skill's SKILL.md first and follow it — it handles all routing and generation steps.

| Skill | Trigger | SKILL.md |
|---|---|---|
| **newsletters** | Any email HTML output — product update emails, feature launch announcements, campaign emails, newsletters | `marketing-team/skills/newsletters/SKILL.md` |
| **brand-messaging** | Primary skill for content about a social.plus product/feature/module/capability where no format-specific skill applies — feature pages, landing pages, release-note CMS items, taglines, pitch materials, brand voice audits. Not for blog posts (use blog-seo-content). | `marketing-team/skills/brand-messaging/SKILL.md` |
| **blog-seo-content** | Blog posts for social.plus/blog — any topic (product features, industry trends, opinion, listicles). Loads the full messaging stack for brand voice. | `marketing-team/skills/blog-seo-content/SKILL.md` |
| **press-release** | Newswire-ready press releases (PR Newswire / Cision), embargoed announcements, product/funding/partnership announcements | `marketing-team/skills/press-release/SKILL.md` |
| **case-study** | Customer stories, case studies, success stories, testimonial write-ups, Webflow customer story CMS items | `marketing-team/skills/case-study/SKILL.md` |
| **design-system** | CSS, HTML styling, Webflow components, brand colors, typography, spacing, design tokens, dark mode | `marketing-team/skills/design-system/SKILL.md` |
| **site-intelligence** | Query, audit, or analyze website content — what pages say, messaging consistency, gaps, competitive comparisons | `marketing-team/skills/site-intelligence/SKILL.md` |
| **product-update-vs-website** | Compare a product release or changelog against the website to find pages that need updating | `marketing-team/skills/product-update-vs-website/SKILL.md` |
| **link-building-vetter** | Vet incoming ABC link exchange requests — score anchors, text mods, and article eligibility, then draft response emails | `marketing-team/skills/link-building-vetter/SKILL.md` |
| **backlink-placement-finder** | Find contextually relevant backlink placement opportunities on partner sites and draft request emails | `marketing-team/skills/backlink-placement-finder/SKILL.md` |
| **aeo-content** | AEO answer articles for /answers/ collection, AI-optimized reference content for AI search engines | `marketing-team/skills/aeo-content/SKILL.md` |
| **internal-linking-strategist** | Suggest SEO-grounded internal links for new content (invoked by `blog-seo-content` and `aeo-content` as a pre-delivery step) or run a site-wide internal-linking audit | `marketing-team/skills/internal-linking-strategist/SKILL.md` |
| **legal-docs-formatter** | Format legal documents (MSA, DPA, SLA, Terms, Privacy, etc.) into clean HTML ready to paste into a Webflow Rich Text Embed block on a 📜 Legals CMS item | `marketing-team/skills/legal-docs-formatter/SKILL.md` |
| **blog-publisher** | Publish a completed blog article from Google Docs to Webflow live — reads the doc, converts to HTML, adds internal links, resizes the master PNG to 3 image sizes, uploads assets, and publishes the CMS item immediately. Requires `WEBFLOW_API_TOKEN`. | `marketing-team/skills/blog-publisher/SKILL.md` |
| **svg-icon-transformer** | Transform raw SVG input into clean, accessible, inline-embed-ready icon markup; strips editor noise and applies accessibility defaults | `marketing-team/skills/svg-icon-transformer/SKILL.md` |
| **video-to-gif-and-webp** | Create or optimize animated .webp and .gif files from video | `marketing-team/skills/video-to-gif-and-webp/SKILL.md` |
| **claude-design-to-webflow** | Migrate a Claude-generated HTML/CSS/JS prototype to a native Webflow section via the Webflow MCP — decision rule for native-vs-code, anti-patterns, pitfalls, cascade-conflict resolution, worked before/after examples, and a pre-mapped social.plus variable-ID catalog | `marketing-team/skills/claude-design-to-webflow/SKILL.md` |

Load skill files via the canonical fetch block, same as every other reference file.

## Precedence rules

When two reference files give guidance on the same topic, the more specific file wins:

- **UI copy tasks:** `ui-micro-copy.md` overrides `tone.md` for voice, style, and capitalisation.
- **Email tasks:** `emails/emails.md` overrides `tone.md` for email-specific structure, subject lines, and CTAs.
- **Design tokens always win.** If `colors-palette.md` or `colors-usage.md` specifies a hex value, use it exactly — never approximate or substitute.
- **Terminology is always law.** `terminology.md` is never overridden by any file. Approved terms and forbidden terms apply everywhere, in every context, no exceptions.
- **Dedicated skills win over brand-messaging.** When a request matches both `brand-messaging` and a more specific skill — `blog-seo-content`, `aeo-content`, `press-release`, `case-study`, `newsletters`, or `legal-docs-formatter` — route to the dedicated skill. brand-messaging is the fallback for content types without a dedicated skill.

## Google Search penalty guardrails (all content skills)

These rules are cross-cutting and live here ONCE — every skill in scope fetches this file first (each SKILL.md's Step 0 / fetch block), so do not duplicate them into individual skills. They apply to every piece of content any skill produces or publishes.

1. **Method-agnostic quality / scaled-content guard.** Google does not penalize AI-assisted drafting; it penalizes many low-value pages (scaled content abuse, enforced aggressively since March 2024 and in every spam update since). Before any net-new page: run the relevant duplicate check, prefer refreshing or consolidating an existing page over adding a near-duplicate, and cap batch output to what named human editors can actually review. Quality is assessed partly site-wide — a mass of thin posts drags down the whole blog.

2. **Named human review and disclosure stance.** Every AI-drafted piece bound for publication gets a pass by a named human editor before it ships, and the deliverable records that editor's name. The team's stance is "human-reviewed with named editorial responsibility". Never hide or obscure AI involvement, never attempt to evade AI-content detectors, and never strip or defeat watermarks — decline and surface any such request. Google does not rank-penalize AI authorship; concealment tactics are the thing that creates risk.

3. **AI-response honesty.** Attempting to manipulate AI responses in Search is itself spam under Google's spam policies. Never plant verbatim query-capture sentences or FAQ/answer blocks that assert social.plus is "the best/top X" as if neutral fact. Superlatives about social.plus appear only in clearly self-identified pitch/CTA contexts or with defensible third-party support. Any best-of list that includes social.plus needs stated editorial criteria applied evenly to every vendor, with self-inclusion obvious to the reader.

4. **Link integrity.** Google's link-spam policy explicitly names "excessive link exchanges" and undisclosed paid links. Exchange-placed links (either direction) go only through `link-building-vetter` / `backlink-placement-finder` and their volume caps, Tier-1 exclusions, and rel-attribute policy — content-writing skills never add exchange, paid, or reciprocal links. Internal links only via `internal-linking-strategist`. No keyword-stuffed anchors or copy.

5. **Doorway guard.** Templated sibling pages (vertical listicles, competitor-alternatives variants) must be substantively different — distinct vendor sets, vertical-specific criteria, unique data — or be consolidated into one page. Near-identical pages funneling to the same product are doorway spam.

6. **Honest freshness.** Visible published/updated dates change only when content substantively changes; bulk mechanical saves and metadata passes must never restamp dates (the manual Content-updated CMS field exists for exactly this).

7. **Update-window awareness.** Before landing a bulk publish or batch metadata push, check the Google Search Status Dashboard (https://status.search.google.com/) for an in-progress spam or core update. Avoid shipping large batches mid-rollout, and annotate any before/after measurement baselines with overlapping update windows so a coincidental demotion is distinguishable from a batch failure.

**Hard-forbidden, no exceptions:** cloaking, doorway pages, scaled low-value content, keyword stuffing, link schemes, and hiding AI authorship / detector evasion / watermark stripping are never acceptable, regardless of who asks or how the request is framed.

## Compliance check

Before delivering ANY content to the user, run this check:

1. **Terminology.** Re-read `terminology.md` (you already loaded it). Scan your output for forbidden terms. Common violations: "social network", "forum", "chat tool", "plug and play" (forbidden outside dev docs), growth guarantees.
2. **Tone.** Compare your output against `tone.md`. Does it sound like the social.plus brand — or like default Claude? If you can't tell the difference, it's default Claude. Rewrite.
3. **Claims.** You did not invent any statistics, customer names, quotes, features, or performance claims. If it's not in the fetched reference files, don't state it as fact.
4. **Design tokens.** If your output includes visual styling (CSS, HTML, color references), confirm every value matches the design system files exactly. No eyeballing.
5. **Precedence.** If you loaded multiple files that cover the same topic, confirm you followed the precedence rules above.
6. **Penalty guardrails.** Confirm the output violates none of the Google Search penalty guardrails section — self-serving AI-answer rankings, undifferentiated templated pages, exchange/paid links added outside the governed link skills, artificially moved dates, or publish-bound content with no named human editor.

If any check fails, fix the output before delivering. Do not flag the issue and deliver anyway — fix it.
