#!/usr/bin/env bash
# Local-only DragonForge launcher. No noninteractive auto-approval.
set -Eeuo pipefail
HERE="$(cd -- "$(dirname -- "$0")" && pwd)"
ROOT="$(cd -- "$HERE/.." && pwd)"
STATE="$HOME/.local/share/dragonforge"
BIN="$STATE/bin/dragonforge"
ENDPOINT="http://127.0.0.1:11434/v1"
N64_LAB="$HOME/dev/dragonforge-n64-lab"
[[ -n "$(printenv DRAGONFORGE_BIN || true)" ]] && BIN="$DRAGONFORGE_BIN"
[[ -n "$(printenv DRAGONFORGE_STATE || true)" ]] && STATE="$DRAGONFORGE_STATE"
[[ -n "$(printenv DRAGONFORGE_OLLAMA_URL || true)" ]] && ENDPOINT="$DRAGONFORGE_OLLAMA_URL"
case "$ENDPOINT" in
  http://127.0.0.1:11434/v1|http://localhost:11434/v1) ;;
  *) echo 'Only loopback Ollama endpoints are supported.' >&2; exit 2 ;;
esac
models() {
  command -v curl >/dev/null || { echo 'curl is required.' >&2; return 1; }
  curl --fail --silent --show-error --connect-timeout 2 --max-time 6 "$ENDPOINT/models" |
    python3 -c 'import json,sys; p=json.load(sys.stdin); print("\n".join(x["id"] for x in p.get("data",[]) if isinstance(x,dict) and isinstance(x.get("id"),str)))'
}
pick_model() {
  local choices n chosen
  choices="$(models)" || return 1
  [[ -n "$choices" ]] || { echo 'No local Ollama models found.' >&2; return 1; }
  printf '%s\n' 'Available models:' >&2
  printf '%s\n' "$choices" | nl -w 2 -s ') ' >&2
  read -r -p 'Model number: ' n
  [[ "$n" =~ ^[0-9]+$ ]] && (( n > 0 )) || { echo 'Invalid model number.' >&2; return 1; }
  chosen="$(printf '%s\n' "$choices" | sed -n "$n""p")"
  [[ -n "$chosen" ]] || { echo 'Model not found.' >&2; return 1; }
  printf '%s' "$chosen"
}
launch() {
  local mode="$1" folder="$2" model="$3" profile="$STATE/profiles/$1"
  [[ -x "$BIN" ]] || { echo "Binary missing: $BIN; choose option 6." >&2; return 1; }
  [[ ! -L "$folder" && ! -L "$profile" ]] || { echo 'Symlink location rejected.' >&2; return 1; }
  mkdir -p "$folder" "$profile/.config/opencode"
  if [[ "$model" != none ]]; then
    python3 - "$profile/.config/opencode/.opencode.json" "$model" <<'PY'
import json,sys
path,model=sys.argv[1:]
obj={"providers":{"local":{"apiKey":"dummy"}},
"agents":{name:{"model":"local."+model,"maxTokens":1024}
          for name in ("coder","task","title","summarizer")},
"autoCompact":True}
with open(path,"w",encoding="utf-8") as fp:
    json.dump(obj,fp,indent=2)
    fp.write("\n")
PY
  fi
  echo "Launching DragonForge in $folder"
  if [[ "$model" = none ]]; then
    env -u OPENAI_API_KEY -u ANTHROPIC_API_KEY -u GOOGLE_API_KEY -u GEMINI_API_KEY \
      -u GROQ_API_KEY -u OPENROUTER_API_KEY -u XAI_API_KEY -u GITHUB_TOKEN \
      -u GH_TOKEN -u LOCAL_ENDPOINT -u OLLAMA_HOST HOME="$profile" \
      XDG_CONFIG_HOME="$profile/.config" "$BIN" --cwd "$folder"
  else
    env -u OPENAI_API_KEY -u ANTHROPIC_API_KEY -u GOOGLE_API_KEY -u GEMINI_API_KEY \
      -u GROQ_API_KEY -u OPENROUTER_API_KEY -u XAI_API_KEY -u GITHUB_TOKEN \
      -u GH_TOKEN HOME="$profile" XDG_CONFIG_HOME="$profile/.config" \
      LOCAL_ENDPOINT="$ENDPOINT" "$BIN" --cwd "$folder"
  fi
}
n64() {
  if [[ -e "$N64_LAB" && ! -f "$N64_LAB/.opencode/skills/n64-dev/SKILL.md" ]]; then
    echo "N64 lab exists but has no starter: $N64_LAB (not overwritten)." >&2; return 1
  fi
  if [[ ! -e "$N64_LAB" ]]; then
    DRAGONFORGE_N64_DEST="$N64_LAB" bash "$HERE/assets/n64-starter/install.sh" || return 1
  fi
  local model
  model="$(pick_model)" || return 1
  launch n64 "$N64_LAB" "$model"
}
build() {
  command -v go >/dev/null || { echo 'Go compiler not found.' >&2; return 1; }
  (cd "$ROOT" && go mod verify && go vet ./... && go test ./... -count=1) || return 1
  mkdir -p "$(dirname "$BIN")"
  local temp
  temp="$(mktemp "$(dirname "$BIN")/.dragonforge.XXXXXXXX")"
  if (cd "$ROOT" && go build -o "$temp" .) && chmod 755 "$temp" && "$temp" --version; then
    mv -f "$temp" "$BIN"
    echo "Built: $BIN"
  else
    rm -f "$temp"
    return 1
  fi
}
if [[ "$#" -gt 0 ]]; then
  [[ "$#" = 1 && "$1" = --help ]] && { echo 'Usage: bash dragonforge/modes.sh'; exit 0; }
  echo 'Unknown arguments.' >&2; exit 2
fi
while :; do
  cat <<'MENU'

=== DRAGONFORGE CODE ===
  1  Standalone agent (no model selected)
  2  General coding + local Ollama
  3  Nintendo 64 + local Ollama (installs starter automatically)
  4  TraceForge reference lab + local Ollama
  5  Check Ollama models
  6  Build and test DragonForge
  0  Exit
MENU
  read -r -p 'Select 0-6: ' number || break
  case "$number" in
    1) launch standalone "$HOME/dev/dragonforge-standalone-lab" none || true ;;
    2) model="$(pick_model)" && launch general "$HOME/dev/dragonforge-general-lab" "$model" || true ;;
    3) n64 || true ;;
    4) echo 'This is a REFERENCE lab, not your existing TraceForge checkout.'
       model="$(pick_model)" && launch traceforge "$HOME/dev/dragonforge-traceforge-reference" "$model" || true ;;
    5) models || true ;;
    6) build || true ;;
    0) break ;;
    *) echo 'Choose a number from the menu.' ;;
  esac
done
