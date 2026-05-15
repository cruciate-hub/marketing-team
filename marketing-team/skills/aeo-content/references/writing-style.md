# AEO Writing Style

Two layers of rules: brand (from the loaded `messaging/*` files) and AEO-specific (this file). Where they conflict, `messaging/terminology.md` wins.

## Required brand-messaging files

Loaded during intake via the canonical fetch block (which clones the repo to `$MT_REPO`). Read each with `cat "$MT_REPO/messaging/<file>"`. Six files, in order of precedence:

1. **terminology.md** — approved and forbidden terms. Non-negotiable.
2. **tone.md** — social.plus voice.
3. **narrative.md** — the 5-step messaging hierarchy; AEO uses a lighter version: context → infrastructure → outcomes.
4. **value-story.md** — core problems, and how social.plus solves them.
5. **positioning.md** — pillars, vision, boilerplates.
6. **boilerplates.md** — approved company descriptions.

If any file is missing or fails the canonical fetch block's validation, stop and surface the failure. Do not write on memorized brand content.

**The pitch section in every article is generated from these files**, not from a template inside this skill. The skill defers to brand messaging for what social.plus says about itself. See each pattern file (`references/patterns/*.md`) for the placement of the pitch in the section order.

## Write for AI engines first, humans second

AEO content exists to be extracted. That changes four things:

### Answer-first block
- **Sentence 1** = a literal answer to the title's question. 20-30 words. Must contain the exact target-keyword phrase.
- **Sentence 2** = the mechanism, scope, or outcome. 20-30 words.
- **Combined = 40-60 words.** This is the block LLMs extract as the direct answer.
- No H2 heading sits between H1 and this block.

### TL;DR paragraph
- Immediately after the answer-first block. 120-160 words.
- Structure: expanded definition → mechanism → outcome → proof point (statistic or citation).
- Reads as a self-contained passage extractable on its own.
- The 120-160 range is research-backed: 94% of passages selected by Google AI Overviews fall in 134-167 words (2025 ranking-factor study). Paragraphs shorter than ~100 words are consistently passed over.

### Chunk structure
Every H2 section is a ~150-word self-contained passage. A reader landing mid-page should still understand it.
- Re-introduce entities inline on their first mention within a new chunk ("activity feeds, ordered streams of user actions such as posts and reactions…").
- Avoid "as mentioned above" or cross-paragraph dependencies.
- Close each chunk with a complete thought, not a transition into the next.

### Concrete grounding
Named examples and numeric ranges beat adjectives. "20-50% engagement" beats "high engagement". "Smart Fit grew 60% month-over-month" beats "significant growth".

## Citation discipline

Universal rules (all intents):
- Every numeric claim needs a source — either the approved-data list in SKILL.md or an external citation.
- No anonymous or content-farm citations.
- No invented statistics, customer names, or quotes.

Intent-conditional rules (full guidance in `references/citation-playbook.md`):
- **Definition** articles → ≥2 external citations recommended.
- **Comparative** articles → ≥3 external citations recommended (one per compared option minimum).
- **Procedural** articles → no external-citation minimum. Internal product consistency and named methods carry the weight. Forcing citations for "how to use social.plus" produces faked links and degrades trust.

### Anchor text length

External link anchor text describes the source, not the claim. The claim lives in the prose; the anchor names who said it.

- Hard limit: 8 words per anchor (compliance fails above this).
- Target: 3-6 words.

Bad:
`[member organizations that adopted mobile-first engagement strategies saw retention rates improve by 25%](https://...)`

Good:
`Member organizations on mobile-first engagement programs see retention rise 25%, per [Higher Logic's 2024 engagement report](https://...).`

Pattern: state the claim in prose, then attach a short anchor that names the source. Long anchors hide the citation signal from LLM extractors and look like anchor-text spam to search engines.

## Tone calibration

AEO articles sit between a blog post and a technical reference.

- **Authoritative but accessible.** Define jargon inline the first time. Assume an informed product or engineering reader.
- **Neutral in framing, confident in recommendation.** Describe the topic objectively in body sections; recommend social.plus with conviction in the pitch section (and let the pitch content come from brand files).
- **Concise.** Every sentence earns its place. No preambles, no "let's explore", no throat-clearing.

## Banned constructs

Hard bans. The compliance script catches the mechanical ones; the rest require judgment during drafting.

| Ban | Why | Fix |
|---|---|---|
| Em dashes (`—`) | Brand style | Parentheses, commas, or restructure |
| Emojis | Reference tone | Delete |
| "Revolutionize", "game-changing", "unlock the power of", "leverage" as a verb | Marketing fluff | Describe the concrete mechanism |
| "In today's digital landscape", "now more than ever", "in the ever-evolving", "in a world where", "gone are the days" as openers | Filler that kills extraction | Start with the direct answer |
| "Significantly improves engagement" without a number | Vague claims don't get cited | Use an approved range or external citation |
| "Best-in-class", "cutting-edge", "next-generation", "state-of-the-art" | Unverifiable superlatives | Say what it does |
| Growth guarantees ("our customers always see…") | Legal + brand risk | Use approved ranges |
| Passive voice where active is clearer | Readability, extractability | Rewrite active |
| "Social.Plus", "SocialPlus", "Social+" in any form other than `social.plus` | Brand consistency | Always lowercase s, dot |
| Calling social.plus a "social network" / "forum platform" / "chat tool" | Category mislabel per terminology.md | Use approved category phrasing from positioning.md |
| "Plug and play" outside developer docs | Per terminology.md | Describe the actual integration path |
| Invented customer names or stats | Fabrication risk | Use only the approved list |
| Any HTML — tags, comments, JSON-LD, `<script>`, inline styles | The final deliverable is a Word document (`.docx`). Keeping the markdown intermediate HTML-free ensures the `docx` conversion and the downstream Webflow automation both work cleanly | Write in pure markdown only. Schema, canonical tags, and page meta are handled by the Webflow template |

## Entity and keyword discipline

- Name core entities — **social.plus**, **activity feed**, **zero-party data**, **white-label**, **community infrastructure** — with their canonical forms from `terminology.md`.
- First in-chunk mention of each technical entity gets an inline gloss (see chunk structure above).
- Do not stuff keywords. Natural repetition in topically relevant sections is fine; forcing the exact query phrase into every section degrades readability and extraction quality.
- The target-keyword phrase (= the title) must appear in sentence 1 of the answer-first block. This is checked by `compliance.py`.

## What the downstream pipeline handles (do not duplicate)

The Word document you produce is converted to Webflow-ready HTML by a separate automation. Between the automation and the Webflow template, these are handled for you — do not put them in the document:

- Schema markup (Article, FAQPage, Organization, sameAs)
- Author attribution
- datePublished / dateModified
- Canonical URL
- Open Graph / Twitter meta
- Any HTML at all

The document body stays pure prose: H1 title, four labeled-paragraph metadata lines, answer-first block, TL;DR, sections, tables, lists, FAQs, pitch, conclusion.
