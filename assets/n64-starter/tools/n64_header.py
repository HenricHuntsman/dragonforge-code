#!/usr/bin/env python3
"""Read only the 64-byte Nintendo 64 ROM header and report basic fields.

No ROM bytes are modified, copied, uploaded, or written by this program.
A valid-looking header does not establish authenticity or runnability.
"""

import argparse
import json
from pathlib import Path

MAGICS = {
    b"\x80\x37\x12\x40": "z64 (big-endian)",
    b"\x37\x80\x40\x12": "v64 (16-bit byte-swapped)",
    b"\x40\x12\x37\x80": "n64 (32-bit word-swapped)",
}


def normalize_header(header: bytes) -> tuple[str, bytes]:
    if len(header) < 64:
        raise ValueError("ROM too small: needs at least 64 bytes")
    order = MAGICS.get(header[:4])
    if order is None:
        raise ValueError("Unrecognized Nintendo 64 ROM header magic")
    if order.startswith("v64"):
        header = b"".join(header[i + 1 : i + 2] + header[i : i + 1] for i in range(0, 64, 2))
    elif order.startswith("n64"):
        header = b"".join(header[i : i + 4][::-1] for i in range(0, 64, 4))
    return order, header


def inspect_rom(path: Path) -> dict[str, object]:
    with path.open("rb") as f:
        raw = f.read(64)
    byte_order, header = normalize_header(raw)
    word = lambda offset: f"0x{int.from_bytes(header[offset : offset + 4], 'big'):08X}"
    return {
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "byte_order": byte_order,
        "title": header[0x20:0x34].decode("ascii", errors="replace").rstrip(" \x00"),
        "entry_point": word(0x08),
        "crc1_header": word(0x10),
        "crc2_header": word(0x14),
        "cartridge_id": header[0x3C:0x3E].decode("ascii", errors="replace"),
        "country_code_hex": f"0x{header[0x3E]:02X}",
        "note": "These are stored header values, not recomputed/verified CRCs.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path, help="ROM to inspect read-only (authorized local file)")
    args = parser.parse_args()
    try:
        result = inspect_rom(args.rom)
    except (OSError, ValueError) as e:
        parser.exit(status=2, message=f"Error: {e}\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
