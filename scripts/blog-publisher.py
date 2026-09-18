#!/usr/bin/env python3
"""
blog-publisher.py — thin wrapper: the Blog collection's positional CLI on top of the shared
engine, scripts/webflow-publisher.py (field map: blog-seo-content/webflow-fields.json).

Kept so every documented command keeps working exactly as before:

    # Create + publish a new post (--staged: live on next site publish; --dry-run: validate only):
    python3 scripts/blog-publisher.py <fielddata.json> <header.webp> <grid.webp> <menu.webp> \
        [img-1.webp ...] [--staged] [--dry-run] [--source <draft.md>]

    # Refresh the 3 hero images on an EXISTING post (re-upload, patch, publish):
    python3 scripts/blog-publisher.py --update <item_id> <header.webp> <grid.webp> <menu.webp> [--dry-run]

The three hero positionals map to the blog field map's image roles header / grid / menu;
further positionals are inline body images. New-style flags (--image, --collection,
--field-map, --list-collections) are passed straight through to the engine.

Environment: WEBFLOW_API_TOKEN (not required for --dry-run). Stdlib only.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent / "webflow-publisher.py"
COLLECTION = "blog"
HERO_ROLES = ("header", "grid", "menu")
VALUE_FLAGS = {"--source", "--update", "--collection", "--field-map"}


def usage(code: int = 1) -> None:
    print("Usage:\n"
          "  create:  python3 blog-publisher.py <fielddata.json> <header.webp> <grid.webp> <menu.webp> "
          "[img-N.webp ...] [--staged] [--dry-run] [--source draft.md]\n"
          "  update:  python3 blog-publisher.py --update <item_id> <header.webp> <grid.webp> <menu.webp>",
          file=sys.stderr)
    sys.exit(code)


def main() -> None:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        usage(0 if argv else 1)

    # New-style invocation → pass through, adding the blog collection if none was named.
    if any(a.startswith("--image") or a in ("--collection", "--field-map", "--list-collections") for a in argv):
        if not any(a in ("--collection", "--field-map", "--list-collections") for a in argv):
            argv = ["--collection", COLLECTION, *argv]
        os.execv(sys.executable, [sys.executable, str(ENGINE), *argv])

    flags, positional, update_id, i = [], [], None, 0
    while i < len(argv):
        a = argv[i]
        if a == "--update":
            if i + 1 >= len(argv):
                usage()
            update_id = argv[i + 1]; i += 2
        elif a in VALUE_FLAGS:
            if i + 1 >= len(argv):
                usage()
            flags += [a, argv[i + 1]]; i += 2
        elif a.startswith("--"):
            flags.append(a); i += 1
        else:
            positional.append(a); i += 1

    if update_id:
        if len(positional) != 3:
            usage()
        cmd = ["--update", update_id, "--collection", COLLECTION]
        for role, path in zip(HERO_ROLES, positional):
            cmd += ["--image", f"{role}={path}"]
    else:
        if len(positional) < 4:
            usage()
        fielddata, heroes, inline = positional[0], positional[1:4], positional[4:]
        cmd = [fielddata, "--collection", COLLECTION]
        for role, path in zip(HERO_ROLES, heroes):
            cmd += ["--image", f"{role}={path}"]
        if inline:
            cmd += ["--inline", *inline]
    cmd += flags
    os.execv(sys.executable, [sys.executable, str(ENGINE), *cmd])


if __name__ == "__main__":
    main()
