# Social Media

Claude skill for creating platform-specific social media posts for social.plus across LinkedIn, Instagram, and X (Twitter).

Each platform has different format constraints, tone expectations, and content structures — this skill enforces them all. Owns all social media output end-to-end (copy, character counts, visual direction, CTA).

## What it does

- Fetches short-form messaging (terminology, tone, boilerplates, positioning, value-story) via the brain router.
- Fetches `design-system/social-posts.md` for platform-specific format specs, character limits, and copy structure.
- Produces platform-optimized variants — same message, different execution per platform — with character counts visible on every element.
- Generates single posts, multi-platform adaptations, or full content calendars depending on the request.
- Runs the compliance check before delivering (forbidden terms in a LinkedIn post are visible to the entire network).

## When it triggers

When the user wants content for social.plus social media accounts. Trigger phrases include "write a LinkedIn post", "social media post", "Instagram caption", "tweet", "X post", "social content", "social media calendar", or any mention of a social platform by name in the context of creating content.

This skill owns all social media output. Do NOT use `brand-messaging` for social posts — this skill loads platform-specific guidelines that `brand-messaging` doesn't.

The skill is not for blog content (use `blog-seo-content`) or email content (use `newsletters`).

## Workflow

1. Fetch `brain.md` and `messaging/brain.md`.
2. Follow **"Social media posts"** routing — loads terminology, tone, boilerplates, positioning, and `design-system/social-posts.md` (which has precedence over `tone.md` for platform-specific tone and formatting).
3. Social posts are short-form, so `value-story.md` is also loaded via **"Short-form content"** routing. Use it for value claims or product capability references.
4. If the post needs visual assets or image specs, fetch `design-system/brain.md`.
5. Produce the post with character count visible on every element.
6. Run the compliance check from `brain.md`.

## Platform rules

### LinkedIn
- Professional thought leadership voice — but not corporate. Conversational authority.
- No character limit in practice; keep to 1–3 short paragraphs for engagement.
- Use line breaks for readability. One idea per line.
- **Hook in the first 2 lines** — before the "see more" fold. This is where the post lives or dies.
- No hashtags in the body. Place 3–5 relevant hashtags at the end, separated by a line break.
- Emojis: sparingly acceptable (max 1–2) as visual anchors, never decorative.

### Instagram
- Visual-first — the image carries the message, caption supports it.
- Max 2,200 characters but keep captions concise and scannable.
- Hashtags: 3–5 relevant ones at the end. No hashtag walls.
- Emojis: more acceptable here, but still purposeful.
- Always suggest an image concept or visual direction alongside the caption.

### X (Twitter)
- 280 character limit — every word earns its place.
- Punchy, direct, single-idea posts.
- Thread format for multi-point content: number each post (1/5, 2/5…).
- No emojis in most posts. Acceptable only when platform culture demands it (reactions, polls).
- No hashtags in the body unless joining a specific conversation/trend.

## Output formats

### Single post

```
## [Platform] Post

**Copy:**
[The post text, exactly as it should appear]

**Hashtags:** [list, or "none"]
**Visual:** [image concept/direction, or "text only"]
**CTA:** [what action the post drives — link, comment, share]
**Character count:** [number] / [platform limit]
```

### Multi-platform

Same message adapted across LinkedIn, Instagram, and X, each with its own character count and platform-specific execution.

### Content calendar

```
## Social Content Calendar — [Period]

### [Date] | [Platform]
**Topic:** [topic]
**Copy:** [post text]
**Visual:** [concept]
**CTA:** [action]
```

## What NOT to do

- Never fabricate statistics, customer names, quotes, or performance claims.
- Never use forbidden terminology (see `terminology.md`).
- Never write platform-generic copy. Each platform gets its own version, even when the message is the same.
- Never stack hashtags inside the body copy. Keep them at the end.
- Never post competitor names unless the user specifically requests a comparison angle.
- Never exceed platform character limits.

## Files

```
social-media/
├── SKILL.md                          Skill entry point — platform rules, output formats
└── README.md                         This file
```

## URL format

All reference files are loaded from a shallow clone of this repo (`git clone --depth 1`) into `$MT_REPO`. The canonical fetch block at the top of each SKILL.md handles the clone; skills then read files with `cat "$MT_REPO/<path>"`.
