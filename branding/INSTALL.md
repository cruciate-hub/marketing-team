# How to install the social.plus brand skills in Claude Code

This guide adds the **`branding`** plugin to your Claude Code (Cowork, Desktop, or terminal). After install, Claude automatically applies social.plus brand voice and design system rules to anything you write or design — and you can draft on-brand press releases on demand.

> **Marketing team:** install `marketing-team` instead of `branding`. Same setup — just substitute the plugin name in Step 3 below. See "Which plugin should I install?" at the bottom of this doc if you're not sure which one fits.

---

## What you get

Three skills, auto-triggered when relevant:

| Skill | Triggers on | What it does |
|---|---|---|
| `brand-messaging` | "review this for brand voice", "is this on-brand?", "write copy for…" | Applies social.plus voice, terminology, tone, and approved phrasings. Catches things like accidentally capitalizing "social.plus" or using forbidden terms. |
| `press-release` | "draft a press release", "we're launching X" | Generates newswire-ready press releases as `.docx`, following social.plus structure (headline, dateline, boilerplate, quote engineering, distribution checklist). |
| `design-system` | "what blue do we use?", "give me the heading sizes", any CSS/visual question | Returns the canonical color palette, type scale, spacing tokens, button states, etc. Don't approximate — get the real values. |

You don't need to invoke them manually. Claude loads them when your request matches.

---

## Setup — one time (~2 minutes)

### Step 1 — Open Claude Cowork (or Claude Code in the terminal)

Either works. The flow is identical.

### Step 2 — Add the marketplace

In Cowork:
1. Click **Customize** in the sidebar
2. Next to **Personal plugins**, click **+**
3. Click **Browse plugins** → select the **Personal** tab
4. Click **+** → select **Add marketplace**
5. Enter `cruciate-hub/marketing-team` → click **Sync**

In the terminal:
```shell
/plugin marketplace add cruciate-hub/marketing-team
```

### Step 3 — Install the `branding` plugin

In Cowork: in the plugin browser, click the **+** next to **`branding`**.

In the terminal:
```shell
/plugin install branding@cruciate-hub
```

### Step 4 — Enable auto-sync (so you stay current)

Without this, you'll miss future updates.

1. Click **⋯** next to `branding` (the plugin you just installed)
2. Toggle **Sync automatically**
3. Click **Check for updates**
4. Close and reopen Claude Desktop

### Step 5 — Test it

In a new conversation, paste any text and say:

> "Review this for brand voice."

Claude should automatically use `brand-messaging` to check tone, terminology, and approved phrasings.

Or try:

> "Draft a press release about a new partnership with Acme Corp."

Claude should automatically use `press-release` to produce a `.docx` file with the canonical social.plus structure.

---

## Verifying the install worked

Type `/help` in any session. You should see three skills under the `branding:` namespace:

- `branding:brand-messaging`
- `branding:press-release`
- `branding:design-system`

If you don't see them, restart Claude Desktop and try again. If still missing, ping Stefan.

---

## Which plugin should I install?

This marketplace has **two plugins**. Pick one, not both.

| If you're… | Install | Why |
|---|---|---|
| On the marketing team | `marketing-team` | Full kit — 14 skills covering content (blog, AEO, newsletters, case studies, press releases, brand voice), design system, SEO & internal linking, backlink work, site intelligence, and formatting utilities (legal docs, SVG icons). |
| Anyone outside the marketing team — execs, sales, engineers, founders, designers — anyone who needs to stay on-brand | `branding` | Minimum on-brand kit — 3 skills covering voice, press releases, and visual design. No SEO/marketing clutter. |

The `branding` plugin's three skills are **the same files** as the equivalents in `marketing-team` (symlinks under the hood). So brand voice, terminology, and design tokens stay consistent across the company.

---

## Troubleshooting

**Skills don't trigger automatically.**
Make sure you restarted after install. Then try invoking directly: `/branding:brand-messaging`.

**"Fetch failed" error in a skill.**
The skill couldn't reach GitHub. Check your internet, then re-run the skill. If it keeps failing, run `rm -rf /tmp/cruciate-hub-marketing-team` to clear the local cache and try again.

**I'm seeing skills I don't want.**
You probably installed `marketing-team` instead of `branding`. Uninstall: `/plugin uninstall marketing-team@cruciate-hub`, then install `branding`.

**I edit copy a lot and want stricter enforcement.**
The `brand-messaging` skill auto-triggers, but you can also force it: `/branding:brand-messaging [paste your text]`. Useful for hard reviews.

---

## Updates

You don't need to do anything. Reference content (voice rules, terminology, design tokens) updates live from GitHub on every skill run. Skill logic updates ride in via the auto-sync you turned on in Step 4.

If something feels stale, run `/plugin marketplace update cruciate-hub` to force a refresh.

---

## Questions

Ping Stefan (`stefan@social.plus`) or open an issue at https://github.com/cruciate-hub/marketing-team/issues.
