# Branding Plugin

The minimum on-brand kit for social.plus — three skills only. Install this if you need to stay on-brand but you're not on the marketing team.

## Skills (3)

| Skill | What it does |
|---|---|
| [brand-messaging](./skills/brand-messaging/SKILL.md) | Brand voice, tone, terminology, positioning, boilerplates. Use for any written copy that represents social.plus. |
| [press-release](./skills/press-release/SKILL.md) | Drafts press releases following social.plus structure — headline, dateline, boilerplate, quote engineering, distribution checklist. |
| [design-system](./skills/design-system/SKILL.md) | Visual reference — colors, typography, spacing, buttons, layout, accessibility. Use for decks, mockups, CSS, or any visual output. |

All three are **symlinks** to the canonical skill files inside the sibling `marketing-team` plugin. There's only one copy on disk; both plugins serve the same up-to-date content. See [Anthropic's docs on share-with-symlinks](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution).

## Who installs this vs `marketing-team`

- **`branding`** — non-marketing teammates who occasionally need brand-consistent output (e.g. an exec drafting a deck, a sales lead writing a customer email, an engineer drafting a launch press release).
- **`marketing-team`** — the marketing team itself. Includes these three plus 11 other skills covering SEO, social media, campaign copy, link strategy, site intelligence, and more.

Install one or the other — not both. (You won't get duplicates if you install both, but there's no benefit either.)

## Installation

```shell
/plugin marketplace add cruciate-hub/marketing-team
/plugin install branding@cruciate-hub
```

After restart, skills are namespaced as `branding:brand-messaging`, `branding:press-release`, `branding:design-system` — and auto-trigger on relevant prompts ("review this for brand voice", "draft a press release about X", "what blue do we use", etc.).

For the full team install guide, see [`branding-plugin-install.md`](https://github.com/cruciate-hub/marketing-team#which-plugin-should-i-install).

## How it stays up to date

Each skill loads its reference files via a shallow `git clone --depth 1` of this repo at runtime, so brand voice updates, design tokens, terminology changes, and press release patterns are always fresh from `main` — no plugin reinstall needed.

When the SKILL.md files themselves change (rare), users run `/plugin marketplace update cruciate-hub` to pick up the new version.
