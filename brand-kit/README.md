# Brand Kit Plugin

The minimum on-brand kit for social.plus — two skills only. Install this if you need to stay on-brand but you're not on the marketing team.

## Skills (2)

| Skill | Triggers on | What it does |
|---|---|---|
| [brand-messaging](./skills/brand-messaging/SKILL.md) | "review this for brand voice", "is this on-brand?", "write copy for…" | Applies social.plus voice, terminology, tone, and approved phrasings. Catches things like accidentally capitalizing "social.plus" or using forbidden terms. |
| [design-system](./skills/design-system/SKILL.md) | "what blue do we use?", "give me the heading sizes", any CSS/visual question | Returns the canonical color palette, type scale, spacing tokens, button states, etc. Don't approximate — get the real values. |

Both skills above are **symlinks** in the source repo, pointing to the canonical SKILL.md files in the sibling `marketing-team` plugin — one source of truth for skill logic. At runtime, the skills fetch their reference content (brand voice, terminology, design tokens) directly from this GitHub repo on every session, so both plugins always show the same up-to-date content.

You don't need to invoke skills manually. Claude loads them when your request matches.

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

### Step 3 — Install the `brand-kit` plugin

In Cowork: in the plugin browser, click the **+** next to **`brand-kit`**.

In the terminal:
```shell
/plugin install brand-kit@cruciate-hub
```

### Step 4 — Enable auto-sync (so you stay current)

Without this, you'll miss future updates.

1. Click **⋯** next to `brand-kit` (the plugin you just installed)
2. Toggle **Sync automatically**
3. Click **Check for updates**
4. Close and reopen Claude Desktop

### Step 5 — Test it

In a new conversation, paste any text and say:

> "Review this for brand voice."

Claude should automatically use `brand-messaging` to check tone, terminology, and approved phrasings.

Or try:

> "What blue does social.plus use, and at what hex?"

Claude should automatically use `design-system` to return the canonical color palette.

## Verify the install worked

Type `/help` in any session. You should see two skills under the `brand-kit:` namespace:

- `brand-kit:brand-messaging`
- `brand-kit:design-system`

If you don't see them, restart Claude Desktop and try again. If still missing, ping Stefan.

## How it stays up to date

You don't need to do anything. Reference content (voice rules, terminology, design tokens) updates live from GitHub on every skill run. Skill logic updates ride in via the auto-sync you turned on in Step 4.

If something feels stale, run `/plugin marketplace update cruciate-hub` to force a refresh.

<details>
<summary><strong>Which plugin should I install — brand-kit or marketing-team?</strong></summary>

This marketplace has **two plugins**. Pick one, not both.

| If you're… | Install | Why |
|---|---|---|
| On the marketing team | `marketing-team` | Full kit — 14 skills covering content (blog, AEO, newsletters, case studies, press releases, brand voice), design system, SEO & internal linking, backlink work, site intelligence, and formatting utilities (legal docs, SVG icons). |
| Anyone outside the marketing team — execs, sales, engineers, founders, designers — anyone who needs to stay on-brand | `brand-kit` | Minimum on-brand kit — 2 skills covering voice and visual design. No press-release, SEO, or marketing clutter. |

The `brand-kit` plugin's two skills are **the same files** as the equivalents in `marketing-team` (symlinks under the hood). So brand voice, terminology, and design tokens stay consistent across the company.

</details>

<details>
<summary><strong>Troubleshooting</strong></summary>

**Skills don't trigger automatically.**
Make sure you restarted after install. Then try invoking directly: `/brand-kit:brand-messaging`.

**"Fetch failed" error in a skill.**
The skill couldn't reach GitHub. Check your internet, then re-run the skill. If it keeps failing, run `rm -rf /tmp/cruciate-hub-marketing-team` to clear the local cache and try again.

**I'm seeing skills I don't want.**
You probably installed `marketing-team` instead of `brand-kit`. Uninstall: `/plugin uninstall marketing-team@cruciate-hub`, then install `brand-kit`.

**I edit copy a lot and want stricter enforcement.**
The `brand-messaging` skill auto-triggers, but you can also force it: `/brand-kit:brand-messaging [paste your text]`. Useful for hard reviews.

</details>

## Questions

Ping Stefan (`stefan@social.plus`) or open an issue at https://github.com/cruciate-hub/marketing-team/issues.
