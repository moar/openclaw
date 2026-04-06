#!/usr/bin/env bash
set -euo pipefail

msg="${1:-}"
if [[ -z "$msg" ]]; then
  echo "Usage: $0 \"commit message\"" >&2
  exit 2
fi

repo_root="${2:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
cd "$repo_root"

if git diff --quiet && git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

git add -A
git commit -m "$msg"
git push
