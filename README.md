# Marketing Team

Shared plugin marketplace and brand reference for the marketing team. Skills fetch content live from this repo, so updates here are instantly available to everyone.

## Installation

1. Open Claude Cowork
2. Click **Customize** in the sidebar
3. Next to **Personal plugins**, click **+**
4. Click **Browse plugins** → select the **Personal** tab
5. Click **+** → select **Add marketplace**
6. Enter `cruciate-hub/marketing-team` → click **Sync**
7. Click **Install** on the **product-marketing-team** plugin

When new skills are added to the plugin, click the **three dots** next to the marketplace name to refresh, then **Update** the plugin.

## Available skills (11)

### Content creation

| Skill | What it does |
|---|---|
| **brand-messaging** | Applies brand voice, terminology, tone, and messaging frameworks to any written content. |
| **blog-seo-content** | SEO-optimized blog posts, thought leadership articles, and long-form content. |
| **social-media** | Platform-specific posts for LinkedIn, Instagram, and X with format and tone guidelines. |
| **campaign-copy** | Ad copy, campaign landing pages, and paid media content (Google, LinkedIn, Meta). |
| **newsletters** | Generates MailerLite-compatible HTML emails from monthly product update docs. |
| **case-study** | Customer stories and success case studies following the social.plus narrative structure. |

### Design & analysis

| Skill | What it does |
|---|---|
| **design-system** | Full visual design system — colors, typography, spacing, buttons, layout, accessibility, and more. |
| **site-intelligence** | Queries, audits, and analyzes the 37 marketing pages via the site-content.json snapshot. |
| **product-update-vs-website** | Compares product release notes against live website content to find pages that need updating. |

### Link building

| Skill | What it does |
|---|---|
| **link-building-vetter** | Vets incoming ABC link exchange requests against social.plus guidelines, scores them 1-10, and drafts response emails. |
| **backlink-placement-finder** | Finds contextually relevant backlink placement opportunities on partner websites and drafts request emails. |

## Repo structure

| Path | Purpose |
|---|---|
| [`brain.md`](./brain.md) | Main brain — cross-domain routing, precedence rules, compliance check |
| [`messaging/`](./messaging) | Brand messaging files — tone, terminology, positioning, narrative, boilerplates, UI micro-copy |
| [`design-system/`](./design-system) | Full visual design system — colors, typography, spacing, buttons, shadows, layout, accessibility, and more. [View brand guidelines live](https://cruciate-hub.github.io/marketing-team/design-system/brand-guidelines.html) |
| [`assets/`](./assets) | Official logo SVGs |
| [`emails/`](./emails) | Email template reference, strategy guide, and HTML examples |
| [`website/`](./website) | Live website content JSON (auto-updated on every Webflow publish via Cloudflare Worker) |
| [`skills/`](./skills) | The plugin source — contains the 9 skill definitions that fetch from the folders above |

## How updates work

**Reference content** (markdown files in `messaging/`, `design-system/`, `emails/`): Edit on GitHub, changes are live immediately for all team members. No reinstall needed.

**Skill logic** (SKILL.md files in `skills/`): Changes require team members to update the plugin.

**Website snapshot** (`website/site-content.json`): Regenerated automatically by a Cloudflare Worker on every Webflow publish.
