#!/usr/bin/env python3
"""
webflow-publisher.py — upload images and publish a CMS item to any Webflow collection
described by a field map (each content-type skill's own webflow-fields.json — schema
documented in webflow-publisher/field-map-schema.md).

Usage:
    # Validate everything, touch no API (needs no token). Exits non-zero on any failed check.
    python3 scripts/webflow-publisher.py <fielddata.json> --collection <name> \
        [--image <role>=<path> ...] [--inline <img-1.webp> ...] [--source <draft.md>] --dry-run

    # Create + publish live (or --staged: create the item, live on the next site publish):
    python3 scripts/webflow-publisher.py <fielddata.json> --collection <name> \
        --image header=… --image grid=… --image menu=… [--inline …] [--staged]

    # Rewrite an EXISTING item (same slug) from fielddata.json — e.g. a glossary rewrite —
    # then publish it. Images are optional here; given ones are re-uploaded and patched too:
    python3 scripts/webflow-publisher.py <fielddata.json> --collection <name> --replace <item_id> \
        [--image <role>=<path> ...] [--inline …] [--dry-run]

    # Refresh image fields on an EXISTING item (re-upload → partial PATCH → publish):
    python3 scripts/webflow-publisher.py --update <item_id> --collection <name> --image <role>=<path> ...

    python3 scripts/webflow-publisher.py --list-collections

    --collection   registry name (blog, glossary, …); or --field-map <path> for any map file.
    --image        one per image field, keyed by the field map's image role.
    --inline       body images, in placeholder order (__INLINE_IMG_1__, _2_, …).
    --source       the markdown intermediate; lets the dry-run compare the number of tables
                   in the source with the number of <table> elements in the body.
    --dry-run      required fields, slug rules, taxonomy consistency, forbidden strings,
                   no <h1>/<style>/<script>, internal links, placeholder↔inline match,
                   structural table checks, exact image dimensions, unconfirmed field slugs.
                   Writes dry-run-report.json next to fielddata.json.
    --replace      PATCH the given item's fields from fielddata.json (its slug must match) and
                   publish. Find the id with GET /v2/collections/{id}/items?slug={slug}.

Environment:
    WEBFLOW_API_TOKEN  —  cms:write + assets:write (+ sites:read for pre-flight).
                          Not required for --dry-run or --list-collections.

Dependencies: Python 3 standard library only — no pip install, no virtualenv. (Image
dimension checks use Pillow if present; without Pillow they are skipped and say so.)
All network calls carry timeouts (30s API / 60s S3) — a hung connection exits with an
error instead of blocking forever.

Outputs (stdout): JSON  { "itemId": "...", "slug": "...", "liveUrl": "https://…" }
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from webflow_fieldmap import (FieldMapError, image_spec, list_collections,  # noqa: E402
                              load_field_map, unconfirmed_slugs)

API_BASE = "https://api.webflow.com/v2"

# Webflow's full-width image block inside rich text. All five figure attributes are
# required and the <img> must be wrapped in a <div>, or the Designer strips it on save.
# alt="__wf_reserved_inherit" matches production; the real alt text lives in the
# collection's standalone alt-text field (see html-conversion.md).
FIGURE_TEMPLATE = (
    '<figure class="w-richtext-figure-type-image w-richtext-align-fullwidth" '
    'style="max-width:{width}px" data-rt-type="image" data-rt-align="fullwidth" '
    'data-rt-max-width="{width}px">'
    '<div><img alt="__wf_reserved_inherit" src="{url}" loading="lazy"></div>'
    '</figure>'
)

# ── HTTP (stdlib only) ───────────────────────────────────────────────────────────

def get_token() -> str:
    token = os.environ.get("WEBFLOW_API_TOKEN", "").strip()
    if not token:
        print("ERROR: WEBFLOW_API_TOKEN is not set.\n  export WEBFLOW_API_TOKEN=your_token", file=sys.stderr)
        sys.exit(1)
    return token


def api_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Accept": "application/json"}


def md5_file(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def http(method: str, url: str, headers=None, json_body=None, raw_body=None, timeout=30):
    """
    Minimal HTTP via urllib. Returns (status, text). Never raises on an HTTP error
    status — returns the error body so callers can report it.

    ALWAYS pass a timeout — a hung connection with no timeout has blocked a scripted run
    for 45 minutes. Default 30s for API calls; the S3 upload passes a longer one.
    """
    headers = dict(headers or {})
    data = None
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif raw_body is not None:
        data = raw_body
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError) as e:
        reason = getattr(e, "reason", e)
        return 0, f"network error / timeout after {timeout}s: {reason}"


def _json(text: str):
    try:
        return json.loads(text)
    except Exception:
        return {}


def _check(status: int, text: str, label: str) -> None:
    if not (200 <= status < 300):
        print(f"ERROR: {label} — HTTP {status}", file=sys.stderr)
        parsed = _json(text)
        print(json.dumps(parsed, indent=2)[:800] if parsed else text[:800], file=sys.stderr)
        sys.exit(1)


def _multipart_body(fields: dict, file_field: str, filename: str,
                    file_bytes: bytes, file_content_type: str):
    """
    Build a multipart/form-data body for an AWS S3 POST-policy upload. The file part MUST
    come last (S3 ignores any field after `file`), so emit all form fields first.
    Returns (body_bytes, content_type_header).
    """
    boundary = "----webflowpub" + uuid.uuid4().hex
    crlf = "\r\n"
    head = "".join(
        f"--{boundary}{crlf}"
        f'Content-Disposition: form-data; name="{k}"{crlf}{crlf}{v}{crlf}'
        for k, v in fields.items()
    )
    file_head = (
        f"--{boundary}{crlf}"
        f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"{crlf}'
        f"Content-Type: {file_content_type}{crlf}{crlf}"
    )
    body = head.encode("utf-8") + file_head.encode("utf-8") + file_bytes + f"{crlf}--{boundary}--{crlf}".encode("utf-8")
    return body, f"multipart/form-data; boundary={boundary}"


# ── Asset upload ───────────────────────────────────────────────────────────────

def upload_asset(token: str, site_id: str, file_path: str, file_name: str) -> tuple:
    """
    Upload an image to Webflow (3-step). Returns (asset_id, hosted_url).
    The hosted S3 URL is built directly from uploadDetails.bucket + key — no extra GET.
    Passing that URL to a CMS Image field makes Webflow accept it and re-host it on CDN.
    (A hand-built cdn.prod.website-files.com URL 403s and the field is silently dropped.)
    Webflow dedupes assets by fileHash: identical bytes return the existing asset under
    its original filename — functionally fine, the library name just won't match this item.
    """
    file_hash = md5_file(file_path)
    print(f"  → {file_name}  (MD5 {file_hash[:8]}…)", file=sys.stderr)

    status, text = http("POST", f"{API_BASE}/sites/{site_id}/assets",
                        headers=api_headers(token),
                        json_body={"fileName": file_name, "fileHash": file_hash})
    _check(status, text, f"asset-register {file_name}")
    meta = _json(text)
    upload_url = meta["uploadUrl"]
    d          = meta["uploadDetails"]
    asset_id   = meta["id"]

    # S3 POST-policy upload (form fields then the file, file last)
    fields = {
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
    }
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    ctype_file = mimetypes.guess_type(file_name)[0] or "image/webp"
    body, ctype = _multipart_body(fields, "file", file_name, file_bytes, ctype_file)
    # 60s timeout: file transfer, slower than a JSON call. Expected success is 201
    # (the success_action_status Webflow sets); 200/204 accepted defensively.
    status, text = http("POST", upload_url, headers={"Content-Type": ctype}, raw_body=body,
                        timeout=60)
    if status not in (200, 201, 204):
        print(f"ERROR: S3 upload failed — HTTP {status}", file=sys.stderr)
        print(text[:500], file=sys.stderr)
        sys.exit(1)

    hosted_url = f"https://s3.amazonaws.com/{d['bucket']}/{d['key']}"
    print(f"     ✓ {hosted_url}", file=sys.stderr)
    return asset_id, hosted_url


# ── Inline image injection ─────────────────────────────────────────────────────

def inject_inline_images(body_html: str, inline_urls: list, width: int) -> str:
    for i, url in enumerate(inline_urls, start=1):
        placeholder = f"__INLINE_IMG_{i}__"
        if placeholder in body_html:
            body_html = body_html.replace(placeholder, FIGURE_TEMPLATE.format(url=url, width=width))
            print(f"  ✓ Injected inline image {i}", file=sys.stderr)
        else:
            print(f"  ⚠ Placeholder {placeholder} not found — skipped", file=sys.stderr)
    return body_html


# ── Publish ────────────────────────────────────────────────────────────────────

def publish_live(token: str, collection_id: str, field_data: dict) -> dict:
    status, text = http("POST", f"{API_BASE}/collections/{collection_id}/items/live",
                        headers=api_headers(token), json_body={"fieldData": field_data})
    _check(status, text, "webflow-publish")
    return _json(text)


def _extract_item(data) -> dict:
    """Bulk endpoint may return a bare list or {"items":[...]}. Normalize to one item dict."""
    if isinstance(data, dict) and "items" in data:
        items = data["items"]
        return items[0] if items else {}
    if isinstance(data, list):
        return data[0] if data else {}
    return data if isinstance(data, dict) else {}


def publish_staged(token: str, collection_id: str, field_data: dict) -> dict:
    """
    Create a staged item via POST /items/bulk. Image fields persist directly in the bulk
    call AS LONG AS each image url is a valid S3 hostedUrl; Webflow re-hosts it on CDN.
    """
    status, text = http("POST", f"{API_BASE}/collections/{collection_id}/items/bulk",
                        headers=api_headers(token),
                        json_body={"fieldData": field_data, "isDraft": False})
    _check(status, text, "webflow-stage")
    return _extract_item(_json(text))


# ── Image helpers ───────────────────────────────────────────────────────────────

def pillow_available() -> bool:
    try:
        import PIL  # noqa: F401
        return True
    except ImportError:
        return False


def image_dims(path: str):
    """(w, h) via Pillow; None when Pillow is missing; raises when the file is unreadable."""
    if not pillow_available():
        return None
    from PIL import Image
    with Image.open(path) as im:
        return im.size


def check_dims(path: str, exp: tuple) -> tuple:
    """Returns (ok, detail). Pillow missing → ok with a 'skipped' note; unreadable → not ok."""
    try:
        dims = image_dims(path)
    except Exception as e:
        return False, f"unreadable image ({type(e).__name__}: {e})"
    if dims is None:
        return True, "dim check skipped (no Pillow)"
    if dims != exp:
        return False, f"{dims[0]}x{dims[1]} (expected {exp[0]}x{exp[1]})"
    return True, f"{dims[0]}x{dims[1]}"


def parse_image_args(pairs: list, fm: dict) -> dict:
    """['header=/p/a.webp', …] → {role: path}; validates roles against the field map."""
    out = {}
    for pair in pairs or []:
        if "=" not in pair:
            print(f"ERROR: --image expects <role>=<path>, got {pair!r}", file=sys.stderr)
            sys.exit(1)
        role, path = pair.split("=", 1)
        image_spec(fm, role)  # raises FieldMapError on an unknown role
        if role in out:
            print(f"ERROR: image role '{role}' given twice", file=sys.stderr)
            sys.exit(1)
        out[role] = path
    return out


# ── Update mode: refresh image fields on an EXISTING item ───────────────────────

def update_images(token: str, fm: dict, item_id: str, images: dict) -> None:
    """
    --update <item_id>: re-upload the given images and PATCH only those fields onto an
    existing item, then publish it.

    Verified in production (blog):
    - A partial PATCH with ONLY the image fields preserves every other field.
    - {"url": <hostedUrl>} is sufficient for an Image field.
    - Webflow RE-INGESTS the image under a new fileId on update, so the response URL
      differs from what was sent. That is normal — verify by the filename surviving as
      the URL suffix.
    """
    cid = fm["collection_id"]
    item_url = f"{API_BASE}/collections/{cid}/items/{item_id}"

    status, text = http("GET", item_url, headers=api_headers(token))
    if status == 404:
        print(f"ERROR: item {item_id} not found in the {fm.get('display_name', fm['_name'])} collection.",
              file=sys.stderr)
        sys.exit(1)
    _check(status, text, "update-get-item")
    fd   = _json(text).get("fieldData", {})
    slug = fd.get("slug", "?")
    print(f"Updating images on: {fd.get('name', '?')!r}  (slug: {slug})", file=sys.stderr)

    # Validate dimensions BEFORE uploading — the collection enforces exact sizes.
    for role, path in images.items():
        spec = image_spec(fm, role)
        ok, detail = check_dims(path, (spec["width"], spec["height"]))
        if not ok:
            print(f"ERROR: {Path(path).name} ({role}): {detail} — the CMS field rejects anything else.",
                  file=sys.stderr)
            sys.exit(1)

    print("Uploading replacement images…", file=sys.stderr)
    patch = {}
    for role, path in images.items():
        _, url = upload_asset(token, fm["site_id"], path, Path(path).name)
        patch[image_spec(fm, role)["slug"]] = {"url": url}

    print("Patching image fields…", file=sys.stderr)
    status, text = http("PATCH", item_url, headers=api_headers(token), json_body={"fieldData": patch})
    _check(status, text, "update-patch")

    resp = _json(text).get("fieldData", {})
    for role, path in images.items():
        field = image_spec(fm, role)["slug"]
        url = (resp.get(field) or {}).get("url", "") if isinstance(resp.get(field), dict) else ""
        ok  = Path(path).name in url
        print(f"  {'✓' if ok else '⚠'} {field}" + ("" if ok else " — filename not in response URL; check the live page"),
              file=sys.stderr)

    print("Publishing…", file=sys.stderr)
    status, text = http("POST", f"{API_BASE}/collections/{cid}/items/publish",
                        headers=api_headers(token), json_body={"itemIds": [item_id]})
    _check(status, text, "update-publish")

    live = f"{fm['live_url_prefix']}{slug}"
    print(json.dumps({"itemId": item_id, "slug": slug, "liveUrl": live, "updated": True}))
    print(f"\n✓ Images refreshed: {live}", file=sys.stderr)


# ── Pre-flight checks ───────────────────────────────────────────────────────────

def preflight_token(token: str, fm: dict) -> None:
    """Token works and has site access — one cheap GET /sites/{id} before any upload."""
    status, text = http("GET", f"{API_BASE}/sites/{fm['site_id']}", headers=api_headers(token))
    if status == 401:
        print("ERROR: Token rejected (401). Check WEBFLOW_API_TOKEN.", file=sys.stderr)
        sys.exit(1)
    if status == 403:
        print("ERROR: Token missing scopes. Needs sites:read, cms:write, assets:write.", file=sys.stderr)
        sys.exit(1)
    _check(status, text, "preflight-site")


def preflight(token: str, fm: dict, slug: str) -> None:
    """
    Fail fast BEFORE uploading any images:
      1. Token works and has site access (one cheap GET /sites/{id}).
      2. Slug is not already taken (avoids N wasted uploads then a 400).
    """
    preflight_token(token, fm)

    qs = urllib.parse.urlencode({"slug": slug})
    status, text = http("GET", f"{API_BASE}/collections/{fm['collection_id']}/items?{qs}",
                        headers=api_headers(token))
    _check(status, text, "preflight-slug")
    existing = _json(text).get("items", [])
    if existing:
        print(f"ERROR: Slug '{slug}' already exists (item {existing[0]['id']}).", file=sys.stderr)
        print("       Stopping before upload. Choose a new slug or update the existing item.", file=sys.stderr)
        print("       Do NOT append a year or numeric suffix — pick a genuinely distinct slug.", file=sys.stderr)
        sys.exit(1)

    print(f"✓ Pre-flight OK — token valid, slug '{slug}' available", file=sys.stderr)


# ── Replace mode: rewrite an EXISTING item's fields ─────────────────────────────

def upload_and_attach_images(token: str, fm: dict, field_data: dict, images: dict, inline_paths: list) -> None:
    """Upload field images (→ {fileId,url,alt}) and inline images (→ <figure> in the body)."""
    f = fm["fields"]
    if images:
        print("Uploading field images…", file=sys.stderr)
        for role, path in images.items():
            asset_id, url = upload_asset(token, fm["site_id"], path, Path(path).name)
            field_data[image_spec(fm, role)["slug"]] = {"fileId": asset_id, "url": url, "alt": None}
    if inline_paths:
        print(f"Uploading {len(inline_paths)} inline image(s)…", file=sys.stderr)
        inline_urls = []
        for path in inline_paths:
            _, url = upload_asset(token, fm["site_id"], path, Path(path).name)
            inline_urls.append(url)
        if inline_urls and f.get("body") in field_data:
            print("Injecting inline images…", file=sys.stderr)
            field_data[f["body"]] = inject_inline_images(field_data[f["body"]], inline_urls,
                                                         fm["inline_images"]["width"])


def replace_item(token: str, fm: dict, item_id: str, field_data: dict, images: dict, inline_paths: list) -> None:
    """
    --replace <item_id>: rewrite an existing item in place (the glossary's common case —
    a rewrite keeps the live slug and URL). Verifies the item exists and that its slug
    matches fielddata's, uploads any given images, PATCHes every field in fielddata
    (partial PATCH: fields not in the payload are preserved), then publishes the item.
    """
    cid = fm["collection_id"]
    item_url = f"{API_BASE}/collections/{cid}/items/{item_id}"
    f = fm["fields"]

    preflight_token(token, fm)
    status, text = http("GET", item_url, headers=api_headers(token))
    if status == 404:
        print(f"ERROR: item {item_id} not found in the {fm.get('display_name', fm['_name'])} collection.",
              file=sys.stderr)
        sys.exit(1)
    _check(status, text, "replace-get-item")
    live = _json(text).get("fieldData", {})
    live_slug, new_slug = live.get("slug", ""), field_data.get(f["slug"], "")
    if live_slug != new_slug:
        print(f"ERROR: live item slug is '{live_slug}' but fielddata says '{new_slug}'. A rewrite keeps the "
              "live slug (glossary-content: 'rewrites should not create redirect debt'). Fix the draft's "
              "`Slug:` line, or create a new item instead.", file=sys.stderr)
        sys.exit(1)
    print(f"Replacing content on: {live.get('name', '?')!r}  (slug: {live_slug})", file=sys.stderr)

    upload_and_attach_images(token, fm, field_data, images, inline_paths)

    print("Patching fields…", file=sys.stderr)
    status, text = http("PATCH", item_url, headers=api_headers(token), json_body={"fieldData": field_data})
    _check(status, text, "replace-patch")

    print("Publishing…", file=sys.stderr)
    status, text = http("POST", f"{API_BASE}/collections/{cid}/items/publish",
                        headers=api_headers(token), json_body={"itemIds": [item_id]})
    _check(status, text, "replace-publish")

    live_url = f"{fm['live_url_prefix']}{live_slug}"
    print(json.dumps({"itemId": item_id, "slug": live_slug, "liveUrl": live_url, "replaced": True}, indent=2))
    print(f"\n✓ Rewritten in place: {live_url}", file=sys.stderr)


# ── Dry-run validation ──────────────────────────────────────────────────────────

YEAR_RE = re.compile(r"(?:19|20)\d{2}")
LEAD_COUNT_RE = re.compile(r"^(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|"
                           r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|"
                           r"eighteen|nineteen|twenty)-")
INTERNAL_LINK_RE = re.compile(r'href="(?:/|https?://(?:www\.)?social\.plus)')
# A markdown table that collapsed into prose looks like "<p>| a | b | |---|---| …</p>".
FLATTENED_TABLE_RE = re.compile(r"<p>\s*\|.*?\|.*?</p>|<p>[^<]*\|-{2,}[^<]*</p>", re.DOTALL)
GFM_TABLE_LINE_RE = re.compile(r"^\s*\|")


def count_markdown_tables(text: str) -> int:
    n, in_tbl = 0, False
    for line in text.split("\n"):
        is_tbl = bool(GFM_TABLE_LINE_RE.match(line)) and bool(line.strip())
        if is_tbl and not in_tbl:
            n += 1
        in_tbl = is_tbl
    return n


def required_field_slugs(fm: dict) -> list:
    f = fm["fields"]
    req = [f["title"], f["slug"]]
    if f.get("body"):
        req.append(f["body"])
    if f.get("intro"):
        req.append(f["intro"])
    for label, spec in fm.get("metadata", {}).items():
        if spec.get("required") and spec.get("slug"):
            req.append(spec["slug"])
    return req


def dry_run_validate(field_data: dict, fm: dict, images: dict, inline_paths: list,
                     fielddata_path: str, source_path: str = None, require_images: bool = True) -> None:
    """
    Validate the full publish payload WITHOUT calling Webflow. Prints a human report
    and writes dry-run-report.json next to fielddata.json. Exits non-zero if any
    check fails, so it's usable as a gate in tests and CI.
    require_images=False (--replace): image fields the map declares may be omitted —
    the live item keeps its current images.
    """
    checks = []  # (name, passed, detail)

    def chk(name, passed, detail=""):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    f = fm["fields"]
    slug = str(field_data.get(f["slug"], ""))

    # 0. Field map readiness — a null slug in the map means "not confirmed", never "absent".
    unc = unconfirmed_slugs(fm)
    chk("fieldmap:required-slugs-confirmed", not unc["required"],
        f"unconfirmed (null) in {fm['_path']}: {unc['required']} — read the real slugs "
        f"from Webflow (Designer or GET /v2/collections/{fm['collection_id']}) and fill them in"
        if unc["required"] else "")
    if unc["optional"]:
        chk("fieldmap:optional-slugs-unconfirmed", True, f"still null (values dropped): {unc['optional']}")
    parked = field_data.get("__unconfirmed__") or {}
    chk("content:no-unconfirmed-values", not parked,
        f"values parked under __unconfirmed__: {sorted(parked)} — cannot be sent to Webflow" if parked else "")

    # 1. Required fields present and non-empty
    for fld in required_field_slugs(fm):
        v = field_data.get(fld)
        chk(f"field:{fld}", bool(v), "" if v else "missing/empty")
    for label, spec in fm.get("metadata", {}).items():
        mx, sl = spec.get("max_length"), spec.get("slug")
        if mx and sl and isinstance(field_data.get(sl), str):
            n = len(field_data[sl])
            chk(f"field:{sl}:max-length", n <= mx, f"{n} chars (max {mx})" if n > mx else f"{n} chars")

    # 2. Slug rules as configured for the collection
    rules = fm.get("slug_rules", {})
    if rules.get("strip_years"):
        chk("slug:no-year", not YEAR_RE.search(slug), slug if YEAR_RE.search(slug) else "")
    if rules.get("strip_leading_count"):
        lead = LEAD_COUNT_RE.match(slug)
        chk("slug:no-leading-count", not lead, f"slug starts with a count: {slug}" if lead else "")
    chk("slug:format", bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug)), slug)

    # 3. Taxonomy consistency (e.g. Tags ⊇ Category)
    for label, spec in fm.get("metadata", {}).items():
        inc = spec.get("must_include")
        if not inc or not spec.get("slug"):
            continue
        ref_slug = fm["metadata"][inc].get("slug")
        ref_id = field_data.get(ref_slug) if ref_slug else None
        multi = field_data.get(spec["slug"]) or []
        chk(f"taxonomy:{spec['slug']}-includes-{ref_slug}", bool(ref_id) and ref_id in multi,
            "" if ref_id and ref_id in multi else f"{ref_slug}={ref_id!r} not in {spec['slug']}")

    # 4. Body integrity
    body_slug = f.get("body")
    pc = field_data.get(body_slug, "") if body_slug else parked.get("body", "")
    for s in fm.get("checks", {}).get("forbidden_body_strings", []):
        chk(f"content:no-leak[{s}]", s not in pc, f"body contains {s!r}" if s in pc else "")
    chk("content:no-h1", "<h1" not in pc)
    chk("content:no-style-block", "<style" not in pc,
        "body contains a <style> block — Webflow renders it as literal text; table CSS belongs in site custom code"
        if "<style" in pc else "")
    chk("content:no-script-or-iframe", not re.search(r"<(script|iframe)\b", pc, re.IGNORECASE))
    if fm.get("checks", {}).get("require_internal_links"):
        n_internal = len(INTERNAL_LINK_RE.findall(pc))
        chk("content:has-internal-links", n_internal >= 1,
            "no internal links found — did the internal-linking step run?" if not n_internal
            else f"{n_internal} internal links")
    n_placeholders = len(re.findall(r"__INLINE_IMG_\d+__", pc))
    chk("content:placeholders-match-inline", n_placeholders == len(inline_paths),
        f"{n_placeholders} placeholders vs {len(inline_paths)} inline images")

    # 5. Tables — structural, never keyed on heading text.
    n_tables   = pc.count("<table")
    n_embedded = pc.count(f"<div data-rt-embed-type='true'><table") + pc.count('<div data-rt-embed-type="true"><table')
    flattened  = FLATTENED_TABLE_RE.search(pc) is not None
    src_tables = None
    if source_path:
        try:
            src_txt = Path(source_path).read_text(encoding="utf-8-sig", errors="replace")
        except OSError as e:
            src_txt = ""
            chk("source:readable", False, f"{source_path}: {e}")
        src_tables = count_markdown_tables(src_txt)
    lost = src_tables is not None and src_tables > n_tables
    chk("content:table-not-flattened", not flattened and not lost,
        ("a <p> carries markdown-table syntax (| … | / |---) — the table collapsed into prose" if flattened else "")
        + (f"; source has {src_tables} table block(s) but body has {n_tables} <table>" if lost else "")
        if (flattened or lost) else (f"{n_tables} table(s)" + (f", {src_tables} in source" if src_tables is not None else "")))
    if n_tables:
        chk("content:table-in-embed", n_embedded == n_tables,
            "" if n_embedded == n_tables else
            f"{n_tables - n_embedded} raw <table> not wrapped in <div data-rt-embed-type='true'> — the Designer can mangle it")
        chk("content:table-structure", pc.count("<thead>") == n_tables and pc.count("<tbody>") == n_tables,
            "" if pc.count("<thead>") == n_tables and pc.count("<tbody>") == n_tables else "a table lacks <thead>/<tbody>")

    # 6. Images — every image field in the map must be supplied at exact dimensions.
    for spec in fm.get("images", []):
        role, path = spec["role"], images.get(spec["role"])
        if require_images or path:
            chk(f"image:{role}:provided", bool(path), "" if path else f"--image {role}=<path> missing")
        if path:
            ok, detail = check_dims(path, (spec["width"], spec["height"]))
            chk(f"image:{Path(path).name}", ok, detail)
            chk(f"image:{Path(path).name}:is-webp", str(path).lower().endswith(".webp"))
    extra_roles = sorted(set(images) - {s["role"] for s in fm.get("images", [])})
    chk("image:no-unknown-roles", not extra_roles, f"roles not in field map: {extra_roles}" if extra_roles else "")
    inline_spec = fm.get("inline_images")
    if inline_paths and not inline_spec:
        chk("image:inline-supported", False, f"collection '{fm['_name']}' declares no inline_images but {len(inline_paths)} given")
    for p in inline_paths:
        if inline_spec:
            ok, detail = check_dims(p, (inline_spec["width"], inline_spec["height"]))
            chk(f"image:{Path(p).name}", ok, detail)
        chk(f"image:{Path(p).name}:is-webp", str(p).lower().endswith(".webp"))

    # Report
    passed = sum(1 for c in checks if c["passed"])
    total  = len(checks)
    print(f"\n── DRY RUN ({fm['_name']}) ── {passed}/{total} checks passed", file=sys.stderr)
    for c in checks:
        mark = "✓" if c["passed"] else "✗"
        line = f"  {mark} {c['check']}"
        if c["detail"]:
            line += f"  — {c['detail']}"
        print(line, file=sys.stderr)

    verb = "Would publish" if require_images else "Would replace"
    print(f"\n  {verb}: name={field_data.get(f['title'])!r}", file=sys.stderr)
    print(f"                 slug={slug!r}  →  {fm['live_url_prefix']}{slug}", file=sys.stderr)
    print(f"                 {len(inline_paths)} inline + {len(images)} field image(s)", file=sys.stderr)
    print(f"                 body {len(pc):,} chars", file=sys.stderr)

    report = {"collection": fm["_name"], "passed": passed, "total": total,
              "all_passed": passed == total, "checks": checks}
    report_path = str(Path(fielddata_path).with_name("dry-run-report.json"))
    with open(report_path, "w") as fh:
        json.dump(report, fh, indent=2)
    print(f"\n  Report: {report_path}", file=sys.stderr)

    print(json.dumps({"dryRun": True, "collection": fm["_name"], "passed": passed, "total": total,
                      "allPassed": passed == total, "slug": slug}))
    if passed != total:
        sys.exit(1)


# ── Main ───────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Publish a CMS item to a Webflow collection (field-map driven).")
    ap.add_argument("fielddata", nargs="?", help="fielddata.json (flat fieldData payload)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--collection", help="registry name (each content-type skill's own webflow-fields.json)")
    g.add_argument("--field-map", help="path to a field-map JSON")
    ap.add_argument("--image", action="append", default=[], metavar="ROLE=PATH",
                    help="image field by role (repeatable)")
    ap.add_argument("--inline", nargs="*", default=[], metavar="PATH", help="body images in placeholder order")
    ap.add_argument("--source", help="markdown intermediate, for the source-vs-output table check")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--staged", action="store_true", help="create the item; live on next site publish")
    ap.add_argument("--update", metavar="ITEM_ID", help="refresh image fields on an existing item")
    ap.add_argument("--replace", metavar="ITEM_ID",
                    help="rewrite an existing item's fields from fielddata.json (same slug), then publish")
    ap.add_argument("--list-collections", action="store_true")
    return ap


def main() -> None:
    ap = build_parser()
    args = ap.parse_args()

    if args.list_collections:
        for name in list_collections():
            try:
                fm = load_field_map(name)
                unc = unconfirmed_slugs(fm)
                status = "ready" if not unc["required"] else f"UNCONFIRMED ({len(unc['required'])} required slug(s) null)"
                print(f"  {name:12} {fm.get('display_name', ''):22} {status}")
            except FieldMapError as e:
                print(f"  {name:12} INVALID: {e}")
        return

    if not (args.collection or args.field_map):
        ap.error("--collection <name> or --field-map <path> is required")
    try:
        fm = load_field_map(args.collection or args.field_map)
        images = parse_image_args(args.image, fm)
    except FieldMapError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # ── Update mode ──────────────────────────────────────────────────────────────
    if args.update:
        if args.staged:
            print("ERROR: --update cannot be combined with --staged (it patches an existing item).", file=sys.stderr)
            sys.exit(1)
        if not images:
            print("ERROR: --update needs at least one --image <role>=<path>.", file=sys.stderr)
            sys.exit(1)
        for path in images.values():
            if not Path(path).exists():
                print(f"ERROR: File not found: {path}", file=sys.stderr)
                sys.exit(1)
        if args.dry_run:
            ok = True
            for role, path in images.items():
                spec = image_spec(fm, role)
                good, detail = check_dims(path, (spec["width"], spec["height"]))
                ok = ok and good
                print(f"  {'✓' if good else '✗'} {Path(path).name} ({role}) — {detail}", file=sys.stderr)
            print(json.dumps({"dryRun": True, "update": True, "collection": fm["_name"], "allPassed": ok}))
            sys.exit(0 if ok else 1)
        update_images(get_token(), fm, args.update, images)
        return

    # ── Create / replace mode ────────────────────────────────────────────────────
    if not args.fielddata:
        ap.error("fielddata.json is required (or use --update / --list-collections)")
    if args.replace and args.staged:
        print("ERROR: --replace cannot be combined with --staged (it patches a live item).", file=sys.stderr)
        sys.exit(1)
    for path in [args.fielddata, *images.values(), *args.inline]:
        if not Path(path).exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            sys.exit(1)

    with open(args.fielddata) as fh:
        field_data = json.load(fh)
    f = fm["fields"]
    slug = field_data.get(f["slug"], "")

    if args.dry_run:
        dry_run_validate(field_data, fm, images, args.inline, args.fielddata, args.source,
                         require_images=not args.replace)
        return

    # Refuse to publish anything the map cannot place. The dry-run says the same thing
    # with more detail; this is the belt for someone who skipped it.
    unc = unconfirmed_slugs(fm)
    if unc["required"] or field_data.get("__unconfirmed__"):
        print(f"ERROR: {fm['_path']} still has unconfirmed (null) slugs "
              f"{unc['required']} or fielddata carries __unconfirmed__ values. Run --dry-run for details. "
              "Confirm the real slugs in Webflow before publishing.", file=sys.stderr)
        sys.exit(1)
    missing_roles = [s["role"] for s in fm.get("images", []) if s["role"] not in images]
    if missing_roles and not args.replace:
        print(f"ERROR: missing --image for role(s) {missing_roles} (every image field in the map is required).",
              file=sys.stderr)
        sys.exit(1)
    if args.inline and not fm.get("inline_images"):
        print(f"ERROR: collection '{fm['_name']}' declares no inline_images.", file=sys.stderr)
        sys.exit(1)

    token = get_token()

    if args.replace:
        replace_item(token, fm, args.replace, field_data, images, args.inline)
        return

    preflight(token, fm, slug)
    upload_and_attach_images(token, fm, field_data, images, args.inline)

    if args.staged:
        print("Staging for next site publish…", file=sys.stderr)
        result = publish_staged(token, fm["collection_id"], field_data)
    else:
        print("Publishing to Webflow…", file=sys.stderr)
        result = publish_live(token, fm["collection_id"], field_data)

    item_id   = result.get("id", "")
    live_slug = (result.get("fieldData") or {}).get("slug", slug)
    live_url  = f"{fm['live_url_prefix']}{live_slug}"
    print(json.dumps({"itemId": item_id, "slug": live_slug, "liveUrl": live_url}, indent=2))
    print(f"\n✓ Done: {live_url}", file=sys.stderr)


if __name__ == "__main__":
    main()
