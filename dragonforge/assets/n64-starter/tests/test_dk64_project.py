import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from dk64_project import prepare


class DK64Tests(unittest.TestCase):
    def test_manifest_preserves_source_and_refuses_overwrite(self):
        data = bytearray(64)
        data[:4] = b'\x80\x37\x12\x40'
        data[0x20:0x34] = b'DONKEY KONG 64'.ljust(20, b' ')
        with tempfile.TemporaryDirectory() as tmp:
            rom = Path(tmp) / 'synthetic.z64'
            rom.write_bytes(data)
            workspace = Path(tmp) / 'study'
            target = prepare(rom, workspace)
            result = json.loads(target.read_text())
            self.assertEqual(result['sha256_file_bytes'], hashlib.sha256(data).hexdigest())
            self.assertEqual(rom.read_bytes(), data)
            before = target.read_bytes()
            with self.assertRaises(FileExistsError):
                prepare(rom, workspace)
            self.assertEqual(target.read_bytes(), before)

    def test_other_game_rejected_before_workspace_creation(self):
        data = b'\x80\x37\x12\x40' + bytes(60)
        with tempfile.TemporaryDirectory() as tmp:
            rom = Path(tmp) / 'other.z64'
            rom.write_bytes(data)
            workspace = Path(tmp) / 'study'
            with self.assertRaises(ValueError):
                prepare(rom, workspace)
            self.assertFalse(workspace.exists())


if __name__ == '__main__':
    unittest.main()
