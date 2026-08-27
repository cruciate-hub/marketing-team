---
name: link-building-vetter
description: Vet incoming link building requests for social.plus ABC link exchanges, and govern the exchange program's overall exposure (volume caps, wind-down decisions). Use when reviewing backlink proposals, evaluating anchor text, checking article eligibility, scoring text modifications for contextual relevance and writing style, drafting response emails to link building partners, or answering program-governance questions. Triggers on phrases like "review this link request", "check this backlink proposal", "vet this anchor", "is this article eligible", "score this modification", "draft a response to this partner", "exchange volume", "wind down the link exchanges", or "re-home partner links". Do NOT use for outbound prospecting on partner sites (finding where social.plus can be linked FROM a partner's articles) — use backlink-placement-finder for that.
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

**BLOCK conditions — automatic rejection regardless of average score.** The average is advisory; any single BLOCK condition vetoes the request outright. A 9-average must not sail past one disqualifier:

- Restricted category (see list below)
- Article is on the excluded list ([references/excluded-articles.md](references/excluded-articles.md))
- Article is a Tier-1/money-page article
- DR < 50
- The social.plus article already carries one exchange-placed outbound link
- Target page competes with the article's keywords
- Branded or competitor-keyword anchor

When a BLOCK fires, the rejection email states the reason category politely ("this article isn't available for placements", "the target page overlaps with our article's topic") without exposing internal analysis, scores, or lists.

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

**Tier-1 rule (standing):** Tier-1 money posts are permanently ineligible for ABC exchanges. [references/excluded-articles.md](references/excluded-articles.md) is the enforcement list and must carry the current Tier-1 set. If a request touches a high-value post that is absent from that list, stop and surface it to Stefan rather than assuming eligibility — an omission from the list is a gap to fix, not an approval.

## Program-level Exposure and Volume Caps

Google's link-spam policy explicitly names "excessive link exchanges" as spam. This program is the single biggest residual penalty exposure for social.plus, and it stays defensible only while it is small and genuinely editorial. Volume is a policy risk, not a growth lever.

- **Hard cap: 1 exchange-placed outbound link per social.plus article, ever.** A second request on the same article is a BLOCK, regardless of quality.
- **Aggregate reporting:** With each approval batch, report to Stefan a running aggregate of live exchange-placed outbound links across the site. Label each figure **Measured** (from inventory or Ahrefs data) or **Estimated** — never present an estimate as a measurement.
- **Shrink, not grow:** The default posture is net reduction. When exchange links are removed from Tier-1 posts, re-homing onto other posts requires a net reduction in total exchange links — never 1:1 re-insertion.
- **Quarter-over-quarter check:** If aggregate exchange density rises quarter over quarter, stop approvals and flag it to Stefan as a policy-exposure decision, not a throughput question.

## Webflow MCP Safety

If Webflow MCP is connected:
- **Minimize API calls**: Webflow MCP credits are limited. Only fetch what's strictly necessary.
- **Batch requests**: If multiple articles need checking, ask user which ones first rather than fetching all.
- **Read operations**: Only when explicitly needed, not proactively.
- **Write operations**: NEVER execute without explicit user confirmation.
- Always state: "I can make this change in Webflow, but I need your green light first. Confirm?"

## Gmail Draft Safety

**Never write a bare domain (e.g. `fatjoe.com`) as plain text in a draft body.** Gmail auto-linkifies bare domain-like strings, and the resulting link gets wrapped in a `google.com/url?q=...` redirect whose visible anchor text is often the full wrapped URL instead of the domain: producing garbled, unprofessional text like `https://www.google.com/url?q=http://fatjoe.com&source=gmail&ust=...` in the sent email.

When a draft needs to reference a competitor/partner domain:
- Prefer not naming the raw domain at all: describe it instead ("the existing outbound link in that sentence", "their current backlink guide").
- If the domain must appear, de-linkify it: `fatjoe[.]com` or `fatjoe dot com`.
- Never paste a domain immediately followed by `.com`/`.io`/etc. with no separator into a `create_draft` body: that pattern is what triggers the autolink.

Before calling `create_draft`, scan the composed body for bare domain patterns and fix them.

## Communication Rules

- **Never speak unprompted**: Only respond when the user asks something.
- **No unsolicited suggestions**: Don't offer additional analysis or next steps unless asked.
- **Be direct**: Give the score, the issues, the draft. No fluff.

## Email Response Templates

Draft emails that are polite, constructive, and strict. See [references/email-templates.md](references/email-templates.md) for examples.

**Tone guidelines:**
- Professional but friendly
- Specific about what's wrong
- Clear about what would make it acceptable
- No passive-aggressive language

## Draft Formatting Rules (non-negotiable)

Drafts get pasted straight into LinkedIn or an email client, so they must survive the paste intact.

- **Never hard-wrap.** Write each paragraph as one single unbroken line, however long it runs. Do not break lines at 60, 70 or 80 characters to make the terminal look tidy. Those breaks become ragged mid-sentence enters in LinkedIn and Gmail.
- **Exactly one blank line between paragraphs.** Never two.
- **Never use em-dashes (—) or en-dashes (–).** Not in drafts, not in the analysis around them. Use a comma, a colon, or two sentences instead.
- **3-5 short paragraphs total:** greeting, verdict, reason, next step, sign-off.
- **Avoid bullet lists in drafts.** Prose reads better in a DM. Only use bullets for 3+ genuinely separate issues, and keep each bullet on one line.

Before handing a draft to the user, reread it and confirm: no mid-sentence line breaks, no double blank lines, no dashes.

## Quick Reference

**Always ask user to verify in Ahrefs:**
- Domain Rating (DR)
- Whether target competes with article keywords

**Instant rejections (BLOCK):**
- Restricted category sites
- Excluded articles
- Tier-1/money-page articles
- DR < 50
- Non-blog pages
- Article already carries an exchange-placed outbound link
- Target page competes with article keywords
- Branded or competitor-keyword anchors
