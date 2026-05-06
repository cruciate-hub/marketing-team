#!/usr/bin/env bash
# audit-skills.sh — verify every SKILL.md that fetches from GitHub uses the
# canonical fetch block (v1) verbatim. Exits non-zero on any drift or missing
# block in a skill that still references github.com.
#
# Run from the repo root:
#   ./scripts/audit-skills.sh
#
# Wire into CI / pre-commit to prevent silent drift across the 14+ skills.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANONICAL="$REPO_ROOT/scripts/canonical-fetch-block-v1.md"
START_MARK='<!-- FETCH-BLOCK:START v1 -->'
END_MARK='<!-- FETCH-BLOCK:END v1 -->'

if [ ! -f "$CANONICAL" ]; then
  echo "ERROR: canonical block missing at $CANONICAL" >&2
  exit 2
fi

EXPECTED_HASH=$(sha256sum "$CANONICAL" | awk '{print $1}')

drift=0
checked=0
skipped=0

# Extract the content between the markers (exclusive of the marker lines themselves).
extract_block() {
  awk -v start="$START_MARK" -v end="$END_MARK" '
    $0 ~ start { inside=1; next }
    $0 ~ end   { inside=0; next }
    inside     { print }
  ' "$1"
}

# Check whether a SKILL.md actually fetches from the marketing-team repo.
references_repo() {
  grep -qE 'github\.com/cruciate-hub/marketing-team|raw\.githubusercontent\.com/cruciate-hub/marketing-team|api\.github\.com/repos/cruciate-hub/marketing-team' "$1"
}

for skill in "$REPO_ROOT"/skills/skills/*/SKILL.md; do
  [ -f "$skill" ] || continue
  rel="${skill#$REPO_ROOT/}"

  block=$(extract_block "$skill")

  if [ -z "$block" ]; then
    if references_repo "$skill"; then
      echo "MISSING: $rel — references the repo but has no FETCH-BLOCK markers"
      drift=1
    else
      skipped=$((skipped + 1))
    fi
    continue
  fi

  hash=$(printf '%s\n' "$block" | sha256sum | awk '{print $1}')
  if [ "$hash" != "$EXPECTED_HASH" ]; then
    echo "DRIFT:   $rel"
    drift=1
  fi
  checked=$((checked + 1))
done

echo
echo "Checked: $checked   Skipped (no fetches): $skipped   Drift: $drift"
exit "$drift"
