# Changelog

## branding 1.2

Aligned the `branding` plugin's description across `.claude-plugin/marketplace.json` and `branding/.claude-plugin/plugin.json` — they previously diverged (one was a skill inventory list, the other a longer value-prop paragraph). Both now use a single canonical line that matches the README's tagline. No skill or behavior changes.

- Set `description` to "The minimum on-brand kit for social.plus — brand voice, press releases, and design system. For non-marketing teammates who need to stay on-brand." in both [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) and [branding/.claude-plugin/plugin.json](branding/.claude-plugin/plugin.json).
- Bumped [branding/.claude-plugin/plugin.json](branding/.claude-plugin/plugin.json) and the branding entry in [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) from 1.1 to 1.2. Version bump is necessary for teammates' clients to re-fetch the manifest and display the new description; without it the catalog and installed-plugin views stay frozen on the old text.

## 12.0

Renamed the `marketing-team` plugin's internal name in `skills/.claude-plugin/plugin.json` from `product-marketing-team` to `marketing-team`, aligning it with `.claude-plugin/marketplace.json`. **Breaking change** — every skill's direct-invoke shortcut moves from `/product-marketing-team:<skill>` to `/marketing-team:<skill>`. Auto-trigger (the normal use path) is unaffected, and the install command (`/plugin install marketing-team@cruciate-hub`) was already using the correct name.

- Renamed `name` field in [skills/.claude-plugin/plugin.json](skills/.claude-plugin/plugin.json) from `product-marketing-team` to `marketing-team`. The skill namespace prefix follows from this field, so all 14 skills now register under `marketing-team:*`.
- Updated every internal cross-reference to the old namespace: [docs/aeo-content.md](docs/aeo-content.md) (troubleshooting row), [docs/backlink-placement-finder.md](docs/backlink-placement-finder.md), [messaging/README.md](messaging/README.md), and [skills/skills/backlink-placement-finder/SKILL.md](skills/skills/backlink-placement-finder/SKILL.md) (two occurrences).
- Teammates with auto-update on will receive this at next Claude Code startup, then need to run `/reload-plugins` (or restart) to pick up the new namespace. Anyone using direct-invoke shortcuts in scripts, prompts, or muscle memory needs to update `/product-marketing-team:*` → `/marketing-team:*`.
- Bumped [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) and [skills/.claude-plugin/plugin.json](skills/.claude-plugin/plugin.json) from 11.1 to 12.0 (semver major — namespace change is breaking). The `branding` plugin is unaffected; its skills continue to register under `branding:*`.

## 11.1

Routing taxonomy rework + press-release v10 migration. [messaging/brain.md](messaging/brain.md) now routes by what content does, not by length; [press-release](skills/skills/press-release/SKILL.md) adopts the v10 canonical fetch block (was the last skill missing it); three downstream skills updated to match the new router.

- Rewrote [messaging/brain.md](messaging/brain.md) routing table around purpose: each row now states a condition based on what the output IS or CONTAINS, and triggers one file load. Replaces the prior length-based "Short-form content" / "Long-form content" split, which miscategorised `boilerplates.md` (used in both 25-word taglines and 70-word press-release "About" blocks) and forced workarounds in case-study and press-release. Structure now mirrors [design-system/brain.md](design-system/brain.md).
- Press-release: full v10 migration. Inserted the canonical FETCH-BLOCK v2 markers ([scripts/canonical-fetch-block-v2.md](scripts/canonical-fetch-block-v2.md)) — was the last fetch-using skill missing them per audit. Replaced two `github.com/.../blob/...` URLs with `cat "$REPO/..."`. Dropped the obsolete "Important: URL format" trailing section. Reordered Step 1's messaging file list to match the new conditional rows; `boilerplates.md` now loads naturally instead of via a "Short-form content" workaround.
- Updated [blog-seo-content](skills/skills/blog-seo-content/SKILL.md), [case-study](skills/skills/case-study/SKILL.md), and [newsletters](skills/skills/newsletters/SKILL.md) to replace dead `"Long-form content"` / `"Short-form content"` category references with explicit per-row conditions. case-study drops its boilerplates workaround step; the file now loads under its own conditional row.
- Audit ([scripts/audit-skills.sh](scripts/audit-skills.sh)): 11 checked, 0 drift (was 1 drift on press-release before this revision).
- Bumped [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) and [skills/.claude-plugin/plugin.json](skills/.claude-plugin/plugin.json) from 11.0 to 11.1. Bumped [branding/.claude-plugin/plugin.json](branding/.claude-plugin/plugin.json) from 1.0 to 1.1 — branding uses press-release as a symlinked skill and inherits the v10 migration.

## 11.0

Breaking changes and structural cleanup — removed two skills, added one (press-release), reorganised per-skill docs per Anthropic's Agent Skills guide, narrowed blog-seo-content to social.plus/blog, and aligned the routing brains so every cross-reference reflects the new skill set.

- Removed the campaign-copy and social-media skills entirely — full directory deletion plus every cross-reference: [brain.md](brain.md) routing rows, anti-trigger clauses in other SKILL.md descriptions, the design-system/social-posts.md format guide that only social-media loaded, and the Typography in Social Media + Social media post imagery rows in the design system. brand-messaging is now the fallback for LinkedIn/Instagram/X posts and ad copy. Breaking change — semver major.
- Added the press-release skill ([skills/skills/press-release/](skills/skills/press-release/)) — produces newswire-ready .docx files for PR Newswire / Cision, embargoed announcements, and product/funding/partnership announcements. Added to brain.md's task-type routing table and the Available skills index. [skills/skills/press-release/INSTALL.md](skills/skills/press-release/INSTALL.md) moved to [docs/press-release.md](docs/press-release.md) to match the new doc layout.
- Restructured per-skill docs to comply with Anthropic's Agent Skills guide ("no README.md inside skill folders") — moved every per-skill README from `skills/skills/<name>/README.md` to [`docs/<name>.md`](docs/) at repo root. Merged aeo-content's USAGE.md into the README before the move as a "Getting started" section. Updated [skills/README.md](skills/README.md) to dual-link each row (skill name → `../docs/<name>.md`, trailing column → SKILL.md). Header now reads "Skills (14)" across the plugin index and the root [README.md](README.md).
- Narrowed [blog-seo-content](skills/skills/blog-seo-content/SKILL.md) to "blog posts for social.plus/blog" only — dropped thought leadership pieces, pillar pages, comparison articles, how-to guides, and external publication from its triggers and use-case lists. Cleaned five cross-references in other skill docs (aeo-content's Related skills, etc.). SKILL.md description trimmed from 1112 to 566 chars.
- Aligned the routing brains: [brain.md](brain.md) now adds a press-release task-type row and drops the stale "Social media posts" routing row and precedence rule; [messaging/brain.md](messaging/brain.md) drops the dedicated "Social media posts" section, the cross-domain file table pointing at social-posts.md, and "thought leadership" / "whitepapers" from the Long-form content section heading; [design-system/brain.md](design-system/brain.md) drops the "Social media content" routing section and the corresponding row from Available files.
- Trimmed three SKILL.md description fields that exceeded Anthropic's 1024-char limit: aeo-content (1036 → 850), blog-seo-content (1112 → 566), legal-docs-formatter (1081 → 969). Anti-trigger clauses preserved.
- Aligned both manifest `description` fields to `"Shared skills for the marketing team."` (was inconsistent — marketplace.json had a short form, plugin.json still claimed 15 skills).
- Bumped [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) and [skills/.claude-plugin/plugin.json](skills/.claude-plugin/plugin.json) from 10.3 to 11.0 (semver major — skill removal is breaking).

## 10.3

Newsletter skill consistency fixes — driven by a low-quality March 2026 product-update render that surfaced contradictions between the spec and the templates, and gaps that forced LLM guesswork.

- Module tags in [emails/product-update-newsletter-blocks.md](emails/product-update-newsletter-blocks.md) now render as coloured pill badges across Tier 2, Tier 3, and Tier 4, matching the badge pattern documented in [emails/product-update-newsletter-spec.md](emails/product-update-newsletter-spec.md). Templates now reference `{{MODULE_BG}}` and `{{MODULE_TEXT}}`.
- Added a Commerce row to the Module Color Accents table in [emails/product-update-newsletter-spec.md](emails/product-update-newsletter-spec.md) (interim values — design to confirm).
- Audited every Module Color Accents pair in [emails/product-update-newsletter-spec.md](emails/product-update-newsletter-spec.md) for WCAG 2.1 AA contrast. Six pairs (Console, UI Kit, Chat, Video, Social, Flutter) failed and have been replaced; all rows now meet ≥ 4.5:1.
- Reworked the subject-line extraction rule in [skills/skills/newsletters/SKILL.md](skills/skills/newsletters/SKILL.md) Step 4 — the old "What's New in [month year]:" pattern conflicted with the 40–50 char limit in [emails/emails.md](emails/emails.md).
- Added a new "Step 4a: Clean the source content" section to [skills/skills/newsletters/SKILL.md](skills/skills/newsletters/SKILL.md) covering emoji stripping in CTAs, Webflow CMS shortcode stripping, missing-module-tag handling for Tier 4, and the CTA URL fallback rule.
- Bumped [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) and [skills/.claude-plugin/plugin.json](skills/.claude-plugin/plugin.json) from 10.2 to 10.3.

## 10.2

Renamed `internal-linking-optimizer` → `internal-linking-strategist` — the skill covers both draft-mode link suggestions for new content AND site-wide audits (orphans, cannibalization, anchor drift), so "optimizer" only captured half of what it does.

- Renamed the skill directory to [skills/skills/internal-linking-strategist/](skills/skills/internal-linking-strategist/SKILL.md); updated `name` + `description` in SKILL.md and moved the per-skill doc to [docs/internal-linking-strategist.md](docs/internal-linking-strategist.md).
- Updated every cross-reference: [brain.md](brain.md) Available skills table, [skills/README.md](skills/README.md) SEO & linking row, root [README.md](README.md), [aeo-content/SKILL.md](skills/skills/aeo-content/SKILL.md) and its `compliance.py` mention, [blog-seo-content/SKILL.md](skills/skills/blog-seo-content/SKILL.md), and `website/link-strategy.md` (the file the skill consumes).
- Version bumped because the skill name is part of the trigger surface — restarting Cowork forces a snapshot refresh so "use the internal-linking-strategist skill" resolves correctly.
- Bumped [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) and [skills/.claude-plugin/plugin.json](skills/.claude-plugin/plugin.json) from 10.1 to 10.2.

## 10.1

Hardening on the v10.0 fetch architecture — strictly additive, surfaced by Cowork cold-tests; the git-clone + cat + sed-chunks design from v10.0 is unchanged.

- [scripts/canonical-fetch-block-v2.md](scripts/canonical-fetch-block-v2.md) now covers both harness truncation-marker formats — the `Output too large (NkB). Full output saved to: …` preview form AND the `Error: result (N characters) exceeds maximum allowed tokens` sidecar-only form. v10.0 only documented the first; an LLM hitting the second could miss the truncation signal and proceed on partial output. Re-stamped across all 12 fetch-using SKILL.md files (audit drift=0).
- Calibrated the truncation threshold empirically at ~50,000 characters of JSON-wrapped tool result (~48–55 KB raw stdout depending on token density); the 250-line `sed` chunks (~17 KB each) recommended in the canonical block keep ~3× safety margin.
- [skills/skills/aeo-content/scripts/duplicate_check.py](skills/skills/aeo-content/scripts/duplicate_check.py) now emits a dual signal — exit code AND a final stdout line: `RESULT: MATCHES` (exit 1), `RESULT: CLEAN` (exit 0), `RESULT: UNVERIFIED` (exit 2). [aeo-content/SKILL.md](skills/skills/aeo-content/SKILL.md) documents both paths and tells the calling LLM to treat any disagreement between exit code and stdout marker as UNVERIFIED.
- Bumped [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) and [skills/.claude-plugin/plugin.json](skills/.claude-plugin/plugin.json) from 10.0 to 10.1.

## 10.0

New fetch architecture — every skill that loads reference content now does a single shallow `git clone` per session into a local /tmp folder, then reads files with `cat` (or `sed` chunks for outliers) instead of fetching per-read over HTTP.

- Replaced the WebFetch + `github.com/.../blob/…` model, which returned 40–55× HTML overhead per file, occasionally tripped GitHub's anonymous abuse-detection on parallel fetches (newsletters fetches 11), and silently rewrote brand-critical strings via WebFetch's internal LLM (e.g. `social.plus` → `Social.plus`).
- Confirmed empirically that every clean-content alternative is blocked in Cowork — `raw.githubusercontent.com`, `cdn.jsdelivr.net`, `api.github.com`, and `codeload.github.com` all return 403; only `github.com` is reachable, which is what made shallow clone the answer. Reviewed by Gemini and a separate Claude session, both converged on the same recommendation.
- Added [scripts/canonical-fetch-block-v2.md](scripts/canonical-fetch-block-v2.md) as the single source of truth for the fetch instructions and [scripts/audit-skills.sh](scripts/audit-skills.sh) to enforce byte-identity across all 12 fetch-using SKILL.md files.
- One clone per session into `/tmp/cruciate-hub-marketing-team`; `cat` for files that fit, 250-line `sed` chunks when the harness's truncation marker fires, halve-and-retry if a chunk itself truncates; `python3`/`jq` for large JSON inventories. Hard-fail on any fetch error with `Fetch failed: <path>. Please check your network connection and rerun.` — no reconstruction from memory, no WebFetch fallback.
- Removed `skills/skills/aeo-content/scripts/fetch_brand.py` (the fragile HTML-parsing helper) and rewrote [duplicate_check.py](skills/skills/aeo-content/scripts/duplicate_check.py) to read directly from `$MT_REPO/website/pages-*.json` instead of fetching at runtime.
- Dropped the stale "raw is blocked" warning copy-pasted across three `brain.md` files; corrected the architecture description in 12 README files.
- Fallout from the v10.0 verification battery (test D1 — "brain.md mentions all 15 skills"): added `internal-linking-optimizer`, `legal-docs-formatter`, and `svg-icon-transformer` to [brain.md](brain.md)'s Available skills table; three skills had been added in earlier commits but never reached the master router.
- Bumped [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) and [skills/.claude-plugin/plugin.json](skills/.claude-plugin/plugin.json) from 0.9.2 to 10.0.
