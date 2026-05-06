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

<!-- FETCH-BLOCK:START v1 -->
Fetch reference files ONLY with `curl` from `raw.githubusercontent.com`, using these exact flags:

    curl -fsSL --max-time 30 --connect-timeout 10 --retry 2 --retry-delay 1 \
      https://raw.githubusercontent.com/cruciate-hub/marketing-team/main/<path>

The repo is public — no authentication required. When fetching multiple files in one step, run the curl commands in parallel (single Bash message, multiple commands) — do not serialise.

Validate every response before using it:
- Markdown files must start with `#` (a leading heading line)
- JSON files must start with `{` or `[`
- HTML files must start with `<`
- Content must be non-empty

If any fetch fails (non-zero exit, empty output, or content that fails the above check):
- Do NOT reconstruct the file from memory or training data.
- Do NOT fall back to WebFetch or any other tool.
- Stop immediately and respond with exactly this line:

  `Fetch failed: <path>. Please check your network connection and rerun.`
<!-- FETCH-BLOCK:END v1 -->

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

