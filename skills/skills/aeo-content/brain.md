# AEO Content — Router

This file is the entry point for all AEO (Answer Engine Optimization) content tasks. It tells you which files to fetch based on what the user needs.

AEO articles are published to the social.plus `/answers/` CMS collection. They are structured to be indexed and cited by AI search engines like ChatGPT, Claude, Perplexity, Gemini, Google AI Overview, and Copilot.

All files are hosted at:
`https://github.com/cruciate-hub/marketing-team/blob/main/skills/skills/aeo-content/`

**Warning:** Always use `github.com/.../blob/...` URLs when fetching. Never convert to `raw.githubusercontent.com` or `api.github.com` — both are blocked by network egress restrictions and will fail.

## Routing table

### Write an AEO article

Fetch all three:
- `article-generation.md` — Purpose, audience, output format, and generation instructions.
- `article-structure.md` — Exact section-by-section template, table patterns, FAQ format, social.plus pitch wording.
- `writing-style.md` — AEO-specific writing rules + pointers to brand messaging files (terminology, tone, narrative, positioning, value story).

## Rules

- Always load `writing-style.md` when generating any written content. It ensures brand compliance.
- The output is a clean, readable article — not HTML. Joy (or another team member) pastes it into a Google Doc. The Make.com pipeline handles HTML conversion and Webflow publishing separately.
- Never invent statistics, customer names, quotes, or performance claims. Only use data from fetched reference files.
- Run the compliance check from the main `brain.md` before delivering.
