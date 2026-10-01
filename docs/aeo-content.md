# AEO Content (v4, skill v2)

Claude skill for writing `/answers/` pages at `social.plus/answers/[slug]`: one page per specific buyer or developer question, built to be cited by AI engines and useful to the reader.

**Big change from earlier versions:** the skill no longer invents article ideas. It writes only from an **Approved** row in the Content Queue (Google Sheet). Ideas come from the content engine's planning step, and a human approves which rows get written. "What is [term]?" pages moved to `glossary-content`.

## Getting started

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

### 2. Writing one page

1. In the Content Queue, set the row's Status to **Approved**.
2. Export the Queue tab as CSV (File > Download > CSV) and attach it, or paste the row.
3. Ask: `Write Queue row A1 for /answers/`.
4. Claude runs the duplication check, reads the brand files and the evidence bank, drafts, links, runs compliance and hands you a `.docx` plus the Queue update to paste back (Status: In review).

If you ask for a page that isn't in the Queue, Claude drafts the row first and asks you to confirm it.

### 3. Writing several pages

Ask: `Write A1, A3 and D1`. Claude checks every row first (approved, dependencies published, no duplicates, evidence available), reports anything it had to skip, then drafts. See `references/workflow-phases.md`.

### 4. Reviewing a draft

Check facts, premises, claims about social.plus and anything Legal-sensitive. The draft carries `Editor (named human reviewer): [fill before publish]`; put your name there when it's ready. Edits: `revise: A3 — shorter summary`.

### 5. What this skill does NOT do

- Generate topic ideas (planning step)
- Glossary entries (`glossary-content`), blog posts, opinion, research or "best X" lists (`blog-seo-content`)
- Publish without a named human reviewer

## Maintainer notes

### The four templates

| Intent | File | For |
|---|---|---|
| how-to | `references/patterns/how-to.md` | Carrying out a task |
| decision | `references/patterns/decision.md` | Build vs buy, cost, timeline, X or Y |
| explainer | `references/patterns/explainer.md` | Why, does, what is a good... |
| playbook | `references/patterns/playbook.md` | Vertical use of social features |

All share `references/patterns/_shared.md`.

### Shared pieces outside the skill

- `scripts/intent_match.py` (repo root): duplication check on meaning, used by this skill and the planning step.
- `messaging/evidence-bank.md`: every approved fact, with usage caps. Also used by `glossary-content` and `blog-seo-content`.

### Compliance, locally

```
python3 marketing-team/skills/aeo-content/scripts/compliance.py outputs/[slug].draft.md --queue queue.csv
```

### Tests

```
python3 marketing-team/skills/aeo-content/tests/run_tests.py
```

Run after changing `compliance.py`, `intent_match.py`, or the customer table in the evidence bank. Fixtures in `tests/fixtures/` are synthetic and not for publication.

### File layout

```
marketing-team/skills/aeo-content/
├── SKILL.md
├── webflow-fields.json            Answers field map (confirmed 2026-10-01)
├── references/
│   ├── patterns/_shared.md        Page shape used by every template
│   ├── patterns/how-to.md
│   ├── patterns/decision.md
│   ├── patterns/explainer.md
│   ├── patterns/playbook.md
│   ├── writing-style.md
│   ├── citation-playbook.md
│   └── workflow-phases.md         Batch workflow (approved Queue IDs)
├── scripts/
│   ├── compliance.py
│   ├── duplicate_check.py         Legacy title check, no longer used by any skill (kept because the canonical fetch block cites it as an example)
│   └── make_zip.py
└── tests/
    ├── run_tests.py
    └── fixtures/
```
