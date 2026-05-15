---
name: design-system
description: >
  Reference for the social.plus design system — colors, typography, spacing, buttons,
  inputs, layout, shadows, icons, imagery, accessibility, and logo usage.
  Use this skill for: writing CSS, styling components, building Webflow elements,
  creating HTML mockups, designing visual layouts, or any output where visual accuracy
  matters for social.plus. Also trigger when someone asks about brand colors, the
  color palette, button states, dark mode colors, design tokens, spacing, border
  radius, typography, or layout. Trigger even for quick questions like "what blue
  do we use" or "what's the hover color for buttons."
  Do NOT trigger for written content only (use brand-messaging skill) — this skill
  is for visual output and design token reference.
---

# social.plus Design System

This skill provides the full social.plus design system reference. The source of truth lives on GitHub and must be fetched fresh every time.

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

## What to do

1. Fetch `brain.md` for cross-domain routing, precedence rules, and the compliance check.

2. Fetch `design-system/brain.md` (the design system router).

3. Follow the design system router's instructions — it tells you which additional files to fetch based on the user's task.

4. If the output includes any text content (headings, labels, CTAs, descriptions), also fetch `messaging/brain.md`.

5. Before delivering, run the compliance check from the main brain.
