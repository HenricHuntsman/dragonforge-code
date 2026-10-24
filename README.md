# OpenCode Modes — single engine, selectable backends and workspaces

This pack gives HenricHuntsman's **Go-based OpenCode Revival** a terminal selection menu on Ubuntu. It is a companion tool, **not** a fork, a new release of OpenCode, or an N64 emulator. It does **not** modify `~/dev/opencode-revival` (where two uncommitted Bash/prompt changes were reported) or `~/dev/TraceForge-FreeBuff-2026-10-17`.

## What the names mean

- **Engine / compiler:** Go compiles OpenCode from [HenricHuntsman/opencode](https://github.com/HenricHuntsman/opencode). It is one binary for all modes.
- **Backend:** Ollama is an optional **separate local inference server** that responds on `http://127.0.0.1:11434/v1`. The launcher does not install, restart, update or download Ollama models.
- **Agent:** OpenCode's existing coder agent runs inside the chosen project directory, with any project skills and instructions found there.
- **Standalone:** Opens an isolated OpenCode TUI without an Ollama endpoint or a configured model. It does not magically provide offline AI; model-based answers need a provider.
- **N64 mode:** Uses a synthetic fixture lab and the `n64-dev` skill. The skill is manual: ask the agent to load it by name.
- **TraceForge reference mode:** Opens a **separate empty research lab**. It does **not** mount or run code inside the real TraceForge repository. Manually copy only files you want examined into that lab. This is intentional while safety/integration is being verified.

## Ubuntu requirements

`bash`, `git`, `go`, `python3`, `curl`, and `unzip` (for extracting this package). A supported terminal is needed for the OpenCode TUI. Build uses network to clone/fetch GitHub and download Go dependencies, and is **opt-in** at menu option 6.

## Run

Extract the archive in your Downloads directory and run:

```bash
cd "$HOME/Downloads" || exit 1
unzip -n opencode-modes-launcher.zip
cd opencode-modes-launcher || exit 1
bash opencode-modes.sh
```

Choose **6** first. This clones into a dedicated source directory at `~/.local/share/opencode-modes/source`, fast-forwards it only when clean and on `main`, runs `go mod verify`, `go vet ./...`, `go test ./... -count=1`, and builds the executable. **Only after everything passes** is the old compiled launcher binary replaced. The original development repositories remain unchanged.

Then choose **2** for Ollama (or **7** to install the N64 lab and **3** to launch it). The menu probes `/v1/models`, lists available model IDs, and writes an isolated local-provider config with your selected model. It starts only **interactive** OpenCode, never `--prompt`, because the legacy non-interactive flow can auto-approve actions.

Option **1** opens the bare TUI. Option **4** opens a **reference workspace** for manually selected TraceForge materials, never your real TraceForge working tree. Option **5** lists models without launching an agent.

The launcher accepts only loopback (`localhost`, `127.0.0.1`, or `::1`) plain-HTTP Ollama addresses, for example:

```bash
OC_OLLAMA_URL=http://127.0.0.1:11434/v1 bash opencode-modes.sh
```

It sets `LOCAL_ENDPOINT`, and for Ollama modes explicitly selects the model in a dedicated config stored beneath `~/.local/share/opencode-modes/profiles/`. It unsets common cloud-provider credentials and uses an isolated HOME. This substantially reduces accidental cloud-provider selection, but **is not an operating-system network sandbox**. Only run code and skills you trust; review tool approval prompts. A working local LLM that supports tool calls is required for agent coding.

## Project locations

| Location | Purpose |
| --- | --- |
| `~/dev/opencode-revival` | Existing development checkout, **untouched** |
| `~/.local/share/opencode-modes/source` | Dedicated clean checkout of current `main` for Go builds |
| `~/.local/share/opencode-modes/bin/opencode` | Built binary for the launcher |
| `~/dev/opencode-standalone-lab` | Bare OpenCode mode |
| `~/dev/opencode-ollama-lab` | OpenCode with Ollama mode |
| `~/dev/opencode-n64-lab` | N64 specialist skill and read-only utilities |
| `~/dev/opencode-traceforge-study` | TraceForge **reference** lab, not the real repository |

## Test the menu locally

```bash
bash -n opencode-modes.sh build-opencode.sh
bash tests/test-launcher.sh
```

This launcher package has not been installed or run on Henric's Ubuntu computer; those tests verify shell syntax and safe menu behaviours in a temporary HOME. Live Ollama chat and full Go builds require Ubuntu and the user's running services. GitHub's current `main` may change after this package was created, so build the checked-out commit and record its version.

## Limits / next milestones

- OpenCode's compatibility with your particular Ollama/Qwen tool-calling model still requires a real chat/agent smoke test. No claims of full integration are made from model discovery alone.
- Existing Go OpenCode may still allow auto-approval in **non-interactive** mode. This launcher never uses that mode, but shell approvals in interactive sessions should still be reviewed carefully.
- The N64 profile is a skill/instruction layer, not automatic reverse-engineering or permission to manipulate ROMs.
- An eventual TraceForge adapter should be read-only and separately tested, rather than opening the user's active working tree to the agent by default.
- No new release tag, branch or GitHub commit is created by this pack. After local tests, the launcher can be added to a reviewed PR in the public fork.
# dragonforge-code
