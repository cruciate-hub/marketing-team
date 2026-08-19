---
name: competitive-intelligence
description: >
  Briefing and query interface for social.plus competitive intelligence.
  Reads from two knowledge layers maintained by the /competitive-intel skill
  (competitive-intel.md for product/SDK profiles, competitive-marketing-intel.md
  for marketing intelligence) and delivers role-tailored briefings, answers
  ad-hoc competitive questions, and surfaces actionable insights.
  Does NOT maintain the knowledge layers -- that is /competitive-intel's job.
  This skill is the read layer; /competitive-intel is the write layer.
when_to_use: >
  Trigger phrases: "competitive briefing", "what's new with competitors",
  "what should I know about [competitor]", "how do we compare to [competitor]",
  "battle card for [competitor]", "competitive positioning",
  "competitor landscape", "what changed competitively",
  "competitive brief", "brief me on competitors",
  "what's [competitor] doing", "compare us to [competitor]",
  "competitor strengths", "competitor weaknesses".
  Do NOT trigger for: "refresh competitive intel", "update competitor profiles",
  "run the monthly refresh", "crawl ad library" -- those are /competitive-intel tasks.
---

# Competitive Intelligence -- Briefing and Query Interface

This skill is the **read layer** for social.plus competitive intelligence. It reads from two knowledge layers maintained by the `/competitive-intel` skill and delivers role-tailored briefings, answers ad-hoc questions, and surfaces actionable insights.

**This skill does NOT maintain the knowledge layers.** If data is stale, missing, or wrong, direct the stakeholder to flag it to Bam, who maintains both layers via the `/competitive-intel` skill on a monthly refresh cadence.

**The knowledge layers are private.** They live in a shared Google Drive folder with restricted access, and all competitor-specific facts, figures, and findings live there -- never in this file. If you cannot find or open the files, the stakeholder does not have access yet: tell them to request access from Bam. Do not work around missing access with external research; a briefing without the knowledge layers is not a briefing.

---

## Before every briefing: ensure you have the latest data

Both knowledge layer files are stored as Google Docs in a shared Drive folder. At the start of every invocation, read the most current versions using the Google Drive MCP.

**How to find and read each file:**

1. Search for `competitive-intel.md`:
   `search_files` with query: `title = 'competitive-intel.md'`
   Then call `read_file_content` with the returned file ID.

2. Search for `competitive-marketing-intel.md`:
   `search_files` with query: `title = 'competitive-marketing-intel.md'`
   Then call `read_file_content` with the returned file ID.

Always search by filename, not by a stored file ID, because the file ID may change when the `/competitive-intel` skill replaces the file during a monthly refresh. If a search returns more than one match, use the most recently modified file and confirm its `Last full refresh` header looks current. Always read them fresh at the start of a briefing session; never rely on a cached or previously-read version from an earlier session. Check the `Last full refresh` date at the top of each file to confirm recency.

---

## The two knowledge layers

| File | Maintained by | What it covers | Example questions it answers |
| :-- | :-- | :-- | :-- |
| `competitive-intel.md` | `/competitive-intel` | Product capabilities, SDK features, pricing, strategic positioning, gap analysis, ICP relevance per competitor | "Does [competitor] have video calling?" / "How does [competitor]'s pricing compare to ours?" / "Which competitors cover livestream shopping?" |
| `competitive-marketing-intel.md` | `/competitive-intel` | Seven marketing dimensions per competitor: web traffic/SEO, content marketing, AEO/LLM visibility, paid advertising (Google/LinkedIn/Meta ad library data), review site presence, developer adoption (npm), conversion/pricing models | "Who's running the most LinkedIn ads?" / "What keywords does [competitor] own that we don't?" / "Which competitor has the highest G2 rating?" / "What ad copy is [competitor] using?" |

**Competitor scope and tiers** are defined in the `Competitor scope` section at the top of `competitive-intel.md`, not in this file. The knowledge layers track competitors in three tiers (Tier 1 = full depth, Tier 2 = medium depth, Tier 3 = lighter depth); read the current scope from the file at the start of each session. If a stakeholder asks about a competitor that is not in scope, say so and log it as a gap (Step 5).

**Known data accuracy issues** are likewise maintained in a `Known data accuracy issues` section at the top of each knowledge layer file (systematic estimate biases, inflated third-party metrics, and similar). Read that section before building the brief and carry its caveats into any affected data point you surface. Never present a caveated number without its caveat.

One accuracy note that is safe to state here because it is public knowledge: social.plus was formerly "Amity Social Cloud" (rebranded Oct 2024). Third-party sites still use the old name. If a stakeholder asks about "Amity" as a competitor, clarify that it is social.plus's former brand.

---

## Workflow

### Step 1: Identify the stakeholder

**Do NOT guess, assume, or infer the stakeholder's role or purpose.** Do not reference anything from the conversation history to pre-fill these answers. Do not lead with phrases like "given your work on X" or "since you're preparing for Y." Every invocation starts fresh with two neutral questions:

1. **What's your role?** (Sales, Marketing/Content, Product, Growth/Paid, Leadership, Engineering, or other)
2. **What's your focus today?** (A specific competitor, a deal, a content piece, a campaign, a general update, anything)

Ask exactly these two questions, plainly, with no preamble or assumptions. Wait for answers before proceeding. Do not ask more than these two questions before delivering the brief. The goal is speed to value.

### Step 2: Read the knowledge layers

Read both `competitive-intel.md` and `competitive-marketing-intel.md` in full. Do NOT run any external research at this stage. The brief is built entirely from what the knowledge layers already contain.

Note the `Last full refresh` date at the top of each file. If either file is older than 45 days, add a staleness warning at the top of the brief: "Note: this data was last refreshed on [date]. Some details may have shifted. Flag anything that seems off and Bam will verify."

### Step 3: Build the brief

The brief has three sections, delivered in this order:

---

**Section 1: What changed (top of brief)**

Surface the 3-5 most important recent changes. These are what everyone should know regardless of role. Pull from "Recent moves" sections, profiles where `last_verified` is more recent than the previous refresh, strategic insights, paid advertising changes, review site shifts, and developer adoption trends.

**Format: each change is a structured block:**

1. **Bold headline** -- one sentence stating the change AND why it matters, not just what happened. Lead with the implication, not the fact.
2. One sentence of supporting context or data if needed. Skip if the headline says it all.

No filler. If nothing meaningful changed, say "No major competitive shifts since the [date] refresh" and move to Section 2.

**Example of what GOOD looks like in chat** (fictional scenario -- the competitors, the events, and every number in BOTH examples below are invented for format illustration; none of it is real intelligence about anyone):

> **[Competitor A] cut their entry price in half**
> Their starter tier dropped from $X to half that. Expect it to come up in every price-sensitive deal this quarter.
>
> **[Competitor B] acquired a video infrastructure vendor**
> Signals a push into livestream. Expect bundled chat-plus-video offers within two quarters.
>
> **[Competitor C]'s review momentum is real**
> Their G2 review velocity roughly doubled this quarter. They are mobilizing customers; expect their comparison pages to lean on it.

**Example of what BAD looks like (do NOT do this; same invented scenario):**

> [Competitor A] reduced their starter tier price from $X to half that, which may affect price-sensitive deals. [Competitor B] acquired a video infrastructure vendor, signaling a push into livestream and possible bundled chat-plus-video offers. [Competitor C]'s G2 review velocity roughly doubled this quarter as they mobilize customers for reviews.

The bad version is a wall of facts with no hierarchy. Each insight competes for attention and none of them land. The good version gives each change its own space and tells the reader why they should care.

---

**Section 2: What matters for your role**

Tailor the depth and angle based on the stakeholder's role and stated focus. Select the 3-5 most relevant insights; do not dump the entire knowledge layer.

**Format: every insight follows the same pattern:**

1. **Bold headline** -- the finding stated as an implication, not a raw fact. "[Competitor A] added SSO to their mid tier" is a fact (an invented one, for illustration). "[Competitor A] is now positioned to poach our enterprise evaluations" is an insight. Lead with the insight.
2. **Why it matters** -- 1-2 sentences connecting the finding to the stakeholder's world. For Sales, that means deal impact. For Product, that means roadmap implications. For Marketing, that means content or campaign opportunity.
3. **Supporting data** -- use a mini comparison table when comparing 3+ data points across competitors. Never bury numbers in a paragraph. If there is only one number, state it inline.

**When to use tables vs inline data:**

Use a table when:
- Comparing the same metric across 3+ competitors
- Showing capability coverage (has/doesn't have)
- Contrasting pricing tiers

Use inline data when:
- There is a single number or percentage
- The comparison is between just two things (social.plus vs one competitor)

**Example of what GOOD looks like in chat** (Growth role, ad focus; fictional scenario -- the competitors, the social.plus row, and every data point in BOTH examples below are invented for format illustration; none of it, including the claims about social.plus, is real intelligence):

> **[Competitor B] is bidding on our brand keyword**
> Their ads show above ours on searches for our own name. A small always-on brand-defense campaign would blunt this cheaply.
>
> | Competitor | Brand bidding | LinkedIn ads | Meta ads | Retargeting |
> |:--|:--|:--|:--|:--|
> | [Competitor A] | -- | Active | -- | Active |
> | [Competitor B] | Yes | Active | Active | -- |
> | [Competitor C] | -- | -- | Active | Active |
> | **social.plus** | [invented] | [invented] | [invented] | [invented] |
>
> **[Competitor C]'s webinar loop is worth studying**
> They run a monthly webinar series that feeds their retargeting audiences. We could pilot the same loop with existing webinar content.

**Example of what BAD looks like (do NOT do this; same invented scenario):**

> The ad library data across the competitive set shows [Competitor B] is bidding on our brand keyword and their ads show above ours on brand searches. Meanwhile, [Competitor C] runs a monthly webinar series that feeds their retargeting audiences, which may be worth studying and replicating.

The bad version buries two separate insights in one paragraph, states facts without implications, and gives the reader no sense of what to do about it.

---

**Role-specific content priorities (what to surface, not how to format it -- format always follows the headline/implication/data pattern above):**

**Sales:**
- Head-to-head capability comparisons for the competitor(s) in their deal
- Pricing differentiators and objection-ready positioning
- "Where they're strong" (so the rep is prepared) and "Where they can't compete" (social.plus's gap advantage)
- If they name a specific competitor, go deep on that one profile
- If general update, rank by evaluation frequency (Tier 1 first, per the scope section in the knowledge layer)

**Marketing / Content:**
- Content gap analysis: keyword territories competitors own that social.plus does not
- Competitor content strategy patterns (volume, comparison pages, developer content)
- AEO/LLM visibility positioning
- Ad creative themes worth studying or replicating
- Third-party pages that mention social.plus under either brand name

**Product:**
- Capability delta tables: where social.plus leads, where competitors lead
- Recent product moves (launches, acquisitions, pivots)
- Developer adoption trends (npm data)
- Capabilities competitors are investing in (R&D direction signals)

**Growth / Paid:**
- Paid advertising: ad creative analysis, conquest patterns, spend signals
- SEM strategist recommendations from the marketing layer
- Conversion model comparisons (freemium vs free trial vs sales-led)
- Competitor page and ad copy patterns worth replicating

**Leadership / Executive:**
- Market landscape summary: positioning map
- Strategic threats (competitors gaining ground, new entrants)
- Market share signals (traffic, developer adoption, review momentum)
- High-level; point to specific profiles for depth

**Engineering:**
- SDK/API capability comparisons
- Developer experience differentiators (docs quality, SDK design)
- Integration ecosystem comparisons
- Technical architecture differences

**Other roles or unclear:**
- Top 3 competitive threats, social.plus's strongest differentiators, and the single most important thing to know right now
- Keep it under 500 words

---

**Section 3: Suggested follow-ups**

After delivering the brief, suggest 2-3 specific follow-up questions tailored to the stakeholder's role and focus. Keep them short, direct, and phrased as things you can actually answer from the knowledge layers. Present them as a simple numbered list, not a paragraph.

Example format in chat:

> **Want to dig deeper?**
> 1. Full capability comparison table: [competitor] vs social.plus
> 2. [Competitor]'s pricing tiers and where we undercut them
> 3. Top 3 objections a [competitor] customer would raise about switching

Tailor the suggestions to the role:
- **Sales:** capability comparisons, pricing, objection handling
- **Marketing:** content gaps, competitor ad copy, AEO/LLM positioning
- **Growth:** conquest page teardowns, ad spend patterns, landing page analysis
- **Product:** capability gaps, competitor R&D direction, developer adoption data
- **Leadership:** landscape shifts, momentum leaders, vulnerability assessment
- **Engineering:** SDK comparisons, developer experience, integration ecosystems

### Step 4: Handle follow-up queries

When the stakeholder asks a follow-up:

**First, answer from the knowledge layers.** Read the relevant section(s). If the answer is there, deliver it. Do not run external research if the layers cover it.

**If the layers partially cover it,** deliver what is known and clearly state what is missing. Then do light research to fill the gap:
- WebSearch for the specific question
- Ahrefs MCP pull if the question is about SEO/traffic data
- npm registry check if the question is about developer adoption

After the light research, deliver the supplementary answer and note: "This finding is not yet in the knowledge layer. It will be incorporated in the next monthly refresh, or flag it to Bam for an immediate update."

**If the layers do not cover it at all,** say so plainly: "The competitive intelligence layers don't currently track [X]. I can do a quick search now, or you can flag this to Bam to add it to the next refresh." If they want the quick search, do it and deliver with appropriate confidence caveats.

**Never fabricate an answer.** If the data is not in the layers and a quick search does not turn it up, say so. "I don't have reliable data on that" is better than a guess.

### Step 5: Log gaps

At the end of a briefing session, if any questions were asked that the knowledge layers could not answer, compile a short list of data gaps. Format:

```
## Gaps flagged from [date] briefing ([stakeholder role])
- [Question asked] -- [what was missing]
- [Question asked] -- [what was missing]
```

Append this to the self-improvement note at the bottom of the relevant knowledge layer file, so the next `/competitive-intel` refresh picks it up.

---

## Voice and format rules

**Tone:**
- No em dashes. Use commas, semicolons, colons, or sentence breaks.
- "social.plus" always lowercase except at sentence start.
- Factual, not spin. Acknowledge competitor strengths honestly. This is internal-grade intelligence.
- Active voice.
- No marketing fluff. No "unlock", "transform", "supercharge."

**Structure (this is critical for readability):**
- Every insight is a standalone block: bold headline, then 1-2 sentences of implication/context, then data if applicable. Never combine multiple insights into one paragraph.
- Headlines state implications, not facts. "[Competitor A] is coming for our enterprise deals" not "[Competitor A] added SSO to their mid tier."
- Use tables for multi-competitor data comparisons (3+ data points). Never describe a table's contents in a paragraph when the table itself is clearer.
- Keep each insight block to 3-4 lines max in chat. If it is getting longer, you are either combining two insights (split them) or over-explaining (cut it).
- Separate insight blocks with a blank line so the reader's eye can jump between them.
- Keep briefs focused. 3-5 sharp insights beat 15 shallow ones.
- The brief should feel like a smart colleague giving you a 2-minute verbal update, not a research report.

**Confidentiality:**
- Briefing output is internal-only. Never paste briefing content, knowledge layer excerpts, or competitor findings into anything public-facing (blog posts, social copy, comparison pages) without explicit review; hand public-facing work to the relevant writing skill instead.

---

## Relationship to other skills

**This skill reads from:**
- `competitive-intel.md` (maintained by `/competitive-intel`)
- `competitive-marketing-intel.md` (maintained by `/competitive-intel`)

**This skill does NOT:**
- Refresh or rewrite the knowledge layers (use `/competitive-intel`)
- Crawl ad libraries, pull Ahrefs data, or run npm checks as part of a scheduled refresh (use `/competitive-intel`)
- Produce ICP-specific competitive positioning (use `/icp-messaging`)
- Write GTM briefs (use `/gtm`)
- Write blog posts (use `/blog-seo-content`)

**When to escalate to /competitive-intel:**
- A stakeholder reports that a data point is wrong or outdated
- A question reveals a significant gap in the knowledge layers
- A new competitor is mentioned that is not profiled
- The staleness warning triggers (data older than 45 days)

In all these cases, note the issue in the gap log and tell the stakeholder: "I've flagged this for the next knowledge layer refresh."
