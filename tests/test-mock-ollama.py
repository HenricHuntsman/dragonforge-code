#!/usr/bin/env python3
"""Exercise OpenCode launcher model selection against a fake loopback Ollama server."""
import http.server
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading

PKG = Path(__file__).resolve().parents[1]

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/v1/models':
            body = json.dumps({'object': 'list', 'data': [{'id': 'qwen2.5-coder:7b'}]}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def log_message(self, *args):
        pass

server = http.server.HTTPServer(('127.0.0.1', 0), Handler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
try:
    with tempfile.TemporaryDirectory() as d:
        home = Path(d) / 'home'
        home.mkdir()
        root = Path(d) / 'state'
        bindir = root / 'bin'
        bindir.mkdir(parents=True)
        binary = bindir / 'opencode'
        binary.write_text('#!/usr/bin/env bash\necho "MOCK_OPENCODE cwd=$2 endpoint=${LOCAL_ENDPOINT} home=${HOME}"\n')
        binary.chmod(0o755)
        env = os.environ.copy()
        env.update({'HOME': str(home), 'OC_MODES_ROOT': str(root),
                    'OC_OLLAMA_URL': f'http://127.0.0.1:{server.server_port}/v1'})
        proc = subprocess.run(['bash', str(PKG / 'opencode-modes.sh')], input='2\n1\n0\n',
                              text=True, capture_output=True, env=env, timeout=15)
        out = proc.stdout + proc.stderr
        assert proc.returncode == 0, out
        assert 'MOCK_OPENCODE' in out, out
        assert 'endpoint=http://127.0.0.1:' in out, out
        profile = root / 'profiles/ollama-home/.config/opencode/.opencode.json'
        data = json.loads(profile.read_text())
        assert data['agents']['coder']['model'] == 'local.qwen2.5-coder:7b', data
        assert data['agents']['coder']['maxTokens'] == 1024, data
        assert not (home / 'dev/opencode-revival').exists()
        print('PASS: fake Ollama discovery, model selection, isolated local profile and TUI launch.')
finally:
    server.shutdown()
    thread.join(timeout=3)
