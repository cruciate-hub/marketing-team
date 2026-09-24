---
name: content-planner
description: >
  Plans social.plus SEO/AEO content from a single human seed (a keyword,
  phrase, prompt or written idea). Researches the seed, proposes candidate
  articles across Glossary, Answer and Blog (zero to ten per collection),
  checks every candidate against the Content Queue and published pages for
  duplication and cannibalisation, and outputs paste-ready Queue rows plus
  a review report. The first step of the content engine; never writes the
  articles themselves.

  Do NOT use for: writing articles (glossary-content, aeo-content,
  blog-seo-content); LinkedIn content calendars (linkedin-content-planner);
  site-wide audits (site-intelligence); SEO keyword research on its own
  (seo-intel).
when_to_use: >
  Trigger phrases: "plan content for X", "what articles can we write about
  X", "content ideas for X", "run the planner on X", "new seed: X",
  "add ideas for X to the queue".
---

# Content planner

The first step of the social.plus content engine:

**Seed (human) > plan (this skill) > duplication check > Queue rows at `Idea` > human approves > writing skill > human review > publish.**

The planner's job is to find every article a seed genuinely deserves, and nothing more. It never approves, prioritises or writes anything. Those decisions stay with a human.

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

The planner uses `scripts/plan_rows.py` (this skill) and the shared `$MT_REPO/scripts/intent_match.py`.

## Inputs

- **The seed.** A keyword ("app retention"), a phrase, a prompt ("how do fitness apps keep users?") or a written idea. If it has two plausible meanings, ask one question; otherwise proceed.
- **The Queue, exported as CSV** (Queue tab, File > Download > CSV). Required: it holds every planned, published and rejected idea, and it's how new rows get the next free ID. Without it, stop and ask for it. Never plan against published pages alone: two seeds a week apart would propose the same unpublished idea twice.
- **Optional:** constraints from the person ("only Answer pages", "fintech angle", "skip anything needing Legal").

## Steps

### 1. Load context

Run the fetch block. Read `messaging/terminology.md`, `positioning.md`, `value-story.md` and `messaging/evidence-bank.md`. Skim the Queue: which clusters exist, what's planned near this seed, what was rejected.

### 2. Research the seed

- **Split it like an AI engine would.** List the sub-questions an engine would plausibly search if a product manager or developer asked about the seed (see `references/ideation-lenses.md`).
- **Real demand.** With Ahrefs MCP: `keywords-explorer-matching-terms` with `terms=questions` (one call, `limit` 30 to 50; each row costs about 20 API units) and `serp-overview` on the head term for People Also Ask. Without Ahrefs, web search. Discard noise that has nothing to do with social.plus's audience. Most useful questions will show little or no search volume; that is normal for AEO and not a reason to drop them.
- **What we can uniquely say.** Check the evidence bank and, for implementation topics, social.plus documentation. A question we can't add anything to is not worth a page.

### 3. Generate candidates

Walk the lenses in `references/ideation-lenses.md` for each collection. Every candidate needs:

| Field | Rule |
|---|---|
| collection | Glossary ("What is [term]?" only), Answer (one journey question), Blog (opinion, research, narrative, honest listicle, trend) |
| intent | Glossary: definition. Answer: how-to, decision, explainer, playbook. Blog: opinion, original research, listicle, narrative, trend |
| question | The canonical question, phrased as people ask it |
| first_sentence | The page's opening answer, max 60 words. This is what duplication is judged on |
| headings | 2+ sub-questions (Answer and Blog) |
| info_source | The unique information the page will carry. Mark "pending" if it depends on unapproved data |
| premise | Source for any assumption in the question |
| demand, cluster, stage, dependencies, suggested_priority | As available |

Apply the permutation rules at the end of the lenses file before moving on. Prefer three strong candidates to ten plausible ones. Zero for a collection is a fine answer.

### 4. Run the gate

Write the candidates to `outputs/candidates.json` (schema in the `plan_rows.py` docstring), then:

```
python3 scripts/plan_rows.py --candidates outputs/candidates.json --queue queue.csv \
  --seed "<seed>" --seed-type <keyword|phrase|prompt|idea> --entered-by "<name>"
```

- `RESULT: INVALID` (exit 1): fix what it lists (missing fields, wrong collection for the question form, duplicates inside the batch, unknown dependencies, over the cap) and re-run.
- `RESULT: PLANNED` (exit 0): open the report.
- For every "Needs review against" entry, apply the test: **would the two pages open with the same first sentence?** If yes, drop the candidate from the JSON (or turn it into a Merge note) and re-run. If no, keep it and say in one line why it differs. Also scan the "Same cluster in Queue" column for near-neighbours the matcher missed.

The matcher is a lexical approximation with a question-form adjustment. It surfaces candidates for judgment; it doesn't replace it.

### 5. Present the plan

In chat:
- One summary line: new rows by collection, merges, updates, rejects, blocked.
- A short table of the new rows (ID, collection, question, status) with one line each on why it earns a page.
- The changes to existing rows (merges, refresh suggestions), for a human to apply.
- Warnings that need a decision (missing premise sources, year in a title, borderline overlaps).

Deliver `outputs/plan-[seed].csv` (paste into the Queue tab, below the last row) and `outputs/plan-[seed].md` (the full report, including the Seeds tab row).

## Rules

- **Never set Status beyond `Idea` or `Blocked: needs data`, and never fill Priority, Target publish date or Reviewer.** Suggested priority goes in Notes. A human decides what gets written and when.
- **Never delete or renumber rows.** New IDs continue each collection's sequence (GL, AN, BL); rejected ideas stay in the Queue so they aren't proposed again.
- **Merges and updates change existing rows, not new ones.** The planner lists them; a human applies them.
- **No promotional questions.** Don't propose an Answer whose honest answer is "social.plus", or a self-ranking "best X" outside the Blog.
- **Stay in scope.** The planner proposes; the writing skills write.

## What happens next

A human reviews the new rows in the Queue, sets the ones worth writing to `Approved`, sets priority and cadence, and hands them to the writing skill for their collection: `glossary-content`, `aeo-content` (v2 reads Approved rows directly) or `blog-seo-content`.

## Tests

```
python3 marketing-team/skills/content-planner/tests/run_tests.py
```

Run after changing `plan_rows.py` or `scripts/intent_match.py` (and run `aeo-content/tests/run_tests.py` too, since both depend on the matcher).

## Open items

- **Queue access.** The planner reads a CSV export and outputs rows to paste. Writing to the Google Sheet automatically needs an integration signed off by IT.
- **Call transcripts as seeds.** Once Gong is in place, sales and support questions can feed the planner as seeds and as unique information.
- **Blog skill.** `blog-seo-content` doesn't read Queue rows yet; until it does, pass it the approved row's question, sub-questions and information source by hand.
- **Glossary skill.** `glossary-content` still runs its own title-based duplicate check; it should move to `intent_match.py` so all three writing skills judge duplication the same way.
