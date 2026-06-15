#!/usr/bin/env python3
"""Regression tests for blog-seo-content/scripts/compliance.py.

Each fixture in tests/fixtures/ asserts one targeted behavior. The runner
executes the script against every fixture, parses [PASS]/[FAIL]/[WARN]
markers, and compares against the per-fixture expectations below. Exit 0
when every fixture behaves as documented; exit 1 with a diff on any drift.

Usage:
    python3 tests/run_tests.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "compliance.py"
FIXTURES = HERE / "fixtures"

# Per-fixture expectations.
# - must_fail / must_warn / must_pass: checks that MUST appear with that status
# - must_not_fail: checks that MUST NOT be FAIL (PASS or WARN is fine)
# - exit_code: expected process exit code (default 1 if any must_fail, else 0)
EXPECTATIONS: dict[str, dict] = {
    "F1-code-heading": {
        "must_pass": ["single_h1", "no_skipped_heading_levels"],
        "must_not_fail": ["single_h1", "no_skipped_heading_levels"],
        "note": "code-block `# ...` lines must not count as real headings",
    },
    "F2-h1-h3-house-style": {
        "must_warn": ["no_skipped_heading_levels"],
        "must_not_fail": ["no_skipped_heading_levels"],
        "note": "H1→H3 (19% of live posts) must WARN, not FAIL",
        "exit_code": 0,
    },
    "F4-emoji-gaps": {
        "must_fail": ["no_emojis"],
        "note": "⏰ ℹ ▶ (U+23F0, U+2139, U+25B6) must trigger no_emojis",
    },
    "F5-autolink": {
        "must_pass": ["no_html"],
        "must_not_fail": ["no_html"],
        "note": "CommonMark autolinks <https://…> are valid markdown, not HTML",
        "exit_code": 0,
    },
    "F6-smart-apostrophe": {
        "must_pass": ["keyword_in_first_paragraph"],
        "must_not_fail": ["keyword_in_first_paragraph"],
        "note": "curly vs straight apostrophe in the keyword must not false-fail",
        "exit_code": 0,
    },
    "F7-alt-violations": {
        "must_fail": ["no_em_dashes", "no_forbidden_terms"],
        "note": "alt text is reader-facing — em-dash + forbidden terms must fire",
    },
    "F8-cp1252": {
        "must_fail": ["no_em_dashes"],
        "note": "cp1252-encoded em-dash (0x97) must be detected, not crash",
    },
    "F9-bold-filler": {
        "must_fail": ["no_filler_opener"],
        "note": "filler opener wrapped in `**` markdown emphasis must still match",
    },
    "F10-reading-time": {
        "must_warn": ["reading_time"],
        "note": "claimed Minutes to read vs computed (~250 wpm) must reconcile",
    },
    "F11-high-leverage": {
        "must_pass": ["no_forbidden_terms"],
        "must_not_fail": ["no_forbidden_terms"],
        "note": "hyphenated 'higher-leverage' is strategy English, not fluff",
        "exit_code": 0,
    },
}

CHECK_LINE = re.compile(r"\[(PASS|FAIL|WARN)\s*\]\s+(\S+)")


def run_fixture(fixture_path: Path) -> tuple[int, dict[str, str]]:
    """Invoke compliance.py on `fixture_path`. Return (exit_code, {check: status})."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(fixture_path)],
        capture_output=True,
        text=True,
    )
    statuses: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        m = CHECK_LINE.search(line)
        if m:
            statuses[m.group(2)] = m.group(1)
    return proc.returncode, statuses


def main() -> int:
    if not SCRIPT.exists():
        print(f"compliance.py not found at {SCRIPT}", file=sys.stderr)
        return 2
    if not FIXTURES.exists():
        print(f"fixtures dir not found at {FIXTURES}", file=sys.stderr)
        return 2

    failures: list[str] = []
    for name, exp in sorted(EXPECTATIONS.items()):
        path = FIXTURES / f"{name}.md"
        if not path.exists():
            failures.append(f"MISSING fixture: {path}")
            continue
        exit_code, statuses = run_fixture(path)
        problems: list[str] = []
        for chk in exp.get("must_fail", []):
            if statuses.get(chk) != "FAIL":
                problems.append(f"  expected {chk}=FAIL, got {statuses.get(chk, '<absent>')}")
        for chk in exp.get("must_warn", []):
            if statuses.get(chk) != "WARN":
                problems.append(f"  expected {chk}=WARN, got {statuses.get(chk, '<absent>')}")
        for chk in exp.get("must_pass", []):
            if statuses.get(chk) != "PASS":
                problems.append(f"  expected {chk}=PASS, got {statuses.get(chk, '<absent>')}")
        for chk in exp.get("must_not_fail", []):
            if statuses.get(chk) == "FAIL":
                problems.append(f"  expected {chk}!=FAIL, got FAIL")
        if "exit_code" in exp and exit_code != exp["exit_code"]:
            problems.append(f"  expected exit {exp['exit_code']}, got {exit_code}")
        if problems:
            failures.append(f"❌ {name}: {exp.get('note', '')}\n" + "\n".join(problems))
        else:
            print(f"✓ {name}: {exp.get('note', '')}")

    print()
    if failures:
        print(f"{len(failures)} fixture(s) drifted:\n")
        for f in failures:
            print(f)
        return 1
    print(f"All {len(EXPECTATIONS)} fixtures behave as expected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
