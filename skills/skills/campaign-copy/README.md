# Campaign Copy

Claude skill for writing ad copy, campaign landing pages, and paid media content for social.plus.

Ad copy operates under extreme space constraints — every word must earn its place while still following brand terminology and positioning. This skill enforces platform character limits, the brand messaging stack, and A/B variant differentiation.

## What it does

- Fetches short-form messaging (terminology, tone, boilerplates, positioning, value-story) via the brain router.
- Produces ad copy for Google Ads (Responsive Search Ads), LinkedIn Ads, and Meta Ads with correct character counts.
- Generates A/B variants differentiated on **angle** (pain point vs. outcome vs. social proof), not just word choice.
- Drafts campaign landing pages following the narrative structure when a campaign includes a page.
- Always shows the character count next to every element so limits are visible.

## When it triggers

When the user wants paid acquisition or marketing campaign content. Trigger phrases include "write ad copy", "Google Ad", "LinkedIn Ad", "campaign landing page", "ad headline", "A/B test", "retargeting", "paid media copy", "ad creative copy", or any mention of advertising platforms or paid campaigns.

The skill is not for organic social media (use `social-media`) or general website copy (use `brand-messaging`).

## Workflow

1. Fetch `brain.md` and `messaging/brain.md`.
2. Follow **"Short-form content"** routing — loads terminology, tone, boilerplates, positioning, value-story.
3. If the campaign includes a landing page, also follow **"Long-form content"** routing for `narrative.md`.
4. If the landing page needs visual design, fetch `design-system/brain.md`.
5. Produce ad copy with character counts visible on every element.
6. Run the compliance check from `brain.md`.

## Ad copy rules

### Headlines
- Lead with the outcome or tension, not the product name.
- Use the value propositions from `value-story.md` — don't invent new claims.

### Descriptions
- One idea per ad. Don't compress the entire product story into 90 characters.
- Match the headline's promise. No bait-and-switch.
- End with a clear CTA that matches the landing page destination.

### A/B variants
- Differentiate on **angle**, not just word choice.
- Label each variant with the angle it tests (pain point / outcome / social proof).

### Landing pages
- Follow the narrative structure from `narrative.md`.
- One primary CTA per section. Never stack two gradient CTAs.
- Hero copy should resolve the headline's promise within 2 sentences.

## Platform formats

### Google Ads — Responsive Search Ads (RSA)

| Element | Max length | Count |
|---|---|---|
| Headline | 30 chars | Up to 15 (min 3) |
| Description | 90 chars | Up to 4 (min 2) |
| Display path | 15 chars each | 2 segments |

- Headlines must make sense in any combination — no headline depends on another.
- Pin headlines only when the user specifies (e.g., brand name in position 1).
- Target keyword in at least 3 headlines.
- At least 1 description includes a CTA.

### LinkedIn Ads

| Element | Max length |
|---|---|
| Introductory text | 600 chars (150 before "see more" truncation) |
| Headline | 200 chars (70 recommended) |
| Description | 100 chars |

- Front-load the hook in the first 150 chars of introductory text.
- Professional tone — audience is decision-makers, not end users.
- Headline states the outcome, not the product.

### Meta Ads (Facebook / Instagram)

| Element | Max length |
|---|---|
| Primary text | 125 chars before truncation (max 2,200) |
| Headline | 40 chars |
| Description | 30 chars |

- Primary text: lead with a hook or question — first 125 chars decide expansion.
- Headline: outcome-driven, short enough to survive mobile truncation.
- Description: supporting detail only — often hidden on mobile.

## Output formats

### Single platform ad set

```
## Google Ads RSA — [Campaign/Topic]

**Headlines:**
1. [headline — XX/30 chars]
...up to 15

**Descriptions:**
1. [description — XX/90 chars]
...up to 4

**Display path:** social.plus / [path1] / [path2]
**Pinning:** [recommendations, or "None — let Google optimize"]
```

### Multi-platform campaign

Grouped by platform with character counts on every element.

### A/B test variants

```
## A/B Test — [What's being tested]

### Variant A — [Angle: e.g., "Pain point"]
[Copy]

### Variant B — [Angle: e.g., "Outcome"]
[Copy]

### Variant C — [Angle: e.g., "Social proof"]
[Copy]

**Hypothesis:** [What each variant is testing and why]
```

### Landing page

```
## Landing Page — [Campaign/Topic]

**Hero headline:** [value]
**Hero subheadline:** [value]
**Hero CTA:** [button text] → [destination URL]

**Section 1:** [heading + body copy]
**Section 2:** [heading + body copy]
...

**Final CTA:** [button text] → [destination URL]

**Meta title:** [under 60 chars]
**Meta description:** [under 155 chars]
```

## What NOT to do

- Never fabricate performance claims ("10x engagement") unless sourced from reference files.
- Never use competitor names in ad headlines — comparison belongs on landing pages.
- Never promise "free" unless the pricing page confirms a free tier exists.
- Never exceed platform character limits. Always show the count.
- Never write an RSA headline that only makes sense paired with another specific headline.

## URL format

All reference files are loaded from a shallow clone of this repo (`git clone --depth 1`) into `$MT_REPO`. The canonical fetch block at the top of each SKILL.md handles the clone; skills then read files with `cat "$MT_REPO/<path>"`.
