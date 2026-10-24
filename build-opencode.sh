#!/usr/bin/env bash
# Build current main safely in a separately managed checkout.
set -euo pipefail
ROOT="${OC_MODES_ROOT:-${HOME}/.local/share/opencode-modes}"
SRC="$ROOT/source"
BINDIR="$ROOT/bin"
BIN="$BINDIR/opencode"
EXPECTED='https://github.com/HenricHuntsman/opencode.git'

for dependency in git go; do
    if ! command -v "$dependency" >/dev/null 2>&1; then
        printf 'Missing prerequisite: %s\n' "$dependency" >&2
        exit 1
    fi
done

if [[ -L "$ROOT" || -L "$SRC" || -L "$BINDIR" ]]; then
    echo 'Refusing symbolic-link build directories.' >&2
    exit 1
fi
mkdir -p "$ROOT"

if [[ ! -e "$SRC" ]]; then
    echo 'Cloning a separate OpenCode build checkout.'
    git clone --branch main --single-branch "$EXPECTED" "$SRC"
else
    [[ -d "$SRC/.git" ]] || { echo 'Source path exists but is not a Git checkout.' >&2; exit 1; }
fi
[[ "$(git -C "$SRC" remote get-url origin)" == "$EXPECTED" ]] || { echo 'Wrong Git remote. Stopping.' >&2; exit 1; }
[[ "$(git -C "$SRC" branch --show-current)" == main ]] || { echo 'Build checkout is not on main. Stopping.' >&2; exit 1; }
[[ -z "$(git -C "$SRC" status --porcelain)" ]] || { echo 'Build checkout has local changes. Stopping.' >&2; exit 1; }

echo 'Fetching current public main...'
git -C "$SRC" fetch origin main --tags
if ! git -C "$SRC" merge-base --is-ancestor HEAD origin/main; then
    echo 'Build checkout diverged from origin/main. Stopping.' >&2
    exit 1
fi
git -C "$SRC" merge --ff-only origin/main

printf 'Building commit: '
git -C "$SRC" rev-parse --short HEAD

cd "$SRC" || exit 1
printf '\n=== GO VERSION ===\n'
go version
printf '\n=== VERIFY DEPENDENCIES ===\n'
go mod verify
printf '\n=== VET ===\n'
go vet ./...
printf '\n=== TEST ===\n'
go test ./... -count=1
printf '\n=== BUILD ===\n'
mkdir -p "$BINDIR"
staged="$(mktemp "$BINDIR/.opencode.new.XXXXXXXX")"
trap 'rm -f -- "$staged"' EXIT
go build -o "$staged" .
chmod 0755 "$staged"
"$staged" --version
mv -f -- "$staged" "$BIN"
trap - EXIT
printf '\nSUCCESS: %s\n' "$BIN"
"$BIN" --version
printf 'Verified commit: '
git rev-parse --short HEAD
printf '\nExisting Ubuntu dev checkout and TraceForge were not changed.\n'
