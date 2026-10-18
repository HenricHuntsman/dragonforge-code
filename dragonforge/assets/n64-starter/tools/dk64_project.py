#!/usr/bin/env python3
"""Prepare a read-only Donkey Kong 64 study workspace from a local ROM."""
import argparse
import hashlib
import json
from pathlib import Path
from n64_header import inspect_rom


def prepare(rom: Path, workspace: Path):
    rom = rom.resolve(strict=True)
    info = inspect_rom(rom)
    if 'DONKEY KONG' not in info['title'].upper():
        raise ValueError('Header title does not identify Donkey Kong; select the DK64 ROM')
    digest = hashlib.sha256()
    with rom.open('rb') as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    manifest = {
        'schema_version': 1, 'project': 'Donkey Kong 64 study',
        'rom': info, 'sha256_file_bytes': digest.hexdigest(),
        'status': 'Header inspected; game revision, ROM integrity and emulation are not verified.',
        'source_policy': 'ROM remains at its original local path; no ROM data is copied into the project.'
    }
    workspace.mkdir(parents=True, exist_ok=True)
    target = workspace / 'rom-manifest.json'
    # Exclusive creation preserves any prior project manifest.
    with target.open('x') as output:
        output.write(json.dumps(manifest, indent=2) + '\n')
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom', type=Path)
    parser.add_argument('--workspace', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = prepare(args.rom, args.workspace)
    except (OSError, ValueError) as error:
        parser.exit(2, f'Error: {error}\n')
    print(f'Created {result}; source ROM unchanged.')


if __name__ == '__main__':
    main()
