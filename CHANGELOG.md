# Changelog

## 10.3

Newsletter skill consistency fixes — driven by a low-quality March 2026 product-update render that surfaced contradictions between the spec and the templates, and gaps that forced LLM guesswork.

- Module tags in [emails/product-update-newsletter-blocks.md](emails/product-update-newsletter-blocks.md) now render as coloured pill badges across Tier 2, Tier 3, and Tier 4, matching the badge pattern documented in [emails/product-update-newsletter-spec.md](emails/product-update-newsletter-spec.md). Templates now reference `{{MODULE_BG}}` and `{{MODULE_TEXT}}`.
- Added a Commerce row to the Module Color Accents table in [emails/product-update-newsletter-spec.md](emails/product-update-newsletter-spec.md) (interim values — design to confirm).
- Audited every Module Color Accents pair in [emails/product-update-newsletter-spec.md](emails/product-update-newsletter-spec.md) for WCAG 2.1 AA contrast. Six pairs (Console, UI Kit, Chat, Video, Social, Flutter) failed and have been replaced; all rows now meet ≥ 4.5:1.
- Reworked the subject-line extraction rule in [skills/skills/newsletters/SKILL.md](skills/skills/newsletters/SKILL.md) Step 4 — the old "What's New in [month year]:" pattern conflicted with the 40–50 char limit in [emails/emails.md](emails/emails.md).
- Added a new "Step 4a: Clean the source content" section to [skills/skills/newsletters/SKILL.md](skills/skills/newsletters/SKILL.md) covering emoji stripping in CTAs, Webflow CMS shortcode stripping, missing-module-tag handling for Tier 4, and the CTA URL fallback rule.
- Bumped [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) and [skills/.claude-plugin/plugin.json](skills/.claude-plugin/plugin.json) to 10.3.
