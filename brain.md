# social.plus — Main Brain

**social.plus** is an in-app community infrastructure platform. It lets digital products embed social experiences (feeds, chats, groups, events) directly inside their apps — so companies own engagement without building from scratch or depending on external social networks.

This is the master router for all social.plus marketing content. Every skill fetches this file alongside its domain-specific router to get cross-domain awareness, precedence rules, and the compliance check.

All reference files are hosted at:
`https://github.com/socialplus-tools/marketing-team/blob/main/`

**Warning:** Always use `github.com/.../blob/...` URLs when fetching. Never convert to `raw.githubusercontent.com` or `api.github.com` — both are blocked by network egress restrictions and will fail.

## Cross-domain routing

Most tasks need references from more than one domain. Use this table to determine which routers to fetch:

| Task type | Fetch these routers |
|---|---|
| Written content (articles, blog posts, scripts, copy) | `messaging/brain.md` |
| Visual output (HTML, CSS, components, decks, emails) | `messaging/brain.md` + `design-system/brain.md` |
| Social media posts | `messaging/brain.md` + `design-system/brain.md` — brain.md routes to `social-posts.md` for platform specs |
| HTML emails / newsletters | `messaging/brain.md` (for terminology + tone) + `design-system/brain.md` (for colors + typography) |
| UI copy (buttons, errors, tooltips, empty states) | `messaging/brain.md` — brain.md routes to `ui-micro-copy.md` |
| Website audit or content analysis | `website/site-content.json` + `messaging/brain.md` |
| Competitive content (comparisons, differentiators) | `messaging/brain.md` — ensure both `positioning.md` and `value-story.md` are loaded |

If your skill's SKILL.md already specifies which domain router to fetch, follow that. Use this table to decide whether you also need the *other* domain router.

## Precedence rules

When two reference files give guidance on the same topic, the more specific file wins:

- **UI copy tasks:** `ui-micro-copy.md` overrides `tone.md` for voice, style, and capitalisation.
- **Social media tasks:** `social-posts.md` overrides `tone.md` for platform-specific tone, format, and structure.
- **Email tasks:** `emails/emails.md` overrides `tone.md` for email-specific structure, subject lines, and CTAs.
- **Design tokens always win.** If `colors-palette.md` or `colors-usage.md` specifies a hex value, use it exactly — never approximate or substitute.
- **Terminology is always law.** `terminology.md` is never overridden by any file. Approved terms and forbidden terms apply everywhere, in every context, no exceptions.

## Compliance check

Before delivering ANY content to the user, run this check:

1. **Terminology.** Re-read `terminology.md` (you already fetched it). Scan your output for forbidden terms. Common violations: "social network", "forum", "chat tool", "plug and play" (forbidden outside dev docs), growth guarantees.
2. **Tone.** Compare your output against `tone.md`. Does it sound like the social.plus brand — or like default Claude? If you can't tell the difference, it's default Claude. Rewrite.
3. **Claims.** You did not invent any statistics, customer names, quotes, features, or performance claims. If it's not in the fetched reference files, don't state it as fact.
4. **Design tokens.** If your output includes visual styling (CSS, HTML, color references), confirm every value matches the design system files exactly. No eyeballing.
5. **Precedence.** If you loaded multiple files that cover the same topic, confirm you followed the precedence rules above.

If any check fails, fix the output before delivering. Do not flag the issue and deliver anyway — fix it.
