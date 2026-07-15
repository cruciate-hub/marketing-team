#!/usr/bin/env bash
# install-git-hooks.sh — one-time local setup for the private-file pre-commit
# guard. .gitignore already blocks normal adds; this hook is the second belt
# against `git add -f`, renames that dodge a pattern, and future slips.
#
#   ./scripts/install-git-hooks.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK="$REPO_ROOT/.git/hooks/pre-commit"

cat > "$HOOK" << 'EOF'
#!/usr/bin/env bash
# Pre-commit guard: this repo is PUBLIC. Block known-private patterns from
# ever being committed, even via `git add -f`. Mirrors .gitignore policy
# and the CI private-file guard (.github/workflows/ci.yml).
set -euo pipefail

blocked=$(git diff --cached --name-only --diff-filter=A | grep -E \
  '^(scenario-.*\.json|prompt-.*\.txt|workers/|emails/(email-module-|lead-|marops-|scenario-))|(^|/)\.DS_Store$' \
  || true)

if [ -n "$blocked" ]; then
  echo "BLOCKED: attempting to commit private/internal files to the PUBLIC repo:" >&2
  echo "$blocked" >&2
  echo "These stay local (see .gitignore policy block). Unstage them: git restore --staged <file>" >&2
  exit 1
fi
EOF

chmod +x "$HOOK"
echo "Installed pre-commit guard at $HOOK"
