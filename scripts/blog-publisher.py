#!/usr/bin/env python3
"""
blog-publisher.py — Upload images and publish a blog post to Webflow CMS live.

Usage:
    python3 scripts/blog-publisher.py <fielddata.json> <header.webp> <grid.webp> <menu.webp> [img-1.webp ...] [--staged]

Environment:
    WEBFLOW_API_TOKEN  —  Webflow API token with cms:write + assets:write scopes.

Outputs (stdout):
    JSON: { "itemId": "...", "slug": "...", "liveUrl": "https://www.social.plus/blog/..." }
"""

import hashlib
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
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


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 5:
        print("Usage: python3 blog-publisher.py <fielddata.json> <header.webp> <grid.webp> <menu.webp> [img-1.webp ...] [--staged]", file=sys.stderr)
        sys.exit(1)

    all_args    = sys.argv[1:]
    staged_mode = "--staged" in all_args
    all_args    = [a for a in all_args if a != "--staged"]

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
