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

<!-- FETCH-BLOCK:START v2 -->
Reference files live in the public `cruciate-hub/marketing-team` GitHub repo. Fetch them by shallow-cloning the repo once per session, then loading individual files with `cat`. Use this exact pattern at the start of every skill that needs reference files:

    REPO="${MT_REPO:-/tmp/cruciate-hub-marketing-team}"
    if [ ! -d "$REPO/.git" ]; then
      git clone --depth 1 --quiet https://github.com/cruciate-hub/marketing-team.git "$REPO"
    else
      git -C "$REPO" pull --ff-only --quiet
    fi

After the clone exists, read files with `cat "$REPO/<path>"`. Examples: `cat "$REPO/brain.md"`, `cat "$REPO/messaging/terminology.md"`.

The Bash tool truncates large stdout when the output exceeds the harness's token/byte cap (observed at ~50 KB in Cowork; varies by environment). When this happens the harness emits one of these signals — both mean the same thing:
- `Output too large (NkB). Full output saved to: …` followed by a short preview, OR
- `Error: result (N characters) exceeds maximum allowed tokens` with no preview, just a sidecar-file pointer.

In either case, the rest of the file is invisible to you in-call. Most files in this repo are small enough that `cat` returns them in full and you never see either signal. **If you do see either form, never proceed using the partial output as if it were the whole file** — switch to one of the patterns below.

- **Truncated markdown** (you saw either truncation signal above) — read in line-range chunks instead. First check the total line count: `wc -l "$REPO/<path>"`. Then read each chunk:

      sed -n '1,250p'     "$REPO/<path>"
      sed -n '251,500p'   "$REPO/<path>"
      sed -n '501,$p'     "$REPO/<path>"

  Each ~250-line chunk fits under the preview cap. Concatenate the chunks mentally. For files much larger than 750 lines, add more chunks at 250-line intervals until you reach the total.

  **If a chunk itself comes back as a truncated preview** (output above the harness's display cap — visible as an "Output too large" or similar marker, with the rest spilled to a file you can't see in-call), halve the chunk size and retry. For example, swap `sed -n '1,250p'` for `sed -n '1,125p'` then `sed -n '126,250p'`. Repeat until each chunk lands in full. Never proceed using a truncated chunk as if it were complete.

- **Large JSON inventories** (`website/pages-*.json`, up to 228 KB) — never `cat` raw. Process with `python3` or `jq` and emit only the fields you need:

      python3 -c "import json; d=json.load(open('$REPO/website/pages-blog.json')); print(len(d['pages']))"
      jq '.pages[].url' "$REPO/website/pages-blog.json"

  Skill helper scripts (e.g. `scripts/duplicate_check.py`) already follow this pattern.

Note: Claude Code's `Read` tool can't reach files in `$REPO` — Cowork sandboxes Read to connected directories and `/tmp` is not connected by default. Use the `cat` / `sed` / `python` patterns above.

Validate every file before using it:
- Markdown: content must start with `#`
- JSON: content must start with `{` or `[`
- HTML: content must start with `<`
- Content must be non-empty

If anything fails — clone error, missing file, empty content, or wrong format:
- Do NOT reconstruct from memory or training data.
- Do NOT fall back to WebFetch or any other tool.
- Stop immediately and respond with exactly this line:

  `Fetch failed: <path>. Please check your network connection and rerun.`
<!-- FETCH-BLOCK:END v2 -->

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

**Context:** This rule scopes to reciprocal/exchange link building — the mode this skill serves. Other inbound link-building modes (digital PR, HARO, guest posts, broken-link outreach) have different risk calculus where commercial-page targets are appropriate, but those modes don't use this skill.

- **Only blog posts (`/blog/...`) and glossary entries (`/glossary/...`).** Nothing else.
- **Off-limits page types** (never link to any of these): homepage, product pages, feature pages, SDK/UIKit pages, use case pages, industry pages, pricing, and any marketing landing page.
- The target page should not compete with the partner article's keywords.
- **Do NOT use the `marketing-team:site-intelligence` skill to pick targets.** That skill only catalogs the static marketing pages on social.plus — which are exactly the off-limits set above. It is useful for *avoiding* marketing pages, never for *picking* link targets. Pull targets from `website/pages-blog.json` and `website/pages-glossary.json` (auto-generated blog + glossary inventories). Apply the matching heuristics from `references/content-inventory.md`.

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

Use `site-explorer-crawled-pages` for URL discovery. **Do not use `pages-by-traffic` or `top-pages` for this purpose.** `pages-by-traffic` returns traffic-bucket distribution counts, not a per-page URL list (this was a long-standing skill bug). `top-pages` returns URLs but filters to pages that rank for at least one organic keyword — crawled-but-unranked pages with strong topical fit are invisible. `crawled-pages` returns Ahrefs's complete crawled URL inventory regardless of ranking status, at 1 unit per row vs 14 for top-pages. Verified on adspyder.io: the article `brand-loyalty-with-video-marketing/` has five verbatim anchor matches in body content but ranks for zero keywords; `top-pages` excludes it, `crawled-pages` returns it.

The Tier 3 query has three required filter layers:

**Layer A — Editorial path scope (`prefix` operator).** Enterprise and mid-size publishers polluted by user-generated content (forums) or marketing tracking links must be scoped to the editorial blog path at the API level. Before the main Tier 3 call, run a probe call to discover the partner's editorial blog path. Try these in order with a small probe (`limit: 5`, `prefix` operator):

1. `https://blog.{domain}/`
2. `https://www.{domain}/blog/`
3. `https://{domain}/blog/`
4. `https://{domain}/articles/`
5. `https://{domain}/resources/`
6. `https://{domain}/insights/`

Use the first candidate that returns rows. If none return rows, skip Layer A and fall back to substring-only filtering — and flag the partner for fallback Step 2 (sitemap / blog-index crawl) since the prefix probe failure usually signals a non-standard editorial path.

**Layer B — Topic filter (`isubstring` OR-clause).** Apply the keyword set against URL substrings. Expanded keyword set (added based on real-world false-negative diagnosis):

- community, engagement, mobile-app, social-network, social-feature, retention, in-app, customer-engagement, user-generated, chat-app, messaging, loyalty, ugc, social-commerce
- brand-loyalty, brand-community, brand-advocate, brand-activation, brand-affinity, brand-collab
- customer-experience, consumer-engagement, employee-engagement, fan-engagement
- referral, word-of-mouth, membership, subscription, super-user, testimonial
- loyalty-program, community-led, content-marketing, video-marketing (the last is counterintuitive but high-yield: video-marketing slugs on ad/marketing blogs routinely contain community/loyalty/UGC body content, verified on adspyder.io)

**Layer C — Tracking-link exclusion (`not isubstring "?"`).** Required on all Tier 3 calls. Verified on hubspot.com to reduce 96 noisy rows (mostly URL-tracking variants where seed keywords appear in query parameters) to 14 clean editorial URLs in one call.

**Combined call shape:**

```
target: domain.com
mode: subdomains
select: url, url_rating, title
where: {
  "and": [
    { "field": "url", "is": ["prefix", "<detected_blog_prefix>"] },
    { "or": [
      { "field": "url", "is": ["isubstring", "community"] },
      { "field": "url", "is": ["isubstring", "engagement"] },
      { "field": "url", "is": ["isubstring", "brand-loyalty"] }
      ...full expanded keyword set above...
    ]},
    { "not": { "field": "url", "is": ["isubstring", "?"] } }
  ]
}
limit: 100
protocol: both
```

**Verified `crawled-pages` constraints (do not extrapolate):**
- Hard-capped at 100 rows per call regardless of `limit` parameter. The schema claims default 1000; empirically tested at 200, 1000, 5000 — all return 100. Plan pagination accordingly.
- Results are alphabetical by URL. There is no `offset` parameter.
- Paginate via URL cursor: add `{ "field": "url", "is": ["gt", "<last_url_from_previous_response>"] }` to the AND-clause and re-run.
- Default session pagination cap: 10 calls (1,000 raw rows). Surface to the user when triggered and proceed with what was collected.

**Verified Ahrefs where-clause grammar (`doc` tool, May 2026):**
- Boolean structure: `{ "and": [...] }`, `{ "or": [...] }`, `{ "not": <expr> }`, or bare `<expr>`
- Condition operators: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `substring`, `isubstring`, `phrase_match`, `iphrase_match`, `prefix`, `suffix`
- NOT supported: `notsubstring` as an operator. Use the `not` wrapper instead.

**Light post-processing pipeline (the API filters do the heavy lifting):**
- Lowercase the host
- Force `https` when the same path exists under both protocols (the API returns `http` and `https` as separate rows)
- Strip leading `www.`
- Strip trailing `/`
- Drop URLs containing `/feed/` (WordPress RSS endpoints still surface)
- Dedupe by the normalized canonical key

**False-positive watchlist:** `community-college`, `engagement-ring`, `marketing-messaging`, `app-store-optimization`. Always verify in Step 2.5 before treating these as fits.

2. `site-explorer-linked-anchors-external` — what anchor patterns has the partner already used when linking out to other sites? **Sample size matters: require ≥10 external anchors before treating this as signal.** Below that it's noise. Use the result to tailor our anchor suggestions to what their editor actually accepts.

---

**Hand-off to Step 1:** Step 0 produces, per partner, (a) a quality verdict, (b) a vertical-fit verdict, (c) a list of candidate URLs (or escalation flag for sitemap crawl), and (d) an anchor-style profile. Pass this directly to Step 2.5 (verify on the actual page).

Escalation criteria from Tier 3 to Step 2 (sitemap / blog-index crawl):
- Canonical count after the post-processing pipeline ≥ 5 → proceed to Step 2.5
- Canonical count < 5 AND pagination not exhausted → paginate first
- Canonical count < 5 AND pagination exhausted (or session cap hit) → escalate to Step 2
- Layer A prefix probe returned no candidates → escalate to Step 2 (non-standard editorial path)

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

1. **Scan for exact anchor matches first** — Search the verified page content for approved anchor phrases from `references/anchors.md` that already exist in the text. Prioritize short anchors first (2-3 words), then check for longer ones. Verbatim matches always have priority over creative matches in step 1b below.

   **1b. Scan for creative-anchor matches (semantic-equivalent phrases).** After the verbatim pass, also identify phrases in the partner's body text that are NOT literally in `references/anchors.md` but are semantically equivalent to a listed anchor and would function as natural anchor text. Examples that qualify:
   - "community-driven platform" → maps to "community platform" anchor family
   - "app retention rate" → maps to "app retention" anchor family
   - "engaged users" → maps to "user engagement" anchor family
   - "build customer loyalty" → maps to "build brand loyalty" anchor family
   - "in-app social interactions" → maps to "social features" anchor family

   A creative anchor candidate is valid only when ALL of the following hold:
   - The phrase appears verbatim in the partner's body text (no paraphrasing — Phase 1 stays verbatim; sentence-level synthesis is Phase 2 only)
   - The phrase is 2-6 words, OR is a single word AND the proposed target is a glossary entry AND the word is the focal noun of its sentence AND the word is unambiguous in context (e.g., "communities" in a sentence about user groups is fine; "users" or "apps" are too ambiguous)
   - The phrase clearly maps to one specific topic family in `references/anchors.md`; the mapping is articulable in plain English ("X maps to Y because they describe the same concept")
   - The phrase is in a body paragraph, not intro or conclusion
   - A social.plus target page exists that directly addresses the mapped topic
   - The phrase does not cannibalize the partner article's primary ranking keywords

   Flag creative-anchor placements in the internal summary table with `[creative-anchor]`. Default fit score caps at ⭐⭐ Strong; ⭐⭐⭐ Perfect requires a verbatim-literal match from `references/anchors.md`.

2. **Check placement position** — The anchor must appear in a body paragraph, not in the introduction or conclusion of the article. Discard matches found in intros/conclusions.

3. **Extract the exact sentence** — For every match, capture the verbatim original sentence from the partner's article. Without a verified original sentence, the placement is incomplete and can't be used.

4. **Match to the best social.plus page** — For each anchor found, determine which social.plus URL is the most relevant target.
   - For definitional/generic anchors → prefer glossary pages (e.g., "user engagement" → `social.plus/glossary/user-engagement`)
   - For strategic/how-to anchors → prefer blog posts (e.g., "app engagement strategies" → `social.plus/blog/app-engagement-strategies`)
   - For SDK/API anchors → prefer technical blog posts or glossary entries
   - The target page should not compete with the partner article's keywords
   - **Target URL Rating check (when Ahrefs is available):** Run `site-explorer-url-rating-history` (or pull from `pages-by-traffic` filtered to the exact URL) on the proposed social.plus target. If URL Rating < 5, swap to a stronger target. Partners reject low-UR targets as "not a fair trade" — DR of social.plus as a domain doesn't help if the specific page has no authority.
   - **Competitor overlap check:** If Tier 2 of Step 0 flagged that the partner already links to social.plus competitors (Bettermode, Mighty Networks, Discourse, Tribe, Circle, etc.), check whether THIS specific article already contains a competitor link. If yes, either pick a different article or note the conflict to Stefan so he can decide whether to ask the partner to swap rather than insert.

5. **Capture traffic and authority signals:**
   - Record the partner article's monthly organic traffic from the Ahrefs `sum_traffic` field already pulled in Step 0 Tier 3.
   - Record the social.plus target page's URL Rating (UR). Pull from `site-explorer-url-rating-history` if not already cached. Each UR call costs ~7 Ahrefs units — budget ~21 units for a 3-placement session. Skip the UR call only if the target is a glossary entry and the partner is low-DR (< 30), where the marginal SEO weight isn't worth the call.
   - These numbers are NOT shown to the partner. They appear only in the internal summary table for Stefan's decision.

6. **Score the fit:**
   - ⭐⭐⭐ **Perfect** — Phase 1 anchor verbatim in body paragraph AND partner article traffic ≥ 50/month AND target UR ≥ 10
   - ⭐⭐ **Strong** — Phase 1 anchor verbatim OR close semantic match in body paragraph, but either partner traffic < 50 OR target UR < 10. Add a `[low-value]` flag in the summary table when partner traffic = 0 AND target UR < 5, with caveat to Stefan: "low-value link both directions — only ship if relationship maintenance is the goal."

The 50, 10, and 5 thresholds are starting heuristics, not absolutes. Adjust based on observed acceptance rates across exchanges.

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
   - Default: use one of our approved anchor texts from `references/anchors.md`

   **Creative anchors in Phase 2 are tightly gated.** Phase 2 creative anchors are allowed ONLY on articles where Phase 1 returned zero matches (both literal AND creative). When triggered, allow ONE Phase 2 creative-anchor placement per such article as a "save the article" option. The creative anchor must still satisfy the same six guardrails listed in Phase 1 step 1b (semantic-equivalent, clearly mapped, etc.) — the only difference is that the surrounding sentence is being drafted by us, not extracted verbatim. Flag in the summary as `[creative-phase2-save]`. Fit score caps at ⭐ Opportunity. Stefan reviews each one in the Step 3.5 decision gate before drafting the email. Do NOT layer Phase 2 creative anchors on articles that already have a Phase 1 placement — that compounds two layers of synthesis and hurts partner relationships over time.

3. **Match to the best social.plus page** — Same logic as Phase 1.

4. **Score as:**
   - ⭐ **Opportunity** — Topic is relevant, specific paragraph identified, text modification suggested. The partner would need to add or edit a sentence.

When a Phase 2 opportunity sits on a high-traffic article (≥ 200/month), append the note "high-traffic article — Phase 2 ask may face more editorial resistance. Write the suggested sentence to read seamlessly in their style."

---

#### Presenting Both Phases

Track Phase 1 and Phase 2 placements distinctly during matching so Stefan can see which is which:
- Phase 1 = "these anchors already exist, just add the link" (easy ask for the partner)
- Phase 2 = "these articles are topically relevant, here's where and how a link could fit" (requires partner cooperation to modify text)

The summary table in Step 5 surfaces the distinction via the Phase column. The reply email itself (Step 4) mixes Phase 1 and Phase 2 placements in a single numbered list — the `Placement:` line on Phase 1 entries vs the `Suggested text:` line on Phase 2 entries is the only marker between them.

If Phase 1 has zero results, say so explicitly when summarizing to Stefan. Never declare a site "no fit" without checking Phase 2 first. A site is only "no fit" when BOTH phases come up empty — meaning no exact matches AND no topically relevant paragraphs across any articles.

### 3.5. Decision Gate (Before Drafting the Email)

Before writing any email, show Stefan the full internal summary table from Step 5 — every viable placement with its traffic, UR, phase, and fit score. Then stop and ask which packaging he wants. Auto-drafting strips Stefan's control over how the request lands with the partner; the gate keeps him in the loop on relationship-side decisions that scoring alone can't make.

**The prompt to Stefan:**

> I found [N] viable placements above. How do you want to package the email?
>
> (a) Stacked list — propose all [N] to the partner in one email, partner picks what works
> (b) Alternatives framing — propose top 2-3 as Option 1 / Option 2 / Option 3, partner picks one or more, "happy with either"
> (c) Single ask — propose only the top-rated one, save the rest for future exchanges

**Wait for Stefan's choice before drafting.** Then map his answer to the corresponding Step 4 template:
- (a) Stacked list → Canonical Phase 1 or Phase 2 structure (numbered placements; mix Phase 1 + Phase 2 entries in the same list as needed)
- (b) Alternatives framing → "Email structure when offering alternatives" (Option 1 / Option 2 / Option 3)
- (c) Single ask → Same canonical structure, but with only the top-rated placement included

See Edge Cases for behavior when only one placement is viable, or when more than 5 are viable.

### 4. Draft the Reply Email

Write a casual-but-professional reply. The tone is direct, friendly, no corporate fluff — like texting a business contact. Every line in every placement block sits flush-left so the email renders cleanly in email, LinkedIn, Slack, and any chat box where markdown doesn't render — indented sub-fields wrap weirdly when the surface strips formatting.

**Canonical Phase 1 email structure (anchor already in body — partner just adds the link):**


```
Hi [Name],

Thanks for sharing. I reviewed [the blog / the docs / your articles] and found [N] good placement[s], which I'd like to request with you:

1. Article: [Article Title]
URL: [article URL]

Add link from: [article URL]
Add link to: [social.plus target URL]
Anchor: [anchor text]
Placement: [section name + verbatim sentence]

[Repeat the numbered block for each additional placement, with a blank line between blocks.]

Please let me know which work for you, and what we can do for you in return.

Cheers,
Stefan
```



**Canonical Phase 2 email structure (partner adds or modifies a sentence to host the link):**


```
Hi [Name],

Thanks for sharing. I reviewed [the blog / the docs / your articles] and found [N] good placement[s], which I'd like to request with you:

1. Article: [Article Title]
URL: [article URL]

Add link from: [article URL]
Add link to: [social.plus target URL]
Anchor: [anchor text]
Suggested text: [the sentence the partner adds or modifies]

[Repeat the numbered block for each additional placement, with a blank line between blocks.]

Please let me know which work for you, and what we can do for you in return.

Cheers,
Stefan
```



**Email structure when offering alternatives (partner has limited capacity or relationship calls for flexibility):**


```
Hi [Name if known, otherwise skip],

Thanks for sharing these. I went through [the content / your articles] and found [N] solid placement opportunities on [partner site] — we're happy with either one, or both if it works for you.

**[Partner Site Name/Domain]**

Option 1
Article: [Article Title]
URL: [article URL]

Add link from: [article URL]
Add link to: [social.plus target URL]
Anchor: [anchor text]
Placement: [section name + verbatim sentence]

Option 2
Article: [Article Title]
URL: [article URL]

Add link from: [article URL]
Add link to: [social.plus target URL]
Anchor: [anchor text]
Placement: [section name + verbatim sentence]

Please let me know which one you'd like to go with, or if both work, and what we can do for you in return.

Cheers,
Stefan
```



**Format rules:**
- Every line in every placement block is flush-left — no indentation under the numbered/Option line. Indented sub-fields wrap weirdly in LinkedIn, Slack, and most chat boxes where markdown doesn't render
- One blank line between each numbered placement block
- Phase 1 placements use `Placement:` (section name + verbatim sentence from the partner's article). Phase 2 placements use `Suggested text:` (the sentence the partner adds or modifies)
- Mix Phase 1 and Phase 2 blocks in the same numbered list when both exist — the `Placement:` vs `Suggested text:` line is the only marker between them
- Match singular/plural to the count: "one good placement" / "two good placements"
- Always close with "Please let me know which work for you, and what we can do for you in return." Link exchanges are reciprocal — the partner expects us to ask back, so never drop this line
- If both Phase 1 and Phase 2 came up empty, do NOT use the request template. Replace the body with one sentence explaining why the site isn't a fit, then sign off. Don't fabricate placements to fill space

**Example — single Phase 1 placement:**


```
Hi Muhammad,

Thanks for sharing. I reviewed the blog and found one good placement, which I'd like to request with you:

1. Article: The Role of Customer Engagement in Digital Growth
URL: https://example.com/blog/customer-engagement-digital-growth

Add link from: https://example.com/blog/customer-engagement-digital-growth
Add link to: https://www.social.plus/blog/effective-customer-engagement-strategies-with-case-studies
Anchor: customer engagement
Placement: "Building Long-Term Loyalty" section — the sentence "Brands that invest in customer engagement see significantly higher retention."

Please let me know which work for you, and what we can do for you in return.

Cheers,
Stefan
```



**Example — single Phase 2 placement (`Suggested text:` replaces `Placement:`):**


```
Hi Alex,

Thanks for sharing. I reviewed the articles and found one good placement, which I'd like to request with you:

1. Article: AI in Ecommerce: A Complete Guide
URL: https://example.com/blog/ai-in-ecommerce-a-complete-guide

Add link from: https://example.com/blog/ai-in-ecommerce-a-complete-guide
Add link to: https://www.social.plus/blog/effective-customer-engagement-strategies-with-case-studies
Anchor: customer engagement strategies
Suggested text: Brands that invest in customer engagement strategies — like in-app communities and personalized social experiences — see significantly higher retention alongside their AI-driven optimizations.

Please let me know which work for you, and what we can do for you in return.

Cheers,
Stefan
```

### 5. Present Results

After the draft email, provide a summary table for Stefan's reference:

| Partner Article | Partner Traffic | Anchor | social.plus Target | Target UR | Phase | Fit Score |
|----------------|----------------|--------|-------------------|-----------|-------|-----------|
| [title] | [monthly traffic] | [anchor] | [URL] | [UR] | 1 or 2 | ⭐⭐⭐/⭐⭐/⭐ |

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
- **Any reference file missing**: The skill depends on four files (two local .md, two remote .json). If any are missing, surface this to Stefan immediately — without them, target picking and anchor matching are guesswork. Don't try to substitute with `marketing-team:site-intelligence` (wrong scope — marketing pages only).
- **Site blocks crawling / WebFetch blocked**: WebFetch is often blocked by the egress proxy. Use Chrome browser tools instead — `navigate` to the URL, then `get_page_text` or JavaScript DOM extraction (see Step 2.5) to read the actual content and verify anchors.
- **`get_page_text` returns garbage on ad-heavy sites**: Fall back to JavaScript DOM extraction using the text-to-script ratio pattern described in Step 2.5. This works reliably on most ad-heavy sites where `get_page_text` fails.
- **No relevant content found**: Only declare "no fit" after both Phase 1 and Phase 2 come up empty. Report: "I checked all [X] articles on this site via their sitemap. None have existing anchor matches (Phase 1) or topically relevant sections for suggested placements (Phase 2). The blog covers [brief topic summary]. Skip this one."
- **Multiple good placements on one article**: Include the best 2, max 3 per article. More than that looks spammy.
- **Single viable placement**: Skip the decision gate (Step 3.5) and proceed directly to Step 4 with the single-ask format. There's nothing for Stefan to choose between.
- **More than 5 placements**: Default to recommending option (b) alternatives framing on the top 3 — proposing 6+ placements in one email reads as spam.
- **Partner site is low quality**: Flag it — "This site looks thin/spammy. Worth considering if the link value justifies the effort."
- **Enterprise publishers return query-string variants**: Sites like HubSpot, Salesforce, Adobe, Atlassian crawl the same canonical article at dozens of tracking-link URL variants (e.g., `?hubs_content=...`). Always include `{ "not": { "field": "url", "is": ["isubstring", "?"] } }` in the Tier 3 `where` clause to exclude these at the API level. Verified on hubspot.com: dropped 96 raw rows to 14 clean editorial URLs.
- **Partner sites with user-generated forums**: Some partners host both an editorial blog AND a user-generated community forum (e.g., intercom.com has `community.intercom.com` alongside `blog.intercom.com`). Substring filters pollute the result with forum threads we can't request placements in. The Layer A `prefix` operator scoped to the editorial blog path excludes forum content at the API level.
- **`crawled-pages` 100-row cap**: The endpoint is hard-capped at 100 rows per call regardless of the `limit` parameter (tested at 200, 1000, 5000). The schema's default-1000 claim is misleading. Plan pagination accordingly.
- **Ahrefs where-clause supports `not` wrapper but not `notsubstring` operator**: The grammar is `{ "not": { "field": "...", "is": [op, value] } }`. Trying `notsubstring` as an operator returns "bad where: invalid JSON syntax". Verified condition operators: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `substring`, `isubstring`, `phrase_match`, `iphrase_match`, `prefix`, `suffix`.
- **Layer A prefix probe returns no candidates**: If none of the standard editorial-blog prefix patterns return rows, escalate immediately to Step 2 (sitemap / blog-index crawl). The partner has a non-standard path that Tier 3 substring-only fallback won't handle cleanly.
- **Phase 1 creative anchor caps fit score at ⭐⭐**: Verbatim-literal anchor matches from `references/anchors.md` are the only path to ⭐⭐⭐ Perfect. Creative semantic-equivalent matches max out at ⭐⭐ Strong. This protects the relationship channel against AI over-reach in anchor identification.
- **Phase 2 creative anchor is a last-resort save**: Allowed only when Phase 1 returned zero matches on the article. Capped at one creative-anchor placement per zero-match article. Flagged as `[creative-phase2-save]` in the summary table. Stefan reviews before email is drafted. Do not layer creative anchors onto articles that already have a Phase 1 placement.
- **Single-word anchors only for glossary targets**: A single-word anchor (e.g., "communities") is allowed when ALL of: the target is a glossary entry, the word reads as the focal noun in context, and the word is unambiguous. Single-word anchors pointing to blog posts remain disallowed because blog targets are strategic/long-form and a one-word link reads forced.

## What NOT to Do

- Don't suggest placements where the link would feel forced or out of context
- Don't recommend linking from irrelevant articles just to get a placement
- Don't invent anchor phrases that don't appear verbatim in the partner's body text. Phase 1 creative anchors must be in the text already; Phase 2 creative anchors require all six guardrails from Phase 1 step 1b and are gated to zero-match articles only.
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
- Don't propose a placement without checking both partner-article traffic and social.plus target URL Rating. The fit score is meaningless without these two numbers
- Don't auto-draft the email when multiple viable placements exist. Always show the summary table first and let Stefan choose the packaging
- Don't use `sum_traffic_merged` as an Ahrefs `order_by` value — it's select-only and the call will fail. Use `sum_traffic`
- Don't skip the existing-backlink check (Step 0.0) on Mode B just because there's no live site to crawl — the domain is still known and the check is cheap
