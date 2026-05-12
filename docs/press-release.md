# Press Release

Claude skill for newswire-ready press releases for social.plus, produced as `.docx` files ready to upload to PR Newswire (Cision) or hand to any agency. Format-agnostic enough to also work for direct media pitches and the social.plus newsroom.

## What it does

- Fetches the full messaging stack (terminology, tone, narrative, value-story, positioning, boilerplates) plus press-release-specific references (structure template, release-type playbooks, brief template, quote engineering, anti-patterns, best-in-class corpus, gold-standard example).
- Determines release type from the brief (product launch / funding / partnership / customer win / exec hire / milestone / award / acquisition) and applies the matching lede formula.
- Drafts the release through a 12-block skeleton: FOR IMMEDIATE RELEASE → headline → subhead → dateline lede → narrative body → exec quote → product/proof detail → customer or partner quote → industry framing → availability → boilerplate → media contact → end marker.
- Runs the anti-patterns self-review (banned phrases, buried lede, quote-as-summary, passive voice in lede, AP-style compliance, word-count band per release type).
- Generates the `.docx` via the bundled `python-docx` script with proper formatting (18pt bold headline, italic grey subhead, bold dateline + plain lede in one paragraph, lead-phrase-bolded detail paragraphs, indented italic-attributed quote blocks, centered `###` end marker).
- Runs the brand compliance check before delivery.

## When it triggers

When the user needs a press release, newswire release, embargoed announcement, or formal media announcement. Trigger phrases include "press release", "newswire", "PR Newswire", "Cision", "embargoed announcement", "press announcement", "media release", "draft a release for", "write a release about", or "announcement for the wire".

The skill is not for blog posts (use `blog-seo-content`), email campaigns (use `newsletters`), or customer case studies (use `case-study`).

## The brief — three required fields

Every release starts with a brief. If any required field is missing or thin, the skill uses `AskUserQuestion` before drafting:

1. **Announcement + key facts** — what's being announced, release type, key numbers/dates/names/geographies, why now (the news hook).
2. **Target audience + angle** — who it's for, the single sentence capturing why it matters to them, the category/industry shift it connects to.
3. **Customer or partner quote(s)** — exact text (never paraphrased), speaker full name, title, company.

The skill provides the rest. **Executive quote**: drafted in the named speaker's voice for review (brief gives speaker name + title only). **Dateline**: defaults to `LONDON, [today's date]`. **Boilerplate**: defaults to the approved version from `boilerplates.md`. **Media contact**: defaults to `marketing@social.plus | social.plus`.

## Workflow

1. Fetch `brain.md` and `messaging/brain.md`. Load `terminology.md`, `tone.md`, `positioning.md`, `value-story.md`, `narrative.md`, and `boilerplates.md` from `messaging/`.
2. Load press-release-specific references from the skill folder: `structure-template.md`, `release-type-playbooks.md`, `brief-template.md`, `quote-engineering.md`, `anti-patterns.md`, `best-in-class-corpus.md`, plus `examples/commerce-launch.md` (the gold-standard).
3. Intake and validate the brief. Fill missing required fields via `AskUserQuestion`.
4. Determine release type and apply the matching lede formula (Who / What / When / Where in 30 words or fewer, Why in the next sentence).
5. Draft the release following the 12-block skeleton.
6. Self-review against `anti-patterns.md` — banned phrases, buried lede, quote-as-summary, passive voice, AP-style compliance, word-count band (400–800 for product/partnership/milestone, 300–500 for hires and awards, up to 900 for funding).
7. Run `scripts/generate_press_release.py` with the structured release as a JSON payload to produce the `.docx`.
8. Run the compliance check from `brain.md` and deliver.

## Output

A `.docx` named `press-release-<short-slug>-<YYYY-MM-DD>.docx`, ready to upload to a newswire portal.

Format inside:

- `FOR IMMEDIATE RELEASE` (or embargo line) at top
- Bold 18pt headline
- Italic 12pt grey subhead
- Bold dateline + plain lede in one paragraph
- Bold sentence-case section subheads
- Lead-phrase-bolded detail paragraphs (Cloudflare style)
- Indented italic-attributed quote blocks with curly quotes
- About boilerplate (from `boilerplates.md` unless overridden)
- Media Contact block
- Centered `###` end marker

The delivery message includes the `.docx` link, a one-line summary of the release angle, the recommended embargo posture (under embargo until X / for immediate release), and any flags: missing data, claims that need legal review, or customer/partner quote that should be confirmed in writing before distribution.

## What this skill never does

- **Never fabricates quotes from real people.** Executive quotes are drafted in the named speaker's voice for their review. Customer/partner quotes must be supplied verbatim.
- **Never invents metrics, dollar amounts, customer counts, or growth percentages.** If the brief asks for a "big number" without giving one, the skill asks.
- **Never names a customer or partner** unless the brief authorizes it.
- **Never includes forward-looking financial guidance** without explicit instruction.
- **Never publishes without human review.** Output is always a draft for Marketing/PR and the named executive speaker.

## Files

```
press-release/
├── SKILL.md                              Entry point — workflow, brief intake, structure, anti-patterns
├── references/
│   ├── structure-template.md             12-block skeleton, block-by-block spec
│   ├── release-type-playbooks.md         Lede formulas per release type
│   ├── brief-template.md                 Canonical brief shape + worked examples
│   ├── quote-engineering.md              4-rule quote test + drafting patterns
│   ├── anti-patterns.md                  Banned words/phrases + self-review checklist
│   └── best-in-class-corpus.md           Patterns from Stripe / Datadog / Snowflake / etc.
├── examples/
│   └── commerce-launch.md                Gold-standard social.plus release
└── scripts/
    ├── generate_press_release.py         python-docx generator
    └── example_payload_commerce.json     Reference JSON payload
```

## URL format

All reference files are loaded from a shallow clone of this repo (`git clone --depth 1`) into `$MT_REPO`. The canonical fetch block at the top of each SKILL.md handles the clone; skills then read files with `cat "$MT_REPO/<path>"`.
