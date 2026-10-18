from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from mips_inspect import decode, inspect


class MIPSTests(unittest.TestCase):
    def test_targets_and_unknowns(self):
        self.assertEqual(decode(0x1000ffff, 0x80001000), 'beq $r0, $r0, 0x80001000')
        self.assertEqual(decode(0x0c000400, 0x80001000), 'jal 0x80001000')
        self.assertIn('unknown', decode(0x0c000400))
        self.assertTrue(decode(0x48000000).startswith('.word'))
        self.assertEqual(decode(0x03e00008), 'jr $r31')

    def test_orders_ranges_and_source_unchanged(self):
        header = b'\x80\x37\x12\x40' + bytes(60)
        data = header + bytes.fromhex('27bdffe003e00008')
        with tempfile.TemporaryDirectory() as tmp:
            for width in (1, 2, 4):
                raw = b''.join(data[i:i+width][::-1] for i in range(0, len(data), width))
                path = Path(tmp) / f'fixture-{width}'
                path.write_bytes(raw)
                result = inspect(path, 64, 2)
                self.assertEqual(result['instructions'][0]['assembly'], 'addiu $r29, $r29, -32')
                self.assertEqual(result['instructions'][1]['assembly'], 'jr $r31')
                self.assertEqual(path.read_bytes(), raw)
                for offset, count in ((1, 1), (64, 3), (0, 0), (0, 4097)):
                    with self.assertRaises(ValueError):
                        inspect(path, offset, count)


if __name__ == '__main__':
    unittest.main()
