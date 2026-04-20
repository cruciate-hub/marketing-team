# Batch workflow — detailed phase specs

Use this file when the brief is a batch request (multiple articles, theme, or "ideas"). The single-article flow lives in SKILL.md; this file is only for the four-phase batch workflow.

Every phase produces a markdown artifact in `outputs/`. The colleague reviews each artifact in the Claude.ai artifact panel and approves or refines via chat. The skill parses her approval lines at the start of each turn and updates the artifact.

---

## Approval syntax (parse first on every turn)

```
approve: 1, 3, 5-7
drop: 2, 6
revise: 4 — make it about retention
next
```

For Phase B (scoped per article):

```
article 1: approve 1-4, drop 5
article 2: approve 1, 3, 5; revise 2 — drop the pricing angle
next
```

Rules:
- Ranges (`5-7`) expand inclusively.
- `approve` is additive — items not mentioned stay in the "pending" state.
- `drop` removes items from the set.
- `revise N — [instruction]` updates item N with the instruction, keeps it in the set.
- `next` moves to the next phase. Require explicit `next` — do not auto-advance.
- Free-form messages that don't match ("can we make 3 more technical?") fall back to natural-language understanding — infer the intent, then echo back as a parsed approval line so the colleague sees what the skill heard.

---

## Phase A — Ideas

### Input
- Brief (from intake): topic area, audience, rough count, constraints.
- Brand-messaging fetch (terminology, tone, narrative, value-story, positioning, boilerplates) — done once at Phase A, reused across the batch.
- Duplicate-scan: `pages-answers.json` and `pages-glossary.json` to surface gaps vs. existing coverage.
- **Optional (Ahrefs MCP tools):** `keywords-explorer-overview` for real search volume + keyword difficulty on each candidate's target keyword; `site-explorer-organic-keywords` on existing /answers/ URLs to catch semantic-duplicate topics the JSON scan missed. Graceful fallback to qualitative scoring if Ahrefs is unavailable.

### Output — `outputs/ideas.md`

```markdown
# AEO Article Ideas

Brief: [one-line summary of the colleague's ask]
Generated: YYYY-MM-DD · 12 candidates · approved: 0 of 12

| # | Title | Intent | Rationale | Target keyword | Fit |
|---|---|---|---|---|---|
| 1 | What are in-app activity feeds? | definition | No existing /answers/ page; high search volume | in-app activity feeds | high |
| 2 | How to add chat to a mobile app | procedural | Adjacent to existing chat content; good query match | add chat to mobile app | high |
| ... |

## Approval syntax
`approve: 1, 3, 5` · `drop: 2, 6` · `revise: 4 — [instruction]` · `next`
```

Rules for the idea list:
- 8-15 candidates. Fewer if the topic is narrow; more if the brief is wide.
- **Intent column** is one of: definition, procedural, comparative.
- **Rationale** is one clause. Why this is a gap, or what query it would capture.
- **Target keyword** is the phrase that would appear in sentence 1 of the drafted article.
- **Fit** is high / medium / low. Reflect: search volume signals, existing coverage gaps, relevance to social.plus's category.
- Never propose ideas that overlap an existing /answers/ page without flagging it in the rationale ("existing /answers/activity-feeds covers this at a surface level; this is a deeper how-to").

### Transitions
- On `approve:` or `drop:`, rewrite the table to show only the approved set plus the pending candidates. Reflect approval counts in the header line.
- On `revise: N — [instruction]`, update that row's title and rationale to reflect the new angle. Keep it in the approved set.
- On `next`, move to Phase B and write `outputs/questions.md`. Keep `outputs/ideas.md` intact for the record.

### Abort
- Brand fetch fails → stop, tell her, do not proceed on memorized brand.
- All candidates overlap existing /answers/ → surface this and ask whether to shift to updating existing articles instead.

---

## Phase B — Questions

### Input
- The approved ideas from Phase A.
- For each approved idea, research candidate FAQ questions:
  - **Preferred (Ahrefs MCP tools available):** `serp-overview` for the core question (returns the literal PAA block), `keywords-explorer-search-suggestions` for question-form variants.
  - **Fallback (no Ahrefs):** `WebSearch` on the core question + a scan of the most relevant subreddit (top-of-all-time + top-of-year).

### Output — `outputs/questions.md`

```markdown
# FAQ Questions per Article

Approved articles: 3 · approved questions: 0 of 24

## Article 1 — What are in-app activity feeds?

Source: PAA for "activity feed", r/gamedev "community features" thread (2024)

| # | Question | Source |
|---|---|---|
| 1 | What is an activity feed? | PAA |
| 2 | Do activity feeds require a social graph? | PAA |
| 3 | Can activity feeds be added to existing apps? | PAA |
| 4 | Is an activity feed suitable for a fitness app? | Reddit r/gamedev |
| 5 | How long does it take to ship a feed? | PAA |
| ... |

## Article 2 — How to add chat to a mobile app

...

## Approval syntax
`article 1: approve 1-4, drop 5` · `next` when all articles are approved
```

Rules:
- 8-10 candidate questions per article.
- Each question has a **Source** column — one of `Ahrefs PAA` / `Ahrefs suggestions` / `WebSearch PAA` / `Reddit` / `LLM` — so the colleague can override any LLM-generated fillers.
- Approved questions become the FAQ section of the eventual draft.
- Final FAQ in each article = 4-6 of the approved questions. If the colleague approves more than 6 for one article, the skill picks the 6 best (most distinct, most citation-worthy) and lists the rest as "deferred" in `overview.md`.

### Transitions
- On per-article approvals, update the table for that article only. Other articles stay as-is.
- On `next`, proceed to Phase C and start drafting. Require all Phase A-approved articles to have at least 4 approved questions. If any article has fewer, tell her and stay in Phase B.

### Abort
- Question research fails for an article (no PAA, subreddit rate-limit, etc.) → flag it, offer a fallback list of LLM-generated questions marked as such, let her proceed or skip.

---

## Phase C — Drafts (batch)

### Input
- Approved ideas + approved questions from Phases A and B.
- Reuses the brand fetch from Phase A.

### Output

- `outputs/[slug].draft.md` — one file per approved idea. Follows the single-article format (labeled paragraph metadata under H1, answer-first block, TL;DR, body sections, FAQ from approved questions, pitch, conclusion). Pick the structure pattern by intent (`references/patterns/{definition,procedural,comparative}.md`).
- `outputs/overview.md` — single-source-of-truth batch summary:

```markdown
# Batch Overview

Brief: [one-line brief] · 3 articles · YYYY-MM-DD

| # | Title | File | Intent | Words | Compliance | Notes |
|---|---|---|---|---|---|---|
| 1 | What are in-app activity feeds? | [activity-feeds.draft.md](activity-feeds.draft.md) | definition | 1,002 | ✓ | — |
| 2 | How to add chat to a mobile app | [add-chat.draft.md](add-chat.draft.md) | procedural | 1,245 | ✓ | — |
| 3 | ... | ... | ... | ... | ⚠ 1 fail | meta description 174 chars |

## Edit syntax
`article 2: shorter` · `article 3: add a pitfalls section` · `article 1: make the pitch more specific`
## Advance
`deliver` — convert all to .docx and zip
```

### Draft rules
- Each draft must pass `python3 scripts/compliance.py outputs/[slug].draft.md` before it counts as "complete." Warnings are allowed; failures block delivery.
- Compliance status in `overview.md`:
  - ✓ — all checks pass
  - ⚠ — only warnings (usually word-count)
  - ✗ — at least one failure, with a one-phrase summary of the worst failure

### Edit cycle
- Colleague chats: `article 2: shorter` or `article 3: add a pitfalls section`.
- Skill edits the draft, re-runs `compliance.py`, updates `overview.md`. Does not touch other drafts.
- Repeat until the colleague says `deliver` or all rows show ✓.

### Transitions
- On `deliver`, require all rows to be ✓ or ⚠. If any ✗, refuse and name the articles to fix.

---

## Phase D — Delivery

### Steps

1. For each `outputs/[slug].draft.md`, invoke the `anthropic-skills:docx` skill to produce `outputs/[slug].docx`. Preserve H1, labeled metadata paragraphs, answer-first block, tables, lists, bold, hyperlinks.
2. Run `python3 scripts/make_zip.py --out outputs/aeo-batch-YYYY-MM-DD.zip` to bundle all `.docx` files. (Default: zip every `.docx` in `outputs/`. Customize with `--files`.)
3. Send the final chat summary:

```markdown
Batch ready — 3 articles delivered.

Files:
- [activity-feeds.docx](outputs/activity-feeds.docx)
- [add-chat.docx](outputs/add-chat.docx)
- [zero-party-data.docx](outputs/zero-party-data.docx)
- [aeo-batch-2026-04-20.zip](outputs/aeo-batch-2026-04-20.zip) — all three as a zip

FAQ source URLs (for your research log):
- activity-feeds: https://…, https://…
- add-chat: https://…, https://…
- zero-party-data: https://…, https://…

Click any file above to download it from the chat. The zip is the fastest way to grab the whole batch.
```

### What the downstream automation does

A separate automation (outside this skill) converts each `.docx` to Webflow-ready HTML and publishes to `/answers/[slug]`. That automation handles:
- Schema markup (Article, FAQPage, Organization, sameAs)
- Canonical URLs
- Open Graph / Twitter meta
- datePublished / dateModified

Which is why the skill's output is pure Word with no HTML anywhere.

### Abort
- `anthropic-skills:docx` unavailable → deliver the `.draft.md` files as fallback, tell the colleague the docx skill is missing, end the batch.
- Zip creation fails → deliver the individual `.docx` files without the zip, log the error.

---

## Maintenance notes

- Each phase writes only to `outputs/`. Do not touch files outside this directory during a batch.
- Old batches aren't cleaned up automatically. If `outputs/` fills up, add a cleanup step to Phase D or ask the colleague.
- The approval syntax is deliberately small. Do not add more commands without thinking — more syntax means more edge cases and harder-to-remember keywords.
