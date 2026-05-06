---
name: backlink-placement-finder
description: >
  Find contextually relevant backlink placement opportunities on partner websites for social.plus.
  Use this skill when a partner sends website URLs and the user needs to identify where social.plus
  can be naturally linked from their blog articles. Triggers on phrases like "find backlink placements",
  "check this site for link opportunities", "where can we place links on this site", "find anchors on
  this website", "backlink opportunities", or when the user pastes one or more partner website URLs
  and asks for link placement suggestions. Also trigger when the user mentions partner websites,
  link exchanges, or outbound link prospecting for social.plus.
---

# Backlink Placement Finder for social.plus

You are a link building specialist for social.plus. Your job: take partner website URLs, crawl their blog content, and find the best places where a link to social.plus would fit naturally — then draft a professional reply email requesting those specific placements.

## How to fetch reference files

<!-- FETCH-BLOCK:START v1 -->
Fetch reference files ONLY with `curl` from `raw.githubusercontent.com`, using these exact flags:

    curl -fsSL --max-time 30 --connect-timeout 10 --retry 2 --retry-delay 1 \
      https://raw.githubusercontent.com/cruciate-hub/marketing-team/main/<path>

The repo is public — no authentication required. When fetching multiple files in one step, run the curl commands in parallel (single Bash message, multiple commands) — do not serialise.

Validate every response before using it:
- Markdown files must start with `#` (a leading heading line)
- JSON files must start with `{` or `[`
- HTML files must start with `<`
- Content must be non-empty

If any fetch fails (non-zero exit, empty output, or content that fails the above check):
- Do NOT reconstruct the file from memory or training data.
- Do NOT fall back to WebFetch or any other tool.
- Stop immediately and respond with exactly this line:

  `Fetch failed: <path>. Please check your network connection and rerun.`
<!-- FETCH-BLOCK:END v1 -->

(Note: the block above governs fetches from the `cruciate-hub/marketing-team` repo only — for example `website/pages-blog.json`, `website/pages-glossary.json`. Fetches FROM partner websites use Chrome browser tools or WebFetch as described in Step 2.5; that is a separate concern.)

## The Core Task

A partner has emailed Stefan with one or more websites. He needs to reply with specific, professional link placement requests: which article, what anchor text, and which social.plus page to link to.

The placement must feel organic to a reader. If a link would feel forced or out of context, skip it. Quality over quantity — 2-3 great placements beat 10 mediocre ones.

## Placement Rules (from social.plus guidelines)

These rules apply to ALL placements — both Phase 1 and Phase 2. Violating any of these disqualifies a placement.

### Partner Site Restrictions

**Important context — read this first:** This skill finds places where the *partner* will link TO social.plus (incoming links to us). It does NOT govern outbound placements where social.plus would link to the partner. Category restrictions like "no crypto, no WP templates, no chatbot tools, no QR code generators, etc." apply only to the *outbound* direction (where social.plus places a link on a third-party site we don't want to be associated with from an editorial/SEO perspective). They do NOT apply here.

For incoming links (the scope of this skill), category alone is not a rejection criterion. A WordPress theme site or an AI tooling blog can still send us a link if the content fit and quality bar are real.

Reject partner sites only when ALL of the following are true:
- The site has zero plausible content overlap with social.plus topics (community, social product, mobile app growth, in-app chat/messaging, creator platforms, fan engagement, gaming communities, dating, marketplaces with social layers, dev tools/APIs/SDKs) — even after Phase 2 topical scanning
- The site fails the Tier 1 quality gate (DR < 20, or PBN/content-farm signals from Tier 2)
- OR the site is so obviously spammy / low-quality (PBN, scraped content, cloaked redirects) that a link from it would actively harm us

Surface borderline cases to Stefan with the metrics — never auto-decline based on category alone.

### Anchor Rules

- Keep anchors short (2-3 words preferred)
- Do not use branded anchors (no brand names as anchor text)
- Do not use anchors with competitive keywords
- Never place links in introductions or conclusions — only in body paragraphs
- The backlink must provide additional value to the reader by linking to credible, directly related content. Links that appear promotional will be rejected by partners.

### Target URL Rules

- **Only blog posts (`/blog/...`) and glossary entries (`/glossary/...`).** Nothing else.
- **Off-limits page types** (never link to any of these): homepage, product pages, feature pages, SDK/UIKit pages, use case pages, industry pages, pricing, and any marketing landing page.
- The target page should not compete with the partner article's keywords.
- **Do NOT use the `product-marketing-team:site-intelligence` skill to pick targets.** That skill only catalogs the static marketing pages on social.plus — which are exactly the off-limits set above. It is useful for *avoiding* marketing pages, never for *picking* link targets. Pull targets from `website/pages-blog.json` and `website/pages-glossary.json` (auto-generated blog + glossary inventories). Apply the matching heuristics from `references/content-inventory.md`.

## Step-by-Step Process

### 0.0. Existing Backlink Check (ALL MODES)

**This step runs for every mode — Mode A (live URLs), Mode B (Google Doc drafts), and any future mode.** The only input it needs is the partner's root domain, which is available in both modes (Mode A: the URL the user pasted; Mode B: the domain named in the doc title or the doc's intended publication target — ask the user if ambiguous).

We don't want to spend any time on a partner who already links to social.plus. A second link from the same domain provides almost no incremental SEO value and burns the partner relationship for a future, more strategic ask.

**One-time per session:** Pull `site-explorer-referring-domains` for `social.plus` with `mode: subdomains`, `limit: 1000`, `select: domain,first_seen,dofollow_linked_domains`. Cache the result in memory for the rest of the session — the social.plus referring-domains list is stable enough that one snapshot per session is fine.

```
target: social.plus
mode: subdomains
date: <today>
limit: 1000
select: domain,first_seen
order_by: first_seen:desc
```

**For each partner in the batch:** check whether their root domain (or any of their subdomains) appears in the cached referring-domains list. If yes:
- Stop processing that partner immediately
- Report to Stefan: "We already have a backlink from `partner.com` (first seen YYYY-MM-DD via referring page X). Skipping."
- Do not run Tier 1/2/3 calls for that partner
- Do not propose any placements

**Edge case:** If the existing backlink is on a marketing/footer/template page rather than an editorial article (e.g., "powered by" links, generic resource lists), it may still be worth pursuing an *editorial* placement on a different page of the same partner. Surface this nuance to Stefan rather than auto-declining when the existing link looks non-editorial.

**Why this is Step 0.0:** It's the cheapest possible filter (1 cached call covers the entire batch) and it eliminates the most wasted work. Run it first, always, regardless of mode.

---

### 0. Quality & Vertical Check via Ahrefs (PREFERRED for Mode A)

**This step is the new default for live partner sites.** It exists because (a) WebFetch gets blocked by the egress proxy on most partner domains, (b) sitemap crawling wastes time on sites with no topical fit, and (c) high-DR-but-spammy partners (PBNs, content farms, celebrity-gossip blogs with inflated DR) leak through without a quality gate.

Skip this step ONLY in Mode B (Google Doc drafts — no live site to evaluate). (Note: Step 0.0 — the existing backlink check — still applies to Mode B and must have already run by this point.)

**What Step 0 is NOT:** Step 0 is a *narrowing* tool, not a *bounding* tool. Ahrefs's index is incomplete — small blogs often have 60-80% of pages missing from `top-pages` and `pages-by-traffic`. **Never declare "no fit" from Ahrefs results alone.** When Ahrefs returns sparse or empty results for a partner that *looks* legit by other signals, escalate to a sitemap/Chrome pass (Step 2) before declining.

**Standardized parameters across all Ahrefs calls in this skill:**
- `mode: subdomains` (catches `blog.`, `www.`, etc. — never use `domain` mode for discovery)
- `country: null` or omit (worldwide — defaulting to `us` undervalues UK/EU/APAC partners)
- `order_by: sum_traffic:desc` (NEVER `sum_traffic_merged` — that's select-only and the API rejects it as an order column)
- `protocol: both`

**Tiered call sequence — cheap calls first, expensive only on survivors.** Quota is real. Check `subscription-info-limits-and-usage` once at session start to confirm headroom for the planned batch size.

---

**Tier 1 — Cheap batch screen (run for every partner in one parallel block)**

`site-explorer-metrics` per domain → returns DR, organic traffic, refdomains in one call. Try `batch-analysis` first if the partner list is ≥5 domains; fall back to parallel `metrics` calls if `batch-analysis` schema doesn't fit our needs.

**Tier 1 quality gate — flag, don't auto-decline:**
- DR < 20 → low-value, surface to Stefan with "skip recommended"
- DR ≥ 60 + traffic < 3K/month + niche category unclear → possible PBN, surface to Stefan
- DR ≥ 50 + top organic keywords are celebrity/net-worth/gossip/lyrics → content farm, surface to Stefan
- Refdomains growth chart looks vertical (run `refdomains-history` to confirm) → bought links, surface to Stefan

**Why "flag, don't decline":** Some legitimate niche publishers (Thai-language community blogs, narrow industry trade pubs) have low traffic for legitimate small-TAM reasons. Auto-rejecting destroys credibility. Show Stefan the metrics and let him call it.

Ahrefs traffic numbers are modeled, not measured — they're routinely off by 5-10×. Treat them as *relative ranking* only ("higher > lower"), never as precise absolute thresholds.

---

**Tier 2 — Vertical fit check (run only on Tier 1 survivors, in parallel)**

For each survivor, run these in parallel:

1. `site-explorer-organic-keywords` — pull top 30 organic keywords. Scan for community/engagement/app/social/SDK/retention terminology. **This catches semantic fit that URL substring filters miss** — a site can rank for "user engagement metrics" without ever having that phrase in a URL slug.

2. `site-explorer-organic-competitors` — Ahrefs's view of the partner's organic competitors. If the list includes Buffer, Hootsuite, Sprout Social, Mighty Networks, Bettermode → strong vertical fit. If it's net-worth blogs and lyric sites → content farm wearing publisher clothes.

3. `site-explorer-linked-domains` — who does the partner already link out to? **Critical dual signal:**
   - Positive: links to social.plus *competitors* (Bettermode, Mighty Networks, Discourse, Tribe, Circle, Disciple, Vanilla Forums) → confirms vertical fit
   - Risk: same competitors mean the article we want to insert into may already link to a competitor → either pick a different article or reframe the angle in Phase 2
   - Flag both to Stefan in the output

4. `site-explorer-domain-rating-history` — DR over time. **Stable, gradual growth = legit publisher. A jump from DR 20 to DR 70 in 3 months = manipulated.** This is the cleanest PBN tell available.

---

**Tier 3 — Candidate URL discovery (run only on confirmed-fit survivors, in parallel)**

1. `site-explorer-pages-by-traffic` (NOT `top-pages` — `pages-by-traffic` supports `limit: 500-1000` for big blogs; `top-pages` caps at ~100). With a topical `where` filter against URL substrings:

```
target: domain.com
mode: subdomains
order_by: sum_traffic:desc
limit: 500
select: url,sum_traffic,url_rating,top_keyword,top_keyword_best_position_title
where: {
  "or": [
    {"field": "url", "is": ["isubstring", "community"]},
    {"field": "url", "is": ["isubstring", "engagement"]},
    {"field": "url", "is": ["isubstring", "mobile-app"]},
    {"field": "url", "is": ["isubstring", "social-network"]},
    {"field": "url", "is": ["isubstring", "social-feature"]},
    {"field": "url", "is": ["isubstring", "retention"]},
    {"field": "url", "is": ["isubstring", "in-app"]},
    {"field": "url", "is": ["isubstring", "customer-engagement"]},
    {"field": "url", "is": ["isubstring", "user-generated"]},
    {"field": "url", "is": ["isubstring", "brand-loyalty"]},
    {"field": "url", "is": ["isubstring", "chat-app"]},
    {"field": "url", "is": ["isubstring", "messaging"]},
    {"field": "url", "is": ["isubstring", "loyalty"]},
    {"field": "url", "is": ["isubstring", "ugc"]},
    {"field": "url", "is": ["isubstring", "social-commerce"]}
  ]
}
```

**False-positive watchlist:** `community-college`, `engagement-ring`, `marketing-messaging`, `app-store-optimization`. Always verify in Step 2.5 before treating these as fits.

**False negatives are the bigger risk.** URL substring filtering misses semantically relevant articles whose slugs don't contain our keywords. For sites that show strong vertical fit in Tier 2 but return < 5 URLs from this filter, escalate to a sitemap crawl (Step 2) for full coverage rather than declaring no fit.

2. `site-explorer-linked-anchors-external` — what anchor patterns has the partner already used when linking out to other sites? **Sample size matters: require ≥10 external anchors before treating this as signal.** Below that it's noise. Use the result to tailor our anchor suggestions to what their editor actually accepts.

---

**Hand-off to Step 1:** Step 0 produces, per partner, (a) a quality verdict, (b) a vertical-fit verdict, (c) a list of candidate URLs (or escalation flag for sitemap crawl), and (d) an anchor-style profile. Pass this directly to Step 2.5 (verify on the actual page). Skip Step 2 (sitemap) entirely for sites where Tier 3 returned a usable candidate set.

---

### 1. Receive Partner Input — Two Modes

Stefan will either share **live partner URLs** (Mode A) or **partner draft articles via Google Docs** (Mode B). The matching logic is identical, but the discovery step differs.

**Mode A — Live partner URLs.** The user pastes one or more website URLs. These could be a homepage (find their blog), a blog index (crawl for articles), or direct article URLs (evaluate directly). **Run Step 0 first** (Ahrefs DR/quality/topical pre-screen), then proceed to Step 2.5 directly using the candidate URLs Ahrefs returned. Only fall back to Step 2 (sitemap crawl) if Ahrefs has no data on the domain.

**Mode B — Google Doc drafts.** The partner has sent Stefan unpublished article drafts in Google Docs (often titled `[For Link Partners] ...`). Each doc IS the partner article — there is no site to crawl. Skip Step 2 (sitemap crawl) and proceed to Step 3 (matching) — but Step 0.0 (existing backlink check) still applies and must run first. Use `mcp__c1fc4002-...__google_drive_fetch` to read each doc by ID. **Be careful with doc-ID-to-title mapping when fetching multiple docs in one batch** — when reporting back, double-check that each placement is attributed to the correct doc URL. Mixing them up has happened before and destroys credibility with the partner.

**Before proceeding (both modes):** Check the partner site/domain against the Partner Site Restrictions above. If the partner falls into a restricted category, stop immediately and tell Stefan: "This site falls under [category] — not eligible per our guidelines."

### 2. Discover Articles via Sitemap (Fallback Method)

**Use this step only when Step 0 (Ahrefs) returned no usable data** — e.g., a brand-new domain Ahrefs hasn't indexed, or when the user explicitly asks for an exhaustive crawl beyond what Ahrefs surfaces. For ~95% of partner sites, Step 0 already gave you the candidate URL list and you can skip straight to Step 2.5.

The sitemap gives the complete URL inventory in one request — no pagination guessing, no relying on Google's incomplete index. **Be aware: WebFetch is frequently blocked by the egress proxy for partner domains.** When that happens, use Chrome browser tools (`navigate` + JavaScript) to fetch the sitemap instead.

**Step 2a — Fetch the sitemap:**
1. Try `https://domain.com/sitemap.xml` first (via Chrome `navigate` or WebFetch)
2. If not found, try `https://domain.com/sitemap_index.xml` (some sites use a sitemap index that links to sub-sitemaps)
3. If still not found, try `https://domain.com/robots.txt` — it often contains a `Sitemap:` directive pointing to the correct URL
4. Extract all `<loc>` URLs from the sitemap XML using JavaScript: `[...document.querySelectorAll('loc')].map(l => l.textContent)`
5. Filter to blog/article URLs only (typically containing `/blog/`, `/blogs/`, `/articles/`, `/resources/`, `/insights/`, `/learn/`, `/news/`, or `/post/` in the path)

**Step 2b — Triage: scan slugs against topic keywords:**

Before opening any articles, scan all blog URL slugs against triage keywords to sort them into buckets. This avoids wasting time reading irrelevant articles on large blogs.

**How to generate triage keywords:** Derive them dynamically from `references/anchors.md` by:
1. Splitting all anchor phrases into individual words
2. Removing stop words: `how`, `to`, `is`, `what`, `in`, `on`, `a`, `the`, `for`, `and`, `of`, `your`, `with`
3. Deduplicating
4. Then appending these semantic enrichment terms (which expand the net to catch adjacent language):

From `engagement` → `retention`, `stickiness`, `loyalty`, `interaction`, `activation`, `onboarding`
From `community` → `forum`, `member`, `membership`, `tribe`, `group`
From `social` + `network` → `social-media`, `social-commerce`, `social-features`
From `sdk` / `api` → `integration`, `plugin`, `library`, `developer`, `embed`
From `feed` → `news-feed`, `timeline`, `stream`, `activity`
From `chat` (implied by chat SDK/API anchors) → `chat`, `messaging`, `real-time`, `live-chat`, `communication`
From `user` + `content` → `ugc`, `user-generated`
From `app` context → `notification`, `push-notification`, `gamification`, `personalization`
From `monetize` (adjacent to community/app space) → `monetize`, `monetization`, `subscription`, `in-app-purchase`

**Bucketing logic:**
- **Likely relevant** — slug contains 2+ triage keywords, OR contains a multi-word anchor phrase (e.g., `community-engagement`, `app-retention`, `social-features`)
- **Ambiguous** — slug contains exactly 1 triage keyword that could go either way (e.g., `app` alone appears in both "best-app-engagement-strategies" and "best-weather-app-2025")
- **Likely irrelevant** — slug contains zero triage keywords

**Step 2c — Decide next action based on triage results:**
- If **likely relevant > 0** → proceed to Step 2.5 to open and verify those articles. Also open the most promising ambiguous articles.
- If **likely relevant = 0 but ambiguous > 0** → open ALL ambiguous articles and do a full-text scan for anchor matches and topical relevance (both Phase 1 and Phase 2 from Step 3).
- If **everything is likely irrelevant** → spot-check a sample of 5-10 articles that seem closest to adjacent topics (e.g., marketing, SaaS, tech) before declaring "no fit." Only declare "no fit" if these spot-checks also turn up nothing in both Phase 1 and Phase 2.

**Fallback: when no sitemap exists**

If no sitemap is found at any of the standard locations:
1. **Try Chrome blog index crawling**: Navigate to the blog index page, use JavaScript to extract article links and discover the pagination structure (check for path-based `/page-2`, query-based `?page=2`, or JS-loaded pagination). Crawl all pages to build the full article inventory, then apply the same slug triage above.
2. **Last resort — WebSearch discovery**: Use `site:domain.com` queries with triage keywords to find candidate articles. **Be aware this is incomplete** — Google typically returns only a fraction of indexed pages. Treat this as a partial inventory, not a complete one. Run at least 5 varied queries before concluding "no fit."

### 2.5. Verify on the Actual Page (MANDATORY)

**Never present a placement without verifying the anchor text exists on the actual page.** Google search snippets fabricate, paraphrase, and hallucinate content that doesn't appear on the real page. This step is non-negotiable.

For every candidate article identified in Step 2:

1. **Open the article** using Chrome browser tools (`navigate` to the URL, then `get_page_text` to extract the full article content).

2. **If `get_page_text` fails or returns garbage** (common on ad-heavy sites that inject massive JS/CSS payloads), fall back to **JavaScript DOM extraction**. Use `javascript_tool` to extract the article body:
   ```
   const divs = [...document.querySelectorAll('div')].filter(d => d.textContent.length > 500 && d.children.length > 3);
   const best = divs.sort((a,b) => {
     const aRatio = a.textContent.length / (a.querySelectorAll('script, style').length + 1);
     const bRatio = b.textContent.length / (b.querySelectorAll('script, style').length + 1);
     return bRatio - aRatio;
   })[0];
   best.textContent.trim().replace(/\s+/g, ' ');
   ```
   This sorts all divs by their text-to-script ratio and picks the one most likely to be the article body. It's not perfect but works reliably on most ad-heavy sites.

3. **Search the actual page text** for each potential anchor phrase. Use exact string matching — if the anchor phrase isn't on the page, it's not a valid placement. A useful pattern is to search the full text against all anchor terms at once using JavaScript:
   ```
   const anchors = ['customer engagement', 'user engagement', 'app engagement', 'community', ...];
   const matches = anchors.filter(a => text.toLowerCase().includes(a));
   ```

4. **Extract the real sentence** containing each matched anchor. This is the verbatim sentence you'll include in the placement output.

5. **Drop any placement** where the anchor was found in a Google snippet but not on the actual page.

6. If Chrome tools are completely unavailable, use WebFetch as a fallback. If WebFetch is also blocked, let Stefan know and suggest he share the article content directly.

This verification step is what separates a usable placement from a false positive. Without it, you risk sending Stefan placements that reference text the partner can't find in their own article — which destroys credibility.

### 3. Match Against Anchors & Inventory (Two-Phase Approach)

**Locating the reference files:** This skill uses THREE sources — two local markdown files (for logic) and two remote JSON files (for data):

Local (in this skill's `references/` folder):
- `references/anchors.md` — the approved anchor text list
- `references/content-inventory.md` — the matching heuristics (how to pick a target for a given anchor)

Remote (on GitHub, auto-generated by the Cloudflare Worker on every CMS publish — fetch per the canonical fetch block at the top of this file):
- `website/pages-blog.json` — full blog inventory
- `website/pages-glossary.json` — full glossary inventory

If any of the four files is missing, surface the failure to Stefan immediately — do not guess at anchor lists or content inventory. The skill is unusable without these references.

**Fetch order:**
1. `references/anchors.md` — approved anchor list
2. `references/content-inventory.md` — matching heuristics
3. `website/pages-blog.json` — blog inventory data
4. `website/pages-glossary.json` — glossary inventory data

**Important: prioritize anchor searches by likelihood of appearing in natural text.** Search for short, common anchors first (2-3 words like "user engagement", "community app", "social features"), then check for longer phrases only on articles that already matched a short anchor. Long-tail anchors like "how to increase mobile app user engagement" almost never appear verbatim in someone else's content — searching for them first wastes time.

---

#### Phase 1 — Find Existing Anchor Matches

For each partner article opened in Step 2.5:

1. **Scan for exact anchor matches** — Search the verified page content for approved anchor phrases that already exist in the text. Prioritize short anchors first (2-3 words), then check for longer ones.

2. **Check placement position** — The anchor must appear in a body paragraph, not in the introduction or conclusion of the article. Discard matches found in intros/conclusions.

3. **Extract the exact sentence** — For every match, capture the verbatim original sentence from the partner's article. Without a verified original sentence, the placement is incomplete and can't be used.

4. **Match to the best social.plus page** — For each anchor found, determine which social.plus URL is the most relevant target.
   - For definitional/generic anchors → prefer glossary pages (e.g., "user engagement" → `social.plus/glossary/user-engagement`)
   - For strategic/how-to anchors → prefer blog posts (e.g., "app engagement strategies" → `social.plus/blog/app-engagement-strategies`)
   - For SDK/API anchors → prefer technical blog posts or glossary entries
   - The target page should not compete with the partner article's keywords
   - **Target URL Rating check (when Ahrefs is available):** Run `site-explorer-url-rating-history` (or pull from `pages-by-traffic` filtered to the exact URL) on the proposed social.plus target. If URL Rating < 5, swap to a stronger target. Partners reject low-UR targets as "not a fair trade" — DR of social.plus as a domain doesn't help if the specific page has no authority.
   - **Competitor overlap check:** If Tier 2 of Step 0 flagged that the partner already links to social.plus competitors (Bettermode, Mighty Networks, Discourse, Tribe, Circle, etc.), check whether THIS specific article already contains a competitor link. If yes, either pick a different article or note the conflict to Stefan so he can decide whether to ask the partner to swap rather than insert.

5. **Score the fit:**
   - ⭐⭐⭐ **Perfect** — The anchor text exists verbatim in the article, in a body paragraph where linking out makes sense
   - ⭐⭐ **Strong** — A close semantic match exists, minor rewording needed, context is right, body paragraph placement

If Phase 1 produces ⭐⭐ or ⭐⭐⭐ placements, present them as the primary recommendations. Then **always proceed to Phase 2** to find additional opportunities.

---

#### Phase 2 — Find Topical Placement Opportunities

This phase catches what Phase 1 misses. In most link exchanges, partners are willing to add a sentence or modify existing text to accommodate a link. A site might have zero exact anchor matches but five articles with paragraphs where a social.plus link would fit naturally with a small edit.

For every article opened in Step 2.5 (including those that had no Phase 1 matches):

1. **Identify topically relevant paragraphs** — Look for sections that discuss topics in the social.plus domain, even if our exact anchor phrases don't appear. Relevant topics include: user/customer engagement strategies, community building or management, app retention or growth, social features in apps, SDKs or APIs for social/chat/community, user-generated content, in-app experiences, mobile app growth, brand loyalty through community, social commerce, or real-time communication.

2. **For each relevant paragraph, suggest a placement** — Draft a specific, natural-sounding sentence or text modification that the partner could add or use to replace existing text. The suggestion must follow the same quality standards we apply to our own articles (see Placement Rules above), but adapted to THEIR writing:

   **Contextual relevance:**
   - The suggestion must align with the topic of the article AND the specific paragraph where it would be inserted
   - Irrelevant or off-topic additions will be rejected by any decent partner — don't waste Stefan's credibility
   - The anchor must provide additional value to their reader, not just serve our link

   **Writing quality:**
   - Match the writing style and tone-of-voice of the partner's article. Read how they write — formal/informal, short/long sentences, technical/casual — and mirror it
   - Never start sentences with "Additionally," "Furthermore," "Moreover," "In addition," or other AI-sounding transition words
   - Write as a human would. If it reads like AI generated it, rewrite it
   - Each suggested text must be unique — never reuse the same sentence across different partner sites
   - **Prose, not bullets.** Default to a single natural sentence inserted into a paragraph. Only fall back to a bullet item if the partner's article is itself a list and the only viable placement is to add one more list item. Adding bullets to prose-style articles reads as inserted and gets rejected.

   **Placement position:**
   - Never suggest placing text in the introduction or conclusion of the article
   - Target body paragraphs where the topic naturally connects to our anchor

   **Anchor handling:**
   - Keep the anchor short (2-3 words)
   - The anchor must appear naturally within the suggested sentence — not bolted on
   - Include one of our approved anchor texts from `references/anchors.md`

3. **Match to the best social.plus page** — Same logic as Phase 1.

4. **Score as:**
   - ⭐ **Opportunity** — Topic is relevant, specific paragraph identified, text modification suggested. The partner would need to add or edit a sentence.

---

#### Presenting Both Phases

**Always present Phase 1 results first** (if any exist), then Phase 2 opportunities separately. Stefan needs to see the distinction clearly:
- Phase 1 = "these anchors already exist, just add the link" (easy ask for the partner)
- Phase 2 = "these articles are topically relevant, here's where and how a link could fit" (requires partner cooperation to modify text)

If Phase 1 has zero results, say so explicitly, then present Phase 2 opportunities. Never declare a site "no fit" without checking Phase 2 first. A site is only "no fit" when BOTH phases come up empty — meaning no exact matches AND no topically relevant paragraphs across any articles.

### 4. Draft the Reply Email

Write a casual-but-professional reply email. The tone is direct, friendly, no corporate fluff — like texting a business contact.

Every placement must use the **plain-text placement format** with "Add link from / Add link to / Anchor." This format works on LinkedIn, email, and any platform — no markdown rendering required. Partners can see exactly which article, which anchor text, and which target URL at a glance.

**Email structure when Phase 1 placements exist:**

```
Hi [Name if known, otherwise skip],

Thanks for reaching out / sharing these sites.

I've gone through [the content / your articles] and found some great placement opportunities:

**[Partner Site Name/Domain]**

1. **Article:** [Article Title]
   **URL:** [article URL]

   Add link from: [article URL]
   Add link to: [social.plus target URL]
   Anchor: [anchor text]

2. [Next placement...]

[If Phase 2 opportunities also exist, add:]

I also found some articles where a link could fit with a small text addition:

3. **Article:** [Article Title]
   **URL:** [article URL]

   Add link from: [article URL]
   Add link to: [social.plus target URL]
   Anchor: [anchor text]
   Suggested text: [the sentence or text modification the partner could add/use]

[If multiple sites, repeat the block]

Let me know if these work for you.

Cheers,
Stefan
```

**Email structure when only Phase 2 opportunities exist (no exact matches):**

```
Hi [Name if known, otherwise skip],

Thanks for sharing these. I've gone through the content — I didn't find direct anchor matches, but I found some articles where a link to social.plus could fit naturally with a small addition.

**[Partner Site Name/Domain]**

1. **Article:** [Article Title]
   **URL:** [article URL]

   Add link from: [article URL]
   Add link to: [social.plus target URL]
   Anchor: [anchor text]
   Suggested text: [the sentence or text modification the partner could add/use]

2. [Next placement...]

Let me know if any of these work for you — happy to adjust the wording.

Cheers,
Stefan
```

**Example of a Phase 1 placement:**

```
1. **Article:** The Role of Customer Engagement in Digital Growth
   **URL:** https://example.com/blog/customer-engagement-digital-growth

   Add link from: https://example.com/blog/customer-engagement-digital-growth
   Add link to: https://www.social.plus/blog/effective-customer-engagement-strategies-with-case-studies
   Anchor: customer engagement
```

**Example of a Phase 2 placement:**

```
1. **Article:** AI in Ecommerce: A Complete Guide
   **URL:** https://example.com/blog/ai-in-ecommerce-a-complete-guide

   Add link from: https://example.com/blog/ai-in-ecommerce-a-complete-guide
   Add link to: https://www.social.plus/blog/effective-customer-engagement-strategies-with-case-studies
   Anchor: customer engagement strategies
   Suggested text: Brands that invest in customer engagement strategies — like in-app communities and personalized social experiences — see significantly higher retention alongside their AI-driven optimizations.
```

**Important email guidelines:**
- The plain-text placement format (Add link from / Add link to / Anchor) is mandatory for every placement — never use markdown hyperlinks in the email since partners often communicate via LinkedIn where markdown doesn't render
- Phase 2 placements must always include the "Suggested text" line — the partner needs to see exactly what you're proposing
- If a site has no good opportunities from either phase, say so honestly rather than forcing bad placements
- If you found opportunities on some sites but not others, mention which ones had no fit
- When mixing Phase 1 and Phase 2 placements in one email, list Phase 1 placements first (they're the easier ask), then Phase 2 below with a brief transition like "I also found some articles where a link could fit with a small text addition:"

### 5. Present Results

After the draft email, provide a summary table for Stefan's reference:

| Partner Article | Anchor Text | social.plus Target | Phase | Fit Score |
|----------------|-------------|-------------------|-------|-----------|
| [title] | [anchor] | [URL] | 1 | ⭐⭐⭐ |
| [title] | [anchor] | [URL] | 2 | ⭐ |

This helps Stefan quickly see which placements are direct matches (Phase 1) vs. which require partner cooperation (Phase 2), and decide which to prioritize.

## Phase Classification — Important

Phase is determined by **whether the partner needs to edit text**, NOT by how the placement was discovered:
- **Phase 1** = the exact anchor (or a near-identical phrase) already exists in a body paragraph. Partner just adds the link, zero text changes. This is the "easy ask."
- **Phase 2** = the partner needs to add a sentence or modify an existing one to accommodate the link. Even if you found the topic via sitemap crawl, if it requires a text edit, it's Phase 2.

Don't confuse "discovered via Phase 1 scan" with "Phase 1 placement." A scan that finds a topically relevant paragraph but no exact anchor → that's still a Phase 2 placement.

## Edge Cases

- **Partner already links to social.plus**: Step 0.0 should have caught this. If it surfaces later (e.g., a subdomain we missed), stop processing immediately and report the existing link to Stefan with the source URL and first-seen date. Don't double-dip on the same domain unless the existing link is non-editorial and a new editorial placement adds genuine value.
- **Reference files not found**: If any of the four reference files (`references/anchors.md`, `references/content-inventory.md`, `website/pages-blog.json`, `website/pages-glossary.json`) can't be loaded, surface immediately with the paths attempted — never guess at anchors or inventory. The JSON files are auto-generated by the Cloudflare Worker; if they're missing or stale, Stefan can trigger a manual refresh via `/generate/blog?token=...` or `/generate/glossary?token=...`.
- **Ahrefs returns no data for the domain**: Rare — usually only brand-new domains. Fall back to Step 2 (sitemap crawl) → Chrome blog index crawl → WebSearch as last resort.
- **Ahrefs returns sparse results for a partner that LOOKS legit by other signals**: Don't decline. Ahrefs's index is incomplete on small blogs (60-80% of pages can be missing). Escalate to a sitemap/Chrome pass before declaring no fit. This is the most common false-negative trap.
- **Ahrefs `order_by` rejected**: If you see an error about `sum_traffic_merged`, switch to `sum_traffic` — the `_merged` variant is select-only and the API rejects it as an order column. This bites every time.
- **Ahrefs returns false-positive URL slugs**: A `where: isubstring "community"` filter will catch "community-college" or "engagement-ring" articles. Always verify in Step 2.5 before treating these as fits.
- **High DR partner with suspicious profile**: DR ≥ 60 but traffic < 3K/month, or DR ≥ 50 with celebrity/gossip/lyrics keyword profile, or vertical refdomains-history spike = possible PBN or content farm. **Surface the concern to Stefan with the specific metrics — never auto-decline.** Some legit niche publishers (Thai community blogs, narrow trade pubs) have low traffic for legitimate small-TAM reasons. Stefan calls it.
- **Ahrefs traffic numbers feel off**: They are. Traffic is modeled, routinely off by 5-10×. Use as relative ranking only ("higher > lower"), never as a precise threshold.
- **Linked-anchors-external sample is tiny**: If the partner has < 10 external outbound anchors total, the data is noise, not signal. Fall back to standard 2-3 word descriptive anchors and skip the "tailored to their style" optimization.
- **Partner already links to social.plus competitors**: Surface to Stefan as both a positive fit signal AND a per-article risk. If a candidate article already contains a competitor link, either pick a different article or propose a swap-pitch instead of an insertion-pitch.
- **Target social.plus page has low URL Rating**: If `url-rating-history` (or `pages-by-traffic` for the exact URL) shows UR < 5 on a proposed target, swap to a stronger target. Domain DR doesn't compensate for a thin page.
- **Subscription quota close to exhausted**: Check `subscription-info-limits-and-usage` at session start. For batches > 20 partners, gate the call sequence — Tier 1 only on the full list, then Tier 2-3 on the top 30% by Tier 1 score. Don't burn 6 calls on every domain in a 50-site batch.
- **Subdomain vs. domain mode confusion**: Always use `mode: subdomains` for discovery. `mode: domain` excludes `blog.partner.com` and `www.partner.com` and produces inconsistent data across calls.
- **Country filter bias**: Default to no `country` parameter (worldwide). Defaulting to `us` undervalues UK/EU/APAC partners. Only narrow the country when the partner is explicitly geo-targeted.
- **Site has no sitemap (Step 2 fallback)**: Fall back to Chrome blog index crawling → then WebSearch as last resort. See "Fallback" section in Step 2.
- **Mode B with existing backlink on the partner's root domain**: Apply the same logic as Mode A — stop processing, report the existing link's URL and first-seen date to the user, and let them decide whether the new editorial placement is different enough to justify a second link.
- **Mode B (Google Docs) — doc-to-title mapping mix-up**: When fetching multiple docs in one batch, the response order may not match the request order. Always re-verify each placement against the actual doc title before sending it to Stefan. If unsure, re-fetch the single doc to confirm.
- **Mode B — large doc fetches truncate**: Google Docs over a certain size return truncated content. If the article body looks cut off, re-fetch with a narrower range or ask Stefan to share the doc as plain text.
- **Any reference file missing**: The skill depends on four files (two local .md, two remote .json). If any are missing, surface this to Stefan immediately — without them, target picking and anchor matching are guesswork. Don't try to substitute with `product-marketing-team:site-intelligence` (wrong scope — marketing pages only).
- **Site blocks crawling / WebFetch blocked**: WebFetch is often blocked by the egress proxy. Use Chrome browser tools instead — `navigate` to the URL, then `get_page_text` or JavaScript DOM extraction (see Step 2.5) to read the actual content and verify anchors.
- **`get_page_text` returns garbage on ad-heavy sites**: Fall back to JavaScript DOM extraction using the text-to-script ratio pattern described in Step 2.5. This works reliably on most ad-heavy sites where `get_page_text` fails.
- **No relevant content found**: Only declare "no fit" after both Phase 1 and Phase 2 come up empty. Report: "I checked all [X] articles on this site via their sitemap. None have existing anchor matches (Phase 1) or topically relevant sections for suggested placements (Phase 2). The blog covers [brief topic summary]. Skip this one."
- **Multiple good placements on one article**: Include the best 2, max 3 per article. More than that looks spammy.
- **Partner site is low quality**: Flag it — "This site looks thin/spammy. Worth considering if the link value justifies the effort."

## What NOT to Do

- Don't suggest placements where the link would feel forced or out of context
- Don't recommend linking from irrelevant articles just to get a placement
- Don't use anchors that aren't on the approved list (or very close semantic matches)
- Don't suggest more than 5 total placements per partner site — keep it focused
- Don't fabricate article content — if you can't access an article, say so
- Don't trust Google search snippets as source material — always verify on the actual page before presenting a placement
- Don't rely on Google `site:` searches as a complete inventory — they typically return only a fraction of a site's indexed pages. Always prefer sitemap or blog index crawling for discovery
- Don't declare "no fit" after Phase 1 alone — always check Phase 2 (topical opportunities) before giving up on a site
- Don't write Phase 2 suggested text that sounds like an ad or is obviously shoehorned in — it must read naturally in context
- Don't start suggested text with "Additionally," "Furthermore," "Moreover," "In addition," or other AI-sounding transitions
- Don't place links in introductions or conclusions — body paragraphs only
- Don't link to social.plus homepage, product pages, landing pages, or service pages — blogs, articles, and glossary only
- Don't process partner sites in restricted categories (crypto, casino, converter tools, etc.) — flag them and stop
- Don't skip Step 0 (Ahrefs pre-screen) on Mode A sites just because the partner "looks legit." DR + traffic + topical fit must be checked before crawling
- Don't trust DR alone as a quality signal — DR 70+ with no traffic and no topical fit is a PBN, not a publisher
- Don't use `sum_traffic_merged` as an Ahrefs `order_by` value — it's select-only and the call will fail. Use `sum_traffic`
- Don't skip the existing-backlink check (Step 0.0) on Mode B just because there's no live site to crawl — the domain is still known and the check is cheap
