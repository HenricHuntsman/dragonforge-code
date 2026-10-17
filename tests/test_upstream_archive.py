import importlib.util
import io
import os
from unittest.mock import patch
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

    def test_disconnected_source_uses_snapshot_and_attaches_exact_sources(self):
        release = {'id': 1, 'tag_name': 'v0.1.0', 'assets': [], 'prerelease': False,
                   'html_url': 'https://github.com/opencode-ai/opencode/releases/tag/v0.1.0',
                   'published_at': '2025-01-01T00:00:00Z', 'author': {'login': 'original'}, 'body': ''}
        calls = []
        def api(path, token, data=None, method=None):
            calls.append((path, data, method))
            if path == '/repos/opencode-ai/opencode/releases/1': return release
            if path == '/repos/' + mirror.DESTINATION + '/releases' and data is not None:
                return {'id': 2, 'draft': True, 'upload_url': 'unused'}
            return None
        with patch.object(mirror, 'request_json', side_effect=api), \
             patch.object(mirror, 'source_commit', return_value='original-sha'), \
             patch.object(mirror, 'upload_asset') as upload, \
             patch.object(mirror.urllib.request, 'urlopen', side_effect=lambda *a, **k: io.BytesIO(b'source fixture')), \
             patch.dict(os.environ, {'ARCHIVE_BASE_SHA': 'snapshot-sha'}):
            mirror.mirror_release(release, 'test-token')
        names = [call.args[1].name for call in upload.call_args_list]
        self.assertIn('upstream-source-v0.1.0.tar.gz', names)
        self.assertIn('upstream-source-v0.1.0.zip', names)
        self.assertIn('upstream-release-metadata.json', names)
        self.assertTrue(any(data and data.get('sha') == 'snapshot-sha' for _, data, _ in calls))
        self.assertEqual(calls[-1][2], 'PATCH')
        self.assertFalse(calls[-1][1]['draft'])

if __name__ == '__main__': unittest.main()
