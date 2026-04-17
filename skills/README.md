# Marketing Plugin

Shared plugin for the marketing team. Ensures all content Claude produces aligns with the latest brand messaging, design system, and website content.

## Skills (12)

### Content creation

| Skill | Lines | Size | What it does |
|---|---:|---:|---|
| [brand-messaging](./skills/brand-messaging/SKILL.md) | 43 | 1.9 KB | Fetches brand guidelines from GitHub and applies them to any written content. |
| [blog-seo-content](./skills/blog-seo-content/SKILL.md) | 230 | 10.5 KB | SEO-optimized blog posts, thought leadership articles, and long-form content. |
| [social-media](./skills/social-media/SKILL.md) | 143 | 5.4 KB | Platform-specific posts for LinkedIn, Instagram, and X. |
| [campaign-copy](./skills/campaign-copy/SKILL.md) | 203 | 6.7 KB | Ad copy, campaign landing pages, and paid media content. |
| [newsletters](./skills/newsletters/SKILL.md) | 172 | 9.9 KB | Generates MailerLite-compatible HTML emails — product update emails, feature launch announcements, campaign emails, and one-off marketing emails. |
| [case-study](./skills/case-study/SKILL.md) | 286 | 14.3 KB | Customer stories and success case studies. |
| [aeo-content](./skills/aeo-content/SKILL.md) | 138 | 8.0 KB | AEO (Answer Engine Optimization) articles for the /answers/ collection, structured for AI search engine citation. |

### Design & analysis

| Skill | Lines | Size | What it does |
|---|---:|---:|---|
| [design-system](./skills/design-system/SKILL.md) | 43 | 1.9 KB | Fetches the full visual design system — colors, typography, spacing, buttons, layout, accessibility, and more. |
| [site-intelligence](./skills/site-intelligence/SKILL.md) | 308 | 17.0 KB | Queries, audits, and analyzes the 10 website inventory files — marketing pages, industry, use cases, blog, glossary, answers, customer stories, release notes, product updates, and webinars. |
| [product-update-vs-website](./skills/product-update-vs-website/SKILL.md) | 190 | 11.0 KB | Compares product updates against website content to find gaps. |

### Link building

| Skill | Lines | Size | What it does |
|---|---:|---:|---|
| [link-building-vetter](./skills/link-building-vetter/SKILL.md) | 111 | 4.6 KB | Vets incoming ABC link exchange requests, scores them 1-10, and drafts response emails. |
| [backlink-placement-finder](./skills/backlink-placement-finder/SKILL.md) | 527 | 40.9 KB | Finds contextually relevant backlink placement opportunities on partner sites and drafts request emails. |

## How it works

Each skill fetches its reference files live from GitHub every time it triggers. All skills also fetch `brain.md` (the main brain) which provides cross-domain routing, precedence rules, and a compliance check. The actual content lives at:

- [`messaging/`](../messaging) — Brand messaging files (tone, terminology, positioning, narrative, boilerplates, UI micro-copy)
- [`design-system/`](../design-system) — Full visual design system (colors, typography, spacing, buttons, shadows, layout, accessibility, and more)
- [`assets/`](../assets) — Official logo SVGs
- [`emails/`](../emails) — Email template reference, strategy guide, and HTML examples
- [`website/`](../website) — Live website content JSON files (10 inventories: marketing, industry, use cases, blog, glossary, answers, customer stories, release notes, product updates, webinars) auto-updated by a Cloudflare Worker on every Webflow publish

## Installation

Install via the marketplace in Claude Cowork, or download the plugin folder and install manually. Works in Cowork and Claude Code (any environment with WebFetch or bash access).

## Updating content

Edit the markdown files in `messaging/` or `design-system/` on GitHub. Changes are live immediately for all team members — no plugin reinstall needed.

Skill logic changes (SKILL.md files) require team members to update the plugin.
