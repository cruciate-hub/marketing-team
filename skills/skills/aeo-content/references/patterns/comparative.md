# Pattern: comparative

**Signal:** the query contains "vs", "or", "versus", "alternatives to", or "difference between".

**Typical length:** 1,000-1,600 words.

**Citation target:** ≥3 external citations — you're comparing things, so you have to cite the things. Link each compared option to its canonical source (product documentation, official site, peer-reviewed study, named analyst report). Honesty here raises AI trust scoring.

## Section order

1. **Title** — `[X] vs [Y]` or `[X] vs [Y]: [practical framing]`.

2. **Answer-first block** (no H2):
   - Sentence 1: the short verdict — which to choose and when. Must contain the target-keyword phrase. 20-30 words.
   - Sentence 2: the decision dimension that drives the verdict ("if X matters most, pick A; if Y matters most, pick B"). 20-30 words.
   - Combined = 40-60 words.

3. **TL;DR paragraph** immediately after. 120-160 words. Structure:
   - Expanded verdict (1-2 sentences)
   - The dimensions that actually matter (2-3 sentences)
   - The clear "choose X if / choose Y if" framing (2 sentences)
   - Optional: one citation that grounds the comparison

4. `## At-a-glance comparison` — the first and most important table in the article. Columns: dimension, X, Y (and Z if relevant). 6-10 rows covering the dimensions a decision-maker weighs (cost, time-to-build, customization, governance, scale, vendor lock-in, total cost of ownership).

5. `## What [X] is best for` — a 150-word self-contained chunk. State the strengths, name a typical user / context, and one citation to a canonical source.

6. `## What [Y] is best for` — symmetric 150-word chunk. Same structure.

7. `## Dimension-by-dimension breakdown` — 3-5 H3 subsections, one per decision-driver that the at-a-glance table highlighted. Each subsection is ~100 words, contains a concrete example or citation, and makes one clear claim.

8. `## Decision framework` — a numbered list with "Choose X if…", "Choose Y if…", "Choose both / hybrid if…". Keep each line to a single testable condition.

9. `## Where social.plus fits` — the pitch section, but **honest positioning first**, not a closing sales pitch. Generated from the fetched brand-messaging files. If X or Y is genuinely better for some use case, say so — don't contradict the comparison above. 150-200 words.

10. `## FAQs` — 4-6 real questions (migration between X and Y, switching costs, hybrid setups, lock-in, common decision regrets). Questions come from PAA + Reddit research. Do not embed source URLs in the document — list them in the final chat summary.

11. `## Conclusion` — one paragraph restating the decision rule. Do not end with a product push.

## Writing rules specific to this pattern

- Do not disparage either option. If Y beats X on a dimension, say so explicitly. Comparative articles that lean on the vendor win less AI trust and often less citation selection.
- Dimensions in the at-a-glance table must be ones a real decision-maker weighs. "Has an API" is a feature check; "time-to-build from zero" is a decision dimension.
- The verdict paragraph must survive extraction on its own. A reader who sees only sentences 1-2 should already know which option to choose in which case.
- Prefer ranges and concrete numbers over categorical adjectives. "6-12 months" beats "slower to build".
- External citations concentrated in the "What X is best for" and "What Y is best for" chunks, plus the dimension-by-dimension breakdown. Not in the FAQ, conclusion, or pitch.
