# AEO Content (v3)

Claude skill for writing AEO (Answer Engine Optimization) articles for `social.plus/answers/[slug]`. Designed to be cited by ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews, and Copilot.

The rest of this file is maintainer-focused. The next section is a step-by-step guide for colleagues using the skill; everything below that is for maintainers.

## Getting started

A step-by-step guide to your first AEO article and your first batch.

AEO articles are reference pages that sit at `social.plus/answers/[slug]`. They are built to be indexed and cited by ChatGPT, Claude, Perplexity, Gemini, and Google AI Overviews.

---

### Before you start

- A Claude Cowork account (claude.ai)
- About 5 minutes for the one-time install

---

### 1. Install (one-time, ~3 min)

#### Step 1 — Install the team plugin

1. Open Claude Cowork.
2. Click **Customize** in the sidebar.
3. Next to **Personal plugins**, click **+**.
4. Click **Browse plugins** → open the **Personal** tab.
5. Click the **+** → select **Add marketplace**.
6. Enter `cruciate-hub/marketing-team` → click **Sync**.
7. Click the **+** to install.

#### Step 2 — Install `anthropic-skills` (needed for Word output)

Still in **Browse plugins**:

1. Switch to the **Anthropic** tab.
2. Find `anthropic-skills`.
3. Click the **+** to install.

If `anthropic-skills` is not listed in the Anthropic tab, your Cowork already has it pre-installed — skip this step.

#### Step 3 — Optional: connect Ahrefs

If your team has an Ahrefs subscription, connecting it improves keyword research and the quality of suggested FAQ questions.

1. **Customize** → **Connectors** in the sidebar.
2. Find **Ahrefs** → click **Connect**.
3. Follow the OAuth flow.

Without Ahrefs, the skill falls back to generic WebSearch and still works — just with less precise data.

---

### 2. First test (2 min)

Start a new chat and type something like:

> `I need an answer page for /answers/ on in-app activity feeds.`

Or, in plain English:

> `Help me draft an /answers/ article explaining what in-app activity feeds are.`

You do not need to say "AEO" or "GEO" — the skill picks itself up from "/answers/" or "answer page."

What should happen:

1. It fetches the brand-messaging files from GitHub.
2. It drafts the article (about 90 seconds).
3. It runs compliance checks automatically.
4. It hands you a `.docx` file to download from the artifact panel.

If all four things happen, you're set. The skill should not ask you any questions when the brief is clear. It may ask a single clarifying question if something is genuinely ambiguous (for example, "feeds" could mean activity feeds, news feeds, or RSS). If it asks more than one question, something is off — flag it.

---

### 3. Writing one article

When you want a single AEO answer article:

1. **Start a chat** and describe what you want in plain English. Mentioning "/answers/" or "answer page" is usually enough for the skill to pick up. Examples:
   - `Draft an answer page on how to add chat to a mobile app.`
   - `I need an /answers/ article explaining zero-party data.`
   - `Help me write a comparison page for /answers/ — activity feeds vs group chats.`
   - `Can you create an answer page about community moderation for consumer apps?`
2. **Wait for the draft**. The skill does not ask intake questions when the brief is clear — it goes straight to drafting. The draft appears in the artifact panel in about 90 seconds. If the skill does ask a clarifying question (rare — only when the topic itself is ambiguous), answer it and move on.
3. **Ask for edits in chat**. Examples:
   - `make the intro shorter`
   - `add a pitfalls section`
   - `focus the pitch on retention, not engagement`
   - `rewrite FAQ 3 to be about moderation`
4. **Download**. When you are satisfied, the skill delivers a `.docx`. Click it in the artifact panel to download.

---

### 4. Writing a batch

When you want multiple articles in one session:

#### Phase A — Ideas

Ask for ideas:

> `Give me 5 /answers/ ideas around community infrastructure for fitness apps.`

The skill produces a list of 8-15 candidates with title, intent, rationale, target keyword, and fit score.

Approve what you like in chat:

```
approve: 1, 3, 5, 7, 9
drop: 2, 8
revise: 4 — shift to retention angle
next
```

#### Phase B — FAQ questions

For each approved idea, the skill surfaces 8-10 candidate FAQ questions (real ones from search results).

Approve per article:

```
article 1: approve 1-4, drop 5
article 2: approve 1, 3, 5; revise 2 — drop the pricing angle
article 3: approve 1, 2, 4, 6
next
```

#### Phase C — Drafts

The skill drafts every approved article. You will see a summary with word count and compliance status per article.

Edit any specific draft in chat:

```
article 2: shorter
article 3: add a pitfalls section
article 1: make the pitch more specific
```

The skill edits that draft, re-runs compliance, and updates the summary.

#### Phase D — Deliver

When you are happy, type:

```
deliver
```

The skill produces one `.docx` per article plus a batch `.zip` containing all of them. Each `.docx` and the `.zip` appear in the artifact panel as downloadable files.

---

### 5. Approval syntax cheat sheet

| Command | What it does |
|---|---|
| `approve: 1, 3, 5` | Keep items 1, 3, 5 |
| `approve: 1-4` | Keep items 1 through 4 |
| `drop: 2, 6` | Remove items 2 and 6 |
| `revise: 4 — [instruction]` | Update item 4 with your instruction |
| `article 2: approve 1-3` | In Phase B, scope to article 2 |
| `next` | Move to the next phase |
| `deliver` | (Phase C only) produce the final `.docx` files |

Free-form messages also work. "Make number 3 more technical" will be understood — the skill falls back to natural language when the message does not match the structured syntax.

---

### 6. Troubleshooting

| Symptom | What to do |
|---|---|
| The skill does not trigger | In **Customize** → **Personal plugins**, confirm `marketing-team` is enabled. If an update badge shows, click the three dots → **Update**. |
| The skill produces a `.md` file instead of a `.docx` | `anthropic-skills` is not installed. Install it from **Browse plugins** → **Anthropic** tab. |
| Brand fetch fails | Reply `retry brand fetch`. If it keeps failing, ping the team — it is usually a GitHub access issue. |
| A customer name you don't recognize appears | Reply `stop, [customer name] is not approved`. Only Noom, Harley-Davidson, Smart Fit, Ulta Beauty, and Betgames are pre-cleared. |
| Compliance fails repeatedly on the same check | Tell the skill what you want: `the TL;DR is fine as-is, skip that check`. The skill can override specific warnings. |
| The article mentions a stat you can't verify | Reply `where is that stat from`. Only the approved ranges (20-50% engagement, 10-35% retention lift, 10-30% active contributors) and published customer stats are pre-cleared. |

---

### 7. Where your articles end up

The skill gives you `.docx` files. A separate automation (outside this skill) converts each `.docx` into Webflow-ready HTML and publishes it to `social.plus/answers/[slug]`. Your job is to produce the `.docx`; the rest is automatic.

---

### 8. What this skill does NOT do

This skill is only for AEO answer articles. For other content types, switch skills:

| You want to write | Use |
|---|---|
| Blog post for social.plus/blog | `blog-seo-content` |
| Customer story / case study | `case-study` |
| Website page copy | `brand-messaging` |
| Monthly newsletter or release email | `newsletters` |

If you ask this skill for something outside its scope (e.g., "write a LinkedIn post"), it will redirect you to the right one.

## What this skill does

Two modes, chosen from the brief:

### Single article
1. Asks for topic + intent (definition / procedural / comparative).
2. Checks `pages-answers.json` for duplicates.
3. Fetches the brand-messaging stack from GitHub.
4. Surfaces real PAA-based FAQ questions before writing.
5. Drafts the article with an answer-first block, self-contained chunks, and intent-appropriate citation density.
6. Delegates internal linking to `internal-linking-strategist`.
7. Runs the deterministic compliance script.
8. Converts the markdown intermediate to `.docx` via `anthropic-skills:docx`.

### Batch (multiple articles, themed, or "ideas")
Four phases, each producing a markdown artifact for chat-based approval:

- **Phase A — Ideas.** Skill produces `outputs/ideas.md` (8-15 candidates with title, intent, rationale, target keyword, fit). Colleague approves a subset via chat.
- **Phase B — Questions.** For each approved idea, skill runs PAA research (Ahrefs MCP preferred, WebSearch fallback) and writes `outputs/questions.md` (8-10 questions per article). Colleague approves per-article.
- **Phase C — Drafts.** Skill drafts each approved article into `outputs/[slug].draft.md` and writes `outputs/overview.md` as a batch-wide status table. Colleague chats edits; skill updates individual drafts and re-runs compliance.
- **Phase D — Delivery.** When all drafts pass compliance, skill converts each to `.docx` via `anthropic-skills:docx`, bundles them into `outputs/aeo-batch-YYYY-MM-DD.zip` via `scripts/make_zip.py`, and sends a final chat summary with file list + FAQ source URLs.

Full phase specs with artifact schemas: `references/workflow-phases.md`. Samples of Phase A and B artifacts: `examples/ideas-sample.md`, `examples/questions-sample.md`.

## Approval syntax (batch mode)

```
approve: 1, 3, 5-7
drop: 2, 6
revise: 4 — make it about retention
next
```

Per-article scope in Phase B:
```
article 1: approve 1-4, drop 5
article 2: approve 1, 3, 5; revise 2 — focus on operational load
next
```

Free-form chat also works — the skill falls back to natural-language understanding when a message doesn't match.

## When to use / not to use

**Use when:** the colleague asks for an AEO article, GEO article, answer article, AI-search-optimized content, batch of answer ideas, or content for `/answers/`.

**Do not use for:**
- Regular blog posts → `blog-seo-content`
- Customer stories → `case-study`
- Website page copy → `brand-messaging`

## File layout

```
aeo-content/
├── SKILL.md                             Entry point — standing rules, both modes, approval syntax
├── README.md                            This file
├── references/
│   ├── workflow-phases.md               Detailed spec of Phase A/B/C/D artifacts and approval flow
│   ├── patterns/
│   │   ├── definition.md                "What is X?" structure
│   │   ├── procedural.md                "How to X?" structure
│   │   └── comparative.md               "X vs Y" structure
│   ├── writing-style.md                 Brand + AEO writing rules, banned constructs, no-HTML rule
│   └── citation-playbook.md             Intent-conditional citation density rules
├── examples/
│   ├── activity-feeds.md                Single-article exemplar (passes compliance)
│   ├── ideas-sample.md                  Phase A artifact sample
│   └── questions-sample.md              Phase B artifact sample
└── scripts/
    ├── compliance.py                    Deterministic compliance checker (20 checks)
    ├── duplicate_check.py               Jaccard-similarity dedupe against `pages-answers.json` and `pages-glossary.json`
    └── make_zip.py                      Bundles `outputs/*.docx` into a timestamped batch zip
```

## Output contract

**Single deliverable per article: a `.docx` Word document.** The markdown intermediate (`[slug].draft.md`) is kept alongside for diff-able revisions. A separate automation (outside this skill) converts each `.docx` to Webflow-ready HTML and publishes at `/answers/[slug]`.

Because the output is Word, **no HTML of any kind appears in the document** — no JSON-LD, no `<script>`, no `<!-- comments -->`. Schema markup, canonical URLs, author, dates, and OG meta are handled by the Webflow template + downstream automation.

The markdown intermediate uses labeled paragraphs for metadata (not YAML frontmatter, which doesn't survive docx conversion):

```
# Article title

Meta description: ≤160 chars including spaces
Slug: lowercase-with-hyphens
Alt text: Abstract visualization of [main topic]
Intent: definition | procedural | comparative

[Answer-first block — sentences 1-2, 40-60 words combined]

[TL;DR paragraph — 120-160 words]

## First body section
...
```

## Compliance checker — local use

```bash
# Intent auto-detected from the Intent: metadata line
python3 scripts/compliance.py outputs/my-article.draft.md

# Override intent (useful before metadata is final)
python3 scripts/compliance.py outputs/my-article.draft.md --intent procedural

# Override word-count range
python3 scripts/compliance.py outputs/my-article.draft.md --min 900 --max 1400

# Machine-readable
python3 scripts/compliance.py outputs/my-article.draft.md --json
```

Exit 0 if no failures (warnings allowed), 1 if any failure.

The 22 checks:

| Category | Checks |
|---|---|
| Metadata | H1 title, Meta description, Slug, Alt text, Intent (+ intent validity) |
| Length | meta description ≤160 chars; word count inside intent-specific typical range (WARN, not fail) |
| Answer-first | sentences 1-2 in 40-60 word range; TL;DR in 120-160 word range; target-keyword phrase in sentence 1 |
| Style | no em dashes, no emojis, no forbidden terms, no filler openers |
| Structure | no HTML of any kind (tags, comments, JSON-LD); single H1; no skipped heading levels |
| Citations | intent-conditional minimum (definition ≥2, comparative ≥3, procedural any) |
| Internal linking | at least one social.plus internal link present (WARN only — flags when `internal-linking-strategist` was skipped) |
| Claims | approved-customer whitelist (Noom, Harley-Davidson, Smart Fit, Ulta Beauty, Betgames) |

## Brand-file loading

Brand-messaging files (`messaging/terminology.md`, `messaging/tone.md`, `messaging/narrative.md`, `messaging/value-story.md`, `messaging/positioning.md`, `messaging/boilerplates.md`) are loaded by the canonical fetch block at the top of the SKILL.md, which shallow-clones the repo to `$MT_REPO`. Skills then read each file with `cat "$MT_REPO/messaging/<file>"`. There is no separate fetch helper — the fetch block is the contract.

## Duplicate-check helper — local use

```bash
# Run from the cloned repo path (default $MT_REPO or /tmp/cruciate-hub-marketing-team)
MT_REPO=/tmp/cruciate-hub-marketing-team python3 scripts/duplicate_check.py "in-app activity feeds"

# Custom threshold
python3 scripts/duplicate_check.py "activity feeds" --threshold 0.5

# Custom repo path
python3 scripts/duplicate_check.py "..." --repo /custom/path

# Machine-readable
python3 scripts/duplicate_check.py "zero-party data" --json
```

Exit codes: 0 = clean, 1 = duplicates found, 2 = unverified (could not read snapshots — re-run the canonical fetch block first).

## Batch zip helper — local use

```bash
# Zip every .docx in outputs/ into outputs/aeo-batch-YYYY-MM-DD.zip
python3 scripts/make_zip.py

# Custom output path
python3 scripts/make_zip.py --out outputs/custom-batch.zip

# Specific files only
python3 scripts/make_zip.py --files outputs/a.docx outputs/b.docx
```

## Boundary with `blog-seo-content`

This skill and `blog-seo-content` are explicitly separated to prevent router collisions. In a real Cowork session, a colleague typed "write an AEO article on ..." and the router loaded `blog-seo-content` instead — "AEO" and "SEO" differ by one letter, and the blog skill's larger trigger list was dominating the embedding match. Both skills' `description:` fields now include explicit anti-triggers pointing at each other, plus a reminder that AEO articles go to `/answers/` as `.docx` files while SEO blog posts go to the blog as markdown. **Do not weaken the anti-trigger wording in this skill's description without making the matching edit in `blog-seo-content/SKILL.md`** — drop one side and the collision returns. Any request mentioning AEO, GEO, answer pages, `/answers/`, AI citation, or AI search must route here, not to the blog skill.

## Related skills

- `anthropic-skills:docx` — called by this skill in Phase D to produce the final `.docx`
- `internal-linking-strategist` — called by this skill to add internal links; do not re-implement
- `blog-seo-content` — blog posts for social.plus/blog (see boundary note above)
- `case-study` — customer stories
- `brand-messaging` — website and general copy
- `site-intelligence` — content audits beyond `pages-answers.json`

## Research sources that shaped this skill

- [Aggarwal et al., "GEO: Generative Engine Optimization" (arxiv 2311.09735)](https://arxiv.org/abs/2311.09735)
- [Semrush — AI Search SEO Traffic Study 2025](https://www.semrush.com/blog/ai-search-seo-traffic-study/)
- [Semrush — Most-Cited Domains in AI](https://www.semrush.com/blog/most-cited-domains-ai/)
- [Conductor — 2026 AEO/GEO Benchmarks](https://www.conductor.com/academy/aeo-geo-benchmarks-report/)
- [Anthropic — Agent Skills docs](https://code.claude.com/docs/en/skills)
- [anthropics/skills — skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
- [obra/superpowers — writing-skills lessons](https://github.com/obra/superpowers/tree/master/skills/writing-skills)
