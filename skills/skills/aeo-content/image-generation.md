# AEO Hero Image Generation

This file explains how to generate a Google Gemini image prompt for an AEO answer article's hero image. The full visual style guide, icon reference table, and example prompts are in a separate file.

## Full style guide

Fetch the complete prompt template, icon table, and worked examples:
```
https://github.com/cruciate-hub/marketing-team/blob/main/docs/aeo-image-prompt-template.md
```

That file contains everything needed to assemble a prompt. This file explains the decision logic.

## How to generate a prompt

### Step 1: Pick the composition mode

**Mode B (floating exploded view)** if the article title:
- Starts with "What is" or "What are"
- Is a broad definition or concept overview

**Mode A (diorama on platform)** for everything else. This is the default — it covers how-to guides, API articles, tool/platform/solution articles, retention, monetization, engagement, feeds, private networks, SDK, white-label.

### Step 2: Classify the topic cluster

Match the article title to one of these clusters based on the primary noun or concept:

| Cluster | Title signals |
|---|---|
| Activity feeds / social feeds | "activity feed", "social feed", "feed" as main subject |
| Community features (general) | "community features", "community capabilities" |
| White-label / SDK / embedding | "white-label", "SDK", "embed" |
| Social networks / full social | "social network", "social features", "social functionality" |
| Retention | "retention", "keep users", "stickiness" |
| Monetization | "monetization", "monetize" |
| Revenue | "revenue", "income" |
| Engagement | "engagement", "engage", "interaction strategies" |
| Private social networks | "private social network", "private community" |
| Decentralized social | "decentralized", "distributed" |
| API / integration | "API", "integrate" (without SDK or white-label) |
| Platform / tool / solution | "platform for", "tool for", "solution for" (catch-all) |
| Planning community features | "plan", "planning", "roadmap" |
| Examples / case studies | "examples of", "case study" |

### Step 3: Select 5-6 objects

Use the Topic-to-Objects Mapping table in `docs/aeo-image-prompt-template.md`. Follow these rules:
- Always include at least one people element (user group, profile card, avatars)
- Always include at least one interaction element (heart, chat bubble, thumbs up)
- Pick 3-4 topic-specific objects from the recommended list
- If generating multiple prompts in one session, vary the objects for similar topics
- Use the exact "Prompt description" phrasing from the Icon Reference Table

### Step 4: Assemble the prompt

Combine into one continuous block of text (no markdown headers or formatting):
1. **Style Prefix** — copy verbatim from the template file
2. **Composition Mode** paragraph — Mode A or B, copy verbatim
3. **Topic line**: `Topic: [Article Title]`
4. **Objects line**: `Feature these 3D objects in the scene:` followed by a comma-separated list of the selected objects

Present the assembled prompt in a single code block, ready to copy-paste.

## Aspect ratio note

The Gemini API supports: 1:1, 9:16, 16:9, 4:3, 3:4. The hero images are approximately 3:2, so use **16:9** as the closest option when calling the API.

## Output

After the code block, add a brief summary:
- **Mode**: A (diorama) or B (floating)
- **Cluster**: which topic cluster was matched
- **Objects**: short list of what was included
