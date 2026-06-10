# Blog Publisher — Improvements Backlog

Captured from live test runs publishing Listicle 1 and Listicle 2 (June 2026).
Ordered by impact. Items marked ✅ are done; the rest are open.

## Resolved from field feedback (hero-image refresh run, June 2026)

A separate session used the skill for an image-refresh job on 5 live posts and filed
11 findings. All folded in (v13.2):

- ✅ **`--update <item_id>` mode** — the refresh path (re-upload 3 heroes → partial
  PATCH of only the image fields → publish) is now one command instead of hand-rolled.
  Verifies via filename suffix, not URL equality (Webflow re-ingests under a new fileId
  on update — expected, not a failure).
- ✅ **Timeouts everywhere** — a run without timeouts once hung 45 minutes. `http()`
  now defaults to 30s (60s for the S3 upload) and exits with an error on timeout.
- ✅ **Pillow is the resize path, never sips/ffmpeg** — `scripts/resize_blog_images.py`
  (validates ≥1578px + ~16:9, emits all exact sizes). sips can't write WebP on macOS;
  ffmpeg often lacks libwebp. The "stdlib only" claim now applies to blog-publisher.py;
  the resize helper declares Pillow and fails with install instructions if absent.
- ✅ **Webflow MCP documented as the no-token fallback** — create_asset → S3 (camelCase
  key mapping gotcha: xAmzAlgorithm→X-Amz-Algorithm etc., file part last, success=201)
  → update/publish_collection_items. In SKILL.md + image-pipeline.md.
- ✅ **Drive sourcing notes** — large files arrive as base64 sidecar .txt (verify
  RIFF…WEBP magic); direct drive.google.com/uc curl fails for non-shared files;
  designer folders are titled by blog TITLE not slug (match via slug lookup);
  `*_open-graph.webp` has no CMS field.
- ✅ **Exact-dimension enforcement documented** (min=max validation; API rejects
  off-size) and gated in --update before any upload.
- ✅ **/tmp non-persistence noted** — single-run files in $TMPDIR are fine; anything
  reusable goes in a stable path.

## Resolved via the skill-creator eval pass (iteration 1 → 2)

- ✅ **No `<style>` block in post-content.** Reverted the earlier "table style block"
  idea. The Data API preserves `<style>`, but Webflow's RichText renderer shows the CSS
  as literal text at the top of the published post. Table CSS now lives in the site's
  custom code (reference CSS kept in `html-conversion.md`); the helper emits clean
  `<table>` markup only. New dry-run gate `content:no-style-block` enforces it.
  (Caught by the user reviewing the live post.)

- ✅ **alt-text over-capture fixed.** Two independent eval subagents found that when the
  doc puts `Image alt text:` / `Image concept:` / `Image sizes needed:` on one physical
  line (L1 and L3 do), the helper grabbed all three into `image-alt-text`. Now cut at the
  next label. Validated: L1/L3 clean, L2 correctly empty (no fabrication).

- ✅ **Script paths made explicit.** SKILL.md now always invokes `$REPO/scripts/...`
  (the scripts live at repo root, not in the skill folder). An eval agent flagged the
  ambiguity.

- ✅ **`--dry-run` validation gate added.** Side-effect-free check of the whole payload
  (fields, slug-no-year, table-not-flattened, no-style-block, placeholder/inline match,
  exact image dims). Exits non-zero on failure; writes dry-run-report.json. This is what
  caught the flattened-table regression in testing.

## Resolved during testing

- ✅ **Image URL must be the S3 hostedUrl, not a constructed CDN URL.**
  `cdn.prod.website-files.com/...` URLs built by hand return 403 and Webflow
  silently drops the image field. The correct value is
  `https://s3.amazonaws.com/{bucket}/{key}`, built from `uploadDetails.bucket`
  and `uploadDetails.key` in the asset-register response — no extra GET needed.
  When passed to a CMS Image field, Webflow re-hosts on CDN and returns a real fileId.

- ✅ **Bulk endpoint DOES persist image fields** (once the URL is a valid S3 URL).
  The earlier "bulk drops images" theory was wrong — it was the 403 URLs.
  The separate auto-patch step is unnecessary and was removed.

- ✅ **sips WebP output is broken on macOS 26.** Use Pillow:
  `Image.open(p).convert("RGB").resize((w,h), Image.LANCZOS).save(out, "WEBP", quality=90)`.
  Pillow is the primary path; sips is a fallback only on older macOS.

- ✅ **Never put the year in a slug** — HARD RULE, promoted to a NON-NEGOTIABLE
  section at the top of SKILL.md. Applies to title-derived slugs, `--slug` overrides,
  AND collision resolution (never append a year to dodge a "slug exists" 400).
  `gdoc_to_fielddata.py` strips `19xx`/`20xx` tokens automatically (validated against
  edge cases — `top-1000-apps` and `4000-users` survive; only real years are removed).
  Regression: the first Listicle 1 publish appended `-2026` to resolve a collision —
  exactly the forbidden move. The rule is now loud enough that it can't be missed.

## Open — high impact

1. **Pre-flight slug check before uploading anything.**
   The Listicle 1 run uploaded all 9 images, THEN hit a 400 slug collision —
   wasting 9 uploads. Check `GET /collections/{id}/items?slug={slug}` first.
   If taken, stop and ask before touching images. Fail fast.

2. **Pre-flight token-scope check.**
   Two of the three tokens supplied during testing had wrong scopes
   (missing `sites:read` / `assets:write`), discovered only mid-run.
   One cheap `GET /sites/{id}` up front confirms the token works before
   the pipeline starts.

3. ✅ **HTML conversion moved into a committed helper script.**
   `scripts/gdoc_to_fielddata.py` takes the raw doc text + listicle number and
   emits `fielddata.json` — metadata extraction, HTML conversion, category
   mapping, year-stripped slug, and `__INLINE_IMG_N__` insertion. Validated to
   byte-match the hand-written output for Listicle 1 and 2 (17,618 / 16,380 chars).
   Handles both `Image alt text:` and `**Image alt text:**`, skips OUTREACH/INTERNAL
   blocks, and warns on empty meta/summary/alt fields. SKILL Phase 2 now calls it.

4. ✅ **Dropped the `requests` dependency** (done).
   `blog-publisher.py` now uses stdlib `urllib` only — no `pip install`, no venv, runs
   anywhere with Python 3. The S3 upload's multipart/form-data body is hand-built (file
   part last, as S3's POST policy requires). Verified end-to-end on the *system* python3
   (which has no `requests`): dry-run 36/36, and a real staged upload+create attached the
   image and embedded the figure correctly (test item then deleted). Matters because this
   is a skill other people run — zero setup.

## Open — medium impact

5. **Webflow dedupes assets by fileHash.**
   Reused images (identical bytes across posts) return the existing asset with
   its *original* filename. Functionally fine (same image), but the asset library
   name won't match the new post's slug. Either accept it or append a per-post
   salt to force distinct assets. Document the behavior either way.

6. **Slug collision after delete is permanent until site publish.**
   Deleting a live item via API reserves its slug until the next *site* publish
   clears the tombstone. So a re-stage with the same slug fails with 400 until
   then. The skill should never delete-then-recreate; prefer staging a new item
   or updating in place.

7. ✅ **Robust internal-link insertion** (done).
   `scripts/apply_internal_links.py` places the strategist's suggestions
   deterministically: it locates each `insert_at` sentence with WHITESPACE-FLEXIBLE
   matching (the exact-match drift that dropped 2 of 7 before), then wraps the anchor
   there or swaps in the rephrase. Never links inside headings or the comparison-table
   embed; reports any genuinely unplaceable link instead of forcing a bad edit. SKILL
   Phase 3 now builds a `links.json` and calls it; the `--dry-run` gate
   `content:has-internal-links` catches a skipped Phase 3. Verified 6/7 on a real L2
   set (the 7th was a deliberately impossible anchor) with zero links in protected regions.

## Open — low impact / polish

8. **`itemId` reporting** — bulk response is `{"items":[...]}`, so the top-level
   `result.get("id")` returned empty in the final JSON even on success. Fixed via
   `_extract_item()`, but worth a regression check.

9. **Cache the Google Doc read.** Each `read_file_content` on the doc is ~58KB.
   For multi-listicle docs, read once to a local file and slice per listicle.

## Net effect if items 1–4 land

- One pre-flight call replaces 9 wasted uploads on a slug clash.
- Zero-dependency script runs anywhere with system Python.
- HTML conversion stops being regenerated every run (the single biggest
  token cost across these test sessions).
