# social.plus internal linking strategy

This file is the single source of truth for **site architecture**, **canonical anchor → page** decisions, **cannibalization warnings**, **link budgets**, **anchor distribution targets**, **placement rules**, and **scoring** across the social.plus content ecosystem. The `internal-linking-strategist` skill consumes this file at runtime. Other content skills (`blog-seo-content`, `aeo-content`, `case-study`, `brand-messaging`) defer to the optimizer and, by extension, to this file.

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

## Executive summary

**Architecture:** hub-and-spoke with soft silos per product cluster (chat / social / video), plus three cross-cluster capability pillars (moderation / monetization / analytics) and an industry lattice (10 `/industry/*` pages) that links across clusters. Definitional/informational content lives in the glossary + AEO answers and routes intent separately from commercial content.

**Primary problems this file solves:**
1. Picking the right target URL for any anchor (canonical anchor map).
2. Preventing keyword cannibalization across 646 pages (cannibalization warnings, grounded in 90d GSC data).
3. Keeping commercial intent separate from definitional intent (glossary vs product/use-case split).
4. Redistributing authority from high-UR glossary/blog pages *to* product pages (authority-flow rules).
5. Catching orphans and under-linked pages before they lose rankings.
6. Enforcing anchor diversity so nothing looks over-optimized.

**Quantitative targets:**
- Structure Score ≥ 8 / 10 site-wide
- Anchor Score ≥ 8 / 10 site-wide
- 0 real orphans (pagination/RSS artifacts excluded)
- Max click depth from homepage: 3
- Exact-match anchor share: ≤ 15% site-wide
- Generic anchor share ("learn more", "this article"): ≤ 5% site-wide

See **Scoring & measurement** for how these are computed.

---

## Architecture model

**Model:** Hub-and-spoke with soft silos.

- **Hubs (pillars)** are the product cluster landers: `/chat`, `/social`, `/video`, plus cross-cluster capability pillars `/moderation`, `/monetization`, `/analytics`, and `/pricing`.
- **Spokes (clusters)** are feature pages (`/chat/features`, `/chat/sdk`, `/chat/uikit`), use-cases (`/use-case/*`), white-label variants (`/white-label/*`), and supporting glossary / blog / AEO / customer-story content.
- **Soft silos**: within a pillar, cluster pages link bidirectionally with the pillar and freely with sibling clusters in the same pillar. Cross-pillar links (e.g. chat → video) are allowed as **bridge links** only when the user intent overlaps (a "live chat during live events" article legitimately bridges chat ↔ video).
- **Industry lattice**: `/industry/*` pages are not part of any single pillar — they are a horizontal lattice that should link across into all three product pillars plus `/moderation`, `/monetization`, `/analytics`, and a customer story from that industry (where approved).
- **Definitional vs commercial routing**: glossary + AEO answers are a parallel universe. Cannibalization warnings below enforce the split (definitional → glossary; commercial → product/use-case).

**Why not a strict silo?** Strict silos trap link equity. Our pillars overlap at the product level (many customers buy chat + social + video), so we want bridge links to reflect real buying journeys.

**Why not flat?** 646 pages is beyond what flat architecture supports without everything ending up 2–3 clicks deep *and* undifferentiated. Hub-and-spoke concentrates authority where we want it (the pillar landers) while letting long-tail content cluster naturally.

**Max click depth from the homepage: 3.** Any page deeper than that should be flagged in audit mode.

---

## Pillar → cluster map

Enforce bidirectional links (pillar ↔ every cluster page) and sibling cross-links within each pillar.

### Chat pillar — `/chat`

| Role | Page |
|---|---|
| Pillar | `https://www.social.plus/chat` |
| Sub-product | `/chat/features`, `/chat/sdk`, `/chat/uikit` |
| Use-cases | `/use-case/live-chat`, `/use-case/group-chat`, `/use-case/1-1-chat` |
| White-label | `/white-label/chat-software` |
| Definitional (glossary) | `/glossary/chat-api`, `/glossary/chat-widget`, `/glossary/chat-channel`, `/glossary/white-label-chat` |

### Social pillar — `/social`

| Role | Page |
|---|---|
| Pillar | `https://www.social.plus/social` |
| Sub-product | `/social/features`, `/social/sdk`, `/social/uikit`, `/social/stories` |
| Use-cases | `/use-case/activity-feed`, `/use-case/groups`, `/use-case/user-profiles`, `/use-case/custom-posts`, `/use-case/polls` |
| White-label | `/white-label/social-network`, `/white-label/in-app-community` |
| Definitional (glossary) | `/glossary/social-feed`, `/glossary/activity-feed`, `/glossary/community-app`, `/glossary/vertical-social-network`, `/glossary/white-label-social-network`, `/glossary/white-label-social-features` |

### Video pillar — `/video`

| Role | Page |
|---|---|
| Pillar | `https://www.social.plus/video` |
| Sub-product | `/video/features`, `/video/sdk` |
| Use-cases | `/use-case/livestream`, `/use-case/stories-and-clips`, `/use-case/events` |
| Competitor compare | `/vs-stream` |
| Definitional (glossary) | `/glossary/video-sdk` |

### Cross-cluster capability pillars

| Pillar | Role | Notes |
|---|---|---|
| `/moderation` | Horizontal — linked from chat + social + video clusters | Currently under-linked (see Orphan section) |
| `/monetization` | Horizontal — linked from social + use-case pages | Currently under-linked |
| `/analytics` | Horizontal — owns the "social.plus AI" query cluster (42 ranking URLs) | See cannibalization rule |
| `/pricing` | Conversion endpoint — linked from every pillar and most use-cases |
| `/product` | Product overview — linked from homepage, blog, AEO |

### Industry lattice

10 `/industry/*` pages (retail, fitness, travel, sports, health-and-wellness, fintech, media-and-news, edtech, gaming, betting). Each industry page must link to:
- The three product pillars (`/chat`, `/social`, `/video`) using industry-framed anchors.
- `/moderation`, `/monetization`, `/analytics` — whichever is most relevant to that industry.
- 1–2 customer stories from that industry (where approved per `messaging/terminology.md`).
- 1–3 glossary entries most relevant to the industry vocabulary.

### Bridge-link policy

Cross-pillar links are allowed when:
- The user intent spans pillars (e.g., "live chat during livestreams" → chat + video).
- A use-case draws on multiple pillars (e.g., `/use-case/events` touches video + social + chat).
- A customer story uses multiple products.

Cross-pillar links are **not** allowed when:
- The linked pillar is only tangentially related. Err on the side of not linking.
- The bridge dilutes the article's primary keyword focus.

Maximum 2 bridge links per article.

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
- **AEO draft (called by `aeo-content`):** marketing + use-cases + glossary + answers (related-answers) + customer-stories
- **Customer story draft (called by `case-study`):** marketing + use-cases + industry + customer-stories + pillar that matches the customer's product usage
- **Standalone audit:** all 10 files
- **Standalone draft (user-pasted content):** marketing + use-cases + industry + glossary by default; ask if more is needed

**Live-fetch budget** (per optimizer invocation):
- Draft mode: max 8 live WebFetch calls (one per shortlisted candidate)
- Audit mode: live fetch reserved for the top 5-10 highest-impact gaps in the implementation plan

---

## How to use this file

**Draft mode (when called by `blog-seo-content`, `aeo-content`, `case-study`, etc.):**

1. Identify candidate anchor terms in the draft.
2. For each candidate, check the **canonical anchor map** — if the anchor matches a row, use the listed target URL.
3. Cross-check against **cannibalization warnings** — if a warning fires, follow its rule (use the recommended target, or split intent: definitional → glossary, commercial → product page).
4. Apply the **link budget by article type** below to cap total link count.
5. Apply the **anchor text distribution targets** — match site-wide proportions.
6. Apply the **placement rules** — allowed/disallowed locations per article type.
7. Apply **per-cluster anchor variation rules** — no anchor should appear more than twice per article pointing to the same page.
8. Apply the **forbidden patterns** check — run the bad/good example filter on every proposed link.
9. Prefer **link-equity hubs** as targets when contextually appropriate, but follow authority-flow rules (high-UR glossary pages should redistribute *to* product pages).
10. Before delivering, run the **evaluation questions** as a final quality gate on every link.

**Audit mode (standalone):**

1. Compute **Structure Score** and **Anchor Score** against the rubric.
2. Compare site-wide anchor usage against the canonical anchor map. Flag mismatches.
3. Cross-reference cannibalization warnings against current link patterns. Flag violations.
4. Identify orphans and under-linked pages across all 10 files and via Ahrefs `pages-by-internal-links`.
5. Compute anchor distribution and flag over-optimization (exact-match > 15% site-wide or generic > 5%).
6. Output the **phased implementation plan** (see template below).
7. Estimate impact per fix using the success-metrics table.

**Reverse mode (when a new page ships in Webflow):**

1. Add canonical anchor row(s) to the appropriate cluster section of this file.
2. Identify 3–10 existing pages that should link *to* the new page (pillar, sibling clusters, related glossary, related blog posts).
3. Propose the inbound edits with specific anchor text and insertion points.
4. Run the placement + forbidden-pattern check on each proposed edit.

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

## Link budgets by article type

**Rule of thumb:** 3–10 internal links per 1,000 words, depending on article type. Quality beats quantity — skipping a weak link is better than forcing one.

| Article type | Min | Target | Max | Notes |
|---|---|---|---|---|
| **Marketing/product page** | 5 | 8 | 15 | Must link to at least 2 siblings, 1 pillar (if not pillar itself), `/pricing`, and 1 supporting use-case |
| **Pillar landing (e.g. `/chat`)** | 8 | 12 | 20 | Must link to every cluster page in its sub-product + use-cases + at least 1 customer story |
| **Use-case page (e.g. `/use-case/live-chat`)** | 3 | 5 | 8 | Must link to pillar, 1–2 sibling use-cases, 1 related glossary, 1 industry page, 1 customer story |
| **White-label page** | 5 | 7 | 10 | Must link to parent pillar + matching glossary definitional page + `/pricing` |
| **Industry page** | 5 | 8 | 12 | Must link to all 3 product pillars, 1–2 customer stories from industry, 1–2 use-cases, 1–2 glossary |
| **Blog post (< 1,000 words)** | 3 | 4 | 6 | At least 1 pillar or use-case link |
| **Blog post (1,000–2,000 words)** | 4 | 6 | 8 | Add 1 cross-link to a sibling blog post |
| **Blog post (2,000+ words)** | 5 | 8 | 12 | Full cluster hub behavior — link to pillar + 2 siblings + customer story + glossary |
| **AEO article (`/answers/*`) — short (< 1,000 words)** | 2 | 3 | 4 | Topical links only; customer-story links are a separate class (see §AEO related-answers) |
| **AEO article (`/answers/*`) — medium (1,000-1,500 words)** | 3 | 4 | 5 | Topical links only; customer-story links separate |
| **AEO article (`/answers/*`) — long (1,500+ words)** | 4 | 5 | 6 | Topical links only; customer-story links separate |
| **Glossary entry** | 2 | 3 | 5 | Must link to 1 product/use-case (commercial alt) + 1 sibling glossary + 1 pillar |
| **Customer story** | 3 | 5 | 7 | Must link to customer's industry page + product pillar(s) they use + 1 related use-case |
| **Product update / release note** | 2 | 3 | 5 | Link to the feature page being updated + `/product` + relevant use-case |
| **Webinar / event page** | 2 | 3 | 5 | Link to the pillar the topic matches + 1 blog post on the same topic |

**Enforcement:**
- Optimizer warns when a draft is below `Min` or above `Max`. Min is a floor (add links); Max is a ceiling (remove or consolidate).
- Link count excludes navigation, header, and footer — only counts in-content links.

---

## Anchor text distribution targets

Over-optimization is a site-wide risk (see the "social plus AI" cannibalization: 42 URLs ranking). Keep anchor distribution under these caps **site-wide** and within reason per-article.

| Anchor type | Share (site-wide) | Share (per article) | Examples |
|---|---|---|---|
| **Exact match** | ≤ 15% | ≤ 20% | "chat SDK" → `/chat/sdk` |
| **Partial match** | 35–45% | 30–50% | "our chat SDK gives you", "modern chat SDK for apps" |
| **Branded** | 15–20% | 10–25% | "social.plus analytics", "our chat infrastructure" |
| **Natural/contextual** | 20–30% | 20–35% | "as covered in this customer story", "in the moderation dashboard" |
| **Generic** | ≤ 5% | ≤ 10% (1 max in short posts) | "learn more", "read this", "see here" — only when surrounded by descriptive context |

**Never mix exact-match identical anchors within one article pointing to different pages** (the core cannibalization trap).

**Never repeat the same anchor-target pair more than twice in one article.** Use the per-cluster anchor variation pool (below) for additional links.

---

## Placement & avoidance rules

### Where internal links belong inside an article

Ranked by value and placement priority:

1. **Body paragraphs introducing a concept** (peak SEO + user value). The first 1–2 uses of a concept should link. Later mentions don't re-link.
2. **Lists where items have dedicated pages**. E.g., "key capabilities include [chat SDK], [social SDK], and [video SDK]" — each list item anchor points to its product page.
3. **After a pain point or problem statement** — link to the solution page. This is the highest-conversion placement.
4. **In the first 1–2 paragraphs** (high attention). One strategic link maximum.
5. **Mid-article** — most contextual links land here.
6. **Before a section break** — linking to a deeper dive of the preceding topic.

### Where internal links do **not** belong

- **AEO article FAQs, conclusions, and metrics tables** (already enforced in AEO section below).
- **Blog post conclusions / CTAs**. The final CTA goes to `/pricing` or a demo form — not a nested internal link.
- **Image captions** (rarely useful, often broken).
- **Footnotes** (no SEO value, often missed by crawlers).
- **Author bios** (should have branded home link only, nothing else).
- **More than 2 links in one paragraph** (feels spammy, dilutes each).
- **The same page linked more than twice in one article**, regardless of anchor variation.

### Good vs bad placement — worked examples

❌ **Bad (forced, generic, bottom-of-page):**

> If you want to build community features into your app, [click here](https://www.social.plus/social) to learn more.

✅ **Good (contextual, mid-body, descriptive):**

> Teams that need user profiles, groups, and activity feeds without building from scratch typically reach for an [in-app community SDK](https://www.social.plus/social/sdk) that bundles the data layer, moderation hooks, and UI components.

❌ **Bad (over-optimized, repeating exact match):**

> Our [chat SDK](https://www.social.plus/chat/sdk) is the best [chat SDK](https://www.social.plus/chat/sdk) for fintech apps — learn more about our [chat SDK](https://www.social.plus/chat/sdk).

✅ **Good (variation, descriptive, natural):**

> Our [chat SDK](https://www.social.plus/chat/sdk) is built for fintech apps. It ships with [compliance-ready moderation](https://www.social.plus/moderation) and plugs into the [React Native UIKit](https://www.social.plus/chat/uikit) when you want UI out of the box.

❌ **Bad (wrong intent routing — commercial anchor pointing to glossary):**

> Pitching a customer: "When you integrate our [chat API](https://www.social.plus/glossary/chat-api) you get…"

✅ **Good (commercial intent → commercial page):**

> When you integrate our [chat API](https://www.social.plus/chat/sdk) you get…

❌ **Bad (forbidden positioning term as anchor to product):**

> Build a [social network](https://www.social.plus/social) for your community.

✅ **Good (approved positioning):**

> Build an [in-app community](https://www.social.plus/social) for your users.

### Links to always avoid

- "Click here", "read more", "this", "here" as standalone anchors.
- Same anchor pointing to different pages within a single article.
- Repeating the same link more than twice.
- Linking to outdated content (check `metaTitle` for year references — flag pre-2024 posts).
- Linking to Webflow pagination query strings (`?*_page=N`) or RSS feeds.
- Linking to `/use-cases/*` (plural) — canonical is `/use-case/*` (singular). See Do-not-link list.

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

## Link-equity hubs & authority flow

When suggesting link **destinations** in draft mode, these are high-priority targets. When suggesting link **sources** in audit mode, these pages are also where outbound links matter most.

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

Notable absence: no in-scope product/feature page broke UR 4.0 at generation time. **This is a finding, not a bug** — product pages are commercial/short-tail and don't accumulate organic backlinks the way glossary/blog content does.

### Authority-flow rules (external → internal redistribution)

The glossary and blog collect backlinks; the product pages need the authority. Audit mode enforces:

| High-UR source | Required downstream links |
|---|---|
| `https://www.social.plus/` (UR 11.0) | Prominent nav/body links to all 3 pillars + `/pricing` + 1–2 customer stories |
| `https://www.social.plus/white-label/social-network` (UR 7.0) | Body links to `/social`, `/social/sdk`, `/social/features`, `/white-label/in-app-community`, `/moderation`, `/pricing` |
| `https://www.social.plus/glossary/social-feed` (UR 4.6) | Commercial-alternative link to `/use-case/activity-feed` + link to `/social` |
| `https://www.social.plus/glossary/community-app` (UR 4.5) | Link to `/social` + `/white-label/in-app-community` |
| `https://www.social.plus/glossary/video-sdk` (UR 4.5) | Commercial-alternative link to `/video/sdk` + `/video` |
| `https://www.social.plus/glossary/chat-api` (UR 4.4) | Commercial-alternative link to `/chat/sdk` + `/chat` |
| `https://www.social.plus/blog/what-is-community-based-marketing-cbm` (UR 4.4) | Links to `/social`, 2–3 sibling blog posts, 1 customer story |

**Audit rule:** If any of these source pages is missing its required downstream links, flag as a Priority 1 fix (biggest authority-flow gains per fix).

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

**Orphan priority tiers:**

| Tier | Criteria | Action |
|---|---|---|
| **P1 — critical** | Page has organic traffic AND 0 inbound contextual links | Add ≥ 3 inbound links from related pillar/use-case/blog within week 1 |
| **P2 — important** | Page has commercial intent but < 2 inbound contextual links | Add ≥ 2 inbound links within week 2 |
| **P3 — optional** | Page has no traffic and < 2 inbound links | Evaluate for consolidation, noindex, or deletion |

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

- **Topical link budget scales with article length** — ~1 per 300 words, with floor 2 and ceiling 6. Per-length-band Min/Target/Max in §"Link budgets by article type". Stricter than blog because AEO chunks need clean extraction.
- **Allowed link locations:** definition paragraph, "why it matters", architecture/features sections, step-by-step. **Disallowed:** FAQs, conclusion, metrics table.
- **Max 1 topical link per section** — prevents stacking multiple links inside one ~150-word chunk, which tanks that chunk's extraction quality.
- **Customer-story links are a separate class.** When an approved customer is named in the article, link the **first mention** of that customer's name to their `/customer-story/*` page. Subsequent mentions of the same customer stay plain text. Multiple customers can each get their own first-mention link. These links are **not counted toward the topical budget**; the 5-customer approved list is the de facto cap. Anchor = customer name (per `internal-linking-strategist/SKILL.md`).
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

## Reverse workflow — when a new page ships

Triggered when `pages-*.json` reports a new entry after a Webflow publish, or when the user explicitly asks "what should link to this new page?"

1. **Add canonical anchors.** Edit the canonical anchor map above to include the new anchor → target row.
2. **Identify inbound-link candidates.** Run this prioritized list:
   - Parent pillar (bidirectional link required).
   - Sibling cluster pages (within same pillar).
   - Related glossary entries (commercial-alt rule).
   - Industry pages, if the new page has industry affinity.
   - Top 3 blog posts whose headings reference the topic (grep the JSON).
   - Top 1–2 AEO articles on the same topic (for definitional cross-references).
3. **Draft inbound edits.** For each candidate, propose:
   - Source page URL
   - Insertion location (H2 section or paragraph anchor)
   - Anchor text (using canonical map + variation pool)
   - Why it fits
4. **Apply forbidden-pattern + placement checks** on each proposed edit.
5. **Schedule the implementation** in the next Webflow publish window.

### Stale content handling

When a blog post / page is confirmed outdated:

| State | Action |
|---|---|
| Outdated but historically traffic-earning | Rewrite + republish with same URL; add updated date |
| Outdated and zero traffic, topic covered elsewhere | 301 redirect to the best replacement; remove from canonical anchor map; audit inbound links and update anchors |
| Outdated and topic no longer relevant | Noindex, remove from canonical anchor map; prune inbound links |

---

## Scoring & measurement

### Structure Score /10

Computed site-wide in audit mode. Target: **≥ 8 / 10**.

| Criterion | Points |
|---|---|
| Orphan pages (0 = 3 pts; 1–3 = 2; 4–10 = 1; > 10 = 0) | 3 |
| Max click depth from homepage (all ≤ 3 clicks = 2 pts; some at 4 = 1; > 4 = 0) | 2 |
| Pillar → cluster coverage (all pillars link to 100% of their clusters = 2 pts; 80%+ = 1; < 80% = 0) | 2 |
| Cluster → pillar bidirectional coverage (all clusters link back = 1 pt) | 1 |
| Bridge-link coverage (each cross-cluster capability pillar linked from ≥ 5 cluster pages = 1 pt) | 1 |
| Industry-lattice coverage (every industry page links to all 3 product pillars = 1 pt) | 1 |

### Anchor Score /10

Computed site-wide in audit mode. Target: **≥ 8 / 10**.

| Criterion | Points |
|---|---|
| Exact-match share ≤ 15% site-wide (pass = 3 pts) | 3 |
| Generic share ≤ 5% site-wide (pass = 2 pts) | 2 |
| No same-anchor-to-different-targets within any article (pass = 2 pts) | 2 |
| All anchors descriptive (no "click here" bare) (pass = 2 pts) | 2 |
| Per-cluster anchor variation respected (no single anchor > 2 uses in one article) | 1 |

### Success metrics per fix type

Track these after each fix. Use as ROI signal for prioritization.

| Fix | Typical impact | Time to measure |
|---|---|---|
| Resolve P1 orphan (add ≥ 3 inbound links) | +15–30% traffic to that page | 2–4 weeks |
| Complete a pillar → cluster coverage gap | +10–25% traffic to new cluster pages | 4–8 weeks |
| Rebalance over-optimized anchor (exact-match reduction to ≤ 15%) | +5–10% ranking improvement for target keyword | 4–12 weeks |
| Consolidate a cannibalization cluster (e.g., "social plus AI" → `/analytics`) | +10–30% traffic consolidation to winning URL | 4–8 weeks |
| Redirect a do-not-link orphan (e.g., `/use-cases/*` plural) | Recovers lost clicks (42/90d in the known case) | Immediate |
| Bridge-link between pillars where intent overlaps | +5–15% traffic to the receiving pillar for cross-intent queries | 4–8 weeks |

### Monitoring cadence

| Cadence | Check | Source |
|---|---|---|
| **Weekly** | Broken internal links; new content linked within 48 h | Ahrefs site-audit or crawler |
| **Bi-weekly** | Orphan candidates from `pages-by-internal-links` (ascending) | Ahrefs site-explorer |
| **Monthly** | Anchor-text distribution drift vs targets; new cannibalization candidates | Ahrefs organic-keywords + GSC |
| **Monthly** | Cluster rank tracking for pillar keywords | Ahrefs rank-tracker |
| **Quarterly (90 days)** | Full refresh via the **Refresh procedure** at the bottom of this file | Multiple |
| **Annual** | Re-evaluate the architecture model — is hub-and-spoke still the right fit? | Stefan + data |

---

## Audit mode — phased implementation plan template

When audit mode runs, output this template. Phases are sequenced so each builds on the prior foundation.

```markdown
# Internal Linking Audit — social.plus

**Audit date:** YYYY-MM-DD
**Structure Score:** X / 10
**Anchor Score:** X / 10
**Estimated traffic impact of full plan:** +X% over 90 days

## Current state

| Metric | Current | Target | Gap |
|---|---|---|---|
| Structure Score | X | 8+ | X |
| Anchor Score | X | 8+ | X |
| Orphan pages (real) | X | 0 | X |
| Max click depth | X | ≤ 3 | X |
| Exact-match anchor share | X% | ≤ 15% | X |
| Generic anchor share | X% | ≤ 5% | X |
| Pillar → cluster coverage | X% | 100% | X |
| Cannibalization violations | X | 0 | X |

## Phase 1 — Critical fixes (Week 1)

### 1a. Resolve P1 orphans
- [ ] [URL] — add inbound from [3–5 specific source URLs with anchor text]
- [ ] [URL] — ...

### 1b. Fix cannibalization violations
- [ ] In [article URL], anchor "chat API" currently points to [X] — rewrite to [correct target] per rule
- [ ] ...

### 1c. Fix do-not-link targets in existing content
- [ ] Any occurrence of `/use-cases/temporary-live-1-1-chat` → replace with `/chat/sdk`

## Phase 2 — Pillar → cluster coverage (Week 2–3)

### 2a. Close pillar → cluster gaps
- [ ] `/chat` currently links to [N / M] cluster pages — add missing: [list]
- [ ] `/social` ...
- [ ] `/video` ...

### 2b. Close cluster → pillar gaps
- [ ] [Cluster URL] missing backlink to [Pillar URL]
- [ ] ...

### 2c. Authority-flow redistribution
- [ ] High-UR glossary page [URL] missing commercial-alt link to [product page]
- [ ] ...

## Phase 3 — Anchor optimization (Week 4+)

### 3a. Rebalance over-optimized anchors
- [ ] "chat SDK" exact-match currently X% — reduce to ≤ 15% by rewriting [N] instances to partial/natural variants
- [ ] ...

### 3b. Eliminate generic anchors
- [ ] Replace "click here" / "learn more" bare anchors: [N] occurrences
- [ ] ...

## Phase 4 — Industry lattice & bridge links (Week 5+)

- [ ] `/industry/edtech` under-linked — add inbound from [specific pages]
- [ ] `/use-case/events` missing bridge to `/video` — add contextual link
- [ ] ...

## Expected outcomes

| Phase | Effort | Traffic impact | Ranking impact |
|---|---|---|---|
| Phase 1 | ~8 h | +15–30% to fixed orphans | Within 2–4 wks |
| Phase 2 | ~16 h | +10–25% to cluster pages | Within 4–8 wks |
| Phase 3 | ~12 h | +5–10% ranking lift | Within 4–12 wks |
| Phase 4 | ~8 h | +5–15% on bridged intents | Within 4–8 wks |

## Tracking

Re-score Structure and Anchor monthly after implementation. Target Structure ≥ 8 and Anchor ≥ 8 within 90 days.
```

---

## Quality gates

### Input validation (before optimizer runs)

- [ ] If draft mode: draft content provided (URL or pasted text).
- [ ] If audit mode: the 10 `pages-*.json` snapshots are current (check `_meta.generatedAt` — warn if > 30 days old).
- [ ] If reverse mode: new page URL + its canonical anchor candidate provided.

### Output validation (before optimizer returns)

- [ ] Every proposed link cites its source rule (canonical map row / cannibalization warning / UR data / orphan tier).
- [ ] Link budget for the article type is respected (within Min / Max).
- [ ] Anchor distribution falls within per-article targets.
- [ ] No forbidden patterns present.
- [ ] No proposed target is on the do-not-link list.
- [ ] All anchors are descriptive (no bare "click here").
- [ ] No anchor repeated more than twice per article pointing to same target.
- [ ] No same anchor pointing to two different targets within one article.

### Evaluation questions — per-link quality gate

Before proposing any link, the optimizer must confirm:

1. **Would a reader genuinely click this?** If no, drop it.
2. **Is this the best target page given all candidates in the data?** If a higher-UR or more-aligned alternative exists, switch.
3. **Does the anchor match the target's primary keyword intent?** If not, pick a different anchor from the variation pool.
4. **Have I already linked to this page in this article?** If yes (≥ 2×), stop.
5. **Is the surrounding context definitional or commercial?** Route intent accordingly — don't cross-wire.
6. **Does this link add to the target's topical authority?** If it's orthogonal, drop it.
7. **Does placing this link violate any placement rule?** (In an FAQ, conclusion-of-AEO, caption, etc.)
8. **Is this anchor + target combination already near the article's link budget cap?** If so, prioritize the highest-value link and drop lower-value.

If any answer is "no" or "unclear", do not propose the link.

---

## Ownership & process

| Action | Owner | When |
|---|---|---|
| Publish new marketing page in Webflow | Content team | Ongoing |
| Regenerate `pages-*.json` snapshots | Webflow publish automation | On every publish |
| Add new page to canonical anchor map | Stefan | Within 48 h of publish, or optimizer flags gap |
| Run audit mode | Stefan (or scheduled agent) | Weekly for broken-link / orphan check; monthly for full audit |
| Refresh this file (90-day full refresh) | Stefan | Every 90 days per Refresh procedure |
| Resolve cannibalization warning during drafting | Content author + this file | At draft time — writer follows rule; if ambiguous, ask Stefan |
| Approve new customer story references | Stefan per `messaging/terminology.md` | At draft time |
| Escalate DR drift > ±5 | Optimizer → Stefan | On refresh |

**Escalation triggers (optimizer → human):**
- A draft violates a cannibalization rule but the writer insists the commercial framing is correct.
- A new page's canonical anchor conflicts with an existing anchor (would create cannibalization).
- `pages-*.json` itemCount jumps by > 10% between publishes (signal of CMS migration or bulk-import — needs review).
- DR drops by > 5 points since last refresh.

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
6. **Re-score Structure and Anchor** against the rubric — compare to last refresh to spot regressions.
7. **Review pillar → cluster map** for new pages that belong in it.
8. **Update link-equity hubs** if any new URL broke UR 4.0.

Update the `Generated:` and `Refresh by:` dates at the top.
