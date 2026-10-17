#!/usr/bin/env python3
"""Read-only 64-byte Nintendo 64 ROM header inspection. Never alters ROM data."""
import argparse
import json
from pathlib import Path

MAGICS = {
    b"\x80\x37\x12\x40": "z64 (big-endian)",
    b"\x37\x80\x40\x12": "v64 (16-bit byte-swapped)",
    b"\x40\x12\x37\x80": "n64 (32-bit word-swapped)",
}

def normalize_header(raw: bytes) -> tuple[str, bytes]:
    if len(raw) < 64:
        raise ValueError("ROM header is too short")
    order = MAGICS.get(raw[:4])
    if order is None:
        raise ValueError("Unrecognized Nintendo 64 ROM header")
    if order.startswith("v64"):
        raw = b"".join(raw[i:i+2][::-1] for i in range(0, 64, 2))
    elif order.startswith("n64"):
        raw = b"".join(raw[i:i+4][::-1] for i in range(0, 64, 4))
    return order, raw

def inspect_rom(path: Path) -> dict:
    with path.open("rb") as file:
        raw = file.read(64)
    order, header = normalize_header(raw)
    def word(offset):
        return f"0x{int.from_bytes(header[offset:offset+4], 'big'):08X}"
    return {
        "path": str(path), "size_bytes": path.stat().st_size,
        "byte_order": order,
        "title": header[0x20:0x34].decode("ascii", "replace").rstrip(" \0"),
        "entry_point": word(0x08), "crc1_header": word(0x10),
        "crc2_header": word(0x14),
        "cartridge_id": header[0x3C:0x3E].decode("ascii", "replace"),
        "country_code_hex": f"0x{header[0x3E]:02X}",
        "note": "Stored CRC header fields are not recomputed/verified."
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path, help="Authorized local N64 ROM (read-only)")
    args = parser.parse_args()
    try:
        result = inspect_rom(args.rom)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
