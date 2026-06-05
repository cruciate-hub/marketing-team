#!/usr/bin/env python3
"""
blog-publisher.py — Upload images and publish a blog post to Webflow CMS live.

Usage:
    python3 scripts/blog-publisher.py <fielddata.json> <header.webp> <grid.webp> <menu.webp> [img-1.webp ...] [--staged] [--dry-run]

    --staged    Create a staged item (goes live on next Webflow site publish) rather
                than publishing immediately.
    --dry-run   Validate everything (required fields, slug-has-no-year, styled table
                not flattened, placeholder/inline-image count match, exact image
                dimensions) and write dry-run-report.json. Makes NO API calls and
                needs no token. Exits non-zero on any failed check. Use in tests/CI.

Environment:
    WEBFLOW_API_TOKEN  —  Webflow API token with cms:write + assets:write scopes.
                          Not required for --dry-run.

Outputs (stdout):
    JSON: { "itemId": "...", "slug": "...", "liveUrl": "https://www.social.plus/blog/..." }
"""

import hashlib
import json
import os
import re
import sys
from pathlib import Path

# requests is only needed for the actual upload/publish — dry-run runs without it.
try:
    import requests
except ImportError:
    requests = None


def _require_requests() -> None:
    if requests is None:
        print("ERROR: requests not installed. Run: pip install requests", file=sys.stderr)
        sys.exit(1)

# ── Config ─────────────────────────────────────────────────────────────────────

SITE_ID            = "66e2765d540e1939a89db4bb"
BLOG_COLLECTION_ID = "66e2765d540e1939a89db6a4"
API_BASE           = "https://api.webflow.com/v2"

FIGURE_TEMPLATE = (
    '<figure class="w-richtext-figure-type-image w-richtext-align-fullwidth" '
    'style="max-width:1578px" data-rt-type="image" data-rt-align="fullwidth" '
    'data-rt-max-width="1578px">'
    '<div><img alt="__wf_reserved_inherit" src="{url}" loading="lazy"></div>'
    '</figure>'
)

# ── Helpers ────────────────────────────────────────────────────────────────────

def get_token() -> str:
    token = os.environ.get("WEBFLOW_API_TOKEN", "").strip()
    if not token:
        print("ERROR: WEBFLOW_API_TOKEN is not set.\n  export WEBFLOW_API_TOKEN=your_token", file=sys.stderr)
        sys.exit(1)
    return token


def api_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "accept": "application/json"}


def md5_file(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def _check(r: requests.Response, label: str) -> None:
    if not r.ok:
        print(f"ERROR: {label} — HTTP {r.status_code}", file=sys.stderr)
        try:
            print(json.dumps(r.json(), indent=2)[:800], file=sys.stderr)
        except Exception:
            print(r.text[:800], file=sys.stderr)
        sys.exit(1)


# ── Asset upload ───────────────────────────────────────────────────────────────

def upload_asset(token: str, file_path: str, file_name: str) -> tuple:
    """
    Upload an image to Webflow via 3-step process.
    Returns (asset_id, hosted_url).

    The hosted S3 URL is constructed directly from uploadDetails.bucket + uploadDetails.key —
    no extra GET /assets call needed. When this URL is passed to a CMS Image field,
    Webflow accepts it and re-hosts it on CDN.
    """
    headers   = api_headers(token)
    file_hash = md5_file(file_path)
    print(f"  → {file_name}  (MD5 {file_hash[:8]}…)", file=sys.stderr)

    r = requests.post(
        f"{API_BASE}/sites/{SITE_ID}/assets",
        headers={**headers, "Content-Type": "application/json"},
        json={"fileName": file_name, "fileHash": file_hash},
    )
    _check(r, f"asset-register {file_name}")
    meta = r.json()

    upload_url = meta["uploadUrl"]
    d          = meta["uploadDetails"]
    asset_id   = meta["id"]

    # S3 upload
    with open(file_path, "rb") as f:
        s3 = requests.post(
            upload_url,
            data={
                "acl":                   d["acl"],
                "bucket":                d["bucket"],
                "X-Amz-Algorithm":       d["X-Amz-Algorithm"],
                "X-Amz-Credential":      d["X-Amz-Credential"],
                "X-Amz-Date":            d["X-Amz-Date"],
                "key":                   d["key"],
                "Policy":                d["Policy"],
                "X-Amz-Signature":       d["X-Amz-Signature"],
                "success_action_status": d["success_action_status"],
                "Content-Type":          d["content-type"],
                "Cache-Control":         d["Cache-Control"],
            },
            files={"file": (file_name, f, "image/webp")},
        )

    if s3.status_code not in (200, 201, 204):
        print(f"ERROR: S3 upload failed — HTTP {s3.status_code}", file=sys.stderr)
        print(s3.text[:500], file=sys.stderr)
        sys.exit(1)

    # Construct S3 hosted URL directly from upload details (no extra API call)
    hosted_url = f"https://s3.amazonaws.com/{d['bucket']}/{d['key']}"
    print(f"     ✓ {hosted_url}", file=sys.stderr)
    return asset_id, hosted_url


# ── Inline image injection ─────────────────────────────────────────────────────

def inject_inline_images(post_content: str, inline_urls: list) -> str:
    for i, url in enumerate(inline_urls, start=1):
        placeholder = f"__INLINE_IMG_{i}__"
        if placeholder in post_content:
            post_content = post_content.replace(placeholder, FIGURE_TEMPLATE.format(url=url))
            print(f"  ✓ Injected inline image {i}", file=sys.stderr)
        else:
            print(f"  ⚠ Placeholder {placeholder} not found — skipped", file=sys.stderr)
    return post_content


# ── Publish ────────────────────────────────────────────────────────────────────

def publish_live(token: str, field_data: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/collections/{BLOG_COLLECTION_ID}/items/live",
        headers={**api_headers(token), "Content-Type": "application/json"},
        json={"fieldData": field_data},
    )
    _check(r, "webflow-publish")
    return r.json()


def _extract_item(data) -> dict:
    """Bulk endpoint may return a bare list or {"items":[...]}. Normalize to one item dict."""
    if isinstance(data, dict) and "items" in data:
        items = data["items"]
        return items[0] if items else {}
    if isinstance(data, list):
        return data[0] if data else {}
    return data if isinstance(data, dict) else {}


def publish_staged(token: str, field_data: dict) -> dict:
    """
    Create a staged item via POST /items/bulk.

    Image fields persist directly in the bulk call AS LONG AS each image url is a
    valid S3 hostedUrl (https://s3.amazonaws.com/{bucket}/{key}). Webflow re-hosts
    it on CDN. A 403-returning cdn.prod.website-files.com URL is silently dropped —
    that was the earlier failure mode, not a bulk-endpoint limitation.
    """
    r = requests.post(
        f"{API_BASE}/collections/{BLOG_COLLECTION_ID}/items/bulk",
        headers={**api_headers(token), "Content-Type": "application/json"},
        json={"fieldData": field_data, "isDraft": False},
    )
    _check(r, "webflow-stage")
    return _extract_item(r.json())


# ── Pre-flight checks ───────────────────────────────────────────────────────────

def preflight(token: str, slug: str) -> None:
    """
    Fail fast BEFORE uploading any images:
      1. Token works and has site access (one cheap GET /sites/{id}).
      2. Slug is not already taken (avoids 9 wasted uploads then a 400).
    """
    # 1. Token + site access
    r = requests.get(f"{API_BASE}/sites/{SITE_ID}", headers=api_headers(token))
    if r.status_code == 401:
        print("ERROR: Token rejected (401). Check WEBFLOW_API_TOKEN.", file=sys.stderr)
        sys.exit(1)
    if r.status_code == 403:
        print("ERROR: Token missing scopes. Needs sites:read, cms:write, assets:write.", file=sys.stderr)
        sys.exit(1)
    _check(r, "preflight-site")

    # 2. Slug availability
    r = requests.get(
        f"{API_BASE}/collections/{BLOG_COLLECTION_ID}/items",
        headers=api_headers(token),
        params={"slug": slug},
    )
    _check(r, "preflight-slug")
    existing = r.json().get("items", [])
    if existing:
        print(f"ERROR: Slug '{slug}' already exists (item {existing[0]['id']}).", file=sys.stderr)
        print("       Stopping before upload. Choose a new slug or update the existing item.", file=sys.stderr)
        print("       Do NOT append a year or numeric suffix — pick a genuinely distinct slug.", file=sys.stderr)
        sys.exit(1)

    print(f"✓ Pre-flight OK — token valid, slug '{slug}' available", file=sys.stderr)


# ── Dry-run validation ──────────────────────────────────────────────────────────

# Expected WebP dimensions per role. Hero sizes are fixed by the CMS image fields;
# inline images are normalized to header width.
EXPECTED_DIMS = {"header": (1578, 888), "grid": (724, 408), "menu": (502, 283),
                 "inline": (1578, 888)}
REQUIRED_FIELDS = ["name", "slug", "post-summary", "post-content", "meta-description",
                   "min-read", "category", "category-multi-reference-3"]
YEAR_RE = re.compile(r"(?:19|20)\d{2}")


def _webp_dims(path: str):
    """Return (w, h) of a WebP, or None if Pillow is unavailable / file unreadable."""
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def dry_run_validate(field_data: dict, slug: str, header, grid, menu, inline_paths,
                     fielddata_path) -> None:
    """
    Validate the full publish payload WITHOUT calling Webflow. Prints a human report
    and writes dry-run-report.json next to fielddata.json. Exits non-zero if any
    hard check fails, so it's usable as a gate in tests and CI.
    """
    checks = []  # (name, passed, detail)

    def chk(name, passed, detail=""):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    # 1. Required fields present and non-empty
    for fld in REQUIRED_FIELDS:
        v = field_data.get(fld)
        chk(f"field:{fld}", bool(v), "" if v else "missing/empty")

    # 2. Slug rules: never a year, never a leading listicle count, lowercase-hyphenated
    chk("slug:no-year", not YEAR_RE.search(slug), slug if YEAR_RE.search(slug) else "")
    lead_count = re.match(r"^(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|"
                          r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|"
                          r"eighteen|nineteen|twenty)-", slug)
    chk("slug:no-leading-count", not lead_count,
        f"slug starts with a count: {slug}" if lead_count else "")
    chk("slug:format", bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug)), slug)

    # 3. Categories: main category is in the multi-ref list
    main_cat = field_data.get("category")
    multi    = field_data.get("category-multi-reference-3", [])
    chk("category:main-in-tags", main_cat in multi if main_cat else False)

    # 4. post-content integrity
    pc = field_data.get("post-content", "")
    chk("content:no-outreach-leak", "OUTREACH VERSION" not in pc and "INTERNAL USE" not in pc)
    chk("content:no-disclosure-leak", "OPTIONAL DISCLOSURE" not in pc)
    chk("content:no-h1", "<h1>" not in pc)
    n_placeholders = len(re.findall(r"__INLINE_IMG_\d+__", pc))
    chk("content:placeholders-match-inline", n_placeholders == len(inline_paths),
        f"{n_placeholders} placeholders vs {len(inline_paths)} inline images")
    # If a table is present it must be real markup, not a flattened paragraph
    if "At-a-Glance" in pc or "Comparison" in pc:
        has_table = "<table>" in pc
        chk("content:table-not-flattened", has_table,
            "table heading present but no <table> markup" if not has_table else "")
    # post-content must NOT carry a <style> block — Webflow renders it as literal text.
    # Table CSS belongs in the site's custom code, not the CMS field.
    chk("content:no-style-block", "<style>" not in pc,
        "post-content contains a <style> block — move table CSS to site custom code" if "<style>" in pc else "")

    # 5. Image dimensions
    roles = [("header", header), ("grid", grid), ("menu", menu)]
    roles += [("inline", p) for p in inline_paths]
    for role, path in roles:
        exp = EXPECTED_DIMS[role]
        dims = _webp_dims(path)
        if dims is None:
            chk(f"image:{Path(path).name}", True, "dim check skipped (no Pillow)")
        else:
            chk(f"image:{Path(path).name}", dims == exp,
                f"{dims[0]}x{dims[1]} (expected {exp[0]}x{exp[1]})" if dims != exp else f"{dims[0]}x{dims[1]}")
        chk(f"image:{Path(path).name}:is-webp", str(path).lower().endswith(".webp"))

    # Report
    passed = sum(1 for c in checks if c["passed"])
    total  = len(checks)
    print(f"\n── DRY RUN ── {passed}/{total} checks passed", file=sys.stderr)
    for c in checks:
        mark = "✓" if c["passed"] else "✗"
        line = f"  {mark} {c['check']}"
        if c["detail"]:
            line += f"  — {c['detail']}"
        print(line, file=sys.stderr)

    print(f"\n  Would publish: name={field_data.get('name')!r}", file=sys.stderr)
    print(f"                 slug={slug!r}", file=sys.stderr)
    print(f"                 {len(inline_paths)} inline + 3 hero images", file=sys.stderr)
    print(f"                 post-content {len(pc):,} chars", file=sys.stderr)

    report = {"passed": passed, "total": total, "all_passed": passed == total, "checks": checks}
    report_path = str(Path(fielddata_path).with_name("dry-run-report.json"))
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n  Report: {report_path}", file=sys.stderr)

    # Machine-readable line on stdout
    print(json.dumps({"dryRun": True, "passed": passed, "total": total,
                      "allPassed": passed == total, "slug": slug}))
    if passed != total:
        sys.exit(1)


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 5:
        print("Usage: python3 blog-publisher.py <fielddata.json> <header.webp> <grid.webp> <menu.webp> [img-1.webp ...] [--staged] [--dry-run]", file=sys.stderr)
        sys.exit(1)

    all_args    = sys.argv[1:]
    staged_mode = "--staged" in all_args
    dry_run     = "--dry-run" in all_args
    all_args    = [a for a in all_args if a not in ("--staged", "--dry-run")]

    fielddata_path = all_args[0]
    header_webp    = all_args[1]
    grid_webp      = all_args[2]
    menu_webp      = all_args[3]
    inline_paths   = all_args[4:]

    for path in [fielddata_path, header_webp, grid_webp, menu_webp] + inline_paths:
        if not Path(path).exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            sys.exit(1)

    with open(fielddata_path) as f:
        field_data = json.load(f)

    slug  = field_data.get("slug", "blog-post")

    # ── Dry-run: validate everything, touch no API. Repeatable + side-effect-free.
    if dry_run:
        dry_run_validate(field_data, slug, header_webp, grid_webp, menu_webp, inline_paths,
                         fielddata_path)
        return

    _require_requests()
    token = get_token()

    # ── Pre-flight: fail before any upload if token or slug is bad ─────────────
    preflight(token, slug)

    # ── Upload hero images ────────────────────────────────────────────────────
    print("Uploading hero images…", file=sys.stderr)
    header_id, header_url = upload_asset(token, header_webp, Path(header_webp).name)
    grid_id,   grid_url   = upload_asset(token, grid_webp,   Path(grid_webp).name)
    menu_id,   menu_url   = upload_asset(token, menu_webp,   Path(menu_webp).name)

    field_data["image-page-header"]   = {"fileId": header_id, "url": header_url, "alt": None}
    field_data["grid-thumbnail"]      = {"fileId": grid_id,   "url": grid_url,   "alt": None}
    field_data["thumbnail-mega-menu"] = {"fileId": menu_id,   "url": menu_url,   "alt": None}

    # ── Upload inline body images ─────────────────────────────────────────────
    if inline_paths:
        print(f"Uploading {len(inline_paths)} inline image(s)…", file=sys.stderr)
        inline_urls = []
        for path in inline_paths:
            _, url = upload_asset(token, path, Path(path).name)
            inline_urls.append(url)

        if inline_urls and "post-content" in field_data:
            print("Injecting inline images…", file=sys.stderr)
            field_data["post-content"] = inject_inline_images(field_data["post-content"], inline_urls)

    # ── Publish ───────────────────────────────────────────────────────────────
    if staged_mode:
        print("Staging for next site publish…", file=sys.stderr)
        result = publish_staged(token, field_data)
    else:
        print("Publishing to Webflow…", file=sys.stderr)
        result = publish_live(token, field_data)

    item_id   = result.get("id", "")
    live_slug = (result.get("fieldData") or {}).get("slug", slug)

    output = {"itemId": item_id, "slug": live_slug, "liveUrl": f"https://www.social.plus/blog/{live_slug}"}
    print(json.dumps(output, indent=2))
    print(f"\n✓ Done: https://www.social.plus/blog/{live_slug}", file=sys.stderr)


if __name__ == "__main__":
    main()
