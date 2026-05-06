---
name: case-study
description: >
  Write customer stories for social.plus following the exact Webflow CMS structure.
  Use this skill for: customer stories, case studies, customer success stories,
  customer spotlights, testimonial write-ups, or any content that tells the story
  of how a customer uses social.plus. Also trigger when the user wants to create
  or update a customer story CMS item in Webflow, or when they provide customer
  data, interview notes, or sales call notes and want them turned into a publishable
  customer story. Trigger on phrases like "case study", "customer story", "success
  story", "customer spotlight", "write about how [customer] uses", "write a CS for",
  or "new customer story."
  Do NOT trigger for general blog posts without a customer focus (use blog-seo-content).
---

# social.plus Customer Stories

This skill produces customer stories that match the exact structure of the social.plus website. The output maps directly to the Webflow CMS collection fields so content can be pasted into the CMS without reformatting.

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

The Bash tool truncates large stdout to a small preview when the output exceeds the harness's display cap (the exact size varies by environment — observed in the 20–50 KB range). When that happens you'll see a marker like `Output too large (NkB). Full output saved to: …` followed by a short preview, and the rest is invisible to you in-call. Most files in this repo are small enough that `cat` returns them in full and you never see the marker. **If you do see the marker, never proceed using the preview as if it were the whole file** — switch to one of the patterns below.

- **Truncated markdown** — read in line-range chunks instead. First check the total line count: `wc -l "$REPO/<path>"`. Then read each chunk:

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

## What to do

1. Read `brain.md` for cross-domain routing, precedence rules, and the compliance check.

2. Read `messaging/brain.md` (the messaging router).

3. Follow the messaging router's **"Long-form content"** routing. This loads:
   - `terminology.md` + `tone.md` (always)
   - `narrative.md` (messaging hierarchy and narrative structure)
   - `value-story.md` (value creation model — maps directly to customer story outcomes)
   - `positioning.md` (product pillars for framing the solution)

4. Also follow **"Short-form content"** routing for:
   - `boilerplates.md` (company descriptions for reference)

5. Read `website/pages-customer-stories.json` for narrative-consistency and cross-referencing.

Use this to:
- **Avoid contradictions** — check how similar customers are already described on the site (e.g., if writing a fitness industry customer, scan existing fitness stories for metrics/framing consistency).
- **Cross-link opportunities** — suggest 1-2 relevant existing customer stories the new story could reference in its body copy.
- **Avoid duplicates** — if the user is writing about a customer already in the collection, tell them so and ask whether they intend an update to the existing story instead of a new one.

## Step 1: Gather missing information before drafting

**Before writing anything**, review what the user has provided and ask for any missing information. Do NOT start drafting the customer story until you have enough data to avoid placeholders. Present one clear list of questions — not multiple rounds.

**Trust the user's intent.** The writer is a social.plus marketing-team member with the authority to proceed on any customer story they initiate. Do not open with disclaimers or questions about customer legitimacy, contractual status, NDA coverage, or brand/legal risk — those belong to their team, not to you. Begin directly with Step 1a.

### 1a. Auto-research public facts first

Once the customer name is known, run web searches to pre-fill what's publicly available: headquarters city/country, founding year, founder names, scale indicators (users, customers, locations, revenue), market position, and key product surface.

Present the findings back to the user in a labelled block so they only need to say "correct" or edit values — never type them from scratch. Only fall back to asking the user if web research genuinely fails.

### 1b. Ask only for what's genuinely missing

**Before sending the question list, filter out anything already answered by the Step 1a web research or by the user's original message. Only ask for what's genuinely missing.**

Check for and ask about:
- **Metrics / engagement data** — For real post-launch customer metrics (engagement lift, DAU/MAU trend, retention delta, feature adoption, integration timeline vs. actuals), the `bq-business-query` skill against the social.plus data warehouse is the source of truth. **Do NOT invoke it from this skill** — direct the user to run it separately and paste results back. Rationale: sales decks and memory-sourced numbers are rounded or wrong; BQ is authoritative. Suggest concrete questions modelled on metrics already used in social.plus customer stories:
  - Month-over-month or year-over-year growth rate for `[customer]`
  - Current user / member / active-community count
  - Launch date (first API activity) — for "time to launch" framing
  - Engagement lift in the months after integration
  - Cumulative content produced since launch (posts, comments, reactions)
  - Top features by usage (which endpoints see the most traffic)

  Company-scale stats (total users, locations, revenue) can also come from public sources via Step 1a. Any BQ-derived number needs customer sign-off before publishing. If `bq-business-query` isn't available, skip the warehouse pull and rely on user-provided figures.
- **Customer quote** — do they have a direct quote from the customer? If yes, who said it (name + title)?
- **Challenge details** — what specific problem was the customer trying to solve?
- **Why social.plus** — why did they choose social.plus over alternatives?
- **Implementation details** — which SDKs, UIKits, platforms (web/app), customization level, and timeline?
- **Results / outcomes** — quantified impact after launch.
- **Company basics** — headquarters location, founding year or scale indicator, industry.
- **Use cases** — which social.plus features does the customer use (Activity Feed, Group Chat, Live Chat, Livestream, etc.)?
- **Customer's product vocabulary** — what does the customer call their own product and its key features internally (e.g. "Wrist Feed," "Community Tab," "H-D app," "Rides," "Bikes")? Use their names in the body, not social.plus's generic feature names. This is the single biggest lever for a story that reads specific rather than templated.

Only ask about items that are genuinely missing from the user's input — don't re-ask what they already provided. Once you have enough information to write without placeholders, proceed to drafting.

Finally, **ask once whether the user has the Webflow connector (`webflow-socialplus` MCP) activated.** If yes, you can create the customer story directly as a draft item in the `💼 Customer Stories` CMS collection instead of producing paste-ready output — see the **Output format** section for how the two modes differ.

## Webflow CMS field mapping

Every customer story is a CMS item in the `💼 Customer Stories` collection. When writing a customer story, produce content for each of these fields. Present each field clearly labeled so the user can paste directly into Webflow.

### Required fields

**Name Company** (`name`, PlainText)
The customer's company name. This is the CMS item name.

**Slug** (`slug`, PlainText)
URL-safe slug. Lowercase, hyphens, no spaces. Example: `smart-fit`, `the-ring-magazine`.

### Hero section

**Hero Title** (`title`, PlainText)
Pattern: "How [Company] [past-tense verb] [outcome] with social.plus"
Examples from the live site:
- "How Smart Fit built a digital fitness community with social.plus"
- "How Talkspace is strengthening teen mental health support with social.plus"
- "How Snai elevated user engagement by integrating social.plus"
- "How Winner redefined interactive betting experiences using social.plus"

Keep it under 80 characters when possible. The customer's outcome leads — not social.plus's product.

**Hero Introduction Paragraph** (`hero-introduction-paragraph`, PlainText)
One to two sentences that expand on the hero title. Sets the scene for the full story.
Examples:
- "Embedding social features into the Smart Fit app to boost engagement, motivation, and member connection."
- "Winner transformed its platform by integrating powerful social features that fostered connection and engagement among users."

### Metrics (up to 3 boxes)

**Metric Box 1–3** (`numbers-box-1`, `numbers-box-2`, `numbers-box-3`, RichText)
Each metric box uses custom HTML tags for styling. Format:
```html
<big-nr>[VALUE]<big-nr><br><cs-number-text>[DESCRIPTION]<cs-number-text>
```
Do NOT wrap metric boxes in `<p>` tags — only the custom tags and `<br>`.

Examples:
- `<big-nr>60%<big-nr><br><cs-number-text>community growth rate MoM<cs-number-text>`
- `<big-nr>1.5M<big-nr><br><cs-number-text>Patients<cs-number-text>`
- `<big-nr>18%<big-nr><br><cs-number-text>Increase in betting rate of casual users<cs-number-text>`

Each box gets one number that stops the reader. Aim for 2 or 3 filled. Good sources, strongest first:

- **Post-launch outcomes** — what changed because of social.plus (engagement lift, retention, growth rate, session frequency). Pull from `bq-business-query` where available, or from the customer's own reporting.
- **Platform scale** — size of the community or user base (MAU, members, countries, locations).
- **Company facts** — founded year, employees, revenue, vehicles sold, patients served, etc.

If a metric isn't available yet, leave the box blank and move on — the story works without it, and the number can be added on a later pass once the customer approves it. Never fill a box with a vague descriptor or an invented figure.

**Keep phrasings durable.** Customer stories stay live for years — anchor metrics to fixed windows ("in 2025", "within their first year", "since launch") rather than rolling ones ("last 12 months", "currently", "recently"). A rolling window reads wrong the day the calendar turns.

**Thumbnail Metric** (`thumbnail-cs-overview-page-large-metric`, PlainText)
The most impressive single number, displayed on the customer stories overview page. Short format: `60%`, `1M`, `200k`, `4 weeks`. Pick the metric that stops someone scrolling.

**Thumbnail Metric Description** (`thumbnail-cs-overview-page-metric-description`, PlainText)
One-line description of the thumbnail metric. Lowercase. Examples: `community growth rate MoM`, `app downloads`, `patients`.

### Customer quote (optional)

**Top Quote** (`top-quote`, PlainText)
A direct quote from the customer. Include quotation marks. Only use if the user provides a real quote — never fabricate.

**Top Quote | Name** (`top-quote-name`, PlainText)
Full name of the person quoted.

**Top Quote | Job Title** (`top-quote-job-title`, PlainText)
Job title. Examples: "CEO", "Online Casino Executive", "Head of Product".

### Main body

**Customer Story** (`section-2-text`, RichText)
This is the full story. It uses rich text with custom HTML tags for section dividers. The structure follows a consistent pattern across all stories on the site:

#### Section structure

1. **Opening paragraphs** (2-3 paragraphs)
   Company background and context. Who they are, what they do, why they matter. Written as narrative prose.

2. **The Challenge** section
   ```html
   <sprscript-green>The Challenge<sprscript-green>
   ```
   Followed by an `<h3>` subheading that frames the specific problem.
   Then 2-3 paragraphs describing the challenge in detail. Frame using the core problems from `value-story.md` where they map naturally.

3. **Why social.plus** section
   ```html
   <sprscript-green>Why social.plus<sprscript-green>
   ```
   Followed by an `<h3>` subheading about why they chose social.plus.
   Then 2-3 paragraphs explaining the selection rationale. Use product pillar language from `positioning.md` but keep the customer as the subject.

4. **Implementation** section (optional, include when the user provides technical details)
   ```html
   <sprscript-green>Implementation<sprscript-green>
   ```
   Followed by `<h3>` and paragraphs about how they built it — SDKs used, UIKits, customization, timeline.

5. **Results / Impact** section (optional, include when outcome data is available)
   ```html
   <sprscript-green>The Results<sprscript-green>
   ```
   Quantified outcomes. Map to the value creation model from `value-story.md`: functional → strategic → economic → compounding.

#### Body formatting rules
- **Output the body as a single raw text block** — NOT inside a code fence, NOT as rendered markdown. The user pastes this directly into Webflow's rich text field (HTML source view). It must be copyable as-is.
- **Do NOT use `<p>` tags anywhere.** No `<p>` wrapping on paragraphs, section dividers, headings, or anything else. Webflow handles paragraph formatting.
- **`<sprscript-green>` tags stand alone on their own line**, bare — no `<p>`, no other wrapper. These are picked up by JavaScript on the site for styled section dividers.
- **`<h3>` tags stand alone on their own line** for subheadings within each section. The paragraph text that follows must start on the **next line** — never on the same line as the `</h3>`.
- Use `<strong>` for inline emphasis where needed.
- Separate paragraphs with blank lines.
- Target length: 4,000–7,000 characters (matching existing stories on the site).
- The customer is the hero. social.plus is the tool they chose. Write "they implemented" not "we provided."
- Images can be referenced with `<figure>` tags but leave image URLs as placeholders for the user to upload.

#### Example body output

The body should look exactly like this when output (raw text, not in a code block):

Founded in 2015, Acme Fitness has grown into one of Latin America's largest digital fitness platforms, serving over 3 million active members across 12 countries.

What started as a simple workout logger evolved into a full lifestyle platform. As their user base scaled, the team recognized that social connection was the missing ingredient.

<sprscript-green>The Challenge<sprscript-green>

<h3>Keeping members engaged beyond the workout</h3>
Acme Fitness faced a familiar problem: users would log workouts for a few weeks, then drop off. The app lacked any social layer — no way to share progress or find workout partners.

They needed a solution that could deliver community features at the quality level their 3M+ users expected, without rebuilding their app architecture.

<sprscript-green>Why social.plus<sprscript-green>

<h3>Infrastructure-grade social, without the infrastructure burden</h3>
After evaluating three providers, Acme chose social.plus for its pre-built UIKits and flexible SDK. The team integrated Activity Feeds and Group Chat within four weeks.

Note: the text after each `<h3>` always starts on the next line, never on the same line as the heading tag.

### Sidebar

**Sidebar | About** (`sidebar-about`, PlainText)
1–2 sentences. Factual, third person. Format: **what they are + scale indicator + distinct positioning angle**. Do NOT include founding year or headquarters — those live in dedicated sidebar fields (`sidebar-location`) and repeating them here is redundant.

Reference patterns from existing live stories:
- "Snai is Italy's favorite sports betting platform with millions of users and a retail network of 1,500+ locations offering gaming and entertainment services."
- "Talkspace is a leading virtual mental health care provider with 5,000+ licensed clinicians, delivering accessible, evidence-based care to over 130 million people through health plans, employers, and institutions."

**Sidebar | Location** (`sidebar-location`, PlainText)
Company headquarters. Format: "City, Country" or just "Country". Examples: "São Paulo, Brazil", "United States", "Limassol, Cyprus".

**Sidebar | Use Cases** (`new-use-cases`, MultiReference)
References to Use Case CMS items. Tell the user which use cases apply so they can link them in Webflow.

**Valid options (from the `🗳️ Use Cases` collection in Webflow, verified 2026-04-22):** Events, Live Chat, Group Chat, 1-1 Chat, Custom Posts, Polls, Stories & Clips, Live Stream, Groups, User Profiles, Activity Feed. Do not invent labels outside this list — these are CMS reference items and must match exactly.

**Sidebar | Implementation** (`implementation-web`, `implementation-mobile-app`, Switches)
Tell the user which to toggle: Web, App, or both.

**Sidebar | SDK and UIKit** (`sdk`, `uikit`, MultiReference)
Tell the user which SDKs and UIKits the customer uses, if known.

**Sidebar | UIKit Customization** (`uikit-customization`, Option)
Options: Low, Medium, High, Custom UI. Indicate which applies based on how heavily the customer customized the UI.

### Meta

**Meta Description** (`meta-description`, PlainText)
SEO meta description, under 155 characters. Pattern: "Discover how [Company] [outcome] with social.plus. [Key metric or detail]."

### Display controls (tell the user to set these)

- **Order and ID** — The user assigns this based on where they want the story in the list.
- **Industry** — Tell the user which industry reference(s) to link.
  **Valid options (from the `↳ Customer Stories - Industry References` collection, verified 2026-04-22):** Health & Wellness, Healthcare, Sports, Software, News & Media, Lifestyle & Community, Travel & Hospitality, Gaming, Fitness, Fintech, Education, E-commerce & Retail, Betting, Automotive, Other. Pick the closest match and state it explicitly; use "Other" only if none apply. Note that **Health & Wellness** (consumer wellness/fitness apps) and **Healthcare** (clinical or provider-facing) are distinct — pick the right one.
- **Show on homepage / /chat / /social / /video** — Recommend which product pages should feature this story based on what the customer uses.
- **Show on industry pages** — Recommend which industry page toggles to enable.
- **Demo Link** — If a demo exists, format: `https://www.social.plus/demo/[slug]`

## Output format

Two delivery modes, depending on whether the user has the `webflow-socialplus` MCP connector activated:

- **Connector activated** → Use `collections_items_create_item` on the `💼 Customer Stories` collection to create a new **draft** item (do not auto-publish). Populate each field with the values produced per the Webflow CMS field mapping above. For MultiReference fields (`Sidebar | Use Cases`, `Industry`, `SDK`, `UIKit`), first look up item IDs via `collections_items_list_items` on the corresponding reference collection, and pass the IDs — never the display names. Report back with a link to the draft, the list of fields populated, and any fields that were skipped so the user can fill them in manually before publishing.
- **Connector not activated** → Produce the field-by-field paste-ready doc shown below. The user copies each value into the corresponding Webflow CMS field manually.

Present the paste-ready output as a clearly labeled field-by-field mapping. Example structure:

```
## [Company Name] — Customer Story

**Name Company:** [value]
**Slug:** [value]
**Hero Title:** [value]
**Hero Introduction Paragraph:** [value]
**Meta Description:** [value]

**Metric Box 1:**
[HTML]

**Metric Box 2:**
[HTML]

**Metric Box 3:**
[HTML]

**Thumbnail Metric:** [value]
**Thumbnail Metric Description:** [value]

**Top Quote:** [quote or "N/A — no quote provided"]
**Top Quote | Name:** [value]
**Top Quote | Job Title:** [value]

**Customer Story (body):**
(Output the full body as raw text below this label — NOT in a code block. The user copies everything between this label and the next field label directly into Webflow's rich text HTML source.)

**Sidebar | About:** [value]
**Sidebar | Location:** [value]
**Sidebar | Use Cases:** [list]
**Sidebar | Implementation:** Web: [yes/no] | App: [yes/no]
**Sidebar | SDK:** [list or "Ask customer"]
**Sidebar | UIKit:** [list or "Ask customer"]
**Sidebar | UIKit Customization:** [Low/Medium/High/Custom UI]

**Display recommendations:**
- Industry: [recommendation]
- Show on homepage: [yes/no]
- Show on /social: [yes/no]
- Show on /chat: [yes/no]
- Show on /video: [yes/no]
- Industry pages: [list]
- Demo link: [URL or "N/A"]
```

## What NOT to do

- Never fabricate metrics, quotes, or customer statements. If the user doesn't provide numbers, ask — leave the field empty rather than inventing data.
- Never introduce a customer name the user didn't provide. If the user names a customer, proceed — don't interrogate them about contractual approval, NDA coverage, legal sign-off, or brand-usage permission. Those belong to their team, not to you.
- Never open with a "critical pause," "critical gate question," or a conditional "if yes… if no, we stop" framing. The writer is a social.plus marketing professional, not a liability to be vetted. Just start Step 1a.
- Never speculate about a third party's legal posture or brand-usage practices (e.g. "their legal team is aggressive," "this invites a C&D"). That's noise, not value.
- Never quote the skill's own rules at the user as disclaimers or justifications ("the skill forbids…," "the skill requires…"). The rules are for you — follow them silently, don't narrate them.
- Never reference UI affordances that don't exist ("elicitation form," "form widget," "modal"). Use a plain-text question list.
- Never overstate social.plus's role. The customer built their experience; social.plus provided the infrastructure.
- Never use competitor names unless the user specifically requests a comparison angle.
- Never use the `<sprscript-green>` tags for anything other than section headers (The Challenge, Why social.plus, Implementation, The Results).

## Before delivering

Run the compliance check from `brain.md`. Customer stories are permanent, public-facing assets — a terminology violation or fabricated claim lives on the website indefinitely.

