#!/usr/bin/env python3
"""
AEO article compliance checker.

Deterministic checks for AEO articles produced by the aeo-content skill.
Human / LLM judgment still owns tone, factuality, and citation quality — this
script owns the mechanical checks that slip past eyeball review.

The script reads the markdown intermediate (outputs/[slug].draft.md) that the
skill produces before converting to `.docx`. Metadata lives in labeled
paragraphs directly under the H1:

    # Article title

    Meta description: ...
    Slug: ...
    Alt text: ...
    Intent: definition | procedural | comparative

    [answer-first block starts here]

Usage:
    python scripts/compliance.py path/to/article.draft.md
    python scripts/compliance.py path/to/article.draft.md --intent definition
    python scripts/compliance.py path/to/article.draft.md --min 1100 --max 1800
    python scripts/compliance.py path/to/article.draft.md --json

Exit codes:
    0 — no failures (warnings are allowed)
    1 — at least one failure
    2 — usage error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


# Case-insensitive patterns — marketing fluff and category mislabels.
FORBIDDEN_TERMS_ANY_CASE = [
    r"\brevolutioni[sz]e\b",
    r"\bgame[- ]chang(ing|er)\b",
    r"\bunlock the power\b",
    r"\bleverag(e|ing)\b",
    r"\bcutting[- ]edge\b",
    r"\bnext[- ]generation\b",
    r"\bbest[- ]in[- ]class\b",
    r"\bstate[- ]of[- ]the[- ]art\b",
    r"\bsocial[- ]network\b",
    r"\bforum platform\b",
    r"\bchat tool\b",
]

# Case-sensitive — brand-name casing (correct form: `social.plus`).
FORBIDDEN_TERMS_CASE_SENSITIVE = [
    r"\bSocial\.Plus\b",
    r"\bSocialPlus\b",
    r"\bSocial\+\b",
]

# Filler openers — fail if the first sentence starts with one of these.
FILLER_OPENERS = [
    r"^In today'?s\b",
    r"^Now more than ever\b",
    r"^In the ever[- ]evolving\b",
    r"^In a world where\b",
    r"^Gone are the days\b",
    r"^It'?s no secret\b",
    r"^As we all know\b",
    r"^In recent years\b",
]

APPROVED_CUSTOMERS = {"Noom", "Harley-Davidson", "Smart Fit", "Ulta Beauty", "Betgames"}

# Customer names we might accidentally reach for but which are not approved.
WATCHED_UNAPPROVED = re.compile(
    r"\b(?:Duolingo|Strava|Reddit|Discord|Slack|Peloton|Calm|Headspace)\b"
)

# Required metadata keys. `title` comes from the H1; the rest come from
# labeled paragraphs directly under the H1 ("Meta description: …", etc.).
REQUIRED_METADATA = ["title", "metaDescription", "slug", "altText", "intent"]

# Map the labeled-paragraph key (case/space-insensitive) to the canonical key.
LABELED_PARAGRAPH_KEYS = {
    "metadescription": "metaDescription",
    "slug": "slug",
    "alttext": "altText",
    "intent": "intent",
}

VALID_INTENTS = {"definition", "procedural", "comparative"}

# Intent-specific defaults.
INTENT_WORD_RANGE: dict[str, tuple[int, int]] = {
    "definition": (900, 1400),
    "procedural": (1100, 1800),
    "comparative": (1000, 1600),
}

INTENT_CITATION_MIN: dict[str, int] = {
    "definition": 2,
    "procedural": 0,  # no minimum
    "comparative": 3,
}

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "]"
)

EM_DASH = "\u2014"
HTML_TAG_PATTERN = re.compile(r"<[a-zA-Z/][^>]*>")
MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class CheckResult:
    name: str
    status: str  # "PASS", "FAIL", "WARN"
    detail: str = ""


@dataclass
class Report:
    results: list[CheckResult] = field(default_factory=list)

    @property
    def failed(self) -> list[CheckResult]:
        return [r for r in self.results if r.status == "FAIL"]

    @property
    def warned(self) -> list[CheckResult]:
        return [r for r in self.results if r.status == "WARN"]

    def as_json(self) -> str:
        return json.dumps(
            {
                "passed": len(self.failed) == 0,
                "failures": len(self.failed),
                "warnings": len(self.warned),
                "results": [
                    {"name": r.name, "status": r.status, "detail": r.detail}
                    for r in self.results
                ],
            },
            indent=2,
        )


def parse_metadata(text: str) -> tuple[dict[str, str], str]:
    """Extract labeled-paragraph metadata from the top of the document.

    Returns `(metadata, body_after_metadata)`. `metadata` always contains
    `title` if an H1 is present; the four label keys (metaDescription, slug,
    altText, intent) are present only if the matching labeled paragraph
    existed.

    Expected top-of-document structure:

        # Article title

        Meta description: ...
        Slug: ...
        Alt text: ...
        Intent: ...

        [answer-first block starts here]

    The function accepts a blank line between the H1 and the labeled
    paragraphs. It stops collecting metadata at the first non-labeled,
    non-blank line (that line is the start of the body).
    """
    meta: dict[str, str] = {}
    lines = text.splitlines()
    i = 0
    # Find the H1.
    while i < len(lines) and not lines[i].strip().startswith("# "):
        i += 1
    if i < len(lines):
        meta["title"] = lines[i].strip().lstrip("#").strip()
        i += 1
    # Skip blank lines.
    while i < len(lines) and not lines[i].strip():
        i += 1
    # Consume labeled paragraphs.
    label_re = re.compile(r"^([A-Za-z][A-Za-z ]+?):\s*(.+)$")
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            # Blank line — provisionally end of metadata, but skip and continue
            # only if the next non-blank line is also a labeled paragraph.
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j >= len(lines):
                i = j
                break
            next_stripped = lines[j].strip()
            if label_re.match(next_stripped) and next_stripped.split(":", 1)[0].lower().replace(" ", "") in LABELED_PARAGRAPH_KEYS:
                i = j
                continue
            i = j
            break
        m = label_re.match(stripped)
        if not m:
            break
        key_raw, value = m.group(1), m.group(2)
        key_norm = key_raw.lower().replace(" ", "")
        if key_norm in LABELED_PARAGRAPH_KEYS:
            meta[LABELED_PARAGRAPH_KEYS[key_norm]] = value.strip()
            i += 1
            continue
        break
    # Remaining lines are the body.
    body = "\n".join(lines[i:]).lstrip("\n")
    return meta, body


def word_count(text: str) -> int:
    # Strip code fences, inline code, HTML comments, table rows, headings.
    t = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.DOTALL)
    t = re.sub(r"`[^`]+`", "", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"^\s*\|.*\|\s*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"^#+\s+", "", t, flags=re.MULTILINE)
    return len(re.findall(r"\b[\w'-]+\b", t))


def first_paragraph(body: str) -> str:
    """The first prose paragraph of the body.

    Robust to:
    - a leftover H1 at the top (`parse_metadata` removes it, but accept both)
    - stray HTML comments that the `no_html` check will separately flag
    """
    after_h1 = re.sub(r"\A#\s+.+?\n+", "", body, count=1)
    for block in after_h1.split("\n\n"):
        stripped = block.strip()
        if not stripped:
            continue
        # Skip pure-comment paragraphs.
        if re.fullmatch(r"<!--.*?-->", stripped, flags=re.DOTALL):
            continue
        return stripped
    return ""


def first_two_sentences(body: str) -> tuple[str, int]:
    para = first_paragraph(body)
    sentences = re.split(r"(?<=[.!?])\s+", para)
    two = " ".join(sentences[:2]).strip()
    return two, len(re.findall(r"\b[\w'-]+\b", two))


def first_sentence(body: str) -> str:
    para = first_paragraph(body)
    return re.split(r"(?<=[.!?])\s+", para)[0].strip()


def extract_keyword_phrase(title: str) -> str:
    """Strip common interrogative prefixes and trailing punctuation to get the
    keyword phrase from a title.
    """
    t = re.sub(
        r"^(what\s+(is|are|does|do)|how\s+to|how\s+do\s+you|guide\s+to|"
        r"why|when|where|introduction\s+to|the\s+ultimate\s+guide\s+to)\s+",
        "",
        title,
        flags=re.IGNORECASE,
    )
    return t.rstrip("?.! ").strip()


# ---------- individual checks ----------


def check_metadata(meta: dict[str, str]) -> list[CheckResult]:
    results: list[CheckResult] = []
    for key in REQUIRED_METADATA:
        present = bool(meta.get(key))
        results.append(
            CheckResult(
                f"metadata_{key}",
                "PASS" if present else "FAIL",
                "" if present else "missing or empty",
            )
        )
    intent = meta.get("intent", "")
    if intent:
        ok = intent in VALID_INTENTS
        results.append(
            CheckResult(
                "metadata_intent_valid",
                "PASS" if ok else "FAIL",
                f"intent={intent}"
                + (f" (expected one of {sorted(VALID_INTENTS)})" if not ok else ""),
            )
        )
    return results


def check_meta_description(meta: dict[str, str]) -> CheckResult:
    md = meta.get("metaDescription", "")
    length = len(md)
    ok = 1 <= length <= 160
    return CheckResult(
        "meta_description_length",
        "PASS" if ok else "FAIL",
        f"{length} chars (max 160)" + ("" if md else " — missing"),
    )


def check_word_count(body: str, lo: int, hi: int) -> CheckResult:
    wc = word_count(body)
    if lo <= wc <= hi:
        return CheckResult("word_count", "PASS", f"{wc} words (target {lo}-{hi})")
    detail = f"{wc} words (target {lo}-{hi})"
    return CheckResult("word_count", "WARN", detail)


def check_answer_first(body: str) -> CheckResult:
    _, wc = first_two_sentences(body)
    ok = 40 <= wc <= 60
    return CheckResult(
        "answer_first_block",
        "PASS" if ok else "FAIL",
        f"first two sentences = {wc} words (target 40-60)",
    )


def check_tldr_word_count(body: str) -> CheckResult:
    """The TL;DR paragraph is the chunk AI engines extract as the citation
    candidate. The research-backed sweet spot is 120-160 words (94% of
    passages selected by Google AI Overviews fall in 134-167 words per the
    2025 ranking-factor study). Shorter paragraphs get passed over for
    longer, more self-contained competitor chunks.

    The TL;DR is the paragraph immediately after the answer-first block
    (i.e., the second substantive paragraph of the body, before any H2).
    """
    # Consider only paragraphs before the first H2.
    paragraphs: list[str] = []
    for p in body.split("\n\n"):
        stripped = p.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            break
        paragraphs.append(stripped)
    if len(paragraphs) < 2:
        return CheckResult(
            "tldr_word_count",
            "FAIL",
            "TL;DR paragraph not found (expected below the answer-first block, above the first H2)",
        )
    tldr = paragraphs[1]
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", tldr)
    wc = len(re.findall(r"\b[\w'-]+\b", plain))
    ok = 120 <= wc <= 160
    return CheckResult(
        "tldr_word_count",
        "PASS" if ok else "FAIL",
        f"TL;DR = {wc} words (target 120-160)",
    )


def check_keyword_in_sentence_1(meta: dict[str, str], body: str) -> CheckResult:
    """Sentence 1 must contain a recognizable form of the title's keyword phrase.

    Practical rule: LLMs tolerate morphology ("add X" <-> "Adding X"), so we
    don't require a literal substring match. The check passes if either:
      1. The full keyword phrase appears verbatim (the best case), or
      2. A 3-word subsequence from the phrase appears verbatim.

    For very short keyword phrases (<3 words) we fall back to requiring all
    the phrase's content words to appear somewhere in sentence 1.
    """
    title = meta.get("title", "")
    if not title:
        return CheckResult(
            "keyword_in_first_sentence",
            "FAIL",
            "no title (no H1 found)",
        )
    phrase = extract_keyword_phrase(title)
    s1 = first_sentence(body).lower()
    phrase_lower = phrase.lower()

    if phrase_lower in s1:
        return CheckResult(
            "keyword_in_first_sentence",
            "PASS",
            f"full phrase '{phrase}' found in sentence 1",
        )

    words = phrase_lower.split()
    if len(words) < 3:
        missing = [w for w in words if w not in s1]
        if not missing:
            return CheckResult(
                "keyword_in_first_sentence",
                "PASS",
                f"all keyword words present in sentence 1",
            )
        return CheckResult(
            "keyword_in_first_sentence",
            "FAIL",
            f"missing words from keyword '{phrase}': {missing}",
        )

    for i in range(len(words) - 2):
        trigram = " ".join(words[i : i + 3])
        if trigram in s1:
            return CheckResult(
                "keyword_in_first_sentence",
                "PASS",
                f"3-word match '{trigram}' found (full phrase '{phrase}' not literal)",
            )

    return CheckResult(
        "keyword_in_first_sentence",
        "FAIL",
        f"no 3-word subsequence of '{phrase}' found in sentence 1",
    )


def check_filler_opener(body: str) -> CheckResult:
    s1 = first_sentence(body)
    for pattern in FILLER_OPENERS:
        if re.match(pattern, s1, re.IGNORECASE):
            return CheckResult(
                "no_filler_opener",
                "FAIL",
                f"sentence 1 starts with a filler phrase: {s1[:50]}…",
            )
    return CheckResult("no_filler_opener", "PASS", "")


def check_em_dashes(text: str) -> CheckResult:
    count = text.count(EM_DASH)
    return CheckResult(
        "no_em_dashes",
        "PASS" if count == 0 else "FAIL",
        f"found {count} em dashes" if count else "0",
    )


def check_emojis(text: str) -> CheckResult:
    hits = EMOJI_PATTERN.findall(text)
    return CheckResult(
        "no_emojis",
        "PASS" if not hits else "FAIL",
        f"found {len(hits)} emoji(s)" if hits else "0",
    )


def check_forbidden_terms(text: str) -> CheckResult:
    hits: list[str] = []
    for pattern in FORBIDDEN_TERMS_ANY_CASE:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            hits.append(m.group(0))
    for pattern in FORBIDDEN_TERMS_CASE_SENSITIVE:
        for m in re.finditer(pattern, text):
            hits.append(m.group(0))
    return CheckResult(
        "no_forbidden_terms",
        "PASS" if not hits else "FAIL",
        "found: " + ", ".join(sorted(set(hits))) if hits else "0",
    )


def check_html_tags(body: str) -> CheckResult:
    """Forbid ALL HTML in the markdown intermediate. The final output is a Word
    document and a downstream automation converts it to Webflow HTML. HTML in
    the source corrupts both. Includes `<!-- comments -->`, which some
    markdown→docx converters render as visible text.
    """
    tag_hits = HTML_TAG_PATTERN.findall(body)
    comment_hits = re.findall(r"<!--.*?-->", body, flags=re.DOTALL)
    total = len(tag_hits) + len(comment_hits)
    if total == 0:
        return CheckResult("no_html", "PASS", "0")
    details = []
    if tag_hits:
        details.append(f"{len(tag_hits)} tag(s): {tag_hits[:3]}")
    if comment_hits:
        trimmed = [c[:40] + "…" if len(c) > 40 else c for c in comment_hits[:2]]
        details.append(f"{len(comment_hits)} comment(s): {trimmed}")
    return CheckResult("no_html", "FAIL", "; ".join(details))


def check_headings(body: str) -> list[CheckResult]:
    headings = HEADING_PATTERN.findall(body)
    levels = [len(h[0]) for h in headings]
    results: list[CheckResult] = []
    h1_count = levels.count(1)
    results.append(
        CheckResult(
            "single_h1",
            "PASS" if h1_count == 1 else "FAIL",
            f"found {h1_count} H1 heading(s)",
        )
    )
    skipped = any(b > a + 1 for a, b in zip(levels, levels[1:]))
    results.append(
        CheckResult(
            "no_skipped_heading_levels",
            "PASS" if not skipped else "FAIL",
            "well-formed" if not skipped else "a heading level was skipped",
        )
    )
    return results


def check_citations(body: str, intent: str) -> CheckResult:
    links = MARKDOWN_LINK_PATTERN.findall(body)
    external = [u for _, u in links if "social.plus" not in u]
    minimum = INTENT_CITATION_MIN.get(intent, 0)
    count = len(external)
    if minimum == 0:
        return CheckResult(
            "external_citations",
            "PASS",
            f"{count} external citation(s); intent={intent} (no minimum)",
        )
    ok = count >= minimum
    return CheckResult(
        "external_citations",
        "PASS" if ok else "FAIL",
        f"{count} external citation(s); intent={intent} (minimum {minimum})",
    )


def check_approved_customers(body: str) -> CheckResult:
    hits = WATCHED_UNAPPROVED.findall(body)
    unapproved = [h for h in hits if h not in APPROVED_CUSTOMERS]
    return CheckResult(
        "approved_customers_only",
        "PASS" if not unapproved else "FAIL",
        f"unapproved mentions: {sorted(set(unapproved))}" if unapproved else "0",
    )


def check_no_jsonld(body: str) -> CheckResult:
    """Webflow handles schema at the template level; the body should not emit
    JSON-LD. Catch the common fenced form.
    """
    if re.search(r"```json-ld", body, re.IGNORECASE):
        return CheckResult(
            "no_jsonld_block",
            "FAIL",
            "found a ```json-ld block — Webflow handles schema at the template level",
        )
    if re.search(r"application/ld\+json", body, re.IGNORECASE):
        return CheckResult(
            "no_jsonld_block",
            "FAIL",
            "found an inline JSON-LD script — Webflow handles schema",
        )
    return CheckResult("no_jsonld_block", "PASS", "")


# ---------- runner ----------


def run(path: Path, intent_override: str | None, lo: int | None, hi: int | None) -> Report:
    report = Report()
    text = path.read_text(encoding="utf-8")
    meta, body = parse_metadata(text)

    intent = intent_override or meta.get("intent", "")
    if intent not in VALID_INTENTS:
        intent = "definition"  # best-effort default for checks that need one

    if lo is None or hi is None:
        lo_default, hi_default = INTENT_WORD_RANGE.get(intent, (1000, 1600))
        lo = lo if lo is not None else lo_default
        hi = hi if hi is not None else hi_default

    # The check_headings check needs the full document (to count the single H1
    # that was consumed by parse_metadata). Reconstruct a pseudo-body with the
    # H1 re-inserted for that one check.
    body_with_h1 = f"# {meta.get('title', '')}\n\n{body}" if meta.get("title") else body

    report.results.extend(check_metadata(meta))
    report.results.append(check_meta_description(meta))
    report.results.append(check_word_count(body, lo, hi))
    report.results.append(check_answer_first(body))
    report.results.append(check_tldr_word_count(body))
    report.results.append(check_keyword_in_sentence_1(meta, body))
    report.results.append(check_filler_opener(body))
    report.results.append(check_em_dashes(body))
    report.results.append(check_emojis(body))
    report.results.append(check_forbidden_terms(body))
    report.results.append(check_html_tags(body))
    report.results.append(check_no_jsonld(body))
    report.results.extend(check_headings(body_with_h1))
    report.results.append(check_citations(body, intent))
    report.results.append(check_approved_customers(body))

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="AEO article compliance checker")
    parser.add_argument("path", type=Path, help="Path to the article markdown file")
    parser.add_argument(
        "--intent",
        choices=sorted(VALID_INTENTS),
        help="Override intent from metadata",
    )
    parser.add_argument("--min", type=int, help="Override minimum word count")
    parser.add_argument("--max", type=int, help="Override maximum word count")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"file not found: {args.path}", file=sys.stderr)
        return 2

    report = run(args.path, args.intent, args.min, args.max)

    if args.json:
        print(report.as_json())
    else:
        print(f"AEO compliance report for {args.path}\n")
        for r in report.results:
            line = f"  [{r.status:4}] {r.name}"
            if r.detail:
                line += f" — {r.detail}"
            print(line)
        print()
        n_fail = len(report.failed)
        n_warn = len(report.warned)
        if n_fail:
            print(f"{n_fail} failure(s), {n_warn} warning(s) — fix failures before delivery.")
        elif n_warn:
            print(f"No failures, {n_warn} warning(s) — review and decide whether to address.")
        else:
            print("All checks passed.")

    return 0 if not report.failed else 1


if __name__ == "__main__":
    sys.exit(main())
