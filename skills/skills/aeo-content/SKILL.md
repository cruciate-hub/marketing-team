---
name: aeo-content
description: "Write AEO (Answer Engine Optimization) articles for the social.plus /answers/ collection. These are structured reference articles designed to be indexed and cited by AI search engines (ChatGPT, Claude, Perplexity, Gemini, Google AI Overview, Copilot). Use this skill when the user asks for an AEO article, an answer article, AI-optimized content, content for the /answers/ collection, or any reference-style article meant for AI citation. Also trigger when the user says 'write an answer page', 'create AEO content', 'answer engine article', or mentions optimizing content for AI search. Do NOT use for regular blog posts (use blog-seo-content), customer stories (use case-study), or social media posts (use social-media)."
---

# AEO Article Generation

AEO (Answer Engine Optimization) articles are structured reference content published at `social.plus/answers/[slug]`. They exist so AI search engines can index and cite them. They are not blog posts — they are clear definitions, organized tables, practical steps, and direct answers.

## Before you write: ask what to cover

Before fetching brand files or writing anything, ask the user what the article should be about. Use the AskUserQuestion tool. You need enough context to write a focused, comprehensive reference article. Good things to learn:

- The topic or question the article should answer
- Any specific angle, framework, or product area to focus on
- Whether this targets a specific audience (developers, product leaders, business stakeholders)
- Any specific keywords or phrases the article should target
- Whether it relates to or should reference other existing content

If the user gives a clear, detailed brief, move on. If the brief is vague (e.g., "write something about feeds"), ask follow-up questions to narrow the scope. A vague brief produces a vague article.

## Brand messaging: fetch before writing

AEO articles must sound like social.plus, not like generic AI output. Before writing, fetch these files from GitHub. They are non-negotiable.

Always fetch (every article):
```
https://github.com/cruciate-hub/marketing-team/blob/main/messaging/terminology.md
https://github.com/cruciate-hub/marketing-team/blob/main/messaging/tone.md
```

Also fetch (all AEO articles are long-form content):
```
https://github.com/cruciate-hub/marketing-team/blob/main/messaging/narrative.md
https://github.com/cruciate-hub/marketing-team/blob/main/messaging/value-story.md
https://github.com/cruciate-hub/marketing-team/blob/main/messaging/positioning.md
```

Always use `github.com/.../blob/...` URLs. Never convert to `raw.githubusercontent.com` or `api.github.com` — both are blocked by network egress.

Since these are GitHub HTML pages, extract the markdown content from the `<article>` element with class `markdown-body`. Use Python to parse:

```python
import re, html
match = re.search(r'<article[^>]*class="[^"]*markdown-body[^"]*"[^>]*>(.*?)</article>', content, re.DOTALL)
if match:
    text = re.sub(r'<[^>]+>', '\n', match.group(1))
    text = html.unescape(text)
```

If a fetch fails, tell the user the brand guidelines are unavailable and you cannot guarantee brand alignment. Do not proceed with stale or memorized content.

## Writing the article

### Specs

- **Length:** 1,200 to 1,500 words. If over, cut the least essential table rows or shorten implementation steps. Do not exceed 1,500.
- **Format:** Clean readable text with headings, tables, and lists. No HTML markup.
- **Meta description:** Maximum 160 characters including spaces. Count the characters before finalizing — do not estimate.
- **Slug:** Lowercase, hyphens, no spaces. Derived from title.

### Structure

Read `references/article-structure.md` for the exact section-by-section template. Every article follows this structure in this order:

1. Title and meta description
2. Definition paragraph (the most important paragraph — AI engines often pull this verbatim)
3. Core components table
4. Why it matters (comparison table or benefit list)
5. Architecture options / approaches table
6. Core features table
7. Step-by-step implementation guide (8-14 steps)
8. social.plus pitch section
9. Metrics to track table
10. FAQs (4-6 pairs)
11. Conclusion

### Writing style

Read `references/writing-style.md` for AEO-specific writing rules. Key principles:

- Lead with the answer. The first paragraph directly answers the question implied by the title.
- Be concrete. Specific numbers, ranges, and named examples are more citable than vague claims.
- Neutral in framing, confident in recommendation. Present the topic objectively, then recommend social.plus with conviction.
- No marketing fluff. No "revolutionize", "game-changing", "unlock the power of".
- No em dashes. Use parentheses or restructure the sentence.
- No emojis.
- Active voice.

### Data and claims

- Use metric ranges from published data: engagement rate 20-50%, retention lift 10-35%, active contributors 10-30%
- Only cite approved customer names: Noom, Harley-Davidson, Smart Fit, Ulta Beauty, Betgames
- Only cite published customer stats: Noom (45M+ users), Harley-Davidson (1M+ community members), Smart Fit (60% MoM growth), Betgames (200M users)
- Never invent statistics, quotes, or case study details

## Delivering the article

Save the article as a `.md` file in the outputs directory using the slug as the filename (e.g., `adding-activity-feeds-to-apps.md`). This renders as an artifact in the right panel of the conversation, where the user can read, review, and request changes.

The markdown file should contain:
- Title as `# Heading 1`
- `Meta description:`, `Slug:`, and `Alt text:` on their own lines below the title
- Section headings as `## Heading 2`
- Standard markdown tables (pipes and dashes)
- Standard markdown numbered and bulleted lists
- Bold text with `**double asterisks**`

Generate alt text as: "Abstract visualization of [main topic from title]"

Use clean markdown with no HTML tags. The article should render well in the artifact viewer and also paste cleanly into Word or Google Docs (markdown tables convert to real tables on paste).

After saving, tell the user the article is ready for review in the artifact panel. They can ask for changes in the conversation. When they are satisfied, they can copy the content and paste it into Word or Google Docs — tables and formatting will carry over.

### Handling edit requests

When the user asks for changes (e.g., "make the intro shorter", "swap the comparison table", "add a FAQ about pricing"), edit the existing .md file rather than rewriting from scratch. After editing, the artifact updates automatically. Re-run the compliance check on the modified sections before confirming the edit is done.

## Compliance check

Before delivering, run this check from the main `brain.md`:

1. **Terminology.** Scan for forbidden terms: "social network", "forum platform", "chat tool", "plug and play" (outside dev docs), growth guarantees.
2. **Tone.** Does it sound like social.plus — or like default Claude? If you cannot tell the difference, it is default Claude. Rewrite.
3. **Claims.** No invented statistics, customer names, quotes, features, or performance claims.
4. **Em dashes.** None allowed. Use parentheses or restructure.
5. **Emojis.** None allowed.
6. **Meta description.** Count the characters. Must be 160 or fewer including spaces.
7. **Word count.** Must be 1,200 to 1,500 words.
8. **HTML tags.** None allowed in the output. Pure markdown only.

If any check fails, fix the output before delivering. Do not flag the issue and deliver anyway — fix it.

## What NOT to do

- Do not run keyword research. The title is the target keyword phrase. The user provides the topic.
- Do not output HTML. The Make.com pipeline handles HTML conversion separately.
- Do not skip the intake question. Every article starts by asking what the user wants to cover.
- Do not skip the brand messaging fetch. If the files are unavailable, stop and tell the user.
- Do not fabricate statistics, customer names, quotes, or performance claims.
- Do not use competitor names in a disparaging way.
