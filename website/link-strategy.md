# social.plus internal linking strategy

This file is the single source of truth for **canonical anchor → page** decisions, **cannibalization warnings**, and **anchor variation rules** across the social.plus content ecosystem. The `internal-linking-optimizer` skill consumes this file at runtime.

**Generated:** 2026-04-17
**Refresh by:** 2026-07-16 (90 days)
**Data sources:**
- Ahrefs site-explorer (organic-keywords, top-pages, pages-by-internal-links, domain-rating) for `social.plus` (subdomains, both protocols)
- Ahrefs GSC integration (gsc-keywords, gsc-pages) for project `7031381` — last 90 days of real Google Search Console data
- The 10 `pages-*.json` snapshots in this directory (regenerated automatically on every Webflow publish)

**Site benchmarks at generation time:**
- Domain Rating (Ahrefs): **65**
- Top organic page (non-brand): `https://www.social.plus/white-label/social-network` (606 monthly traffic, UR 7.0)
- Highest-UR page: `https://www.social.plus/` (UR 11.0) — primary authority hub
- Total ranked keywords surveyed: top 200 by traffic, top 300 by GSC clicks

---

## Data scope

The optimizer reads from these files (all in `website/` of this repo). Together they index **646 pages**:

| File | Items | Role for linking |
|---|---|---|
| `pages-marketing.json` | 22 | Primary commercial targets — homepage, product/feature/SDK pages, white-label pages |
| `pages-use-cases.json` | 11 | Use-case framings (`/use-case/*`) |
| `pages-industry.json` | 10 | Industry vertical pages (`/industry/*`) |
| `pages-glossary.json` | 76 | Definitional/informational targets (`/glossary/*`) |
| `pages-blog.json` | 248 | Blog → blog cross-linking; long-tail informational |
| `pages-customer-stories.json` | 42 | Proof-point links (`/customer-story/*`) |
| `pages-answers.json` | 123 | AEO related-answer links (`/answers/*`) |
| `pages-product-updates.json` | 58 | "What's new" reference links |
| `pages-release-notes.json` | 31 | Specific release reference links |
| `pages-webinars.json` | 25 | Webinar reference links — URLs serve at `/events/{slug}` (the Webflow slug-base is "events", not "webinars") |

All entries share the same shape: `{url, metaTitle, metaDescription, content}`. URLs are full `https://www.social.plus/...`.

**The JSON files are a heading-level index, not full content.** Each entry contains H1-H6 plus metaTitle/metaDescription, no body. Body content lives on the live web. The optimizer compensates with a two-phase workflow: shortlist candidate target pages from the JSON, then live-fetch the top candidates to verify and find precise insertion points. See the optimizer skill's "Architecture: two-phase shortlist + live fetch" section for details.

**Known JSON capture gaps:**
- **Static marketing/industry pages:** the snapshot generator uses Webflow's Pages DOM API, which doesn't traverse Components/Symbols. Headings inside reusable blocks (most of the industry pages and parts of marketing) won't appear in the JSON. The live-fetch phase backfills this completely.
- **Other CMS files** (blog, glossary, answers, etc.) capture all H1-H6 from the rich-text field but don't include the page-template chrome (e.g., the "Subscribe to our newsletter" sections). Live fetch backfills these too.

**Which files to fetch by context** (the optimizer applies these defaults):
- **Blog draft (called by `blog-seo-content`):** marketing + use-cases + industry + glossary + blog + customer-stories
- **AEO draft (called by `aeo-content`):** marketing + use-cases + glossary + answers (related-answers)
- **Standalone audit:** all 10 files
- **Standalone draft (user-pasted content):** marketing + use-cases + industry + glossary by default; ask if more is needed

**Live-fetch budget** (per optimizer invocation):
- Draft mode: max 8 live WebFetch calls (one per shortlisted candidate)
- Audit mode: live fetch reserved for the top 5-10 highest-impact gaps in the implementation plan

---

## How to use this file

**Draft mode (when called by `blog-seo-content`, `aeo-content`, etc.):**

1. Identify candidate anchor terms in the draft.
2. For each candidate, check the **canonical anchor map** below — if the anchor matches a row, use the listed target URL.
3. Cross-check against **cannibalization warnings** — if a warning fires, follow its rule (use the recommended target, or split intent: definitional → glossary, commercial → product page).
4. Apply **per-cluster anchor variation rules** — no anchor should appear more than twice per article pointing to the same page.
5. Prefer **link-equity hubs** as targets when contextually appropriate (homepage, white-label pages, top-traffic glossary entries).

**Audit mode (standalone):**

1. Compare site-wide anchor usage against the canonical anchor map. Flag mismatches.
2. Cross-reference cannibalization warnings against current link patterns. Flag violations.
3. Identify orphans by looking for pages with no contextual inbound links across all 10 files.
4. Recommend phased fixes.

---

## Canonical anchor map

The canonical target is the page that should "own" each anchor. Use the listed URL exactly. URLs are absolute (`https://www.social.plus/...`) per the data files.

### Brand
| Anchor terms | Canonical target |
|---|---|
| "social plus", "socialplus", "social+", "social.plus" | `https://www.social.plus/` |

### Chat cluster
| Anchor terms | Canonical target |
|---|---|
| "in-app chat", "chat infrastructure", "real-time messaging" | `https://www.social.plus/chat` |
| "chat features", "messaging features" | `https://www.social.plus/chat/features` |
| "chat SDK", "messaging SDK", "build chat into your app" | `https://www.social.plus/chat/sdk` |
| "chat UIKit", "react native chat ui", "chat UI components" | `https://www.social.plus/chat/uikit` |
| "live chat" (use-case framing) | `https://www.social.plus/use-case/live-chat` |
| "group chat", "group messaging" | `https://www.social.plus/use-case/group-chat` |
| "1:1 chat", "private chat", "direct message" | `https://www.social.plus/use-case/1-1-chat` |
| "white label chat", "white label messaging" | `https://www.social.plus/white-label/chat-software` |

### Social cluster
| Anchor terms | Canonical target |
|---|---|
| "in-app community", "in-app social", "social features" | `https://www.social.plus/social` |
| "social features list", "community features" | `https://www.social.plus/social/features` |
| "social SDK", "community SDK" | `https://www.social.plus/social/sdk` |
| "social UIKit", "feed UI components" | `https://www.social.plus/social/uikit` |
| "stories" (product), "social stories" | `https://www.social.plus/social/stories` |
| "white label social network", "white label social platform" | `https://www.social.plus/white-label/social-network` |
| "white label community" | `https://www.social.plus/white-label/in-app-community` |
| "activity feed" (product framing) | `https://www.social.plus/use-case/activity-feed` |
| "groups", "communities" | `https://www.social.plus/use-case/groups` |
| "user profiles", "in-app profiles" | `https://www.social.plus/use-case/user-profiles` |
| "custom posts", "rich post types" | `https://www.social.plus/use-case/custom-posts` |
| "polls", "in-app polls" | `https://www.social.plus/use-case/polls` |

### Video cluster
| Anchor terms | Canonical target |
|---|---|
| "live video", "online live video", "video infrastructure" | `https://www.social.plus/video` |
| "video features", "in-app video features" | `https://www.social.plus/video/features` |
| "video SDK" (commercial) | `https://www.social.plus/video/sdk` |
| "livestream", "in-app livestream" | `https://www.social.plus/use-case/livestream` |
| "stories and clips", "clips" | `https://www.social.plus/use-case/stories-and-clips` |
| "events" (use-case framing) | `https://www.social.plus/use-case/events` |
| "vs Stream", "alternative to Stream" | `https://www.social.plus/vs-stream` |

### Cross-cluster
| Anchor terms | Canonical target |
|---|---|
| "moderation", "content moderation", "community moderation" | `https://www.social.plus/moderation` |
| "monetization", "in-app monetization", "social commerce" | `https://www.social.plus/monetization` |
| "analytics", "engagement analytics", "community analytics" | `https://www.social.plus/analytics` |
| "pricing", "social.plus pricing" | `https://www.social.plus/pricing` |
| "product overview" | `https://www.social.plus/product` |

### Industry cluster
| Anchor terms | Canonical target |
|---|---|
| "[industry] community platform", "social for [industry]" | `https://www.social.plus/industry/[industry]` |

Industries: `retail`, `fitness`, `travel`, `sports`, `health-and-wellness`, `fintech`, `media-and-news`, `edtech`, `gaming`, `betting`.

### Glossary (definitional anchors)

The glossary indexes 76 definitional pages. **Default rule:** use a glossary anchor only when the surrounding context is *defining* the term, not pitching the product. For commercial intent, use the product/use-case page above. Common pairs where intent matters:

| Definitional anchor → glossary | Commercial alternative → product/use-case |
|---|---|
| "social feed" → `https://www.social.plus/glossary/social-feed` | "activity feed" → `https://www.social.plus/use-case/activity-feed` |
| "activity feed" (defining) → `https://www.social.plus/glossary/activity-feed` | "activity feed" (product) → `https://www.social.plus/use-case/activity-feed` |
| "video SDK" (defining) → `https://www.social.plus/glossary/video-sdk` | "video SDK" (commercial) → `https://www.social.plus/video/sdk` |
| "websocket" → `https://www.social.plus/glossary/websocket` | (no commercial alternative) |
| "user retention", "user engagement", "session length", "interaction rate" | (definitional only) → matching `/glossary/*` |
| "white label chat" (defining) → `https://www.social.plus/glossary/white-label-chat` | "white label chat" (commercial) → `https://www.social.plus/white-label/chat-software` |
| "white label social features" → `https://www.social.plus/glossary/white-label-social-features` | (commercial → `/white-label/social-network` or `/social`) |
| "white label social network" (defining) → `https://www.social.plus/glossary/white-label-social-network` | "white label social network" (commercial) → `https://www.social.plus/white-label/social-network` |
| "vertical social network" → `https://www.social.plus/glossary/vertical-social-network` | (definitional only — be careful, "social network" is a forbidden positioning term per terminology.md) |
| "chat widget" → `https://www.social.plus/glossary/chat-widget` | (commercial → `/chat`) |
| "chat channel" → `https://www.social.plus/glossary/chat-channel` | (commercial → `/chat`) |

For glossary terms not in this table, use them as link targets only in genuinely definitional/explanatory passages (e.g., AEO articles, blog post lead-in sections defining a concept).

---

## Cannibalization warnings

Pairs or groups of pages competing for the same query. Follow the recommendation strictly.

### ⚠️ "social plus AI" / "social+ AI" — 42 URLs ranking
**Top URL (GSC):** `https://www.social.plus/analytics` (115 clicks/90d for "social plus ai")
**Risk:** 42 different URLs rank for variants of this brand+AI query. Without consolidation, link equity is split.
**Rule:** When an article mentions "social.plus AI", anchor it to `https://www.social.plus/analytics`. Do not create new alternative landing pages for "AI" without first consolidating.

### ⚠️ "live video" vs `/use-case/livestream`
**Top URL:** `https://www.social.plus/video` (top URL for both "live video" and "online live video" per GSC and Ahrefs)
**Rule:** Anchor "live video" / "online live video" → `https://www.social.plus/video`. Anchor "livestream" / "in-app livestream" → `https://www.social.plus/use-case/livestream`. Never anchor "live video" to `https://www.social.plus/use-case/livestream`.

### ⚠️ "chat API" — informational vs commercial split
**Pages:** `https://www.social.plus/glossary/chat-api` (informational) vs `https://www.social.plus/chat`, `https://www.social.plus/chat/sdk` (commercial)
**Rule:**
- **Informational/definitional** content (e.g., "what is a chat API", AEO articles): anchor "chat API" → glossary.
- **Commercial/product** content (blog posts pitching social.plus): anchor "chat API" → `/chat/sdk` (developer-intent) or `/chat` (decision-maker intent).
- **Never use the same anchor "chat API" pointing to two different pages within a single article.**

### ⚠️ "video SDK" — informational vs commercial split
**Pages:** `https://www.social.plus/glossary/video-sdk` vs `https://www.social.plus/video/sdk`
**Rule:** Same pattern as chat API. Definitional → glossary; commercial → product page.

### ⚠️ "social feed" vs "activity feed" — definitional vs product split
**Pages:** `https://www.social.plus/glossary/social-feed` vs `https://www.social.plus/use-case/activity-feed` vs `https://www.social.plus/glossary/activity-feed`
**Rule:**
- "social feed" (definitional) → glossary
- "activity feed" (product, in pitch context) → use-case page
- "activity feed" (defining the term) → glossary
- Never use "social feed" anchor in product framing — readers expect the glossary.

### ⚠️ "white label social network" / "white label chat" — definitional vs commercial split
The data layer now has BOTH a glossary entry and a commercial page for these terms.
**Rule:**
- Defining the term (e.g., AEO article, blog explainer): anchor → `/glossary/white-label-social-network` or `/glossary/white-label-chat`.
- Pitching the product (commercial blog, comparison content): anchor → `/white-label/social-network` or `/white-label/chat-software`.
- These are HIGH-VALUE commercial keywords (Ahrefs: top 3 ranks across multiple "white label" terms). Don't dilute by mixing the two.

### ⚠️ "engagement rate" — weak SERP, not a linking issue
**Page:** `https://www.social.plus/glossary/engagement-rate` (12,393 impressions, 0.19% CTR over 90d per GSC)
**Note:** Page exists and ranks but underperforms in SERP. **No linking action required.** Flag for the content team as a separate page-health issue (title/meta refresh).

### 🚫 Do-not-link list (orphan URLs serving wrong content)

These URLs return 200 but serve content that doesn't match the URL slug. Do not propose them as link targets in any draft. The user should clean them up in Webflow (delete or 301-redirect).

| Orphan URL | What it actually serves | Redirect target (recommended) | GSC clicks/90d |
|---|---|---|---|
| `https://www.social.plus/use-cases/temporary-live-1-1-chat` (note plural `/use-cases/`) | The Chat SDK landing page (H1: "Build in-app messaging faster with a Chat SDK") | `https://www.social.plus/chat/sdk` (where the served content actually lives) or `https://www.social.plus/use-case/1-1-chat` (canonical use-case for the slug intent) | 42 |

If you find more `/use-cases/*` (plural) URLs ranking in GSC, treat them the same way until cleaned up. The canonical use-cases collection is `/use-case/` (singular) per `pages-use-cases.json`.

### ⚠️ Brand URL splitting — informational only
54+ URLs rank for "socialplus" / "social plus" / "social+". For brand terms, Google routes correctly to `/`. **No action required**, but be aware: when writing about social.plus on third-party sites or guest posts, always link the brand mention to `https://www.social.plus/`, never to a feature page.

### ⚠️ "social network" terminology is forbidden in positioning
Per `messaging/terminology.md`, do not call social.plus a "social network" or "forum platform". The `/glossary/vertical-social-network` page exists for definitional/informational content but never anchor it from copy that's pitching social.plus — this is a brand positioning rule, not just a linking rule.

---

## Link-equity hubs (concentration of authority)

When suggesting link **destinations** in draft mode, these are high-priority targets — linking *to* them reinforces site-wide authority. When suggesting link **sources** in audit mode, these pages are also where outbound links matter most.

| Page | URL Rating | File |
|---|---|---|
| `https://www.social.plus/` | 11.0 | pages-marketing |
| `https://www.social.plus/white-label/social-network` | 7.0 | pages-marketing |
| `https://www.social.plus/glossary/social-feed` | 4.6 | pages-glossary |
| `https://www.social.plus/glossary/community-app` | 4.5 | pages-glossary |
| `https://www.social.plus/glossary/video-sdk` | 4.5 | pages-glossary |
| `https://www.social.plus/glossary/engagement-rate` | 4.4 | pages-glossary |
| `https://www.social.plus/glossary/chat-api` | 4.4 | pages-glossary |
| `https://www.social.plus/blog/what-is-community-based-marketing-cbm` | 4.4 | pages-blog |

Notable absence: no in-scope product/feature page broke UR 4.0 at generation time. **This is a finding, not a bug** — product pages are commercial/short-tail and don't accumulate organic backlinks the way glossary/blog content does. Audit mode should propose internal linking patterns that direct authority *from* the high-UR glossary/blog pages *to* product pages.

---

## Orphan / under-linked pages

From Ahrefs `pages-by-internal-links` (ascending). Most "orphan" results were pagination artifacts (`?f806444f_page=2` Webflow query strings) or `docs.social.plus` RSS feeds — those are **not real orphans**.

**Real candidates worth flagging in audit mode:**
- `/events/*` pages (e.g., `/events/understanding-zero-party-data-part-2`) — multiple events appear with only 1 inbound link (events aren't yet in the data files)
- All marketing pages have nav links from header/footer so are not *technical* orphans, but these are *contextually* under-linked per data patterns:
  - `/monetization` — rarely cross-linked
  - `/video/features` — under-linked vs `/video` itself
  - `/industry/edtech`, `/industry/health-and-wellness` — less prominent than `/industry/gaming` or `/industry/betting` in current cross-linking
  - `/use-case/groups`, `/use-case/user-profiles` — fewer inbound contextual links than other use cases

**Note:** The contextual under-linking is a hypothesis from data patterns. Confirm with audit mode runs against the JSON data before acting.

---

## Per-cluster anchor variation rules

To avoid over-optimization, each cluster has 5-8 anchor variants. **Rule:** within a single article, the same anchor pointing to the same page should appear no more than **twice**. Use variants for additional links to the same target.

### Chat cluster
Targets: `/chat`, `/chat/features`, `/chat/sdk`, `/chat/uikit`, `/use-case/live-chat`, `/use-case/group-chat`, `/use-case/1-1-chat`, `/white-label/chat-software`

Anchor variants pool:
- "in-app chat"
- "chat infrastructure"
- "messaging SDK" / "chat SDK"
- "real-time messaging"
- "chat features"
- "build chat into your app"
- "in-app messaging"
- "messaging infrastructure"
- "white label chat"

### Social cluster
Targets: `/social`, `/social/features`, `/social/sdk`, `/social/uikit`, `/social/stories`, `/use-case/activity-feed`, `/use-case/groups`, `/use-case/user-profiles`, `/use-case/custom-posts`, `/use-case/polls`, `/white-label/social-network`, `/white-label/in-app-community`

Anchor variants pool:
- "in-app community"
- "social features"
- "activity feed"
- "social SDK"
- "community building blocks"
- "in-app social experiences"
- "user-generated content infrastructure"
- "white label community"
- "white label social platform"

### Video cluster
Targets: `/video`, `/video/features`, `/video/sdk`, `/use-case/livestream`, `/use-case/stories-and-clips`, `/use-case/events`, `/vs-stream`

Anchor variants pool:
- "live video"
- "in-app livestream"
- "video SDK"
- "live streaming SDK"
- "stories and clips"
- "video infrastructure"
- "events platform"
- "alternative to Stream"

### Industry cluster
Targets: `/industry/retail`, `/industry/fitness`, `/industry/travel`, `/industry/sports`, `/industry/health-and-wellness`, `/industry/fintech`, `/industry/media-and-news`, `/industry/edtech`, `/industry/gaming`, `/industry/betting`

Anchor variants pool (substitute industry name):
- "[industry] community platform"
- "[industry] engagement"
- "social features for [industry]"
- "in-app community for [industry]"
- "[industry] social SDK"

### Cross-cluster
- `/moderation`: "moderation", "content moderation", "community moderation", "in-app moderation"
- `/monetization`: "monetization", "in-app monetization", "social commerce", "community monetization"
- `/analytics`: "analytics", "engagement analytics", "community analytics", "social.plus AI" (with the cannibalization caveat above)
- `/pricing`: "pricing", "social.plus pricing", "see pricing"

---

## Blog → blog cross-linking

`pages-blog.json` contains 248 articles. The optimizer treats blog posts as both *sources* and *targets* for cross-links. Guidelines:

- **Pillar/hub blog posts** (highest UR or sum_traffic per Ahrefs): `/blog/what-is-community-based-marketing-cbm` (UR 4.4), `/blog/effective-customer-engagement-strategies-with-case-studies` (pos #1 for "customer engagement case studies"). These deserve more inbound cross-links.
- **Avoid same-anchor-twice pattern across the entire blog.** If two different blog posts both anchor "community engagement" to the same target, prefer variation.
- **Don't cross-link to outdated posts.** Check `metaTitle` / `metaDescription` for clearly dated content (year in title, deprecated framing). Optimizer should flag outdated targets.
- **Cluster blog posts around a hub.** If 3+ blog posts cover variants of a topic, identify the strongest one as hub and link the others to it.

---

## AEO related-answers

`pages-answers.json` contains 123 AEO articles. AEO articles are reference content cited by AI engines — over-linking dilutes citation value. Guidelines:

- **Maximum 1-3 internal links per AEO article.** Stricter than blog.
- **Allowed link locations:** definition paragraph, "why it matters", architecture/features sections, step-by-step. **Disallowed:** FAQs, conclusion, metrics table.
- **AEO → AEO related-answer links:** at most 1 per article, placed in the definition paragraph or step-by-step. Use when the linked article extends a concept (e.g., "API for Integrating Complete Social Features into Apps" can link to a more specific "Chat API" answer).
- **AEO → glossary links** are usually a better fit than AEO → product pages for the definitional sections.
- **AEO → product page links** belong in the "social.plus pitch" section.

---

## Customer stories as proof points

`pages-customer-stories.json` contains 42 customer stories. Use as link targets when:

- A blog post or marketing page mentions a customer by name (link the customer name to their story).
- A claim needs proof (e.g., "60% MoM growth" → link to Smart Fit story).
- Industry pages (`/industry/*`) should link to customer stories from that industry where available.

**Caution:** Only cite approved customer names per `messaging/terminology.md`. The data file may contain stories for customers not yet approved for marketing use — when in doubt, skip.

---

## Refresh procedure

To regenerate this file, re-run these Ahrefs MCP queries (current values noted for diff comparison):

```
management-projects → confirm social.plus project ID is still 7031381
site-explorer-domain-rating(target=social.plus, date=today) → expect DR ~65
site-explorer-organic-keywords(target=social.plus, mode=subdomains, protocol=both, date=today, select="keyword,best_position,best_position_url,volume,sum_traffic,is_branded,is_commercial,is_informational,keyword_difficulty", order_by="sum_traffic:desc", limit=200)
site-explorer-top-pages(target=social.plus, mode=subdomains, protocol=both, date=today, select="url,sum_traffic,value,top_keyword,top_keyword_volume,top_keyword_best_position,keywords,ur", order_by="sum_traffic:desc", limit=60)
site-explorer-pages-by-internal-links(target=social.plus, mode=subdomains, protocol=both, select="url_to,links_to_target,dofollow_to_target,url_rating_target", order_by="links_to_target:asc", limit=100)
gsc-keywords(project_id=7031381, date_from=today-90d, date_to=today, limit=300)
gsc-pages(project_id=7031381, date_from=today-90d, date_to=today, limit=100)
```

After running, review:
1. **New cannibalization candidates:** any keyword in the GSC table where `urls_count > 10` AND it's NOT a brand term.
2. **New top pages:** changes in the top 10 by sum_traffic — update the canonical map and hub list.
3. **New orphans:** pages with `links_to_target` ≤ 2 that should not be (skip pagination/RSS artifacts).
4. **DR drift:** if DR moves more than ±5, re-evaluate the linking strategy at a higher level (Stefan).
5. **New pages in the JSON snapshots:** check `_meta.itemCount` for each `pages-*.json` — a jump in count means new pages need to be added to the canonical map and cannibalization analysis.

Update the `Generated:` and `Refresh by:` dates at the top.
