---
name: aeo-content
description: >
  Generate AEO (Answer Engine Optimization) answer articles and hero image
  prompts for the social.plus /answers/ CMS collection. Use this skill for:
  AEO articles, answer page content, AI-optimized reference content, hero
  image prompts for answer articles, or any content destined for the /answers/
  collection on social.plus.
  Trigger on phrases like "AEO article", "answer article", "write an answer
  for", "generate an AEO", "answers page", "AI-optimized article", or when
  someone provides an article title and wants content for the /answers/
  collection. Also trigger when the user mentions Joy's AEO workflow, the
  AEO pipeline, or asks for a hero image prompt for an answer article.
  Do NOT trigger for regular blog posts (use blog-seo-content skill), general
  website copy (use brand-messaging skill), or customer stories (use case-study
  skill).
---

# social.plus AEO Content

This skill generates AEO answer articles and hero image prompts for the social.plus `/answers/` CMS collection. AEO articles are structured reference content optimized so AI search engines (ChatGPT, Claude, Perplexity, Gemini, Google AI Overview, Copilot) can index and cite them.

## What to do

1. Fetch the main brain for cross-domain routing, precedence rules, and the compliance check:
```
https://github.com/cruciate-hub/marketing-team/blob/main/brain.md
```

2. Fetch the AEO domain router:
```
https://github.com/cruciate-hub/marketing-team/blob/main/skills/skills/aeo-content/brain.md
```

3. Follow the AEO router's instructions for the user's task:
   - **Writing an article** → router loads `article-generation.md`, `article-structure.md`, and `writing-style.md`
   - **Generating a hero image prompt** → router loads `image-generation.md` and `docs/aeo-image-prompt-template.md`
   - **Both** → router loads all of the above

4. `writing-style.md` will direct you to fetch the brand messaging files:
   - `messaging/terminology.md` + `messaging/tone.md` (always)
   - `messaging/narrative.md` + `messaging/value-story.md` + `messaging/positioning.md` (for long-form content)

5. If writing an article and you need real customer stats or product details, also fetch:
```
https://github.com/cruciate-hub/marketing-team/blob/main/website/site-content.json
```

6. Generate the output following the instructions in the loaded files.

7. Run the compliance check from `brain.md` before delivering.

## Output

**For articles:** A clean, readable document with title, meta description, and article body. No HTML markup — the writer pastes this into a Google Doc, and the Make.com pipeline handles conversion.

**For image prompts:** A complete Gemini prompt in a code block, ready to paste into Google AI Studio or use via the Gemini API.

## What NOT to do

- Never fabricate statistics, customer names, quotes, or performance claims.
- Never produce HTML output — the article should read like a Google Doc.
- Never skip the brand messaging files. AEO articles must follow social.plus terminology and tone.
- Never call social.plus a "social network", "forum", or "chat tool" (see terminology.md).

## Before delivering

Run the compliance check from `brain.md`:
1. Terminology — scan for forbidden terms
2. Tone — does it sound like social.plus?
3. Claims — nothing invented
4. Precedence — terminology.md overrides everything

## Important: URL format

**Always use `github.com/.../blob/...` URLs when fetching files.** Never attempt `raw.githubusercontent.com` — it is blocked by network egress settings.
