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
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

MT_REPO = Path(os.environ.get("MT_REPO", "/tmp/cruciate-hub-marketing-team"))


def _read_text_safe(path: Path) -> str:
    """Try UTF-8 (with BOM strip) first; fall back to cp1252 — same pattern
    as blog-seo-content/scripts/compliance.py's _read_draft(), for the same
    reason: prose pasted from Word emits 0x97 for the em dash, which is
    valid cp1252 but not valid UTF-8. Raises UnicodeDecodeError if neither
    decodes, for the caller to handle (main() exits cleanly; a compliance
    check FAILs gracefully instead of crashing the whole script).
    """
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp1252")


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
        self.add_result(CheckResult(name, ok, level, detail))

    def add_result(self, result: CheckResult) -> None:
        self.checks.append(result)

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


def extract_urls(section_text: str) -> list[str]:
    urls = []
    for _, url in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", section_text):
        # A markdown link may carry a trailing title, e.g. (URL "title") — keep just the URL.
        urls.append(url.split(" ", 1)[0].strip())
    return urls


def _normalize_url(u: str) -> str:
    # Intentionally NOT case-folded: social.plus URLs are canonically lowercase,
    # and folding case would make a mistyped/altered-case URL pass as "the same"
    # URL the optimizer actually proposed, defeating the exact-match guarantee
    # this check exists to provide. Only whitespace and a trailing slash are
    # normalized away, since those are cosmetic, not identity-changing.
    return u.strip().rstrip("/")


def extract_evidence_targets(evidence_text: str) -> set[str]:
    """URLs the optimizer actually proposed as **Target:** lines in its output block."""
    return {_normalize_url(u) for u in re.findall(r"\*\*Target:\*\*\s*(\S+)", evidence_text)}


def _load_known_glossary_and_answers_urls() -> set[str] | None:
    """Normalized URLs from the site's own glossary/answers inventory.

    Returns None (not an empty set) when neither snapshot is readable, so
    callers can distinguish "checked, and every URL is real" from "couldn't
    check" instead of treating an unreachable clone as license to fabricate
    URLs. Mirrors the read pattern in aeo-content/scripts/duplicate_check.py.
    """
    urls: set[str] = set()
    read_any = False
    for rel in ("website/pages-glossary.json", "website/pages-answers.json"):
        p = MT_REPO / rel
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        pages = data.get("pages") if isinstance(data, dict) else data
        if not isinstance(pages, list):
            continue
        read_any = True
        for page in pages:
            u = page.get("url") if isinstance(page, dict) else None
            if u:
                urls.add(_normalize_url(u))
    return urls if read_any else None


def check_links_evidence(rt_section: str, path: str) -> CheckResult:
    """Sibling-file backstop for the internal-linking-strategist invocation.

    This cannot prove the optimizer's two-phase process actually ran — an
    agent can still hand-type a fake evidence file with plausible-looking
    Anchor/Target/Reasoning lines for URLs that happen to be real. What it
    catches: the invocation being skipped entirely (no evidence file, or one
    that doesn't structurally match the optimizer's real output format); a
    bare header with copy-pasted Target lines and no actual Anchor/Reasoning
    content per suggestion; a Related Terms URL that doesn't exactly match a
    Target line (case-sensitive — see _normalize_url); and, when the site's
    glossary/answers inventory snapshots are readable, a Related Terms URL
    that doesn't correspond to any real published page at all. That last
    check degrades silently to "not checked" (not "passed") when the
    inventory snapshots aren't reachable, since an unreachable clone is not
    evidence that a URL is real.
    """
    rt_urls = {_normalize_url(u) for u in extract_urls(rt_section)}
    if not rt_urls:
        # related_terms_links (above) already FAILs the draft on <2 links,
        # so this branch only fires alongside that FAIL, never on its own.
        return CheckResult("links_evidence_file", False, "WARN", "no Related Terms links to verify — see related_terms_links above")

    if not str(path).endswith(".draft.md"):
        return CheckResult(
            "links_evidence_file",
            False,
            "FAIL",
            f"draft path '{path}' doesn't end in .draft.md — can't derive the sibling evidence file name. "
            "Name the draft outputs/[slug].draft.md per the skill's own convention.",
        )

    links_path = Path(str(path)[: -len(".draft.md")] + ".links.md")
    if not links_path.exists():
        return CheckResult(
            "links_evidence_file",
            False,
            "FAIL",
            f"expected {links_path.name} (the internal-linking-strategist output block) alongside the draft — not found. "
            "See SKILL.md 'Required evidence': Related Terms links must come from a real invocation, not a manual lookup.",
        )

    try:
        evidence_text = _read_text_safe(links_path)
    except UnicodeDecodeError as e:
        return CheckResult(
            "links_evidence_file",
            False,
            "FAIL",
            f"{links_path.name} could not be decoded as utf-8 or cp1252 ({e}) — "
            "re-save it as plain UTF-8.",
        )

    if "## Internal link suggestions" not in evidence_text:
        return CheckResult(
            "links_evidence_file",
            False,
            "FAIL",
            f"{links_path.name} exists but is missing the '## Internal link suggestions' header — "
            "this is not the optimizer's real output format.",
        )

    # Require actual suggestion content, not just a header plus copy-pasted
    # Target lines: a bare "## Internal link suggestions\n**Target:** url" with
    # nothing else would otherwise satisfy every check below despite never
    # having been touched by the real optimizer output.
    anchor_count = len(re.findall(r"\*\*Anchor:\*\*", evidence_text))
    reasoning_count = len(re.findall(r"\*\*Reasoning:\*\*", evidence_text))
    if anchor_count < len(rt_urls) or reasoning_count < len(rt_urls):
        return CheckResult(
            "links_evidence_file",
            False,
            "FAIL",
            f"{links_path.name} has {anchor_count} **Anchor:** and {reasoning_count} **Reasoning:** "
            f"line(s) but {len(rt_urls)} Related Terms URL(s) — a real optimizer suggestion has "
            "an Anchor and a Reasoning alongside every Target, not a bare URL list.",
        )

    evidence_targets = extract_evidence_targets(evidence_text)
    missing = sorted(u for u in rt_urls if u not in evidence_targets)
    if missing:
        return CheckResult(
            "links_evidence_file",
            False,
            "FAIL",
            f"Related Terms URL(s) not listed as a **Target:** in {links_path.name}: {missing}",
        )

    known_urls = _load_known_glossary_and_answers_urls()
    if known_urls is not None:
        unknown = sorted(u for u in rt_urls if u not in known_urls)
        if unknown:
            return CheckResult(
                "links_evidence_file",
                False,
                "FAIL",
                f"Related Terms URL(s) not found in website/pages-glossary.json or "
                f"pages-answers.json — likely fabricated: {unknown}",
            )

    inventory_note = "confirmed against site inventory" if known_urls is not None else "site inventory unreadable, not confirmed"
    return CheckResult(
        "links_evidence_file",
        True,
        "PASS",
        f"all {len(rt_urls)} Related Terms URL(s) match an Anchor/Target/Reasoning suggestion in "
        f"{links_path.name} ({inventory_note})",
    )


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

    # Related Terms must be the final H2 — it's the internal-linking section,
    # and the last thing on the page is where a reader (or an AI engine
    # extracting the page) most reliably still sees outbound links. Presence
    # alone (the check above) doesn't catch it landing in the wrong position.
    rt_last = bool(headings) and any(
        re.search(p, headings[-1], re.IGNORECASE) for p in REQUIRED_H2_KEYWORDS["related_terms"]
    )
    report.add(
        "related_terms_is_last_section",
        rt_last,
        "FAIL",
        "" if rt_last else (f"last H2 is '{headings[-1]}'" if headings else "no H2 headings found"),
    )

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
    report.add_result(check_links_evidence(rt_section, path))

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

    try:
        text = _read_text_safe(args.path)
    except UnicodeDecodeError as e:
        print(f"Error: could not decode {args.path} as utf-8 or cp1252: {e}", file=sys.stderr)
        return 2
    report = run_checks(text, str(args.path), args.keyword, args.min, args.max)

    print(report.as_json() if args.json else report.render())
    return 1 if report.has_failure else 0


if __name__ == "__main__":
    sys.exit(main())
