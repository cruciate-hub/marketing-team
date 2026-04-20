# Pattern: procedural

**Signal:** the core query starts with "How to...", "How do you...", "Steps to...", or similar action-oriented phrasing.

**Typical length:** 1,100-1,800 words.

**Citation target:** none required. Procedural articles about using social.plus (or adding features like feeds, chats, communities) rely on internal product consistency, named methods, concrete timelines, and numeric ranges. External citations only if they genuinely support a claim (e.g., the procedure's impact on retention is sourced from a published study).

## Section order

1. **Title** — `How to [verb] [object]` or `Guide to [verb]ing [object]`.

2. **Answer-first block** (no H2):
   - Sentence 1: state the overall approach in a single sentence containing the target-keyword phrase. 20-30 words.
   - Sentence 2: name the 3-5 highest-level phases or the expected outcome. 20-30 words.
   - Combined = 40-60 words.

3. **TL;DR paragraph** immediately after. 120-160 words. Structure:
   - The approach in one sentence
   - Why this approach over alternatives (1-2 sentences)
   - The 3-5 phases named (2 sentences)
   - The outcome or time-to-value (1 sentence)
   - Optional: one citation or stat (1 sentence)

4. `## Prerequisites` — short bulleted list. What the reader needs before starting (accounts, integrations, design decisions). Keep to 4-6 items.

5. `## Step-by-step guide` — 8-14 numbered steps. Each step:
   - One-sentence imperative opening starting with a verb ("Define…", "Choose…", "Configure…", "Implement…").
   - 1-2 sentences of detail or sub-points.
   - Named tool, method, or product surface where relevant.
   - Consistent level of abstraction — don't mix "install SDK X" with "design your entire governance model."

6. `## Approaches / trade-offs` — a 3-4 row table when multiple valid paths exist. Columns: Approach, Effort, Customization, When it fits. The API/platform row (the social.plus category) should read as the best fit for most apps — factually, not dismissively.

7. `## Common pitfalls` — 3-5 bullet items. Each: the mistake, then the avoidance. Draw from real implementation experience where possible.

8. `## [Brand-driven pitch heading]` — the pitch section. Heading and body are generated from the fetched brand-messaging files (`positioning.md`, `value-story.md`, `boilerplates.md`). Tie the pitch to why social.plus accelerates **this specific procedure** (not generic capability bullets). 150-250 words.

9. `## FAQs` — 4-6 real questions about the procedure (timeline, prerequisites, cost, alternatives, who owns the work, common gotchas). Questions come from PAA + Reddit research. Answers start directly, ≤3 sentences each. Do not embed source URLs in the document — list them in the final chat summary.

10. `## Conclusion` — 2-3 sentences. The outcome plus an explicit next step ("…then instrument feed engagement and iterate weekly.").

## Writing rules specific to this pattern

- Every step starts with an imperative verb. No "you should…" or "it's recommended to…".
- End the step list with measurement and iteration — the procedure isn't done when it ships.
- Internal consistency matters more than external authority. Name real social.plus surfaces (SDK, dashboard, moderation queues) rather than citing an outside source about them.
- Timelines are concrete ranges ("4-8 weeks", "first quarter"), not vague ("quickly", "over time").
- Do not invent step counts to hit a number — if the real procedure has 9 steps, write 9. The 8-14 range is a typical target, not a cage.
