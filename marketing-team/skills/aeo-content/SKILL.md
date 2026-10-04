---
name: aeo-content
description: >
  Writes /answers/ pages for social.plus: one page per specific buyer or
  developer question (how to, should I, cost, why, vertical playbooks),
  built to be cited by ChatGPT, Claude, Perplexity, Gemini and Google AI
  Overviews and to be genuinely useful to the reader. Writes only from an
  Approved row in the Content Queue (Google Sheet). Delivers a markdown
  intermediate plus .docx for review.

  Do NOT use for: "What is [term]?" definitions or glossary entries (use
  glossary-content); blog posts, opinion, original research or "best X"
  listicles (use blog-seo-content); customer stories (use case-study);
  website page copy (use brand-messaging); press releases (use
  press-release).
when_to_use: >
  Trigger phrases: "answer page", "AEO article", "GEO article", "content
  for /answers/", "write Queue row A1", "write the approved answers",
  "how-to page for /answers/".
---

# AEO Answer Pages (v2)

Answer pages live at `social.plus/answers/[slug]`. Each one answers **one specific question** from the buyer or developer journey, so well that an AI engine would rather cite it than write its own answer.

**What changed from v1, and why.** v1 wrote whatever keyword it was given, which produced ~80 near-duplicate pages ("SDK for X", "Tool for X", "Platform for X") that repeated the same customer stat and the same "Leading [X] for [Y]: social.plus" section. That pattern matches Google's scaled-content and doorway policies and adds nothing an AI engine would cite. v2 writes only from an approved Content Queue row, checks duplication on meaning rather than titles, requires evidence that isn't reused everywhere, and keeps promotion out of the parts AI engines extract. Definitions moved to `glossary-content`.

## How to fetch reference files

<!-- FETCH-BLOCK:START v2 -->
Reference files live in the public `cruciate-hub/marketing-team` GitHub repo. Fetch them by shallow-cloning the repo once per session, then loading individual files with `cat`. Use this exact pattern at the start of every skill that needs reference files:

    REPO="${MT_REPO:-/tmp/cruciate-hub-marketing-team}"
    REMOTE="https://github.com/cruciate-hub/marketing-team.git"
    # Create the clone only when the path is absent. Never delete an existing
    # directory: it may be a working checkout holding un-pushed local commits.
    if [ ! -e "$REPO" ]; then
      git clone --depth 1 --quiet "$REMOTE" "$REPO" || true
    elif git -C "$REPO" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      # Refresh, but do NOT ignore a failed pull. Silently serving stale
      # content is the exact bug this block exists to prevent.
      git -C "$REPO" pull --ff-only --quiet 2>/dev/null \
        || echo "Note: could not refresh $REPO; verifying existing content below." >&2
    fi
    # Mechanical integrity gate. Do not skip. Probes core files across several
    # top-level dirs so a missing, corrupt, or partial clone stops the skill
    # here instead of letting it read incomplete content and draw wrong conclusions.
    miss=""
    for f in brain.md messaging/brain.md messaging/terminology.md messaging/tone.md design-system/brain.md; do
      [ -s "$REPO/$f" ] || miss="$miss $f"
    done
    if ! git -C "$REPO" rev-parse HEAD >/dev/null 2>&1 || [ -n "$miss" ]; then
      echo "Fetch failed: clone at $REPO is unreachable or incomplete.${miss:+ Absent files:$miss}" >&2
      echo "Check your network. If the clone is corrupt and holds no local work, run  rm -rf \"$REPO\"  then re-run." >&2
      echo "(If \$MT_REPO points at your own checkout, rescue its changes first; this never auto-deletes it.)" >&2
      exit 1
    fi

    # Overlay the live website inventories. The auto-generated pages-*.json
    # are committed to the `site-data` branch (bot commits stay off main);
    # main only carries a point-in-time snapshot. Restricting the overlay to
    # pages-*.json keeps the clone fast-forwardable on the next session's pull.
    if git -C "$REPO" fetch --depth 1 --quiet origin site-data 2>/dev/null; then
      git -C "$REPO" checkout --quiet FETCH_HEAD -- 'website/pages-*.json' 2>/dev/null \
        || echo "Note: site-data overlay failed; website/pages-*.json are the main-branch snapshot (may be stale)." >&2
    else
      echo "Note: could not fetch site-data; website/pages-*.json are the main-branch snapshot (may be stale)." >&2
    fi

After the clone exists, read files with `cat "$REPO/<path>"`. Examples: `cat "$REPO/brain.md"`, `cat "$REPO/messaging/terminology.md"`.

The integrity gate above fails loud rather than serving partial content, and it never deletes `$REPO` (it can hold un-pushed local work). To make skills read your own local edits, point `MT_REPO` at your working checkout before running them.

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

  Some skills ship helper scripts that already follow this pattern (e.g. `marketing-team/skills/aeo-content/scripts/duplicate_check.py`).

  **Degraded-inventory guard.** The pages-*.json files are auto-generated; a generation failure can leave a file syntactically valid but empty or missing pages. After loading any of them, check `_meta.errors` and `len(pages)`:

      python3 -c "
      import json; d=json.load(open('$REPO/website/pages-industry.json'))
      errs = d.get('_meta',{}).get('errors') or []
      print(len(d.get('pages',[])), 'pages;', len(errs), 'extraction errors', errs)"

  If `pages` is empty, or `_meta.errors` is non-empty, the inventory is degraded: name the affected file and the missing paths in your output, scope any 'site-wide' claims accordingly, and never treat an empty inventory as 'this section has no pages'.

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

The Python helpers read from `$MT_REPO`: `scripts/compliance.py` (this skill) and `$MT_REPO/scripts/intent_match.py` (shared with the planning step and other content skills).

## Four principles

Every rule below serves one of these. If a decision doesn't obviously serve one, reconsider it.

1. **One question per page.** The page answers the Queue row's canonical question and nothing that another row owns. Focused pages are cited more often than pages that try to cover a whole topic.
2. **Answer first.** The direct answer and a standalone summary come before anything else. AI citations cluster early on the page.
3. **Something only we can say.** Every page carries facts an AI model couldn't produce itself: approved data, product specifics, sourced numbers, named examples. If a claim cannot be false, it adds nothing.
4. **Honest.** Neutral, defensible answers in the extracted parts; social.plus is compared on the same criteria as everyone else; selling happens only in the pitch section.

## Input: an Approved Queue row

The skill writes from a row in the Content Queue (Google Sheet, Queue tab). It reads: ID, Canonical question, Draft first sentence, Headings (sub-questions), Unique information source, Premise check, Dependencies, Intent.

- **No row, no page.** If someone asks in chat for an answer page that has no row, draft the row first (question, draft first sentence, sub-questions, unique information source, suggested intent), run the duplication check, and show it. A direct request from the person counts as approval once they confirm the row. Remind them to add it to the Queue so the engine's record stays complete.
- **Status must be `Approved`.** Rows at `Idea`, `Blocked: needs data`, `Rejected` or `Merged` are not written. Say which, and stop.
- **Dependencies must be met.** Every ID in Dependencies should be `Published`, or approved in the same batch and written first. Usually these are glossary entries the page links to.
- **Collection must be `Answer`.** A `Glossary` row goes to `glossary-content`; a `Blog` row goes to `blog-seo-content`.

## Steps (single page)

### 1. Duplication check (on meaning)

```
MT_REPO=/tmp/cruciate-hub-marketing-team python3 "$MT_REPO/scripts/intent_match.py" \
  "<canonical question>" --first-sentence "<draft first sentence>" \
  --queue queue.csv --exclude-id <ID>
```

Exit `0` / `RESULT: CLEAN`: continue. Exit `1` / `RESULT: MATCHES`: read every `LIKELY DUPLICATE` and `REVIEW` line and apply the test **"would the two pages open with the same first sentence?"** If yes, stop and recommend Update existing, Merge or Reject for this row. If no, note in one line why they differ and continue. Exit `2` / `RESULT: UNVERIFIED`: do not treat as clean; fix the input or check by hand.

Without `--queue`, only published pages are checked. Say so in your output.

The script is a lexical approximation. It over-flags shared keywords (for example "app retention" in both a benchmark question and a glossary entry); the first-sentence test is the actual decision.

### 2. Brand read (non-negotiable)

Read from the clone: `messaging/terminology.md`, `tone.md`, `narrative.md`, `value-story.md`, `positioning.md`, `boilerplates.md`. If any file fails validation, stop. Do not write from memory.

### 3. Evidence selection

Read `messaging/evidence-bank.md`. Pick the facts this page will use and confirm:

- Every fact is `Approved`. If the page's core claim needs a `Pending` fact, stop and set the row back to `Blocked: needs data`.
- No fact is over its usage cap.
- At least one fact is not used by any other page in the same Queue cluster.
- The page will contain at least 3 statistics in total (evidence bank or external citations).

For how-to pages, check product specifics against current social.plus documentation (learn.social.plus) on the day of writing. Propose new Product facts rows for anything you rely on.

Check the row's Premise check. If the question assumes something ("Why do fitness apps have low retention?"), the premise needs a source before the page is built on it.

### 4. Question research for FAQs

Use Ahrefs MCP when available (`serp-overview` for People Also Ask, `keywords-explorer-matching-terms` with `terms=questions`, `keywords-explorer-search-suggestions`); fall back to web search. Pick 3-5 real questions. Drop any that another Queue row owns; link to that page from the body instead. List FAQ sources in your final message, not in the document.

### 5. Pick the template

Use the row's Intent:

| Intent | Template | For |
|---|---|---|
| how-to | `references/patterns/how-to.md` | Carrying out a task |
| decision | `references/patterns/decision.md` | Build vs buy, cost, timeline, X or Y, what to look for |
| explainer | `references/patterns/explainer.md` | Why, does, what is a good... (not definitions) |
| playbook | `references/patterns/playbook.md` | How a specific vertical uses social features |

All four fill the shared page shape in `references/patterns/_shared.md`. Read both files.

### 6. Draft

Write `outputs/[slug].draft.md`. Body H2s are the row's sub-questions, phrased as questions. Full style rules: `references/writing-style.md`. Citation rules: `references/citation-playbook.md`.

### 7. Internal linking

Invoke `internal-linking-strategist` in draft mode (see "Internal linking" below) before compliance.

### 8. Compliance

Run `python3 scripts/compliance.py outputs/[slug].draft.md --queue queue.csv` and paste the full stdout. Fix and re-run until it exits 0.

### 9. Self-check, deliver, update the Queue

See "Self-check", "Delivery" and "Queue update" below.

## Markdown intermediate

```
# [Canonical question, word for word]

Meta description: [≤160 characters]
Slug: [lowercase-with-hyphens, keep the keyword phrase, no years]
Alt text: [describes the page's main visual, if any]
Intent: [how-to | decision | explainer | playbook]
Queue ID: [e.g. A1]
Last updated: [YYYY-MM-DD]
Editor (named human reviewer): [fill before publish]

[Answer-first block: 1-2 sentences, 25-60 words, no heading]

[Summary: 80-150 words, no heading]

## [Sub-question 1?]
...
## [Sub-question 2?]
...
## [How social.plus helps with <this question>]
...
## FAQs
### [Question?]
...
## Conclusion
...
```

Exactly two paragraphs sit between the metadata block and the first H2. No HTML (the one exception: a `<figure>` block carried over from the live page when an existing answer is rewritten), no JSON-LD, no comments. Page meta comes from the Webflow template; the FAQPage schema is added by the converter at publish, built from the `## FAQs` section.

## Writing rules (essentials)

- **Sentence 1** answers the title directly and contains its keyword phrase. Never mention social.plus in the answer-first block or summary.
- **Self-contained sections.** Each H2 section makes sense on its own. Define technical entities inline on first mention in a section, using `terminology.md` wording.
- **At least one table**, where it answers a sub-question.
- **Concrete over vague.** Ranges and named examples beat adjectives. "4-8 weeks" beats "quickly".
- **Never state prices.** No currency figures for social.plus or any other vendor: no starting prices, per-MAU rates, plan prices or price ranges, in the body, tables, FAQs or meta description. Describe the pricing *model* instead (MAU-based, usage-based, volume discounts, contact sales for a quote) and link to the vendor's pricing page. Prices change without notice and a stale figure is a credibility and legal risk. Cited cost statistics (for example an industry breach-cost study) are fine. Same rule as `blog-seo-content`; `compliance.py` WARNs on price-like figures (`no_price_figures`).
- **Banned:** em dashes, emojis, filler openers, growth guarantees, wrong `social.plus` casing, and the vocabulary tiers below.

## Anti-slop rules (generation time)

Unedited AI-generation patterns are the "little added value" signal Google's scaled-content enforcement keys on, and generic filler is exactly what retrieval systems paraphrase without attribution. The remedy is editing until the page earns citation — never disguising how it was drafted.

### Vocabulary tiers

`scripts/compliance.py` enforces this list, and the two tiers below must stay in agreement with it.

- **FAIL tier (hard block):** "delve", "in today's fast-paced", "digital landscape", "ever-evolving". These join the terms the script already FAILs (revolutionize, game-changing, "unlock the power", leverage-as-verb, best-in-class, growth guarantees).
- **WARN tier (context-dependent):** "unlock", "elevate", "seamless", "robust". Legitimate in narrow technical uses ("robust error handling", "unlock a locked account"); slop as generic filler.

Note: bare "unlock" moves from the old blanket-ban wording to script-enforced WARN — a tightening, since previously only "unlock the power" was actually enforced and bare "unlock" passed silently.

### Structural bans

blog-seo-content's "no intro paragraph that restates the title" ban is deliberately NOT ported here: the answer-first block restates the title as a direct answer by design (principle 2). A future edit must not "fix" that.

- **No additive-transition openers.** No paragraph — and especially no first paragraph of an H2 chunk — begins with "Additionally", "Furthermore", or "Moreover". An additive opener makes the chunk depend on the previous one, breaking the self-contained section contract — extraction engines lift chunks out of context.
- **No empty chunks.** An H2 section whose body only restates its heading or the summary in more words gets cut or merged. Every chunk must add at least one concrete element (named entity, numeric range, worked example, or mechanism) beyond what the summary already said.
- **Conclusion earns its place.** The conclusion remains a required pattern element, but it never opens with "In conclusion" and must give a decision rule or next step rather than a recap. It stays link-free per existing rules.


## Answer honesty

On May 15, 2026, Google updated its spam policies to cover attempts to manipulate generative AI responses in Search, and reporting on the change names biased listicles and "recommendation poisoning". This skill optimizes to be cited, never to manipulate. The line:

- **Extraction blocks are promotion-free.** The answer-first block, summary and every FAQ answer state neutral, defensible facts and never mention social.plus. `compliance.py` enforces this.
- **Same criteria for everyone.** Decision tables and trade-off tables apply the same dimensions to every option, including social.plus. If another option is better for a case, say so. No template instructs the writer to make social.plus "win".
- **No self-ranking on Answer pages.** "Best X" lists belong on the Blog, with social.plus identified as the publisher.
- **Claims about social.plus come only from `messaging/evidence-bank.md`.** No unsourced "leading", "#1" or "best-in-class".

This also serves citability: retrieval systems skip promotional answer blocks.

## Ecosystem hyperlinks

Ecosystem hyperlinks are contextual links to authoritative, non-competing reference sites woven into the body prose. They differ from external citations: citations support a specific factual claim; ecosystem links let a reader go deeper on a concept, standard, protocol, or tool.

**Why they improve AEO:** AI retrieval systems score pages higher when they link to well-established reference nodes. GEO research (Aggarwal et al., arxiv 2311.09735) identifies linking to authoritative adjacent resources as a strong content-level signal for AI visibility — the same signal that makes Wikipedia-citing pages more likely to be extracted than self-contained ones.

### Density

Every article includes **3-5 ecosystem hyperlinks**. Fewer than 3 is a missed AEO opportunity; more than 5 dilutes the signal. Zero is a missed opportunity; the reviewer should ask why.

### Approved targets

Good targets: web standards (developer.mozilla.org, w3.org, IETF RFCs), platform docs (developer.apple.com, developer.android.com), UX research (nngroup.com, baymard.com), academic papers (arxiv.org, dl.acm.org), industry data (pew.org, statista.com), privacy and compliance bodies (iapp.org, owasp.org, gdpr.eu), community research (cmxhub.com, feverbee.com/blog). Full list in `references/citation-playbook.md` (§ Ecosystem hyperlinks).

Never link to direct or partial competitors: in-app messaging/feed platforms (getstream.io, sendbird.com, pubnub.com, pusher.com, ably.com), community platform vendors (circle.so, mighty.social, tribe.so), or social apps competing on engagement (discord.com, slack.com for community use cases). When uncertain, ask: would a reader see this as social.plus endorsing an alternative to their own product?

### Placement rules

- Embed in body sections where the concept is introduced (evidence, mechanism and how-to sections).
- Do not place in: answer-first block, summary, FAQs, conclusion, pitch. Keep these link-clean for AI extraction.
- Anchor text names the concept, standard, or resource. 2-5 words. The claim stays in the prose; the anchor names the source.
  - Good: `relies on the [WebSocket protocol (RFC 6455)](https://www.rfc-editor.org/rfc/rfc6455)`
  - Good: `per [Nielsen Norman Group's notification UX research](https://www.nngroup.com/articles/push-notifications/)`
  - Bad: `[research shows notifications increase 30-day retention by 25%](https://...)` — the claim is in the anchor, not the prose

## Internal linking

After drafting and before compliance, invoke `internal-linking-strategist` in **draft mode**:
- Pass: full draft markdown, the canonical question as target keyword, content type `AEO`.
- It returns **topical links** (about 1 per 300 words, floor 2, ceiling 6; zero only when no relevant target exists) and **customer-story links** (the first mention of an approved customer links to their story; later mentions stay plain).
- Allowed sections: body sections and the pitch. Not allowed: answer-first block, summary, FAQs, conclusion.
- Also link to the glossary entries and Answer pages listed in the row's Dependencies, and to any Queue page whose question an FAQ would otherwise have duplicated.
- Markdown links only. Never force links, never improvise URLs.

## Compliance is non-negotiable

Run before delivering any draft, and after every edit:

```
python3 scripts/compliance.py outputs/[slug].draft.md --queue queue.csv
```

Paste the full stdout. Eyeball review is not a substitute: it reliably misses meta length, em dashes, summary position and FAQ overlap. Exit 0 = ready; exit 1 = fix first.

What it checks:
- Metadata present (title, meta description, slug, alt text, intent, Queue ID) and an `Editor (named human reviewer)` line; intent is one of the four v2 templates (v1 intents FAIL)
- Meta description ≤ 160 characters
- Answer-first block 25-60 words, keyword phrase in sentence 1, no filler opener
- Summary 80-150 words, exactly two paragraphs before the first H2
- At least 60% of body H2s phrased as questions
- At least one table; at least 3 statistics
- Exactly one H2 naming social.plus (the pitch, 80-150 words); no legacy boilerplate headings ("Leading [X] for [Y]: social.plus", "Why social.plus powers...")
- social.plus not mentioned in the answer-first block, summary or FAQs
- 3-5 FAQs as H3 questions; with `--queue`, no FAQ duplicates another row's question
- A Conclusion section that doesn't open with "In conclusion"
- External citations per template (decision ≥3, explainer ≥2, playbook ≥1, how-to none); anchors ≤ 8 words
- No em dashes, emojis, forbidden terms (WARN tier as warnings), HTML or JSON-LD; single H1, no skipped heading levels
- Approved-customer whitelist (kept in sync with the evidence bank by `tests/run_tests.py`); internal links present (WARN)
- Word count 700-1,500 (WARN)

Run `python3 tests/run_tests.py` after changing the script, the evidence bank's customer table, or `intent_match.py`.

## Self-check before delivery

After compliance passes, answer yes or no:

1. Does the page answer the row's canonical question and nothing another row owns?
2. Would sentence 1 stand alone as a correct answer if an AI engine quoted only that?
3. Is every statistic traceable to the evidence bank or an external source, with no fact over its cap and at least one fact unique within the cluster?
4. Does the page contain something an AI model couldn't write without us?
5. Are comparisons and trade-offs fair to every option, including when social.plus isn't the best fit?
6. Is the pitch specific to this question, built from the fetched brand files?
7. Are FAQs from real research, with no duplication of other rows?
8. Did the premise check hold up?

Any "no": revise before delivering.

### BLOCK conditions

These veto delivery regardless of a clean compliance run:

1. Unresolved compliance FAIL, or the script wasn't re-run after the last edit.
2. Row not `Approved` (or not confirmed by the person in chat), or dependencies unmet.
3. A claim about social.plus not traceable to an `Approved` evidence-bank row.
4. Duplication check skipped, or a likely duplicate waved through without the first-sentence test.
5. Improvised internal links (not returned by `internal-linking-strategist`).
6. Missing `Editor (named human reviewer)` line.

## Delivery

1. Convert `outputs/[slug].draft.md` to `outputs/[slug].docx` (`anthropic-skills:docx`, or `pandoc` as a fallback). The `.docx` is the review copy; keep the `.draft.md` alongside, since it is what gets published.
2. In the same message: compliance output, FAQ sources, evidence-bank facts used, and anything the reviewer should check (premises, Legal-sensitive statements).
3. For edits, change the `.draft.md`, re-run compliance, re-convert.

### Queue update

Output the Queue changes for the row so a human can paste them (or write them directly once the automated Sheets connection is approved by IT):
- Status: `In review`
- Draft link: where the `.docx` or draft lives
- Draft first sentence: the final sentence 1 (keeps future duplication checks accurate)
- Evidence bank: the rows whose `Used on` should get this ID after approval

## Publishing to Webflow

Publishing runs through `webflow-publisher`, after compliance passes and a named editor signs off. The Answers field map (`webflow-fields.json`) was confirmed against the live collection on 2026-10-01: the whole article below the H1 goes into `content`, the meta title is copied from the title unless the draft sets `Meta title:`, and the optional `image-2` stays empty until a person approves an image. The converter adds FAQPage schema from the `## FAQs` section (the answers template has none of its own) and puts every table in the table standard.

## Rationalization table

| Excuse | Reality |
|---|---|
| "This topic is obviously new, I'll skip the duplication check." | The legacy collection is 80 pages of "obviously new" topics. Run it. |
| "The row is at Idea but the person clearly wants it." | Ask them to approve the row. The Queue is the record. |
| "A small permutation (SDK vs API) deserves its own page." | Only if the first sentence would differ. It almost never does. |
| "Smart Fit's 60% fits here too." | Check the cap and the cluster rule. Repeated facts add no evidence. |
| "Mentioning social.plus in the summary helps us get cited." | Backwards. Promotional answer blocks get skipped, and Google's spam policies now cover manipulating AI answers. |
| "The trade-off table should show social.plus as the best fit." | Same criteria for every option. Say so when another approach wins. |
| "This FAQ is useful even if another row covers it." | Link to that page instead. Otherwise the two pages compete. |
| "I'll eyeball compliance." | Run the script and paste the output. |
| "The brand fetch failed but I remember the tone." | Stop and say so. |
| "I can pad to reach 700 words." | Under length means the question is narrow. That's fine; the word count is a warning, not a target. |
| "A definition page is basically an answer page." | Definitions belong to glossary-content. Link to the glossary entry. |

## Batch workflow

For several Approved rows at once ("write A1, A3, D1"), follow `references/workflow-phases.md`: pre-flight checks for every row, drafts, then review handoff with Queue updates. v2 batch mode never generates ideas; that is the planning step's job.

## Parallel-subagent orchestration

Drafting rows in parallel is fine, but subagents rationalize around rules. These safeguards are mandatory.

**Parent session, before spawning:** run the fetch block; run pre-flight from `references/workflow-phases.md`; pass each subagent its Queue row, template path, chosen evidence-bank facts and `$MT_REPO`.

**Each subagent returns:**
1. The path to `outputs/[slug].draft.md`.
2. The **full, verbatim stdout** of `compliance.py --queue` for that draft.
3. Evidence that `internal-linking-strategist` ran: each link's anchor, URL and the section plus first 8 words where it was inserted. If zero, the reason. URLs without insertion evidence count as improvised.
4. FAQ sources and evidence-bank facts used.

**Fingerprint rule.** The parent checks each payload for the literal string `AEO compliance report for` and at least one `[PASS]`, `[FAIL]` or `[WARN]` line. If either is missing, treat it as "script not run", re-run in the parent, and mark the draft higher-risk.

**Parent verification:** re-run compliance on every draft; if `internal_links` WARNs, run `internal-linking-strategist` from the parent; check that no two drafts in the batch now use the same unique fact; then deliver.

Known failure modes: invented compliance output (unicode checkmarks, prose summaries), dropped linking step, summary with an extra paragraph or a "TL;DR" heading, em dashes, and two parallel drafts answering each other's FAQs.

## Related skills

- `glossary-content`: "What is [term]?" entries; Answer pages link to them
- `blog-seo-content`: opinion, original research, narratives, honest listicles
- `internal-linking-strategist`: called by this skill; do not reimplement
- `webflow-publisher`: publishes the `.draft.md`
- `site-intelligence`: audits beyond single-page checks
- Shared: `$MT_REPO/scripts/intent_match.py`, `messaging/evidence-bank.md`

## Open items

- **Answers Webflow fields.** Confirmed against the live collection on 2026-10-01 (see "Publishing to Webflow"). Still open: add fields for last-updated date, author and reviewer so freshness and expertise are visible on the page. Needs whoever manages the Webflow CMS (the repo names Stefan).
- **Queue access.** The skill reads a CSV export of the Queue until an automated Google Sheets connection is set up and signed off by IT.
- **Evidence bank growth.** Product facts are empty and platform benchmarks are pending Legal. Until they fill up, many pages will be limited to the legacy approved ranges and customer stats, which is exactly what the usage caps are designed to flag.
