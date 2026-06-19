# Backlink Placement Finder

Claude skill for finding contextually relevant backlink placement opportunities on partner websites for social.plus.

Given one or more partner URLs (or Google Doc drafts), this skill vets the site quality, discovers the best candidate articles, verifies anchor fit on the real page, and drafts a reply email with specific placement requests — which article, what anchor, which social.plus target.

## What it does

- Pre-screens partner sites via Ahrefs (DR, traffic, vertical fit, PBN/content-farm signals) before spending time on crawling.
- Checks whether social.plus already has a backlink from the partner domain — skips duplicates automatically.
- Discovers candidate articles via Ahrefs `crawled-pages` (the complete crawled inventory at ~1 unit/row; `pages-by-traffic` and `top-pages` are deliberately avoided), falling back to sitemap or Chrome index crawling when needed.
- Verifies every proposed anchor on the actual page (no hallucinated snippets).
- Matches anchors to the best social.plus target (blog post or glossary entry) — never homepage, product, or landing pages.
- Drafts a casual-but-professional reply email in the plain-text "Add link from / Add link to / Anchor" format that works on LinkedIn and email alike — plain URLs only, never markdown links (they don't render in email/LinkedIn/Slack).

## When it triggers

When a partner shares one or more website URLs (or unpublished article drafts in Google Docs) and the user needs outbound link placement suggestions. Trigger phrases include "find backlink placements", "check this site for link opportunities", "where can we place links on this site", "find anchors on this website", "backlink opportunities", or any paste of partner URLs asking for link placement suggestions.

The skill is for outbound link prospecting only (see `link-building-vetter` for vetting incoming requests).

## Two input modes

- **Mode A — Live partner URLs.** User pastes one or more website URLs (homepage, blog index, or direct articles). Ahrefs pre-screen runs first, then verification on real pages.
- **Mode B — Google Doc drafts.** Partner sends unpublished article drafts (often titled `[For Link Partners] ...`). No live site to crawl — the doc IS the article. Matching logic is identical; discovery step is skipped.

## Workflow

1. **Existing backlink check** — Pull social.plus referring domains once per session; skip any partner we already have a link from.
2. **Ahrefs pre-screen (Mode A)** — Tiered calls, cheapest first. Tier 1: DR/traffic/refdomains batch screen. Tier 2: vertical fit via organic keywords, competitors, linked domains, DR history. Tier 3: candidate URL discovery with topical `where` filters.
3. **Sitemap fallback** — Only when Ahrefs has no usable data. Try `sitemap.xml` → `sitemap_index.xml` → `robots.txt`. Filter to blog/article slugs. Triage by keyword match before opening.
4. **Verify on the actual page (MANDATORY)** — Never propose a placement without confirming the anchor text exists on the real page. Tool priority for live page reads: Vercel agent-browser if connected (primary), else Claude in Chrome. Read with `get_page_text`; if it returns empty or a stub, retry once after the page settles, then fall back to JavaScript DOM extraction via text-to-script ratio on ad-heavy sites.
5. **Match against anchors & inventory** — Two-phase approach. Phase 1 defaults to **editorial mode** at this stage of the funnel: read each surviving article end-to-end and surface 5-10 candidate angles per article BEFORE consulting any list. The lists (`anchors.md`, the pattern cache, the blog/glossary inventory) become *fences* applied to editorially-generated candidates, not *lookups* consulted before. By the time Phase 1 runs, the earlier tiers have narrowed the universe to ≤5 articles per surviving partner, so the cost concern that originally motivated list-matching ("can't read every page") no longer applies — at this scale, the reading IS the work. Editorial mode is what catches creative anchors the mechanical scan would never surface (e.g., the Pineable "social sellers" placement). When the funnel returned more than 5 candidates per partner, fall back to the semantic-territory scan from 13.20 instead. All six Phase 1 guardrails, the Anchor Diversity Check, and the fit-score ceilings apply regardless of mode.
   - **Phase 1** — Anchor exists verbatim in a body paragraph and maps to a valid target (anchor family or inventory topic). Partner just adds the link, zero text changes.
   - **Phase 2** — Topically relevant paragraph; partner needs to add or modify a sentence to accommodate the link.
6. **Draft the reply email** — Plain-text placement format, Phase 1 first, then Phase 2 with suggested text. When emitting via the Gmail draft tool (`create_draft`), an explicit `htmlBody` is also passed so visible anchor text stays clean (Gmail otherwise substitutes its outbound redirect as the visible link text).
7. **Summary table** — Every evaluation ends with a table of partner article → anchor → target → phase → fit score.

## Files

```
backlink-placement-finder/
├── SKILL.md                          Skill entry point — workflow, tiered Ahrefs calls, placement rules
├── README.md                         This file
└── references/
    ├── anchors.md                    Approved anchor text list
    ├── content-inventory.md          Matching heuristics — how to pick a target for a given anchor
    └── creative-anchor-patterns.md   Cache of confirmed Type B/C mappings (NOT the primary mechanism — Phase 1 step 0 territory scan is)
```

Two additional reference files live in the repo root (auto-generated by the Cloudflare Worker on every CMS publish):

- `website/pages-blog.json` — full blog inventory
- `website/pages-glossary.json` — full glossary inventory

If any of the five reference files is missing, the skill surfaces the failure immediately and refuses to guess. Stefan can trigger a manual refresh via the Cloudflare Worker's `/generate/blog` and `/generate/glossary` endpoints.

## Fit scoring

Phase 1 candidates come in three first-class types, all sharing the same six guardrails. The fit-score ceiling differs by type.

- **Type A: Literal anchor match.** Exact phrase from `references/anchors.md` appears verbatim in the partner's body paragraph.
- **Type B: Creative anchor match.** 2-6 word phrase verbatim in body, not literally in `anchors.md`, semantically equivalent to EITHER (a) a listed anchor family OR (b) a topic represented in the blog/glossary inventory (`metaTitle` / `metaDescription` / `content` headings). Route (b) catches phrases that map to real social.plus content even when the curated anchor list doesn't cover them — e.g., "social sellers" → `/blog/from-viewers-to-belonging-why-community-is-the-engine-of-live-commerce`.
- **Type C: Single-word glossary anchor.** Single word verbatim in body, focal noun of its sentence, unambiguous in context, maps to a glossary entry.

| Score | Meaning |
|---|---|
| ⭐⭐⭐ | Perfect — Type A literal anchor verbatim in body paragraph, partner article traffic ≥ 50/month, target UR ≥ 10, AND the anchor is not a saturated commercial head term (≥10 non-spam refdomains in the live profile — those cap at ⭐⭐ and yield to a fresher co-located variant). Type B and Type C never reach this tier. |
| ⭐⭐ | Strong — Type A with traffic or UR below the Perfect thresholds; OR any Type B creative match in body; OR any Type C single-word glossary match in body. |
| ⭐ | Opportunity — Phase 2: topic is relevant, specific paragraph identified, text modification required. |

Phase is determined by **whether the partner needs to edit text**, not by how the placement was discovered. Type A, B, and C all sit in Phase 1 (the partner just adds the link). The ⭐⭐ cap on B and C protects the relationship channel from AI over-reach on anchor identification; it is not a signal of lower discovery priority.

**Flags appended to the score in the summary table:**

- `[fresh-anchor]` — Type B or Type C placement whose anchor phrase has zero presence in the live anchor profile (positive signal: creative AND profile-diversifying).
- `[creative-anchor]` — Type B match (semantic-equivalent, not a literal `anchors.md` entry).
- `[single-word-glossary]` — Type C match.
- `[anchor-reuse: N refdomains]` — proposed anchor is at ≥5 refdomains in the live profile (saturation warning).
- `[low-value]` — partner traffic = 0 AND target UR < 5 (relationship-only).
- `[creative-phase2-save]` — Phase 2 creative anchor on a zero-Phase-1-match article (last-resort save).

**Anchor type, not just anchor text.** Anchors are classified by over-optimization risk (branded · naked-URL · generic/navigational · partial-match · exact-match commercial · stat-citation), and the skill prefers the lowest-risk type that fits — stat-citation and contextual anchors over exact-match commercial keywords, with at most one exact-match commercial anchor per batch. Variety comes from each partner's own sentences and from varying type per placement, never from synthetic rotation. The skill does not benchmark its anchor mix against competitors (their profiles are dominated by spam, UGC member-URLs, and "powered-by" widget links, so there is no valid target to drift toward).

## Placement rules (summary)

Hard rules enforced on every placement:

- **Anchors** — short (2–3 words), no branded anchors, no competitive keywords, never in intro or conclusion.
- **Target URLs** — blog posts (`/blog/...`) and glossary entries (`/glossary/...`) only. Never homepage, product, feature, SDK/UIKit, use-case, industry, pricing, or any marketing landing page.
- **Target UR check** — if the proposed social.plus page has URL Rating < 5, swap to a stronger target. Domain DR doesn't compensate for a thin page.
- **No competitor conflicts** — if the partner article already links to a social.plus competitor (Bettermode, Mighty Networks, Discourse, Tribe, Circle, etc.), either pick a different article or propose a swap instead of an insertion.

## What the skill will NOT do

- Trust Google search snippets as source — always verifies on the actual page.
- Use `marketing-team:site-intelligence` to pick targets — that skill catalogs static marketing pages, which are exactly the off-limits set.
- Decline a partner on category alone for incoming links — only the outbound direction has category restrictions.
- Auto-reject high-DR-low-traffic sites — surfaces them to Stefan with metrics and lets him call it.
- Suggest more than 5 placements per partner (best 2–3 per article, max).
- Write Phase 2 text that starts with "Additionally," "Furthermore," "Moreover," or other AI-sounding transitions.

## Ahrefs notes

- Always use `mode: subdomains` (never `domain`) to catch `blog.partner.com` and `www.partner.com`.
- Default to worldwide (no `country` parameter) — defaulting to `us` undervalues UK/EU/APAC partners.
- Order by `sum_traffic:desc` — `sum_traffic_merged` is select-only and the API rejects it as an order column.
- Check `subscription-info-limits-and-usage` at session start. For batches > 20 partners, gate Tier 2–3 to the top 30% by Tier 1 score.
- Ahrefs traffic is modeled, routinely off by 5–10×. Use as relative ranking only, never as a precise threshold.
- Ahrefs's index is incomplete on small blogs (60–80% of pages can be missing). Never declare "no fit" from Ahrefs alone — escalate to a sitemap/Chrome pass for sites that look legit on other signals.

## Output contract

Every run returns, in this order:

1. A draft reply email in the plain-text "Add link from / Add link to / Anchor" format.
2. A summary table of all placements with phase and fit score.
3. Any surfaced concerns (possible PBN, low-UR target, existing backlink, competitor conflict) with the specific metrics.

No unsolicited next steps, no fluff, no additional analysis unless asked.
