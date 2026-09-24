# Ideation lenses

How to turn one seed into candidate articles across Glossary, Answer and Blog. The lenses make sure the planner looks at a seed from every angle a buyer, a developer or an AI engine would; the rules at the end keep that from turning into permutations.

## Start by splitting the seed the way an AI engine would

AI engines break a prompt into several narrower searches (Google AI Mode runs roughly 5 to 16 per prompt) and pick one passage per search. For a seed, write down the sub-questions an engine would plausibly run if a product manager or developer asked about it. Those sub-questions are the raw material; each surviving one becomes either a candidate page or a heading inside one.

Example, seed "app retention": what is it, how is it measured, what is good, why does it drop, how to increase it, does community help, which categories retain best, how do fitness apps handle it, push vs community, how to prove impact.

## Glossary lenses (0-10 per seed)

Glossary owns "What is [term]?". Propose a term only if people would plausibly search the definition on its own and the Queue has no row for it.

- **The seed itself**, if it is a term (usually already in the Queue: then it's an Update existing or Merge, not a new row).
- **Metric variants and formulas** the seed depends on (Day 7 retention, cohort analysis, stickiness).
- **Adjacent terms** a reader of the seed's pages would need defined (churn, DAU, UGC).

Skip: terms that are only meaningful inside a longer explanation, and synonyms of existing terms.

## Answer lenses (0-10 per seed)

Answer owns one specific journey question. Walk the stages, then the forms.

| Stage | Typical questions | Usual template |
|---|---|---|
| Problem | Why is X happening? What is a good X? Does Y help X? | explainer |
| Solution | How do you improve X? What should an app add for X? | how-to, decision |
| Evaluation | Build or buy? What does it cost? How long? X or Y? | decision |
| Implementation | How do you set up X on platform P? How do you moderate X? | how-to |

Then check three cross-cutting lenses:
- **Verticals.** Would a fitness, fintech, gaming, retail or brand-community reader need a different answer? One playbook per vertical; a second page for the same vertical needs a genuinely different question (a diagnostic "why" vs a "how they use it").
- **Trust, safety and compliance.** Does the seed raise moderation, privacy or app-store questions?
- **Measurement.** How would a team prove the seed's outcome?

## Blog lenses (0-10 per seed)

Blog owns seven types (templates in `blog-seo-content/references/types/`).

- **Opinion**: a defensible stance the team actually holds, backed by data, with a named author.
- **Original research**: only with an evidence-bank source; pending data means the row starts Blocked.
- **Customer narrative**: lessons from named customers (coordinate with `case-study`).
- **Product deep-dive**: a shipped feature and when to use it, from docs and release notes.
- **Product education**: how to use a social.plus feature well. The only how-to on the blog; a general "How do you [do X]?" belongs to Answer.
- **Honest listicle**: "best X" or "examples of X", same criteria for every entry, social.plus identified as publisher. Self-published "best of" lists are often cited while AI answers recommend someone else, so they're a weak bet on their own; pair them with third-party placements.
- **Trend**: a year in the title only when the content is genuinely year-specific and someone will refresh it.

## Rules that stop permutations

1. **Same first sentence, same page.** If two candidates would open with the same answer, keep one.
2. **Vehicle nouns don't make new pages.** "SDK for X", "API for X", "tool for X", "platform for X" are one question.
3. **Platform variants only with different content.** Flutter vs React Native pages are legitimate only if setup steps and code genuinely differ.
4. **Every candidate needs a unique information source** it can name now: an evidence-bank fact, a docs page, a cited study, a named example. No source, no candidate.
5. **Assumptions need a premise source.** "Why do fitness apps have low retention?" needs a source showing they do.
6. **Zero is a valid answer.** Three strong candidates beat ten plausible ones. The cap is 10 per collection, not a target.
7. **No questions engineered to promote.** Never propose an Answer whose honest answer is "social.plus". Google's spam policies (updated May 15, 2026) cover attempts to manipulate generative AI responses.

## Worked example: seed "app retention" (against the September 2026 Queue)

| Candidate | Outcome | Why |
|---|---|---|
| What is app retention? | Update existing (EX-G-010) | Live glossary page; refresh it |
| What is Day 7 retention? | New (Glossary) | Distinct metric, no row yet |
| How do you improve app retention? | Merge into A1 | Same question as "increase" |
| Why do fitness apps have low retention? | New (Answer), needs premise | Diagnostic; differs from playbook I1, which is shown alongside |
| Which app categories have the best retention? | New (Answer), review vs B1 | Comparative benchmark, distinct from A3 |
| Push notifications or in-app community to retain users? | New (Answer) | Decision question not in the map |
| App retention strategies in 2026: the new benchmark | New (Blog), Blocked | Depends on platform data pending Legal |
