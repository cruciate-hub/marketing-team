---
name: product-update-vs-website
description: Compare new product releases or monthly updates against the current social.plus website content to identify gaps — pages that should mention a new feature but don't yet. Use this skill when someone pastes a release note, monthly product update, or changelog entry and wants to know which website pages need updating. Also trigger when someone asks "what's missing from the site", "does the website reflect this update", "which pages need to change", or references the site-content.json file. Always use this skill for any product-update-to-website comparison task, even if the user doesn't explicitly name the skill.
---

# Product Update vs Website

Compares social.plus product updates (release notes, monthly updates) against the current website content to identify which marketing pages are missing new features and need updating.

## What to do

1. **Fetch the main brain** for cross-domain routing, precedence rules, and the compliance check:
```
https://github.com/cruciate-hub/marketing-team/blob/main/brain.md
```
2. **Load current site content** from `website/site-content.json` in this repo (or fetch the raw file from GitHub)
3. **Take the product update** — a release note, monthly product update, or changelog entry provided by the user
4. **Cross-reference** every new feature/capability mentioned in the update against every page in the JSON
5. **Output a gap report** showing which pages should mention this feature but currently don't
6. **Draft copy suggestions** for each gap, matching the existing page's tone and structure

## Site content reference

The site content JSON is maintained automatically by a Cloudflare Worker that regenerates it on every Webflow site publish. It lives at:

**Repo path:** `website/site-content.json`
**GitHub URL:** `https://github.com/cruciate-hub/marketing-team/blob/main/website/site-content.json`

The JSON structure:
```json
{
  "_meta": { "generatedAt": "...", "pageCount": 37 },
  "pages": [
    {
      "url": "/social/features",
      "metaTitle": "...",
      "metaDescription": "...",
      "content": "# heading\n## section\n### feature name\nFeature description..."
    }
  ]
}
```

Each page's `content` field preserves heading hierarchy using markdown-style markers (`#`, `##`, `###`).

## Pages covered

### Product feature pages (most likely to have gaps)
- `/social/features` — all social features
- `/chat/features` — all chat/messaging features
- `/video/features` — all video features
- `/analytics` — analytics and insights
- `/moderation` — moderation tools
- `/monetization` — monetization features

### Product landing pages
- `/product` — product overview
- `/social` — social product landing
- `/chat` — chat product landing
- `/video` — video product landing
- `/social/sdk`, `/chat/sdk`, `/video/sdk` — SDK pages
- `/social/uikit`, `/chat/uikit` — UIKit pages

### Use case pages
- `/use-case/1-1-chat`, `/use-case/activity-feed`, `/use-case/custom-posts`, `/use-case/group-chat`, `/use-case/groups`, `/use-case/live-chat`, `/use-case/livestream`, `/use-case/polls`, `/use-case/stories-and-clips`, `/use-case/user-profiles`

### Industry pages
- `/industry/retail`, `/industry/fitness`, `/industry/travel`, `/industry/sports`, `/industry/health-and-wellness`, `/industry/fintech`, `/industry/media-and-news`, `/industry/edtech`, `/industry/gaming`, `/industry/betting`

### Other
- `/` — homepage
- `/pricing` — pricing page

## Gap detection logic

For each new feature or capability in the product update:

1. **Identify the product area** — is this Social, Chat, Video, Analytics, Moderation, or Monetization?
2. **Check the primary features page** — does `/social/features` (or `/chat/features`, `/video/features`) already list this feature by name or description?
3. **Check the product landing page** — does `/social` (or `/chat`, `/video`) mention this capability?
4. **Check relevant use case pages** — would any use case page benefit from mentioning this feature?
5. **Check relevant industry pages** — does any industry page reference this type of capability?
6. **Check pricing** — the `/pricing` page has a detailed Core vs Max feature comparison table organized by group (Chat, Activity Feeds, Communities, Stories, User Profiles, Video, AI, Analytics, Moderation, Security & Compliance, Integrations). For each new feature, check:
   - Should it appear as a **new line item** in the comparison table? (e.g., a new chat capability, a new post type, a new moderation tool)
   - Does it **change the Core/Max availability** of an existing line item? (e.g., a feature moving from Max-only to Core, or a new limit change)
   - Does it affect **add-on status**? (e.g., a feature becoming an add-on, or an add-on becoming included)
   - Does it affect **AI feature limits**? (e.g., Analyze posts/month or Research topics/month changing)
   - Does it introduce a **new feature group** that doesn't exist in the table yet?

### Mandatory pricing pass

After completing the page-by-page scan above, do a **dedicated pricing check**. This is a separate, mandatory step — not optional. Take every new feature from the product update and verify whether it exists as a line item in the `/pricing` comparison table. If a feature is missing from the table and is comparable in granularity to existing line items (e.g., "Feed Pagination", "Change User Roles", "Poll Posts"), flag it as a pricing gap. This step must run even if no other pricing gaps were found during the main scan.

### What counts as a gap
- The feature name does not appear anywhere on the page
- The feature exists but the description is outdated or doesn't match the new capability
- A use case or industry page describes a workflow that this feature enables, but doesn't mention it
- A new feature is missing from the `/pricing` comparison table as a line item

### What does NOT count as a gap
- The feature is already listed with an accurate description
- The feature is too granular for a landing page (SDK-level detail on a marketing page)
- The page covers a different product area entirely

## Output format

Always start with a brief summary, then list each gap grouped by page. Every entry must follow the exact same structure. Every field on its own line with a single line break between fields. Consistent casing. No variations. No double blank lines between fields.

### Summary (always first)

Start every report with a link to the release note or product update, followed by a short paragraph summarizing what was found. Use the slug from the CMS item to construct the URL. Example:

Release note: https://www.social.plus/release-note/event-creation-and-management-on-console

Found 6 gaps across 6 pages — 1 high priority, 3 medium, 2 low. The primary gap is on /social/features where events are not listed as a feature at all.

### Gap entries (grouped by page)

Each page gets its own section. Use the full clickable URL (https://www.social.plus/...) — never just the path. Every field on its own line. Single line break between fields — no double blank lines.

---

https://www.social.plus/social/features
Feature: Event creation and management
Section: Communities
Status: Missing — no mention of events anywhere on this page
Suggested heading: Event Creation and Management
Suggested copy: Enable admins and moderators to create and manage digital live streams, virtual events, and in-person gatherings. Events surface automatically across group tabs, the Event Hub, and community feeds.
Priority: 🔴 High — primary features page missing this entirely

---

https://www.social.plus/use-case/livestream
Feature: Event scheduling and RSVPs
Section: What you get with social.plus
Status: Could be enhanced — lists live video but no scheduling or RSVPs
Suggested heading: Event Scheduling & RSVPs
Suggested copy: Create events in advance, collect RSVPs, and send reminders so your audience is ready when you go live.

---

https://www.social.plus/pricing
Feature: Event Creation and Management
Section: Communities (comparison table)
Status: Missing — no line item for events in the Communities group
Suggested line item: Event Creation and Management: Core=✓, Max=✓
Priority: 🟡 Medium — pricing comparison table should list this alongside other community features
Priority: 🟡 Medium — livestream use case page omits pre-stream planning

---

### Priority guide
- 🔴 High — primary features page for this product area is missing the feature entirely
- 🟡 Medium — landing page or relevant use case page could benefit from mentioning it
- 🟢 Low — industry page or secondary page could reference it for completeness

### No gaps found

If no gaps are found, say so clearly: "✅ No gaps found — the website already reflects this update."

### Files loaded (always last)

Always end the report listing which brand guideline files you actually read and applied. Only list files you loaded — if a file was unavailable or empty, don't list it.

Files loaded:
[list only the files you successfully loaded from messaging/]

## Instructions for Claude

1. Always load the site-content.json first. If running in an environment with file access (Cowork, Claude Desktop), read it from the local repo. Otherwise, fetch from the raw GitHub URL.
2. **Load the brand messaging guidelines** by fetching the router file first, then the files it specifies:
   ```
   https://github.com/cruciate-hub/marketing-team/blob/main/messaging/brain.md
   ```
   At minimum, fetch `terminology.md`, `tone.md`, `positioning.md`, and `boilerplates.md` from the base URL in that router. All suggested copy must follow these guidelines.
3. Read the full product update the user provides.
4. Extract every distinct feature, capability, or improvement mentioned.
5. For each one, scan ALL pages in the JSON — not just the obvious ones. A chat feature might be relevant to a use case page or industry page.
6. Be specific in gap identification. Don't say "this page might need updating" — say exactly what's missing and where it should go.
7. Match the existing copy style. Look at how other features on the same page are described (heading level, sentence length, tone) and mirror that. Apply the brand tone and terminology from the messaging guidelines.
8. If no gaps are found, say so explicitly. Not every update requires website changes.
9. Group gaps by page, not by feature — the person updating the site works page-by-page.
10. Before delivering, run the compliance check from `brain.md` (the main brain). All suggested copy must pass terminology and tone checks.
