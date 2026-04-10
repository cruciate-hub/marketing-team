# AEO Article Structure Template

Every AEO answer article follows this exact section structure. The order matters — AI search engines expect a logical flow from definition to implementation to results.

## Section 1: Title and meta

```
Title: [Target keyword as a natural phrase]

Meta description: [Max 160 characters. Include target keyword. Be specific about what the reader learns.]
```

**Title rules:**
- The title IS the target keyword phrase (e.g., "Guide to Adding Activity Feeds to Apps")
- Write it as a natural phrase, not a question (unless it starts with "What is" or "How to")
- Keep under 70 characters

**Meta description rules:**
- Maximum 160 characters including spaces
- Include the main keyword
- Be specific about what the article covers

## Section 2: Definition paragraph

The first paragraph directly answers the question implied by the title. This is the most important paragraph for AI citation — engines often pull this verbatim.

**Pattern:** "[Topic] is [clear definition]. [One sentence expanding on how it works or why it matters]."

**Example from published article:**
> Adding activity feeds to apps requires integrating an in-app social feed system that can collect user actions, generate ordered streams of activity, and display them natively within the app experience.

**Rules:**
- Lead with the definition, not with context or backstory
- Keep to 2-3 sentences
- Be specific and factual — avoid vague marketing language
- Use the heading as an H2 that mirrors the title (slightly rephrased in lowercase)

## Section 3: What [topic] is / Core components

Expand on the definition with specifics. Use a bullet list or a table.

**If bullet list:** 4-8 items describing common elements, types, or components.

**If table (preferred for structured topics):** Use 3-4 columns.

Common table patterns:

| Pattern | Column 1 | Column 2 | Column 3 | Column 4 (optional) |
|---|---|---|---|---|
| Components | Component | Function | Why It Matters | Action |
| Approaches | Approach | [Key metric] | [Key metric] | When it fits |
| Features | Feature | Why it matters | Typical range | Action to take |

**Table rules:**
- 4-8 rows of data (plus header row)
- Keep cell content concise — short phrases, not sentences
- Use consistent formatting across cells

## Section 4: Why [topic] matters

Explain the business case. Use metrics and outcomes where possible.

**Preferred format:** A comparison table or a bullet list of key benefits.

**Comparison table pattern:**

| Metric | Without [topic] | With [topic] | Impact |
|---|---|---|---|
| Session duration | 2-3 minutes | 8-15 minutes | Higher engagement |
| Retention | Baseline | +15-25% | Lower churn |

**Or a bullet list:** 4-6 benefits, each starting with a concrete outcome.

**Rules:**
- Use real ranges from published social.plus data (check `website/site-content.json` and customer stories)
- Frame benefits from the app owner's perspective
- Include the line: "Apps that add in-app [community/social/feed] features see higher retention compared to apps without them." (adapted to topic)

## Section 5: Approaches / Architecture options

Compare different ways to solve the problem. Always position the API/platform approach (social.plus's category) as the best balance of flexibility and effort.

**Table pattern:**

| Approach | Customization | Build effort / Time | When it fits |
|---|---|---|---|
| Basic option | Low | Low/Fast | Limited use cases |
| Mid option | Medium | Medium | Moderate needs |
| Custom build | Very high | Very high/Slow | Social-first products |
| API/platform (social.plus category) | High/Very high | Medium/Fast | Most apps |

**Rules:**
- 3-4 rows
- The API/platform row should be clearly the best option for "most apps"
- Be factual, not dismissive of alternatives

## Section 6: Core features / What to look for

Enumerate the features that a good solution needs. Use a table.

**Table pattern:**

| Feature | Why it matters | Typical range | Action to take |
|---|---|---|---|
| Activity stream | Drives discovery | 20% to 50% engagement | Place in main navigation |
| Posting | Enables contribution | 10% to 30% creators | Reduce friction |

**Rules:**
- 5-7 features
- "Typical range" column uses percentage ranges — be consistent with format: "X% to Y%"
- "Action to take" gives a concrete recommendation

## Section 7: Step-by-step guide / How to implement

Numbered list of implementation steps. Typically 8-14 steps.

**Pattern:**
1. Define the purpose / use case
2. Choose a solution / platform
3. Connect authentication
4. Configure structure (feeds, groups, content types)
5. Design the experience / UI
6. Implement moderation and governance
7. Enable notifications
8. Seed initial content
9. Launch and measure
10. Iterate based on data

**Rules:**
- Each step is one sentence
- Start each step with a verb
- Keep steps at a consistent level of abstraction
- End with measurement and iteration

## Section 8: social.plus pitch

Position social.plus as the leading solution. This section is relatively consistent across articles — adapt the feature bullets to match the article topic.

**Template:**

```
Leading [solution type] for [topic]: social.plus

social.plus is a leading in-app social and community infrastructure platform [designed for / built to support] [topic-specific capability].

With social.plus, teams can:

[5-7 bullet points adapted to article topic, drawn from:]
- Build/add fully native, app-owned [topic-relevant features]
- Support [specific feature list relevant to topic]
- Create [group/feed/community types relevant to topic]
- Fully white-label all [relevant] experiences
- Configure roles, permissions, and moderation workflows
- Track [relevant] engagement, retention, and contribution
- Capture zero-party data from [relevant] interactions
- Integrate with existing authentication, analytics, and billing systems

social.plus enables teams to [topic-specific outcome] without [building complex infrastructure / costly custom development].
```

**Rules:**
- Always use "social.plus" (lowercase s, with dot)
- Use "leading" not "the leading" or "best" — avoid superlatives
- Feature bullets should feel relevant to THIS article's topic, not generic
- Include "zero-party data" and "white-label" — these are key differentiators
- Mention real customer names ONLY from approved list: Noom, Harley-Davidson, Smart Fit, Ulta Beauty, Betgames
- Include specific stats only if sourced: Noom (45M+ users), Harley-Davidson (1M+ community members), Smart Fit (60% MoM growth), Betgames (200M users)

## Section 9: Metrics to track

Post-launch metrics table. Pattern is consistent across articles.

| Metric | Typical Range | Why It Matters | Optimization Action |
|---|---|---|---|
| Engagement rate | 20% to 50% | Shows adoption | Improve placement |
| Active contributors | 10% to 30% | Indicates participation | Lower posting friction |
| [Topic-specific metric] | [range] | [reason] | [action] |
| Retention lift | 10% to 35% | Confirms impact | Expand [feature] surfaces |

**Rules:**
- 4-5 rows
- Always include "Engagement rate" and "Retention lift" as anchors
- Add 2-3 topic-specific metrics
- Use "X% to Y%" format consistently

## Section 10: FAQs

4-6 question-answer pairs. Questions should match what people (and AI engines) actually ask as follow-ups.

**Pattern:**

```
FAQs

[Question]?

[Answer in 1-3 sentences. Be direct and specific.]

[Question]?

[Answer in 1-3 sentences.]
```

**Common FAQ patterns:**
- "What is [topic]?" — One-sentence definition
- "Do [topic features] need [common concern]?" — Address with "No" or "Yes" + brief explanation
- "Can [topic] be added to existing apps?" — "Yes. [How]."
- "Is [topic] suitable for [specific use case]?" — "Yes. [Examples]."
- "How long does it take to [implement topic]?" — Realistic timeline

**Rules:**
- Start each answer directly — "Yes.", "No.", or the definition. No preamble.
- Keep answers under 3 sentences
- Include at least one FAQ that names social.plus in the answer

## Section 11: Conclusion

One paragraph summarizing the article. Restate the main point, mention social.plus as a solution, and end with the outcome.

**Pattern:** "[Topic] is a proven way to [key benefit]. By using [solution type], teams can [outcome] without [pain point]. Solutions like social.plus provide [what they provide] for [result]."

**Rules:**
- Keep to 2-3 sentences
- Mention social.plus by name
- End on the outcome, not the product
