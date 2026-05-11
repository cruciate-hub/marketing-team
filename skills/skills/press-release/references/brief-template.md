# Press release brief template

This is the canonical brief format. Provide as much detail as possible — anything missing will become a clarifying question before drafting starts.

The skill drafts executive quotes (just give name + title). The skill never drafts customer or partner quotes — those must be supplied verbatim.

---

## Universal brief fields

### 1. Release type
One of:
- `product_launch` — new product / feature suite / module / GA of a beta
- `funding` — Seed / Series A–D / growth round / strategic investment
- `partnership` — strategic / integration / GTM / co-selling partnership
- `customer_win` — notable customer signs / deploys / expands
- `exec_hire` — C-suite / VP / board / advisor
- `milestone` — number-anchored news (users, revenue, geographic, anniversary)
- `award` — analyst recognition / industry award / list inclusion
- `acquisition` — buying / being bought / asset purchase

### 2. The news, in one sentence
The single sentence a journalist would write if they had only one sentence. Specific. No adjectives. No hype.

> Good: "social.plus is launching Commerce, a suite that lets brands tag products inside community posts and livestreams."
> Bad: "social.plus is launching its revolutionary new commerce capabilities."

### 3. Key facts
A bulleted dump of the specifics:
- Product / partner / customer / round / hire name(s)
- Dates: launch date, close date, start date, embargo date
- Numbers: amounts, counts, percentages, growth — with sources
- Geographies: which markets, which offices
- Names: people quoted, parties involved
- Anything that should appear in the body verbatim

### 4. Why now
What makes this newsworthy *this week*? The news hook.
- Customer or market demand that triggered this
- Category shift this connects to
- Calendar alignment (conference, fiscal year, anniversary)
- Competitive timing

### 5. Target audience + angle
- Primary audience (industry press, trade outlets, financial press, analysts, customer prospects)
- The single sentence that explains why this announcement matters to them
- Strategic context: what wider category shift does this connect to?

### 6. Executive speaker(s)
For each speaker the brief wants quoted:
- Full name
- Exact title
- (Optional) one-line guidance on what claim or position to make in the quote — but only if you want to constrain the skill. Otherwise the skill drafts based on the speaker's role and the news.

### 7. Customer or partner quote(s)
**Required for: partnerships, customer wins, funding rounds with named investor quotes.**

For each external quote:
- The full quote text (verbatim — the skill does not draft)
- Speaker full name
- Speaker exact title
- Speaker company / affiliation
- Confirmation the speaker has approved the quote for the release

### 8. Dateline
- City (e.g. `LONDON`, `NEW YORK`, `SAN FRANCISCO`)
- Date (the release date — defaults to today if omitted)

### 9. Availability or next steps
- When (now / on [date] / Q3 2026)
- How (Console, contact sales, sign-up URL)
- Where to read more (docs URL, learn.social.plus)
- For funding: use of funds (R&D, GTM, hires)
- For partnerships: integration availability
- For hires: start date, reporting line

### 10. Media contact
- Default: `marketing@social.plus | social.plus`
- Override if a different PR firm or comms lead handles inquiries

### 11. Boilerplate override (optional)
- Default: pulled from `boilerplates.md`
- Override only if the announcement introduces a new pillar the boilerplate should reflect, or if legal has requested a modified version

### 12. Embargo
- Default: `null` (FOR IMMEDIATE RELEASE)
- If embargoed: full embargo line, e.g. `UNDER EMBARGO UNTIL Tuesday, May 12, 2026, 9:00 a.m. ET`

### 13. Legal / compliance flags (optional but valuable)
- Any claim that needs legal review
- Any forward-looking statement
- Any number whose methodology must be defensible
- Any customer or partner that hasn't formally approved being named yet

---

## Brief examples by release type

### Example A — Product launch brief

```yaml
release_type: product_launch
news_in_one_sentence: |
  social.plus is launching Commerce, a suite that connects high-intent community moments to products users can act on inside the app.

key_facts:
  - Product name: Commerce
  - Three capabilities: Product Catalogue, Product Tagging in Posts, Tag and Pin Products in Livestream
  - Up to 20 items can be tagged in a livestream; one can be pinned as a live overlay
  - Available now across the social.plus platform
  - Existing customers enable via Feature Settings in the Console
  - Documentation: learn.social.plus

why_now: |
  Community platforms generate high-intent commerce signals, but most have no infrastructure to act on them. Brands are increasingly investing in owned community and need conversion attached.

target_audience: |
  B2B tech press (TechCrunch, The Information), retail tech trades (Retail Dive, Modern Retail), and analyst community covering community platforms and shoppable commerce.

angle: |
  social.plus is closing the loop between community engagement and commerce, eliminating the off-platform handoff that costs brands attribution and conversion.

speakers:
  - name: Amadeus Norén
    title: VP of Marketing
    # No quote guidance — the skill drafts based on role + news

customer_partner_quotes: []  # No customer quote provided for this launch

dateline:
  city: LONDON
  date: April 29, 2026

availability: |
  Available now. Existing customers enable via Console > Feature Settings. New customers contact social.plus sales at social.plus/contact/contact-sales. Documentation at learn.social.plus.

media_contact: marketing@social.plus | social.plus

embargo: null

legal_flags: []
```

### Example B — Funding round brief

```yaml
release_type: funding
news_in_one_sentence: |
  social.plus has raised $30M in Series B funding led by Index Ventures to expand its community infrastructure platform globally.

key_facts:
  - Round: Series B
  - Amount: $30M
  - Lead investor: Index Ventures
  - Participating investors: Sequoia, EQT Ventures, Octopus Ventures
  - Total funding to date: $52M
  - New board member: Sarah Cannon (Index Ventures)
  - Close date: May 8, 2026

use_of_funds:
  - R&D: deepening Commerce capabilities; expanding into AI-driven moderation
  - GTM: opening Singapore office; scaling EMEA team
  - Hires: VP Engineering (London), Head of APAC GTM (Singapore), 20+ engineering roles

why_now: |
  Brands are accelerating investment in owned community as third-party social platforms become less reliable for engagement. The Commerce launch in April demonstrated demand; this round funds the build-out.

target_audience: |
  Financial press (TechCrunch, Sifted, PitchBook), community-platform analysts, and senior buyers at brand customers.

angle: |
  Owned community is the next infrastructure category. social.plus is the layer underneath.

speakers:
  - name: [CEO name]
    title: CEO and Founder
  - name: Sarah Cannon
    title: Partner, Index Ventures

customer_partner_quotes:
  - text: "We've watched social.plus build the most thoughtful infrastructure for community we've seen. ..."  # verbatim from Sarah, approved
    speaker_name: Sarah Cannon
    speaker_title: Partner
    speaker_affiliation: Index Ventures
    approval_status: approved via email 2026-05-07

dateline:
  city: LONDON
  date: May 12, 2026

embargo:
  until: Tuesday, May 12, 2026, 6:00 a.m. ET

media_contact: marketing@social.plus | social.plus

legal_flags:
  - Valuation: do NOT disclose ($X discussed informally; not for the release)
  - Total funding to date number ($52M) confirmed by finance team
```

### Example C — Customer win brief

```yaml
release_type: customer_win
news_in_one_sentence: |
  Smart Fit, the largest fitness chain in Latin America, has built its in-app community on social.plus, reaching 1.5M active members in six months.

key_facts:
  - Customer: Smart Fit
  - Customer descriptor: largest fitness chain in Latin America, 4,400+ locations across 15 countries
  - Outcome: 1.5M active community members in 6 months
  - Engagement: 60% month-over-month growth in community activity
  - Features used: activity feed, group chat, livestream
  - Customer approved being named: Yes — written confirmation from Smart Fit Head of Digital 2026-04-15

why_now: |
  Smart Fit completed its first full quarter on social.plus and the engagement data is now publicly shareable. Aligns with fitness industry's annual digital strategy review cycle.

target_audience: |
  Fitness industry trade press, Latin American tech press, and prospective fitness/health customers evaluating community platforms.

angle: |
  Fitness brands need community to retain members. Smart Fit built theirs in 6 months on owned infrastructure.

speakers:
  - name: [CEO name]
    title: CEO and Founder
    quote_guidance: Validate the category (fitness as a community-led category) — do not claim credit for Smart Fit's success

customer_partner_quotes:
  - text: "We knew our community had to live inside our app, not on someone else's platform. ..."  # verbatim, approved
    speaker_name: [Customer exec name]
    speaker_title: Head of Digital
    speaker_affiliation: Smart Fit
    approval_status: approved via email 2026-04-15

dateline:
  city: SÃO PAULO
  date: May 15, 2026

media_contact: marketing@social.plus | social.plus

legal_flags:
  - 1.5M member number and 60% engagement growth confirmed in writing by Smart Fit
```

### Example D — Executive hire brief

```yaml
release_type: exec_hire
news_in_one_sentence: |
  social.plus has hired Maria González as Chief Technology Officer to lead its global engineering organisation.

key_facts:
  - Name: Maria González
  - Title: Chief Technology Officer
  - Start date: June 1, 2026
  - Reporting to: CEO
  - Previous role: VP of Engineering at Twilio (5 years)
  - Prior roles: Engineering lead at Stripe (3 years); ML engineer at Google
  - Education: MS Computer Science, Stanford

why_now: |
  social.plus has 80+ engineers and is expanding into APAC. CTO role is a new addition — previously engineering reported to CEO.

target_audience: |
  Tech press, engineering recruiting community, and existing engineering team (internal credibility).

angle: |
  social.plus is investing in technical leadership to scale its community infrastructure platform into a developer-first product category.

speakers:
  - name: Maria González
    title: Chief Technology Officer
    quote_guidance: |
      Speaks to what becomes possible technically — not gratitude for the opportunity.
      May reference Twilio experience scaling communication infrastructure.
  - name: [CEO name]
    title: CEO and Founder
    quote_guidance: |
      Explains why this hire, what Maria will own, what becomes possible with her on the team.

customer_partner_quotes: []  # Not used for hire announcements

dateline:
  city: LONDON
  date: May 20, 2026

media_contact: marketing@social.plus | social.plus

legal_flags: []
```

---

## Common brief mistakes (heads-up)

- **Vague numbers.** "Significant growth" is not a number. Provide the actual figure or skip the claim.
- **Unnamed customers.** "A leading global retailer" — if they can't be named, this isn't a customer release.
- **Fabricated quotes.** Customer/partner quotes must be verbatim and approved. The skill will refuse to invent them.
- **Two news events in one brief.** "We raised $30M AND launched a new product" — split into two releases.
- **No "why now".** A release without a news hook becomes filler. Define why this matters this week.
- **Vague availability.** "Coming soon" — give a date, month, or quarter, or hold the release.
- **Missing legal flags.** If a number is uncomfortable, a customer hasn't fully approved, or a forward-looking statement is involved, flag it.

When in doubt, over-share in the brief. The skill prefers too much detail (it will be selective) over too little (it will have to ask).
