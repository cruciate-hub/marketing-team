---
name: campaign-copy
description: >
  Write ad copy, campaign landing pages, and paid media content for social.plus.
  Use this skill for: Google Ads copy, LinkedIn Ads, Meta Ads, display ad copy,
  retargeting copy, landing page hero sections, campaign landing pages, A/B test
  variants, ad headlines, ad descriptions, call-to-action copy for paid campaigns,
  or any content tied to a paid acquisition or marketing campaign.
  Trigger on phrases like "write ad copy", "Google Ad", "LinkedIn Ad", "campaign
  landing page", "ad headline", "A/B test", "retargeting", "paid media copy",
  "ad creative copy", or when the user mentions advertising platforms or paid campaigns.
  Do NOT trigger for organic social media (use social-media skill) or general website
  copy (use brand-messaging skill).
---

# social.plus Campaign & Ad Copy (BETA/v1, needs optimization)

This skill produces high-converting ad copy and campaign landing page content for social.plus. Ad copy operates under extreme space constraints, so every word must earn its place — while still following brand terminology and positioning.

## How to fetch reference files

<!-- FETCH-BLOCK:START v1 -->
Fetch reference files ONLY with `curl` from `raw.githubusercontent.com`, using these exact flags:

    curl -fsSL --max-time 30 --connect-timeout 10 --retry 2 --retry-delay 1 \
      https://raw.githubusercontent.com/cruciate-hub/marketing-team/main/<path>

The repo is public — no authentication required. When fetching multiple files in one step, run the curl commands in parallel (single Bash message, multiple commands) — do not serialise.

Validate every response before using it:
- Markdown files must start with `#` (a leading heading line)
- JSON files must start with `{` or `[`
- HTML files must start with `<`
- Content must be non-empty

If any fetch fails (non-zero exit, empty output, or content that fails the above check):
- Do NOT reconstruct the file from memory or training data.
- Do NOT fall back to WebFetch or any other tool.
- Stop immediately and respond with exactly this line:

  `Fetch failed: <path>. Please check your network connection and rerun.`
<!-- FETCH-BLOCK:END v1 -->

## What to do

1. Fetch `brain.md` for cross-domain routing, precedence rules, and the compliance check.

2. Fetch `messaging/brain.md` (the messaging router).

3. Follow the messaging router's **"Short-form content"** routing. This loads:
   - `terminology.md` + `tone.md` (always)
   - `boilerplates.md` (elevator pitches — useful as ad copy starting points)
   - `positioning.md` (product pillars for framing)
   - `value-story.md` (differentiation framework, core problems — essential for ad copy)

4. If the campaign includes a landing page, also follow **"Long-form content"** routing for:
   - `narrative.md` (messaging hierarchy for page structure)

5. If the landing page needs visual design, also fetch `design-system/brain.md`.

## Ad copy guidelines

### Headlines
- Lead with the outcome or tension, not the product name.
- "Your users leave apps without community" > "social.plus adds community features"
- Use the value propositions from `value-story.md` — don't invent new claims.

### Descriptions
- One idea per ad. Don't compress the entire product story into 90 characters.
- Match the headline's promise — don't bait-and-switch.
- End with a clear CTA that matches the landing page destination.

### A/B variants
- When asked for variants, differentiate on **angle** (pain point vs. outcome vs. social proof), not just word choice.
- Label each variant with the angle it tests.

### Landing pages
- Follow the narrative structure from `narrative.md` for page flow.
- One primary CTA per section. Never stack two gradient CTAs.
- Hero copy should resolve the headline's promise within 2 sentences.

## Platform-specific formats

### Google Ads — Responsive Search Ads (RSA)

RSAs allow up to 15 headlines and 4 descriptions. Google dynamically tests combinations.

| Element | Max length | Count |
|---|---|---|
| Headline | 30 chars | Up to 15 (min 3) |
| Description | 90 chars | Up to 4 (min 2) |
| Display path | 15 chars each | 2 segments |

**Rules:**
- Headlines must make sense in any combination — no headline should depend on another.
- Pin headlines to positions only when specified by the user (e.g., brand name in position 1).
- Include the target keyword in at least 3 headlines.
- At least 1 description should include a CTA.
- Provide display path suggestions (e.g., `/community` `/sdk`).

### LinkedIn Ads

| Element | Max length |
|---|---|
| Introductory text | 600 chars (150 before truncation) |
| Headline | 200 chars (70 recommended) |
| Description | 100 chars |

**Rules:**
- Front-load the hook in the first 150 chars of introductory text (before "see more").
- Professional tone — LinkedIn audience is decision-makers, not end users.
- Headline should state the outcome, not the product.

### Meta Ads (Facebook/Instagram)

| Element | Max length |
|---|---|
| Primary text | 125 chars before truncation (max 2,200) |
| Headline | 40 chars |
| Description | 30 chars |

**Rules:**
- Primary text: lead with a hook or question. The first 125 chars determine whether users expand.
- Headline: outcome-driven. Short enough that it doesn't truncate on mobile.
- Description: supporting detail — often hidden on mobile, so don't put critical info here.

## Output formats

### Single platform ad set

```
## Google Ads RSA — [Campaign/Topic]

**Headlines:**
1. [headline — XX/30 chars]
2. [headline — XX/30 chars]
...up to 15

**Descriptions:**
1. [description — XX/90 chars]
2. [description — XX/90 chars]
...up to 4

**Display path:** social.plus / [path1] / [path2]
**Pinning:** [any pinning recommendations, or "None — let Google optimize"]
```

### Multi-platform campaign

```
## [Campaign Name] — Ad Copy

### Google Ads RSA
**Headlines:** [numbered list with char counts]
**Descriptions:** [numbered list with char counts]

### LinkedIn Ads
**Introductory text:** [copy — XX/600 chars]
**Headline:** [copy — XX/200 chars]
**Description:** [copy — XX/100 chars]

### Meta Ads
**Primary text:** [copy — XX/125 chars visible]
**Headline:** [copy — XX/40 chars]
**Description:** [copy — XX/30 chars]
```

### A/B test variants

```
## A/B Test — [What's being tested]

### Variant A — [Angle: e.g., "Pain point"]
[Copy for the variant]

### Variant B — [Angle: e.g., "Outcome"]
[Copy for the variant]

### Variant C — [Angle: e.g., "Social proof"]
[Copy for the variant]

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
- Never use competitor names in ad headlines — comparison belongs in landing page body.
- Never promise "free" unless the pricing page confirms a free tier exists.
- Never exceed platform character limits. Always show the character count next to each element.
- Never write a headline that only makes sense when paired with a specific other headline (RSA rule).

## Before delivering

Run the compliance check from `brain.md`. Ad copy is high-spend content — a terminology violation wastes budget and confuses prospects.

