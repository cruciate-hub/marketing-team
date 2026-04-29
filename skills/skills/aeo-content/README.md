# AEO Content (v2)

Claude skill for writing AEO (Answer Engine Optimization) articles for `social.plus/answers/[slug]`. Designed to be cited by ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews, and Copilot.

**New to this skill?** Start with [USAGE.md](USAGE.md) — a step-by-step guide for colleagues using the skill. The rest of this file is maintainer-focused.

## What this skill does

Two modes, chosen from the brief:

### Single article
1. Asks for topic + intent (definition / procedural / comparative).
2. Checks `pages-answers.json` for duplicates.
3. Fetches the brand-messaging stack from GitHub.
4. Surfaces real PAA-based FAQ questions before writing.
5. Drafts the article with an answer-first block, self-contained chunks, and intent-appropriate citation density.
6. Delegates internal linking to `internal-linking-optimizer`.
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
- Social media posts → `social-media`
- Website page copy → `brand-messaging`
- Ad copy → `campaign-copy`

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
    ├── fetch_brand.py                   GitHub blob-HTML fetcher for brand-messaging files
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

[Answer-first block — sentences 1-2, 30-50 words combined]

[TL;DR paragraph — 80-120 words]

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

The 20 checks:

| Category | Checks |
|---|---|
| Metadata | H1 title, Meta description, Slug, Alt text, Intent (+ intent validity) |
| Length | meta description ≤160 chars; word count inside intent-specific typical range (WARN, not fail) |
| Answer-first | sentences 1-2 in 30-50 word range; target-keyword phrase in sentence 1 |
| Style | no em dashes, no emojis, no forbidden terms, no filler openers |
| Structure | no HTML of any kind (tags, comments, JSON-LD); single H1; no skipped heading levels |
| Citations | intent-conditional minimum (definition ≥2, comparative ≥3, procedural any) |
| Claims | approved-customer whitelist (Noom, Harley-Davidson, Smart Fit, Ulta Beauty, Betgames) |

## Brand-fetch helper — local use

```bash
# Fetch all six brand files to stdout
python3 scripts/fetch_brand.py

# Single file
python3 scripts/fetch_brand.py --file tone.md

# Write to a directory
python3 scripts/fetch_brand.py --out /tmp/brand/
```

Uses `github.com/.../blob/...` URLs exclusively — raw and API hosts are blocked by runtime network egress. Extraction uses stdlib `html.parser` with a regex fallback; fetches retry with exponential backoff on transient errors.

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
- `internal-linking-optimizer` — called by this skill to add internal links; do not re-implement
- `blog-seo-content` — long-form blog posts, pillar pages (see boundary note above)
- `case-study` — customer stories
- `social-media` — LinkedIn, Instagram, X
- `brand-messaging` — website and general copy
- `campaign-copy` — paid-campaign copy
- `site-intelligence` — content audits beyond `pages-answers.json`

## Research sources that shaped this skill

- [Aggarwal et al., "GEO: Generative Engine Optimization" (arxiv 2311.09735)](https://arxiv.org/abs/2311.09735)
- [Semrush — AI Search SEO Traffic Study 2025](https://www.semrush.com/blog/ai-search-seo-traffic-study/)
- [Semrush — Most-Cited Domains in AI](https://www.semrush.com/blog/most-cited-domains-ai/)
- [Conductor — 2026 AEO/GEO Benchmarks](https://www.conductor.com/academy/aeo-geo-benchmarks-report/)
- [Anthropic — Agent Skills docs](https://code.claude.com/docs/en/skills)
- [anthropics/skills — skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
- [obra/superpowers — writing-skills lessons](https://github.com/obra/superpowers/tree/master/skills/writing-skills)
