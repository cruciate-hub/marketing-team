# Project conventions

## Commit attribution

When committing on behalf of this user, use the generic co-author line:

```
Co-Authored-By: Claude <noreply@anthropic.com>
```

Do **not** include the specific model version (e.g. `Claude Opus 4.7 (1M context)`) — the Claude Code auto-mode classifier rejects model-specific co-author attribution as impersonation, so any commit using a model-version line fails to land. The generic form is the only attribution that consistently lands across model versions.

## Website pages: which skills to use

For any new or redesigned social.plus website page (static Webflow pages, not CMS posts), use these skills in this order and no others:

1. **Words:** `brand-messaging` (positioning, voice, product claims) and `site-intelligence` (read-only: what the live site already says).
2. **Design:** a Claude Design canvas built with the `design-system` skill (tokens, foundations, sections).
3. **Visuals:** `social-plus-illustration` (images), `social-plus-motion` (loops/video), `svg-icon-transformer` (icons), `video-to-gif-and-webp` (animated files).
4. **Build in Webflow:** `claude-design-to-webflow` is the only build skill. It reuses the site's existing classes, components and variables; Stefan's Developer Portal header is the reference pattern.
5. **Checks and publish:** the build skill's gate, then Webflow's `accessibility-audit` and `safe-publish` where installed. Claude publishes to staging only; production is Stefan's call.

Never use: Webflow's `figma-to-webflow`: the only flow is Claude Design → Webflow (a design that detours through Figma goes back into Claude Design before it is built), `webflow-publisher` and the blog/glossary/answers skills (CMS content only, not pages).
