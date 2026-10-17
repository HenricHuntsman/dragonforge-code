#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "$0")/../.." && pwd)"
cd "$ROOT"
bash -n dragonforge/modes.sh dragonforge/assets/n64-starter/install.sh
python3 -m unittest discover -s dragonforge/assets/n64-starter/tests -v
bash dragonforge/modes.sh --help | grep -q 'Usage'
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/fake" "$TMP/home"
cat >"$TMP/fake/curl" <<'MOCK'
#!/usr/bin/env bash
printf '{"data":[{"id":"qwen3-kilo:8b"},{"id":"qwen3:8b"}]}'
MOCK
cat >"$TMP/fake/dragonforge" <<'MOCK'
#!/usr/bin/env bash
printf 'MOCK-AGENT cwd=%s model_endpoint=%s\n' "$2" "$LOCAL_ENDPOINT"
MOCK
chmod +x "$TMP/fake/curl" "$TMP/fake/dragonforge"
printf '3\n1\n0\n' | env PATH="$TMP/fake:$PATH" HOME="$TMP/home" \
  DRAGONFORGE_BIN="$TMP/fake/dragonforge" DRAGONFORGE_STATE="$TMP/state" \
  bash dragonforge/modes.sh >"$TMP/log" 2>&1
python3 - "$TMP" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
assert (p/"home/dev/dragonforge-n64-lab/.opencode/skills/n64-dev/SKILL.md").is_file()
prof=p/"state/profiles/n64/.config/opencode/.opencode.json"
assert json.loads(prof.read_text())["agents"]["coder"]["model"] == "local.qwen3-kilo:8b"
assert "MOCK-AGENT" in (p/"log").read_text()
print("PASS: N64 auto-install, isolated Ollama model and interactive agent launch (mock)")
PY
if env DRAGONFORGE_OLLAMA_URL="http://example.com/v1" bash dragonforge/modes.sh --help >/dev/null 2>&1; then
  echo 'FAIL: non-loopback endpoint accepted' >&2
  exit 1
fi
echo 'PASS: shell syntax, synthetic N64 headers, local model selection, loopback guard'
