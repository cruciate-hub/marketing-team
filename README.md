# Marketing Team

Shared plugin marketplace and brand reference for social.plus. Skills load content live from this repo via a shallow git clone (`git clone --depth 1`) at the start of each session, so updates pushed here propagate to every teammate's next skill run — no plugin reinstall needed.

## Which plugin should I install?

This marketplace ships **two plugins** — install one, not both.

| Plugin | Who it's for | Skills | Install command |
|---|---|---|---|
| **`marketing-team`** | The marketing team — full kit | 14 skills (content, design, SEO, linking, formatting) | `/plugin install marketing-team@cruciate-hub` |
| **`brand-kit`** | Everyone else | 3 skills: `brand-messaging`, `press-release`, `design-system` | `/plugin install brand-kit@cruciate-hub` |

Both plugins read from the same source files (`brand-kit`'s skills are symlinks into `marketing-team`), so brand voice, terminology, and design tokens are always consistent across the company. See the [`brand-kit/`](./brand-kit) folder for that plugin's README and full install walkthrough.

## Installation

<table style="width: 100%;">
<thead>
<tr>
<th style="width: 80px; text-align: center;">Step</th>
<th style="text-align: left;">Action</th>
</tr>
</thead>
<tbody>
<tr><td style="text-align: center;">1 🚀</td><td>Open Claude Cowork</td></tr>
<tr><td style="text-align: center;">2 ⚙️</td><td>Click <kbd>Customize</kbd> in the sidebar</td></tr>
<tr><td style="text-align: center;">3 ➕</td><td>Next to <strong>Personal plugins</strong>, click <kbd>+</kbd></td></tr>
<tr><td style="text-align: center;">4 🔍</td><td>Click <kbd>Browse plugins</kbd> → select the <strong>Personal</strong> tab</td></tr>
<tr><td style="text-align: center;">5 🏪</td><td>Click <kbd>+</kbd> → select <strong>Add marketplace</strong></td></tr>
<tr><td style="text-align: center;">6 🔗</td><td>Enter <code>cruciate-hub/marketing-team</code> → click <kbd>Sync</kbd></td></tr>
<tr><td style="text-align: center;">7 ➕</td><td>Click the <kbd>+</kbd> next to <strong>your plugin</strong> to install — <code>marketing-team</code> (marketing team, 14 skills) or <code>brand-kit</code> (everyone else, 3 skills). See "Which plugin should I install?" above.</td></tr>
</tbody>
</table>

Steps 8–11 pull in new skills and skill improvements automatically (whenever a commit lands on `main`). Without them, you'll stay frozen on the version you installed and miss every future update.

<table style="width: 100%;">
<thead>
<tr>
<th style="width: 80px; text-align: center;">Step</th>
<th style="text-align: left;">Action</th>
</tr>
</thead>
<tbody>
<tr><td style="text-align: center;">8 🎛️</td><td>Click the <kbd>⋯</kbd> next to your installed plugin (<code>marketing-team</code> or <code>brand-kit</code>)</td></tr>
<tr><td style="text-align: center;">9 🔵</td><td>Toggle <kbd>Sync automatically</kbd></td></tr>
<tr><td style="text-align: center;">10 🔄</td><td>Click <kbd>Check for updates</kbd></td></tr>
<tr><td style="text-align: center;">11 🔁</td><td>Close and reopen the Claude Desktop App</td></tr>
</tbody>
</table>

![Sync automatically and Check for updates in the Cowork plugin menu](./assets/cowork-sync-automatically.png)

## Available skills (14)

### Content creation

| Skill | What it does |
|---|---|
| **brand-messaging** | Applies brand voice, terminology, tone, and messaging frameworks to any written content. |
| **blog-seo-content** | SEO-optimized blog posts for social.plus/blog. |
| **aeo-content** | AEO (Answer Engine Optimization) articles for the `/answers/` collection, structured for AI search engine citation. |
| **newsletters** | Generates MailerLite-compatible HTML emails from monthly product update docs. |
| **case-study** | Customer stories and success case studies following the social.plus narrative structure. |
| **press-release** | Newswire-ready press releases as `.docx` files for PR Newswire / Cision, embargoed announcements, and direct media pitches. |

### Design & analysis

| Skill | What it does |
|---|---|
| **design-system** | Full visual design system — colors, typography, spacing, buttons, layout, accessibility, and more. |
| **site-intelligence** | Queries, audits, and analyzes the 10 website inventory files (marketing, industry, use cases, blog, glossary, answers, customer stories, release notes, product updates, webinars). |
| **product-update-vs-website** | Compares product release notes against live website content to find pages that need updating. |

### SEO & linking

| Skill | What it does |
|---|---|
| **internal-linking-strategist** | Suggests SEO-grounded internal links for new content (invoked by `blog-seo-content` and `aeo-content`) and runs site-wide link audits. Uses a canonical anchor map and cannibalization warnings from `link-strategy.md`, with live page-fetch to verify insertion points. |
| **link-building-vetter** | Vets incoming ABC link exchange requests against social.plus guidelines, scores them 1-10, and drafts response emails. |
| **backlink-placement-finder** | Finds contextually relevant backlink placement opportunities on partner websites and drafts request emails. |

### Formatting & conversion

| Skill | What it does |
|---|---|
| **legal-docs-formatter** | Converts legal documents (MSA, DPA, SLA, Terms, Privacy, etc.) into clean HTML ready to paste into a Webflow Rich Text Embed block on a 📜 Legals CMS item. |
| **svg-icon-transformer** | Transforms SVG input into clean, accessible, inline-embed-ready icon markup with `1em` sizing and correct accessibility defaults. |

## Repo structure

| Path | Purpose |
|---|---|
| [`brain.md`](./brain.md) | Main brain — cross-domain routing, precedence rules, compliance check |
| [`messaging/`](./messaging) | Brand messaging files — tone, terminology, positioning, narrative, boilerplates, UI micro-copy |
| [`design-system/`](./design-system) | Full visual design system — colors, typography, spacing, buttons, shadows, layout, accessibility, and more. [View brand guidelines live](https://cruciate-hub.github.io/marketing-team/design-system/brand-guidelines.html) |
| [`assets/`](./assets) | Official logo SVGs |
| [`emails/`](./emails) | Email template reference, strategy guide, and HTML examples |
| [`website/`](./website) | Live website content JSON (auto-updated on every Webflow publish via a Cloudflare Worker) |
| [`skills/`](./skills) | `marketing-team` plugin — the 14 skill definitions that fetch from the folders above |
| [`brand-kit/`](./brand-kit) | `brand-kit` plugin — a 3-skill subset (`brand-messaging`, `press-release`, `design-system`), symlinked from `skills/` so updates flow automatically |

## How updates work

**Reference content** (markdown files in `messaging/`, `design-system/`, `emails/`): Edit on GitHub, changes are live immediately for all team members. No reinstall needed.

**Skill logic** (SKILL.md files in `skills/`): Changes require team members to update the plugin.

**Website snapshots** (`website/pages-*.json`): 10 auto-generated JSON files covering every published page on social.plus — marketing, industry, use cases, blog, glossary, answers, customer stories, release notes, product updates, and webinars. Regenerated by a Cloudflare Worker on every Webflow publish (site publish refreshes marketing + industry; per-collection CMS publish refreshes the rest).
