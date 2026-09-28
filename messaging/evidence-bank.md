# Evidence bank

The single list of facts social.plus content may state about itself, its customers and its platform. Used by `aeo-content`, `glossary-content` and `blog-seo-content`. If a fact is not here, or is not `Approved`, it does not ship.

## Why this file exists

The legacy /answers/ collection repeated the same four customer stats on nearly every page, because nothing else was approved. Repeating one fact across dozens of pages adds no independent evidence for AI engines and reads as templated content. This file fixes that in two ways: it grows the pool of facts, and it caps how often each one is used.

## Rules

1. **Only `Approved` facts may be published.** `Pending` facts can be drafted against, but the page stays at `Blocked: needs data` in the Content Queue until approval.
2. **Usage cap.** Each fact has a maximum number of Answer pages it can appear on (default 5). Glossary and Blog uses are tracked but not capped. When a fact hits its cap, find another fact or leave the claim out.
3. **Record every use.** After a page is approved in review, add its Queue ID to `Used on`. The writing skill proposes the update; a human confirms it.
4. **Cluster rule.** Every Answer page needs at least one fact not used by any other page in the same Queue cluster.
5. **Wording.** State the fact as written in `Claim`. Do not round up, generalise or combine facts into a new claim.
6. **Adding facts.** Add a row with source, date, owner and status `Pending`. Only the owner (or Legal, where noted) changes status to `Approved`.

## Approved customers

`aeo-content/scripts/compliance.py` keeps a matching whitelist (`APPROVED_CUSTOMERS`). The regression test in `aeo-content/tests/run_tests.py` fails if the two lists drift apart. Never name a customer who is not in this table, and never attribute a use case a customer has not publicly disclosed.

| Name | Claim | Source | Status | Cap (Answers) | Used on |
|---|---|---|---|---|---|
| Customer: Noom | 45M+ users | Published social.plus data (legacy approved list) | Approved | 5 | |
| Customer: Harley-Davidson | 1M+ community members | Published social.plus data (legacy approved list) | Approved | 5 | |
| Customer: Smart Fit | 60% month-over-month community growth after launch | Published social.plus data (legacy approved list) | Approved | 5 | |
| Customer: Ulta Beauty | Named only, no stat approved | Legacy approved list | Approved | 5 | |
| Customer: Betgames | 200M users | Published social.plus data (legacy approved list) | Approved | 5 | |

## Approved platform ranges

| ID | Claim | Source | Status | Cap (Answers) | Used on |
|---|---|---|---|---|---|
| R1 | Engagement rate on community features: 20-50% | Published social.plus data (legacy approved list) | Approved | 5 | |
| R2 | Retention lift vs apps without community features: 10-35% | Published social.plus data (legacy approved list) | Approved | 5 | |
| R3 | Active contributors: 10-30% of MAU post, react or follow | Published social.plus data (legacy approved list) | Approved | 5 | |

## Product facts

Verifiable specifics from social.plus documentation (learn.social.plus). These are the easiest source of unique information for how-to pages. Add each with the docs URL and the date checked.

| ID | Claim | Source (docs URL) | Date checked | Status | Cap (Answers) | Used on |
|---|---|---|---|---|---|---|
| | | | | | | |

## Pending: platform benchmarks (needs Legal approval)

Aggregated, anonymised data from the social.plus platform (BigQuery). This is the highest-value evidence in the engine because no competitor or AI model can reproduce it. Nothing here publishes until Legal approves both the metric and the wording.

| ID | Proposed claim | Query / method | Owner | Status | Blocks Queue IDs |
|---|---|---|---|---|---|
| P1 | Retention curves for users who join a community vs users who don't | To define | To assign | Pending | A4, BL1 |
| P2 | Participation benchmarks by vertical (fitness, fintech, gaming, retail) | To define | To assign | Pending | A3, BL1 |

## External facts

Third-party statistics used on more than one page. Record them here once so every page cites the same source and wording. Single-use external citations can live in the page only.

| ID | Claim | Source URL | Published | Date checked | Status | Used on |
|---|---|---|---|---|---|---|
| | | | | | | |
