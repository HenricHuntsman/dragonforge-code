#!/usr/bin/env bash
set -euo pipefail
src="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
dest="$HOME/dev/opencode-n64-lab"
if [[ -e "$dest" ]]; then
  echo "Refusing to overwrite existing lab: $dest" >&2
  exit 1
fi
mkdir -p "$HOME/dev"
cp -a "$src" "$dest"
cd "$dest"
git init -q
echo "Created isolated N64 starter at: $dest"
echo "No changes were made to the OpenCode or TraceForge repositories."
echo "Next: cd \"$dest\" && python3 -m unittest discover -s tests -v"
