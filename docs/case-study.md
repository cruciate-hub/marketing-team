# Case Study

Claude skill for writing customer stories that match the exact structure of the social.plus website.

Output maps directly to the Webflow CMS `💼 Customer Stories` collection fields — hero title, metric boxes, quote, customer story body (with custom `<sprscript-green>` section dividers), sidebar, meta description, and display controls.

## What it does

- Fetches the full messaging stack (terminology, tone, narrative, value-story, positioning) plus boilerplates for company descriptions.
- Scans `website/pages-customer-stories.json` for existing stories to avoid contradictions and suggest cross-links.
- Gathers missing customer data (metrics, quotes, implementation details) in a single question round before drafting.
- Produces the full customer story body with the site's custom HTML section dividers, ready to paste into Webflow's HTML source view.
- Recommends sidebar fields (Use Cases, SDKs, UIKits, implementation targets, customization level) and display controls (industry tags, which product pages to feature on).

## When it triggers

When the user wants to create or update a customer story / case study for social.plus. Trigger phrases include "case study", "customer story", "success story", "customer spotlight", "write about how [customer] uses", "write a CS for", or "new customer story".

The skill is not for general blog posts without a customer focus (use `blog-seo-content`).

## Workflow

1. Fetch `brain.md` and `messaging/brain.md`. Load `terminology.md`, `tone.md`, `positioning.md`, `value-story.md`, `narrative.md`, and `boilerplates.md` from `messaging/` (every conditional row in the router except UI applies to customer stories).
2. Fetch `website/pages-customer-stories.json` to check for duplicates and cross-link opportunities.
3. **Auto-research public facts first.** Web-search the customer name for headquarters, founding year, founders, scale indicators, market position, and key product surface. Present findings as a labelled block the writer can edit, not type from scratch.
4. **Ask only for what's genuinely missing.** One consolidated list covering metrics (route to `bq-business-query` against the social.plus warehouse if available — sales-deck and memory-sourced numbers are unreliable), quote, challenge, why social.plus, implementation, results, and use cases. Don't draft with placeholders. Trust the writer's intent — don't gate on NDA / contract / brand-legal questions; those belong to their team.
5. **Ask once whether the `webflow-socialplus` MCP connector is activated.** If yes, the skill creates the customer story directly as a **draft** item in the `💼 Customer Stories` CMS collection via MCP; if no, it produces paste-ready field-by-field output.
6. Produce every CMS field labeled for copy-paste into Webflow (or create the draft via MCP).
7. Run the compliance check from `brain.md`.

## Webflow CMS fields

### Required
- **Name Company** (`name`) — customer's company name, CMS item name.
- **Slug** (`slug`) — lowercase-hyphens, e.g. `smart-fit`, `the-ring-magazine`.

### Hero
- **Hero Title** (`title`) — "How [Company] [past-tense verb] [outcome] with social.plus", under 80 chars where possible.
- **Hero Introduction Paragraph** (`hero-introduction-paragraph`) — 1–2 sentence expansion of the hero title.

### Metrics (up to 3 boxes, custom HTML)

Each box uses custom tags (never wrap in `<p>`):
```html
<big-nr>60%<big-nr><br><cs-number-text>community growth rate MoM<cs-number-text>
```

- **Metric Box 1–3** (`numbers-box-1/2/3`) — company facts, platform stats, or social.plus outcomes. Aim for ≥2 boxes. If the user doesn't provide numbers, ask — don't invent.
- **Thumbnail Metric** (`thumbnail-cs-overview-page-large-metric`) — the single most impressive number (short format: `60%`, `1M`, `4 weeks`).
- **Thumbnail Metric Description** (`thumbnail-cs-overview-page-metric-description`) — one-line lowercase description.

### Quote (optional)
- **Top Quote**, **Top Quote Name**, **Top Quote Job Title** — only if the user provides a real quote. Never fabricate.

### Body (`section-2-text`, RichText)

Follows a consistent section pattern:

1. **Opening paragraphs** (2–3) — company background and context as narrative prose.
2. **The Challenge** — `<sprscript-green>The Challenge<sprscript-green>` divider, then `<h3>` framing the problem, then 2–3 paragraphs mapping to core problems from `value-story.md`.
3. **Why social.plus** — `<sprscript-green>Why social.plus<sprscript-green>` divider, then `<h3>` and paragraphs on selection rationale using product-pillar language from `positioning.md` (customer stays the subject).
4. **Implementation** (optional) — `<sprscript-green>Implementation<sprscript-green>` — SDKs, UIKits, customization, timeline.
5. **The Results** (optional) — `<sprscript-green>The Results<sprscript-green>` — quantified outcomes mapped to the value creation model (functional → strategic → economic → compounding).

### Body formatting rules

- Output the body as **raw text** (not in a code fence, not rendered markdown). User pastes directly into Webflow's HTML source view.
- **No `<p>` tags anywhere.** Webflow handles paragraph formatting.
- `<sprscript-green>` tags stand alone on their own line, bare (no `<p>`, no wrapper). JavaScript on the site picks these up as styled section dividers.
- `<h3>` tags stand alone; paragraph text that follows starts on the **next line**, never on the same line as `</h3>`.
- Separate paragraphs with blank lines.
- Target length: 4,000–7,000 characters.
- The customer is the hero. social.plus is the tool they chose — write "they implemented," not "we provided."

### Sidebar
- **About** — 2–3 sentences: what they do, founding year or scale, headquarters/region.
- **Location** — "City, Country" or just "Country".
- **Use Cases** — multi-reference to Use Case CMS items. Canonical list (verified 2026-05-12): 1-1 Chat, Activity Feed, Custom Posts, Events, Group Chat, Groups, Live Chat, Live Commerce, Live Stream, Polls, Social Commerce, Stories & Clips, User Profiles.
- **Implementation** — Web / App toggles.
- **SDK** and **UIKit** — multi-reference lists; say "Ask customer" if unknown.
- **UIKit Customization** — Low / Medium / High / Custom UI.

### Meta
- **Meta Description** — ≤155 chars. Pattern: "Discover how [Company] [outcome] with social.plus. [Key metric or detail]."

### Display controls
- Order and ID, Industry reference, show-on-page toggles (homepage, `/social`, `/chat`, `/video`), industry page toggles, demo link.

## Files

```
case-study/
├── SKILL.md                          Skill entry point — CMS field mapping, body structure
└── README.md                         This file
```

## What NOT to do

- Never fabricate metrics, quotes, or customer statements. Ask — leave fields empty rather than invent data.
- Never name a customer without explicit permission.
- Never overstate social.plus's role. The customer built their experience; social.plus provided infrastructure.
- Never use competitor names unless the user requests a comparison angle.
- Never use `<sprscript-green>` tags for anything other than section dividers (The Challenge, Why social.plus, Implementation, The Results).

## URL format

All reference files are loaded from a shallow clone of this repo (`git clone --depth 1`) into `$MT_REPO`. The canonical fetch block at the top of each SKILL.md handles the clone; skills then read files with `cat "$MT_REPO/<path>"`.
