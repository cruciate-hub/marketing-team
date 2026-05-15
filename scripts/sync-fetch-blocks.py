#!/usr/bin/env python3
"""
sync-fetch-blocks.py — propagate the canonical fetch block into every
fetch-using SKILL.md.

Workflow
--------
1. Edit scripts/canonical-fetch-block-v2.md (the single source of truth).
2. Run this script:    python3 scripts/sync-fetch-blocks.py
3. The canonical content is copied into the section between
       <!-- FETCH-BLOCK:START v2 -->
       <!-- FETCH-BLOCK:END v2 -->
   in every SKILL.md that has those markers (currently 11 fetch-using
   skills). SKILL.md files without the markers (legal-docs-formatter,
   link-building-vetter, svg-icon-transformer) are skipped — they
   don't fetch from GitHub.
4. Commit the canonical + the updated SKILL.md files together.

Companion to scripts/audit-skills.sh:
- audit-skills.sh (read-only)  — detects drift between canonical and the SKILL.md copies.
- sync-fetch-blocks.py (write) — prevents drift by overwriting copies from the canonical.

Run sync first, then audit. After a sync the audit should report 0 drift.

This script is idempotent: running it twice in a row leaves the second
run with zero changes.
"""

import sys
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parent.parent
CANONICAL   = REPO_ROOT / "scripts" / "canonical-fetch-block-v2.md"
SKILLS_DIR  = REPO_ROOT / "marketing-team" / "skills"
START_MARK  = "<!-- FETCH-BLOCK:START v2 -->"
END_MARK    = "<!-- FETCH-BLOCK:END v2 -->"


def sync_one(skill_md: Path, canonical_content: str):
    """Sync canonical into one SKILL.md.

    Returns one of: 'updated', 'unchanged', 'no-markers', 'malformed'.
    """
    text = skill_md.read_text()

    start_idx = text.find(START_MARK)
    end_idx   = text.find(END_MARK)

    if start_idx == -1 and end_idx == -1:
        return "no-markers"
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        return "malformed"

    # Content begins right after the newline that terminates the START marker line.
    nl_after_start = text.find("\n", start_idx)
    if nl_after_start == -1:
        return "malformed"
    content_start = nl_after_start + 1

    # Content ends at the start of the END marker line. The END marker is on its
    # own line, so we walk back from end_idx to the preceding newline (content
    # includes everything up to but not including the END marker line itself).
    content_end = end_idx

    new_text = text[:content_start] + canonical_content + text[content_end:]
    if new_text == text:
        return "unchanged"

    skill_md.write_text(new_text)
    return "updated"


def main():
    if not CANONICAL.exists():
        print(f"ERROR: canonical missing at {CANONICAL}", file=sys.stderr)
        return 2
    if not SKILLS_DIR.is_dir():
        print(f"ERROR: skills directory missing at {SKILLS_DIR}", file=sys.stderr)
        return 2

    canonical_content = CANONICAL.read_text()

    counts = {"updated": 0, "unchanged": 0, "no-markers": 0, "malformed": 0}

    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        rel = skill_md.relative_to(REPO_ROOT)
        status = sync_one(skill_md, canonical_content)
        counts[status] += 1

        if status == "updated":
            print(f"  updated:   {rel}")
        elif status == "malformed":
            print(f"  MALFORMED: {rel} — markers missing or out of order", file=sys.stderr)

    print()
    print(f"Canonical:                                  {CANONICAL.relative_to(REPO_ROOT)} ({len(canonical_content)} bytes)")
    print(f"Updated:                                    {counts['updated']}")
    print(f"Unchanged:                                  {counts['unchanged']}")
    print(f"Skipped (non-fetching, no markers):         {counts['no-markers']}")
    if counts['malformed']:
        print(f"MALFORMED (markers missing/out of order):   {counts['malformed']}")

    if counts['malformed']:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
