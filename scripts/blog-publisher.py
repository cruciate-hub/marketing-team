#!/usr/bin/env python3
"""
blog-publisher.py — Upload images and publish a blog post to Webflow CMS live.

Usage:
    python3 scripts/blog-publisher.py <fielddata.json> <header.png> <grid.png> <menu.png>

Environment:
    WEBFLOW_API_TOKEN  —  Webflow API token with CMS read/write access

Outputs (stdout):
    JSON: { "itemId": "...", "slug": "...", "liveUrl": "https://www.social.plus/blog/..." }

Errors go to stderr; exits with code 1 on any failure.
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

def upload_asset(token: str, file_path: str, file_name: str) -> str:
    """
    Three-step Webflow asset upload.
    1. Compute MD5 hash.
    2. POST /v2/sites/{siteId}/assets  →  S3 pre-signed URL + signing headers.
    3. POST file to S3.
    4. GET asset to retrieve hostedUrl.
    Returns the public CDN URL.
    """
    headers = api_headers(token)
    file_hash = md5_file(file_path)
    print(f"  → {file_name}  (MD5 {file_hash[:8]}…)", file=sys.stderr)

    # Step 1: register with Webflow
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

    # Step 2: upload to S3
    with open(file_path, "rb") as f:
        s3 = requests.post(
            upload_url,
            data={
                "acl":                  d["acl"],
                "bucket":               d["bucket"],
                "X-Amz-Algorithm":      d["X-Amz-Algorithm"],
                "X-Amz-Credential":     d["X-Amz-Credential"],
                "X-Amz-Date":           d["X-Amz-Date"],
                "key":                  d["key"],
                "Policy":               d["Policy"],
                "X-Amz-Signature":      d["X-Amz-Signature"],
                "success_action_status": d["success_action_status"],
                "Content-Type":         d["content-type"],
                "Cache-Control":        d["Cache-Control"],
            },
            files={"file": (file_name, f, "image/png")},
        )

    if s3.status_code not in (200, 201, 204):
        print(f"ERROR: S3 upload failed — HTTP {s3.status_code}", file=sys.stderr)
        print(s3.text[:500], file=sys.stderr)
        sys.exit(1)

    # Step 3: fetch the hosted URL from Webflow
    asset_r = requests.get(
        f"{API_BASE}/sites/{SITE_ID}/assets/{asset_id}",
        headers=headers,
    )
    _check(asset_r, f"asset-get {asset_id}")
    data = asset_r.json()
    hosted_url = data.get("hostedUrl") or data.get("url") or ""

    if not hosted_url:
        print(f"ERROR: No hostedUrl in asset response for {file_name}", file=sys.stderr)
        print(json.dumps(data, indent=2)[:500], file=sys.stderr)
        sys.exit(1)

    print(f"     ✓ {hosted_url}", file=sys.stderr)
    return hosted_url


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


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) != 5:
        print(
            "Usage: python3 blog-publisher.py <fielddata.json> <header.png> <grid.png> <menu.png>",
            file=sys.stderr,
        )
        sys.exit(1)

    fielddata_path, header_png, grid_png, menu_png = sys.argv[1:]

    for path in [fielddata_path, header_png, grid_png, menu_png]:
        if not Path(path).exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            sys.exit(1)

    with open(fielddata_path) as f:
        field_data = json.load(f)

    token = get_token()
    slug = field_data.get("slug", "blog-post")
    alt_text = field_data.get("image-alt-text", "")

    # Upload all three images
    print("Uploading images…", file=sys.stderr)
    header_url = upload_asset(token, header_png, f"{slug}-header.png")
    grid_url   = upload_asset(token, grid_png,   f"{slug}-grid.png")
    menu_url   = upload_asset(token, menu_png,   f"{slug}-menu.png")

    # Inject image objects (alt text duplicated per Webflow image field spec)
    field_data["image-page-header"]   = {"url": header_url, "alt": alt_text}
    field_data["grid-thumbnail"]      = {"url": grid_url,   "alt": alt_text}
    field_data["thumbnail-mega-menu"] = {"url": menu_url,   "alt": alt_text}

    # Publish live
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
