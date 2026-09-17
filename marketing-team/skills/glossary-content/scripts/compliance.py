#!/usr/bin/env python3
"""
Glossary entry compliance checker.

Deterministic checks for glossary entries produced by the glossary-content
skill. Human / LLM judgment still owns tone, factuality, and citation
quality — this script owns the mechanical checks that slip past eyeball
review (word count, missing tables, forbidden vocabulary, metadata gaps).

The script reads the markdown intermediate (outputs/[slug].draft.md) that
the skill produces before conversion to .docx. Metadata lives in labeled
paragraphs directly under the H1:

    # Term

    Meta description: ...
    Slug: ...
    Alt text: ...
    Category: ...

    [definition paragraph starts here]

Usage:
    python scripts/compliance.py path/to/entry.draft.md
    python scripts/compliance.py path/to/entry.draft.md --keyword "active user"
    python scripts/compliance.py path/to/entry.draft.md --min 500 --max 900
    python scripts/compliance.py path/to/entry.draft.md --json

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


# Kept in sync with blog-seo-content/scripts/compliance.py and
# aeo-content/scripts/compliance.py — shared brand law / anti-slop tiers.
FORBIDDEN_TERMS_ANY_CASE = [
    r"\brevolutioni[sz]e\b",
    r"\bgame[- ]chang(ing|er)\b",
    r"\bunlock the power\b",
    r"(?<![-\w])leverag(e|es|ed|ing)\b",
    r"\bcutting[- ]edge\b",
    r"\bnext[- ]generation\b",
    r"\bbest[- ]in[- ]class\b",
    r"\bstate[- ]of[- ]the[- ]art\b",
    r"\bforum platform\b",
    r"\bchat tool\b",
    r"\bad[- ]network\b",
    r"\bguarantee[ds]?\s+(?:growth|retention|revenue|results?|outcomes?|success|engagement)\b",
    r"\bdelv(e|es|ed|ing)\b",
    r"\bin today[’']?s fast[- ]paced\b",
    r"\bdigital landscape\b",
    r"\bever[- ]evolving\b",
    r"\bpivotal\b",
    r"\bin the (?:realm|world) of\b",
]

SELF_REFERENTIAL_SOCIAL_NETWORK = [
    r"\bsocial\.plus\s+is\s+(?:a|an|the)?\s*social[- ]network\b",
    r"\bwe(?:'re|\s+are)\s+(?:a|an|the)?\s*social[- ]network\b",
]

RISKY_TERMS_WARN = [
    r"\bunlock\b",
    r"\belevate\b",
    r"\bseamless\b",
    r"\brobust\b",
]

REQUIRED_METADATA_FIELDS = ["Meta description", "Slug", "Category"]

REQUIRED_H2_KEYWORDS = {
    "why_it_matters": [r"why .* matters?", r"benefits? of"],
    "metrics_or_mechanism": [r"metric", r"measure", r"calculat", r"types? of", r"how .* works?"],
    "and_social_plus": [r"and social\.plus"],
    "related_terms": [r"related terms?"],
    "key_takeaways": [r"key takeaways?"],
}

TABLE_ROW_RE = re.compile(r"^\s*\|.+\|\s*$", re.MULTILINE)
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$", re.MULTILINE)


@dataclass
class CheckResult:
    name: str
    passed: bool
    level: str  # "FAIL" or "WARN"
    detail: str = ""


@dataclass
class Report:
    path: str
    checks: list = field(default_factory=list)

    def add(self, name: str, ok: bool, level: str, detail: str = "") -> None:
        self.checks.append(CheckResult(name, ok, level, detail))

    @property
    def has_failure(self) -> bool:
        return any((not c.passed) and c.level == "FAIL" for c in self.checks)

    def render(self) -> str:
        lines = [f"Glossary compliance report for {self.path}", ""]
        for c in self.checks:
            if c.passed:
                lines.append(f"  [PASS] {c.name}" + (f" — {c.detail}" if c.detail else ""))
            else:
                tag = "FAIL" if c.level == "FAIL" else "WARN"
                lines.append(f"  [{tag}] {c.name}" + (f" — {c.detail}" if c.detail else ""))
        lines.append("")
        lines.append("All checks passed." if not self.has_failure else "One or more checks FAILED.")
        return "\n".join(lines)

    def as_json(self) -> str:
        return json.dumps(
            {
                "path": self.path,
                "checks": [
                    {"name": c.name, "passed": c.passed, "level": c.level, "detail": c.detail}
                    for c in self.checks
                ],
                "result": "FAIL" if self.has_failure else "PASS",
            },
            indent=2,
        )


def parse_metadata(text: str) -> dict:
    meta = {}
    for line in text.splitlines():
        m = re.match(r"^\s*(Meta description|Slug|Alt text|Category)\s*:\s*(.+)$", line)
        if m:
            meta[m.group(1)] = m.group(2).strip()
    return meta


def get_h1(text: str) -> str | None:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def get_h2_headings(text: str) -> list[str]:
    return [m.strip() for m in re.findall(r"^##\s+(.+)$", text, re.MULTILINE)]


def get_intro_paragraph(text: str, meta_end_idx: int) -> str:
    """First non-empty paragraph after the metadata block, before the first H2."""
    remainder = text[meta_end_idx:]
    first_h2 = re.search(r"^##\s", remainder, re.MULTILINE)
    body = remainder[: first_h2.start()] if first_h2 else remainder
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    return paragraphs[0] if paragraphs else ""


def word_count(text: str) -> int:
    # Strip metadata lines and markdown table pipes from the count so the
    # length check reflects prose, not table syntax.
    body_lines = [
        l for l in text.splitlines()
        if not re.match(r"^\s*(Meta description|Slug|Alt text|Category)\s*:", l)
    ]
    body = "\n".join(body_lines)
    body = re.sub(r"^#.*$", "", body, flags=re.MULTILINE)  # drop headings from count? keep headings out only if desired
    words = re.findall(r"\b[\w’']+\b", body)
    return len(words)


def has_table(text: str) -> bool:
    return bool(TABLE_ROW_RE.search(text) and TABLE_SEPARATOR_RE.search(text))


def find_forbidden(text: str, patterns: list[str]) -> list[str]:
    hits = []
    for pat in patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            hits.append(m.group(0))
    return hits


def check_required_sections(headings: list[str]) -> dict:
    results = {}
    for key, patterns in REQUIRED_H2_KEYWORDS.items():
        found = any(
            any(re.search(p, h, re.IGNORECASE) for p in patterns) for h in headings
        )
        results[key] = found
    return results


def extract_section(text: str, heading_substring_patterns: list[str]) -> str:
    """Return the body text of the first H2 section whose heading matches any pattern."""
    headings = list(re.finditer(r"^##\s+(.+)$", text, re.MULTILINE))
    for i, h in enumerate(headings):
        if any(re.search(p, h.group(1), re.IGNORECASE) for p in heading_substring_patterns):
            start = h.end()
            end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
            return text[start:end]
    return ""


def count_bullets(section_text: str) -> int:
    return len(re.findall(r"^\s*[-*]\s+.+$", section_text, re.MULTILINE))


def count_links(section_text: str) -> int:
    return len(re.findall(r"\[[^\]]+\]\([^)]+\)", section_text))


def run_checks(text: str, path: str, keyword: str | None, min_words: int, max_words: int) -> Report:
    report = Report(path=path)

    # --- Metadata ---
    h1 = get_h1(text)
    report.add("metadata_title", bool(h1), "FAIL", h1 or "no H1 found")

    meta = parse_metadata(text)
    for field_name in REQUIRED_METADATA_FIELDS:
        report.add(
            f"metadata_{field_name.lower().replace(' ', '_')}",
            field_name in meta and bool(meta[field_name]),
            "FAIL",
            meta.get(field_name, "missing"),
        )

    if "Meta description" in meta:
        mdlen = len(meta["Meta description"])
        report.add(
            "meta_description_length",
            mdlen <= 160,
            "FAIL",
            f"{mdlen} chars (max 160)",
        )

    if "Slug" in meta:
        slug_ok = bool(re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", meta["Slug"]))
        report.add("slug_format", slug_ok, "FAIL", meta["Slug"])

    # --- Structure: single H1, required H2 sections, no H3s ---
    h1_count = len(re.findall(r"^#\s+", text, re.MULTILINE))
    report.add("single_h1", h1_count == 1, "FAIL", f"found {h1_count} H1 heading(s)")

    h3_count = len(re.findall(r"^###\s+", text, re.MULTILINE))
    report.add("no_h3_headings", h3_count == 0, "WARN", f"found {h3_count} H3 heading(s) — glossary entries should be flat")

    headings = get_h2_headings(text)
    section_hits = check_required_sections(headings)
    for key, found in section_hits.items():
        report.add(f"required_section_{key}", found, "FAIL", "not found among H2 headings" if not found else "")

    # --- Answer-first definition paragraph ---
    meta_lines_end = 0
    for fname in ["Meta description", "Slug", "Alt text", "Category"]:
        m = re.search(rf"^\s*{re.escape(fname)}\s*:.*$", text, re.MULTILINE)
        if m:
            meta_lines_end = max(meta_lines_end, m.end())
    intro = get_intro_paragraph(text, meta_lines_end)
    intro_words = len(re.findall(r"\b[\w’']+\b", intro))
    report.add(
        "answer_first_definition_length",
        0 < intro_words <= 50,
        "WARN",
        f"{intro_words} words (target 30-50)",
    )
    if keyword:
        kw_found = keyword.lower() in intro.lower()
        report.add("keyword_in_definition", kw_found, "FAIL", f"'{keyword}' in first paragraph")

    # --- Word count ---
    wc = word_count(text)
    report.add("word_count", min_words <= wc <= max_words, "WARN", f"{wc} words (target {min_words}-{max_words})")

    # --- Table requirement ---
    table_present = has_table(text)
    report.add(
        "has_table",
        table_present,
        "FAIL",
        "" if table_present else "no markdown table found — every glossary entry requires one",
    )

    # --- Key Takeaways ---
    kt_section = extract_section(text, REQUIRED_H2_KEYWORDS["key_takeaways"])
    kt_bullets = count_bullets(kt_section)
    report.add("key_takeaways_bullets", 3 <= kt_bullets <= 5, "WARN", f"{kt_bullets} bullets (target 3-5)")

    # --- Related Terms ---
    rt_section = extract_section(text, REQUIRED_H2_KEYWORDS["related_terms"])
    rt_links = count_links(rt_section)
    report.add("related_terms_links", rt_links >= 2, "FAIL", f"{rt_links} link(s) found (minimum 2)")

    # --- Vocabulary ---
    forbidden = find_forbidden(text, FORBIDDEN_TERMS_ANY_CASE)
    report.add("no_forbidden_terms", len(forbidden) == 0, "FAIL", f"found: {forbidden}" if forbidden else "")

    self_ref = find_forbidden(text, SELF_REFERENTIAL_SOCIAL_NETWORK)
    report.add("no_self_referential_social_network", len(self_ref) == 0, "FAIL", f"found: {self_ref}" if self_ref else "")

    risky = find_forbidden(text, RISKY_TERMS_WARN)
    report.add("risky_terms_check", len(risky) == 0, "WARN", f"found: {risky}" if risky else "")

    em_dashes = text.count("—")
    report.add("no_em_dashes", em_dashes == 0, "FAIL", f"{em_dashes} found")

    emoji_pattern = re.compile(
        "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]"
    )
    emoji_count = len(emoji_pattern.findall(text))
    report.add("no_emojis", emoji_count == 0, "FAIL", f"{emoji_count} found")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Glossary entry compliance checker")
    parser.add_argument("path", type=Path, help="Path to the .draft.md file")
    parser.add_argument("--keyword", default=None, help="Target term, to verify it appears in the definition paragraph")
    parser.add_argument("--min", type=int, default=500, help="Minimum word count (default 500)")
    parser.add_argument("--max", type=int, default=900, help="Maximum word count (default 900)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: {args.path} does not exist", file=sys.stderr)
        return 2

    text = args.path.read_text(encoding="utf-8")
    report = run_checks(text, str(args.path), args.keyword, args.min, args.max)

    print(report.as_json() if args.json else report.render())
    return 1 if report.has_failure else 0


if __name__ == "__main__":
    sys.exit(main())
