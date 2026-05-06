# Product Update vs Website

Claude skill for comparing new product releases or monthly updates against the current social.plus website content to identify gaps — pages that should mention a new feature but don't yet.

Given a release note, monthly product update, or changelog entry, this skill scans marketing, industry, and use-case pages, identifies every page that's missing relevant features, and drafts copy suggestions that match each page's tone and structure.

## What it does

- Loads the current site content from three JSON files (`pages-marketing.json`, `pages-industry.json`, `pages-use-cases.json`) and merges them into a single dataset.
- Extracts every distinct feature, capability, or improvement from the user's product update.
- Cross-references each feature against every page — feature pages, product landing pages, use case pages, industry pages, homepage, pricing.
- Runs a **mandatory dedicated pricing pass** to check whether new features should appear as line items in the `/pricing` comparison table.
- Outputs a gap report grouped by page, with priority-tagged suggestions and draft copy that matches the existing page's tone.

## When it triggers

When the user pastes a release note, monthly product update, or changelog entry and wants to know which website pages need updating. Trigger phrases include "what's missing from the site", "does the website reflect this update", "which pages need to change", or references to `pages-marketing.json`.

Always use this skill for any product-update-to-website comparison, even if the user doesn't explicitly name it.

## Workflow

1. Fetch `brain.md` (main brain).
2. Fetch all three site-content JSONs and merge their `pages` arrays:
   - `website/pages-marketing.json` — static marketing pages (homepage, pricing, product, feature/SDK/UIKit, white-label, vs-stream)
   - `website/pages-industry.json` — all `/industry/*` pages
   - `website/pages-use-cases.json` — all `/use-case/*` pages
3. Load brand guidelines via `messaging/brain.md` — at minimum, `terminology.md`, `tone.md`, `positioning.md`, `boilerplates.md`.
4. Read the full product update. Extract every feature, capability, or improvement.
5. For each feature, scan ALL pages (not just obvious ones) — a chat feature might be relevant to a use case or industry page.
6. **Run the dedicated pricing pass** — verify every new feature against the `/pricing` comparison table as a separate step.
7. Output a gap report grouped by page. Run the compliance check from `brain.md`.

## Pages covered

### Product feature pages (most likely to have gaps)
`/social/features`, `/chat/features`, `/video/features`, `/analytics`, `/moderation`, `/monetization`

### Product landing pages
`/product`, `/social`, `/chat`, `/video`, `/social/sdk`, `/chat/sdk`, `/video/sdk`, `/social/uikit`, `/chat/uikit`

### Use case pages
`/use-case/1-1-chat`, `/use-case/activity-feed`, `/use-case/custom-posts`, `/use-case/group-chat`, `/use-case/groups`, `/use-case/live-chat`, `/use-case/livestream`, `/use-case/polls`, `/use-case/stories-and-clips`, `/use-case/user-profiles`

### Industry pages
`/industry/retail`, `/industry/fitness`, `/industry/travel`, `/industry/sports`, `/industry/health-and-wellness`, `/industry/fintech`, `/industry/media-and-news`, `/industry/edtech`, `/industry/gaming`, `/industry/betting`

### Other
`/` (homepage), `/pricing`

## Gap detection logic

For each new feature:

1. Identify the product area (Social / Chat / Video / Analytics / Moderation / Monetization).
2. Check the primary features page — does it list this feature?
3. Check the product landing page — does it mention this capability?
4. Check relevant use case pages.
5. Check relevant industry pages.
6. Check `/pricing` — new line item, changed Core/Max availability, add-on status, AI feature limit, or new feature group.

### Mandatory pricing pass (separate, dedicated step)

After the page-by-page scan, run a dedicated pricing check: take every new feature and verify it exists as a line item in the `/pricing` comparison table. If a feature is missing and is comparable in granularity to existing line items (e.g., "Feed Pagination", "Change User Roles", "Poll Posts"), flag it as a pricing gap. This step runs **even if no other pricing gaps were found**.

### What counts as a gap
- The feature name doesn't appear anywhere on the page.
- The feature exists but the description is outdated or doesn't match the new capability.
- A use case or industry page describes a workflow this feature enables but doesn't mention it.
- A new feature is missing from the `/pricing` comparison table as a line item.

### What does NOT count as a gap
- The feature is already listed with an accurate description.
- The feature is too granular for a landing page (SDK-level detail on a marketing page).
- The page covers a different product area entirely.

## Output format

### Summary (first)

Start with a link to the release note + short paragraph summarizing what was found:

> Release note: https://www.social.plus/release-note/event-creation-and-management-on-console
>
> Found 6 gaps across 6 pages — 1 high priority, 3 medium, 2 low. The primary gap is on /social/features where events are not listed as a feature at all.

### Gap entries (grouped by page)

Each page gets its own section. Format rules are strict (output is emailed; inconsistency looks unprofessional):

- Page URL as heading with 🔍 prefix: `🔍 [URL](URL)`
- Blank line after the URL heading
- Field labels in **bold** with colon
- **Suggested copy** wrapped in a blockquote (`>`) for highlight rendering
- No horizontal rules (`---`) between entries — the heading + blank line is enough separation
- Priority uses colored circle emoji inline (🔴 🟡 🟢)

Example:

```
🔍 [https://www.social.plus/social/features](https://www.social.plus/social/features)

**Feature:** Event creation and management
**Section:** Communities
**Status:** Missing — no mention of events anywhere on this page
**Suggested heading:** Event Creation and Management
> **Suggested copy:** Enable admins and moderators to create and manage digital live streams, virtual events, and in-person gatherings. Events surface automatically across group tabs, the Event Hub, and community feeds.

**Priority:** 🔴 High — primary features page missing this entirely
```

### Priority guide
- 🔴 **High** — primary features page for the product area is missing the feature entirely
- 🟡 **Medium** — landing page or relevant use case page could benefit from mentioning it
- 🟢 **Low** — industry page or secondary page could reference it for completeness

### No gaps found
Say so clearly: "✅ No gaps found — the website already reflects this update."

### Files loaded (last)
Always end the report listing which messaging guideline files were actually loaded.

## Files

```
product-update-vs-website/
├── SKILL.md                          Skill entry point — workflow, gap logic, output format
└── README.md                         This file
```

## URL format

All reference files are loaded from a shallow clone of this repo (`git clone --depth 1`) into `$MT_REPO`. The canonical fetch block at the top of each SKILL.md handles the clone; skills then read files with `cat "$MT_REPO/<path>"`.
