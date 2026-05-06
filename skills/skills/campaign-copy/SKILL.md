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

<!-- FETCH-BLOCK:START v2 -->
Reference files live in the public `cruciate-hub/marketing-team` GitHub repo. Fetch them by shallow-cloning the repo once per session, then loading individual files with `cat`. Use this exact pattern at the start of every skill that needs reference files:

    REPO="${MT_REPO:-/tmp/cruciate-hub-marketing-team}"
    if [ ! -d "$REPO/.git" ]; then
      git clone --depth 1 --quiet https://github.com/cruciate-hub/marketing-team.git "$REPO"
    else
      git -C "$REPO" pull --ff-only --quiet
    fi

After the clone exists, read files with `cat "$REPO/<path>"`. Examples: `cat "$REPO/brain.md"`, `cat "$REPO/messaging/terminology.md"`.

The Bash tool truncates large stdout to a small preview when the output exceeds the harness's display cap (the exact size varies by environment — observed in the 20–50 KB range). When that happens you'll see a marker like `Output too large (NkB). Full output saved to: …` followed by a short preview, and the rest is invisible to you in-call. Most files in this repo are small enough that `cat` returns them in full and you never see the marker. **If you do see the marker, never proceed using the preview as if it were the whole file** — switch to one of the patterns below.

- **Truncated markdown** — read in line-range chunks instead. First check the total line count: `wc -l "$REPO/<path>"`. Then read each chunk:

      sed -n '1,250p'     "$REPO/<path>"
      sed -n '251,500p'   "$REPO/<path>"
      sed -n '501,$p'     "$REPO/<path>"

  Each ~250-line chunk fits under the preview cap. Concatenate the chunks mentally. For files much larger than 750 lines, add more chunks at 250-line intervals until you reach the total.

  **If a chunk itself comes back as a truncated preview** (output above the harness's display cap — visible as an "Output too large" or similar marker, with the rest spilled to a file you can't see in-call), halve the chunk size and retry. For example, swap `sed -n '1,250p'` for `sed -n '1,125p'` then `sed -n '126,250p'`. Repeat until each chunk lands in full. Never proceed using a truncated chunk as if it were complete.

- **Large JSON inventories** (`website/pages-*.json`, up to 228 KB) — never `cat` raw. Process with `python3` or `jq` and emit only the fields you need:

      python3 -c "import json; d=json.load(open('$REPO/website/pages-blog.json')); print(len(d['pages']))"
      jq '.pages[].url' "$REPO/website/pages-blog.json"

  Skill helper scripts (e.g. `scripts/duplicate_check.py`) already follow this pattern.

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

