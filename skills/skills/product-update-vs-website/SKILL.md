---
name: product-update-vs-website
description: Compare new product releases or monthly updates against the current social.plus website content to identify gaps — pages that should mention a new feature but don't yet. Use this skill when someone pastes a release note, monthly product update, or changelog entry and wants to know which website pages need updating. Also trigger when someone asks "what's missing from the site", "does the website reflect this update", "which pages need to change", or references the pages-marketing.json file. Always use this skill for any product-update-to-website comparison task, even if the user doesn't explicitly name the skill.
---

# Product Update vs Website

Compares social.plus product updates (release notes, monthly updates) against the current website content to identify which marketing pages are missing new features and need updating.

## How to fetch reference files

<!-- FETCH-BLOCK:START v2 -->
Reference files live in the public `cruciate-hub/marketing-team` GitHub repo. Fetch them by shallow-cloning the repo once per session, then loading individual files with `cat`. Use this exact pattern at the start of every skill that needs reference files:

    REPO="${MT_REPO:-/tmp/cruciate-hub-marketing-team}"
    if [ ! -d "$REPO/.git" ]; then
      git clone --depth 1 --quiet https://github.com/cruciate-hub/marketing-team.git "$REPO"
    else
      git -C "$REPO" pull --ff-only --quiet
    fi

After the clone exists, read files with `cat "$REPO/<path>"`. Examples: `cat "$REPO/brain.md"`, `cat "$REPO/messaging/terminology.md"`.

The Bash tool truncates large stdout to a small preview when the output exceeds the harness's display cap (the exact size varies by environment — observed in the 20–50 KB range). When that happens you'll see a marker like `Output too large (NkB). Full output saved to: …` followed by a short preview, and the rest is invisible to you in-call. Most files in this repo are small enough that `cat` returns them in full and you never see the marker. **If you do see the marker, never proceed using the preview as if it were the whole file** — switch to one of the patterns below.

- **Truncated markdown** — read in line-range chunks instead. First check the total line count: `wc -l "$REPO/<path>"`. Then read each chunk:

      sed -n '1,250p'     "$REPO/<path>"
      sed -n '251,500p'   "$REPO/<path>"
      sed -n '501,$p'     "$REPO/<path>"

  Each ~250-line chunk fits under the preview cap. Concatenate the chunks mentally. For files much larger than 750 lines, add more chunks at 250-line intervals until you reach the total.

  **If a chunk itself comes back as a truncated preview** (output above the harness's display cap — visible as an "Output too large" or similar marker, with the rest spilled to a file you can't see in-call), halve the chunk size and retry. For example, swap `sed -n '1,250p'` for `sed -n '1,125p'` then `sed -n '126,250p'`. Repeat until each chunk lands in full. Never proceed using a truncated chunk as if it were complete.

- **Large JSON inventories** (`website/pages-*.json`, up to 228 KB) — never `cat` raw. Process with `python3` or `jq` and emit only the fields you need:

      python3 -c "import json; d=json.load(open('$REPO/website/pages-blog.json')); print(len(d['pages']))"
      jq '.pages[].url' "$REPO/website/pages-blog.json"

  Skill helper scripts (e.g. `scripts/duplicate_check.py`) already follow this pattern.

Note: Claude Code's `Read` tool can't reach files in `$REPO` — Cowork sandboxes Read to connected directories and `/tmp` is not connected by default. Use the `cat` / `sed` / `python` patterns above.

Validate every file before using it:
- Markdown: content must start with `#`
- JSON: content must start with `{` or `[`
- HTML: content must start with `<`
- Content must be non-empty

If anything fails — clone error, missing file, empty content, or wrong format:
- Do NOT reconstruct from memory or training data.
- Do NOT fall back to WebFetch or any other tool.
- Stop immediately and respond with exactly this line:

  `Fetch failed: <path>. Please check your network connection and rerun.`
<!-- FETCH-BLOCK:END v2 -->

## What to do

1. **Read `brain.md`** for cross-domain routing, precedence rules, and the compliance check.
2. **Load current site content** from THREE JSON files in this repo (read all three — they cover different page types):
   - `website/pages-marketing.json` — static marketing pages (homepage, pricing, product, feature/SDK/UIKit pages, white-label, vs-stream)
   - `website/pages-industry.json` — all `/industry/*` pages (retail, fitness, travel, sports, health-and-wellness, fintech, media-and-news, edtech, gaming, betting)
   - `website/pages-use-cases.json` — all `/use-case/*` pages (activity feed, group chat, livestream, polls, etc.)
   Combine the `pages` arrays from all three files before running gap detection — they are one logical dataset split into three files for maintenance reasons.
3. **Take the product update** — a release note, monthly product update, or changelog entry provided by the user
4. **Cross-reference** every new feature/capability mentioned in the update against every page in the JSON
5. **Output a gap report** showing which pages should mention this feature but currently don't
6. **Draft copy suggestions** for each gap, matching the existing page's tone and structure

## Site content reference

The site content JSONs are maintained automatically by a Cloudflare Worker. Marketing and industry are regenerated on every Webflow site publish (both are static-page inventories); use cases are regenerated on every Use Cases CMS publish.

All three files share the same JSON structure:
```json
{
  "_meta": { "generatedAt": "...", "itemCount": 22 },
  "pages": [
    {
      "url": "https://www.social.plus/social/features",
      "metaTitle": "...",
      "metaDescription": "...",
      "content": "# heading\n## section\n### feature name\nFeature description..."
    }
  ]
}
```

URLs are fully qualified (`https://www.social.plus/...`) — use them as-is in report output. Each page's `content` field preserves heading hierarchy using markdown-style markers (`#`, `##`, `###`).

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

### Use case pages (loaded from `pages-use-cases.json`)
- `/use-case/1-1-chat`, `/use-case/activity-feed`, `/use-case/custom-posts`, `/use-case/group-chat`, `/use-case/groups`, `/use-case/live-chat`, `/use-case/livestream`, `/use-case/polls`, `/use-case/stories-and-clips`, `/use-case/user-profiles`
- New use cases are auto-included when published — the JSON reflects whatever currently exists in the Webflow Use Cases CMS collection.

### Industry pages (loaded from `pages-industry.json`)
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

Always start with a brief summary, then list each gap grouped by page. Every entry must follow the **exact same structure** — no formatting variations between entries. This is critical because the output is emailed and inconsistent formatting looks unprofessional.

### Summary (always first)

Start every report with a link to the release note or product update, followed by a short paragraph summarizing what was found. Use the slug from the CMS item to construct the URL. Example:

Release note: https://www.social.plus/release-note/event-creation-and-management-on-console

Found 6 gaps across 6 pages — 1 high priority, 3 medium, 2 low. The primary gap is on /social/features where events are not listed as a feature at all.

### Gap entries (grouped by page)

Each page gets its own section. The format must be **exactly** as shown below — no variations between entries. This is critical for consistent email rendering.

**Format rules:**
- Page URL as a markdown heading with 🔍 prefix: `🔍 [URL](URL)`
- Blank line after the URL heading
- All field labels in **bold** with colon (e.g., `**Feature:**`)
- **Suggested copy** must be wrapped in a blockquote (`>`) so it renders with a highlight background
- No horizontal rules (`---`) between entries — the heading + blank line provides enough visual separation
- Priority uses the colored circle emoji (🔴 🟡 🟢) inline

**Example entries:**

🔍 [https://www.social.plus/social/features](https://www.social.plus/social/features)

**Feature:** Event creation and management
**Section:** Communities
**Status:** Missing — no mention of events anywhere on this page
**Suggested heading:** Event Creation and Management
> **Suggested copy:** Enable admins and moderators to create and manage digital live streams, virtual events, and in-person gatherings. Events surface automatically across group tabs, the Event Hub, and community feeds.

**Priority:** 🔴 High — primary features page missing this entirely

🔍 [https://www.social.plus/use-case/livestream](https://www.social.plus/use-case/livestream)

**Feature:** Event scheduling and RSVPs
**Section:** What you get with social.plus
**Status:** Could be enhanced — lists live video but no scheduling or RSVPs
**Suggested heading:** Event Scheduling & RSVPs
> **Suggested copy:** Create events in advance, collect RSVPs, and send reminders so your audience is ready when you go live.

**Priority:** 🟡 Medium — livestream use case page omits pre-stream planning

🔍 [https://www.social.plus/pricing](https://www.social.plus/pricing)

**Feature:** Event Creation and Management
**Section:** Communities (comparison table)
**Status:** Missing — no line item for events in the Communities group
**Suggested line item:** Event Creation and Management: Core=✓, Max=✓
**Priority:** 🟡 Medium — pricing comparison table should list this alongside other community features

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

1. Always load `pages-marketing.json`, `pages-industry.json`, AND `pages-use-cases.json` first (via the fetch block at the top of this file). Merge their `pages` arrays into one combined dataset before gap detection.
2. **Load the brand messaging guidelines** by reading `messaging/brain.md` first, then the files it routes to. At minimum, read `messaging/terminology.md`, `messaging/tone.md`, `messaging/positioning.md`, and `messaging/boilerplates.md`. All suggested copy must follow these guidelines.
3. Read the full product update the user provides.
4. Extract every distinct feature, capability, or improvement mentioned.
5. For each one, scan ALL pages in the JSON — not just the obvious ones. A chat feature might be relevant to a use case page or industry page.
6. Be specific in gap identification. Don't say "this page might need updating" — say exactly what's missing and where it should go.
7. Match the existing copy style. Look at how other features on the same page are described (heading level, sentence length, tone) and mirror that. Apply the brand tone and terminology from the messaging guidelines.
8. If no gaps are found, say so explicitly. Not every update requires website changes.
9. Group gaps by page, not by feature — the person updating the site works page-by-page.
10. Before delivering, run the compliance check from `brain.md` (the main brain). All suggested copy must pass terminology and tone checks.
