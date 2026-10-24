#!/usr/bin/env bash
# Interactive OpenCode multi-mode launcher. No one-shot auto-approve mode.
set -euo pipefail
PACKAGE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${OC_MODES_ROOT:-${HOME}/.local/share/opencode-modes}"
BIN="$ROOT/bin/opencode"
BASE="${OC_OLLAMA_URL:-http://127.0.0.1:11434/v1}"

help_text() {
cat <<'EOF'
OpenCode Modes — Ubuntu launcher
  1  OpenCode standalone (isolated profile; no selected AI model)
  2  OpenCode + local Ollama
  3  OpenCode N64 lab + local Ollama
  4  OpenCode TraceForge REFERENCE lab + local Ollama
  5  Check Ollama local model server
  6  Compile/test latest GitHub main in isolated checkout
  7  Install N64 starter lab, refusing to overwrite existing lab
  0  Exit

No mode writes to the existing OpenCode dev checkout or TraceForge.
Mode 4 is a separate study workspace; it does NOT directly connect to TraceForge.
Ollama URL: OC_OLLAMA_URL=http://127.0.0.1:11434/v1
EOF
}

need_binary() {
    if [[ ! -x "$BIN" ]]; then
        printf '\nCompiled binary missing: %s\nSelect option 6 to build it first.\n' "$BIN" >&2
        return 1
    fi
}

# Only accept locally hosted URLs; never silently send project data to a remote host.
normalized_url() {
    python3 - "$BASE" <<'PY'
import sys
from urllib.parse import urlsplit
raw=sys.argv[1].strip()
u=urlsplit(raw)
if u.scheme != 'http' or u.hostname not in ('127.0.0.1','localhost','::1'):
    sys.exit('Refusing non-loopback or non-HTTP Ollama endpoint')
if u.username or u.password or u.query or u.fragment or not u.port or u.path not in ('', '/', '/v1', '/v1/'):
    sys.exit('Endpoint must be http://127.0.0.1:PORT[/v1] (no query or credentials)')
print(f'{u.scheme}://{u.netloc}/v1')
PY
}

get_models() {
    local base="$1" output
    if ! output="$(curl -fSs --connect-timeout 2 --max-time 5 "$base/models")"; then
        echo 'Ollama unavailable. Verify it is running and exposes /v1/models.' >&2
        return 1
    fi
    printf '%s' "$output" | python3 -c '
import json,sys
obj=json.load(sys.stdin)
for item in obj.get("data",[]):
    if isinstance(item,dict) and isinstance(item.get("id"),str):
        print(item["id"])
'
}

select_model() {
    local base="$1" choice i
    local -a models=()
    mapfile -t models < <(get_models "$base")
    if (( ${#models[@]} == 0 )); then
        echo 'No Ollama models were returned (or the server is unavailable).' >&2
        return 1
    fi
    printf 'Available local models:\n' >&2
    for i in "${!models[@]}"; do
        printf '  %d) %s\n' "$((i + 1))" "${models[$i]}" >&2
    done
    read -r -p 'Select model number: ' choice
    if [[ ! "$choice" =~ ^[0-9]+$ ]] || (( choice < 1 || choice > ${#models[@]} )); then
        echo 'Invalid model selection.' >&2
        return 1
    fi
    printf '%s' "${models[$((choice - 1))]}"
}

# Unique profile HOME prevents normal home config/cloud provider selection from leaking in.
write_local_profile() {
    local home="$1" model="$2"
    mkdir -p "$home/.config/opencode"
    python3 - "$home/.config/opencode/.opencode.json" "$model" <<'PY'
import json,sys
path,model=sys.argv[1:]
config={
    'providers':{'local':{'apiKey':'dummy'}},
    'agents':{key:{'model':'local.'+model,'maxTokens':1024} for key in ('coder','task','title','summarizer')},
    'autoCompact': True,
}
with open(path,'w') as f:
    json.dump(config,f,indent=2)
    f.write('\n')
PY
}

run_sandboxed() {
    local cwd="$1" profile_home="$2" base="$3"
    [[ ! -L "$cwd" && ! -L "$profile_home" ]] || { echo 'Symlink workspace/profile rejected.' >&2; return 1; }
    mkdir -p "$cwd" "$profile_home/.config"
    local -a cmd=(env)
    # Do not pass API keys to the subprocess. The dedicated HOME has no cloud profiles.
    local name
    for name in ANTHROPIC_API_KEY OPENAI_API_KEY GOOGLE_API_KEY GEMINI_API_KEY \
                GROQ_API_KEY OPENROUTER_API_KEY XAI_API_KEY AZURE_OPENAI_API_KEY \
                AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN \
                GITHUB_TOKEN GH_TOKEN; do
        cmd+=(-u "$name")
    done
    cmd+=("HOME=$profile_home" "XDG_CONFIG_HOME=$profile_home/.config")
    if [[ -n "$base" ]]; then
        cmd+=("LOCAL_ENDPOINT=$base")
    else
        cmd+=(-u LOCAL_ENDPOINT -u OLLAMA_HOST)
    fi
    cmd+=("$BIN" --cwd "$cwd")
    "${cmd[@]}"
}

run_local_mode() {
    local mode="$1" base model cwd prof
    need_binary || return 1
    base="$(normalized_url)" || return 1
    model="$(select_model "$base")" || return 1
    case "$mode" in
        ollama) cwd="$HOME/dev/opencode-ollama-lab" ;;
        n64)
            cwd="$HOME/dev/opencode-n64-lab"
            if [[ ! -f "$cwd/.opencode/skills/n64-dev/SKILL.md" ]]; then
                echo 'N64 starter is missing; select option 7 to install it.' >&2
                return 1
            fi
            ;;
        traceforge) cwd="$HOME/dev/opencode-traceforge-study" ;;
        *) echo 'Unknown local mode' >&2; return 1 ;;
    esac
    prof="$ROOT/profiles/$mode-home"
    if [[ -L "$prof" || -L "$cwd" ]]; then
        echo 'Refusing symlink profile or workspace.' >&2
        return 1
    fi
    write_local_profile "$prof" "$model"
    if [[ "$mode" == traceforge ]]; then
        echo 'TRACEFORGE REFERENCE MODE: launches in its own study folder.'
        echo 'No existing TraceForge files are mounted or copied.'
        echo 'Copy only selected, safe, non-sensitive snippets here for review.'
    elif [[ "$mode" == n64 ]]; then
        echo 'N64 skill: ask the agent to load skill name "n64-dev".'
    fi
    run_sandboxed "$cwd" "$prof" "$base"
}

install_n64_lab() {
    local folder="$PACKAGE_DIR/assets/n64-starter"
    if [[ ! -f "$folder/install.sh" ]]; then
        echo 'Bundled N64 starter not found. Extract the complete ZIP.' >&2
        return 1
    fi
    bash "$folder/install.sh"
}

ollama_status() {
    local base
    base="$(normalized_url)" || return 1
    echo "Checking $base/models"
    get_models "$base"
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    help_text
    exit 0
fi
if [[ "${1:-}" == "--list" ]]; then
    normalized_url
    exit 0
fi
if [[ $# -gt 0 ]]; then
    echo 'Unsupported option. Use --help.' >&2
    exit 2
fi
while :; do
    echo
    echo '========================================'
    echo '         OPENCODE MODES (UBUNTU)'
    echo '========================================'
    help_text
    read -r -p 'Select 0–7: ' choice || break
    case "$choice" in
        1)
            if need_binary; then
                echo 'Standalone TUI: no Ollama selected. No model calls until configured.'
                run_sandboxed "$HOME/dev/opencode-standalone-lab" "$ROOT/profiles/standalone-home" '' || true
            fi
            ;;
        2) run_local_mode ollama || true ;;
        3) run_local_mode n64 || true ;;
        4) run_local_mode traceforge || true ;;
        5) ollama_status || true ;;
        6) bash "$PACKAGE_DIR/build-opencode.sh" || true ;;
        7) install_n64_lab || true ;;
        0) echo 'Goodbye.'; break ;;
        *) echo 'Choose one of the listed numbers.' ;;
    esac
done
