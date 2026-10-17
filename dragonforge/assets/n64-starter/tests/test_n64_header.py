import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from n64_header import inspect_rom, normalize_header

def sample():
    raw = bytearray(64)
    raw[:4] = b"\x80\x37\x12\x40"
    raw[8:12] = (0x80000400).to_bytes(4, "big")
    raw[0x10:0x14] = (0x12345678).to_bytes(4, "big")
    raw[0x20:0x34] = b"SYNTHETIC N64".ljust(20, b" ")
    return bytes(raw)

class HeaderTests(unittest.TestCase):
    def test_three_orders(self):
        header = sample()
        variants = (
            header,
            b"".join(header[i:i+2][::-1] for i in range(0,64,2)),
            b"".join(header[i:i+4][::-1] for i in range(0,64,4)),
        )
        for fmt, buf in zip(("z64", "v64", "n64"), variants):
            order, normalized = normalize_header(buf)
            self.assertTrue(order.startswith(fmt))
            self.assertEqual(normalized, header)

    def test_read_only(self):
        original = sample()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.z64"
            path.write_bytes(original)
            info = inspect_rom(path)
            self.assertEqual(info["entry_point"], "0x80000400")
            self.assertEqual(info["crc1_header"], "0x12345678")
            self.assertEqual(path.read_bytes(), original)

    def test_bad_headers(self):
        for data in (b"", b"?"*64):
            with self.assertRaises(ValueError):
                normalize_header(data)

if __name__ == "__main__":
    unittest.main()
