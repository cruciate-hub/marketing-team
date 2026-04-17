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

**Why this works even when the JSON is sparse:** known limitations of the snapshot generator (e.g., the static-page extractor can't reach Webflow Components, so industry pages capture only the headings outside components) are compensated by the Phase 2 live fetch — the live page sees everything.

## Step 0: Fetch the main brain

Fetch the main brain for cross-domain routing, precedence rules, and the compliance check:

```
https://github.com/cruciate-hub/marketing-team/blob/main/brain.md
```

## Step 1: Determine which data files to fetch

Always fetch `link-strategy.md`. Then pick `pages-*.json` files based on context:

| Calling context | Files to fetch |
|---|---|
| Called by `blog-seo-content` (draft mode) | `pages-marketing.json`, `pages-use-cases.json`, `pages-industry.json`, `pages-glossary.json`, `pages-blog.json`, `pages-customer-stories.json` |
| Called by `aeo-content` (draft mode) | `pages-marketing.json`, `pages-use-cases.json`, `pages-glossary.json`, `pages-answers.json` |
| Standalone draft mode (user-pasted content) | `pages-marketing.json`, `pages-use-cases.json`, `pages-industry.json`, `pages-glossary.json` (default — ask if blog/customer-stories/answers should also be considered) |
| Audit mode | All 10 files: `pages-marketing.json`, `pages-use-cases.json`, `pages-industry.json`, `pages-glossary.json`, `pages-blog.json`, `pages-customer-stories.json`, `pages-answers.json`, `pages-product-updates.json`, `pages-release-notes.json`, `pages-webinars.json` |

Always fetch in parallel using WebFetch. URLs follow the pattern:
```
https://github.com/cruciate-hub/marketing-team/blob/main/website/link-strategy.md
https://github.com/cruciate-hub/marketing-team/blob/main/website/pages-marketing.json
https://github.com/cruciate-hub/marketing-team/blob/main/website/pages-use-cases.json
... etc
```

If `link-strategy.md` is missing or its `Refresh by:` date is in the past, surface this to the user before continuing. Stale strategy beats no strategy, but the user should know.

### GitHub HTML parsing

These are GitHub HTML pages. Extract the markdown content from the `<article>` element with class `markdown-body`. Use Python:

```python
import re, html
match = re.search(r'<article[^>]*class="[^"]*markdown-body[^"]*"[^>]*>(.*?)</article>', content, re.DOTALL)
if match:
    text = re.sub(r'<[^>]+>', '\n', match.group(1))
    text = html.unescape(text)
```

For JSON files served as HTML on GitHub, extract the same way then `json.loads(text.strip())`. Each `pages-*.json` has shape `{"_meta": {...}, "pages": [{"url", "metaTitle", "metaDescription", "content"}, ...]}`. URLs are full `https://www.social.plus/...`.

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

**4. Apply count rules by content type.**

- **Blog post draft:** target 3-7 internal links (per `link-strategy.md` and `blog-seo-content`).
- **AEO article draft:** target 1-3 internal links MAX. Allowed only in definition paragraph, "why it matters", architecture/features, step-by-step. Disallowed in FAQs, conclusion, metrics table.
- **Generic/standalone draft:** default 3-5 unless user specifies.

Quality over quantity. Better to return 3 strong suggestions than 7 weak ones.

**5. Apply per-cluster anchor variation rules.**

If the draft would result in the same anchor pointing to the same page more than twice, use a variant from the cluster's anchor pool in `link-strategy.md`.

### Draft mode output format

Return a clearly-labeled section the calling skill can embed in its own output. Match the format to the consuming content type:

- For **blog content** (HTML output from `blog-seo-content`): provide ready-to-paste `<a href="..." target="_blank">anchor</a>` tags.
- For **AEO content** (markdown output from `aeo-content`): provide markdown links `[anchor](URL)` only.
- For **generic drafts**: provide both formats.

```
## Internal link suggestions

**Mode:** Draft (target keyword: "[keyword]", cluster: [Brand/Chat/Social/Video/Industry/Cross], content type: [blog/AEO/generic])

### Cannibalization check
[If any warnings fired:] ⚠️ This draft uses "[anchor term]" — see link-strategy.md cannibalization rule. [Brief recommendation.]
[If clean:] ✅ No cannibalization risks detected.

### Suggested links

1. **Anchor:** "[anchor text]"
   **Target:** [full URL]
   **Insert at:** [section heading or quoted sentence from draft]
   **Format:** `<a href="[URL]" target="_blank">[anchor text]</a>` OR `[[anchor text]]([URL])`
   **Reasoning:** [why this link, in 1 sentence — cite link-strategy.md row if a canonical match]

2. ...

[3-7 for blog, 1-3 for AEO]

### Notes for the writer
- [Optional: any cluster-specific anchor variation guidance applied]
- [Optional: any out-of-canonical-map link targets used (e.g., long-tail blog/glossary pages) and why]
- [Optional: AEO-specific section restrictions surfaced]
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
```

**2. Orphan and under-linked pages.**

Cross-reference Ahrefs orphan candidates from `link-strategy.md` against the fetched data. Flag pages with no contextual inbound links from other pages in the data set (header/footer nav doesn't count for SEO purposes).

```markdown
## Orphans and under-linked pages

[For each:]
- **[full URL]** ([file]) — Currently linked from: [list, or "no contextual inbound"]. Should be linked from: [list with reasoning].
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

Synthesize all findings into a phased plan.

```markdown
## Implementation plan

### Week 1: High-impact, low-effort
1. [Specific action: page, anchor, target]

### Week 2-3: Medium effort
1. [...]

### Week 4+: Strategic / requires content changes
1. [...]

### Tracking
- Re-run this audit in 90 days to measure progress.
- Key metrics: orphan count, generic anchor count, canonical violations, AEO over-linking instances.
```

### Audit mode "While looking at this..."

After the 7-step audit, always add a "While looking at this..." section with 2-3 observations the user didn't ask for but would want to know. This is the same pattern as `site-intelligence`. Be specific, quotable, actionable.

```markdown
## While looking at this...

- [Observation 1: connection across pages, missed opportunity, or pattern worth flagging]
- [Observation 2: ...]
- [Observation 3: ...]
```

---

## General principles (both modes)

**Quote, don't paraphrase.** When citing page content, quote it exactly. For headings or metadata, the JSON is the source. For body sentences (e.g., insertion-point context), you must have live-fetched the page first — never quote body content from memory or speculation.

**Be specific about locations.** Don't say "link from the chat page". Say "in `https://www.social.plus/chat`, under the `## Real-time messaging` section, after the existing paragraph about typing indicators, anchor 'in-app chat' to..."

**Respect the canonical map strictly.** If `link-strategy.md` says anchor X → page Y, that's the rule. If you think it's wrong, surface that as a flag for the user to update `link-strategy.md` — don't silently override.

**Definitional vs commercial intent matters.** A glossary anchor in product-pitch context is wrong. A product anchor in a definition paragraph is wrong. Match intent to target.

**Don't over-link.** Targets per content type:
- Blog: 3-7
- AEO: 1-3 max
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

## Adoption credit

The 7-step audit framework adapts patterns from [openclaw/skills internal-linking-optimizer](https://github.com/openclaw/skills/tree/main/skills/aaron-he-zhu/internal-linking-optimizer) (Apache-2.0). The cannibalization handling, canonical anchor map, social.plus-specific data layer, intent-aware definitional/commercial split, and skill-to-skill invocation pattern are net-new for this skill.
