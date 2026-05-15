# Citation Playbook

Why this file exists: for the topics where external citations genuinely support the claim, citation density is the single strongest content-level lever on AI visibility (Princeton/GT GEO study, +30-40% relative). But forcing citations into product how-tos produces fake or irrelevant links and degrades trust. This playbook defines what to cite, when, and where — by intent.

## Targets by intent

| Intent | External citations | Rationale |
|---|---|---|
| Definition | ≥2 required | Definitions and scale claims benefit from authoritative backing. Cite the concept's canonical source (spec, paper, analyst report) and one scale statistic. The compliance script enforces this minimum as a hard FAIL. |
| Comparative | ≥3 required | You're comparing things — link each compared option to its canonical source. Minimum one citation per compared option plus one for the decision criteria. The compliance script enforces this minimum as a hard FAIL. |
| Procedural | 0 required | Procedural articles about using social.plus rely on internal product consistency. A real social.plus how-to should name real surfaces (SDK, dashboard, moderation queues). External citations are only welcome if they support a claim about impact (e.g., retention lift from published research). |

Universal rule across all intents: **every numeric claim needs a source.** Either from the approved-data list in SKILL.md or an external citation. A number without a source is a fabrication risk.

## What counts as authoritative

Ranked by citation weight in AI retrieval:

1. **Peer-reviewed research** — arxiv.org, published journals, conference proceedings.
2. **Standards bodies** — W3C, IETF, NIST.
3. **Government and academic** — .gov and .edu domains.
4. **Named industry research with disclosed methodology** — Gartner, Forrester, Pew, McKinsey, Bain.
5. **Named product-company research** — Semrush, Ahrefs, HubSpot, Schema App studies; social.plus customer case studies.
6. **Primary-source news reports** — Reuters, FT, WSJ, The Verge (when they break the story).

Avoid:
- Content farms and SEO-mill "studies" with no methodology.
- Anonymous blog posts.
- Competitor marketing content.
- Wikipedia as a primary factual source (link for entity anchoring only, not for the claim).

## How to cite

### External sources

Inline markdown link, publisher name in the anchor text. Place the citation immediately after the claim:

> Apps with an in-app community layer see 10-35% higher retention than comparable apps without one ([Semrush AI Search study, 2025](https://www.semrush.com/blog/ai-search-seo-traffic-study/)).

Rules:
- Prefer the publisher name as anchor text, not "here" or "this study".
- Include the year when the finding is time-sensitive.
- Don't concentrate all citations in one section — distribute across the claim-heavy sections.

### Statistics

Every statistic includes the source and, when time-sensitive, the year. Prefer ranges over point estimates when the data supports it.

Good:
> Active-user engagement with feed surfaces typically lands in the 20-50% range.

(Acceptable without an external citation because 20-50% is in the approved-data list.)

Good:
> Brand mentions correlate with AI visibility at r=0.664 ([Ahrefs Brand Radar, July 2025](https://ahrefs.com/blog/)).

Bad:
> In-app feeds drive high engagement and significant retention gains.

### Quotations

Direct quotations from named sources score high AI visibility on their own. Keep them short (1-2 sentences) and attributed.

- Only real people, real statements, verified source.
- Never invent or paraphrase-to-quote.
- If the exact quote can't be verified, use paraphrase-plus-citation.

## Where to place citations

Priority order (concentrate citations where they drive extraction):

1. **Inside the TL;DR paragraph** — at least one citation or statistic for definition and comparative intents. This is the passage LLMs extract verbatim.
2. **"Why it matters" / "What X is best for" sections** — the business case should not lean on adjectives. At least one citation per major claim here.
3. **Dimension-by-dimension breakdown** (comparative only) — one citation per dimension where possible.

Do not place external citations inside the FAQ section, the conclusion, the pitch, or the metrics table. These stay clean so AI engines extract them without citation-chain overhead.

## Approved social.plus data (use freely, pre-cleared)

### Metric ranges (published social.plus data)

| Metric | Range |
|---|---|
| Engagement rate (active-user interaction with community features) | 20-50% |
| Retention lift (vs. apps without community features) | 10-35% |
| Active contributors (% of MAU who post/react/follow) | 10-30% |

### Approved customers and stats

| Customer | Approved stat |
|---|---|
| Noom | 45M+ users |
| Harley-Davidson | 1M+ community members |
| Smart Fit | 60% MoM growth |
| Ulta Beauty | (named only — no stat approved) |
| Betgames | 200M users |

Never invent customer names, stats, or quotes. Never attribute a customer to a use case they haven't publicly disclosed. When in doubt, omit.

## Pre-flight

Before running compliance, eyeball the article against this list (intent-aware):

- [ ] Intent-appropriate citation count: definition ≥2, comparative ≥3, procedural as-needed
- [ ] Every numeric claim has a source (approved list or external link)
- [ ] The TL;DR paragraph carries at least one citation or statistic (definition / comparative)
- [ ] FAQ, conclusion, pitch, and metrics table are citation-free
- [ ] No anonymous, content-farm, or competitor-marketing citations
- [ ] Every approved-customer mention matches the approved-stat list exactly
