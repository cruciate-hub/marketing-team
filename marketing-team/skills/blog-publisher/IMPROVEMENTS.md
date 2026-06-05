# Blog Publisher — Improvements Backlog

Captured from live test runs publishing Listicle 1 and Listicle 2 (June 2026).
Ordered by impact. Items marked ✅ are done; the rest are open.

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

4. **Drop the `requests` dependency.**
   `requests` isn't installed by default and the externally-managed Python on
   macOS blocks `pip install`, forcing a venv. Rewriting the script on stdlib
   `urllib.request` removes that whole friction class — no venv, no install.

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

7. **Robust internal-link insertion.**
   The strategist returns "Insert at: <verbatim sentence>" but 2 of 7 anchors
   for Listicle 2 didn't match the converted HTML verbatim (punctuation/spacing
   drift), so they were skipped on the first pass. Either have the strategist
   return the full edited post-content, or insert against a normalized copy.

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
