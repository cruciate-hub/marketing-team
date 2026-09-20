---
name: glossary-content
description: >
  Writes glossary entries for the social.plus /glossary/ collection —
  short, definition-focused pages engineered to build topical authority
  for high-value terms, feed internal linking, and rank for definitional
  search queries ("what is X"). Strict format: 6 fixed sections, at least
  one table, answer-first definition, concise (500-900 words). Always use
  this skill for glossary entries, dictionary terms, or "add X to the
  glossary" requests — including when the term already exists on
  social.plus/glossary and needs a rewrite, since the existing collection
  was produced with early-generation AI and does not meet current
  formatting or citability standards.

  Do NOT use for: /answers/ pages (use aeo-content); blog posts (use
  blog-seo-content); website page copy (use brand-messaging).
when_to_use: >
  Trigger phrases: "glossary entry", "glossary page", "add to the
  glossary", "define X for the glossary", "glossary term", "dictionary
  entry for X", "rewrite the glossary page for X".
---

# social.plus Glossary Content

Glossary entries live at `social.plus/glossary/[slug]`. They exist to do three things at once: rank for short definitional searches, get cited by AI engines answering "what is X", and anchor internal links from blog and answer pages back to a stable definition. Every rule below serves one of those three goals — if a decision doesn't obviously serve one, cut it.

**Why this skill exists.** The current glossary was written when LLMs were new and used without much editorial structure — the result reads as generic AI filler (e.g. the live `active-user` entry currently says leveraging the metric "can be a game-changer," and has no tables, no metrics breakdown, and no related-terms section). Model quality has improved substantially since; this skill is stricter than that first pass, not just newer.

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

## Before writing

### 1. Duplicate-topic check (reuse, don't reimplement)

Run `MT_REPO=/tmp/cruciate-hub-marketing-team python3 "$MT_REPO/marketing-team/skills/aeo-content/scripts/duplicate_check.py" "<term>"`. It already reads both `pages-glossary.json` and `pages-answers.json` and reports matches above a 0.5 coverage threshold.

- **Exit 0 / `RESULT: CLEAN`** — proceed.
- **Exit 1 / `RESULT: MATCHES`** — if the match is the *same term already on the glossary*, this is a rewrite, not a new page: keep the existing slug and URL, rewrite the content in full against this skill's structure, and say so explicitly to the user ("rewriting the existing glossary entry, not creating a duplicate"). If the match is in `/answers/` instead, flag it — the term likely belongs to one collection, not both; ask which one before writing.
- **Exit 2 / `RESULT: UNVERIFIED`** — do not proceed without manually checking `pages-glossary.json` for the term.

### 2. Brand-messaging read (non-negotiable)

Read `messaging/terminology.md` and `messaging/tone.md` from the cloned repo. If the entry's "and social.plus" section will make any product or comparative claim, also read `messaging/positioning.md` and `messaging/value-story.md`. Do not proceed on memorized brand content if any file fails validation.

### 3. Scope check — does this term deserve a glossary page?

The strategy is explicit that glossary pages are for **high-value, specific terms** — not everything. Before drafting, confirm the term is:
- A concept a prospect or user would plausibly search "what is [term]" for, on its own, outside the context of a full article
- Narrow enough to answer completely in 500-900 words — if the term actually needs 1,200+ words to do justice to, it's a blog or answer topic, not glossary (flag this to the user instead of padding a thin glossary page)

## Structure — six fixed sections, in this order

Unlike `aeo-content` (which branches by query intent), glossary entries use **one fixed template** every time. This is deliberate: appsflyer.com/glossary and adjust.com/glossary — the reference standards named in the strategy — both use a rigid, repeatable structure across their entire glossary, which is part of what makes them easy to scan and easy for AI engines to learn to extract from consistently.

1. **Definition** — the entry's only H1 is the term itself. Immediately below the metadata block, the first paragraph is the definition: 1-2 sentences, 30-50 words total, containing the exact term. No throat-clearing, no "in the world of digital platforms" preamble — the current social.plus glossary's biggest weakness is starting with scene-setting instead of the answer. This paragraph is the block an AI engine extracts verbatim, so it must stand alone as a complete, correct answer to "what is [term]?"

2. **Why [Term] Matters** (H2) — 2-4 sentences on the practical benefit of tracking/understanding/using this term. Concrete, not aspirational — "helps X team decide Y," not "can be a game-changer."

3. **[Term] Metrics** or **How to Measure/Calculate [Term]** (H2) — only when the term is quantifiable. **This section requires a markdown table** — a breakdown of variants (like DAU/WAU/MAU), a formula, or a comparison of measurement approaches. This is the section AI engines lift most reliably (tables are the single highest-value structural element for AI readability), and it's also the section the current glossary is missing entirely. If the term genuinely isn't quantifiable (e.g. an abstract concept with no formula or metric), rename this section to fit — e.g. "Types of [Term]" or "How [Term] Works" — but it must still contain a table of some kind (a comparison, a breakdown, or a decision matrix). No glossary entry ships without at least one table.

4. **[Term] and social.plus** (H2) — connects the term to the product. This is the section most exposed to overclaiming — every specific or numeric claim about social.plus here must come from the approved-data list (fetch it from `aeo-content`'s "Approved data and customer names" section; this skill doesn't carry its own copy). If there's no approved data point that genuinely fits, keep this section to a general, honest statement of relevance rather than inventing a stat.

5. **Key Takeaways** (H2) — 3-4 bullet points, each one sentence, recapping the definition, the "why it matters," and the one metric/formula from section 3. This is the second-most-extractable block after the definition — write it as if it's the only section an AI engine reads.

6. **Related Terms** (H2) — 3-6 internal links to other glossary or answer entries. This is the section that does the internal-linking work the strategy calls out explicitly (2. Content Types & Goals: "Related Terms (For internal linking)"). Populated by `internal-linking-strategist` (see below), not improvised. **Must be the last section in the document — nothing follows it.** `compliance.py` enforces this as a FAIL, not just checking that the section exists: the internal-linking section is deliberately placed last so a reader (or an AI engine extracting the page) still reaches it after everything else.

## Formatting rules that make this different from the old glossary

Pulled directly from what appsflyer.com/glossary and adjust.com/glossary do well, and what social.plus's current glossary (built pre-this-skill) does not:

- **Answer-first, not scene-setting.** Never open with "In the world of X" / "In today's landscape" / "Understanding X is pivotal for." Open with the answer.
- **At least one table, every entry.** Not optional, not "where it fits naturally." If section 3 can't produce a real table, the entry needs a table somewhere else (a comparison of related terms, a decision matrix in "Why it matters") — see compliance check `has_table`.
- **Concise over comprehensive.** 500-900 words. This is a glossary, not a blog post — per the strategy doc, resist the pull to turn it into a long-form article. If a draft exceeds 900 words, that's a signal a sub-topic wants to be its own answer or blog page, not more glossary content.
- **No filler transitions or hedge words.** Same FAIL/WARN vocabulary tiers as `blog-seo-content` and `aeo-content` (see `scripts/compliance.py`) — "game-changer," "pivotal," "delve," "digital landscape," "leverage" as a verb, "unlock the power," "revolutionize," etc. are hard blocks. The live `active-user` entry currently fails this check twice over; don't reproduce that pattern.
- **One worked example where it clarifies a formula or metric.** AppsFlyer's DAU/MAU worked example ("2,000 DAU / 8,000 MAU = 25% stickiness") is the model — concrete numbers, not abstract description.
- **No H3s.** Glossary entries are short enough that H2-only keeps the structure flat and scannable; if a section needs sub-headings, it's grown into blog- or answer-length content and should be scoped down or moved.

## Markdown intermediate structure

```
# [Term]

Meta description: [≤160 chars, includes the term]
Slug: [lowercase-with-hyphens]
Alt text: [for any diagram/formula image, if used]
Category: [topic category — reuse blog-seo-content's Main Category Tag list where it fits, e.g. Engagement, Retention, Acquisition]

[Definition paragraph — 30-50 words, contains the exact term]

## Why [Term] Matters

...

## [Term] Metrics
(or "How to Calculate [Term]" / "Types of [Term]" — pick whichever fits; must contain a table)

| ... | ... |
|---|---|

## [Term] and social.plus

...

## Key Takeaways

- ...
- ...
- ...

## Related Terms

- [Related term 1](URL)
- [Related term 2](URL)
```

No HTML in the intermediate. Internal `<a href>` / markdown links in "Related Terms" are added by `internal-linking-strategist`, not improvised (see below). This exact shape is also what `webflow-publisher` converts for publishing (see "Publishing to Webflow"), so keep the `Slug:` line equal to the live slug on a rewrite and never add HTML to work around a formatting need.

## Internal linking

Before running compliance, invoke `internal-linking-strategist` in **draft mode**, passing the full draft, the term as target keyword, the category, and content type: `glossary`. Per its own "Standalone draft mode" routing rule, it fetches `pages-marketing.json`, `pages-use-cases.json`, `pages-industry.json`, and `pages-glossary.json` by default, and will ask whether to also pull in `pages-answers.json` (or blog/customer-stories) — say yes when the term plausibly has a related `/answers/` page.

(Note: this step must come before compliance, not after. `compliance.py`'s `related_terms_links` check FAILs on fewer than 2 links, so a draft can never legitimately "pass compliance" while Related Terms is still empty — invoking the optimizer first is the only ordering that works. This is a glossary-specific constraint: `aeo-content`'s own internal-link check is WARN-only, not FAIL, so it isn't forced into this ordering the way this skill is — glossary-content simply chooses to place the step here regardless.)

- Populate "Related Terms" from its output — this is the section that exists specifically for this purpose, so it should rarely come back empty. If it does, surface that to the user rather than inventing related terms from memory.
- Additional inline links elsewhere in the body (e.g. linking "retention rate" the first time it's mentioned in "Why It Matters") follow the same rule as `aeo-content` and `blog-seo-content`: only from the optimizer's output, never improvised.

**This must be a real invocation, not a substitute.** Confirming a URL exists in `pages-glossary.json` (e.g. via `duplicate_check.py` output or a manual grep) is not the same as running `internal-linking-strategist`'s two-phase shortlist-plus-live-fetch process, and does not satisfy this step. This distinction is here because it was observed in practice: this step was silently replaced with a manual lookup that produced real, valid URLs but skipped the optimizer's cannibalization check and anchor-distribution rules — which read as compliant but wasn't.

**Required evidence (paste into your response before delivering).** `aeo-content` requires this same class of evidence in its parallel-subagent batch mode, for a related reason (batch orchestration was observed silently dropping this step there too); this skill requires it on every draft, batch or not, since the same drop-off can happen in a single-draft run:
1. The full labeled output block `internal-linking-strategist` returns (starts with `## Internal link suggestions`). If that heading is missing from what you're about to paste, the skill was not actually invoked — go back and invoke it for real.
2. For each Related Terms link used: the `**Anchor:**`, `**Target:**` URL, and `**Reasoning:**` line the optimizer gave for it, exactly as it returned them. (Whether its `Insert at` sentence-quote field is populated for a Related Terms suggestion depends on how the optimizer itself treats list-style output — don't assume it's absent and don't fabricate one either way; paste whatever it actually returned.) A URL you sourced yourself (grep, memory, or a duplicate-check hit) without this evidence is an improvised link per BLOCK condition 3 below, even if the URL itself is correct.

Save this evidence block verbatim to `outputs/[slug].links.md` alongside the draft — see "Compliance" below for why.

## Compliance

Run `python3 scripts/compliance.py outputs/[slug].draft.md` before delivering any draft, and again after every edit. Paste the full stdout into your response — a manual eyeball pass is not a substitute (this is the same rule `blog-seo-content` and `aeo-content` enforce, and for the same reason: eyeball review reliably misses meta-description length, em dashes, and forbidden terms).

The script checks: metadata completeness, word count (500-900), the answer-first definition (first paragraph ≤50 words, contains the term), presence of a markdown table, presence and length of Key Takeaways, presence of Related Terms links, Related Terms being the final H2 section (not just present — a draft with it placed mid-document FAILs), presence of a matching `outputs/[slug].links.md` evidence file with a real Anchor/Target/Reasoning entry (not just a bare Target line) covering every Related Terms link, and the shared forbidden/risky vocabulary tiers. When the site's `pages-glossary.json`/`pages-answers.json` snapshots are readable, it also confirms every Related Terms URL corresponds to a real published page. See the script's own docstring for the full list and `--json` output mode.

The `.links.md` check is a mechanical backstop, not a replacement for honesty: a determined agent can still hand-type a fake evidence file with real Anchor/Target/Reasoning content for a URL that's genuinely on the site. But it turns "trust the agent's paste" into a checkable, diffable artifact a human (or the script) can inspect independently, and it closes off the cheapest fabrication (a bare URL list, or a URL that doesn't exist), instead of relying purely on the same agent that skipped the step to self-report accurately.

### BLOCK conditions — holistic veto (same class as blog-seo-content/aeo-content)

A fired BLOCK condition vetoes delivery regardless of a clean compliance run:

1. **Unresolved script FAIL**, or the script wasn't re-run after the latest edit.
2. **Unverifiable claim about social.plus** in the "and social.plus" section not traceable to the approved-data list.
3. **Improvised internal link** — any "Related Terms" entry or inline link not returned by `internal-linking-strategist`, including a technically-valid URL sourced by the writer directly instead of through the optimizer's actual draft-mode run (see "Required evidence" above) — valid-but-improvised still fires this condition.
4. **Missing table** — section 3 (or any section) shipping without at least one markdown table.
5. **Missing named editor at publish handoff** — same rule as `blog-seo-content`: `Editor (named human reviewer): [fill before publish]` must be present in the delivered metadata and filled with an actual named human before this is marked publish-ready.

## Delivery

Same cascade as `blog-seo-content` and `aeo-content`:

1. **Google Drive MCP**, if available — create the `.docx` directly via `anthropic-skills:docx` then upload.
2. **Suggest connection**, if not available — offer to help connect it, then fall through.
3. **Fallback**: create the `.docx` locally via `anthropic-skills:docx` and present it for download.

The `.docx` is the review artifact. Publishing does not go through it: the shared `webflow-publisher` skill converts this skill's `outputs/[slug].draft.md` directly (see "Publishing to Webflow" below). No `.docx`-to-Webflow-HTML automation exists anywhere in this repo — `aeo-content`'s SKILL.md still describes one, but nothing implements it, and `blog-seo-content`'s real publish path is `blog-publisher`, a Google Doc adapter, not a `.docx` converter.

Every delivery carries `Editor (named human reviewer): [fill before publish]` in its metadata block, and the delivery message states the draft isn't publish-ready until a named editor completes a pass.

## Publishing to Webflow (via `webflow-publisher`)

This skill's `outputs/[slug].draft.md` **is** the common intermediate `webflow-publisher` consumes: `# Term` as the only H1, the labeled metadata block, six H2 sections, a markdown table, Related Terms as markdown links. No `.docx` round-trip, no hand-written HTML. Run only after `compliance.py` passes on the current text and a named human editor has signed off:

```bash
# 0. Readiness check (should show "ready" — see below if it doesn't)
python3 "$REPO/scripts/webflow-publisher.py" --list-collections

# 1. Convert. The definition paragraph stays as the first <p> of the body; the Metrics table lands
#    in a Webflow Embed block; Related Terms links become same-tab <a href> tags.
python3 "$REPO/scripts/md_to_webflow_html.py" outputs/[slug].draft.md --collection glossary \
  --out outputs/[slug].fielddata.json

# 2. Validate, no token needed. --source enables the source-vs-output table count, so a Metrics
#    table that collapsed into prose fails here regardless of what the section is called.
python3 "$REPO/scripts/webflow-publisher.py" outputs/[slug].fielddata.json --collection glossary \
  --source outputs/[slug].draft.md --dry-run

# 3a. NEW term: create + publish (--staged to review in Webflow first). A slug collision stops the
#     run — never append a suffix.
python3 "$REPO/scripts/webflow-publisher.py" outputs/[slug].fielddata.json --collection glossary [--staged]

# 3b. REWRITE of a live entry (the common case): keep the live slug via the draft's `Slug:` line and
#     patch the existing item in place. Find the id: GET /v2/collections/66e2765d540e1939a89db93e/items?slug=[slug]
python3 "$REPO/scripts/webflow-publisher.py" outputs/[slug].fielddata.json --collection glossary --replace <item_id>
```

**Current state: unblocked as of 2026-09-18.** This skill's own `webflow-fields.json` (collection `66e2765d540e1939a89db93e`, from `pages-glossary.json`) has `fields.body` and `metadata['Meta description']` confirmed against the live Webflow schema via `scripts/sync_fieldmap.py`. The collection genuinely has no `intro`, `date`, `Alt text` or `Category` field — confirmed absent, not unconfirmed — so `--dry-run` passes `fieldmap:required-slugs-confirmed` and step 3 publishes. If a future re-run of `sync_fieldmap.py --collection glossary` reports `--list-collections` as UNCONFIRMED again (e.g. Webflow added a required field), do not fill in a plausible-looking slug to get past it: run `python3 "$REPO/scripts/sync_fieldmap.py" --collection glossary` (needs `WEBFLOW_API_TOKEN`) and resolve whatever it flags as ambiguous or unmatched by hand.

## Rewriting an existing entry (the common case, initially)

Since the primary near-term job is fixing the existing ~76-entry glossary rather than writing net-new terms, rewrites are a first-class workflow, not an edge case:

1. Pull the current live content for the term (via `pages-glossary.json`'s `content` field for the heading structure, and a live fetch of the URL for full text) so you can see exactly what's being replaced.
2. Rewrite against the six-section structure above — don't patch the old structure, replace it. The old headings ("Introduction to X," "Understanding X: A deep dive," "X vs. traditional Y") don't map onto the new sections and shouldn't be preserved for continuity's sake.
3. Keep the same slug and URL unless the user says otherwise — rewrites should not create redirect debt.
4. Flag in the delivery message that this is a rewrite of an existing live page, not a new one.

## Batch rewrites

When asked to rewrite multiple existing entries at once (e.g. "redo the first 10 glossary pages"), follow the same phased/parallel-subagent orchestration *pattern* `aeo-content` uses for batches — see its SKILL.md "Batch workflow" and "Parallel-subagent orchestration" sections for the approval syntax and per-article overview tracking. Don't reinvent that orchestration here; the failure modes are the same regardless of content type.

**Do not import aeo-content's compliance-output fingerprint string or its internal-link evidence format as-is — they don't match this skill's own mechanisms:**
- aeo-content's fingerprint rule checks a subagent's payload for the literal string `AEO compliance report for`. This skill's own `compliance.py` prints `Glossary compliance report for {path}` — a parent verifying a glossary batch subagent's payload must check for *that* string instead, or the fingerprint check silently never matches anything.
- aeo-content's batch-mode internal-link evidence is a prose block pasted into the subagent's return payload (per-class link counts and quotes), not a written file. That does not produce this skill's required `outputs/[slug].links.md` sibling file, and `compliance.py`'s `links_evidence_file` check will FAIL every batch item if a subagent follows aeo-content's evidence format literally instead of this skill's. Each glossary batch subagent must still save its own `internal-linking-strategist` output to `outputs/[slug].links.md` per this skill's "Required evidence" section above, and the parent verifying batch output should require that exact evidence, not aeo-content's prose-paste equivalent.

## Open items (surface these to the user, don't guess silently)

- **Five live Webflow fields have no mapping in `webflow-fields.json` and their purpose is unconfirmed:** `term`, `term-alternative-name` (both PlainText), `meta-title` (PlainText, displayed "Title & Meta title"), `exclude-indexing-letters` (PlainText, displayed "Indexing"), `not-in-use` (Switch). Whether this skill's draft should populate any of them is Stefan's call — don't guess.
- **Topic category list** — the live Glossary collection has no Reference/Category field at all (confirmed 2026-09-18, not just unconfirmed), so this skill's borrowed `blog-seo-content` Main Category Tag list has nowhere to publish to. The `Category:` metadata entry was removed from `webflow-fields.json` rather than left `null`. Confirm with Stefan whether the `Category:` line in the draft should be dropped entirely or kept for some other purpose (e.g. internal organization only, never sent to Webflow).
- **Rewrites publish via `--replace <item_id>`**, which needs the live item ID (slug lookup). The collection has no date field, so a rewrite cannot restamp a "last updated" date (brain.md guardrail 6: honest freshness) — confirmed, not an open question.

## Related skills

- `webflow-publisher` — publishes this skill's `.draft.md` to the Glossary collection; owns conversion, dry-run and the Webflow API calls. This skill owns the field map (`webflow-fields.json`) that tells it how.
- `aeo-content` — /answers/ pages; source of the approved-data list and the duplicate-check script this skill reuses
- `blog-seo-content` — blog posts; source of the forbidden-vocabulary tiers this skill's compliance script mirrors
- `internal-linking-strategist` — called by this skill; do not reimplement
- `site-intelligence` — for auditing the glossary collection beyond single-entry duplicate checks
