# DragonForge local-first workspaces

This folder adds a launcher to the independently maintained DragonForge Go coding agent.

- Standalone terminal coding UI (no AI model preselected).
- General coding with your existing local Ollama/Qwen installation.
- Nintendo 64 specialist with automatic installation of an isolated lab and read-only ROM header inspection.
- Separate TraceForge **reference lab**; never points at the existing TraceForge source tree.
- Ollama model discovery and a tested local Go build action.

## Ubuntu setup

Clone the standalone repository and start:

    git clone https://github.com/HenricHuntsman/dragonforge-code.git
    cd dragonforge-code
    bash dragonforge/modes.sh

Select **6** to compile and run the Go tests. Select **5** to verify Ollama.
Select **3** to start the Nintendo 64 specialist; the starter is installed automatically when missing.

The launcher uses the local Ollama endpoint http://127.0.0.1:11434/v1, keeps a separate
local configuration profile for each mode, and unsets common cloud credentials.
It is **not a filesystem security sandbox**: review and approve risky tool actions.
Never use unattended/noninteractive auto-approval for repository changes.

For local smoke tests:

    bash dragonforge/tests/test-modes.sh

For N64 header inspection in the isolated lab:

    python3 tools/n64_header.py /path/to/authorized/rom.z64

Header-only inspection does not prove game compatibility or validate checksums.
