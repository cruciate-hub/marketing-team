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

## Ecosystem hyperlinks

Ecosystem hyperlinks are a distinct link class from external citations. Citations support a specific claim. Ecosystem links let the reader go deeper on a concept, standard, or tool mentioned in the article.

Target count per article: **3-5**. Place in body sections (definition chunk, architecture/features, best-practices). Never in FAQs, conclusion, or pitch.

### Curated approved domains by category

**Web standards and protocols**
- `developer.mozilla.org` — Web APIs, push notifications, service workers, IndexedDB, WebSocket; neutral and educational, no product pitch
- `w3.org` / `w3.org/TR/WCAG22` — HTML, CSS, WebPush, Web Notifications, accessibility specs (WCAG); canonical authority for web standards
- `rfc-editor.org` — IETF RFCs; link specific RFC numbers (e.g., RFC 6455 for WebSocket, RFC 4287 for Atom feeds)

**Mobile platform documentation**
- `developer.apple.com` — iOS SDK, UserNotifications framework, Sign in with Apple; official Apple authority
- `developer.apple.com/design` (Apple HIG) — Human Interface Guidelines for iOS notification UX, accessibility, UI patterns
- `developer.android.com` — Android SDK, WorkManager, Firebase Cloud Messaging; official Google authority
- `m3.material.io` (Material Design 3) — notification UX patterns, engagement UI components, accessibility, dark mode

**UX and product design research**
- `nngroup.com` — Nielsen Norman Group; peer-reviewed UX research on engagement, notification patterns, community design; highest weight for UX claims
- `baymard.com` — Baymard Institute; e-commerce and app UX research with disclosed methodology
- `smashingmagazine.com` — independent web design; long-form UX articles on push notification patterns, real-time interaction, accessibility

**Accessibility**
- `a11yproject.com` — community-led WCAG guidance; practical and non-commercial
- `deque.com/blog` — Deque Systems; accessibility consulting research; WCAG compliance and inclusive design
- `section508.gov` — U.S. government accessibility compliance standards; authoritative for legal obligations

**Academic and peer-reviewed research**
- `arxiv.org` — CS, HCI, networking preprints; link to specific papers with DOI; verify the paper is from CS/HCI domain
- `dl.acm.org` — ACM Digital Library; CHI and CSCW conference papers on social software, moderation, feed algorithms; highest academic weight for community/engagement claims

**Industry analysts and market data**
- `pew.org` (Pew Research Center) — longitudinal studies on social media adoption, mobile usage, trust in platforms; government-funded, disclosed methodology
- `statista.com` — aggregated market data; cite when you have verified access (many stats are paywalled)
- `gartner.com` — analyst reports; link to published blog summaries or press releases, not gated Magic Quadrant content
- `forrester.com` — analyst reports; same rule as Gartner; useful for community engagement benchmarking

**Privacy and compliance**
- `iapp.org` (IAPP) — zero-party data, GDPR in community platforms, user consent; gold standard for privacy compliance
- `owasp.org` — content moderation security, API security, authorization in community features; canonical security authority
- `gdpr.eu` — GDPR text and guidance; for data retention, consent, and privacy-by-design claims
- `nist.gov` — security frameworks, threat modeling, incident response; for security and compliance claims

**Community research and strategy**
- `cmxhub.com` (CMX Hub) — community management benchmark studies, engagement metrics; the industry's primary research body for community professionals
- `feverbee.com/blog` — Richard Millington's community strategy research; foundational for community design, moderation hiring, community ROI; cite blog articles, not service pages
- `reforge.com/blog` — product management and growth education; retention mechanics, engagement loops, lifecycle marketing; well-researched frameworks, not opinion

**Analytics and measurement**
- `amplitude.com/blog` — engagement metrics definitions, user behavior patterns, product analytics frameworks; cite research articles, not product pages
- `mixpanel.com/blog` — event-driven metrics, user cohort analysis, engagement scoring; same rule
- `appsflyer.com/blog` — mobile measurement, app retention benchmarks, fraud prevention; cite their published reports

**App market intelligence**
- `sensortower.com/blog` — app category benchmarks, retention by category, downloads and revenue statistics
- `data.ai/blog` (data.ai, formerly App Annie) — app market data; MAU trends, engagement by category

**Privacy advocacy**
- `blog.mozilla.org` — privacy-by-design, notification privacy, data protection, browser security standards; non-commercial and authoritative

### Competitor domains — never link to these

| Domain | Competitor category |
|---|---|
| getstream.io | In-app activity feeds and chat (direct competitor) |
| sendbird.com | In-app chat and messaging (direct competitor) |
| pubnub.com | Real-time messaging infrastructure (direct competitor) |
| cometchat.com | In-app chat (direct competitor) |
| pusher.com | Real-time messaging (direct competitor) |
| ably.com | Real-time messaging (direct competitor) |
| twilio.com | Messaging infrastructure (competing on chat use cases) |
| vonage.com | Messaging APIs (competing on messaging use cases) |
| circle.so | Community platform (direct competitor) |
| mighty.social / mightynetworks.com | Community platform (direct competitor) |
| tribe.so | Community platform (direct competitor) |
| commsor.com | Community engagement analytics (direct competitor) |
| hivebrite.com | Community platform (direct competitor) |
| discord.com | Community chat and engagement (competing on community use cases) |
| slack.com | Workspace communication (competing on community use cases) |

### Per-topic link targets

| Article topic | Best ecosystem targets |
|---|---|
| In-app activity feeds (definition) | developer.mozilla.org, nngroup.com, arxiv.org |
| In-app chat / messaging | developer.mozilla.org (WebSocket), rfc-editor.org (RFC 6455), iapp.org |
| Push notifications | developer.apple.com, developer.android.com, nngroup.com |
| Community engagement and retention | cmxhub.com, feverbee.com/blog, pew.org |
| Content moderation | owasp.org, iapp.org, dl.acm.org |
| Zero-party data | iapp.org, gdpr.eu, pew.org |
| User engagement metrics | amplitude.com/blog, mixpanel.com/blog, nngroup.com |
| Notification UX best practices | nngroup.com, m3.material.io, developer.apple.com/design |
| Accessible community features | a11yproject.com, w3.org/TR/WCAG22, deque.com/blog |
| Mobile community SDKs | developer.apple.com, developer.android.com, w3.org |

## Pre-flight

Before running compliance, eyeball the article against this list (intent-aware):

- [ ] Intent-appropriate citation count: definition ≥2, comparative ≥3, procedural as-needed
- [ ] Every numeric claim has a source (approved list or external link)
- [ ] The TL;DR paragraph carries at least one citation or statistic (definition / comparative)
- [ ] FAQ, conclusion, pitch, and metrics table are citation-free
- [ ] No anonymous, content-farm, or competitor-marketing citations
- [ ] Every approved-customer mention matches the approved-stat list exactly
- [ ] 3-5 ecosystem hyperlinks placed in body sections (not FAQs, conclusion, or pitch)
- [ ] No ecosystem link points to a domain in the competitor exclusion list
