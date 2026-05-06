---
name: social-media
description: >
  Create social media posts for social.plus across LinkedIn, Instagram, and X (Twitter).
  Use this skill for: LinkedIn posts, Instagram captions, X/Twitter posts, social media
  campaigns, social content calendars, platform-specific copy, or any content destined
  for social.plus social media accounts. Trigger on phrases like "write a LinkedIn post",
  "social media post", "Instagram caption", "tweet", "X post", "social content",
  "social media calendar", or when the user mentions any social platform by name in
  the context of creating content.
  This skill owns all social media output. Do NOT use brand-messaging for social posts —
  this skill loads the platform-specific guidelines that brand-messaging doesn't.
  Do NOT use for blog content (use blog-seo-content) or email content (use newsletters).
---

# social.plus Social Media Content (BETA/v1, needs optimization)

This skill produces platform-specific social media content for social.plus. Each platform has different format constraints, tone expectations, and content structures — this skill ensures they're all followed.

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

1. Fetch `brain.md` for cross-domain routing, precedence rules, and the compliance check.

2. Fetch `messaging/brain.md` (the messaging router).

3. Follow the messaging router's **"Social media posts"** routing. This loads:
   - `terminology.md` + `tone.md` (always)
   - `boilerplates.md` (short descriptions and elevator pitches as starting points)
   - `positioning.md` (company overview, vision, mission, product pillars)
   - `design-system/social-posts.md` (platform-specific format specs, character limits, copy structure — this file has precedence over tone.md for platform-specific tone and formatting)

4. Social posts are short-form content, so `value-story.md` is also loaded via the **"Short-form content"** routing. Use it when posts make value claims or reference product capabilities.

5. If the post needs visual assets or image specs, also fetch `design-system/brain.md`. Follow its routing for colors, typography, and imagery guidelines.

## Platform-specific rules

Detailed rules are in `social-posts.md`, but the key constraints:

### LinkedIn
- Professional thought leadership voice — but not corporate. Conversational authority.
- No character limit in practice, but keep to 1-3 short paragraphs for engagement.
- Use line breaks for readability. One idea per line.
- Hook in the first 2 lines (before the "see more" fold). This is where the post lives or dies.
- No hashtags in the body. Place 3-5 relevant hashtags at the end, separated by line break.
- Emojis: sparingly acceptable (max 1-2) as visual anchors, never decorative.

### Instagram
- Visual-first — the image carries the message, caption supports it.
- Max 2,200 characters but keep captions concise and scannable.
- Hashtags: 3-5 relevant ones at the end of the caption. No hashtag walls.
- Emojis: more acceptable here than other platforms, but still purposeful, not decorative.
- Always suggest an image concept or visual direction alongside the caption.

### X (Twitter)
- 280 character limit — every word earns its place.
- Punchy, direct, single-idea posts.
- Thread format for multi-point content: number each post (1/5, 2/5…).
- No emojis in most posts. Acceptable only when the platform culture demands it (reactions, polls).
- No hashtags in the body unless the post is joining a specific conversation/trend.

## Output formats

### Single post
When the user asks for a single post or post for a specific platform:

```
## [Platform] Post

**Copy:**
[The post text, exactly as it should appear]

**Hashtags:** [list, or "none"]
**Visual:** [Image concept/direction, or "text only"]
**CTA:** [What action the post drives — link, comment, share, etc.]
**Character count:** [number] / [platform limit]
```

### Multi-platform
When the user wants the same message adapted across platforms:

```
## [Topic] — Social Media Posts

### LinkedIn
**Copy:**
[LinkedIn-optimized version]
**Character count:** [number]

### Instagram
**Copy:**
[Instagram-optimized caption]
**Visual:** [Image concept]
**Character count:** [number]

### X
**Copy:**
[X-optimized version]
**Character count:** [number] / 280
```

### Content calendar
When the user asks for a batch of posts or a calendar:

```
## Social Content Calendar — [Period]

### [Date] | [Platform]
**Topic:** [topic]
**Copy:** [post text]
**Visual:** [concept]
**CTA:** [action]

### [Date] | [Platform]
...
```

## What NOT to do

- Never fabricate statistics, customer names, quotes, or performance claims.
- Never use forbidden terminology (see terminology.md).
- Never write platform-generic copy. Each platform gets its own version, even if the message is the same.
- Never stack hashtags inside the body copy. Keep them at the end.
- Never post competitor names on social unless the user specifically requests a comparison angle.
- Never exceed platform character limits.

## Before delivering

Run the compliance check from `brain.md`. Social posts are public and permanent — a forbidden term in a LinkedIn post is visible to your entire network.

