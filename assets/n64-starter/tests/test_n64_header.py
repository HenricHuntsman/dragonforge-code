"""Synthetic-only tests: no ROM uploads or third-party assets required."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from n64_header import inspect_rom, normalize_header  # noqa: E402


def canonical() -> bytes:
    b = bytearray(64)
    b[:4] = b"\x80\x37\x12\x40"
    b[8:12] = (0x80000400).to_bytes(4, "big")
    b[0x10:0x14] = (0x12345678).to_bytes(4, "big")
    b[0x14:0x18] = (0xAABBCCDD).to_bytes(4, "big")
    b[0x20:0x34] = b"N64 SYNTHETIC TEST".ljust(20, b" ")
    b[0x3C:0x3E] = b"AB"
    b[0x3E] = ord("E")
    return bytes(b)


def swap16(b: bytes) -> bytes:
    return b"".join(b[i : i + 2][::-1] for i in range(0, len(b), 2))


def swap32(b: bytes) -> bytes:
    return b"".join(b[i : i + 4][::-1] for i in range(0, len(b), 4))


class N64HeaderTests(unittest.TestCase):
    def test_three_byte_orders(self):
        original = canonical()
        for fmt, buf in [("z64", original), ("v64", swap16(original)), ("n64", swap32(original))]:
            with self.subTest(fmt=fmt):
                label, normalized = normalize_header(buf)
                self.assertTrue(label.startswith(fmt))
                self.assertEqual(normalized, original)

    def test_inspect_header_without_modification(self):
        original = canonical()
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "sample.z64"
            path.write_bytes(original)
            got = inspect_rom(path)
            self.assertEqual(got["entry_point"], "0x80000400")
            self.assertEqual(got["crc1_header"], "0x12345678")
            self.assertEqual(got["cartridge_id"], "AB")
            self.assertEqual(path.read_bytes(), original)

    def test_short_and_invalid_rom(self):
        for b in (b"", b"x" * 64):
            with self.subTest(data=b[:4]):
                with self.assertRaises(ValueError):
                    normalize_header(b)


if __name__ == "__main__":
    unittest.main()
