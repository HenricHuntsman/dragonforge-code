# OpenCode N64 — isolated specialist starter

This is a **small profile and read-only tool**, **not** a second OpenCode executable and **not** a fork of TraceForge. It works toward an N64-specialized Go OpenCode agent while preserving the general-purpose `HenricHuntsman/opencode` project.

## Three distinct layers

| Layer | Owns | Keep separate from |
|---|---|---|
| OpenCode Revival (`~/dev/opencode-revival`) | Go coding agent, safe tool permissions, local model support, releases | All ROM and analysis source |
| N64 specialist lab (`~/dev/opencode-n64-lab`) | N64 instructions, synthetic fixtures, read-only inspection tooling | Installed OpenCode binary and other projects |
| TraceForge / M64Tool / RomForge64 / Hyrule Reborn | Real N64 reverse engineering, testing, tools and games | OpenCode's generic agent core |

A future optional adapter can allow the specialist agent to invoke **read-only** TraceForge analysis, but it should not copy, reset, merge, or push any TraceForge files.

## Installation on Ubuntu

Extract the ZIP. From inside the extracted `opencode-n64-starter` folder, run:

```bash
bash install.sh
```

The installer refuses to overwrite an existing `~/dev/opencode-n64-lab` directory. It initializes a distinct **local-only Git repository** in that new lab (does not push or create anything on GitHub).

## Test without any Nintendo 64 ROM

```bash
cd "$HOME/dev/opencode-n64-lab"
python3 -m unittest discover -s tests -v
```

## Optional read-only ROM header inspection

Only with an image you are authorized to inspect:

```bash
python3 tools/n64_header.py "/path/to/your/rom.z64"
```

The script reads the ROM's first 64 bytes only. It displays stored header CRC fields, **not validated CRCs**, and does not write to the ROM.

## Use with the Go OpenCode revival

After separately verifying/building a current OpenCode binary, start it **interactively** from the lab's directory, with a local provider endpoint as desired:

```bash
cd "$HOME/dev/opencode-n64-lab"
export LOCAL_ENDPOINT="http://127.0.0.1:11434/v1"
# /path/to/your/verified/opencode
```

The Go revival's skills feature (merged in PR #6) can discover `.opencode/skills/n64-dev/SKILL.md` in this workspace. `opencode/autoinvoke: "false"` means it must be explicitly selected by name `n64-dev`, rather than automatically advertised to the model.

**Important:** The legacy noninteractive prompt mode has previously auto-approved permissions. Do not use it for autonomous writes, shell actions, ROM edits or valuable workspaces until the remaining approval safeguards are tested.

## What this does *not* claim

The pack does not connect to a live Ollama server, start OpenCode, parse N64 assembly, run Ghidra, emulate games, or modify your existing project repositories. Those are later, separately tested integration stages.
