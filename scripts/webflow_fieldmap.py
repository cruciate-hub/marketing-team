#!/usr/bin/env python3
"""
webflow_fieldmap.py — load and validate a per-collection Webflow field map.

Each content-type skill owns its own field map, at marketing-team/skills/<skill>/webflow-fields.json
(e.g. glossary-content/webflow-fields.json) — not webflow-publisher, which only owns the
mechanics (HTML conversion, table embedding, image pipeline, the publish CLI). A field map
tells the shared publishing scripts which Webflow collection to target, which CMS field
slug each draft label maps to, the category taxonomy, the exact image sizes, and the slug
rules. The registry name used by --collection is the map's own "collection" key, not its
folder — this module finds it by scanning every skills/*/webflow-fields.json. The schema is
documented in marketing-team/skills/webflow-publisher/field-map-schema.md.

Conventions:
  - Keys that start with "_" are documentation (provenance, CONFIRM notes) and are ignored.
  - A field slug of null means "not confirmed yet". The converter parks such values under
    "__unconfirmed__" in fielddata.json and the engine refuses to publish while any
    required slug is unconfirmed. Never fill in a plausible-looking slug to get past that —
    read the real one from the Webflow Designer or GET /v2/collections/{collection_id}.

Usage (importable; also a tiny CLI for inspection):
    python3 scripts/webflow_fieldmap.py --list
    python3 scripts/webflow_fieldmap.py blog
    python3 scripts/webflow_fieldmap.py path/to/custom-map.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "marketing-team" / "skills"
FIELD_MAP_FILENAME = "webflow-fields.json"

SUPPORTED_SCHEMA = 1


class FieldMapError(Exception):
    pass


def _registry() -> dict:
    """{registry name -> path}, discovered by scanning every skills/*/webflow-fields.json
    and reading each one's own "collection" key (never the folder name — a skill's folder
    is named for its content type, e.g. glossary-content, not the Webflow collection)."""
    reg = {}
    if not SKILLS_DIR.is_dir():
        return reg
    for path in sorted(SKILLS_DIR.glob(f"*/{FIELD_MAP_FILENAME}")):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        name = raw.get("collection")
        if name:
            reg[name] = path
    return reg


def list_collections() -> list:
    return sorted(_registry())


def _strip_doc_keys(obj):
    """Drop every key starting with '_' (documentation only), recursively."""
    if isinstance(obj, dict):
        return {k: _strip_doc_keys(v) for k, v in obj.items() if not str(k).startswith("_")}
    if isinstance(obj, list):
        return [_strip_doc_keys(v) for v in obj]
    return obj


def resolve_path(ref: str) -> Path:
    """`ref` is either a registry name (blog, glossary, …) or a path to a JSON file."""
    p = Path(ref)
    if p.suffix == ".json" or p.exists():
        return p
    reg = _registry()
    if ref in reg:
        return reg[ref]
    known = ", ".join(sorted(reg)) or "(none found)"
    raise FieldMapError(f"unknown collection '{ref}'. Known: {known}. "
                        f"Or pass a path to a field-map JSON file.")


def validate_field_map(fm: dict) -> list:
    """Return a list of hard errors (empty = usable). Unconfirmed slugs are NOT errors here —
    they are reported separately via unconfirmed_slugs() so dry-run can list them."""
    errs = []
    if fm.get("schema_version") != SUPPORTED_SCHEMA:
        errs.append(f"schema_version must be {SUPPORTED_SCHEMA} (got {fm.get('schema_version')!r})")
    for key in ("collection", "site_id", "collection_id", "live_url_prefix"):
        if not fm.get(key):
            errs.append(f"missing '{key}'")
    fields = fm.get("fields")
    if not isinstance(fields, dict):
        errs.append("'fields' must be an object with title/slug/body/intro/date")
    else:
        for key in ("title", "slug", "body", "intro", "date"):
            if key not in fields:
                errs.append(f"fields.{key} missing (use null when the collection has no such field)")
        if fields.get("title") in (None, "") or fields.get("slug") in (None, ""):
            errs.append("fields.title and fields.slug must be set (every Webflow collection has name + slug)")
    if not isinstance(fm.get("metadata", {}), dict):
        errs.append("'metadata' must be an object of draft-label → {slug, …}")
    for label, spec in (fm.get("metadata") or {}).items():
        if not isinstance(spec, dict) or "slug" not in spec:
            errs.append(f"metadata[{label!r}] must be an object with a 'slug' key (null if unconfirmed)")
            continue
        t = spec.get("type", "text")
        if t not in ("text", "reference", "multi_reference"):
            errs.append(f"metadata[{label!r}].type must be text | reference | multi_reference")
        if t in ("reference", "multi_reference") and not spec.get("taxonomy"):
            errs.append(f"metadata[{label!r}] is a {t} but names no 'taxonomy'")
        if spec.get("taxonomy") and spec["taxonomy"] not in (fm.get("taxonomies") or {}):
            errs.append(f"metadata[{label!r}] refers to taxonomy '{spec['taxonomy']}' which is not defined")
        if spec.get("must_include") and spec["must_include"] not in (fm.get("metadata") or {}):
            errs.append(f"metadata[{label!r}].must_include names unknown label '{spec['must_include']}'")
    images = fm.get("images", [])
    if not isinstance(images, list):
        errs.append("'images' must be a list")
    else:
        roles = set()
        for im in images:
            for k in ("role", "slug", "variant", "width", "height"):
                if k not in im:
                    errs.append(f"images[] entry missing '{k}': {im}")
            if im.get("role") in roles:
                errs.append(f"duplicate image role '{im.get('role')}'")
            roles.add(im.get("role"))
    inline = fm.get("inline_images")
    if inline is not None and not all(k in inline for k in ("variant", "width", "height")):
        errs.append("'inline_images' must have variant/width/height (or be null)")
    return errs


def unconfirmed_slugs(fm: dict) -> dict:
    """{'required': [...names...], 'optional': [...names...]} of slugs still null."""
    req, opt = [], []
    fields = fm.get("fields", {})
    if fields.get("body") is None:
        req.append("fields.body")
    for label, spec in (fm.get("metadata") or {}).items():
        if spec.get("slug") is None:
            (req if spec.get("required") else opt).append(f"metadata[{label}]")
    for im in fm.get("images", []):
        if im.get("slug") is None:
            req.append(f"images[{im.get('role')}]")
    return {"required": req, "optional": opt}


def load_field_map(ref: str) -> dict:
    """Load, strip documentation keys, validate. Raises FieldMapError on a broken map."""
    path = resolve_path(ref)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise FieldMapError(f"cannot read field map {path}: {e}")
    fm = _strip_doc_keys(raw)
    fm.setdefault("metadata", {})
    fm.setdefault("taxonomies", {})
    fm.setdefault("defaults", {})
    fm.setdefault("images", [])
    fm.setdefault("inline_images", None)
    fm.setdefault("slug_rules", {})
    fm.setdefault("checks", {})
    errs = validate_field_map(fm)
    if errs:
        raise FieldMapError(f"field map {path} is invalid:\n  - " + "\n  - ".join(errs))
    fm["_name"] = fm.get("collection") or path.stem
    fm["_path"] = str(path)
    return fm


def image_spec(fm: dict, role: str) -> dict:
    for im in fm.get("images", []):
        if im["role"] == role:
            return im
    raise FieldMapError(f"collection '{fm.get('_name')}' has no image role '{role}'. "
                        f"Roles: {[i['role'] for i in fm.get('images', [])] or 'none'}")


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] == "--list":
        for name in list_collections():
            try:
                fm = load_field_map(name)
                unc = unconfirmed_slugs(fm)
                status = "ready" if not unc["required"] else f"UNCONFIRMED ({len(unc['required'])} required slug(s) missing)"
            except FieldMapError as e:
                status = f"INVALID: {e}"
            print(f"  {name:12} {status}")
        return 0
    try:
        fm = load_field_map(args[0])
    except FieldMapError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    unc = unconfirmed_slugs(fm)
    print(json.dumps({k: v for k, v in fm.items() if not k.startswith("_")}, indent=2))
    if unc["required"] or unc["optional"]:
        print(f"\nUnconfirmed required: {unc['required']}\nUnconfirmed optional: {unc['optional']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
