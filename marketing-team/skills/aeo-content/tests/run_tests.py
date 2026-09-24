#!/usr/bin/env python3
"""Regression tests for aeo-content v2 scripts. Run from anywhere:
    python3 marketing-team/skills/aeo-content/tests/run_tests.py
Fixtures are synthetic test drafts, not publishable content."""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
ROOT = SKILL.parents[1].parent
COMPLIANCE = SKILL / "scripts" / "compliance.py"
FIX = HERE / "fixtures"
sys.path.insert(0, str(ROOT / "scripts"))
from intent_match import score, LIKELY_DUPLICATE, NEEDS_REVIEW  # noqa: E402

failures = []


def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


def run(fx):
    p = subprocess.run([sys.executable, str(COMPLIANCE), str(FIX / fx)], capture_output=True, text=True)
    return p.returncode, p.stdout


print("compliance: compliant v2 draft")
code, out = run("pass-how-to.draft.md")
check("exits 0", code == 0, out)
check("fingerprint string present", "AEO compliance report for" in out)

print("compliance: legacy permutation draft")
code, out = run("fail-legacy.draft.md")
check("exits 1", code == 1)
for name in ["metadata_intent_valid", "no_em_dashes", "no_forbidden_terms", "question_headings",
             "has_table", "statistics_count", "no_boilerplate_headings", "promotion_clean_extraction_blocks",
             "conclusion", "editor_line_present", "no_filler_opener"]:
    check(f"flags {name}", re.search(rf"\[FAIL\] {name}\b", out) is not None)

print("compliance: FAQ overlap against a queue")
p = subprocess.run([sys.executable, str(COMPLIANCE), str(FIX / "pass-how-to.draft.md"), "--queue",
                    str(FIX / "queue-sample.csv")], capture_output=True, text=True)
check("FAQ that duplicates row A3 is flagged", "[FAIL] faq_queue_overlap" in p.stdout and "A3" in p.stdout, p.stdout)
check("rejected rows and the page's own row are ignored", "X9" not in p.stdout and "TEST-001" not in p.stdout)

print("intent_match")
check("vehicle-noun permutation is a likely duplicate",
      score("SDK for Building Community Features in Apps", "", "Tool for Building Community Features in Apps", "") >= LIKELY_DUPLICATE)
check("improve/increase synonym is a likely duplicate",
      score("How to Improve Community Retention", "", "How to Increase Online Community Retention", "") >= LIKELY_DUPLICATE)
check("distinct questions stay below review",
      score("Should you build or buy social features for your app?", "", "How much does it cost to build in-app chat?", "") < NEEDS_REVIEW)

print("intent_match: glossary cases (shared matcher)")
check("rephrased definition of the same term is a likely duplicate",
      score("What is app retention?", "", "What does app retention mean?", "") >= LIKELY_DUPLICATE)
check("synonym terms are a likely duplicate",
      score("What is in-app messaging?", "", "What is in-app chat?", "") >= LIKELY_DUPLICATE)
check("different terms do not match",
      score("What is app retention?", "", "What is churn rate?", "") < NEEDS_REVIEW)

print("evidence bank and compliance whitelist agree")
bank = (ROOT / "messaging" / "evidence-bank.md").read_text()
src = COMPLIANCE.read_text()
wl = set(re.findall(r'"([^"]+)"', re.search(r"APPROVED_CUSTOMERS = \{(.+?)\}", src).group(1)))
bank_customers = set(re.findall(r"^\| Customer: ([^|]+?) \|", bank, re.MULTILINE))
check("same approved customers", wl == bank_customers, f"script={sorted(wl)} bank={sorted(bank_customers)}")

print()
print("ALL TESTS PASSED" if not failures else f"{len(failures)} FAILED: {failures}")
sys.exit(1 if failures else 0)
