---
name: aeo-content
description: >
  Writes reference-style articles for the social.plus /answers/ collection,
  engineered to be cited by ChatGPT, Claude, Perplexity, Gemini, Google AI
  Overviews, and Copilot. Delivers .docx (a downstream automation converts
  it to Webflow HTML). This skill always wins when the destination is
  /answers/, regardless of subject.

  Do NOT use for: blog posts (use blog-seo-content for non-product topics,
  or brand-messaging for product/feature blogs); customer stories
  (use case-study); website page copy (use brand-messaging); press
  releases (use press-release).
when_to_use: >
  Trigger phrases: "AEO article", "GEO article", "answer page", "content
  for /answers/", "reference article on X", "what is X" reference page,
  "FAQ for /answers/", "glossary entry".
---

# AEO Article Generation

AEO articles live at `social.plus/answers/[slug]`. They exist so large-language models will extract and cite them. Every rule in this skill serves that goal.

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

The Bash tool truncates large stdout when the output exceeds the harness's token/byte cap (observed at ~50 KB in Cowork; varies by environment). When this happens the harness emits one of these signals — both mean the same thing:
- `Output too large (NkB). Full output saved to: …` followed by a short preview, OR
- `Error: result (N characters) exceeds maximum allowed tokens` with no preview, just a sidecar-file pointer.

In either case, the rest of the file is invisible to you in-call. Most files in this repo are small enough that `cat` returns them in full and you never see either signal. **If you do see either form, never proceed using the partial output as if it were the whole file** — switch to one of the patterns below.

- **Truncated markdown** (you saw either truncation signal above) — read in line-range chunks instead. First check the total line count: `wc -l "$REPO/<path>"`. Then read each chunk:

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

The Python helper scripts in `scripts/` (e.g. `duplicate_check.py`) read files from `$MT_REPO`. Set the env var when invoking them: `MT_REPO=/tmp/cruciate-hub-marketing-team python3 scripts/duplicate_check.py "<topic>"`.

## Standing instructions

This file is loaded once per session and cached in context. Everything below is a standing rule for the whole task, not a one-time checklist. Treat each numbered step as a gate — if you can't satisfy it, stop and surface the problem rather than proceeding.

## Three load-bearing AEO principles

Every structural and stylistic decision ties back to one of these. If a decision doesn't obviously serve one of them, reconsider.

1. **Answer-first extractability.** First sentence answers the title's question using the exact target-keyword phrase. First two sentences fit in 40-60 words. TL;DR paragraph of 120-160 words sits immediately below. This is the block LLMs extract verbatim. 120-160 is the 94th-percentile sweet spot for Google AI Overview passage selection (2025 ranking-factor study); shorter chunks get passed over for longer, more self-contained ones.
2. **Semantic chunking.** Every major section is a self-contained ~150-word passage. Entities are defined inline on first mention within a chunk, not only in the intro.
3. **Concrete grounding.** Named examples, numeric ranges, and internal consistency with product terminology. Citations where they genuinely support a claim — not as SEO padding.

## Single article vs. batch

Two modes, chosen from the brief:

- **Single article** — user asks for one article ("write an AEO article on activity feeds"). Run the linear flow in "Before writing", then "Writing" and "Delivery".
- **Batch** — user asks for multiple articles, a theme, or ideas ("5 articles on community infrastructure", "some ideas for /answers/"). Run the four-phase workflow in "Batch workflow" at the end. Full specs in `references/workflow-phases.md`.

When unclear, ask: "Single article now, or a batch of ideas to work through in phases?" Default to batch if the brief mentions a count ≥2 or "ideas".

## Before writing

### 1. Intake — minimal, only when the brief is genuinely ambiguous

**Default: do not ask intake questions.** If the brief names a topic ("write an AEO article on in-app activity feeds", "answer page on zero-party data"), proceed to the duplicate check. Infer everything else:

- **Intent** — infer from title phrasing. "What is X?" → definition. "How to X?" / "How do you X?" → procedural. "X vs Y" / "alternatives to X" → comparative. If ambiguous, default to definition.
- **Audience** — social.plus's default is product and engineering teams at consumer apps. Use that unless told otherwise.
- **Must-cover sub-topics** — pick what the intent pattern naturally calls for (see `references/patterns/*.md`).
- **Word count** — use the intent-specific range (definition 900-1400, procedural 1100-1800, comparative 1000-1600).

**Only use `AskUserQuestion`** when something is genuinely unresolvable:

- The topic name has multiple plausible meanings (`feeds` — activity feeds? news feeds? RSS?) → ask *one* question: which one?
- The title phrasing doesn't clearly map to an intent and the wrong intent would produce a structurally different article → ask *one*: definition, how-to, or comparison?
- Batch mode only: user said "give me ideas" without a topic → ask *one*: what topic area and roughly how many.

Never ask about word count, audience, or must-cover sub-topics. Never ask "just to confirm." Never chain multiple `AskUserQuestion` calls — that's the bad UX this rule exists to prevent.

If the article misses the mark, the colleague will tell you via chat edits. Cheaper than front-loading a 4-question survey.

### 2. Duplicate-topic check
Run the canonical fetch block first (so `$MT_REPO` is populated), then `MT_REPO=/tmp/cruciate-hub-marketing-team python3 scripts/duplicate_check.py "<topic phrase>"`. The script reads `website/pages-answers.json` and `website/pages-glossary.json` from the cloned repo and lists matches above a 0.5 query-coverage threshold, sorted by score.

The script signals outcome two ways — use whichever your environment makes more reliable:
- **Exit code**: `0` = clean, `1` = matches found, `2` = unverified (read failure)
- **Final stdout line**: `RESULT: CLEAN`, `RESULT: MATCHES`, or `RESULT: UNVERIFIED`

Both signals must agree. If they disagree (e.g. exit `0` but stdout says `RESULT: MATCHES`), treat as `UNVERIFIED` and surface to the user — the result can't be trusted.

- If the script flags a close match in `/answers/`, surface the URL and ask whether to update that page instead. Duplicate pages split authority across the same citation slot.
- If the script flags a match in `/glossary/`, consider whether the topic belongs in the glossary instead.

### 3. Brand-messaging read (non-negotiable)
Read these files from the cloned repo:
- `messaging/terminology.md`
- `messaging/tone.md`
- `messaging/narrative.md`
- `messaging/value-story.md`
- `messaging/positioning.md`
- `messaging/boilerplates.md`

Use the canonical fetch block's validation rules. If any file is missing or fails validation, stop and tell the user. Do not proceed on memorized brand content.

The pitch section at the end of every article is **generated from these brand-messaging files**, not from a template inside this skill. `positioning.md` and `value-story.md` define what social.plus says about itself; `boilerplates.md` provides the approved long-form descriptions.

### 4. Question research
Before writing the FAQ section, surface real follow-up questions. Use Ahrefs MCP tools when available, fall back to WebSearch:

- **Preferred (Ahrefs MCP tools available):**
  - `serp-overview` for the core question — returns the literal PAA block and "Related searches". Most accurate source.
  - `keywords-explorer-search-suggestions` for question-form variants of the target keyword.
  - `keywords-explorer-overview` for the target keyword — confirms volume and intent alignment.
- **Fallback (no Ahrefs):**
  - `WebSearch` on the core question; capture "People Also Ask" phrasings from results.
- Write the FAQ using real phrasings, not invented ones. In `outputs/questions.md`, the **Source** column records each candidate's origin (Ahrefs PAA, Ahrefs suggestions, WebSearch, LLM fallback).
- Do not embed source URLs in the document (no HTML comments — output is a Word document). List source URLs in the final message to the user.

## Article structure — choose by intent

Match structure to query intent. Don't force every article into one template. Each pattern is a starting point; adapt as the topic demands.

| Intent signal | Pattern file |
|---|---|
| "What is X?" / topic is a concept | `references/patterns/definition.md` |
| "How to X?" / "How do you X?" / "Steps to..." | `references/patterns/procedural.md` |
| "X vs Y" / "X or Y" / "alternatives to X" | `references/patterns/comparative.md` |

Every pattern shares these required elements: answer-first block (sentences 1-2 = 40-60 words, TL;DR = 120-160 words), at least one markdown table, 4-6 FAQ pairs from real phrasings, pitch section (brand-driven), conclusion. No fixed section count beyond those — if a sub-topic doesn't belong, don't add it.

## Writing rules (essentials)

Full rules: `references/writing-style.md`. Non-negotiables:

- **Sentence 1** = a direct definition containing the exact target-keyword phrase. 20-30 words.
- **Sentence 2** = the mechanism, scope, or outcome. 20-30 words. Combined with sentence 1: 40-60 words total.
- **TL;DR paragraph** immediately below = 120-160 words, structured as expanded definition → mechanism → outcome → proof point. This is the block AI engines extract verbatim; 120-160 is the research-backed sweet spot for AI-Overview passage selection.
- **~150-word chunks.** Each H2 section is self-contained. A reader landing mid-page still understands it.
- **First mention of a technical entity gets an inline one-clause gloss** using canonical phrasing from `terminology.md`.
- **Citation density depends on intent** (see below) — don't force citations into product how-tos where they'd be faked.
- **Concrete over vague.** Named examples and numeric ranges beat adjectives.
- **Banned constructs:** em dashes, emojis, "revolutionize / unlock / game-changing / leverage", "in today's / now more than ever / in the ever-evolving" openers, passive voice where active works, growth guarantees, wrong `social.plus` casing.

## Citation density by intent

Forcing external citations into product how-tos produces faked or irrelevant links. Apply per-intent rules:

| Intent | External citations | Internal grounding |
|---|---|---|
| Definition | ≥2 required — cite authoritative sources for the definition and scale | Named social.plus entities and inline glosses |
| Comparative | ≥3 required — you're comparing things, cite the things | Dimension-specific data points, honest positioning |
| Procedural | None required | Internal product consistency, named methods, numeric ranges, concrete timelines |

All intents: every numeric claim needs a source (internal approved list or external link). No anonymous or content-farm citations.

Full guidance: `references/citation-playbook.md`.

## Approved data and customer names

Use only these. Never fabricate.

**Metric ranges (from published social.plus data):**
- Engagement rate: 20-50%
- Retention lift: 10-35%
- Active contributors: 10-30%

**Approved customers:** Noom, Harley-Davidson, Smart Fit, Ulta Beauty, Betgames.

**Approved customer stats:**
- Noom: 45M+ users
- Harley-Davidson: 1M+ community members
- Smart Fit: 60% MoM growth
- Betgames: 200M users

## Output format

The final deliverable is a **Word document** saved as `outputs/[slug].docx`. A separate automation (outside this skill) converts it to Webflow-ready HTML.

Because the output is Word, **no HTML of any kind appears in the document** — no JSON-LD, no `<script>`, no `<!-- comments -->`, no inline HTML. Schema, canonical tags, and page meta are handled downstream by the Webflow automation.

### Two-stage production

1. **Draft a markdown intermediate** at `outputs/[slug].draft.md`. This is what the compliance script reads.
2. **Convert to `.docx`** by invoking `anthropic-skills:docx` with the intermediate as input. It preserves headings, tables, lists, bold, hyperlinks. Deliver `outputs/[slug].docx` as the primary artifact.

Keep the `.draft.md` alongside the `.docx` so maintainers can diff edits.

### Markdown intermediate structure

```
# [Article title]

Meta description: [≤160 chars including spaces]
Slug: [lowercase-with-hyphens; preserve compound modifiers like "in-app" or "multi-user"; drop leading articles ("a", "the"); keep the keyword phrase intact]
Alt text: Abstract visualization of [main topic from title]
Intent: [definition | procedural | comparative]

[Answer-first block — sentences 1-2, 40-60 words combined]

[TL;DR paragraph — 120-160 words]

## [First body section]

...
```

Rules for the intermediate:
- `# Title` is the only H1.
- The four labeled-paragraph metadata lines sit between the H1 and the answer-first block. They become body paragraphs in the Word doc; the Webflow automation parses and strips them.
- **Exactly two paragraphs sit between the metadata block and the first H2**, in this order:
  1. The answer-first block (sentences 1-2, 40-60 words combined). **No heading, no prefix.**
  2. The TL;DR paragraph (120-160 words). **No heading, no "TL;DR:" prefix, never wrap in a `## TL;DR` section.**
  Additional paragraphs here will be mis-identified by compliance and fail the TL;DR check. Compliance detects the TL;DR by position (second paragraph), not by label.
- Markdown tables, numbered/bulleted lists, `**bold**`, and inline markdown links `[anchor](URL)` are supported by the docx conversion.
- External citations as markdown links where intent calls for them. Internal links (to social.plus URLs) are handled by `internal-linking-strategist`.

Alt text pattern: `Abstract visualization of [main topic from title]`.

## Internal linking

After drafting and before running compliance, invoke `internal-linking-strategist` in **draft mode**:
- Pass: full article markdown, article title (= target keyword), content type `AEO`.
- The optimizer returns two classes of markdown links for AEO drafts:
  - **Topical links**, scaled by length (~1 per 300 words; floor 2, ceiling 6 — a 900-word definition typically gets 2-3, a 1.5k+ word pillar gets 4-6). Zero only when no relevant target exists — never force them.
  - **Customer-story links**, a separate class not counted toward the topical budget. When an approved customer is named (Noom, Harley-Davidson, Smart Fit, Ulta Beauty, Betgames), the **first mention** becomes a `[customer name](https://social.plus/customer-story/[customer])` link; subsequent mentions stay plain text. Multiple customers each get their own first-mention link.
- Allowed sections (both classes): definition chunk, "why it matters", architecture/features, step-by-step, the social.plus pitch.
- Disallowed (both classes): FAQs, conclusion, metrics table — stay link-free for clean citation extraction. If a customer's first mention falls in a disallowed section, wait for the next allowed-section mention.
- AEO articles use markdown links only, never HTML.
- Never force links. Zero topical and zero customer-story is acceptable when no relevant target exists and no approved customer is named.

## Compliance is non-negotiable

**Before delivering any draft, run `python3 scripts/compliance.py outputs/[slug].draft.md` and paste the full stdout into your response.**

- Manual / eyeball review is **not** a substitute. Field testing shows eyeball review consistently misses meta-description length, em dashes (Unicode `—` mixed with hyphens), filler openers, TL;DR position edge cases, customer-whitelist violations.
- If you are a subagent in a parallel orchestration, the full script stdout is a required field in your return payload. Not a summary, not a paraphrase — the literal output. The parent re-runs the script and treats any disagreement as a failure.
- If any check fails, fix and re-run. Do not ship-and-flag. Do not claim the script "is not available" — if you can read the markdown with Read, you can run the script with `python3`.

The script reads the markdown intermediate. Exit 0 = ready to convert; exit 1 = fix first.

Checks:
- Required labeled-paragraph metadata present (title from H1; Meta description, Slug, Alt text, Intent from labeled paragraphs under H1)
- Intent is one of: definition, procedural, comparative
- Meta description ≤ 160 characters including spaces
- Title-keyword phrase appears in sentence 1 of the answer-first block
- Sentence 1 does not start with a filler opener ("In today's…", "Now more than ever…", "In the ever-evolving…", "In a world where…")
- First two sentences in 40-60 word range
- TL;DR paragraph in 120-160 word range
- No em dashes, no emojis, no forbidden terms
- No HTML of any kind — no tags, no comments, no JSON-LD. The output is a Word document.
- Heading hierarchy well-formed (single H1, no skipped levels)
- External citations count meets intent target (definition ≥2, comparative ≥3, procedural any)
- Approved-customer whitelist — no mentions of unapproved customer names
- Internal-link presence — at least one `https://social.plus/...` link in the body (WARN only — a zero usually means `internal-linking-strategist` was skipped). Binary presence check, **not a topical-link-floor check**: the optimizer enforces its own per-length floor (2 for short, up to 6 for long). Compliance just catches "optimizer never ran." Legitimate zero only when no related page exists AND no approved customer was named.
- Word count inside the intent-specific typical range (warning only)

Fix every failure before delivering. Warnings are informational — address if it strengthens the article, skip if not.

## Self-check before delivery

After the compliance script passes, answer each of these yes/no before returning the article:

1. Does sentence 1 literally answer the question the title asks, using the target-keyword phrase?
2. Does the TL;DR paragraph stand alone as an extractable 120-160 word passage?
3. Does every numeric claim have a source (approved-data list or external citation)?
4. Does the pitch section reflect the fetched `positioning.md` / `value-story.md` / `boilerplates.md`, not a template from memory?
5. Are the FAQ questions phrased from real-user research (not invented patterns)?
6. Did I check the deferred-tool list for Ahrefs MCP tools before defaulting to WebSearch?
7. Did the compliance script exit 0?

Any "no" → revise before delivering. Do not ship with unresolved "no".

## Delivery

1. After compliance passes, convert `outputs/[slug].draft.md` to `outputs/[slug].docx`. Two options:
   - **Preferred:** invoke `anthropic-skills:docx` with the intermediate as input.
   - **Fast fallback (if docx skill unavailable):** `pandoc outputs/[slug].draft.md -o outputs/[slug].docx` — sufficient for this markdown profile (H1/H2, tables, lists, bold, inline links).
2. Tell the user the `.docx` is ready in the artifact panel; `.draft.md` is kept alongside for diff-able revisions.
3. In the same message, list the FAQ source URLs (not embedded in the document).
4. For edits, modify `.draft.md`, re-run compliance, re-convert to `.docx` and overwrite. Keep them in sync.

## Rationalization table — common shortcuts that fail

| Excuse | Reality |
|---|---|
| "The intro reads better with context first." | LLMs extract the first two sentences. If the answer isn't there, it isn't cited. |
| "Procedural articles need external citations too." | No — they need internal product consistency. Fake citations are worse than none. |
| "I can skip the duplicate check — this topic feels unique." | Check anyway. Rewriting into an existing page beats creating a near-duplicate. |
| "The brand fetch failed but I remember the tone." | Stop. Memorized brand content drifts. Tell the user. |
| "I'll eyeball compliance — the article looks clean." | Run the script. Meta length, keyword-in-sentence-1, and filler openers consistently slip past eyeball review. |
| "I can pad to hit the word count target." | Padding dilutes chunk quality. Under target → brief is thinner than expected; raise with the user. Over → cut padding, not substance. |
| "The pitch template is easier than adapting from brand files." | The pitch is brand-driven. Generic pitches get skipped by LLMs. |
| "I can invent a plausible customer example." | Never. Use the approved list or omit. |
| "I should confirm what the user wants before drafting." | Only if genuinely unresolvable. A clear brief is a green light. Asking 3-4 intake questions on a clear brief is the most annoying failure mode this skill has. |
| "Long anchor text gives the link more context." | Wrong. The claim belongs in the prose. Anchors name the source in 3-6 words. Anchors over 8 words fail compliance — they degrade LLM extraction signal and look like spam to search engines. |

## Batch workflow

When the brief covers multiple articles, run these four phases instead of the single-article flow. Each phase produces a markdown artifact in `outputs/` that the colleague reviews. She approves or refines via chat using the approval syntax below. The skill moves to the next phase when she says `next`. Full specs in `references/workflow-phases.md`.

### Phase A — Ideas
- If the brief names a topic area and count ("5 articles on community infrastructure"), **skip intake** and proceed to brand fetch + gap scan. Only ask one `AskUserQuestion` when the user said "give me ideas" with no topic area — and even then, ask about topic area and count, nothing else.
- Fetch brand once, then scan `pages-answers.json` (and `pages-glossary.json`) for gaps.
- **Fit scoring:** if Ahrefs MCP tools are available, use `keywords-explorer-overview` for real volume + difficulty per candidate, and `site-explorer-organic-keywords` on existing /answers/ URLs to catch semantic duplicates the JSON scan missed. Without Ahrefs, fall back to qualitative fit (high/medium/low).
- Write `outputs/ideas.md` with **8-15 candidate articles** (columns: #, title, intent, rationale, target keyword, fit). Always more than requested — extras exist so she has real choice. If she asked for 3, show 8-12 and note `approved: 0 of 3 target (from 10 candidates)`. If she asked for 10, show 12-15. Never show fewer than the target.
- She approves a subset. The skill rewrites `outputs/ideas.md` to show only the approved set.

### Phase B — Questions
- For each approved idea, run the question research (PAA via Ahrefs or WebSearch fallback).
- Write `outputs/questions.md` — one section per approved idea, 8-10 candidate FAQ questions each.
- She approves per-article. The skill updates the file.

### Phase C — Drafts
- For each approved idea with approved questions, draft `outputs/[slug].draft.md` following the single-article structure.
- Write `outputs/overview.md` — one row per article with title, word count, compliance status.
- She can chat edits on any draft ("article 2 shorter", "add pitfalls to article 3"). The skill edits, re-runs `scripts/compliance.py`, updates `overview.md`.

### Phase D — Delivery
- When all drafts pass compliance, convert each `[slug].draft.md` to `outputs/[slug].docx` via `anthropic-skills:docx`.
- Run `python3 scripts/make_zip.py` to bundle all `.docx` files into `outputs/aeo-batch-YYYY-MM-DD.zip`.
- Send a final chat summary listing each `.docx` filename, the zip filename, and FAQ source URLs per article. Files appear in the artifact panel.

### Approval syntax

Consistent across phases. Parse these lines at the start of each chat turn; fall back to natural language if the message doesn't match.

```
approve: 1, 3, 5-7
drop: 2, 6
revise: 4 — make it about retention
next
```

For Phase B, scope to an article:
```
article 1: approve 1-4, drop 5
article 2: approve 1, 3, 5; revise 2 — drop the pricing angle
next
```

### When to abort a batch

- Brand fetch fails → stop at Phase A, tell her, do not proceed on memorized brand.
- No gaps found in `pages-answers.json` → surface this at Phase A, ask whether to update existing articles instead.
- Compliance failures in Phase C that can't be auto-fixed after one rewrite → surface to her before moving to Phase D.
- `anthropic-skills:docx` unavailable → fall back to `pandoc outputs/[slug].draft.md -o outputs/[slug].docx` (see Delivery section). If pandoc is also unavailable, deliver the `.draft.md` files and tell the user.

### Parallel-subagent orchestration (alternative to the phased flow)

The four-phase workflow is a gated review loop — fits "help me decide which ideas are worth pursuing, then iterate each draft." Some briefs are different: **"draft all N articles in parallel, no per-phase review"**. Parallel subagents are the right tool.

Field testing shows subagents consistently rationalize around the skill's rules when orchestrated in parallel. The mitigations below are mandatory in this mode.

**Required parent-session setup (once before spawning subagents):**

1. Run the canonical fetch block (clones the repo to `$MT_REPO`). Brand files are at `$MT_REPO/messaging/*.md`. Pass `$MT_REPO` to each subagent so they read from the same clone.
2. Run `MT_REPO=/tmp/cruciate-hub-marketing-team python3 scripts/duplicate_check.py "<topic>"` for each topic. **Check the exit code.** `0` = clean; `1` = likely duplicates, get user confirmation before drafting; `2` = "RESULT: UNVERIFIED" — do not proceed without manually checking via GitHub UI. Do not silently assume "clean" on UNVERIFIED.
3. Decide the intent for each topic up front from title phrasing; pass the matching `references/patterns/<intent>.md` path in the subagent brief.

**Required subagent contract (each return payload must include):**

1. The path to `outputs/[slug].draft.md`.
2. The **full, verbatim stdout** of `python3 scripts/compliance.py outputs/[slug].draft.md`. Not a summary, not a paraphrase — the literal output. See "Compliance-output fingerprint rule" and "Sample expected compliance output" below.
3. Evidence that `internal-linking-strategist` was invoked. Paste both classes:
   - **Topical links** (count + each anchor + URL + insertion-point quote — section heading + first 8 words). Example: `Returned 3 topical links: [activity feed SDK](https://social.plus/chat/sdk) — inserted in "## How activity feeds work", paragraph starting "A modern feed platform adds a ranking layer…".` If zero, state the reason.
   - **Customer-story links** (count + each customer-name anchor + URL + first-mention location). Example: `Returned 1 customer-story link: [Noom](https://social.plus/customer-story/noom) — first mention inside "## Where social.plus fits".` If no approved customer named, write `none — no approved customer mentioned`.

   Memory-guessed URLs without insertion-point proof are an auto-failure. The parent's `check_internal_links` backstop catches absence; per-class evidence catches fabrication.
4. A list of FAQ source URLs used.

**Compliance-output fingerprint rule.** Before trusting any subagent's claim, the parent checks the payload for two literal strings:

1. `AEO compliance report for`
2. At least one line matching `[PASS]`, `[FAIL]`, or `[WARN]`

If either is missing, treat as "script not run" regardless of what the subagent says. The parent re-runs the script as a backstop — and marks the draft as higher-risk, because a subagent that fabricates output once will fabricate again.

**Sample expected compliance output.** The script's stdout looks exactly like this:

```
AEO compliance report for outputs/[slug].draft.md

  [PASS] metadata_title
  [PASS] metadata_metaDescription
  [PASS] metadata_slug
  [PASS] metadata_altText
  [PASS] metadata_intent
  [PASS] metadata_intent_valid — intent=definition
  [PASS] meta_description_length — 135 chars (max 160)
  [PASS] word_count — 1247 words (target 900-1400)
  [PASS] answer_first_block — first two sentences = 48 words (target 40-60)
  [PASS] tldr_word_count — TL;DR = 138 words (target 120-160)
  [PASS] keyword_in_first_sentence — full phrase '...' found in sentence 1
  [PASS] no_filler_opener
  [PASS] no_em_dashes — 0
  [PASS] no_emojis — 0
  [PASS] no_forbidden_terms — 0
  [PASS] no_html — 0
  [PASS] no_jsonld_block
  [PASS] single_h1 — found 1 H1 heading(s)
  [PASS] no_skipped_heading_levels — well-formed
  [PASS] external_citations — 2 external citation(s); intent=definition (minimum 2)
  [PASS] internal_links — 1 internal social.plus link(s)
  [PASS] approved_customers_only — 0

All checks passed.
```

Paste it verbatim. Do not reformat, summarize, or invent checkmarks/percentage bars/headings. The fingerprint rule looks for the literal `AEO compliance report for` and `[PASS]` / `[FAIL]` / `[WARN]` lines — anything else, the parent treats the claim as unverified.

**Required parent-session verification (after subagents return, before converting to `.docx`):**

1. Re-run `python3 scripts/compliance.py` on every `.draft.md`. If the re-run disagrees with the subagent's claim, fix in the parent and re-verify. Don't trust the subagent's claim alone.
2. Confirm each draft includes at least one `https://social.plus/...` link (the `internal_links` check WARNs if zero). If zero, invoke `internal-linking-strategist` from the parent and re-insert.
3. Convert each `.draft.md` to `.docx` via `anthropic-skills:docx` or `pandoc`.
4. Zip via `scripts/make_zip.py`.
5. Report per-article status in the chat summary.

**Known subagent failure modes to guard against:**

- "Manual compliance check ✓" without running the script. → Re-run in the parent; treat as failure.
- **Fabricated compliance output** in a format that isn't the script's (e.g., `1. METADATA REQUIREMENTS ✓ Title present: True` with unicode checkmarks). → Fingerprint rule catches; treat as "script not run" and re-run in parent.
- **Prose-summary compliance claim** with no pasted output ("Compliance status: All checks PASSED (exit code 0)"). → Same; fingerprint catches.
- `## TL;DR` heading or extra paragraph between metadata and first H2. → Compliance catches; do not override.
- Em dashes introduced despite the writing-style ban. → Compliance catches; do not override.
- Dropped `internal-linking-strategist` call "to simplify orchestration." → Parent runs it as a backstop when `internal_links` WARNs.
- **Claimed internal links not actually in the draft** (or URLs fabricated from memory). → Parent's re-run catches zero real links; if WARN fires while the subagent claimed N, the optimizer claim was fabricated — invoke from the parent and re-insert.

## Related skills

- `blog-seo-content` — blog posts for social.plus/blog
- `case-study` — customer stories
- `brand-messaging` — general website copy
- `internal-linking-strategist` — called by this skill; do not re-implement
- `site-intelligence` — content audits beyond `pages-answers.json`
