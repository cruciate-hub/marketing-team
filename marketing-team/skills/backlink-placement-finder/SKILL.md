---
name: backlink-placement-finder
description: >
  Find contextually relevant backlink placement opportunities on partner websites for social.plus.
  Use this skill when a partner sends website URLs and the user needs to identify where social.plus
  can be naturally linked from their blog articles. Triggers on phrases like "find backlink placements",
  "check this site for link opportunities", "where can we place links on this site", "find anchors on
  this website", "backlink opportunities", or when the user pastes one or more partner website URLs
  and asks for link placement suggestions. Also trigger when the user mentions partner websites,
  link exchanges, or outbound link prospecting for social.plus. Defaults to editorial reading mode
  for ≤5 candidate articles per partner — read articles end-to-end, generate angles editorially,
  then validate against lists as constraints rather than lookups.
---

# Backlink Placement Finder for social.plus

You are a link building specialist for social.plus. Your job: take partner website URLs, crawl their blog content, and find the best places where a link to social.plus would fit naturally — then draft a professional reply email requesting those specific placements.

## How to fetch reference files

<!-- FETCH-BLOCK:START v2 -->
Reference files live in the public `cruciate-hub/marketing-team` GitHub repo. Fetch them by shallow-cloning the repo once per session, then loading individual files with `cat`. Use this exact pattern at the start of every skill that needs reference files:

    REPO="${MT_REPO:-/tmp/cruciate-hub-marketing-team}"
    REMOTE="https://github.com/cruciate-hub/marketing-team.git"
    # Create the clone only when the path is absent. Never delete an existing
    # directory: it may be a working checkout holding un-pushed local commits.
    if [ ! -e "$REPO" ]; then
      git clone --depth 1 --quiet "$REMOTE" "$REPO" || true
    elif git -C "$REPO" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      # Refresh, but do NOT ignore a failed pull. Silently serving stale
      # content is the exact bug this block exists to prevent.
      git -C "$REPO" pull --ff-only --quiet 2>/dev/null \
        || echo "Note: could not refresh $REPO; verifying existing content below." >&2
    fi
    # Mechanical integrity gate. Do not skip. Probes core files across several
    # top-level dirs so a missing, corrupt, or partial clone stops the skill
    # here instead of letting it read incomplete content and draw wrong conclusions.
    miss=""
    for f in brain.md messaging/brain.md messaging/terminology.md messaging/tone.md design-system/brain.md; do
      [ -s "$REPO/$f" ] || miss="$miss $f"
    done
    if ! git -C "$REPO" rev-parse HEAD >/dev/null 2>&1 || [ -n "$miss" ]; then
      echo "Fetch failed: clone at $REPO is unreachable or incomplete.${miss:+ Absent files:$miss}" >&2
      echo "Check your network. If the clone is corrupt and holds no local work, run  rm -rf \"$REPO\"  then re-run." >&2
      echo "(If \$MT_REPO points at your own checkout, rescue its changes first; this never auto-deletes it.)" >&2
      exit 1
    fi

After the clone exists, read files with `cat "$REPO/<path>"`. Examples: `cat "$REPO/brain.md"`, `cat "$REPO/messaging/terminology.md"`.

The integrity gate above fails loud rather than serving partial content, and it never deletes `$REPO` (it can hold un-pushed local work). To make skills read your own local edits, point `MT_REPO` at your working checkout before running them.

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

**Scope of the fetch block above — read before cloning.** That block is generic boilerplate shared verbatim across many skills (kept in sync by `scripts/sync-fetch-blocks.py`), so its opening line — "Reference files live in the public repo" — is true for THIS skill only of the two remote JSON inventories: `website/pages-blog.json` and `website/pages-glossary.json`. The three `references/*.md` files this skill uses (`anchors.md`, `content-inventory.md`, `creative-anchor-patterns.md`) are LOCAL to this skill folder — read them directly with `Read`/`cat` from `skills/backlink-placement-finder/references/`. There is no `$REPO/references/` directory; do not clone or look there for them. (Fetches FROM partner websites are a separate concern — use the live-page-read tools described in Step 2.5 — Vercel agent-browser first, then Claude in Chrome — or WebFetch.)

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
- **Vary anchors.** Never propose the same anchor text twice in one batch/email, and check every proposed anchor against the live social.plus anchor profile before finalizing (see "Anchor Diversity Check" in Step 3). Repeated anchors read as a link-building footprint on both sides of the exchange.
- **Prefer the lowest-risk anchor type that fits, and vary type across the batch.** Over-optimization risk runs low→high: branded · naked-URL · generic/navigational · partial-match · exact-match commercial — with stat-citation anchors (citing a social.plus number) the lowest-risk editorial type of all. Default toward stat-citation, partial-match and contextual anchors; treat an exact-match commercial keyword as the thing to justify, not the default, and use at most one per batch. Do NOT randomize or rotate anchors to fake variety — real variation comes from each partner's own sentences and from varying type per placement; synthetic rotation is itself a footprint. (See the Anchor Diversity Check in Step 3.)

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
- Do not run Tier 1/2/3 calls for that partner (no wasted Ahrefs units, no fresh placement asks)
- Report to Stefan: "We already have a backlink from `partner.com` (first seen YYYY-MM-DD via referring page X). Skipping Tier 1-3."
- Still include the partner in the email output with the existing-backlink callout: one paragraph noting the existing link — partner URL, social.plus URL, anchor, and first-seen date. In a multi-domain request this goes into the consolidated email (see Step 4, "Consolidated multi-site email"). In a single-domain request, draft a short standalone reply: greeting → existing-backlink paragraph → lighter close ("Happy to keep an eye out on future rounds.") → sign-off

**Edge case:** If the existing backlink is on a marketing/footer/template page rather than an editorial article (e.g., "powered by" links, generic resource lists), it may still be worth pursuing an *editorial* placement on a different page of the same partner. Surface this nuance to Stefan rather than auto-declining when the existing link looks non-editorial.

**Why this is Step 0.0:** It's the cheapest possible filter (1 cached call covers the entire batch) and it eliminates the most wasted work. Run it first, always, regardless of mode.

---

### 0. Quality & Vertical Check via Ahrefs (PREFERRED for Mode A)

**This step is the new default for live partner sites.** It exists because (a) WebFetch gets blocked by the egress proxy on most partner domains, (b) sitemap crawling wastes time on sites with no topical fit, and (c) high-DR-but-spammy partners (PBNs, content farms, celebrity-gossip blogs with inflated DR) leak through without a quality gate.

Skip this step ONLY in Mode B (Google Doc drafts — no live site to evaluate). (Note: Step 0.0 — the existing backlink check — still applies to Mode B and must have already run by this point.)

**What Step 0 is NOT:** Step 0 is a *narrowing* tool, not a *bounding* tool. Ahrefs's index is incomplete — small blogs often have 60-80% of pages missing from `top-pages` and `pages-by-traffic`. **Never declare "no fit" from Ahrefs results alone.** When Ahrefs returns sparse or empty results for a partner that *looks* legit by other signals, escalate to a sitemap/browser pass (Step 2) before declining.

**Standardized parameters across all Ahrefs calls in this skill:**
- `mode: subdomains` (catches `blog.`, `www.`, etc. — never use `domain` mode for discovery)
- `country: null` or omit (worldwide — defaulting to `us` undervalues UK/EU/APAC partners)
- `order_by: sum_traffic:desc` (NEVER `sum_traffic_merged` — that's select-only and the API rejects it as an order column)
- `protocol: both`

**Tiered call sequence — cheap calls first, expensive only on survivors.** Quota is real. Check `subscription-info-limits-and-usage` once at session start to confirm headroom for the planned batch size.

---

**Tier 1 — Cheap batch screen (run for every partner in one parallel block)**

`site-explorer-metrics` per domain → returns DR, organic traffic, refdomains in one call. Try `batch-analysis` first if the partner list is ≥5 domains; fall back to parallel `metrics` calls if `batch-analysis` schema doesn't fit our needs.

Valid `batch-analysis` select fields include: `domain_rating`, `org_traffic`, `org_keywords`, `refdomains`, `refdomains_dofollow`, `backlinks`, `linked_domains`, `linked_domains_dofollow`, `url_rating`, `ahrefs_rank`. There is no `linked_root_domains` field — use `linked_domains`.

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
- Unwrap Google/Gmail redirect wrappers: if the URL host is a `google.<tld>` and the path is `/url`, replace the URL with the decoded value of its `q` (or `url`) query parameter. Then continue with the steps below (this is what upgrades the unwrapped `http://` target to `https` and canonicalizes it).
- Lowercase the host
- Force `https` when the same path exists under both protocols (the API returns `http` and `https` as separate rows)
- Strip leading `www.`
- Strip trailing `/`
- Drop URLs containing `/feed/` (WordPress RSS endpoints still surface)
- Dedupe by the normalized canonical key

Reference implementation for the unwrap step (use when URLs are extracted via Chrome JS rather than returned by the Ahrefs API):

```js
function unwrapGoogleRedirect(u) {
  try {
    const url = new URL(u);
    if (/(^|\.)google\.[a-z.]+$/.test(url.hostname) && url.pathname === "/url") {
      const real = url.searchParams.get("q") || url.searchParams.get("url");
      if (real) return decodeURIComponent(real);
    }
  } catch (e) {}
  return u;
}
```

**False-positive watchlist:** `community-college`, `engagement-ring`, `marketing-messaging`, `app-store-optimization`. Always verify in Step 2.5 before treating these as fits.

**Publisher/magazine sites — bypass the substring filter.** For known publisher/magazine sites (descriptive title slugs, a `/magazine`, `/blog`, or `/news` index), the URL-substring topic filter under-recalls badly: article slugs are descriptive titles that contain none of the topic keywords, so `crawled-pages` returns zero rows even when the editorial fit is strong. Go straight to a browser index scan of the editorial section (Step 2.5 tool priority — Vercel agent-browser, then Claude in Chrome) and read the article titles, rather than trusting `crawled-pages`. Never declare "no fit" off an empty `crawled-pages` result — this is the same rule as Step 0's "never declare no-fit from Ahrefs alone."

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

**Mode A — Live partner URLs.** The user pastes one or more website URLs. Before using any partner URL, unwrap Google/Gmail redirect wrappers (`google.<tld>/url?q=REAL_URL&source=gmail...`) back to the real destination, then canonicalize. This applies whether URLs were pasted from a Gmail message or read via the Gmail API. These could be a homepage (find their blog), a blog index (crawl for articles), or direct article URLs (evaluate directly). **Run Step 0 first** (Ahrefs DR/quality/topical pre-screen), then proceed to Step 2.5 directly using the candidate URLs Ahrefs returned. Only fall back to Step 2 (sitemap crawl) if Ahrefs has no data on the domain.

**Mode B — Google Doc drafts.** The partner has sent Stefan unpublished article drafts in Google Docs (often titled `[For Link Partners] ...`). Before using any partner URL (the publication-target domain, or any link pasted alongside the docs), unwrap Google/Gmail redirect wrappers (`google.<tld>/url?q=REAL_URL&source=gmail...`) back to the real destination, then canonicalize. This applies whether URLs were pasted from a Gmail message or read via the Gmail API. Each doc IS the partner article — there is no site to crawl. Skip Step 2 (sitemap crawl) and proceed to Step 3 (matching) — but Step 0.0 (existing backlink check) still applies and must run first. Use `mcp__c1fc4002-...__google_drive_fetch` to read each doc by ID. **Be careful with doc-ID-to-title mapping when fetching multiple docs in one batch** — when reporting back, double-check that each placement is attributed to the correct doc URL. Mixing them up has happened before and destroys credibility with the partner.

**Before proceeding (both modes):** Check the partner site/domain against the Partner Site Restrictions above. If the partner falls into a restricted category, stop immediately and tell Stefan: "This site falls under [category] — not eligible per our guidelines."

### 2. Discover Articles via Sitemap (Fallback Method)

**Use this step only when Step 0 (Ahrefs) returned no usable data** — e.g., a brand-new domain Ahrefs hasn't indexed, or when the user explicitly asks for an exhaustive crawl beyond what Ahrefs surfaces. For ~95% of partner sites, Step 0 already gave you the candidate URL list and you can skip straight to Step 2.5.

The sitemap gives the complete URL inventory in one request — no pagination guessing, no relying on Google's incomplete index. **Be aware: WebFetch is frequently blocked by the egress proxy for partner domains.** When that happens, use the live-page-read browser tools (Step 2.5 priority — Vercel agent-browser first, then Claude in Chrome) with `navigate` + JavaScript to fetch the sitemap instead.

**Step 2a — Fetch the sitemap:**
1. Try `https://domain.com/sitemap.xml` first (via the Step 2.5 browser tools' `navigate`, or WebFetch)
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
1. **Try browser-based blog index crawling** (Step 2.5 tool priority — Vercel agent-browser, then Claude in Chrome): Navigate to the blog index page, use JavaScript to extract article links and discover the pagination structure (check for path-based `/page-2`, query-based `?page=2`, or JS-loaded pagination). Crawl all pages to build the full article inventory, then apply the same slug triage above.
2. **Last resort — WebSearch discovery**: Use `site:domain.com` queries with triage keywords to find candidate articles. **Be aware this is incomplete** — Google typically returns only a fraction of indexed pages. Treat this as a partial inventory, not a complete one. Run at least 5 varied queries before concluding "no fit."

### 2.5. Verify on the Actual Page (MANDATORY)

**Never present a placement without verifying the anchor text exists on the actual page.** Google search snippets fabricate, paraphrase, and hallucinate content that doesn't appear on the real page. This step is non-negotiable.

For every candidate article identified in Step 2:

1. **Open the article.** **Canonical live-page-read tool priority — applies everywhere this skill reads a partner page (the Step 0 magazine/index scans, the Step 2 sitemap and blog-index crawls, the Edge Cases, and here):** use the Vercel agent-browser if connected (primary); fall back to Claude in Chrome; use WebFetch only if both are unavailable. If the primary is unavailable, note that to the user rather than silently falling through. Navigate to the URL, then `get_page_text` (or the agent-browser equivalent) to extract the full article content. After navigating, if `get_page_text` returns empty or a stub, retry once after the page settles, then fall back to the JS DOM-extraction snippet in step 2 below.

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

6. If both live-page-read browser tools (Vercel agent-browser and Claude in Chrome) are unavailable, use WebFetch as a fallback. If WebFetch is also blocked, let Stefan know and suggest he share the article content directly.

This verification step is what separates a usable placement from a false positive. Without it, you risk sending Stefan placements that reference text the partner can't find in their own article — which destroys credibility.

### 3. Match Against Anchors & Inventory (Two-Phase Approach)

**Locating the reference files:** This skill uses five files — three local markdown files and two remote JSON files:

Local (in this skill's `references/` folder):
- `references/anchors.md` — the approved anchor text list
- `references/content-inventory.md` — the matching heuristics (how to pick a target for a given anchor)
- `references/creative-anchor-patterns.md` — confirmed Type B and Type C phrase-to-family mappings

Remote (on GitHub, auto-generated by the Cloudflare Worker on every CMS publish — fetch per the canonical fetch block at the top of this file):
- `website/pages-blog.json` — full blog inventory
- `website/pages-glossary.json` — full glossary inventory

If any of the five files is missing, surface the failure to Stefan immediately — do not guess at anchor lists or content inventory. The skill is unusable without these references.

**Fetch order:**
1. `references/anchors.md` — approved anchor list
2. `references/content-inventory.md` — matching heuristics
3. `references/creative-anchor-patterns.md` — confirmed Type B and Type C phrase mappings
4. `website/pages-blog.json` — blog inventory data
5. `website/pages-glossary.json` — glossary inventory data

**Important: prioritize anchor searches by likelihood of appearing in natural text.** Search for short, common anchors first (2-3 words like "user engagement", "community app", "social features"), then check for longer phrases only on articles that already matched a short anchor. Long-tail anchors like "how to increase mobile app user engagement" almost never appear verbatim in someone else's content — searching for them first wastes time.

---

#### Anchor Diversity Check (run once per session, before finalizing any anchor)

Added 2026-06-10 after Stefan flagged that batches were reusing the same few anchors. Anchor repetition is a double problem: over-optimization risk on the social.plus side and template-smell on the partner side. Discovery (Phase 1/2 scanning) is unaffected — this check governs which anchor you *finalize* when a sentence offers more than one option.

1. **Pull the live anchor profile once per session:** `site-explorer-anchors` with `target: social.plus`, `mode: subdomains`, `history: live`, `select: anchor,refdomains,links_to_target,dofollow_links,is_spam`, `order_by: refdomains:desc`, `limit: 150`. Costs ~8 units/row (~1,200 units) — cache the result for the whole session. Ignore rows where `is_spam` = true (this flags spammy linking domains regardless of anchor text — covers Telegram/SEO-service anchors but also legitimate-looking phrases like "Customer engagement" that were syndicated across spam networks) and brand/URL/bare anchors; classify only non-spam editorial phrase anchors.
2. **Classify by refdomains:** ≥10 = saturated (avoid), 5–9 = caution (use only when the placement is clearly the best option), 1–4 = fine, 0 = preferred.
3. **Reference snapshot (2026-06-15 — re-pull, don't trust this list blindly):** "Customer engagement" (21 refdomains, all dofollow) and "greater user engagement and loyalty" (24 refdomains, all dofollow) are both now flagged `is_spam` by Ahrefs — syndication/scrape footprints of spammy linking domains, NOT output of this skill. Exclude them from saturation counting. The genuinely-editorial saturated commercial anchors at ≥10 refdomains are only: "social media app development" (11, dofollow, non-spam) and "Community features" (11). "social features" (10) sits at the threshold. "community based marketing" (~6 confirmed, possibly more across casing variants) and "User-Generated Content" (8) follow in the caution band (5–9). The profile head is dominated by branded/URL anchors (healthy: "social.plus" 57, "Social+" 16, "Social Plus" 21 refdomains) and by PBN/Telegram link-service spam (a disavow concern outside this skill). Stat-citation anchors are growing organically: "76% of internet users" (9), "84% of consumers" (7), "Approximately 70% of apps doubled user engagement" (5) — confirming the default-to-stat-citation strategy is producing natural-looking editorial links. Fresh (zero presence) still includes the whole retention family, the app-engagement family, app stickiness, activity/news feed, app/community monetization, in-app chat/messaging, real-time messaging, social commerce, live streaming, community platform, in-app community, brand advocate.
4. **De-dupe within the batch:** never the same anchor twice in one email. If two articles host the same head term, vary the phrasing per article ("customer loyalty" on one, "building customer loyalty" on the other) — each variant must still appear verbatim on its page.
5. **Prefer verbatim on-page variants over saturated head terms.** The same sentence often contains a fresher 2-4 word variant: "building customer loyalty" instead of "customer loyalty", "higher engagement rates" instead of "engagement rates", "community platform" instead of "community engagement". The variant must still pass all six Phase 1 guardrails (it usually lands as Type B, capped ⭐⭐).
6. **Placement quality still wins.** If the only fresh-anchor alternative is a worse placement (forced context, table cell, intro position), keep the better placement with the lightly-used anchor and note the tradeoff.
7. **Flag reuse in the Step 5 summary table:** append `[anchor-reuse: N refdomains]` to any proposed anchor with ≥5 refdomains in the live profile so Stefan sees it at a glance.
8. **Most natural pattern in the live profile: stat-citation anchors** ("84% of consumers", "5% rise in retention", "Approximately 70% of apps doubled user engagement") pointing at the stat-blog series — writers cite numbers without being pushed. For Phase 2 suggested sentences, citing a social.plus statistic with the stat phrase as the anchor is the most editorial-feeling ask available.
9. **Classify by anchor type and vary it across the batch.** Six types, lowest→highest over-optimization risk: **branded** (brand name/variant) · **naked-URL** (a raw social.plus URL) · **generic/navigational** ("here", "this guide", "source") · **partial-match** (descriptive multi-word phrase) · **exact-match commercial** (a commercial keyword straight from `anchors.md`) · and **stat-citation** (cites a social.plus number), the lowest-risk editorial type of all. Across a multi-placement batch, at most ONE placement may use an exact-match commercial anchor; spread the rest across the other types so a single email never reads as a keyword-anchor template. This governs only the 2–3 anchors we actually propose — it is not a profile-wide quota, and the skill emits far too few anchors to "rebalance" a profile dominated by spam and syndication it never created.
10. **No synthetic rotation, no competitor benchmarking.** Real variation comes from each partner's own sentences and from varying type (step 9) — never from rotating or randomizing anchors to look natural; a rotation pattern is itself a footprint. We also deliberately do NOT compute our exact-match share against competitors (Bettermode, Mighty Networks, Circle): their live anchor profiles are dominated by spam, UGC member-URLs, and "powered-by" widget links, so they yield no valid "natural" target to drift toward — verified by direct Ahrefs pulls.
11. **Flag freshness in the Step 5 summary table:** append `[fresh-anchor]` to any Type B or Type C placement whose anchor phrase has zero presence in the cached live anchor profile (step 1 above). This is the positive counterpart to `[anchor-reuse: N refdomains]`: Stefan sees at a glance that the placement is both creative AND adds anchor-profile diversity — a positive signal in addition to the ⭐⭐ score. Determined by verbatim cross-check against the cached profile, not by manual recall. Do not apply to Type A literal matches — those are by definition on the curated anchor list and the flag would be misleading.

---

#### Phase 1 — Find Existing Anchor Matches

For each partner article opened in Step 2.5, scan body paragraphs for any of three Phase 1 candidate types. All three are first-class and use the same six guardrails. The only difference is the fit-score ceiling.

0. **Editorial reading of survivor articles (default mode at this stage).** By the time you reach Phase 1, the tier funnel (Step 0 Ahrefs pre-screen → Step 2 sitemap → Step 2.5 verification) has already narrowed the universe — typically ≤5 candidate articles per surviving partner. At that scale, reading every article end-to-end is cheap and the bottleneck stops being throughput. It becomes creative judgment. Switch out of list-matching mode entirely.

   - Read each survivor article end-to-end, in order — not paragraph-by-paragraph against a checklist.
   - For each article, ask the editorial question: *"If I were the editor of this piece and a reader hit this paragraph, where would a link to social.plus genuinely improve the reading experience? What concept is the reader reaching toward that social.plus has content on?"*
   - Surface 5-10 candidate angles per article. Be deliberately wider than feels necessary; the point of editorial mode is to generate options the mechanical scan would never propose. The "social sellers" placement on Pineable (2026-06-19) was found this way — by reading the AI-photo-tools article end-to-end and noticing that the phrase landed squarely in social.plus's live-commerce / social-commerce territory, despite appearing nowhere in `anchors.md` or the pattern cache. A list-scan, no matter how big the list, would not have surfaced it.
   - **Lists are FENCES applied AFTER editorial thinking, not LOOKUPS consulted BEFORE.** `references/anchors.md`, `references/creative-anchor-patterns.md`, and the blog/glossary inventory exist to *validate* candidates, not to *generate* them. Generate from the article; validate against the lists.
   - **Procedural enforcement — write candidates BEFORE consulting any list.** Write down all 5-10 candidate angles per article BEFORE opening `references/anchors.md`, `references/creative-anchor-patterns.md`, or the blog/glossary inventory. Consulting any list during the read contaminates editorial mode and reintroduces the lookup reflex. Open the lists ONLY during the validation pass in step 1 below.
   - **Stop-check before listing candidates — resist saturated-head defaults.** If your top angles include "brand loyalty", "customer engagement", "online community", "community features", "social features", or "user-generated content" as the standalone head (with no fresher co-occurring angle alongside), you skipped editorial mode. Redo the read. These six are the most saturated commercial heads in the live anchor profile (per the Anchor Diversity Check below), and reaching for them first is the lookup-reflex this mode is built to prevent. Fresh families live in `references/anchors.md` and the worked-example library below.

   **Worked-example library — fresh angles editorial mode surfaces (and lookup mode misses):**

   | Phrase found in partner body | Type | Maps to |
   |---|---|---|
   | "social sellers" | B | live commerce / social commerce — `/blog/from-viewers-to-belonging-why-community-is-the-engine-of-live-commerce` (2026-06-19 Pineable find) |
   | "brand voice" | B | brand-voice / brand-community topic (route b) |
   | "fan engagement" | B | fan-engagement / community-led growth topic (route b) |
   | "super-fans" | B | brand-advocate family (route a; fresh — zero-presence head) |
   | "audience interaction" | B | community-engagement family (fresher route-a substitute for the saturated "community engagement" head) |
   | "creator commerce" | B | live-commerce / social-commerce topic (route b) |
   | "in-app social" | B | social-features family OR in-app community content (multi-family — article context resolves) |
   | "community-led selling" | B | live-commerce / community-driven commerce topic (route b) |

   Each row is a phrase that appeared (or could appear) verbatim in a partner paragraph and maps to social.plus content via route (a) [an anchor family in `anchors.md`] or route (b) [an inventory topic in `pages-blog.json` / `pages-glossary.json`]. This library lives inline so agents see priming examples without a separate fetch; the full confirmed-pattern cache is in `references/creative-anchor-patterns.md` and should be appended when new finds land. **Treat this library as priming, not as a closed list — the whole point of editorial mode is that genuinely fresh angles arise from each individual read.** If you find yourself only proposing phrases from this table or from `creative-anchor-patterns.md`, you reverted to lookup mode.

   **What editorial mode does NOT relax — the plot.** Editorial mode changes how candidates are *generated*, not what makes them *valid*. Every candidate must still pass the six guardrails in step 1 (verbatim on page, articulable mapping to an anchor family OR an inventory topic, body paragraph not intro/conclusion, real target exists, no cannibalization, length rules). The Anchor Diversity Check (step 3 below) still applies — saturated head terms still cap at ⭐⭐ and yield to fresher co-located variants. The fit-score ceilings still hold (Type A ⭐⭐⭐, Type B/C ⭐⭐). The per-article cap is still 2-3 placements; the per-partner cap is still ≤5. The lists were never the problem — using them as discovery sources was. They remain authoritative as constraints.

   **Long-tail fallback — semantic-territory scan (only when >5 candidate articles per partner).** When the tier funnel returned more than 5 candidate articles for a partner (rare — usually means a thin or noisy Tier 3 filter on a large blog), reading every article end-to-end is impractical and editorial mode does not scale. Fall back to the cheaper mechanism: for each candidate article, list 3-5 candidate phrases per paragraph that could semantically map to ANY anchor family in `references/anchors.md` OR ANY topic in `website/pages-blog.json` / `website/pages-glossary.json` (match against `metaTitle`, `metaDescription`, or `content` heading hierarchy). Validate each candidate against the six guardrails in step 1. This is the 13.20 mechanism, retained so the skill still scales when reading every survivor isn't viable. Editorial mode remains the default whenever the candidate count makes it possible.

1. **Identify Phase 1 candidates.** Three candidate types qualify. Treat B and C exactly like A during discovery. Under-flagging B and C is the most common reason this skill leaves strong placements on the table; over-flagging is recoverable in the Step 3.5 decision gate, under-flagging is not.

   **Type A: Literal anchor match.** The exact phrase from `references/anchors.md` appears verbatim in the partner's body text.

   **Type B: Creative anchor match.** A 2-6 word phrase appears verbatim in the partner's body text, is NOT literally in `references/anchors.md`, and is semantically equivalent to EITHER (a) a listed anchor family, OR (b) a topic represented in the live blog/glossary inventory (`website/pages-blog.json`, `website/pages-glossary.json` — match against `metaTitle`, `metaDescription`, or `content` heading hierarchy). Route (b) exists because `anchors.md` is a curated list that necessarily lags new content — any phrase that maps cleanly to a real social.plus blog or glossary topic is a valid Type B candidate, even when no entry in `anchors.md` covers it. Examples — route (a): "customer retention" maps to the user-retention anchor family. Route (b): "social sellers" maps to `/blog/from-viewers-to-belonging-why-community-is-the-engine-of-live-commerce` (live commerce / social commerce topic). The mapping must still be articulable in plain English ("'X' maps to anchor family Y" / "'X' maps to <target URL> on topic Z"). See `references/creative-anchor-patterns.md` for the cache of already-confirmed mappings; append new ones as you discover them. The cache exists to speed re-encounters, NOT as a closed list — absence from the cache is not evidence against a valid mapping.

   **Type C: Single-word glossary anchor.** A single word appears verbatim in the partner's body text, reads as the focal noun of its sentence, is unambiguous in context, AND maps to a glossary entry. Example: "personalization" maps to `/glossary/app-personalization`. "users" or "apps" alone do NOT qualify (too ambiguous). See `references/creative-anchor-patterns.md` for the full list of confirmed mappings; append new ones there as you discover them.

   Search short anchors first (2-3 words), then longer phrases. Long-tail phrases like "how to increase mobile app user engagement" almost never appear verbatim and searching for them first wastes time.

   **The six guardrails (A, B, and C identically).** A candidate is valid only when ALL hold:
   1. The phrase appears verbatim in the partner's body text. Phase 1 never paraphrases. Sentence-level synthesis is Phase 2 only.
   2. The phrase maps to EITHER (a) one topic family in `references/anchors.md` (or two sibling families where article context resolves which target to pick — e.g., user-engagement-metrics vs app-engagement-metrics), OR (b) one topic represented in `website/pages-blog.json` / `website/pages-glossary.json` (match against `metaTitle`, `metaDescription`, or `content` heading hierarchy; the matched page becomes the link target). Either route works. The mapping must be articulable in plain English ("'X' maps to anchor family Y because they describe the same concept" for route (a); "'X' maps to social.plus content at <URL> on topic Z" for route (b)). For sibling-family ambiguity, also state which one the article's framing selects (e.g., "the article is about app-level metrics, so target the app-engagement-metrics family"). Mappings that span unrelated families or unrelated topics disqualify.
   3. The phrase sits in a body paragraph, not an intro or conclusion.
   4. A social.plus target page exists that directly addresses the mapped topic.
   5. The phrase does not cannibalize the partner article's primary ranking keywords.
   6. Length: Type A and B are 2-6 words. Type C is exactly one word AND the target is a glossary entry AND the word is the focal noun of its sentence AND it is unambiguous in context.

   **Fit-score ceilings.** Type A literal matches can reach ⭐⭐⭐ Perfect. Type B creative matches cap at ⭐⭐ Strong, flagged `[creative-anchor]`. Type C single-word glossary matches cap at ⭐⭐ Strong, flagged `[single-word-glossary]`. The caps protect the relationship channel from AI over-reach. They are not a signal of lower discovery priority.

   **One carve-out lowers a Type A ceiling: saturated commercial head terms.** A Type A literal match whose phrase is a saturated commercial keyword — already at ≥10 non-spam refdomains in the live social.plus profile (see the Anchor Diversity Check; "social media app development" and "Community features" at 11 each are today's examples) — does NOT reach ⭐⭐⭐. Cap it at ⭐⭐ and prefer a fresher co-located variant from the same sentence. The Anchor Diversity Check is authoritative over the fit score: when they disagree, the Diversity Check wins. This is a control on our own over-optimization, not a discovery filter — keep flagging the head term during discovery, just don't headline it in the email.

   **Per-section distribution.** The article-level cap is up to 3 placements. There is no per-section cap. If three viable Phase 1 hits all sit in the same section (real case: a Reddit AMAs article with "online communities", "brand loyalty", and "community engagement" as three Type A matches in one section), ship all three.

2. **Check placement position** — The anchor must appear in a body paragraph, not in the introduction or conclusion of the article. Discard matches found in intros/conclusions.

3. **Extract the exact sentence** — For every match, capture the verbatim original sentence from the partner's article. Without a verified original sentence, the placement is incomplete and can't be used.

4. **Match to the best social.plus page** — For each anchor found, determine which social.plus URL is the most relevant target.
   - **Default: prefer a blog post over a glossary entry** (Stefan's correction, 2026-07-06), even for short/definitional anchors like "user engagement" — search `website/pages-blog.json` first for a post that plausibly covers the topic (a stats/benchmarks or strategy post counts) before falling back to glossary. See `references/content-inventory.md` section 2 for the full rule. Exception: Type C single-word anchors still must target glossary (see Phase 1 step 1 length rule) — a one-word link into a blog post reads forced.
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
   - ⭐⭐⭐ **Perfect** — Type A literal anchor verbatim in body paragraph AND partner article traffic ≥ 50/month AND target UR ≥ 10 AND the anchor is NOT a saturated commercial head term (≥10 non-spam refdomains in the live profile — see Anchor Diversity Check; a saturated head term caps at ⭐⭐ and should yield to a fresher co-located variant). Type B and Type C never reach this tier, even when traffic and UR clear the thresholds.
   - ⭐⭐ **Strong** — any of: (a) Type A literal anchor in body paragraph, but either partner traffic < 50 OR target UR < 10; (b) Type B creative anchor in body paragraph (regardless of traffic/UR); (c) Type C single-word glossary anchor in body paragraph (regardless of traffic/UR). Add a `[low-value]` flag in the summary table when partner traffic = 0 AND target UR < 5, with caveat to Stefan: "low-value link both directions, only ship if relationship maintenance is the goal."

The 50, 10, and 5 thresholds are starting heuristics, not absolutes. Adjust based on observed acceptance rates across exchanges.

**Flags appended to the score in the Step 5 summary table:**
- `[fresh-anchor]` — Type B or Type C placement whose anchor phrase has zero presence in the cached live anchor profile (positive signal — creative AND profile-diversifying; see Anchor Diversity Check item 11).
- `[creative-anchor]` — Type B match (semantic-equivalent, not a literal `anchors.md` entry).
- `[single-word-glossary]` — Type C match (single-word anchor into a glossary target).
- `[anchor-reuse: N refdomains]` — proposed anchor is at ≥5 refdomains in the live profile (saturation warning; see Anchor Diversity Check item 7).
- `[low-value]` — partner traffic = 0 AND target UR < 5 (relationship-only placement).
- `[creative-phase2-save]` — Phase 2 creative anchor on a zero-Phase-1-match article (last-resort save; gated to one per article).

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
   - **Anchor preference order (lowest over-optimization risk first — we are drafting the sentence here, so we control the anchor type):**
     1. A **stat-citation** anchor that cites a social.plus statistic and points at the matching stat blog (the "84% of consumers" / "5% rise in retention" pattern). Lowest-risk, most editorial-feeling ask, and the most natural pattern already in our live profile — prefer it whenever a relevant stat exists.
     2. A **partial-match / contextual** phrase already present in the partner's paragraph that maps cleanly to a target.
     3. Only then an approved anchor text from `references/anchors.md` — and never a saturated commercial head term when a fresher option exists (see Anchor Diversity Check).

   **Creative anchors in Phase 2 are tightly gated.** Phase 2 creative anchors are allowed ONLY on articles where Phase 1 returned zero matches across Types A, B, and C. When triggered, allow ONE Phase 2 creative-anchor placement per such article as a "save the article" option. The creative anchor must still satisfy the same six guardrails listed in Phase 1 step 1 (semantic-equivalent, clearly mapped, etc.). The only difference is that the surrounding sentence is being drafted by us, not extracted verbatim. Flag in the summary as `[creative-phase2-save]`. Fit score caps at ⭐ Opportunity. Stefan reviews each one in the Step 3.5 decision gate before drafting the email. Do NOT layer Phase 2 creative anchors on articles that already have a Phase 1 placement; that compounds two layers of synthesis and hurts partner relationships over time.

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

**Gating precondition — run this gate ONLY when 2 or more viable placements exist across the batch.** If viable placements ≤ 1, skip the gate and proceed directly to Step 4 with the single-ask format. Never ask the user anything about existing-backlink partners: the action there is always "acknowledge the existing link, make no new ask." Default to deciding and proceeding; reserve questions for genuine 2+ way packaging choices.

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

**Consolidated multi-site email (DEFAULT when the input contains 2+ partner domains):**

When the user pastes multiple partner domains from one contact, produce ONE consolidated reply — not separate emails per domain. The contact proposed a multi-site exchange and expects a single reply addressing every domain.

**Default assumption (Stefan's correction, 2026-07-06):** a flat pasted list of domains, with no other framing, IS one contact — treat it as one exchange conversation by default. This holds even when each domain's research was parallelized (e.g., separate research passes per domain) — parallelizing the *discovery* work doesn't change that the *output* is one email. Only split into separate per-domain emails when Stefan explicitly says the domains belong to different contacts.

Structure: greeting → one framing line → one section per domain (header = domain name, content varies by outcome) → one closing line → sign-off.

Per-domain section content by outcome:
- **Fresh partner with verified placements** → numbered placement blocks (same Phase 1/Phase 2 format as the single-partner templates below)
- **Existing-backlink partner** (caught by Step 0.0) → one paragraph: "We already have an editorial backlink from your site — [partner URL] links to our article [social.plus URL] using the anchor '[anchor]' (live since [date])."
- **No-fit partner** → one diplomatic line: "I couldn't find a strong topical fit on the blog this round." or "Same — no strong fit on our end this round." Never reveal internal analysis (PBN signals, DR concerns, Chrome navigation blocks, etc.) to the partner.

Closing rules:
- If at least one placement request exists across any domain: standard close "Please let me know which work for you, and what we can do for you in return."
- If zero placements across all domains (all existing-backlink or no-fit): lighter close, e.g. "Happy to keep an eye out on future rounds." No reciprocal ask.

Within each domain section the format is flush-left, no indentation — exactly like the single-partner format.

**Worked example — consolidated multi-site email:**


```
Hi [Name],

Thanks for sharing the list. Here's where we landed on each site:

paylinedata.com
We already have an editorial backlink from your site — paylinedata.com/blog/the-role-of-big-data-in-shaping-banking-services-in-2025 links to our article social.plus/blog/how-to-use-social-features-to-enhance-fintech-app-engagement using the anchor "engagement" (live since 13 March 2025).

pepper.inc
I couldn't find a strong topical fit on the blog this round.

clickpost.ai
Found two good placements I'd like to request:

1. Article: Customer Loyalty Statistics: Key Trends & Insights for 2025
Add link from: https://www.clickpost.ai/blog/customer-loyalty-statistics
Add link to: https://www.social.plus/blog/building-brand-loyalty-the-power-of-digital-communities
Anchor: brand loyalty
Placement: "Why Customer Loyalty Is the New Growth Engine for Ecommerce in 2025" section — the bullet that starts "Brand loyalty programs influence 79% of buying decisions". Anchor goes on the words "Brand loyalty".

Please let me know which work for you, and what we can do for you in return.

Cheers,
Stefan
```


**Single-partner email templates (use when the input is one domain):**

**Canonical Phase 1 email structure (anchor already in body — partner just adds the link):**


```
Hi [Name],

Thanks for sharing. I reviewed [the blog / the docs / your articles] and found [N] good placement[s], which I'd like to request with you:

1. Article: [Article Title]
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
Add link from: [article URL]
Add link to: [social.plus target URL]
Anchor: [anchor text]
Placement: [section name + verbatim sentence]

Option 2
Article: [Article Title]
Add link from: [article URL]
Add link to: [social.plus target URL]
Anchor: [anchor text]
Placement: [section name + verbatim sentence]

Please let me know which one you'd like to go with, or if both work, and what we can do for you in return.

Cheers,
Stefan
```



**Format rules:**
- **Never show the partner article's URL twice.** Don't print a standalone `URL:` line above `Add link from:` — `Add link from:` already states the article URL unambiguously, so a separate `URL:` line is pure repetition (Stefan's correction, 2026-07-06). Each placement block starts with `Article: [title]` and goes straight to `Add link from:` / `Add link to:` — see the templates below.
- Every line in every placement block is flush-left — no indentation under the numbered/Option line. Indented sub-fields wrap weirdly in LinkedIn, Slack, and most chat boxes where markdown doesn't render
- Email bodies use PLAIN URLs only, never markdown links. Markdown does not render in email/LinkedIn/Slack, and wrapping a redirect URL in markdown produces a malformed anchor. Print the full canonical `https://` URL as plain text
- When the reply is delivered by creating a Gmail draft (the Gmail MCP draft tool, e.g. create_draft), pass an explicit `htmlBody` in addition to the plain-text `body`. In the `htmlBody`, render every URL as `<a href="CANONICAL_URL">CANONICAL_URL</a>` so the visible anchor text is the clean canonical URL, render each per-domain section header as bold plain text (`<b>domain.com</b>`, not a link), and use `<br>` for line breaks with every line flush-left. Why: if only a plain-text `body` is passed, Gmail builds the HTML itself and substitutes its outbound redirect (`https://www.google.com/url?q=REAL&source=gmail&ust=...&sa=E`) as both the link target and the visible text, so the recipient sees the wrapped tracking URL. Supplying your own `htmlBody` keeps the visible text clean. Gmail will still rewrite the underlying href to its google.com/url redirect; that is normal, invisible to the reader, and must not be worked around
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
- **Reference files not found**: If any of the five reference files (`references/anchors.md`, `references/content-inventory.md`, `references/creative-anchor-patterns.md`, `website/pages-blog.json`, `website/pages-glossary.json`) can't be loaded, surface immediately with the paths attempted — never guess at anchors or inventory. The JSON files are auto-generated by the Cloudflare Worker; if they're missing or stale, Stefan can trigger a manual refresh via `/generate/blog?token=...` or `/generate/glossary?token=...`.
- **Ahrefs returns no data for the domain**: Rare — usually only brand-new domains. Fall back to Step 2 (sitemap crawl) → browser blog-index crawl (Step 2.5 tool priority) → WebSearch as last resort.
- **Ahrefs returns sparse results for a partner that LOOKS legit by other signals**: Don't decline. Ahrefs's index is incomplete on small blogs (60-80% of pages can be missing). Escalate to a sitemap/browser pass before declaring no fit. This is the most common false-negative trap.
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
- **Site has no sitemap (Step 2 fallback)**: Fall back to browser-based blog-index crawling (Step 2.5 tool priority) → then WebSearch as last resort. See "Fallback" section in Step 2.
- **Mode B with existing backlink on the partner's root domain**: Apply the same logic as Mode A — stop processing, report the existing link's URL and first-seen date to the user, and let them decide whether the new editorial placement is different enough to justify a second link.
- **Mode B (Google Docs) — doc-to-title mapping mix-up**: When fetching multiple docs in one batch, the response order may not match the request order. Always re-verify each placement against the actual doc title before sending it to Stefan. If unsure, re-fetch the single doc to confirm.
- **Mode B — large doc fetches truncate**: Google Docs over a certain size return truncated content. If the article body looks cut off, re-fetch with a narrower range or ask Stefan to share the doc as plain text.
- **Any reference file missing**: The skill depends on five files (three local .md, two remote .json). If any are missing, surface this to Stefan immediately — without them, target picking and anchor matching are guesswork. Don't try to substitute with `marketing-team:site-intelligence` (wrong scope — marketing pages only).
- **Site blocks crawling / WebFetch blocked**: WebFetch is often blocked by the egress proxy. Use the live-page-read tools instead (Step 2.5 priority — Vercel agent-browser first, then Claude in Chrome) — `navigate` to the URL, then `get_page_text` or JavaScript DOM extraction (see Step 2.5) to read the actual content and verify anchors.
- **`get_page_text` returns garbage on ad-heavy sites**: Fall back to JavaScript DOM extraction using the text-to-script ratio pattern described in Step 2.5. This works reliably on most ad-heavy sites where `get_page_text` fails.
- **No relevant content found**: Only declare "no fit" after both Phase 1 and Phase 2 come up empty. Report: "I checked all [X] articles on this site via their sitemap. None have existing anchor matches (Phase 1) or topically relevant sections for suggested placements (Phase 2). The blog covers [brief topic summary]. Skip this one."
- **Multiple good placements on one article**: Include the best 2, max 3 per article. The cap is article-level only. There is no per-section cap. If three viable Phase 1 hits all sit in one section, ship all three.
- **Single viable placement**: Skip the decision gate (Step 3.5) and proceed directly to Step 4 with the single-ask format. There's nothing for Stefan to choose between.
- **More than 5 placements**: Default to recommending option (b) alternatives framing on the top 3 — proposing 6+ placements in one email reads as spam.
- **Partner site is low quality**: Flag it — "This site looks thin/spammy. Worth considering if the link value justifies the effort."
- **Enterprise publishers return query-string variants**: Sites like HubSpot, Salesforce, Adobe, Atlassian crawl the same canonical article at dozens of tracking-link URL variants (e.g., `?hubs_content=...`). Always include `{ "not": { "field": "url", "is": ["isubstring", "?"] } }` in the Tier 3 `where` clause to exclude these at the API level. Verified on hubspot.com: dropped 96 raw rows to 14 clean editorial URLs.
- **Partner sites with user-generated forums**: Some partners host both an editorial blog AND a user-generated community forum (e.g., intercom.com has `community.intercom.com` alongside `blog.intercom.com`). Substring filters pollute the result with forum threads we can't request placements in. The Layer A `prefix` operator scoped to the editorial blog path excludes forum content at the API level.
- **`crawled-pages` 100-row cap**: The endpoint is hard-capped at 100 rows per call regardless of the `limit` parameter (tested at 200, 1000, 5000). The schema's default-1000 claim is misleading. Plan pagination accordingly.
- **Ahrefs where-clause supports `not` wrapper but not `notsubstring` operator**: The grammar is `{ "not": { "field": "...", "is": [op, value] } }`. Trying `notsubstring` as an operator returns "bad where: invalid JSON syntax". Verified condition operators: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `substring`, `isubstring`, `phrase_match`, `iphrase_match`, `prefix`, `suffix`.
- **Layer A prefix probe returns no candidates**: If none of the standard editorial-blog prefix patterns return rows, escalate immediately to Step 2 (sitemap / blog-index crawl). The partner has a non-standard path that Tier 3 substring-only fallback won't handle cleanly.
- **Phase 1 fit-score ceilings**: Only Type A literal matches from `references/anchors.md` reach ⭐⭐⭐ Perfect — and only when the phrase is not a saturated commercial head term (≥10 non-spam refdomains in the live profile; those cap at ⭐⭐ and yield to a fresher co-located variant per the Anchor Diversity Check). Type B creative semantic-equivalent matches cap at ⭐⭐ Strong. Type C single-word glossary matches cap at ⭐⭐ Strong. The caps protect the relationship channel against AI over-reach in anchor identification; they do NOT signal lower discovery priority. Treat B and C as first-class Phase 1 candidates.
- **Phase 2 creative anchor is a last-resort save**: Allowed only when Phase 1 returned zero matches across Types A, B, and C on the article. Capped at one creative-anchor placement per zero-match article. Flagged as `[creative-phase2-save]` in the summary table. Stefan reviews before email is drafted. Do not layer creative anchors onto articles that already have a Phase 1 placement.
- **Type C single-word glossary anchors require glossary targets**: A single-word anchor (e.g., "personalization", "communities") is allowed when ALL of: the target is a glossary entry, the word reads as the focal noun in context, and the word is unambiguous. Single-word anchors pointing to blog posts remain disallowed because blog targets are strategic/long-form and a one-word link reads forced. Fit score caps at ⭐⭐ Strong.
- **Proposed anchor is saturated in our live profile or duplicated in the batch**: Look for a verbatim variant in the same sentence first (see Anchor Diversity Check, Step 3), then consider a different anchor family on the same article. If no clean alternative exists and the placement is strong, keep it but flag `[anchor-reuse: N refdomains]` in the summary table — Stefan decides. Never silently ship two identical anchors in one email.
- **Multiple partner domains in one request**: Produce a single consolidated email addressing all domains (see Step 4, "Consolidated multi-site email"). Never split into separate per-domain emails — the contact proposed a multi-site exchange and expects one reply.
- **PBN/content-farm reject**: The partner-facing email gets only a diplomatic "no strong fit this round" line. PBN signals, manipulated DR patterns, pirate-keyword profiles, and Ahrefs unit budgets are user-facing analysis only — never expose these to the partner.
- **Live-page reads blocked on a partner domain** (both Vercel agent-browser and Claude in Chrome fail): Flag to Stefan as a user-facing note. For partner-facing copy, treat as no-fit ("no strong fit this round") unless Stefan unblocks and re-runs.

## What NOT to Do

- Don't suggest placements where the link would feel forced or out of context
- Don't recommend linking from irrelevant articles just to get a placement
- Don't invent anchor phrases that don't appear verbatim in the partner's body text. Phase 1 Types A, B, and C all require the phrase to be in the text already. Phase 2 creative anchors require all six guardrails from Phase 1 step 1 and are gated to zero-match articles only.
- Don't under-flag Type B creative or Type C single-word glossary candidates because they "feel like exceptions." They are first-class Phase 1 hits and the most common source of leaked-on-the-table placements. The ⭐⭐ cap handles the relationship risk; discovery should be confident.
- Don't reuse the same anchor text across two placements in one batch, and don't default to saturated head terms ("social media app development", "Community features", "social features") when a fresh verbatim variant exists in the same sentence — run the Anchor Diversity Check in Step 3 and skip neither the profile pull nor the batch de-dupe
- Don't randomize or rotate anchors to manufacture natural-looking variety, and don't reach for an exact-match commercial keyword as the default — prefer the lowest-risk type that fits (stat-citation or contextual over exact-match commercial), and let real variation come from each partner's own sentences (see Anchor Rules and the Anchor Diversity Check, steps 9–10). Synthetic rotation is itself a footprint.
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
- Don't expose internal quality analysis to the partner. PBN/content-farm rejections, DR concerns, Ahrefs unit budgets, Chrome access errors, and tier-2 vertical-fit verdicts are user-facing only. The partner-facing line is always a diplomatic "no strong fit this round" or equivalent
- Don't split a multi-domain request into multiple emails. When the input contains 2+ partner domains from one contact, produce one consolidated reply (see Step 4)
- Don't default to exact-match commercial anchors when a lower-risk type fits the context (see Anchor Diversity Check step 9)
