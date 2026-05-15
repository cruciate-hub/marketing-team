---
name: link-building-vetter
description: Vet incoming link building requests for social.plus ABC link exchanges. Use when reviewing backlink proposals, evaluating anchor text, checking article eligibility, scoring text modifications for contextual relevance and writing style, or drafting response emails to link building partners. Triggers on phrases like "review this link request", "check this backlink proposal", "vet this anchor", "is this article eligible", "score this modification", or "draft a response to this partner".
---

# Link Building Vetter for social.plus

Vet incoming ABC link exchange requests against social.plus guidelines. Score proposals numerically (1-10) and draft polite, constructive, but strict response emails.

## Workflow

1. **Identify request type** → anchor proposal, text modification, or full link request
2. **Check article eligibility** → see [references/excluded-articles.md](references/excluded-articles.md)
3. **Evaluate against criteria** → see [references/guidelines.md](references/guidelines.md)
4. **Score each criterion** → 1-10 scale with justification
5. **Draft response email** → approval, revision request, or rejection

## Scoring System

Score each applicable criterion 1-10:

| Criterion | What to evaluate |
|-----------|------------------|
| **Site Quality** | DR 50+, blog/article/glossary only, no restricted niches |
| **Anchor Quality** | No branded terms, short length, provides reader value |
| **Placement** | Not in intro/conclusion, provides reader value |
| **Text Relevance** | Aligns with article topic and paragraph context |
| **Writing Quality** | Human-written, matches article tone, no AI phrases |

**Overall score** = average of applicable criteria, rounded.

- 8-10: Approve
- 5-7: Request revision (specify issues)
- 1-4: Reject

## Evaluation Checklist

### Site/Page Requirements
- [ ] DR ≥ 50 (ask user to verify in Ahrefs if unknown)
- [ ] Page type: blog, article, or glossary only
- [ ] No homepage, product page, landing page, or service page
- [ ] No location-specific pages ("Marketing agency in Dubai")
- [ ] No highly niche industry blogs ("SEO Tips for Law Firms")
- [ ] Target page doesn't compete with article keywords

### Restricted Categories (auto-reject)
- Crypto, casino, gambling
- Design/editing software, presentation software/templates
- WordPress templates, chatbots, converter tools
- Brand name/logo generators, PC/OS cleanup apps
- QR code generators, dropshipping, B2C products
- "Ways to make money" content

### Anchor Text Rules
- [ ] No branded anchors (brand names)
- [ ] Short anchor text
- [ ] Not placed in introduction or conclusion
- [ ] Provides genuine reader value (not promotional)

### Text Modification Rules
- [ ] Aligns with article topic
- [ ] Fits the specific paragraph context
- [ ] 100% human-written
- [ ] Matches article's writing style and tone
- [ ] No AI phrases: "Additionally", "Furthermore", "Moreover", "In addition"
- [ ] Not duplicated on other websites

## Article Eligibility

Before evaluating, check article status in [references/excluded-articles.md](references/excluded-articles.md):

- **Excluded articles**: Not available for link exchanges (reject immediately)
- **Existing anchor only**: No text edits allowed (anchor changes only)
- **All other articles**: Full evaluation applies

## Webflow MCP Safety

If Webflow MCP is connected:
- **Minimize API calls** — Webflow MCP credits are limited. Only fetch what's strictly necessary.
- **Batch requests** — If multiple articles need checking, ask user which ones first rather than fetching all.
- **Read operations**: Only when explicitly needed, not proactively.
- **Write operations**: NEVER execute without explicit user confirmation.
- Always state: "I can make this change in Webflow, but I need your green light first. Confirm?"

## Communication Rules

- **Never speak unprompted** — Only respond when the user asks something.
- **No unsolicited suggestions** — Don't offer additional analysis or next steps unless asked.
- **Be direct** — Give the score, the issues, the draft. No fluff.

## Email Response Templates

Draft emails that are polite, constructive, and strict. See [references/email-templates.md](references/email-templates.md) for examples.

**Tone guidelines:**
- Professional but friendly
- Specific about what's wrong
- Clear about what would make it acceptable
- No passive-aggressive language

## Quick Reference

**Always ask user to verify in Ahrefs:**
- Domain Rating (DR)
- Whether target competes with article keywords

**Instant rejections:**
- Restricted category sites
- Excluded articles
- DR < 50
- Non-blog pages
