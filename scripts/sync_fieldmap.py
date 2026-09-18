#!/usr/bin/env python3
"""
sync_fieldmap.py — fetch a collection's LIVE Webflow schema and propose slugs for the
null entries in its field map (marketing-team/skills/webflow-publisher/collections/<name>.json).

Why this exists: field slugs are not a mechanical transform of a display name (the live
Blog collection's "Minutes to Read" field has slug "min-read", not "minutes-to-read"), so
this never invents one. It fetches the real live field list (GET /v2/collections/{id},
needs cms:read) and matches it against the field map's null entries by display name + type.
Only unambiguous matches are proposed; anything ambiguous or unmatched is left null and
reported so a human decides. Same rule as the rest of webflow-publisher: never fill in a
plausible-looking slug. This replaces the manual "open the Webflow Designer and hand-type
slugs into JSON" step, not the human confirmation step.

Usage:
    python3 scripts/sync_fieldmap.py --collection glossary            # report only, no writes
    python3 scripts/sync_fieldmap.py --collection glossary --write    # also fill in the unambiguous ones

Environment:
    WEBFLOW_API_TOKEN — needs cms:read.

Dependencies: Python 3 standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from webflow_fieldmap import FieldMapError, resolve_path  # noqa: E402

API_BASE = "https://api.webflow.com/v2"
BUILTIN_SLUGS = {"name", "slug"}

# structural field key -> (acceptable Webflow field types, displayName hints)
STRUCTURAL_HINTS = {
    "body":  (("RichText",), ["body", "content", "definition"]),
    "intro": (("PlainText", "RichText"), ["summary", "intro", "excerpt", "introduction"]),
    "date":  (("DateTime",), ["date", "published"]),
}


def get_token() -> str:
    token = os.environ.get("WEBFLOW_API_TOKEN", "").strip()
    if not token:
        print("ERROR: WEBFLOW_API_TOKEN is not set.\n  export WEBFLOW_API_TOKEN=your_token", file=sys.stderr)
        sys.exit(1)
    return token


def http_get(url: str, token: str, timeout: int = 30):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8", "replace"))
        except Exception:
            return e.code, {}
    except (urllib.error.URLError, TimeoutError) as e:
        return 0, {"error": f"network error / timeout after {timeout}s: {getattr(e, 'reason', e)}"}


def normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def _match(candidates: list, used: set, types: tuple, scorer) -> list:
    """Only ever returns fields the scorer actually matched by name — never a bare
    "only one candidate left of this type" guess. Guessing by elimination is exactly
    what this tool exists to avoid; an empty result means "no match", not "assume it"."""
    pool = [f for f in candidates if f["slug"] not in used and f["type"] in types]
    return [f for f in pool if scorer(f)]


def propose(fm: dict, live_fields: list) -> dict:
    candidates = [f for f in live_fields if f["slug"] not in BUILTIN_SLUGS]
    used = set()
    report = {"fields": {}, "metadata": {}, "unmapped_live": []}

    for key in ("body", "intro", "date"):
        if fm.get("fields", {}).get(key) is not None:
            continue
        types, hints = STRUCTURAL_HINTS[key]
        matches = _match(candidates, used, types,
                          lambda f: any(h in normalize(f["displayName"]) for h in hints))
        report["fields"][key] = _resolve(matches, used)

    for label, spec in (fm.get("metadata") or {}).items():
        if spec.get("slug") is not None:
            continue
        wanted = {"reference": ("Reference",), "multi_reference": ("MultiReference",)}.get(
            spec.get("type", "text"), ("PlainText", "RichText"))
        label_n = normalize(label)
        matches = _match(candidates, used, wanted,
                          lambda f: normalize(f["displayName"]) == label_n)
        if not matches:
            matches = _match(candidates, used, wanted,
                              lambda f: label_n in normalize(f["displayName"])
                              or normalize(f["displayName"]) in label_n)
        report["metadata"][label] = _resolve(matches, used)

    mapped = used | {im.get("slug") for im in fm.get("images", []) if im.get("slug")}
    report["unmapped_live"] = [{"slug": f["slug"], "displayName": f["displayName"], "type": f["type"]}
                                for f in candidates if f["slug"] not in mapped]
    return report


def _resolve(matches: list, used: set) -> dict:
    if len(matches) == 1:
        f = matches[0]
        used.add(f["slug"])
        return {"slug": f["slug"], "displayName": f["displayName"], "confidence": "unambiguous"}
    if len(matches) > 1:
        return {"slug": None, "confidence": "ambiguous",
                "candidates": [(f["slug"], f["displayName"]) for f in matches]}
    return {"slug": None, "confidence": "no match"}


def apply_write(path: Path, raw: dict, report: dict) -> int:
    n = 0
    for key, res in report["fields"].items():
        if res["confidence"] == "unambiguous" and raw.get("fields", {}).get(key) is None:
            raw["fields"][key] = res["slug"]
            n += 1
    for label, res in report["metadata"].items():
        if res["confidence"] == "unambiguous" and raw.get("metadata", {}).get(label, {}).get("slug") is None:
            raw["metadata"][label]["slug"] = res["slug"]
            n += 1
    if n:
        path.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
    return n


def _print_line(name: str, res: dict) -> None:
    if res["confidence"] == "unambiguous":
        print(f"  ✅ {name:35s} -> {res['slug']!r:30s} ({res['displayName']})")
    elif res["confidence"] == "ambiguous":
        cands = ", ".join(f"{s!r} ({d})" for s, d in res["candidates"])
        print(f"  ⚠️  {name:35s} -> AMBIGUOUS: {cands} — resolve manually")
    else:
        print(f"  —  {name:35s} -> no matching live field; delete this entry if the collection has none")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--collection", required=True, help="registry name in webflow-publisher/collections/")
    ap.add_argument("--write", action="store_true", help="write unambiguous matches back into the field map file")
    args = ap.parse_args()

    try:
        path = resolve_path(args.collection)
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (FieldMapError, OSError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    collection_id = raw.get("collection_id")
    if not collection_id:
        print(f"ERROR: {path} has no collection_id", file=sys.stderr)
        sys.exit(1)

    token = get_token()
    status, body = http_get(f"{API_BASE}/collections/{collection_id}", token)
    if status != 200:
        print(f"ERROR: GET /collections/{collection_id} -> {status}: {body}", file=sys.stderr)
        sys.exit(1)

    live_fields = body.get("fields", [])
    report = propose(raw, live_fields)

    print(f"Collection: {raw.get('collection')} ({collection_id}) — {len(live_fields)} live fields\n")
    if not report["fields"] and not report["metadata"]:
        print("  Nothing to sync — every fields.*/metadata.* slug is already confirmed.")
    for key, res in report["fields"].items():
        _print_line(f"fields.{key}", res)
    for label, res in report["metadata"].items():
        _print_line(f"metadata[{label!r}]", res)

    if report["unmapped_live"]:
        print("\nLive fields with no local mapping (FYI — e.g. image fields not yet added to the map):")
        for f in report["unmapped_live"]:
            print(f"  {f['slug']:30s} [{f['type']}]  {f['displayName']}")

    all_res = list(report["fields"].values()) + list(report["metadata"].values())
    unambiguous = [r for r in all_res if r["confidence"] == "unambiguous"]
    remaining = [r for r in all_res if r["confidence"] != "unambiguous"]

    if args.write:
        n = apply_write(path, raw, report)
        print(f"\nWrote {n} unambiguous slug(s) to {path}")
    elif unambiguous:
        print(f"\n{len(unambiguous)} unambiguous match(es) found. Re-run with --write to fill them in.")

    if remaining:
        print(f"{len(remaining)} entr(y/ies) still need a manual decision — see ⚠️/— lines above.")


if __name__ == "__main__":
    main()
