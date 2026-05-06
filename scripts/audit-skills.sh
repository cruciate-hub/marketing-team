#!/usr/bin/env bash
# audit-skills.sh — verify every SKILL.md that uses the shared fetch
# architecture contains the canonical fetch block (v2) verbatim.
#
# Run from the repo root:
#   ./scripts/audit-skills.sh
#
# Wire into CI / pre-commit to prevent silent drift across the 14+ skills.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANONICAL="$REPO_ROOT/scripts/canonical-fetch-block-v2.md"
START_MARK='<!-- FETCH-BLOCK:START v2 -->'
END_MARK='<!-- FETCH-BLOCK:END v2 -->'

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

# Skills that genuinely don't need to fetch from the repo. Listed explicitly so
# any new skill that needs fetching but lacks the block is caught.
NON_FETCHING_SKILLS=(
  "link-building-vetter"
  "legal-docs-formatter"
  "svg-icon-transformer"
)

is_non_fetching() {
  local name="$1"
  for ns in "${NON_FETCHING_SKILLS[@]}"; do
    [ "$ns" = "$name" ] && return 0
  done
  return 1
}

for skill in "$REPO_ROOT"/skills/skills/*/SKILL.md; do
  [ -f "$skill" ] || continue
  rel="${skill#$REPO_ROOT/}"
  name="$(basename "$(dirname "$skill")")"

  block=$(extract_block "$skill")

  if [ -z "$block" ]; then
    if is_non_fetching "$name"; then
      skipped=$((skipped + 1))
    else
      echo "MISSING: $rel — fetch-using skill but has no FETCH-BLOCK markers"
      drift=1
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
echo "Checked: $checked   Skipped (non-fetching): $skipped   Drift: $drift"
exit "$drift"
