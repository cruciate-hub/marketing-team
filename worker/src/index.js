/**
 * cruciate-hub-site-json — Cloudflare Worker
 *
 * Keeps JSON snapshots of the social.plus website on GitHub, and runs
 * AI-powered gap analysis when new product features are released.
 *
 * Required env vars:
 *   Secrets:
 *     GITHUB_TOKEN        — fine-grained token for cruciate-hub/marketing-team repo
 *     ANTHROPIC_API_KEY   — Claude API key
 *     WEBFLOW_API_TOKEN   — Webflow Data API token
 *     MAKE_WEBHOOK_URL    — Make.com webhook URL for email delivery
 *     WORKER_AUTH_TOKEN   — Required. Protects /generate/* routes. If unset, all auth-gated routes return 401.
 *
 *   Webflow CMS collection IDs (wrangler.toml is source-of-truth — do NOT edit in dashboard):
 *     USE_CASES         — 66e2765d540e1939a89db7a6
 *     PRICING_FEATURES  — 66e2765d540e1939a89db7be  (embedded in /pricing, not a standalone page)
 *     RELEASE_NOTES     — 697713f21a4cfd3f4db2768b  (inventory + gap analysis)
 *     PRODUCT_UPDATES   — 66e2765d540e1939a89db971  (inventory + gap analysis)
 *     BLOG              — 66e2765d540e1939a89db6a4
 *     GLOSSARY          — 66e2765d540e1939a89db93e
 *     ANSWERS           — 68f643838f7abffca74efbc1
 *     CUSTOMER_STORIES  — 66e2765d540e1939a89db5eb
 *     WEBINARS          — 66e2765d540e1939a89db84e
 *
 * Debug: `npx wrangler tail` from ~/Projects/socialplus/socialplus-site-json to stream live logs.
 */

// ─── Config ──────────────────────────────────────────────────────────────────

const SITE_ID = '66e2765d540e1939a89db4bb';
const GITHUB_REPO = 'cruciate-hub/marketing-team';
const WEBFLOW_API_BASE = 'https://api.webflow.com/v2';
const SITE_BASE_URL = 'https://www.social.plus';

const FILES = {
  marketing: 'website/pages-marketing.json',
  useCases: 'website/pages-use-cases.json',
  blog: 'website/pages-blog.json',
  glossary: 'website/pages-glossary.json',
  answers: 'website/pages-answers.json',
  customerStories: 'website/pages-customer-stories.json',
  releaseNotes: 'website/pages-release-notes.json',
  productUpdates: 'website/pages-product-updates.json',
  webinars: 'website/pages-webinars.json',
};

const TRACKED_MARKETING_PAGES = [
  // Core
  '/', '/product', '/pricing',
  // Product landings
  '/social', '/chat', '/video', '/analytics', '/moderation', '/monetization',
  // Feature / SDK / UIKit
  '/social/features', '/social/sdk', '/social/uikit', '/social/stories',
  '/chat/features', '/chat/sdk', '/chat/uikit',
  '/video/features', '/video/sdk',
  // Industry (10)
  '/industry/retail', '/industry/fitness', '/industry/travel',
  '/industry/sports', '/industry/health-and-wellness', '/industry/fintech',
  '/industry/media-and-news', '/industry/edtech', '/industry/gaming',
  '/industry/betting',
  // Sales-facing
  '/app-audit', '/developer-kits', '/vs-stream', '/partner-program',
  '/professional-services', '/collaborate',
  // White-label
  '/white-label/chat-software', '/white-label/in-app-community', '/white-label/social-network',
];

const CMS_PAGE_ENRICHMENT_FORMATS = {
  '/pricing': 'pricing-features',
};

const SKIP_EXACT = new Set(['-', '•', '→', '←']);
const MIN_CONTENT_LENGTH = 3;
const API_DELAY_MS = 1100; // 1.1s between requests → ~55 req/min, under Webflow's 60/min limit

// ─── Auth ────────────────────────────────────────────────────────────────────

/**
 * Fail-closed auth. If WORKER_AUTH_TOKEN is unset, all calls are denied.
 * Prevents silent open-access if env var is accidentally removed.
 */
function checkAuth(request, env) {
  if (!env.WORKER_AUTH_TOKEN) return false;
  const token = new URL(request.url).searchParams.get('token');
  return token === env.WORKER_AUTH_TOKEN;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function webflowFetch(path, env, params = {}) {
  const url = new URL(`${WEBFLOW_API_BASE}${path}`);
  Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));

  const res = await fetch(url.toString(), {
    headers: {
      'Authorization': `Bearer ${env.WEBFLOW_API_TOKEN}`,
      'accept': 'application/json',
    },
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Webflow API ${res.status} on ${path}: ${text}`);
  }
  return res.json();
}

async function listAllPages(env) {
  const pages = [];
  let offset = 0;
  const limit = 100;
  while (true) {
    const data = await webflowFetch(`/sites/${SITE_ID}/pages`, env, { limit, offset });
    pages.push(...data.pages);
    if (pages.length >= data.pagination.total) break;
    offset += limit;
    await sleep(API_DELAY_MS);
  }
  return pages;
}

async function getPageTextNodes(pageId, env) {
  const nodes = [];
  let offset = 0;
  const limit = 100;
  while (true) {
    const data = await webflowFetch(`/pages/${pageId}/dom`, env, { limit, offset });
    nodes.push(...data.nodes);
    if (nodes.length >= data.pagination.total) break;
    offset += limit;
    await sleep(API_DELAY_MS);
  }
  return nodes;
}

async function getAllCollectionItems(collectionId, env) {
  const items = [];
  let offset = 0;
  const limit = 100;
  while (true) {
    const data = await webflowFetch(`/collections/${collectionId}/items`, env, { limit, offset });
    items.push(...data.items);
    if (items.length >= data.pagination.total) break;
    offset += limit;
    await sleep(API_DELAY_MS);
  }
  return items;
}

// ─── Content extraction ──────────────────────────────────────────────────────

function shouldSkipText(text) {
  const trimmed = text.trim();
  if (!trimmed || trimmed.length < MIN_CONTENT_LENGTH) return true;
  if (SKIP_EXACT.has(trimmed)) return true;
  return false;
}

function isHeading(html) {
  return /^<h[1-4]/.test(html);
}

function extractTextFromNodes(nodes) {
  const lines = [];
  let contentStarted = false;
  for (const node of nodes) {
    if (node.type !== 'text') continue;
    const html = node.text?.html || '';
    const text = node.text?.text?.trim();
    if (!text || shouldSkipText(text)) continue;
    if (!contentStarted) {
      if (isHeading(html)) {
        contentStarted = true;
      } else {
        continue;
      }
    }
    if (html.startsWith('<h1')) lines.push(`# ${text}`);
    else if (html.startsWith('<h2')) lines.push(`## ${text}`);
    else if (html.startsWith('<h3')) lines.push(`### ${text}`);
    else if (html.startsWith('<h4')) lines.push(`#### ${text}`);
    else lines.push(text);
  }
  return lines.join('\n');
}

/**
 * Extract H1-H6 heading hierarchy from a Webflow RichText HTML string.
 * Used by blog, glossary, answers, etc. where the body content lives in a RichText field
 * rather than being reachable via the Pages DOM API.
 *
 * Returns markdown-style headings: "# H1\n## H2\n### H3\n..." matching extractTextFromNodes output.
 * Non-heading content (paragraphs, lists, images) is intentionally skipped — we only want structure.
 */
function extractHeadingsFromRichText(html) {
  if (!html) return '';
  const lines = [];
  // Matches <h1>..</h1> through <h6>..</h6> (including attributes, multiline content)
  const regex = /<h([1-6])[^>]*>([\s\S]*?)<\/h\1>/gi;
  let match;
  while ((match = regex.exec(html)) !== null) {
    const level = parseInt(match[1], 10);
    // Strip any inner HTML (e.g., <strong>, <em>, <a>) to get the plain heading text
    const text = match[2].replace(/<[^>]+>/g, '').trim();
    if (text) {
      lines.push(`${'#'.repeat(level)} ${text}`);
    }
  }
  return lines.join('\n');
}

function formatPricingFeatures(items) {
  items.sort((a, b) => (a.fieldData.order || 0) - (b.fieldData.order || 0));
  const lines = ['## Usage & Features Comparison'];
  for (const item of items) {
    const fd = item.fieldData;
    const name = fd.name;
    const core = fd['tier-2'] ? '✓' : (fd['text---tier-2'] || '—');
    const max = fd['tier-3'] ? '✓' : (fd['text---tier-3'] || '—');
    lines.push(`${name}: Core=${core}, Max=${max}`);
  }
  return lines.join('\n');
}

function formatUseCaseItem(fd) {
  const lines = [];
  lines.push(`# ${fd.name}`);
  if (fd['short-description']) lines.push(fd['short-description']);
  if (fd['section-2-title']) lines.push(`## ${fd['section-2-title']}`);
  for (let i = 1; i <= 3; i++) {
    const title = fd[`section-2-card-${i}-title`];
    const desc = fd[`section-2-card-${i}-description`];
    if (title) lines.push(`### ${title}`);
    if (desc) lines.push(desc);
  }
  if (fd['section-3-main-title']) lines.push(`## ${fd['section-3-main-title']}`);
  for (let i = 1; i <= 4; i++) {
    const title = fd[`section-3-topic-${i}-title`];
    const desc = fd[`section-3-topic-${i}`];
    if (title) lines.push(`### ${title}`);
    if (desc) lines.push(desc);
  }
  for (let i = 1; i <= 6; i++) {
    const title = fd[`section-4-card-${i}-title`];
    const desc = fd[`section-4-card-${i}`];
    if (title) lines.push(`### ${title}`);
    if (desc) lines.push(desc);
  }
  return lines.filter(l => l && l.trim()).join('\n');
}

// ─── Generators ──────────────────────────────────────────────────────────────

async function generateMarketingPagesJSON(env) {
  console.log('Generating pages-marketing.json...');

  const allPages = await listAllPages(env);
  const pageByPath = {};
  for (const p of allPages) {
    if (p.publishedPath && !p.draft) {
      pageByPath[p.publishedPath] = p;
    }
  }
  console.log(`Found ${Object.keys(pageByPath).length} published pages`);

  const pages = [];
  const errors = [];

  for (let i = 0; i < TRACKED_MARKETING_PAGES.length; i++) {
    const path = TRACKED_MARKETING_PAGES[i];
    const pageInfo = pageByPath[path];
    if (!pageInfo) {
      console.warn(`Page not found for path: ${path}`);
      errors.push(path);
      continue;
    }
    if (i > 0) await sleep(API_DELAY_MS);

    try {
      console.log(`Extracting [${i + 1}/${TRACKED_MARKETING_PAGES.length}]: ${path}`);
      const nodes = await getPageTextNodes(pageInfo.id, env);
      let content = extractTextFromNodes(nodes);

      if (CMS_PAGE_ENRICHMENT_FORMATS[path] === 'pricing-features') {
        const cmsItems = await getAllCollectionItems(env.PRICING_FEATURES, env);
        content += '\n\n' + formatPricingFeatures(cmsItems);
      }

      pages.push({
        url: `${SITE_BASE_URL}${path}`,
        metaTitle: pageInfo.seo?.title || pageInfo.title || '',
        metaDescription: pageInfo.seo?.description || '',
        content,
      });
    } catch (err) {
      console.error(`Error extracting ${path}: ${err.message}`);
      errors.push(path);
    }
  }

  return {
    _meta: {
      generatedAt: new Date().toISOString(),
      itemCount: pages.length,
      method: 'webflow-data-api',
      errors: errors.length > 0 ? errors : undefined,
    },
    pages,
  };
}

async function generateUseCasesJSON(env) {
  console.log('Generating pages-use-cases.json...');
  if (!env.USE_CASES) throw new Error('USE_CASES env var not set');

  const items = await getAllCollectionItems(env.USE_CASES, env);
  console.log(`Found ${items.length} use case items`);

  const pages = [];
  for (const item of items) {
    if (item.isDraft || item.isArchived) continue;
    const fd = item.fieldData;
    if (!fd.slug) continue;

    pages.push({
      url: `${SITE_BASE_URL}/use-case/${fd.slug}`,
      metaTitle: fd.name || '',
      metaDescription: fd['short-description'] || '',
      content: formatUseCaseItem(fd),
    });
  }

  return {
    _meta: {
      generatedAt: new Date().toISOString(),
      itemCount: pages.length,
      collectionId: env.USE_CASES,
      method: 'webflow-data-api',
    },
    pages,
  };
}

async function generateBlogJSON(env) {
  console.log('Generating pages-blog.json...');
  if (!env.BLOG) throw new Error('BLOG env var not set');

  const items = await getAllCollectionItems(env.BLOG, env);
  console.log(`Found ${items.length} blog items`);

  const pages = [];
  for (const item of items) {
    if (item.isDraft || item.isArchived) continue;
    const fd = item.fieldData;
    if (!fd.slug) continue;

    // Prepend the post title as H1 — Webflow renders `name` as the page H1,
    // but it's not inside the post-content RichText field.
    const headings = extractHeadingsFromRichText(fd['post-content']);
    const content = [`# ${fd.name}`, headings].filter(Boolean).join('\n');

    pages.push({
      url: `${SITE_BASE_URL}/blog/${fd.slug}`,
      metaTitle: fd.name || '',
      metaDescription: fd['meta-description'] || '',
      content,
    });
  }

  return {
    _meta: {
      generatedAt: new Date().toISOString(),
      itemCount: pages.length,
      collectionId: env.BLOG,
      method: 'webflow-data-api',
    },
    pages,
  };
}

async function generateGlossaryJSON(env) {
  console.log('Generating pages-glossary.json...');
  if (!env.GLOSSARY) throw new Error('GLOSSARY env var not set');

  const items = await getAllCollectionItems(env.GLOSSARY, env);
  console.log(`Found ${items.length} glossary items`);

  const pages = [];
  for (const item of items) {
    if (item.isDraft || item.isArchived) continue;
    const fd = item.fieldData;
    if (!fd.slug) continue;
    // Glossary collection has a dedicated "not-in-use" switch for deprecated entries.
    if (fd['not-in-use']) continue;

    const headings = extractHeadingsFromRichText(fd.glossary);
    const content = [`# ${fd.name}`, headings].filter(Boolean).join('\n');

    pages.push({
      url: `${SITE_BASE_URL}/glossary/${fd.slug}`,
      metaTitle: fd['meta-title'] || fd.name || '',
      metaDescription: fd['meta-description'] || '',
      content,
    });
  }

  return {
    _meta: {
      generatedAt: new Date().toISOString(),
      itemCount: pages.length,
      collectionId: env.GLOSSARY,
      method: 'webflow-data-api',
    },
    pages,
  };
}

async function generateAnswersJSON(env) {
  console.log('Generating pages-answers.json...');
  if (!env.ANSWERS) throw new Error('ANSWERS env var not set');

  const items = await getAllCollectionItems(env.ANSWERS, env);
  console.log(`Found ${items.length} answer items`);

  const pages = [];
  for (const item of items) {
    if (item.isDraft || item.isArchived) continue;
    const fd = item.fieldData;
    if (!fd.slug) continue;

    const headings = extractHeadingsFromRichText(fd.content);
    const content = [`# ${fd.name}`, headings].filter(Boolean).join('\n');

    pages.push({
      url: `${SITE_BASE_URL}/answers/${fd.slug}`,
      metaTitle: fd['meta-title'] || fd.name || '',
      metaDescription: fd['meta-description'] || '',
      content,
    });
  }

  return {
    _meta: {
      generatedAt: new Date().toISOString(),
      itemCount: pages.length,
      collectionId: env.ANSWERS,
      method: 'webflow-data-api',
    },
    pages,
  };
}

async function generateCustomerStoriesJSON(env) {
  console.log('Generating pages-customer-stories.json...');
  if (!env.CUSTOMER_STORIES) throw new Error('CUSTOMER_STORIES env var not set');

  const items = await getAllCollectionItems(env.CUSTOMER_STORIES, env);
  console.log(`Found ${items.length} customer story items`);

  const pages = [];
  for (const item of items) {
    if (item.isDraft || item.isArchived) continue;
    const fd = item.fieldData;
    if (!fd.slug) continue;
    // Skip stories hidden from the website.
    if (fd['do-not-show-on-the-website']) continue;

    // Hero title sits in `title`; body lives in RichText `section-2-text`.
    const headings = extractHeadingsFromRichText(fd['section-2-text']);
    const heroTitle = fd.title ? `# ${fd.title}` : `# ${fd.name}`;
    const content = [heroTitle, headings].filter(Boolean).join('\n');

    pages.push({
      url: `${SITE_BASE_URL}/customer-story/${fd.slug}`,
      metaTitle: fd.name || fd.title || '',
      metaDescription: fd['meta-description'] || fd['hero-introduction-paragraph'] || '',
      content,
    });
  }

  return {
    _meta: {
      generatedAt: new Date().toISOString(),
      itemCount: pages.length,
      collectionId: env.CUSTOMER_STORIES,
      method: 'webflow-data-api',
    },
    pages,
  };
}

async function generateReleaseNotesJSON(env) {
  console.log('Generating pages-release-notes.json...');
  if (!env.RELEASE_NOTES) throw new Error('RELEASE_NOTES env var not set');

  const items = await getAllCollectionItems(env.RELEASE_NOTES, env);
  console.log(`Found ${items.length} release note items`);

  const pages = [];
  for (const item of items) {
    if (item.isDraft || item.isArchived) continue;
    const fd = item.fieldData;
    if (!fd.slug) continue;

    const headings = extractHeadingsFromRichText(fd['paragraph-2']);
    const content = [`# ${fd.name}`, headings].filter(Boolean).join('\n');

    pages.push({
      url: `${SITE_BASE_URL}/release-note/${fd.slug}`,
      metaTitle: fd.name || '',
      metaDescription: fd['intro-text'] || '',
      content,
    });
  }

  return {
    _meta: {
      generatedAt: new Date().toISOString(),
      itemCount: pages.length,
      collectionId: env.RELEASE_NOTES,
      method: 'webflow-data-api',
    },
    pages,
  };
}

async function generateProductUpdatesJSON(env) {
  console.log('Generating pages-product-updates.json...');
  if (!env.PRODUCT_UPDATES) throw new Error('PRODUCT_UPDATES env var not set');

  const items = await getAllCollectionItems(env.PRODUCT_UPDATES, env);
  console.log(`Found ${items.length} product update items`);

  const pages = [];
  for (const item of items) {
    if (item.isDraft || item.isArchived) continue;
    const fd = item.fieldData;
    if (!fd.slug) continue;

    const headings = extractHeadingsFromRichText(fd['post-content']);
    const content = [`# ${fd.name}`, headings].filter(Boolean).join('\n');

    pages.push({
      url: `${SITE_BASE_URL}/product-update/${fd.slug}`,
      metaTitle: fd.name || '',
      metaDescription: fd['meta-description'] || fd['post-summary'] || '',
      content,
    });
  }

  return {
    _meta: {
      generatedAt: new Date().toISOString(),
      itemCount: pages.length,
      collectionId: env.PRODUCT_UPDATES,
      method: 'webflow-data-api',
    },
    pages,
  };
}

async function generateWebinarsJSON(env) {
  console.log('Generating pages-webinars.json...');
  if (!env.WEBINARS) throw new Error('WEBINARS env var not set');

  const items = await getAllCollectionItems(env.WEBINARS, env);
  console.log(`Found ${items.length} webinar items`);

  const pages = [];
  for (const item of items) {
    if (item.isDraft || item.isArchived) continue;
    const fd = item.fieldData;
    if (!fd.slug) continue;

    // The Webinars collection is routed at `/webinars/{slug}` on the live site.
    const headings = extractHeadingsFromRichText(fd['page-content-2']);
    const content = [`# ${fd.name}`, headings].filter(Boolean).join('\n');

    pages.push({
      url: `${SITE_BASE_URL}/webinars/${fd.slug}`,
      metaTitle: fd.name || '',
      metaDescription: fd['pop-up-cta-subtitle'] || '',
      content,
    });
  }

  return {
    _meta: {
      generatedAt: new Date().toISOString(),
      itemCount: pages.length,
      collectionId: env.WEBINARS,
      method: 'webflow-data-api',
    },
    pages,
  };
}

// ─── GitHub commit ───────────────────────────────────────────────────────────

/**
 * Commit a JSON file to GitHub with automatic retry on 409 SHA conflicts.
 *
 * A 409 happens when another commit (e.g., a parallel generator or a merged PR)
 * lands between our GET-SHA and our PUT-with-that-SHA. On 409, we re-fetch the
 * current SHA and retry the PUT. Max 2 retries before giving up.
 */
async function commitToGitHub(content, env, filePath, attempt = 0) {
  const MAX_ATTEMPTS = 3; // initial + 2 retries
  const jsonStr = JSON.stringify(content, null, 2);
  const base64Content = btoa(unescape(encodeURIComponent(jsonStr)));

  const getRes = await fetch(
    `https://api.github.com/repos/${GITHUB_REPO}/contents/${filePath}`,
    {
      headers: {
        'Authorization': `token ${env.GITHUB_TOKEN}`,
        'User-Agent': 'cruciate-hub-site-json-worker',
        'Accept': 'application/vnd.github.v3+json',
      },
    }
  );

  let sha = null;
  let existingContent = null;
  if (getRes.ok) {
    const data = await getRes.json();
    sha = data.sha;
    existingContent = data.content?.replace(/\n/g, '');
  }

  if (existingContent && existingContent === base64Content.replace(/\n/g, '')) {
    console.log(`No changes detected for ${filePath} — skipping commit`);
    return { committed: false, reason: 'no-changes', filePath };
  }

  const fileName = filePath.split('/').pop();
  const body = {
    message: `Update ${fileName} (${content._meta.itemCount} items, ${(jsonStr.length / 1024).toFixed(0)}KB)`,
    content: base64Content,
    branch: 'main',
  };
  if (sha) body.sha = sha;

  const putRes = await fetch(
    `https://api.github.com/repos/${GITHUB_REPO}/contents/${filePath}`,
    {
      method: 'PUT',
      headers: {
        'Authorization': `token ${env.GITHUB_TOKEN}`,
        'User-Agent': 'cruciate-hub-site-json-worker',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    }
  );

  // 409 = SHA conflict (parallel commit landed). Retry by re-fetching the SHA.
  if (putRes.status === 409 && attempt + 1 < MAX_ATTEMPTS) {
    console.warn(`SHA conflict on ${filePath} (attempt ${attempt + 1}/${MAX_ATTEMPTS}) — retrying after 500ms`);
    await sleep(500);
    return commitToGitHub(content, env, filePath, attempt + 1);
  }

  if (!putRes.ok) {
    const err = await putRes.text();
    throw new Error(`GitHub commit failed for ${filePath}: ${putRes.status} ${err}`);
  }

  console.log(`Committed ${filePath} to GitHub${attempt > 0 ? ` (after ${attempt} retry)` : ''}`);
  return { committed: true, filePath };
}

// ─── Gap analysis ────────────────────────────────────────────────────────────

async function fetchGitHubFile(path, env) {
  const res = await fetch(
    `https://api.github.com/repos/${GITHUB_REPO}/contents/${path}`,
    {
      headers: {
        'Authorization': `token ${env.GITHUB_TOKEN}`,
        'User-Agent': 'cruciate-hub-site-json-worker',
        'Accept': 'application/vnd.github.v3+json',
      },
    }
  );
  if (!res.ok) return null;
  const data = await res.json();
  return decodeURIComponent(escape(atob(data.content.replace(/\n/g, ''))));
}

async function runGapAnalysis(itemName, itemSlug, introText, type, env) {
  const [
    marketingPages, useCasesPages,
    mainBrain, messagingBrain, skillMd,
    toneMd, terminologyMd, positioningMd, boilerplatesMd, narrativeMd, valueStoryMd,
  ] = await Promise.all([
    fetchGitHubFile(FILES.marketing, env),
    fetchGitHubFile(FILES.useCases, env),
    fetchGitHubFile('brain.md', env),
    fetchGitHubFile('messaging/brain.md', env),
    fetchGitHubFile('skills/skills/product-update-vs-website/SKILL.md', env),
    fetchGitHubFile('messaging/tone.md', env),
    fetchGitHubFile('messaging/terminology.md', env),
    fetchGitHubFile('messaging/positioning.md', env),
    fetchGitHubFile('messaging/boilerplates.md', env),
    fetchGitHubFile('messaging/narrative.md', env),
    fetchGitHubFile('messaging/value-story.md', env),
  ]);

  if (!marketingPages || !skillMd) {
    throw new Error('Failed to fetch required files from GitHub');
  }

  const combinedSiteContent = JSON.stringify({
    _meta: { note: 'Marketing pages + use cases combined for gap analysis' },
    pages: [
      ...(JSON.parse(marketingPages).pages || []),
      ...(useCasesPages ? (JSON.parse(useCasesPages).pages || []) : []),
    ],
  }, null, 2);

  const brandGuidelines = [
    mainBrain && `## Main Brain (routing & compliance)\n${mainBrain}`,
    messagingBrain && `## Messaging Router\n${messagingBrain}`,
    toneMd && `## Tone\n${toneMd}`,
    terminologyMd && `## Terminology\n${terminologyMd}`,
    positioningMd && `## Positioning\n${positioningMd}`,
    boilerplatesMd && `## Boilerplates\n${boilerplatesMd}`,
    narrativeMd && `## Narrative\n${narrativeMd}`,
    valueStoryMd && `## Value Story\n${valueStoryMd}`,
  ].filter(Boolean).join('\n\n');

  const prompt = `You are analyzing a new ${type} for social.plus to identify gaps in the marketing website.

## Skill instructions (follow these exactly)
${skillMd}

## Brand messaging guidelines (apply to all suggested copy)
${brandGuidelines}

## Current website content (JSON — includes both static marketing pages AND use case pages)
${combinedSiteContent}

## New ${type} to analyze
Name: ${itemName}
${introText ? `Description: ${introText}` : ''}

IMPORTANT formatting rules for this automated report:
- Page URLs in the JSON are already fully-qualified (https://www.social.plus/...). Use them as-is in report links.
- Output the report in both plain text AND HTML format
- For the HTML version, wrap each gap in a styled div with the priority color as left border
- Keep the same structure defined in the SKILL.md
- Run the compliance check from brain.md before finalizing the report

Now analyze the ${type} and produce the gap report.`;

  const anthropicRes = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': env.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4096,
      messages: [{ role: 'user', content: prompt }],
    }),
  });

  if (!anthropicRes.ok) {
    const err = await anthropicRes.text();
    throw new Error(`Anthropic API error: ${anthropicRes.status} ${err}`);
  }

  const result = await anthropicRes.json();
  return result.content[0].text;
}

function splitReport(report) {
  const htmlMarker = report.indexOf('<div');
  if (htmlMarker > 0) {
    return {
      plainText: report.substring(0, htmlMarker).trim(),
      html: report.substring(htmlMarker).trim(),
    };
  }
  return {
    plainText: report,
    html: `<div style="font-family: -apple-system, Arial, sans-serif; line-height: 1.6;">${report.replace(/\n/g, '<br>')}</div>`,
  };
}

async function sendToMake(type, itemName, itemSlug, introText, report, env) {
  const { plainText, html } = splitReport(report);
  const itemUrl = itemSlug
    ? `${SITE_BASE_URL}/${type === 'Release Note' ? 'release-note' : 'product-update'}/${itemSlug}`
    : '';

  const payload = {
    type,
    itemName,
    itemUrl,
    introText: introText || '',
    gapReport: plainText,
    gapReportHtml: html,
    timestamp: new Date().toISOString(),
  };

  const res = await fetch(env.MAKE_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    console.error(`Make.com webhook failed: ${res.status}`);
  }
  return payload;
}

// ─── Regen dispatcher ────────────────────────────────────────────────────────

const GENERATORS = {
  marketing: { fn: generateMarketingPagesJSON, path: FILES.marketing },
  'use-cases': { fn: generateUseCasesJSON, path: FILES.useCases },
  blog: { fn: generateBlogJSON, path: FILES.blog },
  glossary: { fn: generateGlossaryJSON, path: FILES.glossary },
  answers: { fn: generateAnswersJSON, path: FILES.answers },
  'customer-stories': { fn: generateCustomerStoriesJSON, path: FILES.customerStories },
  'release-notes': { fn: generateReleaseNotesJSON, path: FILES.releaseNotes },
  'product-updates': { fn: generateProductUpdatesJSON, path: FILES.productUpdates },
  webinars: { fn: generateWebinarsJSON, path: FILES.webinars },
};

async function regenerate(target, env) {
  const g = GENERATORS[target];
  if (!g) throw new Error(`Unknown generate target: ${target}`);
  const json = await g.fn(env);
  return commitToGitHub(json, env, g.path);
}

async function regenerateAll(env) {
  const results = {};
  for (const target of Object.keys(GENERATORS)) {
    try {
      results[target] = await regenerate(target, env);
    } catch (err) {
      results[target] = { error: err.message };
    }
  }
  return results;
}

// ─── Request handler ─────────────────────────────────────────────────────────

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // ── GET /generate/:target ──
    const generateMatch = path.match(/^\/generate\/([a-z-]+)$/);
    if (generateMatch && request.method === 'GET') {
      if (!checkAuth(request, env)) return new Response('Unauthorized', { status: 401 });
      const target = generateMatch[1];

      if (target === 'all') {
        try {
          const results = await regenerateAll(env);
          return Response.json({ ok: true, results });
        } catch (err) {
          return Response.json({ ok: false, error: err.message }, { status: 500 });
        }
      }

      if (!GENERATORS[target]) {
        return Response.json(
          { ok: false, error: `Unknown target: ${target}` },
          { status: 404 }
        );
      }

      try {
        const g = GENERATORS[target];
        const json = await g.fn(env);
        const result = await commitToGitHub(json, env, g.path);
        return Response.json({
          ok: true,
          target,
          items: json._meta.itemCount,
          sizeKB: Math.round(JSON.stringify(json).length / 1024),
          ...result,
        });
      } catch (err) {
        return Response.json({ ok: false, error: err.message }, { status: 500 });
      }
    }

    // ── POST /webhook/publish — Webflow site publish ──
    if (path === '/webhook/publish' && request.method === 'POST') {
      ctx.waitUntil(
        (async () => {
          try {
            await regenerate('marketing', env);
          } catch (err) {
            console.error('Publish webhook error:', err.message);
          }
        })()
      );
      return new Response('OK', { status: 200 });
    }

    // ── POST /webhook/cms-published — Webflow CMS item published ──
    if (path === '/webhook/cms-published' && request.method === 'POST') {
      const payload = await request.json();
      const item = payload.payload?.items?.[0] || {};
      const collectionId = item.collectionId || null;

      if (!collectionId) {
        return new Response('OK — no collectionId', { status: 200 });
      }

      const isReleaseNote = collectionId === env.RELEASE_NOTES;
      const isProductUpdate = collectionId === env.PRODUCT_UPDATES;
      const isUseCase = collectionId === env.USE_CASES;
      const isBlog = collectionId === env.BLOG;
      const isGlossary = collectionId === env.GLOSSARY;
      const isAnswer = collectionId === env.ANSWERS;
      const isCustomerStory = collectionId === env.CUSTOMER_STORIES;
      const isWebinar = collectionId === env.WEBINARS;

      // Recognized collections fall into two groups:
      //   - Inventory-only:   use-cases, blog, glossary, answers, customer-stories, webinars
      //   - Inventory + gap analysis:  release-notes, product-updates
      const recognized = isReleaseNote || isProductUpdate || isUseCase || isBlog
        || isGlossary || isAnswer || isCustomerStory || isWebinar;

      if (!recognized) {
        return new Response('OK — ignored collection', { status: 200 });
      }

      // Inventory regen first — applies to ALL recognized collections, including
      // release-notes/product-updates so their inventory files stay fresh too.
      const inventoryTarget =
        isUseCase ? 'use-cases' :
        isBlog ? 'blog' :
        isGlossary ? 'glossary' :
        isAnswer ? 'answers' :
        isCustomerStory ? 'customer-stories' :
        isWebinar ? 'webinars' :
        isReleaseNote ? 'release-notes' :
        isProductUpdate ? 'product-updates' :
        null;

      // Inventory-only paths return immediately after queuing regen.
      if (!isReleaseNote && !isProductUpdate) {
        ctx.waitUntil(
          (async () => {
            try {
              await regenerate(inventoryTarget, env);
            } catch (err) {
              console.error(`${inventoryTarget} regen error: ${err.message}`);
            }
          })()
        );
        return new Response(`OK — ${inventoryTarget} regen queued`, { status: 200 });
      }

      // Release-notes / product-updates: regen inventory AND run gap analysis.
      // Queue the inventory regen first, then fall through to the dedup + gap-analysis flow below.
      ctx.waitUntil(
        (async () => {
          try {
            await regenerate(inventoryTarget, env);
          } catch (err) {
            console.error(`${inventoryTarget} regen error: ${err.message}`);
          }
        })()
      );

      // Release notes / product updates → dedup + gap analysis
      const itemId = item.id || 'unknown';
      const cache = caches.default;
      const dedupKey = new Request(`https://dedup.internal/${collectionId}/${itemId}`);
      if (await cache.match(dedupKey)) {
        return new Response('OK — dedup skipped', { status: 200 });
      }
      await cache.put(dedupKey, new Response('processed', {
        headers: { 'Cache-Control': 'public, max-age=86400' },
      }));

      const type = isReleaseNote ? 'Release Note' : 'Monthly Product Update';
      const fd = item.fieldData || {};
      const itemName = fd.name || fd.title || 'Unknown';
      const itemSlug = fd.slug || '';
      const introText = fd['post-summary'] || fd['meta-description'] || fd['intro-text']
        || fd.summary || fd.description || '';

      ctx.waitUntil(
        (async () => {
          try {
            const report = await runGapAnalysis(itemName, itemSlug, introText, type, env);
            await sendToMake(type, itemName, itemSlug, introText, report, env);
          } catch (err) {
            console.error(`Gap analysis error: ${err.message}`);
          }
        })()
      );

      return new Response('OK — processing', { status: 200 });
    }

    // ── Fallback: minimal 200, no route disclosure ──
    return new Response('cruciate-hub-site-json\n', {
      status: 200,
      headers: { 'Content-Type': 'text/plain' },
    });
  },
};
