# Marketing Team

Shared plugin marketplace and brand reference for social.plus. Skills load content live from this repo via a shallow git clone (`git clone --depth 1`) at the start of each session, so updates pushed here propagate to every teammate's next skill run — no plugin reinstall needed.

## Which plugin should I install?

This marketplace ships **two plugins** — install one, not both.

| Plugin | Who it's for | Skills | Install command |
|---|---|---|---|
| **`marketing-team`** | The marketing team — full kit | 14 skills (content, design, SEO, linking, formatting) | `/plugin install marketing-team@cruciate-hub` |
| **`brand-kit`** | Everyone else | 2 skills: `brand-messaging`, `design-system` | `/plugin install brand-kit@cruciate-hub` |

Both plugins read from the same source files (`brand-kit`'s skills are symlinks into `marketing-team`), so brand voice, terminology, and design tokens are always consistent across the company. See the [`brand-kit/`](./brand-kit) folder for that plugin's README and full install walkthrough.

## Installation

A click-by-click visual guide with annotated screenshots walks you through opening the marketplace, installing the right plugin for your role, and turning on auto-sync. Takes about two minutes — you only do this once.

<a href="./docs/install.md">
  <img alt="Open the install guide" src="https://img.shields.io/badge/%F0%9F%93%96%20Open%20the%20install%20guide-1f6feb?style=for-the-badge">
</a>

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
| [`marketing-team/`](./marketing-team) | `marketing-team` plugin — the 14 skill definitions that fetch from the folders above |
| [`brand-kit/`](./brand-kit) | `brand-kit` plugin — a 2-skill subset (`brand-messaging`, `design-system`), symlinked from `marketing-team/` so updates flow automatically |

## How updates work

**Reference content** (markdown files in `messaging/`, `design-system/`, `emails/`): Edit on GitHub, changes are live for all team members on their next session — no version bump needed, no reinstall needed.

**Skill logic** (SKILL.md files in `marketing-team/skills/`): A change requires a `version` bump in `marketplace.json` (and the matching `plugin.json`). Teammates with auto-sync on (Steps 8–11 of the [install guide](./docs/install.md)) pick it up automatically at next Claude desktop startup. Anyone without auto-sync needs to run `/plugin marketplace update cruciate-hub` and `/plugin update <plugin>@cruciate-hub` once.

**Website snapshots** (`website/pages-*.json`): 10 auto-generated JSON files covering every published page on social.plus — marketing, industry, use cases, blog, glossary, answers, customer stories, release notes, product updates, and webinars. Regenerated by a Cloudflare Worker on every Webflow publish (site publish refreshes marketing + industry; per-collection CMS publish refreshes the rest).
