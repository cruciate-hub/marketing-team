# Internal Linking Optimizer

Claude skill for producing SEO-grounded internal link recommendations for social.plus content — either inline link suggestions for a specific draft, or a site-wide linking audit across all 646 pages.

Every recommendation is grounded in `link-strategy.md` (canonical anchor map, cannibalization warnings, hub pages, anchor variation rules), regenerated quarterly from Ahrefs and GSC data.

## What it does

- **Draft mode** — given a specific draft (blog post, AEO article, or other), returns a ranked list of suggested links with anchor text, target URL, exact insertion point, and reasoning. Called as a pre-delivery step by `blog-seo-content` and `aeo-content`.
- **Audit mode** — given no specific draft, runs a 7-step site-wide audit and returns a prioritized fix plan with Structure Score and Anchor Score (target ≥ 8 / 10).
- **Reverse mode** — when a new page ships in Webflow, identifies 3-10 existing pages that should link *to* the new page and drafts the inbound edits.

## When it triggers

Trigger phrases include "audit internal linking", "check anchor text", "fix orphan pages", "internal link audit", "linking strategy", or "where should this article link to". Also invoked from other content-writing skills (`blog-seo-content`, `aeo-content`) as a pre-delivery step.

Do **not** use for backlink or external link work — that's `backlink-placement-finder` (outbound prospecting) or `link-building-vetter` (incoming requests).

## Architecture: two-phase shortlist + live fetch

The `pages-*.json` snapshot files are intentionally a lightweight heading index (H1-H6 + metaTitle + metaDescription, no body). Body content lives on the live web. This keeps snapshots small and the auto-regeneration cheap, but means heading-only data isn't enough to confidently pick an insertion point.

Every run uses two phases:

1. **Phase 1 — Shortlist (from JSON).** Scan headings + metadata to identify candidate link targets. Cheap, fast.
2. **Phase 2 — Verify + extract (live WebFetch).** For the top N shortlisted candidates only, fetch the live page. Use the fresh body to confirm the topic match, find the specific insertion sentence, and quote the surrounding context.

**Live-fetch budget:**
- Draft mode: max 1 WebFetch per shortlisted candidate, capped at 8 per invocation.
- Audit mode: reserved for the top 5-10 highest-impact gaps.

## Data files

Pick the files relevant to the context — don't load all 10 unless the question genuinely spans the whole site. All files share `{url, metaTitle, metaDescription, content}` structure; `content` preserves heading hierarchy via `#`, `##`, `###` markers.

| File | Covers | Items (approx) |
|---|---|---|
| `website/pages-marketing.json` | Homepage, product, pricing, feature/SDK/UIKit, white-label | ~22 |
| `website/pages-industry.json` | Static `/industry/*` pages | ~10 |
| `website/pages-use-cases.json` | `/use-case/*` | ~11 |
| `website/pages-blog.json` | `/blog/*` | ~248 |
| `website/pages-glossary.json` | `/glossary/*` | ~76 |
| `website/pages-answers.json` | `/answers/*` (AEO articles) | ~123 |
| `website/pages-customer-stories.json` | `/customer-story/*` | ~42 |
| `website/pages-release-notes.json` | `/release-note/*` | ~31 |
| `website/pages-product-updates.json` | `/product-update/*` | ~58 |
| `website/pages-webinars.json` | `/webinars/*` | ~25 |

`link-strategy.md` is always loaded — it's the ground truth for canonical decisions.

## Workflow (Draft mode)

1. Identify target keyword and topic cluster (Brand / Chat / Social / Video / Industry / Cross-cluster).
2. Cross-reference cannibalization warnings in `link-strategy.md`.
3. Phase 1 — shortlist up to 8 candidate pages from JSON by topic relevance + canonical anchor match.
4. Phase 2 — live-fetch each candidate; drop ones that don't pan out.
5. Score + rank by contextual relevance, canonical compliance, link-equity benefit, anchor variety, intent fit.
6. Apply the link budget for the article type (14 types in `link-strategy.md`): e.g. blog 3-7, AEO 1-3, glossary 2-4.
7. Apply anchor distribution targets + per-cluster variation rules.
8. Run the 8 evaluation questions + placement check + do-not-link check before finalizing.

## Workflow (Audit mode)

1. Link structure analysis — distribution table + Structure Score /10.
2. Orphan and under-linked pages classified by P1 / P2 / P3 tier.
3. Anchor text distribution + canonical compliance + Anchor Score /10.
4. Topic cluster analysis — pillar → children, children → pillar, sibling cross-links.
5. Authority-flow redistribution check (Priority 1 fixes — highest-leverage wins).
6. Contextual link gaps (JSON shortlist + live verification).
7. Cluster-specific reviews (AEO over-linking, customer-story ↔ industry, glossary citation gaps, blog cohesion).
8. Prioritized 4-phase implementation plan with effort + impact estimates, plus a "While looking at this..." section.

## General principles

- **Quote, don't paraphrase.** For headings or metadata, the JSON is the source. For body sentences, live-fetch first — never quote from memory.
- **Anchor text is keyword-only.** "chat widget", not "a chat widget". If the draft's phrasing blocks a clean anchor, propose a rewrite via the `Rephrase suggestion` field.
- **Respect the canonical map strictly.** If `link-strategy.md` says anchor X → page Y, that's the rule. Surface disagreements as flags, don't silently override.
- **Definitional vs commercial intent matters.** Glossary for definitions, product/use-case for commercial. Route per `link-strategy.md`.
- **Customer-story anchors use the customer name.** "Bitazza", "Noom" — not a proof-point claim.
- **Don't over-link.** Blog 3-7, AEO 1-3, generic 3-5.
- **No same-anchor-twice-to-same-target in one piece.** Use cluster anchor variants.

## Files

```
internal-linking-optimizer/
├── SKILL.md                          Skill entry point — three modes, two-phase architecture, workflow
└── README.md                         This file
```

Two external data files (auto-generated quarterly + on every CMS publish) live in the repo root and are fetched at runtime:

- `website/link-strategy.md` — canonical anchor map, cannibalization warnings, hub pages, scoring rubrics, link budgets
- `website/pages-*.json` — 10 page inventories (structure above)

If `link-strategy.md` is missing or its `Refresh by:` date is > 14 days in the past, the skill surfaces this before continuing.

## Output contracts

**Draft mode** — a clearly-labeled `## Internal link suggestions` block the calling skill embeds verbatim. Format matches the consuming content type (HTML `<a>` tags for blog, markdown `[anchor](URL)` for AEO). Each suggestion includes anchor, target URL, verbatim insertion quote, optional rephrase, ready-to-paste format, and one-line reasoning.

**Audit mode** — the 7-step analysis with tables, scores, and a prioritized 4-phase implementation plan. Always ends with a "While looking at this..." section (2-3 specific observations the user didn't ask for).

**Reverse mode** — a canonical anchor row to add to `link-strategy.md`, plus 3-10 ready-to-implement inbound edits (source URL + section + anchor + rule citation).

## Out of scope

- **`docs.social.plus`** — developer documentation lives on a separate subdomain not captured in any `pages-*.json`. When draft content references docs, the skill surfaces "no in-scope link target" rather than guessing.
- **The forum.** Same reason as docs.
- **External links / backlinks.** Use `backlink-placement-finder` or `link-building-vetter`.
- **Live Ahrefs runtime calls.** The skill stays static-data-driven; `link-strategy.md` is regenerated quarterly. Live WebFetch is used only for verifying insertion points on social.plus pages.
- **Auto-publishing to Webflow.** The skill recommends; the user implements.

## Escalation triggers (stop and ask Stefan)

- A cannibalization rule is violated but the writer insists the framing is correct.
- A new page's canonical anchor would conflict with an existing one.
- `pages-*.json` `_meta.itemCount` jumps by > 10% between publishes.
- DR drops by > 5 points since last `link-strategy.md` refresh.
- A proposed anchor would use a forbidden positioning term per `messaging/terminology.md`.
- The draft's target keyword is already cannibalized across 10+ URLs per GSC.
- `link-strategy.md` §"Refresh by:" is > 14 days in the past.

## Related skills

- `blog-seo-content` — invokes this skill as a pre-delivery step for long-form blog posts
- `aeo-content` — invokes this skill as a pre-delivery step for AEO articles (markdown links only)
- `backlink-placement-finder` — outbound link prospecting (sister skill, opposite direction)
- `link-building-vetter` — incoming link exchange requests (sister skill, opposite direction)
- `site-intelligence` — site-wide content audits beyond linking

## How files are loaded

All reference files are loaded from a shallow clone of this repo (`git clone --depth 1`) into `$MT_REPO`. The canonical fetch block at the top of the SKILL.md handles the clone; the skill then reads files with `cat "$MT_REPO/<path>"`.

## Adoption credit

The 7-step audit framework adapts patterns from [openclaw/skills internal-linking-optimizer](https://github.com/openclaw/skills/tree/main/skills/aaron-he-zhu/internal-linking-optimizer) (Apache-2.0). The cannibalization handling, canonical anchor map, social.plus-specific data layer, intent-aware definitional/commercial split, and skill-to-skill invocation pattern are net-new for this skill.
