# Marketing Plugin

Shared plugin for the marketing team. Ensures all content Claude produces aligns with the latest brand messaging, design system, and website content.

## Skills (19)

### Content creation

| Skill | Lines | Size | What it does | SKILL.md |
|---|---:|---:|---|---|
| [brand-messaging](../docs/brand-messaging.md) | 124 | 7.6 KB | Non-blog marketing content: feature pages, landing pages, homepage copy, product descriptions, release-note CMS items, product updates, taglines, pitch materials, investor copy, and brand voice audits. NOT for blog posts (use blog-seo-content for any topic). | [SKILL.md →](./skills/brand-messaging/SKILL.md) |
| [blog-seo-content](../docs/blog-seo-content.md) | 431 | 26.1 KB | SEO-optimized blog posts for social.plus/blog — any topic (product features, industry trends, opinion, listicles). Default output is a styled Google Doc / .docx for team review; HTML field-by-field for Webflow is opt-in. Loads the full messaging stack for brand voice. Drafts run through a deterministic compliance gate (`scripts/compliance.py`) before delivery; `--scan-text` mode vets linker-supplied anchors. Regression suite under `tests/`. | [SKILL.md →](./skills/blog-seo-content/SKILL.md) |
| [newsletters](../docs/newsletters.md) | 242 | 16.6 KB | Generates MailerLite-compatible HTML emails — product update emails, feature launch announcements, campaign emails, and one-off marketing emails. | [SKILL.md →](./skills/newsletters/SKILL.md) |
| [case-study](../docs/case-study.md) | 422 | 27.2 KB | Customer stories and success case studies. | [SKILL.md →](./skills/case-study/SKILL.md) |
| [aeo-content](../docs/aeo-content.md) | 530 | 38.0 KB | AEO (Answer Engine Optimization) articles for the /answers/ collection, structured for AI search engine citation. | [SKILL.md →](./skills/aeo-content/SKILL.md) |
| glossary-content | 300 | 28 KB | Glossary entries for /glossary/ — six fixed sections, at least one table, answer-first definition, 500–900 words; deterministic compliance gate (`scripts/compliance.py`). Publishes through `webflow-publisher` once the Glossary field slugs are confirmed. | [SKILL.md →](./skills/glossary-content/SKILL.md) |
| [press-release](../docs/press-release.md) | 269 | 17.3 KB | Newswire-ready press releases as `.docx` files for PR Newswire / Cision, embargoed announcements, and direct media pitches. | [SKILL.md →](./skills/press-release/SKILL.md) |

### Design & analysis

| Skill | Lines | Size | What it does | SKILL.md |
|---|---:|---:|---|---|
| [design-system](../docs/design-system.md) | 113 | 7.1 KB | Fetches the full visual design system — colors, typography, spacing, buttons, layout, accessibility, and more. | [SKILL.md →](./skills/design-system/SKILL.md) |
| [site-intelligence](../docs/site-intelligence.md) | 399 | 24.5 KB | Queries, audits, and analyzes the 10 website inventory files — marketing pages, industry, use cases, blog, glossary, answers, customer stories, release notes, product updates, and webinars. | [SKILL.md →](./skills/site-intelligence/SKILL.md) |
| [product-update-vs-website](../docs/product-update-vs-website.md) | 287 | 18.2 KB | Compares product updates against website content to find gaps. | [SKILL.md →](./skills/product-update-vs-website/SKILL.md) |
| [claude-design-to-webflow](../docs/claude-design-to-webflow.md) | 95 | 23.3 KB | Migrates a Claude-generated HTML/CSS/JS prototype into native Webflow elements via the Webflow MCP. Decision rule for native-vs-code, anti-pattern catalog (10), pitfalls (45), worked before/after examples, plus a pre-mapped social.plus variable-ID catalog so property bindings skip a `query_variables` round-trip. | [SKILL.md →](./skills/claude-design-to-webflow/SKILL.md) |

### SEO & linking

| Skill | Lines | Size | What it does | SKILL.md |
|---|---:|---:|---|---|
| [internal-linking-strategist](../docs/internal-linking-strategist.md) | 657 | 41.1 KB | Suggests SEO-grounded internal links for new content (invoked by `blog-seo-content` and `aeo-content`), runs site-wide link audits with Structure Score + Anchor Score, and proposes inbound edits when a new page ships (Reverse mode). Uses a canonical anchor map, cannibalization warnings, link budgets for 14 article types, and authority-flow rules from `link-strategy.md`, with live page-fetch to verify insertion points. | [SKILL.md →](./skills/internal-linking-strategist/SKILL.md) |
| [link-building-vetter](../docs/link-building-vetter.md) | 122 | 5.5 KB | Vets incoming ABC link exchange requests, scores them 1-10, and drafts response emails. | [SKILL.md →](./skills/link-building-vetter/SKILL.md) |
| [backlink-placement-finder](../docs/backlink-placement-finder.md) | 909 | 93.3 KB | Finds contextually relevant backlink placement opportunities on partner sites and drafts request emails. | [SKILL.md →](./skills/backlink-placement-finder/SKILL.md) |

### Formatting & conversion

| Skill | Lines | Size | What it does | SKILL.md |
|---|---:|---:|---|---|
| [legal-docs-formatter](../docs/legal-docs-formatter.md) | 210 | 7.0 KB | Converts legal documents (MSA, DPA, SLA, Terms, Privacy, etc.) into clean HTML ready to paste into a Webflow Rich Text Embed block on a 📜 Legals CMS item. | [SKILL.md →](./skills/legal-docs-formatter/SKILL.md) |
| [svg-icon-transformer](../docs/svg-icon-transformer.md) | 168 | 7.6 KB | Transforms SVG input into clean, accessible, inline-embed-ready icon markup. Strips editor noise, applies accessibility defaults, and uses `1em` sizing that avoids the Safari flex/absolute collapse bug. | [SKILL.md →](./skills/svg-icon-transformer/SKILL.md) |
| [video-to-gif-and-webp](../docs/video-to-gif-and-webp.md) | 226 | 10.0 KB | Creates or optimizes animated .webp and .gif files from YouTube videos, local video files, or existing animated images. Guided intake, auto-iteration to hit file size targets, preset dimensions for webinars, product updates, customer stories, and email newsletters. | [SKILL.md →](./skills/video-to-gif-and-webp/SKILL.md) |

### Publishing & CMS

| Skill | Lines | Size | What it does | SKILL.md |
|---|---:|---:|---|---|
| [webflow-publisher](../docs/webflow-publisher.md) | 250 | 16 KB | Shared publishing engine for any Webflow CMS collection. Takes the common markdown intermediate (the `.draft.md` the writing skills already produce) plus a per-collection field map (each content-type skill's own `webflow-fields.json`: IDs, field slugs, taxonomy, exact image sizes, slug rules — this skill owns none itself), converts to Webflow rich-text HTML (tables in an Embed block, full-width figures, same-tab internal links), resizes images (Pillow), validates side-effect-free (`--dry-run`, incl. structural table checks and a hard fail on unconfirmed slugs), and creates (`--staged` optional), rewrites (`--replace`) or refreshes images (`--update`) via the Data API v2. Stdlib-only engine; regression suite under `tests/`. Blog and Glossary field maps are ready; Answers awaits confirmed slugs. Requires `WEBFLOW_API_TOKEN`. | [SKILL.md →](./skills/webflow-publisher/SKILL.md) |
| [blog-publisher](../docs/blog-publisher.md) | 420 | 24 KB | Blog adapter on top of `webflow-publisher`: reads a Google Doc listicle, normalizes the export into the shared intermediate (`gdoc_to_fielddata.py`: year/count-free slug, H3 platform entries, comparison table in a Webflow Embed), adds internal links via `internal-linking-strategist` (deterministic `apply_internal_links.py`), matches a related webinar, resizes the master PNG to 3 WebP sizes and publishes (`--staged` to review first, `--update` to refresh hero images). Same positional CLI as before (`blog-publisher.py`, `resize_blog_images.py` are wrappers over the shared engine). Requires `WEBFLOW_API_TOKEN` with cms:write + assets:write. | [SKILL.md →](./skills/blog-publisher/SKILL.md) |

## How it works

Each skill loads its reference files via a shallow `git clone --depth 1` of this repo into `$MT_REPO` (default `/tmp/cruciate-hub-marketing-team`) once per session. The canonical fetch block at the top of every fetch-using SKILL.md handles the clone and validation; skills then read individual files with `cat "$MT_REPO/<path>"`. All skills also load `brain.md` (the main brain) which provides cross-domain routing, precedence rules, and a compliance check. The actual content lives at:

- [`messaging/`](../messaging) — Brand messaging files (tone, terminology, positioning, narrative, boilerplates, UI micro-copy)
- [`design-system/`](../design-system) — Full visual design system (colors, typography, spacing, buttons, shadows, layout, accessibility, and more)
- [`assets/`](../assets) — Official logo SVGs
- [`emails/`](../emails) — Email template reference, strategy guide, and HTML examples
- [`website/`](../website) — Website content JSON files (10 inventories: marketing, industry, use cases, blog, glossary, answers, customer stories, release notes, product updates, webinars). The live copies are auto-committed by a Cloudflare Worker to the `site-data` branch on every Webflow publish; the fetch block overlays that branch, so skills always read fresh data while `main` keeps a snapshot

## Installation

Install via the marketplace in Claude Cowork, or download the plugin folder and install manually. Works in any environment with `git` and `bash` (Cowork, Claude Desktop, Claude Code).

## Updating content

Edit the markdown files in `messaging/` or `design-system/` on GitHub and push to `main`. The next teammate session does a `git pull --ff-only` and picks up the change — no plugin reinstall needed.

Skill logic changes (SKILL.md files) ride along with the same pull and don't require manual reinstall either, but bumping the plugin version (in `marketing-team/.claude-plugin/plugin.json` — the single source of truth; the marketplace entry deliberately carries no version) forces a session-snapshot refresh, which is the cleanest way to roll out behavioral changes.
