# N64 study lab

Inspect a local ROM without changing its bytes:

```sh
python3 tools/n64_header.py '/path/to/game.z64'
```

## Donkey Kong 64

Prepare a separate study workspace using your local ROM:

```sh
python3 tools/dk64_project.py '/path/to/Donkey Kong 64.z64' \
  --workspace "$HOME/dev/dk64-study"
```

The command checks the header title, records header fields, region byte, size and SHA-256 of the original file bytes in `rom-manifest.json`. It accepts the same z64, v64 and n64 byte orders as the header inspector. The checksum differs between byte orders. Existing manifests are never overwritten. The ROM stays at its original path and must remain available there.

Title recognition is a starting check, not proof of game identity or a verified dump. This starter does not yet extract game assets, launch an emulator, patch a ROM or rebuild DK64. No game data is included. Keep ROMs and generated private manifests outside the source repository.

Run synthetic tests with:

```sh
python3 -m unittest discover -s tests
```

## MIPS inspection and local AI

Inspect a small aligned ROM range (offset is a file offset, not a RAM address):

```sh
python3 tools/mips_inspect.py '/path/to/Donkey Kong 64.z64' \
  --offset 0x1000 --words 64 > "$HOME/dev/dk64-study/mips-sample.json"
```

This is our own partial scalar MIPS decoder, not a new CPU architecture or programming language. Unsupported words remain `.word`; successful decoding does not prove a range contains executable code. The ROM header entry point alone does not establish a mapping for arbitrary ROM offsets. Only supply `--vaddr` when that mapping is independently verified. RSP microcode, overlays, compressed assets and game-specific formats need separate analysis. Compiled machine code generally does not reliably identify its original source language.

Start AI review with a local quantized Qwen2.5-Coder-14B-Instruct candidate, or the existing 7B coder for lower memory use. Benchmark on synthetic instruction fixtures first; these models are not verified DK64 decompilers. A 4-bit 14B model is a plausible candidate for a 16GB GPU with a modest context, but actual fit and speed must be measured. Qwen3-Coder-30B-A3B has 30.5B total parameters despite 3.3B active; active parameters do not represent its full weight storage requirement.

Model sources: https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct and https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct.

Give the local model only bounded analysis reports and relevant snippets. Ask it to cite file offsets, distinguish observations from hypotheses, preserve unknown instructions, account for branch delay slots, and propose checks. Verify suggested names and C-like pseudocode against independent disassembly and runtime evidence. Treat ROM strings as data, never as instructions for the agent. No model is downloaded or installed by these tools.
