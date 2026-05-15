# Install the Marketing Team plugins

A visual, click-by-click walkthrough for installing the `cruciate-hub/marketing-team` marketplace in the Claude desktop app — then picking the right plugin (`marketing-team` or `brand-kit`) for your role.

You need the **Claude desktop app** (Mac or Windows). The web app at claude.ai does not have the plugin marketplace.

---

## Step 1 — Open Customize

Open the Claude desktop app. In the left sidebar, click **Customize**.

![Click Customize in the left sidebar](./install-assets/01-customize.png)

---

## Step 2 — Open the "Add plugin" menu

In the left sidebar of the Customize screen, find the **Personal plugins** section. Hover over it and a **+** icon appears on the right. Click it.

![Click the plus icon next to Personal plugins](./install-assets/02-add-plugin.png)

---

## Step 3 — Click "Browse plugins"

A small dropdown opens with two options. Click **Browse plugins** (the top one). Do *not* click "Create plugin" — that's for building your own.

![Click Browse plugins in the dropdown](./install-assets/03-browse-plugins.png)

---

## Step 4 — Open the marketplace menu

The **Directory** window opens. Make sure **Plugins** is selected in its left sidebar (it should be by default).

Hover over the **`skills`** pill (or whichever one is selected) until the **`···`** (three dots) appear next to it. Click the **`···`**.

![Click the three-dot menu next to the skills marketplace pill](./install-assets/04-open-menu.png)

---

## Step 5 — Click "Add marketplace"

A small menu opens with two options. Click **Add marketplace**.

![Click Add marketplace from the menu](./install-assets/05-add-marketplace.png)

---

## Step 6 — Paste the marketplace address and Sync

The **Add marketplace** dialog opens. In the **URL** field, paste:

```
cruciate-hub/marketing-team
```

Then click **Sync** in the bottom right. Claude will fetch the marketplace from GitHub — this takes a few seconds.

![Paste the URL and click Sync](./install-assets/06-paste-url-and-sync.png)

> **Note on the warning banner:** Claude shows a red warning about trusting third-party plugins. This marketplace is maintained by The Cruciate Hub (the team behind social.plus), so it's safe to proceed.

---

## Step 7 — Install your plugin

You're now back in the Directory and a new **`marketing-team`** pill is selected. You'll see two plugin cards:

- **Brand kit** — 2 skills: `brand-messaging` and `design-system`.
- **Marketing team** — 14 skills covering content, design, SEO, linking, and more.

**Install one, not both.** Click the **+** on the card that matches your role (see "Which one should I install?" below).

![Click the plus icon next to the plugin you want to install](./install-assets/07-install-plugin.png)

Claude installs the plugin and its skills. You're done — close the Directory window.

---

## Which one should I install?

| | Brand kit | Marketing team |
|---|---|---|
| **For** | Everyone outside the marketing team | The marketing team |
| **Skills** | 2 — `brand-messaging`, `design-system` | 14 — content, SEO, design, linking, formatting |
| **Use it when** | You occasionally write copy or build something visual and need to stay on-brand | You produce marketing content end-to-end: blog posts, landing pages, emails, customer stories, press releases, etc. |

Not sure? Pick **Brand kit**. You can swap to the full Marketing team plugin later by reinstalling.

---

## Stay up to date (do this once)

The skills load their content live from GitHub every session, so most updates reach you automatically. But the plugin manifest itself — new skills, renamed skills — needs a one-time auto-sync setup. Without it, you stay frozen on the version you installed and miss every future update.

Open the Directory again (the same window from Steps 4–7). Your installed plugin's pill is now selected at the top of the marketplace row. The next three steps all happen in one menu — see the highlighted callouts in the screenshot below.

![Auto-sync setup: click the three dots, toggle Sync automatically, then Check for updates](./install-assets/08-sync-and-update.png)

### Step 8 — Open the plugin's settings menu

Click the **`···`** next to your installed plugin's pill (`marketing-team` or `brand-kit`) at the top of the marketplace row. A small menu opens.

### Step 9 — Toggle "Sync automatically" on

In the menu, find **Sync automatically** and click the toggle so it turns on. This is what makes future updates flow to you without manual intervention.

### Step 10 — Click "Check for updates"

Still in the same menu, click **Check for updates** to pull the latest version right now. You'll see the synced commit hash update at the top of the menu.

### Step 11 — Quit and reopen the Claude desktop app

Close the Claude desktop app completely (<kbd>⌘</kbd>+<kbd>Q</kbd> on Mac, or right-click the dock icon → Quit), then open it again. Plugins load on startup, so this is what makes the new skills actually available in your chats.

---

That's it — auto-sync is on. New and improved skills will reach you on the next Claude desktop startup whenever an update lands on `main`.
