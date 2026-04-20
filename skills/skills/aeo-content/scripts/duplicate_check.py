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
    0 — no matches above threshold (check ran cleanly)
    1 — at least one likely-duplicate match (or matches found AND partial
        fetch failure — the caller should still review matches but be
        aware not all collections were checked)
    2 — usage error, OR check could not be verified (at least one
        collection fetch failed AND no matches from any collection that
        did succeed). The script does NOT silently report "safe to
        draft" in this case — field testing caught an earlier version
        exiting 0 on network failure, which is a false-clean.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

# Blob URLs only. raw.githubusercontent.com is blocked by the skill runtime's
# network egress policy; fetch_brand.py uses the same blob-URL convention for
# the same reason. Do not switch to raw hosts — the egress block returns a
# 403 Tunnel Forbidden which this script used to swallow as a false-clean.
ANSWERS_URL = (
    "https://github.com/cruciate-hub/marketing-team/blob/main/website/pages-answers.json"
)
GLOSSARY_URL = (
    "https://github.com/cruciate-hub/marketing-team/blob/main/website/pages-glossary.json"
)
USER_AGENT = "aeo-content-duplicate-check/2 (+https://social.plus)"

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


def _fetch_html(url: str, max_retries: int = 3) -> str:
    """HTTP GET with exponential backoff on transient errors.

    Mirrors the retry/backoff pattern in scripts/fetch_brand.py — same
    constants so the two scripts behave identically under network stress.
    """
    last: Exception | None = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            # 4xx is not retryable — it will keep failing.
            if 400 <= e.code < 500:
                raise RuntimeError(f"HTTP {e.code} fetching {url}") from e
            last = e
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # 1s, 2s, 4s
    raise RuntimeError(
        f"fetch failed after {max_retries} attempts: {last}"
    ) from last


def _extract_raw_json_from_blob_html(html_text: str, url: str) -> str:
    """Pull the raw JSON file content out of a GitHub blob HTML page.

    GitHub embeds the raw file as a list of per-line strings in a
    react-app payload at
      data['payload']['codeViewBlobLayoutRoute.StyledBlob']['rawLines']
    (note the dotted composite key). Joining with '\\n' reconstructs the
    raw file.

    Falls back to recursive search for any 'rawLines' list if GitHub
    changes the exact path — so small markup drift doesn't break this.
    Raises RuntimeError if neither path yields usable content.
    """
    script_match = re.search(
        r'<script[^>]*data-target="react-app\.embeddedData"[^>]*>(.*?)</script>',
        html_text,
        re.DOTALL,
    )
    if not script_match:
        raise RuntimeError(
            f"could not find react-app payload in blob page for {url} "
            f"(GitHub markup may have changed; update _extract_raw_json_from_blob_html)"
        )

    try:
        payload = json.loads(html.unescape(script_match.group(1)))
    except json.JSONDecodeError as e:
        raise RuntimeError(f"react-app payload at {url} is not valid JSON: {e}") from e

    # Primary path: the dotted composite key GitHub currently uses.
    raw_lines = None
    try:
        raw_lines = payload["payload"]["codeViewBlobLayoutRoute.StyledBlob"]["rawLines"]
    except (KeyError, TypeError):
        pass

    # Fallback: recursive search for the first 'rawLines' list of strings.
    if raw_lines is None:
        raw_lines = _find_raw_lines(payload)

    if not isinstance(raw_lines, list):
        raise RuntimeError(
            f"rawLines not found in blob payload for {url} "
            f"(expected list of strings at payload.codeViewBlobLayoutRoute.StyledBlob.rawLines)"
        )
    return "\n".join(raw_lines)


def _find_raw_lines(obj: object) -> list[str] | None:
    """Recursive search for the first 'rawLines' list of strings."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "rawLines" and isinstance(v, list) and all(isinstance(x, str) for x in v):
                return v
            found = _find_raw_lines(v)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = _find_raw_lines(v)
            if found is not None:
                return found
    return None


def fetch_json(url: str) -> list[dict]:
    """Fetch a pages-*.json snapshot via its blob URL and return its pages.

    The snapshot schema is `{"_meta": {...}, "pages": [ {...}, ... ]}`.
    This function unwraps the `pages` array and returns it as a list;
    callers iterate pages directly.

    Uses github.com/.../blob/... (not raw.githubusercontent.com) because
    the skill runtime blocks raw hosts. See module docstring / SKILL.md
    URL-format rule.
    """
    html_text = _fetch_html(url)
    raw = _extract_raw_json_from_blob_html(html_text, url)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"extracted content at {url} is not valid JSON: {e}") from e

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


@dataclass
class CheckResult:
    matches: list[Match]
    fetch_errors: list[tuple[str, str]]  # (collection, error_message)
    collections_checked: list[str]


def check(topic: str, threshold: float) -> CheckResult:
    query = tokens(topic)
    if not query:
        raise RuntimeError(f"topic has no content tokens: {topic!r}")

    matches: list[Match] = []
    fetch_errors: list[tuple[str, str]] = []
    checked: list[str] = []

    for collection, url in (("answers", ANSWERS_URL), ("glossary", GLOSSARY_URL)):
        try:
            pages = fetch_json(url)
        except Exception as e:
            fetch_errors.append((collection, str(e)))
            print(f"warning: could not fetch {collection}: {e}", file=sys.stderr)
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
        fetch_errors=fetch_errors,
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
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = p.parse_args()

    try:
        result = check(args.topic, args.threshold)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2

    matches = result.matches
    fetch_errors = result.fetch_errors
    # Unverified state: at least one collection failed AND no matches were
    # found from any collection that did succeed. Emitting "Safe to draft"
    # in this state would be a false-clean — the caller needs to know the
    # check could not run, not that no duplicates exist.
    unverified = bool(fetch_errors) and not matches

    if args.json:
        print(
            json.dumps(
                {
                    "topic": args.topic,
                    "threshold": args.threshold,
                    "matches": [m.__dict__ for m in matches],
                    "collections_checked": result.collections_checked,
                    "fetch_errors": [
                        {"collection": c, "error": e} for c, e in fetch_errors
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
                f"RESULT: UNVERIFIED — could not reach duplicate data for '{args.topic}'."
            )
            print()
            print("Collections that failed to fetch:")
            for c, err in fetch_errors:
                url = ANSWERS_URL if c == "answers" else GLOSSARY_URL
                print(f"  - {c}: {err}")
                print(f"    ({url})")
            print()
            print(
                "Manual check required: open the URLs above in a browser and scan "
                "the metaTitle fields for topic overlap. Do NOT proceed assuming no "
                "duplicates exist — this script could not verify."
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
            if fetch_errors:
                print()
                failed = ", ".join(c for c, _ in fetch_errors)
                print(
                    f"WARNING: at least one collection could not be checked ({failed}); "
                    f"results may be incomplete — verify against the failed URL(s) manually."
                )

    if unverified:
        return 2
    return 1 if matches else 0


if __name__ == "__main__":
    sys.exit(main())
