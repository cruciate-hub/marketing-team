# Getting started with aeo-content

A step-by-step guide to your first AEO article and your first batch.

AEO articles are reference pages that sit at `social.plus/answers/[slug]`. They are built to be indexed and cited by ChatGPT, Claude, Perplexity, Gemini, and Google AI Overviews.

---

## Before you start

- A Claude Cowork account (claude.ai)
- About 5 minutes for the one-time install

---

## 1. Install (one-time, ~3 min)

### Step 1 — Install the team plugin

1. Open Claude Cowork.
2. Click **Customize** in the sidebar.
3. Next to **Personal plugins**, click **+**.
4. Click **Browse plugins** → open the **Personal** tab.
5. Click the **+** → select **Add marketplace**.
6. Enter `cruciate-hub/marketing-team` → click **Sync**.
7. Click the **+** to install.

### Step 2 — Install `anthropic-skills` (needed for Word output)

Still in **Browse plugins**:

1. Switch to the **Anthropic** tab.
2. Find `anthropic-skills`.
3. Click the **+** to install.

If `anthropic-skills` is not listed in the Anthropic tab, your Cowork already has it pre-installed — skip this step.

### Step 3 — Optional: connect Ahrefs

If your team has an Ahrefs subscription, connecting it improves keyword research and the quality of suggested FAQ questions.

1. **Customize** → **Connectors** in the sidebar.
2. Find **Ahrefs** → click **Connect**.
3. Follow the OAuth flow.

Without Ahrefs, the skill falls back to generic WebSearch and still works — just with less precise data.

---

## 2. First test (2 min)

Start a new chat and type something like:

> `I need an answer page for /answers/ on in-app activity feeds.`

Or, in plain English:

> `Help me draft an /answers/ article explaining what in-app activity feeds are.`

You do not need to say "AEO" or "GEO" — the skill picks itself up from "/answers/" or "answer page."

What should happen:

1. It fetches the brand-messaging files from GitHub.
2. It drafts the article (about 90 seconds).
3. It runs compliance checks automatically.
4. It hands you a `.docx` file to download from the artifact panel.

If all four things happen, you're set. The skill should not ask you any questions when the brief is clear. It may ask a single clarifying question if something is genuinely ambiguous (for example, "feeds" could mean activity feeds, news feeds, or RSS). If it asks more than one question, something is off — flag it.

---

## 3. Writing one article

When you want a single AEO answer article:

1. **Start a chat** and describe what you want in plain English. Mentioning "/answers/" or "answer page" is usually enough for the skill to pick up. Examples:
   - `Draft an answer page on how to add chat to a mobile app.`
   - `I need an /answers/ article explaining zero-party data.`
   - `Help me write a comparison page for /answers/ — activity feeds vs group chats.`
   - `Can you create an answer page about community moderation for consumer apps?`
2. **Wait for the draft**. The skill does not ask intake questions when the brief is clear — it goes straight to drafting. The draft appears in the artifact panel in about 90 seconds. If the skill does ask a clarifying question (rare — only when the topic itself is ambiguous), answer it and move on.
3. **Ask for edits in chat**. Examples:
   - `make the intro shorter`
   - `add a pitfalls section`
   - `focus the pitch on retention, not engagement`
   - `rewrite FAQ 3 to be about moderation`
4. **Download**. When you are satisfied, the skill delivers a `.docx`. Click it in the artifact panel to download.

---

## 4. Writing a batch

When you want multiple articles in one session:

### Phase A — Ideas

Ask for ideas:

> `Give me 5 /answers/ ideas around community infrastructure for fitness apps.`

The skill produces a list of 8-15 candidates with title, intent, rationale, target keyword, and fit score.

Approve what you like in chat:

```
approve: 1, 3, 5, 7, 9
drop: 2, 8
revise: 4 — shift to retention angle
next
```

### Phase B — FAQ questions

For each approved idea, the skill surfaces 8-10 candidate FAQ questions (real ones from search results and Reddit).

Approve per article:

```
article 1: approve 1-4, drop 5
article 2: approve 1, 3, 5; revise 2 — drop the pricing angle
article 3: approve 1, 2, 4, 6
next
```

### Phase C — Drafts

The skill drafts every approved article. You will see a summary with word count and compliance status per article.

Edit any specific draft in chat:

```
article 2: shorter
article 3: add a pitfalls section
article 1: make the pitch more specific
```

The skill edits that draft, re-runs compliance, and updates the summary.

### Phase D — Deliver

When you are happy, type:

```
deliver
```

The skill produces one `.docx` per article plus a batch `.zip` containing all of them. Each `.docx` and the `.zip` appear in the artifact panel as downloadable files.

---

## 5. Approval syntax cheat sheet

| Command | What it does |
|---|---|
| `approve: 1, 3, 5` | Keep items 1, 3, 5 |
| `approve: 1-4` | Keep items 1 through 4 |
| `drop: 2, 6` | Remove items 2 and 6 |
| `revise: 4 — [instruction]` | Update item 4 with your instruction |
| `article 2: approve 1-3` | In Phase B, scope to article 2 |
| `next` | Move to the next phase |
| `deliver` | (Phase C only) produce the final `.docx` files |

Free-form messages also work. "Make number 3 more technical" will be understood — the skill falls back to natural language when the message does not match the structured syntax.

---

## 6. Troubleshooting

| Symptom | What to do |
|---|---|
| The skill does not trigger | In **Customize** → **Personal plugins**, confirm `product-marketing-team` is enabled. If an update badge shows, click the three dots → **Update**. |
| The skill produces a `.md` file instead of a `.docx` | `anthropic-skills` is not installed. Install it from **Browse plugins** → **Anthropic** tab. |
| Brand fetch fails | Reply `retry brand fetch`. If it keeps failing, ping the team — it is usually a GitHub access issue. |
| A customer name you don't recognize appears | Reply `stop, [customer name] is not approved`. Only Noom, Harley-Davidson, Smart Fit, Ulta Beauty, and Betgames are pre-cleared. |
| Compliance fails repeatedly on the same check | Tell the skill what you want: `the TL;DR is fine as-is, skip that check`. The skill can override specific warnings. |
| The article mentions a stat you can't verify | Reply `where is that stat from`. Only the approved ranges (20-50% engagement, 10-35% retention lift, 10-30% active contributors) and published customer stats are pre-cleared. |

---

## 7. Where your articles end up

The skill gives you `.docx` files. A separate automation (outside this skill) converts each `.docx` into Webflow-ready HTML and publishes it to `social.plus/answers/[slug]`. Your job is to produce the `.docx`; the rest is automatic.

---

## 8. What this skill does NOT do

This skill is only for AEO answer articles. For other content types, switch skills:

| You want to write | Use |
|---|---|
| Blog post, long-form article, pillar page | `blog-seo-content` |
| Customer story / case study | `case-study` |
| Social media post (LinkedIn, Instagram, X) | `social-media` |
| Ad copy or campaign landing page | `campaign-copy` |
| Website page copy | `brand-messaging` |
| Monthly newsletter or release email | `newsletters` |

If you ask this skill for something outside its scope (e.g., "write a LinkedIn post"), it will redirect you to the right one.
