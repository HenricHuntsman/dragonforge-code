#!/usr/bin/env bash
set -euo pipefail
src="$(cd -- "$(dirname -- "$0")" && pwd)"
dest="$HOME/dev/dragonforge-n64-lab"
[[ -n "$(printenv DRAGONFORGE_N64_DEST || true)" ]] && dest="$DRAGONFORGE_N64_DEST"
if [[ -e "$dest" || -L "$dest" ]]; then
  echo "Refusing to overwrite existing N64 lab: $dest" >&2
  exit 1
fi
mkdir -p "$(dirname -- "$dest")"
cp -a "$src" "$dest"
echo "Created isolated N64 lab: $dest. Existing projects unchanged."
