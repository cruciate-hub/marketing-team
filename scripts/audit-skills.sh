#!/usr/bin/env bash
# audit-skills.sh — repo-wide drift audit:
#
#   1. Fetch-block coherence — every fetch-using SKILL.md contains the
#      canonical fetch block (v2) verbatim.
#   2. Manifest coherence — every plugin entry's `version` in
#      `.claude-plugin/marketplace.json` matches the corresponding plugin's
#      own `plugin.json` `version`.
#   3. brand-kit symlink integrity — every entry under `brand-kit/skills/` is
#      a real symlink (mode 120000) pointing at an existing skill folder
#      under `skills/skills/`, with a readable SKILL.md at the target.
#
# Run from the repo root:
#   ./scripts/audit-skills.sh
#
# Wire into CI / pre-commit to prevent silent drift across the 14+ skills
# and the meta-plugin (brand-kit).

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

# ---------------------------------------------------------------------------
# Check 2 — manifest version coherence
# ---------------------------------------------------------------------------

manifest_drift=0
MARKETPLACE_JSON="$REPO_ROOT/.claude-plugin/marketplace.json"

if [ -f "$MARKETPLACE_JSON" ]; then
  while IFS=$'\t' read -r plugin_name plugin_source plugin_market_version; do
    [ -n "$plugin_name" ] || continue
    plugin_json="$REPO_ROOT/${plugin_source#./}/.claude-plugin/plugin.json"
    if [ ! -f "$plugin_json" ]; then
      echo "MISSING:    $plugin_name — plugin.json not found at ${plugin_json#$REPO_ROOT/}"
      manifest_drift=1
      continue
    fi
    plugin_local_version=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['version'])" "$plugin_json")
    if [ "$plugin_market_version" != "$plugin_local_version" ]; then
      echo "VERSION MISMATCH: $plugin_name — marketplace.json=$plugin_market_version, plugin.json=$plugin_local_version"
      manifest_drift=1
    fi
  done < <(python3 -c '
import json, sys
m = json.load(open(sys.argv[1]))
for p in m.get("plugins", []):
    print("\t".join([p.get("name",""), p.get("source",""), p.get("version","")]))
' "$MARKETPLACE_JSON")
else
  echo "ERROR: marketplace.json missing at $MARKETPLACE_JSON" >&2
  manifest_drift=1
fi

# ---------------------------------------------------------------------------
# Check 3 — brand-kit symlink integrity
# ---------------------------------------------------------------------------

symlink_drift=0
symlinks_checked=0
BRAND_KIT_SKILLS_DIR="$REPO_ROOT/brand-kit/skills"

if [ -d "$BRAND_KIT_SKILLS_DIR" ]; then
  for entry in "$BRAND_KIT_SKILLS_DIR"/*; do
    [ -e "$entry" ] || [ -L "$entry" ] || continue
    name="$(basename "$entry")"
    rel="brand-kit/skills/$name"

    if [ ! -L "$entry" ]; then
      echo "NOT A SYMLINK: $rel — should be a symlink to ../../skills/skills/$name"
      symlink_drift=1
      continue
    fi

    target=$(readlink "$entry")
    expected="../../skills/skills/$name"
    if [ "$target" != "$expected" ]; then
      echo "UNEXPECTED TARGET: $rel -> $target (expected $expected)"
      symlink_drift=1
    fi

    if [ ! -r "$entry/SKILL.md" ]; then
      echo "BROKEN SYMLINK: $rel -> $target (target SKILL.md unreadable)"
      symlink_drift=1
    fi

    symlinks_checked=$((symlinks_checked + 1))
  done
else
  echo "WARN: brand-kit/skills/ not found — meta-plugin missing? Skipping symlink check."
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

total_drift=$((drift + manifest_drift + symlink_drift))

echo
echo "Fetch-blocks:  $checked checked, $skipped skipped (non-fetching), $drift drift"
echo "Manifests:     coherence drift = $manifest_drift"
echo "Symlinks:      $symlinks_checked checked, $symlink_drift drift"
echo "TOTAL DRIFT:   $total_drift"

exit "$total_drift"
