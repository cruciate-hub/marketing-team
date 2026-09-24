#!/usr/bin/env python3
"""
Intent-level duplication check for the social.plus content engine.

Compares a candidate question (and, optionally, its draft first sentence)
against every row in the Content Queue and every published page, and
flags rows that would likely answer the same question.

Why not titles alone: the legacy /answers/ collection shipped ~80
near-duplicate pages ("SDK for X", "Tool for X", "Platform for X") that a
title-word check scored as different. This script normalises away the
"vehicle nouns" (SDK, API, platform, tool, solution, guide...) and folds
synonyms (community features / social features / in-app community...)
before comparing, so those collapse to the same intent.

This is still a lexical approximation. It surfaces candidates; the final
call uses the same-first-sentence test in the calling skill: if two pages
would open with the same answer, one of them should not exist.

Inputs
    question            the candidate canonical question (required)
    --first-sentence    the candidate's draft first sentence (recommended)
    --queue PATH        Content Queue exported as CSV (File > Download > CSV,
                        Queue tab). Columns used: ID, Canonical question,
                        Draft first sentence, Status, Collection, Published URL
    --pages GLOB        website/pages-*.json inventories (default: glossary,
                        answers and blog under $MT_REPO/website)
    --exclude-id ID     ignore this Queue ID (the row being checked itself)

Output
    One line per candidate above the review threshold, sorted by score,
    then a final line:  RESULT: CLEAN | RESULT: MATCHES | RESULT: UNVERIFIED

Exit codes
    0  clean (no candidate at or above the review threshold)
    1  candidates found (likely duplicate or needs review)
    2  unverified (an input could not be read; do not treat as clean)
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import re
import sys
from pathlib import Path

MT_REPO = Path(os.environ.get("MT_REPO", "/tmp/cruciate-hub-marketing-team"))

LIKELY_DUPLICATE = 0.60
NEEDS_REVIEW = 0.40

# Multi-word synonyms first (longest match wins), then single words.
PHRASE_SYNONYMS = [
    (r"\bsocial network(?:ing)? (?:features?|functions?|functionality|tools?|capabilities|components?)\b", "community"),
    (r"\bcommunity social network\b", "community"),
    (r"\b(?:in[- ]app|online|digital) community\b", "community"),
    (r"\bcommunity (?:features?|functions?|functionality|experiences?|systems?|modules?|platform)\b", "community"),
    (r"\bsocial (?:features?|functions?|functionality|experiences?|layer|modules?|capabilities)\b", "community"),
    (r"\bprivate social network\b", "community private"),
    (r"\bsocial network\b", "community"),
    (r"\b(?:activity|social|news) feeds?\b", "feed"),
    (r"\bin[- ]app (?:chat|messaging)\b", "chat"),
    (r"\breal[- ]time (?:chat|messaging)\b", "chat"),
    (r"\bmobile apps?\b", "app"),
    (r"\bwhite[- ]label\b", "whitelabel"),
    (r"\buser[- ]generated content\b", "ugc"),
    (r"\bfrom scratch\b", ""),
]

WORD_SYNONYMS = {
    "improve": "increase", "boost": "increase", "grow": "increase", "raise": "increase",
    "monetization": "monetize", "monetisation": "monetize", "monetise": "monetize", "revenue": "monetize",
    "retain": "retention", "retaining": "retention",
    "engaging": "engagement", "engage": "engagement",
    "messaging": "chat", "messages": "chat", "message": "chat",
    "application": "app", "applications": "app", "apps": "app",
    "build": "add", "building": "add", "create": "add", "creating": "add", "develop": "add",
    "developing": "add", "implement": "add", "implementing": "add", "integrate": "add",
    "integrating": "add", "embed": "add", "embedding": "add", "adding": "add", "launch": "add",
}

# Vehicle nouns and filler that carry no intent.
STOPWORDS = set("""
a an the to for in into inside within of on with and or your our my you i we it its is are be
do does can how what why which when where who should would could vs versus without directly
own using use via best top leading guide sdk sdks api apis platform platforms tool tools solution
solutions software service services kit kits system way ways need needs make get
""".split())


def normalise(text: str) -> set[str]:
    t = (text or "").lower()
    t = re.sub(r"https?://\S+", " ", t)
    for pat, rep in PHRASE_SYNONYMS:
        t = re.sub(pat, f" {rep} ", t)
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    tokens = []
    for w in t.split():
        w = WORD_SYNONYMS.get(w, w)
        if w in STOPWORDS or len(w) < 3:
            continue
        if w.endswith("s") and len(w) > 4 and not w.endswith("ss"):
            w = w[:-1]
        tokens.append(w)
    return set(tokens)


# Question form. Two questions about the same subject but of a different
# form ("What is app retention?" vs "How do you increase app retention?")
# are usually different pages, so a form mismatch discounts the score.
FORM_PENALTY = 0.6
_FORMS = [
    ("benchmark", r"^what(?:'s| is| are) (?:a |the )?(?:good|average|typical|normal)\b"),
    ("list", r"^(?:best|top|examples?|\d+ (?:best|ways|examples))\b|^what are (?:the )?(?:best|top)\b|^who are the top\b"),
    ("decision", r"^(?:should|which|how much|how long)\b|\bvs\.?\b|\bversus\b|\bor\b.*\?$|^(?:build|buy)\b"),
    ("why", r"^why\b"),
    ("howto", r"^(?:how (?:do|does|can|to|should|would)|how\b|guide to|steps to)\b"),
    ("definition", r"^what(?:'s| is| are| does)\b"),
    ("whether", r"^(?:do|does|is|are|can|will)\b"),
]


def question_form(text: str) -> str:
    t = (text or "").strip().lower()
    for name, pat in _FORMS:
        if re.search(pat, t):
            return name
    return "other"


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def score(cand_q: str, cand_s: str, other_q: str, other_s: str, form_aware: bool = True) -> float:
    """Best of question-vs-question and combined question+sentence overlap,
    discounted when the two questions are of a different form."""
    q = jaccard(normalise(cand_q), normalise(other_q))
    if cand_s and other_s:
        q = max(q, jaccard(normalise(cand_q + " " + cand_s), normalise(other_q + " " + other_s)))
    if form_aware:
        fa, fb = question_form(cand_q), question_form(other_q)
        if fa != fb and "other" not in (fa, fb):
            q *= FORM_PENALTY
    return q


def load_queue(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            rows.append({
                "source": "queue",
                "id": (r.get("ID") or "").strip(),
                "question": (r.get("Canonical question") or "").strip(),
                "sentence": (r.get("Draft first sentence") or "").strip(),
                "status": (r.get("Status") or "").strip(),
                "collection": (r.get("Collection") or "").strip(),
                "url": (r.get("Published URL") or "").strip(),
            })
    return rows


def load_pages(pattern: str) -> list[dict]:
    rows = []
    for fp in sorted(glob.glob(pattern)):
        d = json.load(open(fp, encoding="utf-8"))
        collection = Path(fp).stem.replace("pages-", "")
        for p in d.get("pages", []):
            rows.append({
                "source": "published",
                "id": "",
                "question": p.get("metaTitle") or p.get("url", "").rstrip("/").split("/")[-1].replace("-", " "),
                "sentence": p.get("metaDescription") or "",
                "status": "Published",
                "collection": collection,
                "url": p.get("url", ""),
            })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="Intent-level duplication check")
    ap.add_argument("question")
    ap.add_argument("--first-sentence", default="")
    ap.add_argument("--queue", type=Path)
    ap.add_argument("--pages", action="append",
                    help="glob for pages-*.json (repeatable). Default: glossary, answers, blog")
    ap.add_argument("--exclude-id", default="")
    ap.add_argument("--include-removed", action="store_true",
                    help="also compare against rows with status Scheduled for removal / Rejected / Merged")
    args = ap.parse_args()

    candidates: list[dict] = []
    try:
        if args.queue:
            candidates += load_queue(args.queue)
        patterns = args.pages or [str(MT_REPO / "website" / f"pages-{c}.json") for c in ("glossary", "answers", "blog")]
        for pat in patterns:
            if not glob.glob(pat):
                raise FileNotFoundError(pat)
            candidates += load_pages(pat)
    except Exception as e:  # noqa: BLE001
        print(f"Could not read input: {e}")
        print("RESULT: UNVERIFIED")
        return 2

    if not args.queue:
        print("Note: no --queue given; planned and in-progress ideas were NOT checked.")

    queue_urls = {c["url"].rstrip("/") for c in candidates if c["source"] == "queue" and c["url"]}
    inactive = {"scheduled for removal", "rejected", "merged"}
    hits = []
    for c in candidates:
        if args.exclude_id and c["id"] == args.exclude_id:
            continue
        # A published page that also has a Queue row is scored once, via the Queue row.
        if c["source"] == "published" and c["url"].rstrip("/") in queue_urls:
            continue
        if not args.include_removed and c["status"].lower() in inactive:
            continue
        s = score(args.question, args.first_sentence, c["question"], c["sentence"])
        if s >= NEEDS_REVIEW:
            hits.append((s, c))

    hits.sort(key=lambda x: -x[0])
    for s, c in hits:
        label = "LIKELY DUPLICATE" if s >= LIKELY_DUPLICATE else "REVIEW"
        ref = c["id"] or c["url"]
        print(f"{s:.2f}  {label:16}  [{c['collection']}/{c['status']}]  {ref}  |  {c['question']}")

    print("RESULT: MATCHES" if hits else "RESULT: CLEAN")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
