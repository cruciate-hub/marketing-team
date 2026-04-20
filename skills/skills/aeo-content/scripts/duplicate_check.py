#!/usr/bin/env python3
"""
Duplicate-topic check for AEO articles.

Scans the team's published /answers/ and /glossary/ collections (via the
website/pages-*.json snapshots) for semantic overlap with a proposed topic.

Usage:
    python scripts/duplicate_check.py "in-app activity feeds"
    python scripts/duplicate_check.py "activity feeds" --threshold 0.5
    python scripts/duplicate_check.py "zero-party data" --json

Emits per-match details so the skill (or the author) can decide whether
to update the existing page or write something genuinely different.

Exit codes:
    0 — no matches above threshold
    1 — at least one likely-duplicate match
    2 — usage or fetch error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ANSWERS_URL = (
    "https://raw.githubusercontent.com/cruciate-hub/marketing-team/main/website/pages-answers.json"
)
GLOSSARY_URL = (
    "https://raw.githubusercontent.com/cruciate-hub/marketing-team/main/website/pages-glossary.json"
)
USER_AGENT = "aeo-content-duplicate-check/1 (+https://social.plus)"

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
    This makes compound-modifier queries like "in-app activity feeds" match
    pages that write "activity feeds ... inside an app". Short tokens and
    stopwords are dropped afterwards.
    """
    # Split on anything that isn't an apostrophe or letter (hyphens included).
    words = re.findall(r"[a-z][a-z']*", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) >= 3}


def coverage(query: set[str], haystack: set[str]) -> float:
    """Fraction of query tokens that appear in the haystack.

    Used instead of Jaccard because the haystack (a full page) has many
    more tokens than the query (a topic phrase), and Jaccard penalizes
    that asymmetry in a way that hides real matches.
    """
    if not query:
        return 0.0
    return len(query & haystack) / len(query)


def fetch_json(url: str) -> list[dict]:
    """Fetch a pages-*.json snapshot and return its list of pages.

    The snapshot schema is `{"_meta": {...}, "pages": [ {...}, ... ]}`.
    This function unwraps the `pages` array and returns it as a list;
    callers iterate pages directly.

    raw.githubusercontent.com is usable from local dev; the skill
    runtime should run this script via bash, not via the skill-runtime
    egress rules that block raw.*.
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} fetching {url}") from e
    except (urllib.error.URLError, TimeoutError) as e:
        raise RuntimeError(f"network error fetching {url}: {e}") from e

    if isinstance(data, dict) and "pages" in data:
        pages = data["pages"]
    elif isinstance(data, list):
        pages = data
    else:
        raise RuntimeError(f"unexpected JSON shape at {url}")
    if not isinstance(pages, list):
        raise RuntimeError(f"expected list under 'pages' at {url}")
    return pages


def entries(pages: list[dict]) -> Iterable[tuple[str, str, str]]:
    """Yield (title, url, content) per page, tolerating schema drift.

    Expected fields per page (as of the 2026 snapshots):
        url, metaTitle, metaDescription, content
    """
    for p in pages:
        title = p.get("metaTitle") or p.get("title") or p.get("name") or ""
        url = p.get("url") or ""
        content = p.get("content") or p.get("metaDescription") or ""
        yield title, url, content


def check(topic: str, threshold: float) -> list[Match]:
    query = tokens(topic)
    if not query:
        raise RuntimeError(f"topic has no content tokens: {topic!r}")

    matches: list[Match] = []

    for collection, url in (("answers", ANSWERS_URL), ("glossary", GLOSSARY_URL)):
        try:
            pages = fetch_json(url)
        except Exception as e:
            print(f"warning: could not fetch {collection}: {e}", file=sys.stderr)
            continue

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
    return matches


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
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = p.parse_args()

    try:
        matches = check(args.topic, args.threshold)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2

    if args.json:
        print(
            json.dumps(
                {
                    "topic": args.topic,
                    "threshold": args.threshold,
                    "matches": [m.__dict__ for m in matches],
                },
                indent=2,
            )
        )
    else:
        if not matches:
            print(f"No likely duplicates for '{args.topic}' (threshold {args.threshold}).")
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

    return 1 if matches else 0


if __name__ == "__main__":
    sys.exit(main())
