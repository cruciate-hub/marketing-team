---
name: site-intelligence
description: >
  Query, audit, and analyze the social.plus marketing website using a structured
  JSON snapshot of all page content. Use this skill whenever someone asks about
  website content, what pages say, which pages mention a feature or topic, messaging
  consistency across the site, content gaps, page health, competitive comparisons
  against the site, or anything related to "our website," "our pages," "what do we
  say about," "site content," "which pages," or "does the site mention." Also trigger
  when someone wants to write new copy and needs awareness of what already exists on
  the site, or when auditing the site for contradictions, stale content, or messaging
  drift. Trigger even for simple questions like "what does the pricing page say" or
  "do we mention AI on the homepage." If the answer depends on what's currently on
  the social.plus website, use this skill.
---

# social.plus Site Intelligence

This skill gives you full awareness of what the social.plus marketing website says — every page, every heading, every claim — so you can query it, audit it, find gaps, and generate site-aware recommendations.

## Step 0: Fetch the main brain

Fetch the main brain for cross-domain routing, precedence rules, and the compliance check:

```
https://github.com/cruciate-hub/marketing-team/blob/main/brain.md
```

## Step 1: Load the site content

Fetch the site content JSON using WebFetch:
```
https://github.com/cruciate-hub/marketing-team/blob/main/website/marketing-pages.json
```

The JSON structure:
```json
{
  "_meta": { "generatedAt": "...", "pageCount": 37 },
  "pages": [
    {
      "url": "/social/features",
      "metaTitle": "...",
      "metaDescription": "...",
      "content": "# heading\n## section\n### feature name\nFeature description..."
    }
  ]
}
```

Each page's `content` field preserves heading hierarchy using markdown-style markers (`#`, `##`, `###`). This is your source of truth for what the website currently says.

The JSON is regenerated automatically by a Cloudflare Worker on every Webflow publish, so it always reflects the latest live site content.

### Scope notice

This skill covers **37 marketing pages only** — product pages, feature pages, use case pages, industry pages, pricing, and the homepage. It does **not** include blog posts, documentation (docs.social.plus), customer stories, tutorials, events, the forum, or legal pages. When your analysis could be misread as covering the entire web presence, make this scope clear in your response — e.g., "Across the 37 marketing pages..." rather than "Across the website..." so the user knows exactly what's included and what's not.

## Step 2: Load brand guidelines (when needed)

For any analysis that involves evaluating messaging quality, suggesting copy, or checking brand consistency, also fetch the brand routing file:
```
https://github.com/cruciate-hub/marketing-team/blob/main/messaging/brain.md
```
Follow its instructions to load the relevant guideline files. Not every query needs this — simple lookups ("what does page X say about Y") don't. But audits, gap analysis, and copy suggestions always do.

## Step 3: Determine the analysis mode

Read the user's question and route to the appropriate mode. Most questions map naturally — don't overthink this. If a question spans multiple modes, combine them.

---

## Mode: Query

**When to use:** The user wants to know what the site says about something. Keywords like "what do we say about," "which pages mention," "does the site cover," "find every reference to."

**What to do:**

1. Search every page's `content` field for the term or concept.
2. Return every match with the page URL, the heading hierarchy where it appears, and the exact surrounding text (enough to understand context — typically the paragraph or bullet).
3. After listing matches, note any pages where the term is **contextually relevant but absent**. This is what separates a smart query from a dumb search. If someone asks "which pages mention livestream," don't just list the hits — also flag that `/industry/sports` and `/industry/media-and-news` don't mention it despite being obvious fits.

**Output format:**

Start with a count: "Found [N] mentions across [M] pages."

Then for each page, show:
```
/page-url — [heading context]
"Exact quote from the page content showing the match and enough surrounding text for context."
```

End with a "Notable absences" section if any pages should logically mention this topic but don't.

**Precision matters.** Quote the actual content from the JSON. Don't paraphrase, don't summarize, don't add words that aren't there. The user is trying to understand what the site *actually* says, not what you think it says.

---

## Mode: Consistency Audit

**When to use:** The user asks to find contradictions, inconsistencies, or messaging drift across the site. Also use when someone asks to "audit the site," "check for contradictions," or "is our messaging consistent."

**What to do:**

Scan all pages and cross-reference these specific categories:

1. **Numerical claims.** Customer counts, feature counts, uptime percentages, response times, "X+ brands" claims. Flag any number that appears differently on two pages.

2. **Feature names and descriptions.** The same feature described with different names on different pages (e.g., "live chat" vs. "real-time messaging" vs. "in-app chat"). Flag terminology drift — even if both are technically correct, inconsistency confuses prospects and hurts SEO.

3. **Feature lists vs. counts.** If a page says "20+ messaging features" but the features page only lists 17, that's a contradiction. You have the full JSON — actually count the distinct features listed under each heading on feature pages and compare against any numerical claims elsewhere. Never hedge with "without access to exact counts" — you have the data, so count it.

4. **Positioning statements.** How social.plus is described at a high level. If the homepage says "the most customizable" but a product page says "the easiest to integrate," those are potentially conflicting positioning angles. Flag these for review — they may be intentional but should be conscious choices.

5. **CTA consistency.** Do similar pages use the same CTAs? If most product pages say "Start free" but one says "Request a demo," note it. This may be intentional for enterprise pages but warrants attention.

6. **Product scope claims.** If one page implies a feature is available on all plans but the pricing page restricts it to higher tiers, that's a trust-damaging inconsistency.

**Output format:**

Group findings by severity:

🔴 **Contradictions** — Factual conflicts that will confuse or mislead visitors
🟡 **Inconsistencies** — Different terminology or framing for the same thing
🟢 **Minor drift** — Stylistic differences worth noting but not urgent

For each finding:
```
🔴 [Category]: [Brief description]
Page A (/url-a): "exact quote"
Page B (/url-b): "exact quote"
Recommendation: [specific suggestion to resolve]
```

If the site is clean, say so: "No contradictions found. [N] minor terminology inconsistencies noted below."

---

## Mode: Coverage Map

**When to use:** The user wants to see where a specific theme, feature, or narrative appears across the site and where it's missing. Keywords like "where do we mention [X]," "how well do we cover [topic]," "mapping our [X] messaging," "which pages should talk about [Y]."

**What to do:**

1. Define the theme clearly. If the user says "AI," determine whether they mean AI-powered features, AI in general marketing messaging, or specific AI capabilities. Ask for clarification only if genuinely ambiguous.

2. Scan every page and categorize each as:
   - **Strong presence**: The theme is a primary focus with dedicated sections or multiple mentions.
   - **Mentioned**: The theme appears but isn't a focus — a passing reference or single bullet.
   - **Absent but relevant**: The page's topic naturally connects to this theme but doesn't mention it.
   - **Not applicable**: The page has no logical connection to this theme.

3. For absent-but-relevant pages, explain *why* it's relevant and suggest where on the page the theme could be introduced (which section, after which existing content).

**Output format:**

Start with a summary: "[Theme] appears on [N] of [total] pages. [M] pages have strong coverage, [K] mention it briefly, and [J] pages should cover it but don't."

Then ALWAYS show the compact visual map first — this is the bird's-eye view the reader needs before diving into detail:
```
Strong:    /page-a, /page-b, /page-c
Mentioned: /page-d, /page-e
Missing:   /page-f (relevant because...), /page-g (relevant because...)
```

Only after the visual map, expand into the detailed per-page breakdown. The map is navigation — the detail is the working document. Don't skip the map and go straight to detail.

For each "Missing" page, include a one-liner on where the theme fits and what angle to take — grounded in what the page already covers. Load brand guidelines for these suggestions.

---

## Mode: Page Health Check

**When to use:** The user asks about a specific page — "audit the chat page," "is the pricing page up to date," "review /social/features," "what's wrong with [page]."

**What to do:**

Run a comprehensive check on the target page against the rest of the site:

1. **Internal consistency.** Does the page contradict itself? Are claims in the hero consistent with details lower on the page?

2. **Cross-site consistency.** Compare the page's claims against related pages. Does `/chat` align with `/chat/features`? Does `/pricing` reflect what feature pages promise?

3. **Content completeness.** Compare against sibling pages. If `/social/features` lists 15 features but `/chat/features` only lists 8, is the chat page genuinely thinner or is the product smaller? Cross-reference with other pages that mention chat features to see if any are missing from the features page.

4. **Messaging alignment.** Does the page's positioning match the overall brand narrative? Load brand guidelines and check tone, terminology, and value propositions.

5. **Structural analysis.** Heading hierarchy, content depth relative to similar pages, presence of CTAs, meta title and description quality for SEO.

**Output format:**

Start with a health score and one-line summary:
```
/chat — 7/10 — Solid feature coverage but terminology drifts from other chat pages and missing 2 features mentioned elsewhere on the site.
```

Then detail each check with findings. Group by: what's working well, what needs attention, and specific recommendations. Every recommendation should reference the exact content that needs changing and suggest replacement text aligned with brand guidelines.

---

## Mode: Competitive Comparison

**When to use:** The user provides a competitor URL (or competitor name + page) and wants to compare against social.plus positioning. Keywords like "compare against [competitor]," "how does our page stack up," "competitive analysis vs [URL]."

**What to do:**

1. Fetch the competitor page using WebFetch.
2. Load the relevant social.plus pages from the JSON (determine which pages are comparable based on the competitor page's content).
3. Load brand guidelines.
4. Analyze across these dimensions:

   - **Claims they make that we don't.** Features, capabilities, social proof, or positioning angles present on their page but absent from comparable social.plus pages. For each: is this a real gap (we don't have it), a messaging gap (we have it but don't mention it), or not relevant to our positioning?

   - **Claims we make that they don't.** Our differentiators and unique positioning. Are we making the most of these, or burying them?

   - **Head-to-head messaging.** Where both companies address the same capability, whose messaging is stronger? More specific? More benefit-oriented? More credible?

   - **Social proof and trust signals.** Customer logos, case studies, certifications, uptime claims, security badges. Compare what each side shows.

   - **Content depth and structure.** Who gives more detail? Who has better page structure? Who makes it easier for a prospect to find what they need?

**Output format:**

Start with a one-paragraph executive summary of the competitive position.

Then structured findings:
```
They claim, we don't:
- [Claim] — Gap type: [real/messaging/irrelevant] — Recommendation: [action]

We claim, they don't:
- [Claim] — Are we leveraging this enough? [assessment]

Head-to-head:
- [Topic]: Their angle: "..." | Our angle: "..." | Edge: [them/us/neutral] — Why: [reasoning]
```

End with 3-5 prioritized actions to strengthen competitive positioning, grounded in brand guidelines.

---

## Go beyond the question

After answering what was asked, always add a **"While looking at this..."** section with 2-3 observations the user didn't ask for but would want to know. This is what makes the skill feel like a smart colleague, not a search engine.

The observations should come naturally from what you noticed while scanning the data to answer the original question. Think like a strategist who's been hired to review the site — you wouldn't just answer the brief and leave; you'd flag the things that jumped out.

**What good observations look like:**

- Connections across pages: "While checking the chat pages, I noticed `/use-case/live-chat` and `/chat/features` describe typing indicators differently — one says 'real-time typing indicators,' the other says 'presence indicators.' Worth aligning."
- Missing opportunities: "The moderation page doesn't link to or reference any industry pages, but `/industry/gaming` and `/industry/betting` both have heavy moderation needs — cross-linking would strengthen both pages."
- Patterns the user can act on: "5 of your 10 industry pages use identical boilerplate for the SDK section. The pages that perform differently (gaming, fintech) have industry-specific SDK copy. Might be worth customizing the others."
- Competitive angles: "You mention AI moderation on 3 pages, but always as a feature bullet. Competitors like Sendbird dedicate entire sections to it. Given the market trend toward trust & safety, this could be a positioning opportunity."
- Content quality signals: "The `/video` landing page is half the length of `/social` and `/chat`. If video is a growth priority, the page doesn't reflect that."

**What bad observations look like:**

- Generic advice: "Consider adding more CTAs." (too vague, not grounded in data)
- Restating the obvious: "The pricing page contains pricing information." (no insight)
- Observations that require information you don't have: "Your conversion rate on this page might be low." (you can't know that)

Keep it to 2-3 observations. Make each one specific, quotable, and actionable. The user should finish reading and think "I wouldn't have caught that."

---

## General principles across all modes

**Quote, don't paraphrase.** When referencing site content, use the exact text from the JSON. Put it in quotes. The user needs to know what the site *actually* says, not your interpretation.

**Be specific about locations.** Don't say "the features page could mention this." Say "on `/chat/features`, under the `## Messaging` section, after the existing paragraph about typing indicators, add..."

**Page-by-page actionability.** Group recommendations by page whenever possible. The person acting on your analysis works page-by-page in Webflow.

**Don't over-flag.** Not every minor difference is a problem. Some pages intentionally use different framing for different audiences (enterprise vs. developer). Use judgment about what's genuinely problematic vs. what's intentional variation. When in doubt, flag it but note that it may be intentional.

**Combine modes when natural.** If someone asks "audit the pricing page and compare it to [competitor]," run both Page Health Check and Competitive Comparison. Don't force a single-mode answer.

## Important: URL format

**Always use `github.com/.../blob/...` URLs when fetching files.** Never attempt `raw.githubusercontent.com` — it is blocked by network egress settings and will throw an error.

## Pages covered

### Product feature pages
- `/social/features` — all social features
- `/chat/features` — all chat/messaging features
- `/video/features` — all video features
- `/analytics` — analytics and insights
- `/moderation` — moderation tools
- `/monetization` — monetization features

### Product landing pages
- `/product` — product overview
- `/social` — social product landing
- `/chat` — chat product landing
- `/video` — video product landing
- `/social/sdk`, `/chat/sdk`, `/video/sdk` — SDK pages
- `/social/uikit`, `/chat/uikit` — UIKit pages

### Use case pages
- `/use-case/1-1-chat`, `/use-case/activity-feed`, `/use-case/custom-posts`, `/use-case/group-chat`, `/use-case/groups`, `/use-case/live-chat`, `/use-case/livestream`, `/use-case/polls`, `/use-case/stories-and-clips`, `/use-case/user-profiles`

### Industry pages
- `/industry/retail`, `/industry/fitness`, `/industry/travel`, `/industry/sports`, `/industry/health-and-wellness`, `/industry/fintech`, `/industry/media-and-news`, `/industry/edtech`, `/industry/gaming`, `/industry/betting`

### Other
- `/` — homepage
- `/pricing` — pricing page
