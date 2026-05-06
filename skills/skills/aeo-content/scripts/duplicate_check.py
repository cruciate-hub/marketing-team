#!/usr/bin/env python3
"""
Duplicate-topic check for AEO articles.

Scans the team's published /answers/ and /glossary/ collections (via the
website/pages-*.json snapshots) for semantic overlap with a proposed topic.

Reads the snapshots from the repo cloned by the canonical fetch block (see
SKILL.md). Default cloned path is `/tmp/cruciate-hub-marketing-team`; override
with the MT_REPO environment variable.

Usage:
    MT_REPO=/tmp/cruciate-hub-marketing-team \\
        python3 scripts/duplicate_check.py "in-app activity feeds"
    python3 scripts/duplicate_check.py "activity feeds" --threshold 0.5
    python3 scripts/duplicate_check.py "zero-party data" --json
    python3 scripts/duplicate_check.py "..." --repo /custom/path

Exit codes:
    0 — no matches above threshold (check ran cleanly)
    1 — at least one likely-duplicate match (or matches found AND partial
        read failure — the caller should still review matches but be
        aware not all collections were checked)
    2 — usage error, OR check could not be verified (at least one
        collection read failed AND no matches from any collection that
        did succeed). The script does NOT silently report "safe to
        draft" in this case.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_REPO = os.environ.get("MT_REPO", "/tmp/cruciate-hub-marketing-team")

ANSWERS_REL = "website/pages-answers.json"
GLOSSARY_REL = "website/pages-glossary.json"

# Non-content words that should not drive match scores.
STOPWORDS = {
    "a", "an", "and", "as", "at", "be", "by", "for", "from", "has", "have",
    "how", "in", "is", "it", "of", "on", "or", "the", "to", "vs", "what",
    "where", "why", "with", "your", "you", "this", "that", "these", "those",
    "are", "am", "was", "were", "do", "does", "can", "will", "would",
}


@dataclass
class Match:
    collection: str
    title: str
    url: str
    score: float
    matched_terms: list[str]


def tokens(text: str) -> set[str]:
    """Lowercase content tokens, minus stopwords.

    Hyphens are treated as word separators — so "in-app" yields {"in", "app"}.
    Short tokens and stopwords are dropped afterwards.
    """
    words = re.findall(r"[a-z][a-z']*", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) >= 3}


def coverage(query: set[str], haystack: set[str]) -> float:
    """Fraction of query tokens that appear in the haystack."""
    if not query:
        return 0.0
    return len(query & haystack) / len(query)


def read_json(path: Path) -> list[dict]:
    """Read a pages-*.json snapshot from disk and return its pages.

    The snapshot schema is `{"_meta": {...}, "pages": [ {...}, ... ]}`.
    """
    if not path.exists():
        raise RuntimeError(f"file not found: {path}")
    if not path.is_file():
        raise RuntimeError(f"not a file: {path}")

    text = path.read_text()
    if not text.strip():
        raise RuntimeError(f"file is empty: {path}")
    if text.lstrip()[:1] not in "{[":
        raise RuntimeError(
            f"file does not start with '{{' or '[' (canonical fetch-block "
            f"validation): {path}"
        )

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"not valid JSON: {path}: {e}") from e

    if isinstance(data, dict) and "pages" in data:
        pages = data["pages"]
    elif isinstance(data, list):
        pages = data
    else:
        raise RuntimeError(f"unexpected JSON shape at {path}")
    if not isinstance(pages, list):
        raise RuntimeError(f"expected list under 'pages' at {path}")
    return pages


def entries(pages: list[dict]) -> Iterable[tuple[str, str, str]]:
    """Yield (title, url, content) per page, tolerating schema drift."""
    for p in pages:
        title = p.get("metaTitle") or p.get("title") or p.get("name") or ""
        url = p.get("url") or ""
        content = p.get("content") or p.get("metaDescription") or ""
        yield title, url, content


@dataclass
class CheckResult:
    matches: list[Match]
    read_errors: list[tuple[str, str]]  # (collection, error_message)
    collections_checked: list[str]


def check(topic: str, threshold: float, repo_root: Path) -> CheckResult:
    query = tokens(topic)
    if not query:
        raise RuntimeError(f"topic has no content tokens: {topic!r}")

    matches: list[Match] = []
    read_errors: list[tuple[str, str]] = []
    checked: list[str] = []

    for collection, rel in (("answers", ANSWERS_REL), ("glossary", GLOSSARY_REL)):
        path = repo_root / rel
        try:
            pages = read_json(path)
        except Exception as e:
            read_errors.append((collection, str(e)))
            print(f"warning: could not read {collection}: {e}", file=sys.stderr)
            continue
        checked.append(collection)

        for title, url_entry, content in entries(pages):
            haystack = tokens(title + " " + content)
            score = coverage(query, haystack)
            if score >= threshold:
                matched_terms = sorted(query & haystack)
                matches.append(
                    Match(
                        collection=collection,
                        title=title,
                        url=url_entry,
                        score=round(score, 3),
                        matched_terms=matched_terms,
                    )
                )

    matches.sort(key=lambda m: m.score, reverse=True)
    return CheckResult(
        matches=matches,
        read_errors=read_errors,
        collections_checked=checked,
    )


def main() -> int:
    p = argparse.ArgumentParser(description="AEO duplicate-topic checker")
    p.add_argument(
        "topic",
        help='The proposed article topic, e.g. "in-app activity feeds"',
    )
    p.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Query-coverage threshold (0-1) for a match (default: 0.5 — at least half the topic's content words appear in the page)",
    )
    p.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help=(
            "Path to the cloned cruciate-hub/marketing-team repo "
            "(default: $MT_REPO or /tmp/cruciate-hub-marketing-team). "
            "The canonical fetch block in SKILL.md ensures this clone exists."
        ),
    )
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = p.parse_args()

    repo_root = Path(args.repo)
    if not (repo_root / ".git").exists():
        msg = (
            f"repo not cloned at {repo_root} — run the canonical fetch block "
            "from SKILL.md first to populate it"
        )
        print(f"error: {msg}", file=sys.stderr)
        # Also emit the canonical stdout marker so the calling skill's
        # grep-based signal path sees it consistently with the exit code.
        print("\nRESULT: UNVERIFIED")
        return 2

    try:
        result = check(args.topic, args.threshold, repo_root)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        print("\nRESULT: UNVERIFIED")
        return 2

    matches = result.matches
    read_errors = result.read_errors
    # Unverified state: at least one collection failed AND no matches were
    # found from any collection that did succeed.
    unverified = bool(read_errors) and not matches

    if args.json:
        print(
            json.dumps(
                {
                    "topic": args.topic,
                    "threshold": args.threshold,
                    "matches": [m.__dict__ for m in matches],
                    "collections_checked": result.collections_checked,
                    "read_errors": [
                        {"collection": c, "error": e} for c, e in read_errors
                    ],
                    "status": (
                        "UNVERIFIED" if unverified
                        else "MATCHES" if matches
                        else "CLEAN"
                    ),
                },
                indent=2,
            )
        )
    else:
        if unverified:
            print(
                f"Could not read duplicate data for '{args.topic}'."
            )
            print()
            print("Collections that failed to read:")
            for c, err in read_errors:
                rel = ANSWERS_REL if c == "answers" else GLOSSARY_REL
                print(f"  - {c}: {err}")
                print(f"    (expected at {repo_root / rel})")
            print()
            print(
                "Manual check required: re-run the canonical fetch block to "
                "ensure the repo is cloned and up-to-date, then retry."
            )
        elif not matches:
            print(f"No likely duplicates for '{args.topic}' (threshold {args.threshold}).")
            print(f"Collections checked: {', '.join(result.collections_checked)}.")
            print("Safe to draft a new article.")
        else:
            print(f"Likely duplicates for '{args.topic}' (threshold {args.threshold}):\n")
            for m in matches:
                print(f"  [{m.score:.2f}] {m.collection:8}  {m.title}")
                print(f"              {m.url}")
                print(f"              matched: {', '.join(m.matched_terms[:8])}")
                print()
            print(
                "At least one strong match exists. Consider updating the existing page "
                "instead of drafting a near-duplicate."
            )
            if read_errors:
                print()
                failed = ", ".join(c for c, _ in read_errors)
                print(
                    f"WARNING: at least one collection could not be read ({failed}); "
                    f"results may be incomplete — verify the missing snapshots manually."
                )

        # Final canonical stdout marker — calling skills can grep this as a
        # redundant signal alongside the exit code. Both must agree; if they
        # disagree, treat as UNVERIFIED and surface to the user.
        print()
        if unverified:
            print("RESULT: UNVERIFIED")
        elif matches:
            print("RESULT: MATCHES")
        else:
            print("RESULT: CLEAN")

    if unverified:
        return 2
    return 1 if matches else 0


if __name__ == "__main__":
    sys.exit(main())
