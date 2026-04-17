# Brand Messaging

Claude skill for enforcing social.plus brand messaging consistency across all written content.

This is the generic brand-alignment skill — it routes to the appropriate messaging files based on the task at hand. The source of truth lives on GitHub and is fetched fresh every time, never memorized.

## What it does

- Fetches `brain.md` for cross-domain routing, precedence rules, and the compliance check.
- Fetches `messaging/brain.md` (the messaging router) and follows its instructions to load the specific files the task needs.
- Optionally fetches `design-system/brain.md` when the output includes visual styling.
- Runs the main brain's compliance check before delivering.

## When it triggers

For general marketing copy, blog posts, landing page text, press releases, pitch materials, website copy, product descriptions, investor communications, taglines, subject lines, or any text representing the social.plus brand. Also for reviewing or auditing existing copy against brand guidelines, or when someone asks about brand voice, tone, approved terminology, messaging frameworks, value propositions, competitive positioning, or boilerplates.

The skill is not for:
- HTML email generation — use `newsletters` (handles both copy and HTML with format-specific instructions).
- Social media posts — use `social-media` (loads platform-specific guidelines).
- Blog posts — use `blog-seo-content` (maps to Webflow CMS fields).
- Customer stories — use `case-study` (has CMS-specific structure).
- Ad copy / campaign landing pages — use `campaign-copy` (platform character limits, A/B variants).
- AEO articles — use `aeo-content` (structured for AI citation).

## Workflow

1. Fetch `brain.md` — cross-domain routing, precedence rules, compliance check.
2. Fetch `messaging/brain.md` — the router — and follow its task-specific instructions.
3. If the output includes HTML, CSS, colors, or layout, also fetch `design-system/brain.md`.
4. Run the main brain's compliance check before delivering.

## Why this skill is thin

`brand-messaging` is intentionally minimal — a dispatcher, not a content producer. The heavy lifting lives in the routing layer (`messaging/brain.md`) and the actual guideline files (`terminology.md`, `tone.md`, `narrative.md`, `value-story.md`, `positioning.md`, `boilerplates.md`). Keeping the skill shell small means guideline updates flow through without needing to rewrite this skill.

For format-heavy tasks (emails, social posts, case studies), a dedicated skill loads additional format-specific files that this generic skill does not — which is why those tasks have their own skills.

## Files

```
brand-messaging/
├── SKILL.md                          Skill entry point — minimal, routes to GitHub files
└── README.md                         This file
```

No `references/` subdirectory — all guidelines live in the repo root's `messaging/` and `design-system/` folders and are fetched at runtime.

## URL format

Always fetch via `github.com/.../blob/...` URLs. Never use `raw.githubusercontent.com` — blocked by network egress. This applies to `brain.md` and every file it routes to.
