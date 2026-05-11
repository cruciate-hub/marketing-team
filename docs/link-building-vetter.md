# Link Building Vetter

Claude skill for vetting incoming ABC link exchange requests against social.plus guidelines.

Given a partner's proposal — anchor text, target URL, placement, and any text modifications — this skill scores it against a fixed rubric and drafts a polite but strict response email.

## What it does

- Checks the target social.plus article against an exclusion list (fully excluded vs anchor-only).
- Evaluates the proposal against hard guidelines: site quality, anchor quality, placement, text relevance, writing quality.
- Scores each applicable criterion 1–10 and returns an overall verdict: approve (8–10), revise (5–7), or reject (1–4).
- Drafts a ready-to-send response email tuned to the verdict.

## When it triggers

Any message that includes an incoming link exchange proposal — usually pasted from Slack, email, or LinkedIn. Trigger phrases include "review this link request", "vet this anchor", "check this backlink proposal", "score this modification", "is this article eligible", or "draft a response to this partner".

The skill is not for outbound link prospecting (see `backlink-placement-finder` for that).

## Workflow

1. Identify the request type — new anchor, anchor swap on existing link, or text modification.
2. Check article eligibility against `references/excluded-articles.md`:
   - Fully excluded → reject immediately, don't score.
   - Existing-anchor-only → text modifications not allowed; only anchor swaps on pre-existing links.
   - Everything else → full evaluation.
3. Score against `references/guidelines.md` on the applicable criteria.
4. Draft a response email using `references/email-templates.md` as the tone and structure baseline.

For ambiguous proposals that clear the hard-rule filter, the skill can fetch the live article (via WebFetch on the public URL) to verify tone, placement context, and whether the proposed addition reads naturally. Snippet-only evaluation is the default; full-article fetch is only used when the decision depends on it.

## Files

```
link-building-vetter/
├── SKILL.md                          Skill entry point — workflow, scoring, checklists
├── README.md                         This file
└── references/
    ├── excluded-articles.md          Two lists: fully excluded + existing-anchor-only
    ├── guidelines.md                 Hard rules: site, anchor, text, restricted categories
    └── email-templates.md            Approval, revision, and rejection templates
```

## Scoring rubric

| Criterion | What it checks |
|---|---|
| Site Quality | DR ≥ 50, page is blog/article/glossary, not in a restricted category |
| Anchor Quality | Not branded, short, reads naturally, provides reader value |
| Placement | Not in intro or conclusion, sits naturally in the body |
| Text Relevance | Aligns with article topic and the specific paragraph |
| Writing Quality | Human-written, matches article tone, no AI phrases |

Overall score = average of applicable criteria, rounded.

## Auto-rejects

Some proposals fail on a single hard rule and don't get scored:

- Article is on the fully excluded list.
- Article is existing-anchor-only but the proposal modifies or adds text.
- Target domain is in a restricted category (crypto, gambling, dropshipping, chatbots, converter tools, etc. — see `guidelines.md`).
- Target page is location-specific ("best X in India"), a homepage, product page, landing page, or service page.
- Target page competes with the article's ranking keywords.

## Maintenance

Update these files as guidelines evolve:

- **New article to exclude** — add its slug to the relevant section in `references/excluded-articles.md`.
- **New restricted category** — add to the list in `references/guidelines.md`.
- **Email tone adjustment** — edit `references/email-templates.md`. Templates are intentionally polite-but-firm; keep that register.
- **New evaluation criterion** — update both `SKILL.md` (checklist + scoring table) and `references/guidelines.md`.

## Webflow MCP note

If the Webflow MCP is connected, the skill treats its credits as scarce:

- Prefer WebFetch on the public blog URL over Webflow MCP for reading article content.
- Only use Webflow MCP when CMS-internal data is actually needed (existing anchors with their URLs, meta fields, draft state).
- Never execute write operations without explicit user confirmation.

## Output contract

Every evaluation returns, in this order:

1. Verdict (approve / revise / reject) with overall score.
2. Specific issues found, tied to the rubric criteria.
3. A draft response email in a code block, ready to paste.

No unsolicited next steps, no fluff, no additional analysis unless asked.
