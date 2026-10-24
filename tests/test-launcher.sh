#!/usr/bin/env bash
set -euo pipefail
p="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
export HOME="$tmp/home"
export OC_MODES_ROOT="$tmp/state"
mkdir -p "$HOME"

bash -n "$p/opencode-modes.sh" "$p/build-opencode.sh" "$p/assets/n64-starter/install.sh"

help="$(bash "$p/opencode-modes.sh" --help)"
grep -q 'OpenCode + local Ollama' <<< "$help"
grep -q 'TraceForge REFERENCE lab' <<< "$help"

addr="$(bash "$p/opencode-modes.sh" --list)"
[[ "$addr" == 'http://127.0.0.1:11434/v1' ]]

addr="$(OC_OLLAMA_URL=http://localhost:12345 bash "$p/opencode-modes.sh" --list)"
[[ "$addr" == 'http://localhost:12345/v1' ]]

if OC_OLLAMA_URL=https://example.org/v1 bash "$p/opencode-modes.sh" --list >"$tmp/out" 2>&1; then
    echo 'Expected remote HTTPS address to fail.' >&2
    exit 1
fi

printf '0\n' | bash "$p/opencode-modes.sh" > "$tmp/out"
grep -q 'Goodbye.' "$tmp/out"
[[ ! -d "$OC_MODES_ROOT" ]] || { echo 'Test created state without selecting a mode.' >&2; exit 1; }

echo 'PASS: menu syntax, model URL normalisation, loopback guard, clean exit.'
