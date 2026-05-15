---
name: press-release
description: >
  Write newswire-ready press releases for social.plus. Use this skill for: press releases,
  newswire releases, PR Newswire / Cision releases, embargoed announcements, product launch
  press releases, funding announcement press releases, partnership press releases, customer
  win press releases, executive hire press releases, milestone press releases, award press
  releases, acquisition press releases, or any formal media announcement intended for
  distribution through a newswire. Trigger on phrases like "press release", "newswire",
  "PR Newswire", "Cision", "embargoed announcement", "press announcement", "media release",
  "draft a release for", "write a release about", or "announcement for the wire". This skill
  always outputs a properly formatted Word document (.docx) ready to upload to a newswire
  portal. Do NOT trigger for blog posts (use blog-seo-content), email campaigns (use
  newsletters), or customer case studies (use case-study).
---

# social.plus Press Release Generator

This skill produces newswire-ready press releases at the standard of a world-class B2B tech PR firm. Every output is a fully formatted `.docx` that can be uploaded directly to PR Newswire (Cision) or any major newswire, and is format-agnostic enough to also work for direct media pitches and the social.plus newsroom.

**Two non-negotiables:**

1. **Consistency.** Every release follows the same structural skeleton: FOR IMMEDIATE RELEASE → headline → subhead → dateline lede → narrative body → executive quote → product/proof detail → customer or partner quote → industry framing → availability → boilerplate → media contact → end marker.
2. **Conviction over excitement.** The release earns attention through specificity, not adjectives. Hyperbole, throat-clearing ("is pleased to announce"), and quote-as-summary are banned. See `references/anti-patterns.md`.

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

The Bash tool truncates large stdout when the output exceeds the harness's token/byte cap (observed at ~50 KB in Cowork; varies by environment). When this happens the harness emits one of these signals — both mean the same thing:
- `Output too large (NkB). Full output saved to: …` followed by a short preview, OR
- `Error: result (N characters) exceeds maximum allowed tokens` with no preview, just a sidecar-file pointer.

In either case, the rest of the file is invisible to you in-call. Most files in this repo are small enough that `cat` returns them in full and you never see either signal. **If you do see either form, never proceed using the partial output as if it were the whole file** — switch to one of the patterns below.

- **Truncated markdown** (you saw either truncation signal above) — read in line-range chunks instead. First check the total line count: `wc -l "$REPO/<path>"`. Then read each chunk:

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

## Step 0 — Read the main brain

Read the cross-domain routing, precedence rules, and the compliance check you must run before delivering:

```
cat "$REPO/brain.md"
```

## Step 1 — Read the messaging router and load brand-messaging references

Read the messaging router:

```
cat "$REPO/messaging/brain.md"
```

Press releases trigger every conditional row in the router except UI. Load each file with `cat "$REPO/messaging/<file>"`:

- `terminology.md` and `tone.md` — voice, capitalization, banned/preferred terms (always-load)
- `positioning.md` — product pillars used for category framing
- `value-story.md` — value creation model (functional → strategic → economic → compounding)
- `narrative.md` — messaging hierarchy and 5-step narrative structure
- `boilerplates.md` — approved company description for the "About social.plus" block (Block 15)

Press releases are public, permanent, and indexed. Terminology and tone compliance are mandatory.

## Step 2 — Load press-release-specific references

Read these from this skill folder in order:

1. `references/structure-template.md` — the exact skeleton with placeholders and word-count guidance for each block
2. `references/release-type-playbooks.md` — release-type-specific lede formulas (product launch, funding, partnership, customer win, exec hire, milestone, award, acquisition)
3. `references/brief-template.md` — canonical brief shape and worked examples by release type
4. `references/quote-engineering.md` — the four-rule quote test, exec quote drafting patterns, customer/partner quote handling
5. `references/anti-patterns.md` — banned words and phrases, structural anti-patterns, mandatory self-review checklist
6. `references/best-in-class-corpus.md` — distilled patterns from Stripe, Datadog, Snowflake, MongoDB, Cloudflare, HashiCorp, Atlassian
7. `examples/commerce-launch.md` — gold-standard social.plus release. Study tone, paragraph length, quote style, subhead phrasing.

Load these into context. They are not optional — they are the difference between a competent release and a publishable one.

## Step 3 — Intake and validate the brief

Every press release starts with a brief. The brief must contain three required fields. If any is missing or thin, use AskUserQuestion to fill the gap **before drafting**.

### Required brief fields

**A. Announcement + key facts**
- What is being announced (product, feature, deal, hire, metric)?
- Release type (product launch / funding / partnership / customer win / exec hire / milestone / award / acquisition)
- Key facts: numbers, dates, names, geographies, the specific "thing"
- Why now (the news hook — what makes this newsworthy this week)

**B. Target audience + angle**
- Who is this release for (industry press, trade outlets, financial press, customer prospects, analysts)?
- The angle (the single sentence that captures why this matters to them)
- Strategic context (what category / industry shift this connects to)

**C. Customer or partner quote(s)**
- Direct quote text (must be exact — never paraphrase a customer)
- Speaker full name, job title, company

### Brief fields the skill provides

- **Executive quote** — Brief gives speaker name + title only. The skill drafts the quote following `references/quote-engineering.md`.
- **Dateline** — Defaults to `LONDON, [today's date]` unless brief specifies otherwise.
- **Boilerplate** — Defaults to the approved version from `boilerplates.md`. The brief may override.
- **Media contact** — Defaults to `marketing@social.plus | social.plus` unless brief specifies otherwise.

### Brief intake — what to do if fields are missing

If the brief omits any required field, use AskUserQuestion to ask for it. Do not invent facts, customers, quotes, numbers, or dates. If the user provides a vague answer, ask one focused follow-up before drafting.

### Brief intake — what to do if the brief is rich

Acknowledge the inputs you have, ask only what is missing or unclear, and proceed.

## Step 4 — Determine the release type and pick the lede formula

Use `references/release-type-playbooks.md` to identify the release type and apply the matching lede formula. The lede must answer Who / What / When / Where in 30 words or fewer, with Why in the next sentence.

## Step 5 — Draft the release

Follow the skeleton in `references/structure-template.md` exactly. Apply these voice rules from `tone.md` plus these PR-specific rules:

- The lede is one paragraph. Plain English. No adjectives in the verb slot ("today launched" — not "today proudly announced").
- The second paragraph adds context, not features.
- One section subhead per major narrative beat. Subheads are sentence case, declarative, and contain a verb or implied verb.
- Executive quote: one tight paragraph. Two sentences max. Follows the four-rule test in `quote-engineering.md`.
- Customer/partner quote: appears after the product detail, before the industry framing.
- Numbers are specific. "Millions of times each day" is acceptable when the brief asserts it. Made-up precision ("47%") is not.
- The "About social.plus" boilerplate is verbatim from `boilerplates.md` unless overridden in the brief.
- The release ends with the media contact block, then `###` on a new line (newswire convention for end-of-release).

## Step 6 — Self-review against the anti-patterns checklist

Before generating the .docx, run the full checklist in `references/anti-patterns.md`. Specifically verify:

- No banned phrases ("is excited to announce", "is pleased to announce", "industry-leading", "best-in-class", "robust", "synergy", "revolutionary", "game-changing", "world-class", "cutting-edge", "next-generation", "seamless", "leverage")
- No buried lede (the news appears in the first sentence — not the second paragraph)
- No quote-as-summary (the quote cannot just restate the lede)
- No passive voice in the lede ("was launched by" — make it "social.plus launched")
- No throat-clearing intros ("In today's fast-paced digital landscape...")
- No empty superlatives without proof
- AP style compliance: dates ("April 29, 2026" — not "29 April 2026"), numbers under 10 spelled out except in datelines and metrics, no Oxford comma in headlines, percent symbol ok in body
- Subhead style matches example: sentence-case, declarative, scannable
- Total word count is 400–800 words for product/partnership/milestone releases; 300–500 for hires and awards; up to 900 for funding

If any check fails, fix and re-review.

## Step 7 — Generate the .docx

Run the docx generator script located at `scripts/generate_press_release.py` inside this skill folder. It takes a JSON payload (shape documented at the top of the script) and produces a clean Word document.

Resolve the script path relative to the skill folder. In Cowork sessions, plugins typically mount under `/sessions/<slug>/mnt/.remote-plugins/<plugin_id>/skills/press-release/scripts/generate_press_release.py`. The agent should locate this file dynamically — do not hard-code an absolute path.

Workflow:

1. Write the structured release content to a JSON payload file in the outputs directory (e.g. `release_payload.json`)
2. Run the script:
   ```bash
   python3 <skill_dir>/scripts/generate_press_release.py \
     --input <outputs_dir>/release_payload.json \
     --output <outputs_dir>/press-release-<short-slug>-<YYYY-MM-DD>.docx
   ```
3. Filename convention for the output: `press-release-<short-slug>-<YYYY-MM-DD>.docx` where slug is a kebab-case 2–3 word summary (e.g. `press-release-commerce-launch-2026-04-29.docx`).

The script handles all formatting: header line, headline (18pt bold), subhead (12pt italic grey), bold dateline + plain-text lede in one paragraph, body paragraphs, section subheads (12pt bold), lead-phrase-bolded detail paragraphs, indented quote blocks with curly quotes and italic attribution, boilerplate(s), media contact, and the centered `###` end marker.

If running `python3 -c "import docx"` errors, install python-docx with `pip install --break-system-packages python-docx`.

## Step 8 — Run the compliance check and deliver

Run the compliance check from `brain.md`. Pay special attention to:

- Terminology violations (these live on the wire indefinitely)
- Tone drift in the executive quote
- Any unverifiable claim about market position or industry size

Deliver the .docx with a `computer://` link. Include in the message:

1. The link to the .docx
2. A one-line summary of the release angle
3. The recommended embargo posture (under embargo until X / for immediate release)
4. Any flags: missing data, claims that need legal review, customer/partner quote that should be confirmed in writing before distribution

## What this skill never does

- **Never fabricates quotes** from real people. Executive quotes are drafted in the voice of a named speaker for their review and approval. Customer/partner quotes must be supplied verbatim in the brief.
- **Never invents metrics, dollar amounts, customer counts, or growth percentages.** If the brief asks for a "big number" without giving one, ask.
- **Never names a customer or partner** unless the brief explicitly authorizes naming them.
- **Never includes forward-looking financial guidance** without explicit instruction (this triggers regulatory issues even for private companies in some jurisdictions).
- **Never publishes without human review.** Output is always a draft for review by Marketing/PR and the named executive speaker.
