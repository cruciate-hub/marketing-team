#!/usr/bin/env python3
"""Targeted regression tests for glossary-content/scripts/compliance.py.
Fixtures are synthetic and deliberately minimal: each test asserts one named
check, not a full passing entry."""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "compliance.py"
FIX = HERE / "fixtures"
failures = []


def status(fixture, check, *extra):
    out = subprocess.run([sys.executable, str(SCRIPT), str(FIX / fixture), *extra], capture_output=True, text=True).stdout
    m = re.search(rf"\[(PASS|FAIL|WARN)\] {re.escape(check)}\b", out)
    return m.group(1) if m else None


def expect(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f" (got {got}, want {want})"))
    if not ok:
        failures.append(name)


print("Queue ID is required")
expect("draft with Queue ID passes metadata_queue_id", status("with-queue-id.draft.md", "metadata_queue_id"), "PASS")
expect("draft without Queue ID fails metadata_queue_id", status("without-queue-id.draft.md", "metadata_queue_id"), "FAIL")
expect("Queue ID line is not read as the definition paragraph",
       status("with-queue-id.draft.md", "keyword_in_definition", "--keyword", "churn rate"), "PASS")
expect("definition length is measured on the definition, not the Queue ID line",
       status("with-queue-id.draft.md", "answer_first_definition_length"), "PASS")

print()
print("ALL TESTS PASSED" if not failures else f"{len(failures)} FAILED: {failures}")
sys.exit(1 if failures else 0)
