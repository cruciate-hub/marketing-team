# Marketing Plugin

Shared plugin for the marketing team. Ensures all content Claude produces aligns with the latest brand messaging, design system, and website content.

## Skills (17)

### Content creation

| Skill | Lines | Size | What it does | SKILL.md |
|---|---:|---:|---|---|
| [brand-messaging](../docs/brand-messaging.md) | 43 | 1.9 KB | Primary skill for content about a social.plus product/feature/module/capability where no format-specific skill applies (feature pages, product blog posts incl. SEO blog format, release-note CMS items, taglines, pitch materials). | [SKILL.md →](./skills/brand-messaging/SKILL.md) |
| [blog-seo-content](../docs/blog-seo-content.md) | 365 | 22.0 KB | SEO-optimized blog posts for social.plus/blog on **non-product topics only** — industry trends, opinion, listicles. Product blogs go to `brand-messaging`. Drafts run through a deterministic compliance gate (`scripts/compliance.py`) before delivery; `--scan-text` mode vets linker-supplied anchors. Regression suite under `tests/`. | [SKILL.md →](./skills/blog-seo-content/SKILL.md) |
| [newsletters](../docs/newsletters.md) | 172 | 9.9 KB | Generates MailerLite-compatible HTML emails — product update emails, feature launch announcements, campaign emails, and one-off marketing emails. | [SKILL.md →](./skills/newsletters/SKILL.md) |
| [case-study](../docs/case-study.md) | 286 | 14.3 KB | Customer stories and success case studies. | [SKILL.md →](./skills/case-study/SKILL.md) |
| [aeo-content](../docs/aeo-content.md) | 138 | 8.0 KB | AEO (Answer Engine Optimization) articles for the /answers/ collection, structured for AI search engine citation. | [SKILL.md →](./skills/aeo-content/SKILL.md) |
| [press-release](../docs/press-release.md) | 181 | 11.4 KB | Newswire-ready press releases as `.docx` files for PR Newswire / Cision, embargoed announcements, and direct media pitches. | [SKILL.md →](./skills/press-release/SKILL.md) |

### Design & analysis

| Skill | Lines | Size | What it does | SKILL.md |
|---|---:|---:|---|---|
| [design-system](../docs/design-system.md) | 43 | 1.9 KB | Fetches the full visual design system — colors, typography, spacing, buttons, layout, accessibility, and more. | [SKILL.md →](./skills/design-system/SKILL.md) |
| [site-intelligence](../docs/site-intelligence.md) | 308 | 17.0 KB | Queries, audits, and analyzes the 10 website inventory files — marketing pages, industry, use cases, blog, glossary, answers, customer stories, release notes, product updates, and webinars. | [SKILL.md →](./skills/site-intelligence/SKILL.md) |
| [product-update-vs-website](../docs/product-update-vs-website.md) | 190 | 11.0 KB | Compares product updates against website content to find gaps. | [SKILL.md →](./skills/product-update-vs-website/SKILL.md) |
| [claude-design-to-webflow](../docs/claude-design-to-webflow.md) | 501 | 32.6 KB | Migrates a Claude-generated HTML/CSS/JS prototype into native Webflow elements via the Webflow MCP. Decision rule for native-vs-code, anti-pattern catalog (9), pitfalls (14), worked before/after examples, plus a pre-mapped social.plus variable-ID catalog so property bindings skip a `query_variables` round-trip. | [SKILL.md →](./skills/claude-design-to-webflow/SKILL.md) |

### SEO & linking

| Skill | Lines | Size | What it does | SKILL.md |
|---|---:|---:|---|---|
| [internal-linking-strategist](../docs/internal-linking-strategist.md) | 647 | 41.1 KB | Suggests SEO-grounded internal links for new content (invoked by `blog-seo-content` and `aeo-content`), runs site-wide link audits with Structure Score + Anchor Score, and proposes inbound edits when a new page ships (Reverse mode). Uses a canonical anchor map, cannibalization warnings, link budgets for 14 article types, and authority-flow rules from `link-strategy.md`, with live page-fetch to verify insertion points. | [SKILL.md →](./skills/internal-linking-strategist/SKILL.md) |
| [link-building-vetter](../docs/link-building-vetter.md) | 111 | 4.6 KB | Vets incoming ABC link exchange requests, scores them 1-10, and drafts response emails. | [SKILL.md →](./skills/link-building-vetter/SKILL.md) |
| [backlink-placement-finder](../docs/backlink-placement-finder.md) | 872 | 82.6 KB | Finds contextually relevant backlink placement opportunities on partner sites and drafts request emails. | [SKILL.md →](./skills/backlink-placement-finder/SKILL.md) |

### Formatting & conversion

| Skill | Lines | Size | What it does | SKILL.md |
|---|---:|---:|---|---|
| [legal-docs-formatter](../docs/legal-docs-formatter.md) | 211 | 7.1 KB | Converts legal documents (MSA, DPA, SLA, Terms, Privacy, etc.) into clean HTML ready to paste into a Webflow Rich Text Embed block on a 📜 Legals CMS item. | [SKILL.md →](./skills/legal-docs-formatter/SKILL.md) |
| [svg-icon-transformer](../docs/svg-icon-transformer.md) | 168 | 7.6 KB | Transforms SVG input into clean, accessible, inline-embed-ready icon markup. Strips editor noise, applies accessibility defaults, and uses `1em` sizing that avoids the Safari flex/absolute collapse bug. | [SKILL.md →](./skills/svg-icon-transformer/SKILL.md) |
| [video-to-gif-and-webp](../docs/video-to-gif-and-webp.md) | 227 | 12.0 KB | Creates or optimizes animated .webp and .gif files from YouTube videos, local video files, or existing animated images. Guided intake, auto-iteration to hit file size targets, preset dimensions for webinars, product updates, customer stories, and email newsletters. | [SKILL.md →](./skills/video-to-gif-and-webp/SKILL.md) |

### Publishing & CMS

| Skill | Lines | Size | What it does | SKILL.md |
|---|---:|---:|---|---|
| [blog-publisher](../docs/blog-publisher.md) | 380 | 18 KB | Publishes a completed blog article from Google Docs to Webflow — reads the doc, converts to HTML (year/count-free slug, H3 platform entries, comparison table in a Webflow Embed), adds internal links via `internal-linking-strategist` (deterministic `apply_internal_links.py`), resizes the master PNG to 3 WebP sizes, uploads via Data API v2, and publishes (`--staged` to review first). Side-effect-free `--dry-run` validates the whole payload; `--update <item_id>` refreshes hero images on an existing post in one command. Publish engine is stdlib-only (resize helper uses Pillow). Requires `WEBFLOW_API_TOKEN` with cms:write + assets:write. Helper scripts at repo-root `scripts/`. | [SKILL.md →](./skills/blog-publisher/SKILL.md) |

## How it works

Each skill loads its reference files via a shallow `git clone --depth 1` of this repo into `$MT_REPO` (default `/tmp/cruciate-hub-marketing-team`) once per session. The canonical fetch block at the top of every fetch-using SKILL.md handles the clone and validation; skills then read individual files with `cat "$MT_REPO/<path>"`. All skills also load `brain.md` (the main brain) which provides cross-domain routing, precedence rules, and a compliance check. The actual content lives at:

- [`messaging/`](../messaging) — Brand messaging files (tone, terminology, positioning, narrative, boilerplates, UI micro-copy)
- [`design-system/`](../design-system) — Full visual design system (colors, typography, spacing, buttons, shadows, layout, accessibility, and more)
- [`assets/`](../assets) — Official logo SVGs
- [`emails/`](../emails) — Email template reference, strategy guide, and HTML examples
- [`website/`](../website) — Live website content JSON files (10 inventories: marketing, industry, use cases, blog, glossary, answers, customer stories, release notes, product updates, webinars) auto-updated by a Cloudflare Worker on every Webflow publish

## Installation

Install via the marketplace in Claude Cowork, or download the plugin folder and install manually. Works in any environment with `git` and `bash` (Cowork, Claude Desktop, Claude Code).

## Updating content

Edit the markdown files in `messaging/` or `design-system/` on GitHub and push to `main`. The next teammate session does a `git pull --ff-only` and picks up the change — no plugin reinstall needed.

Skill logic changes (SKILL.md files) ride along with the same pull and don't require manual reinstall either, but bumping the plugin version (in `.claude-plugin/marketplace.json` and `marketing-team/.claude-plugin/plugin.json`) forces a session-snapshot refresh, which is the cleanest way to roll out behavioral changes.
