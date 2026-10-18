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
