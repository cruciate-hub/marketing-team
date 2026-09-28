# Batch workflow (v2)

In v1, batch mode started by inventing 8-15 article ideas. In v2, ideas come from the content engine's planning step and the Content Queue (Google Sheet). This skill only writes rows a human has set to **Approved**.

## Inputs

- A list of Queue IDs, for example `write A1, A3, D1`.
- The Queue exported as CSV (Queue tab, File > Download > CSV), or read through the Google Drive connector when available. The CSV also powers the FAQ overlap check (`compliance.py --queue`).

## Phase 1: Pre-flight (parent session, once)

1. Run the canonical fetch block.
2. For every ID: confirm Status is `Approved`, Collection is `Answer`, and every ID in Dependencies is `Published` (or approved to publish in the same batch, ordered first). Stop and list any row that fails.
3. Re-run `scripts/intent_match.py` for every row with its canonical question and draft first sentence. Rows are checked at planning time, but the queue may have changed since. Any `LIKELY DUPLICATE` stops that row.
4. Check `messaging/evidence-bank.md`: every row needs at least one `Approved` fact that fits and is under its cap. A row whose core claim depends on a `Pending` fact goes back to `Blocked: needs data`.
5. Post a one-table summary: ID, question, template, status of each check. Wait for `go` if anything was stopped; otherwise continue.

## Phase 2: Drafts

For each row, draft `outputs/[slug].draft.md` following SKILL.md and the template file for the row's intent. Parallel subagents are fine (see SKILL.md, "Parallel drafting"), but each draft goes through the same steps as a single article.

Write `outputs/overview.md`: ID, title, word count, compliance result, evidence-bank facts used, open questions for the reviewer.

## Phase 3: Review handoff

1. Convert each passing draft to `.docx`.
2. Bundle with `python3 scripts/make_zip.py` when there are more than two.
3. For each row, output the Queue update for a human to paste (or write it directly once the automated Sheets connection is approved): Status `In review`, Draft link, and the evidence-bank rows to update after approval.

## Approval syntax (for chat edits after drafts)

```
revise: A3 — shorter summary, add the fintech benchmark
drop: D4
approve: A1, A3
```

`approve` here means "ready for human review", not "publish". Publishing happens only after a named editor signs off.

## When to stop a batch

- Brand fetch fails: stop, report, do not write from memory.
- A row isn't `Approved` or its dependencies aren't met: skip it and say why.
- A draft fails compliance twice after rewriting: surface it instead of forcing it through.
