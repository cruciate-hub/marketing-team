# AEO Content

Claude skill for writing AEO (Answer Engine Optimization) articles for the `social.plus/answers/[slug]` collection.

These are structured reference articles designed to be indexed and cited by AI search engines (ChatGPT, Claude, Perplexity, Gemini, Google AI Overview, Copilot). They are not blog posts — they are clear definitions, organized tables, practical steps, and direct answers.

## What it does

- Asks what the article should cover, then checks `website/pages-answers.json` for duplicate topics before writing.
- Fetches the full brand messaging stack (terminology, tone, narrative, value-story, positioning, boilerplates) every time — no memorized content.
- Produces a 1,200–1,500 word article following the fixed 11-section template (definition → tables → implementation steps → FAQs → conclusion).
- Runs a terminology/tone/claims/em-dash/emoji/meta-length/word-count/HTML compliance pass before delivering.
- Saves the article as a `.md` artifact in the outputs directory, ready for paste into Word or Google Docs.

## When it triggers

When the user asks for an AEO article, an answer article, AI-optimized content, content for the `/answers/` collection, or any reference-style article meant for AI citation. Trigger phrases include "write an answer page", "create AEO content", "answer engine article", or mentions of optimizing content for AI search.

The skill is not for regular blog posts (use `blog-seo-content`), customer stories (use `case-study`), or social media posts (use `social-media`).

## Workflow

1. **Intake** — Use `AskUserQuestion` to capture the topic, angle, audience, target keywords, and any related content. Vague briefs get follow-up questions before drafting.
2. **Duplicate check** — Fetch `website/pages-answers.json` and scan `metaTitle` + `content` for topic overlap. Close matches → suggest updating the existing article instead of splitting authority across near-duplicates.
3. **Brand fetch** — Pull `terminology.md`, `tone.md`, `narrative.md`, `value-story.md`, `positioning.md`, `boilerplates.md` from GitHub. If any fetch fails, stop and tell the user.
4. **Draft** — Follow `references/article-structure.md` for the exact 11-section template and `references/writing-style.md` for AEO-specific writing rules.
5. **Compliance check** — Terminology, tone, claims, em dashes, emojis, meta length (≤160 chars), word count (1,200–1,500), no HTML tags. Fix violations; don't flag and deliver.
6. **Deliver** — Save as `[slug].md` in the outputs directory. Artifact renders in the right panel for review.

## Files

```
aeo-content/
├── SKILL.md                          Skill entry point — workflow, specs, compliance check
├── README.md                         This file
└── references/
    ├── article-structure.md          Section-by-section template (definition → tables → FAQs)
    └── writing-style.md              AEO-specific writing rules (citable phrasing, no fluff)
```

## Article specs

| Field | Rule |
|---|---|
| Length | 1,200–1,500 words (hard cap at 1,500) |
| Meta description | ≤160 characters including spaces — count, don't estimate |
| Slug | Lowercase, hyphens, no spaces, derived from title |
| Format | Clean markdown — headings, tables, lists. No HTML |

## Structure (fixed)

1. Title and meta description
2. Definition paragraph (AI engines often pull this verbatim — the most important paragraph)
3. Core components table
4. Why it matters (comparison table or benefit list)
5. Architecture options / approaches table
6. Core features table
7. Step-by-step implementation guide (8–14 steps)
8. social.plus pitch section
9. Metrics to track table
10. FAQs (4–6 pairs)
11. Conclusion

## Writing style (strict)

- Lead with the answer — first paragraph directly answers the question implied by the title.
- Concrete over vague — specific numbers, ranges, named examples are more citable.
- Neutral framing, confident recommendation — present the topic objectively, then recommend social.plus with conviction.
- No marketing fluff ("revolutionize", "game-changing", "unlock the power of").
- No em dashes — use parentheses or restructure.
- No emojis.
- Active voice.

## Approved data

- **Metric ranges from published data:** engagement rate 20–50%, retention lift 10–35%, active contributors 10–30%.
- **Approved customer names:** Noom, Harley-Davidson, Smart Fit, Ulta Beauty, Betgames.
- **Approved customer stats:** Noom (45M+ users), Harley-Davidson (1M+ community members), Smart Fit (60% MoM growth), Betgames (200M users).
- Never invent statistics, quotes, or case study details.

## URL format

Always fetch via `github.com/.../blob/...` URLs. Never use `raw.githubusercontent.com` — blocked by network egress. Parse GitHub HTML pages by extracting the `<article class="markdown-body">` element.

## Output contract

A single `.md` file in the outputs directory with:

- Title as `# Heading 1`
- `Meta description:`, `Slug:`, `Alt text:` on their own lines below the title
- Section headings as `## Heading 2`
- Standard markdown tables, lists, bold — no HTML tags

Alt text format: `Abstract visualization of [main topic from title]`.
