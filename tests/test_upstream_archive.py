import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('mirror', Path(__file__).resolve().parents[1] / 'scripts/mirror_upstream_releases.py')
mirror = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mirror)

class ArchiveTests(unittest.TestCase):
    def test_historical_tag_namespace(self):
        self.assertEqual(mirror.archive_tag('v0.0.55'), 'upstream-v0.0.55')
        for tag in ('../main', '', 'bad tag'):
            with self.assertRaises(ValueError): mirror.archive_tag(tag)

    def test_asset_paths(self):
        for name in ('../binary', '/binary', 'a/b', 'a\\b', '.', ''):
            with self.assertRaises(ValueError): mirror.safe_asset_name(name)
        self.assertEqual(mirror.safe_asset_name('checksums.txt'), 'checksums.txt')

    def test_checksum_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / 'binary'
            p.write_bytes(b'known fixture')
            digest = mirror.verify_digest(p)
            self.assertEqual(mirror.verify_digest(p, 'sha256:' + digest), digest)
            with self.assertRaises(ValueError): mirror.verify_digest(p, '0' * 64)

if __name__ == '__main__': unittest.main()
