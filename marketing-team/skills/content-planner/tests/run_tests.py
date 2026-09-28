#!/usr/bin/env python3
"""Regression tests for content-planner. Fixtures are synthetic."""
import csv
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "plan_rows.py"
FIX = HERE / "fixtures"
failures = []


def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


def run(cands, out):
    return subprocess.run([sys.executable, str(SCRIPT), "--candidates", str(FIX / cands), "--queue",
                           str(FIX / "queue-sample.csv"), "--seed", "retention test", "--date", "2026-09-24",
                           "--out-dir", out], capture_output=True, text=True)


with tempfile.TemporaryDirectory() as out:
    print("valid batch")
    p = run("candidates-valid.json", out)
    check("exits 0", p.returncode == 0, p.stdout + p.stderr)
    rows = list(csv.DictReader(open(Path(out) / "plan-retention-test.csv")))
    report = (Path(out) / "plan-retention-test.md").read_text()
    by_q = {r["Canonical question"]: r for r in rows}
    check("new glossary term gets next GL id", by_q.get("What is Day 7 retention?", {}).get("ID") == "GL5")
    check("first Answer id is AN1", any(r["ID"] == "AN1" for r in rows))
    check("pending data -> Blocked", by_q.get("What platform data shows about community and retention", {}).get("Status") == "Blocked: needs data")
    check("batch ref dependency resolved to new id", by_q.get("What platform data shows about community and retention", {}).get("Dependencies") == "GL5; A1")
    check("synonym of planned row -> Merge", "**Merge**" in report and "A1" in report and "How do you improve app retention?" not in by_q)
    check("same as published page -> Update existing", "**Update existing**" in report and "What is churn rate?" not in by_q)
    check("previously rejected -> Reject", "**Reject**" in report and "What is the best time to send push notifications?" not in by_q)
    check("legacy page scheduled for removal is ignored", "Why does community retention drop in 2026?" in by_q)
    check("friendly blog intent is canonicalised", by_q.get("What platform data shows about community and retention", {}).get("Intent") == "original-research")
    check("year warning", "year in an evergreen question" in report)
    check("premise warning", "no premise source" in report)
    check("header matches Queue columns", list(rows[0].keys())[0] == "ID" and len(rows[0]) == 26)

    print("invalid batch")
    p = run("candidates-invalid.json", out)
    check("exits 1 and writes nothing", p.returncode == 1 and "RESULT: INVALID" in p.stdout)
    for needle in ["Glossary questions are 'What is [term]?'", "intent 'definition' not valid for Answer",
                   "at least 2 sub-questions", "dependency 'NOPE'", "look like the same question"]:
        check(f"reports: {needle}", needle in p.stdout, p.stdout)

print()
print("ALL TESTS PASSED" if not failures else f"{len(failures)} FAILED: {failures}")
sys.exit(1 if failures else 0)
