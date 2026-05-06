---
name: brand-messaging
description: >
  Enforces social.plus brand messaging consistency across all written content.
  Use this skill for: marketing copy, blog posts, landing page text, press releases,
  pitch materials, website copy, product descriptions,
  investor communications, taglines, subject lines, or any text representing the
  social.plus brand. Also trigger when reviewing or auditing existing copy against
  brand guidelines, or when someone asks about brand voice, tone, approved terminology,
  messaging frameworks, value propositions, competitive positioning, or boilerplates.
  Do NOT trigger for HTML email generation (use newsletters skill) or social media
  posts (use social-media skill) — those have dedicated skills with format-specific
  instructions.
---

# social.plus Brand Messaging

This skill ensures all social.plus content aligns with official brand messaging. The source of truth lives on GitHub and must be fetched fresh every time.

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

3. Follow the messaging router's instructions — it tells you which additional files to fetch based on the user's task.

4. If the output includes any visual styling (HTML, CSS, colors, layout), also fetch `design-system/brain.md`.

5. Before delivering, run the compliance check from the main brain.
