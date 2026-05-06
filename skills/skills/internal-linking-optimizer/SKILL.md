---
name: internal-linking-optimizer
description: >
  Optimize internal linking for social.plus content. Two modes: (1) Draft mode
  suggests inline link targets and anchor text for a specific piece of new
  content (typically invoked by blog-seo-content, aeo-content, or other writing
  skills before delivery). (2) Audit mode runs a site-wide internal linking
  analysis across all 10 pages-*.json data files (646 total pages: marketing,
  use-cases, industry, glossary, blog, customer-stories, answers, product-updates,
  release-notes, webinars). Use this skill when someone asks to "audit internal
  linking", "check anchor text", "fix orphan pages", "internal link audit",
  "linking strategy", or "where should this article link to". Also invoke this
  skill from other content-writing skills as a pre-delivery step to attach
  SEO-grounded link suggestions to a draft. Do NOT trigger when the user is just
  writing content without a linking question — let the writing skill invoke this
  one. Do NOT use for backlink/external link work (use backlink-placement-finder
  or link-building-vetter).
---

# social.plus Internal Linking Optimizer

This skill produces SEO-grounded internal link recommendations for social.plus content. It runs in two modes:

- **Draft mode** — given a specific draft (blog post, AEO article, or other), returns a ranked list of suggested links (anchor text + target URL + insertion point + reasoning). This is the mode `blog-seo-content` and `aeo-content` invoke as a pre-delivery step.
- **Audit mode** — given no specific draft, runs a 7-step site-wide audit using the `pages-*.json` data files and `link-strategy.md`, returns a prioritized fix plan.

Every recommendation is grounded in `link-strategy.md` (canonical anchor map, cannibalization warnings, hub pages, anchor variation rules), regenerated quarterly from Ahrefs and GSC data.

## Architecture: two-phase shortlist + live fetch

The `pages-*.json` files are intentionally a **lightweight heading index** — full H1-H6 plus metaTitle and metaDescription, no body. Body content lives on the live web. This keeps snapshots small and the auto-regen cheap.

**Trade-off:** heading-only data isn't enough to confidently pick an insertion point or quote surrounding context. So the optimizer always runs in two phases:

1. **Phase 1 — Shortlist (from JSON).** Scan the headings + metadata in the relevant `pages-*.json` files to identify candidate link targets. Cheap, fast, no network beyond the GitHub fetches.
2. **Phase 2 — Verify + extract (live WebFetch).** For the top N shortlisted candidates only, fetch the live page. Use the fresh body to confirm the topic match, find the specific insertion sentence, and quote the surrounding context.

**Live-fetch budget:**
- Draft mode: at most **one WebFetch per shortlisted candidate**, capped at **8 candidates per draft** (so ≤8 live fetches per invocation). If the shortlist returns more than 8 strong candidates, take the top 8 by score.
- Audit mode: live fetch is reserved for the **top 5-10 highest-impact gaps** in the implementation plan. The rest of the audit is JSON-only.
- **If the calling context overrides the cap** (e.g., explicit "use only 4 fetches"), re-shortlist from scratch by score down to that lower N. Do not just slice the top N off an existing 8-item list — the candidate ranking should reflect the actual budget, since a tighter budget changes which candidates are worth verifying.

**Why this works even when the JSON is sparse:** known limitations of the snapshot generator (e.g., the static-page extractor can't reach Webflow Components, so industry pages capture only the headings outside components) are compensated by the Phase 2 live fetch — the live page sees everything.

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

## Step 0: Fetch the main brain

Fetch `brain.md` for cross-domain routing, precedence rules, and the compliance check.

If the fetch fails, proceed with the link suggestions but append this notice at the end of your output: "⚠️ brain.md was unreachable — the compliance check (terminology, tone, claims, em-dashes, emojis) was not applied. The calling skill should run its own compliance pass before publishing." Linking decisions don't depend on brain.md, so a missing brain.md is a soft failure, not a stop condition.

## Step 1: Determine which data files to fetch

Always fetch `website/link-strategy.md`. Then pick `pages-*.json` files based on context:

| Calling context | Files to fetch |
|---|---|
| Called by `blog-seo-content` (draft mode) | `pages-marketing.json`, `pages-use-cases.json`, `pages-industry.json`, `pages-glossary.json`, `pages-blog.json`, `pages-customer-stories.json` |
| Called by `aeo-content` (draft mode) | `pages-marketing.json`, `pages-use-cases.json`, `pages-glossary.json`, `pages-answers.json`, `pages-customer-stories.json` |
| Standalone draft mode (user-pasted content) | `pages-marketing.json`, `pages-use-cases.json`, `pages-industry.json`, `pages-glossary.json` (default — ask if blog/customer-stories/answers should also be considered) |
| Audit mode | All 10 files: `pages-marketing.json`, `pages-use-cases.json`, `pages-industry.json`, `pages-glossary.json`, `pages-blog.json`, `pages-customer-stories.json`, `pages-answers.json`, `pages-product-updates.json`, `pages-release-notes.json`, `pages-webinars.json` |

Run all fetches in parallel via the canonical fetch block at the top of this file. Files live under `website/` (e.g. `website/link-strategy.md`, `website/pages-marketing.json`).

If `link-strategy.md` is missing or its `Refresh by:` date is in the past, surface this to the user before continuing. Stale strategy beats no strategy, but the user should know.

### File contents

Each `pages-*.json` has shape `{"_meta": {...}, "pages": [{"url", "metaTitle", "metaDescription", "content"}, ...]}`. URLs are full `https://www.social.plus/...`. Because `curl` returns raw JSON, parse directly with `json.loads(content)` — no HTML extraction needed.

## Step 2: Determine mode

- **Draft mode** — A draft (title + body + target keyword) is present in the invocation context. Either passed by a calling skill, or supplied directly by the user with a request like "suggest internal links for this article".
- **Audit mode** — No specific draft present. The user asked for a site-wide check, an orphan analysis, an anchor text audit, or similar.

If genuinely ambiguous, ask the user. Do not assume.

---

## Mode: Draft

**When:** A draft is in context. Calling skill passed it, or user pasted it.

### Workflow

**1. Identify the draft's target keyword and topic cluster.**

The calling skill should pass the target keyword. If not, infer from the draft's H1 / page title. Map to one of the clusters defined in `link-strategy.md` (Brand / Chat / Social / Video / Industry / Cross-cluster).

**2. Cross-reference cannibalization warnings.**

Scan the draft for any phrase that matches a cannibalization-warning anchor in `link-strategy.md`. For each match:
- Determine intent (definitional vs commercial) from the surrounding sentence.
- Note the canonical target per the warning's rule.
- If the draft *itself* targets a cannibalized term as its primary keyword, flag this **before** proposing links — the article may compete with existing pages and the user should know.

**3a. Phase 1 — Shortlist candidate target pages from JSON.**

For each page in the fetched JSON files, score topic relevance against the draft:
- Match draft headings, key terms, and target keyword against each page's `metaTitle`, `metaDescription`, and heading hierarchy in `content`.
- Apply the canonical anchor map: if a draft sentence is reaching for an anchor that has a canonical target in `link-strategy.md`, that target is a strong candidate.
- Filter by intent fit (definitional anchor → glossary; commercial anchor → product/use-case page).

Rank candidates and **take the top 8 maximum** (the live-fetch budget). Quality over quantity — if only 3 candidates are clearly relevant, only shortlist 3.

**3b. Phase 2 — Live-fetch verification and insertion-point extraction.**

For each shortlisted candidate, WebFetch the live page (URL from the JSON's `url` field — already a full `https://www.social.plus/...`). Then for each page, ask the fetched content:
- Does the topic match still hold? (The live page may have changed since the JSON snapshot.)
- Where in the *draft* would a link to this page make the most sense? Identify the specific sentence or paragraph.
- What surrounding context from the live page confirms it's the right destination?

If a candidate doesn't pan out on live verification, drop it. If you discover a stronger target during live exploration that wasn't in the original shortlist, you may add it (subject to the 8-fetch budget).

**3c. Score and rank final suggestions.**

For each surviving candidate:
- **Contextual relevance** (does the surrounding sentence's meaning match the target page's topic?)
- **Canonical-anchor compliance** (does the suggested anchor match the canonical map in `link-strategy.md`?)
- **Link-equity benefit** (is the target a hub page or under-linked priority page per `link-strategy.md`?)
- **Anchor variety** (have we already used this anchor in the draft?)
- **Intent fit** (definitional anchor → glossary; commercial anchor → product/use-case page)

**4. Apply the link budget for the article's type.**

The draft's article type determines the Min / Target / Max link count. Look up the type in `link-strategy.md` §"Link budgets by article type" (14 types: marketing/product page, pillar landing, use-case page, white-label, industry, blog by length band, AEO, glossary entry, customer story, product update, webinar).

If the count falls below **Min**, add links until it reaches Target. If it exceeds **Max**, drop the weakest candidates until it reaches Target. For AEO, the table also constrains placement (disallowed in FAQs, conclusion, metrics table) — enforce both count and placement rules.

Link count excludes header, footer, and nav. Only in-content links count.

Quality over quantity. Better to return 3 strong suggestions at the floor than 7 weak ones at the ceiling.

**5. Apply anchor-text distribution targets + per-cluster variation rules.**

Two constraints run simultaneously:

- **Per-article anchor distribution** — match the per-article proportions in `link-strategy.md` §"Anchor text distribution targets": exact-match ≤ 20%, partial 30–50%, branded 10–25%, natural 20–35%, generic ≤ 10% (and at most 1 in short posts). Count proposed anchors across all your suggestions and reject combinations that overweight exact-match or generic.
- **Per-cluster variation** — if the same anchor would point to the same page more than twice in the draft, use a variant from the cluster's anchor pool in `link-strategy.md` §"Per-cluster anchor variation rules".

Also forbidden: using the same anchor text pointing to two different targets within one draft (cannibalization trap). Reject any suggestion combination that would do this.

**6. Run the 8 evaluation questions + placement check before finalizing.**

For each proposed link, run through the 8 evaluation questions from `link-strategy.md` §"Evaluation questions — per-link quality gate". If any answer is "no" or "unclear", drop the suggestion.

Then run the placement check from `link-strategy.md` §"Placement & avoidance rules" — reject any suggestion placed in a forbidden location (AEO FAQ/conclusion/metrics table, blog conclusion CTA, image caption, footnote, author bio, or a paragraph already containing 2 other links).

Finally, check every suggested target against `link-strategy.md` §"Do-not-link list" — if a target URL is on that list, drop it and surface the issue to the writer (e.g., `/use-cases/*` plural URLs).

This is the final quality gate. Only links that pass this step appear in the output.

### Draft mode output format

Return a clearly-labeled section the calling skill can embed in its own output. Match the format to the consuming content type:

- For **blog content** (HTML output from `blog-seo-content`): provide ready-to-paste `<a href="..." target="_blank">anchor</a>` tags.
- For **AEO content** (markdown output from `aeo-content`): provide markdown links `[anchor](URL)` only.
- For **generic drafts**: provide both formats.

```
## Internal link suggestions

**Mode:** Draft (target keyword: "[keyword]", clusters: [primary cluster — list multiple if applicable, e.g., "Chat + Industry"], content type: [blog/AEO/generic])

### Cannibalization check
Use exactly one of these three states:
- ⚠️ **Fired:** This draft uses "[anchor term]" in [definitional/commercial] intent. Per link-strategy.md, route to [target URL]. [Specific recommendation.]
- ℹ️ **Informational (non-firing):** This draft uses "[anchor term]" which has a known cannibalization split. Confirming the article is on the [definitional/commercial] side — no action needed.
- ✅ **Clean:** No cannibalization risks detected.

### Suggested links

1. **Anchor:** "[keyword-only anchor text — no surrounding articles like 'a' or 'the']"
   **Target:** [full URL]
   **Insert at:** "[exact verbatim quote of the draft sentence where the link goes]"
   **Rephrase suggestion:** "[rewritten sentence with anchor inline — OMIT THIS FIELD ENTIRELY if the original sentence accommodates the anchor cleanly without rewording]"
   **Format:** `<a href="[URL]" target="_blank">[anchor text]</a>` OR `[[anchor text]]([URL])`
   **Reasoning:** [why this link, in 1 sentence — cite link-strategy.md row if a canonical match]

2. ...

[3-7 for blog topical, 2-6 for AEO topical (scaled by length per `link-strategy.md`), plus customer-story links when approved customers are named]

### Notes for the writer

Include only the bullets that apply to the current draft; OMIT any that don't.

- **Cluster anchor variation applied:** [describe any variants used to avoid same-anchor-twice]
- **Out-of-canonical-map targets used:** [list with rationale — e.g., long-tail blog or glossary pages not in the canonical map]
- **AEO section restrictions surfaced:** [include only when content type is AEO — note any suggestions dropped because they fell in disallowed sections like FAQs, conclusion, metrics table]
- **Skipped suggestions:** [optional — note candidates you considered but cut, with one-line reason]
```

The calling skill is responsible for embedding these into its final output. This skill does not edit the draft directly.

---

## Mode: Audit

**When:** No draft present. User asked for a site-wide linking analysis.

### Workflow

Run all 7 steps in order. Use the fetched `pages-*.json` files as the source of truth for what each page contains; use `link-strategy.md` as ground truth for canonical decisions.

**1. Link structure analysis.**

For each page across all 10 data files, count the internal links present in its `content` field. Build a distribution table per file.

```markdown
## Link structure overview

**Pages analyzed:** 646 (across 10 pages-*.json files)
**Total internal links:** [count]
**Average outbound links per page:** [count]

### Distribution by file

| File | Page count | Avg outbound links | Min | Max |
|---|---|---|---|---|
| pages-marketing | 22 | [n] | [n] | [n] |
| pages-use-cases | 11 | [n] | [n] | [n] |
| pages-industry | 10 | [n] | [n] | [n] |
| pages-glossary | 76 | [n] | [n] | [n] |
| pages-blog | 248 | [n] | [n] | [n] |
| pages-customer-stories | 42 | [n] | [n] | [n] |
| pages-answers | 123 | [n] | [n] | [n] |
| pages-product-updates | 58 | [n] | [n] | [n] |
| pages-release-notes | 31 | [n] | [n] | [n] |
| pages-webinars | 25 | [n] | [n] | [n] |

### Structure Score

Compute per the rubric in `link-strategy.md` §"Scoring & measurement" → "Structure Score /10". Output as a single number plus per-criterion breakdown:

| Criterion | Max | Actual |
|---|---|---|
| Orphan pages (0=3, 1-3=2, 4-10=1, >10=0) | 3 | [n] |
| Max click depth (≤3=2, 4=1, >4=0) | 2 | [n] |
| Pillar → cluster coverage (100%=2, 80%+=1, <80%=0) | 2 | [n] |
| Cluster → pillar bidirectional | 1 | [n] |
| Bridge-link coverage | 1 | [n] |
| Industry-lattice coverage | 1 | [n] |
| **Total** | **10** | **[score]** |

Target: ≥ 8 / 10. Compare to last audit if available.
```

**2. Orphan and under-linked pages (classified by tier).**

Cross-reference Ahrefs orphan candidates from `link-strategy.md` against the fetched data. Flag pages with no contextual inbound links from other pages in the data set (header/footer nav doesn't count for SEO purposes). Classify each flagged page per `link-strategy.md` §"Orphan priority tiers":

- **P1 — critical:** has organic traffic AND 0 inbound contextual links. Fix in week 1.
- **P2 — important:** has commercial intent but < 2 inbound contextual links. Fix in week 2.
- **P3 — optional:** no traffic and < 2 inbound. Evaluate for consolidation, noindex, or deletion.

```markdown
## Orphans and under-linked pages

### P1 — critical (week 1)
- **[full URL]** ([file]) — Currently linked from: [list, or "no contextual inbound"]. Should be linked from: [≥3 source URLs with reasoning + suggested anchors].

### P2 — important (week 2)
- **[full URL]** ([file]) — Currently linked from: [list]. Should be linked from: [≥2 source URLs with reasoning + suggested anchors].

### P3 — optional (evaluate for pruning)
- **[full URL]** ([file]) — Assessment: [consolidate into X / noindex / delete / leave as-is].
```

**3. Anchor text distribution + canonical compliance.**

Extract every anchor used across all pages. Cross-reference against the canonical anchor map. Flag:
- Generic anchors ("click here", "read more", "learn more")
- Anchors that violate the canonical map
- Same anchor pointing to multiple targets
- Definitional vs commercial intent violations (e.g., "social feed" anchor pointing to a product page when it should point to glossary)

```markdown
## Anchor text audit

### Generic anchors found
| Anchor | Count | Pages | Recommendation |
|---|---|---|---|

### Canonical map violations
| Anchor | Currently links to | Should link to | Pages affected |
|---|---|---|---|

### Anchor-to-target conflicts
| Anchor | Targets used | Recommendation |
|---|---|---|

### Definitional vs commercial intent violations
| Anchor | Page (source) | Current target (intent mismatch) | Recommended target |
|---|---|---|---|

### Anchor Score

Compute per the rubric in `link-strategy.md` §"Scoring & measurement" → "Anchor Score /10":

| Criterion | Max | Actual |
|---|---|---|
| Exact-match share ≤ 15% site-wide | 3 | [n] |
| Generic share ≤ 5% site-wide | 2 | [n] |
| No same-anchor-to-different-targets in any article | 2 | [n] |
| All anchors descriptive (no bare "click here") | 2 | [n] |
| Per-cluster anchor variation respected | 1 | [n] |
| **Total** | **10** | **[score]** |

Report site-wide percentages for exact-match and generic shares — these are the most actionable data points.
```

**4. Topic cluster analysis.**

For each cluster (Chat, Social, Video, Industry, Cross), check:
- Do pillar pages (`/chat`, `/social`, `/video`) link to all their cluster children?
- Do cluster children link back to the pillar?
- Are siblings cross-linked where contextually relevant?
- For blog: are blog posts in the same topic cluster cross-linking to each other and to the relevant pillar?

```markdown
## Topic cluster analysis

### Chat cluster
- Pillar: /chat
- Marketing children: /chat/features, /chat/sdk, /chat/uikit, /white-label/chat-software
- Use-case children: /use-case/live-chat, /use-case/group-chat, /use-case/1-1-chat
- Glossary support: /glossary/chat-api, /glossary/chat-widget, /glossary/chat-channel, /glossary/white-label-chat
- Blog cluster (top related posts): [list from pages-blog.json]
- ✅/❌ Pillar → all marketing children: [findings]
- ✅/❌ All children → pillar: [findings]
- ✅/❌ Sibling cross-links: [findings]
- ✅/❌ Blog → cluster pillar: [findings]

[Repeat for Social, Video, Industry]
```

**4b. Authority-flow redistribution check.**

Apply the rules in `link-strategy.md` §"Link-equity hubs & authority flow" → "Authority-flow rules (external → internal redistribution)". For each high-UR source page (homepage UR 11.0, `/white-label/social-network` UR 7.0, and the UR 4.4+ glossary/blog pages), verify the required downstream links are in place. Flag any missing downstream link as a **Priority 1** fix — these are the highest-leverage wins because they redirect accumulated external link equity toward commercial pages.

```markdown
## Authority-flow gaps (Priority 1)

| Source page (UR) | Required downstream | Currently linked? | Action |
|---|---|---|---|
| `https://www.social.plus/` (11.0) | 3 pillars, /pricing, 1–2 customer stories | [yes/no per target] | [add links with anchors] |
| `https://www.social.plus/white-label/social-network` (7.0) | /social, /social/sdk, /social/features, /white-label/in-app-community, /moderation, /pricing | ... | ... |
| `https://www.social.plus/glossary/social-feed` (4.6) | /use-case/activity-feed (commercial alt), /social | ... | ... |
| [etc. per the rule table in link-strategy.md] | | | |
```

**5. Contextual link gaps.**

Find places where one page mentions a concept that has its own dedicated page but doesn't link to it. This is the most actionable kind of internal linking work.

Use the two-phase pattern here too:
- **Phase 1 (JSON):** scan headings + meta to identify candidate gaps (page A's heading mentions a concept that page B owns canonically).
- **Phase 2 (live fetch):** for the top 5-10 most-likely gaps, WebFetch both the source page and the target page. Confirm the gap is real (the source's body doesn't already link to the target — JSON only sees headings, so the body might already have the link). Quote the specific sentence where the link should go.

```markdown
## Contextual link gaps

[For each:]
- **[source URL]** ([file]) — mentions "[concept]" in [section] but doesn't link to [target URL] (its canonical target).
  Suggested anchor: "[anchor]"
  Suggested insertion point: [quoted sentence from live page]
  Verified live: [date]
```

**6. Cluster-specific reviews.**

- **AEO articles:** are they over-linked (more than 3 internal links)? Are links in disallowed sections (FAQs, conclusion)?
- **Customer stories:** are they linked from the matching `/industry/*` page?
- **Glossary entries:** are they cited from blog/AEO content where the term is used definitionally?
- **Blog posts:** are pillar/hub posts receiving inbound links from cluster posts?

```markdown
## Cluster-specific findings

### AEO over-linking
| Article | Link count | Disallowed sections |
|---|---|---|

### Industry pages → customer stories
| Industry page | Stories from this industry | Currently linked? |
|---|---|---|

### Glossary citation gaps
| Glossary term | Pages mentioning the term but not linking | Recommended source pages to add link |
|---|---|---|

### Blog cluster cohesion
| Hub blog post | Related posts | Linking back? |
|---|---|---|
```

**7. Prioritized implementation plan.**

Synthesize all findings using the 4-phase template in `link-strategy.md` §"Audit mode — phased implementation plan template". Fill in the actual numbers from steps 1–6: Structure Score and Anchor Score (current vs target), orphan counts by tier, cannibalization violations, pillar → cluster gaps, authority-flow gaps, and over-optimization data.

Include the expected-outcomes table from the template (effort hours + typical traffic/ranking impact + time-to-measure) so the user can prioritize by ROI. Pull those numbers from `link-strategy.md` §"Success metrics per fix type".

### Monitoring cadence (include in plan)

Per `link-strategy.md` §"Monitoring cadence":

- **Weekly:** broken internal links, new content linked within 48 h.
- **Bi-weekly:** orphan candidates via Ahrefs `pages-by-internal-links`.
- **Monthly:** anchor distribution drift vs targets + new cannibalization candidates + cluster rank tracking.
- **Quarterly (90 days):** full refresh via `link-strategy.md` §"Refresh procedure".

Re-score Structure and Anchor monthly after implementation starts. Target ≥ 8 / 10 on both within 90 days.

### Audit mode "While looking at this..."

After the 7-step audit, always add a "While looking at this..." section with 2-3 observations the user didn't ask for but would want to know. This is the same pattern as `site-intelligence`. Be specific, quotable, actionable.

```markdown
## While looking at this...

- [Observation 1: connection across pages, missed opportunity, or pattern worth flagging]
- [Observation 2: ...]
- [Observation 3: ...]
```

---

## Mode: Reverse

**When:** A new page just shipped in Webflow (detected by a `_meta.itemCount` change in a `pages-*.json` between publishes, or flagged by the user with "what should link to this new page?").

### Workflow

**1. Add canonical anchors to `link-strategy.md`.**

Edit the canonical anchor map to include a row for each new page: `anchor term(s) → target URL`. Pick the anchor(s) from the new page's H1, metaTitle, and target keyword. If the anchor conflicts with an existing canonical entry (would create cannibalization), stop and escalate to Stefan per the escalation-triggers list — don't add both.

**2. Identify inbound-link candidates (prioritized).**

For the new page, grep the 10 `pages-*.json` files and optionally live-fetch to find 3–10 existing pages that should link *to* the new page:

- Parent pillar (bidirectional link required).
- Sibling cluster pages within the same pillar.
- Related glossary entries (apply the commercial-alt / definitional split rule).
- Industry pages, if the new page has industry affinity.
- Top 3 blog posts whose headings reference the topic.
- Top 1–2 AEO articles on the same topic (for definitional cross-references).

Rank by link-equity benefit (higher-UR sources first).

**3. Draft inbound edits.**

For each candidate source page, propose:

- Source page URL
- Insertion location (H2 section or specific paragraph anchor)
- Anchor text (from canonical map + cluster variation pool)
- Why it fits (cite the rule or data point)

**4. Run the quality gates.**

Apply the placement check, forbidden-pattern check, do-not-link-list check, and the 8 evaluation questions from `link-strategy.md` §"Quality gates" to each proposed edit.

**5. Output a ready-to-implement edit list.**

```markdown
## Inbound links to add for [new page URL]

**Canonical anchor row to add to link-strategy.md:**
- Anchors: "[term 1]", "[term 2]"
- Target: [new page URL]
- Cluster: [Chat / Social / Video / Cross / Industry]

### Proposed inbound edits

1. **From:** [source URL]
   **Section/anchor point:** [H2 name + quoted sentence]
   **Anchor text:** "[anchor]"
   **Why:** [rule citation]

2. [...]
```

Typical output: 3–10 inbound edits for a new product/use-case page, 2–4 for a new blog post, 1–3 for a new glossary entry.

---

## General principles (all modes)

**Quote, don't paraphrase.** When citing page content, quote it exactly. For headings or metadata, the JSON is the source. For body sentences (e.g., insertion-point context), you must have live-fetched the page first — never quote body content from memory or speculation.

**Be specific about locations.** Don't say "link from the chat page". Say "in `https://www.social.plus/chat`, under the `## Real-time messaging` section, after the existing paragraph about typing indicators, anchor 'in-app chat' to..."

**Anchor text is keyword-only.** The anchor must be the exact natural keyword phrase from `link-strategy.md`'s canonical map (e.g., "chat widget", "in-app chat"), not a surrounding-article variant ("a chat widget", "the in-app chat"). SEO weight flows to the linked phrase; articles dilute it. The "Insert at" field of a suggestion quotes the draft sentence verbatim; if the draft's natural phrasing prevents a clean keyword anchor, use the **Rephrase suggestion** field to propose a rewrite — don't compromise on the anchor.

**Respect the canonical map strictly.** If `link-strategy.md` says anchor X → page Y, that's the rule. If you think it's wrong, surface that as a flag for the user to update `link-strategy.md` — don't silently override.

**Definitional vs commercial intent matters.** A glossary anchor in product-pitch context is wrong. A product anchor in a definition paragraph is wrong. Match intent to target.

**Customer-story anchors use the customer name.** When suggesting a `/customer-story/*` link, the anchor must be the customer name (e.g., "Bitazza", "Noom"), not a proof-point claim or industry framing. Customer stories are case-study citations — name-anchored is the convention readers expect.

**Don't over-link.** Targets per content type:
- Blog: 3-7
- AEO topical links: scaled by length — ~1 per 300 words (floor 2, ceiling 6). See `link-strategy.md` §"Link budgets by article type" for per-length-band Min/Target/Max.
- AEO customer-story links: separate class, **not counted toward the topical budget**. First mention of an approved customer becomes a `/customer-story/*` link; subsequent mentions of the same customer stay plain text. Multiple customers can each get their own first-mention link. The 5-customer approved list is the de facto cap.
- Generic: 3-5

**No same-anchor-twice-to-same-target in one piece.** Use cluster anchor variants from `link-strategy.md`.

**Use full https URLs.** All `pages-*.json` URLs are full `https://www.social.plus/...`. Match this format in suggestions.

## Compliance check

Before delivering, run the standard compliance check from the main `brain.md`:

1. **Terminology.** No forbidden terms ("social network", "forum platform", "chat tool", growth guarantees). Note: glossary entries like `/glossary/vertical-social-network` exist for definitional content — the term itself is not forbidden, only positioning social.plus as one is.
2. **Tone.** Sound like social.plus, not default Claude.
3. **Claims.** No invented stats, customer names, quotes.
4. **Em dashes.** None — use parentheses or restructure.
5. **Emojis.** None in user-facing output. (Internal warning markers like ⚠️ in the output sections above signal a flag, not decoration.)

If any check fails, fix the output before delivering.

## Important: URL format

**Always use `github.com/.../blob/...` URLs when fetching files.** Never attempt `raw.githubusercontent.com` or `api.github.com` — both are blocked by network egress settings.

## Out of scope (v1)

- **`docs.social.plus`** — developer documentation lives on a separate subdomain not yet captured in any `pages-*.json` file. When draft content references docs, surface this as "no in-scope link target" rather than guessing a URL.
- **The forum.** Same reason as docs.
- **External links / backlinks.** Use `backlink-placement-finder` or `link-building-vetter` for outbound work.
- **Live Ahrefs runtime calls.** This skill stays static-data-driven for cannibalization/strategy decisions (`link-strategy.md` is regenerated quarterly). Live WebFetch is used only for verifying link insertion points on social.plus pages, not for SEO data.
- **Auto-publishing changes to Webflow.** This skill recommends; the user implements.

## Escalation triggers (stop and ask Stefan)

Stop execution and surface to the user when any of these fire:

- A draft violates a cannibalization rule but the writer insists the commercial framing is correct. Surface the rule and the writer's rationale; let Stefan decide.
- A new page's canonical anchor would conflict with an existing anchor (would create a new cannibalization trap).
- `pages-*.json` `_meta.itemCount` jumps by > 10% between publishes (possible CMS migration or bulk-import — needs review before running audit).
- DR drops by > 5 points since last `link-strategy.md` refresh.
- A proposed anchor would use a forbidden positioning term (e.g., "social network" as a product anchor per `messaging/terminology.md`).
- The draft's target keyword is already cannibalized across 10+ URLs per GSC, and the proposed article would add an 11th. Recommend consolidation rather than publishing.
- `link-strategy.md` §"Refresh by:" date is more than 14 days in the past. Surface as "strategy is stale — needs refresh" before running audits.

Format the escalation as a clearly-flagged block at the top of the output so Stefan sees it before the linking details.

## Adoption credit

The 7-step audit framework adapts patterns from [openclaw/skills internal-linking-optimizer](https://github.com/openclaw/skills/tree/main/skills/aaron-he-zhu/internal-linking-optimizer) (Apache-2.0). The cannibalization handling, canonical anchor map, social.plus-specific data layer, intent-aware definitional/commercial split, and skill-to-skill invocation pattern are net-new for this skill.
