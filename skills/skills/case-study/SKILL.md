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

## What to do

1. Fetch the main brain for cross-domain routing, precedence rules, and the compliance check:
```
https://github.com/cruciate-hub/marketing-team/blob/main/brain.md
```

2. Fetch the messaging router:
```
https://github.com/cruciate-hub/marketing-team/blob/main/messaging/brain.md
```

3. Follow the messaging router's **"Long-form content"** routing. This loads:
   - `terminology.md` + `tone.md` (always)
   - `narrative.md` (messaging hierarchy and narrative structure)
   - `value-story.md` (value creation model — maps directly to customer story outcomes)
   - `positioning.md` (product pillars for framing the solution)

4. Also follow **"Short-form content"** routing for:
   - `boilerplates.md` (company descriptions for reference)

## Step 1: Gather missing information before drafting

**Before writing anything**, review what the user has provided and ask for any missing information. Do NOT start drafting the customer story until you have enough data to avoid placeholders. Present one clear list of questions — not multiple rounds.

Check for and ask about:
- **Metrics / engagement data** — specific numbers for the metric boxes (e.g., engagement rate increase, user growth, retention lift, integration timeline). Without real numbers, the metric boxes cannot be filled.
- **Customer quote** — do they have a direct quote from the customer? If yes, who said it (name + title)?
- **Challenge details** — what specific problem was the customer trying to solve?
- **Why social.plus** — why did they choose social.plus over alternatives?
- **Implementation details** — which SDKs, UIKits, platforms (web/app), customization level, and timeline?
- **Results / outcomes** — quantified impact after launch.
- **Company basics** — headquarters location, founding year or scale indicator, industry.
- **Use cases** — which social.plus features does the customer use (Activity Feed, Group Chat, Live Chat, Livestream, etc.)?

Only ask about items that are genuinely missing from the user's input — don't re-ask what they already provided. Once you have enough information to write without placeholders, proceed to drafting.

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

Metrics can be: company facts (founded year, employees, revenue), platform stats (users, downloads, locations), or social.plus outcomes (engagement growth, retention lift, integration timeline). Aim for at least 2 boxes. If the user doesn't provide specific numbers, ask — don't invent them.

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
2-3 sentences describing the customer's company. Factual, third person. Include: what they do, founding year or scale indicator, and headquarters/region.

**Sidebar | Location** (`sidebar-location`, PlainText)
Company headquarters. Format: "City, Country" or just "Country". Examples: "São Paulo, Brazil", "United States", "Limassol, Cyprus".

**Sidebar | Use Cases** (`new-use-cases`, MultiReference)
References to Use Case CMS items. Tell the user which use cases apply (e.g., "Activity Feed", "Group Chat", "Live Chat", "Livestream") so they can link them in Webflow.

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
- **Show on homepage / /chat / /social / /video** — Recommend which product pages should feature this story based on what the customer uses.
- **Show on industry pages** — Recommend which industry page toggles to enable.
- **Demo Link** — If a demo exists, format: `https://www.social.plus/demo/[slug]`

## Output format

Present the output as a clearly labeled field-by-field mapping. The user copies each value into the corresponding Webflow CMS field. Example structure:

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
- Never name a customer without explicit permission from the user.
- Never overstate social.plus's role. The customer built their experience; social.plus provided the infrastructure.
- Never use competitor names unless the user specifically requests a comparison angle.
- Never use the `<sprscript-green>` tags for anything other than section headers (The Challenge, Why social.plus, Implementation, The Results).

## Before delivering

Run the compliance check from `brain.md`. Customer stories are permanent, public-facing assets — a terminology violation or fabricated claim lives on the website indefinitely.

## Important: URL format

**Always use `github.com/.../blob/...` URLs when fetching files.** Never attempt `raw.githubusercontent.com` — it is blocked by network egress settings.
