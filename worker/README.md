# socialplus-site-json — Cloudflare Worker

The worker that keeps every `website/pages-*.json` file in this repo in sync with Webflow, and runs AI-powered gap analysis when new product updates publish.

## What it does

1. **Snapshots Webflow content to GitHub.** On every Webflow site publish or CMS item publish, the corresponding `website/pages-{type}.json` file is regenerated and committed. No manual steps.
2. **Runs gap analysis.** When a Release Note or Monthly Product Update publishes, the worker fetches the marketing + use-cases inventories, calls Claude, and sends a gap report to a Make.com webhook for email delivery.

Nine inventory files are maintained:

| File | Source |
|---|---|
| `website/pages-marketing.json` | Static Webflow pages (Pages API) |
| `website/pages-use-cases.json` | Use Cases CMS collection |
| `website/pages-blog.json` | Blog Posts CMS |
| `website/pages-glossary.json` | Glossaries CMS |
| `website/pages-answers.json` | Answers CMS |
| `website/pages-customer-stories.json` | Customer Stories CMS |
| `website/pages-release-notes.json` | Release Notes CMS |
| `website/pages-product-updates.json` | Monthly Product Updates CMS |
| `website/pages-webinars.json` | Webinars CMS |

## Routes

| Route | Method | Purpose |
|---|---|---|
| `/generate/<target>` | GET | Regenerate one target. `<target>` is one of `marketing`, `use-cases`, `blog`, `glossary`, `answers`, `customer-stories`, `release-notes`, `product-updates`, `webinars`, or `all`. Requires `?token=<WORKER_AUTH_TOKEN>`. |
| `/webhook/publish` | POST | Webflow site publish webhook. Regenerates `pages-marketing.json`. |
| `/webhook/cms-published` | POST | Webflow CMS publish webhook. Dispatches by collection ID → regenerates the right inventory file; for Release Notes / Product Updates also runs gap analysis. |

Unknown routes return a minimal 200 with no disclosure.

**Note:** on Workers Free plan (50 subrequests per invocation), `/generate/all` may hit the cap. Backfills should use per-target `/generate/<target>` calls instead. An upgrade to Workers Paid lifts this to 10,000.

## Environment

**Source of truth: `wrangler.toml`.** Variables declared there are overwritten in the Cloudflare dashboard on every `wrangler deploy`. Edit `wrangler.toml`, not the dashboard, for plaintext variables. Secrets are managed separately (see below).

### Plaintext variables (in `wrangler.toml`)

All 9 Webflow CMS collection IDs. Safe to commit — these are public identifiers.

### Secrets (Cloudflare dashboard only, never committed)

| Secret | Purpose |
|---|---|
| `GITHUB_TOKEN` | Fine-grained PAT for this repo (`contents: write`) |
| `ANTHROPIC_API_KEY` | Claude API key (used during gap analysis) |
| `WEBFLOW_API_TOKEN` | Webflow Data API token |
| `MAKE_WEBHOOK_URL` | Make.com webhook that forwards gap reports to email |
| `WORKER_AUTH_TOKEN` | Protects `/generate/*` routes. If unset, all `/generate/*` calls return 401 (fail-closed). |

To rotate a secret:
```bash
cd worker
npx wrangler secret put SECRET_NAME
```

## Local setup

```bash
cd worker
npm install           # installs wrangler locally
npx wrangler login    # one-time OAuth against the Cloudflare account
npx wrangler whoami   # verify
```

## Deploying

```bash
cd worker
npx wrangler deploy
```

Deploys from `src/index.js` to the production worker. Takes ~5 seconds. Wrangler writes the compiled version + `wrangler.toml` env vars; dashboard secrets are left untouched.

## Debugging

Stream live logs from the production worker:
```bash
cd worker
npx wrangler tail
```

## File layout

```
worker/
├── README.md            ← this file
├── wrangler.toml        ← config + plaintext env vars
├── package.json         ← wrangler version pin
├── package-lock.json
├── .gitignore
└── src/
    └── index.js         ← the entire worker (~1000 lines, single file)
```

## When to edit

- **Adding a new Webflow CMS collection** → add a collection ID to `wrangler.toml`, write a new `generateXxxJSON` function in `src/index.js`, register it in the `GENERATORS` dispatcher, extend `/webhook/cms-published`, add an entry to `FILES`.
- **Changing which marketing pages are tracked** → edit `TRACKED_MARKETING_PAGES` in `src/index.js`. Keep total under 45 to stay safely under the 50-subrequest Free plan cap.
- **Changing gap-analysis prompt or brand fetch list** → edit `runGapAnalysis` in `src/index.js`.

## Known deferred items

- **Webhook signature verification** not yet implemented on `/webhook/*` — anyone who knows the URL can POST and trigger a regen + gap analysis + Make email. Worth fixing.
- **No retry-on-429** if Webflow rate-limits. Current throttle (1.1s delay) stays under the 60/min cap so this hasn't bitten us.
