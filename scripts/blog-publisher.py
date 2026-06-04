#!/usr/bin/env python3
"""
blog-publisher.py — Upload images and publish a blog post to Webflow CMS live.

Usage:
    python3 scripts/blog-publisher.py <fielddata.json> <header.webp> <grid.webp> <menu.webp> [img-1.webp img-2.webp ...]

    Required args:
        fielddata.json  — CMS field data; post-content may contain __INLINE_IMG_1__ … __INLINE_IMG_N__
                          placeholders that will be replaced with real CDN URLs before publish.
        header.webp     — Page header image (1578×888)
        grid.webp       — Grid thumbnail (724×408)
        menu.webp       — Mega menu thumbnail (502×283)

    Optional additional args (inline body images, in order):
        img-1.webp …    — Inline images for the post body, already converted to WebP.
                          Each replaces the corresponding __INLINE_IMG_N__ placeholder
                          in post-content. Pass them in the same order they appear in
                          the article (img-1 = first platform section, etc.).

Environment:
    WEBFLOW_API_TOKEN  —  Webflow API token with cms:write + assets:write scopes.

Outputs (stdout):
    JSON: { "itemId": "...", "slug": "...", "liveUrl": "https://www.social.plus/blog/..." }

Errors go to stderr; exits with code 1 on any failure.
"""

import hashlib
import json
import os
import sys
import urllib.parse
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

# CDN base confirmed from production CMS asset URLs.
# Pattern: https://cdn.prod.website-files.com/{SITE_ASSETS_CDN_ID}/{assetId}_{filename}
SITE_ASSETS_CDN_ID = "66e2765d540e1939a89db4e3"
CDN_BASE           = f"https://cdn.prod.website-files.com/{SITE_ASSETS_CDN_ID}"

# Webflow Rich Text figure template for inline images.
# max-width matches inline image width (1578px); alt is Webflow's standard placeholder.
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
        print("ERROR: WEBFLOW_API_TOKEN is not set.", file=sys.stderr)
        print("  export WEBFLOW_API_TOKEN=your_token", file=sys.stderr)
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
            detail = r.json()
            print(json.dumps(detail, indent=2)[:800], file=sys.stderr)
        except Exception:
            print(r.text[:800], file=sys.stderr)
        sys.exit(1)


# ── Asset upload ───────────────────────────────────────────────────────────────

def upload_asset(token: str, file_path: str, file_name: str) -> tuple:
    """
    Three-step Webflow asset upload.
    1. MD5 hash.
    2. POST /v2/sites/{siteId}/assets  →  S3 pre-signed URL + signing headers.
    3. POST file to S3 as image/webp.
    4. GET asset to retrieve hostedUrl.
    Returns (asset_id, hosted_url).
    """
    headers = api_headers(token)
    file_hash = md5_file(file_path)
    print(f"  → {file_name}  (MD5 {file_hash[:8]}…)", file=sys.stderr)

    # Register asset with Webflow
    r = requests.post(
        f"{API_BASE}/sites/{SITE_ID}/assets",
        headers={**headers, "Content-Type": "application/json"},
        json={"fileName": file_name, "fileHash": file_hash},
    )
    _check(r, f"asset-register {file_name}")
    meta = r.json()

    upload_url = meta["uploadUrl"]
    d = meta["uploadDetails"]
    asset_id = meta["id"]

    # Upload to S3
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

    # Construct CDN URL directly from the confirmed production pattern:
    # https://cdn.prod.website-files.com/{SITE_ASSETS_CDN_ID}/{assetId}_{encoded_filename}
    # (GET /v2/sites/{siteId}/assets/{assetId} does not exist in Webflow API v2)
    hosted_url = f"{CDN_BASE}/{asset_id}_{urllib.parse.quote(file_name, safe='')}"
    print(f"     ✓ {hosted_url}", file=sys.stderr)
    return asset_id, hosted_url


# ── Inline image injection ─────────────────────────────────────────────────────

def inject_inline_images(post_content: str, inline_urls: list) -> str:
    """
    Replace __INLINE_IMG_1__ … __INLINE_IMG_N__ placeholders in post_content
    with Webflow <figure> tags containing the real CDN URLs.
    Placeholders must be placed verbatim in post-content by the SKILL before
    this script runs (one per platform section, after the opening <h2> tag).
    """
    for i, url in enumerate(inline_urls, start=1):
        placeholder = f"__INLINE_IMG_{i}__"
        figure = FIGURE_TEMPLATE.format(url=url)
        if placeholder in post_content:
            post_content = post_content.replace(placeholder, figure)
            print(f"  ✓ Injected inline image {i}", file=sys.stderr)
        else:
            print(f"  ⚠ Placeholder {placeholder} not found in post-content — skipped", file=sys.stderr)
    return post_content


# ── Publish ────────────────────────────────────────────────────────────────────

def publish_live(token: str, field_data: dict) -> dict:
    """POST to /items/live — creates and immediately publishes the blog post."""
    r = requests.post(
        f"{API_BASE}/collections/{BLOG_COLLECTION_ID}/items/live",
        headers={**api_headers(token), "Content-Type": "application/json"},
        json={"fieldData": field_data},
    )
    _check(r, "webflow-publish")
    return r.json()


def publish_staged(token: str, field_data: dict) -> dict:
    """POST to /items/bulk — creates a staged item (goes live on next Webflow site publish)."""
    r = requests.post(
        f"{API_BASE}/collections/{BLOG_COLLECTION_ID}/items/bulk",
        headers={**api_headers(token), "Content-Type": "application/json"},
        json={"fieldData": field_data, "isDraft": False},
    )
    _check(r, "webflow-stage")
    # Bulk endpoint returns a list; take the first item
    data = r.json()
    if isinstance(data, list):
        return data[0] if data else {}
    return data


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 5:
        print(
            "Usage: python3 blog-publisher.py <fielddata.json> <header.webp> <grid.webp> <menu.webp> [img-1.webp ...] [--staged]",
            file=sys.stderr,
        )
        sys.exit(1)

    all_args     = sys.argv[1:]
    staged_mode  = "--staged" in all_args
    all_args     = [a for a in all_args if a != "--staged"]

    fielddata_path = all_args[0]
    header_webp    = all_args[1]
    grid_webp      = all_args[2]
    menu_webp      = all_args[3]
    inline_paths   = all_args[4:]  # optional, zero or more

    for path in [fielddata_path, header_webp, grid_webp, menu_webp] + inline_paths:
        if not Path(path).exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            sys.exit(1)

    with open(fielddata_path) as f:
        field_data = json.load(f)

    slug  = field_data.get("slug", "blog-post")
    token = get_token()

    # ── Upload hero images ────────────────────────────────────────────────────
    print("Uploading hero images…", file=sys.stderr)
    header_id, header_url = upload_asset(token, header_webp, Path(header_webp).name)
    grid_id,   grid_url   = upload_asset(token, grid_webp,   Path(grid_webp).name)
    menu_id,   menu_url   = upload_asset(token, menu_webp,   Path(menu_webp).name)

    # Production format: { fileId, url, alt: null }
    field_data["image-page-header"]   = {"fileId": header_id, "url": header_url, "alt": None}
    field_data["grid-thumbnail"]      = {"fileId": grid_id,   "url": grid_url,   "alt": None}
    field_data["thumbnail-mega-menu"] = {"fileId": menu_id,   "url": menu_url,   "alt": None}

    # ── Upload inline body images & inject into post-content ──────────────────
    if inline_paths:
        print(f"Uploading {len(inline_paths)} inline image(s)…", file=sys.stderr)
        inline_urls = []
        for path in inline_paths:
            _, url = upload_asset(token, path, Path(path).name)
            inline_urls.append(url)

        if "post-content" in field_data and inline_urls:
            print("Injecting inline images into post-content…", file=sys.stderr)
            field_data["post-content"] = inject_inline_images(
                field_data["post-content"], inline_urls
            )

    # ── Publish (live or staged) ──────────────────────────────────────────────
    if staged_mode:
        print("Staging for next site publish…", file=sys.stderr)
        result = publish_staged(token, field_data)
    else:
        print("Publishing to Webflow…", file=sys.stderr)
        result = publish_live(token, field_data)

    item_id   = result.get("id", "")
    live_slug = (result.get("fieldData") or {}).get("slug", slug)

    output = {
        "itemId":  item_id,
        "slug":    live_slug,
        "liveUrl": f"https://www.social.plus/blog/{live_slug}",
    }
    print(json.dumps(output, indent=2))
    print(f"\n✓ Published: https://www.social.plus/blog/{live_slug}", file=sys.stderr)


if __name__ == "__main__":
    main()
