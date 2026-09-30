import base64
import copy
import hashlib
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.run import Client, install_runtime, safe_path, verify_cache, validate_lock
from workbook_mcp.bundle import runtime_bundle


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.bundle = runtime_bundle()
        self.lock = {key: self.bundle[key] for key in ('runtimeId', 'manifest')}

    def test_bundle_contains_only_server_runtime(self):
        names = [item['path'] for item in self.bundle['artifacts']]
        self.assertFalse(any(name.startswith(('workbooks/', 'outputs/', 'reports/', '.env')) for name in names))
        self.assertEqual(self.bundle, runtime_bundle())
        self.assertEqual(self.lock, json.loads((ROOT / 'runtime.lock.json').read_text(encoding='utf-8')))

    def test_tampering_never_installs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            result = copy.deepcopy(self.bundle)
            result['artifacts'][0]['base64'] = base64.b64encode(b'changed').decode()
            with self.assertRaises(ValueError):
                install_runtime(result, self.lock, root)
            self.assertFalse((root / self.lock['runtimeId']).exists())

    def test_incomplete_and_duplicate_artifacts_rejected(self):
        for artifacts in (self.bundle['artifacts'][:-1], self.bundle['artifacts'] + self.bundle['artifacts'][:1]):
            with tempfile.TemporaryDirectory() as folder:
                with self.assertRaises(ValueError):
                    install_runtime(self.bundle | {'artifacts': artifacts}, self.lock, Path(folder))

    def test_paths_cannot_escape_or_alias_on_windows(self):
        for path in ('../a', '/a', 'C:/a', 'x\\a', 'a//b', 'a/./b', 'a/NUL.py', 'a/x.', 'a/x ', 'a/x:y', 'a/\x00b'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                safe_path(path)

    def test_extra_cache_code_is_quarantined_and_pinned_runtime_restored(self):
        with tempfile.TemporaryDirectory() as folder:
            runtime = install_runtime(self.bundle, self.lock, Path(folder))
            (runtime / 'workbook_engine/extra.py').write_text('bad', encoding='utf-8')
            repaired = install_runtime(self.bundle, self.lock, Path(folder))
            self.assertEqual(runtime, repaired)
            verify_cache(repaired, self.lock['manifest'])
            quarantined = list(Path(folder).glob('.invalid-*'))
            self.assertEqual(1, len(quarantined))
            self.assertTrue((quarantined[0] / 'workbook_engine/extra.py').is_file())

    def test_local_lock_cannot_be_replaced_by_server(self):
        bad = self.bundle | {'runtimeId': '0' * 64}
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                install_runtime(bad, self.lock, Path(folder))
        with self.assertRaises(ValueError):
            validate_lock(self.lock | {'runtimeId': '0' * 64})


class HTTPIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.token = secrets.token_urlsafe(32)
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            port = probe.getsockname()[1]
        cls.url = f'http://127.0.0.1:{port}/mcp'
        env = dict(os.environ, WORKBOOK_MCP_API_TOKEN=cls.token, PORT=str(port), HOST='127.0.0.1', PYTHONDONTWRITEBYTECODE='1')
        cls.log = (cls.root / 'server.log').open('w', encoding='utf-8')
        cls.process = subprocess.Popen([sys.executable, '-X', 'utf8', '-m', 'workbook_mcp.server'],
                                       cwd=ROOT, env=env, stdout=cls.log, stderr=cls.log,
                                       creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            try:
                cls.client = Client(cls.url, cls.token)
                break
            except (OSError, ValueError):
                if cls.process.poll() is not None:
                    raise RuntimeError('Server failed to start')
                time.sleep(0.2)
        else:
            cls.process.terminate()
            raise RuntimeError('Server startup timed out')
        cls.bundle = cls.client.call('workbook_get_runtime', {'runtime_id': runtime_bundle()['runtimeId']})
        cls.lock = json.loads((ROOT / 'runtime.lock.json').read_text(encoding='utf-8'))
        cls.runtime = install_runtime(cls.bundle, cls.lock, cls.root / 'cache')

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.wait(timeout=10)
        cls.log.close()
        cls.temp.cleanup()

    def execute(self, mode, args):
        result = subprocess.run([sys.executable, '-I', '-B', '-X', 'utf8',
                                 str(self.runtime / 'workbook_mcp/runtime_entry.py'),
                                 '--workspace', str(ROOT), mode, *args],
                                cwd=ROOT, capture_output=True, text=True, encoding='utf-8', timeout=60)
        self.assertEqual(0, result.returncode, result.stderr)
        return result

    def test_unauthorized_request_fails(self):
        with self.assertRaises(HTTPError) as error:
            Client(self.url, 'wrong-token')
        self.assertIn(error.exception.code, (401, 403))

    def test_pinned_runtime_mismatch_fails(self):
        with self.assertRaises(ValueError):
            self.client.call('workbook_get_runtime', {'runtime_id': '0' * 64})

    def test_guide_exposes_new_stage9_authoring_contract(self):
        guidance = self.client.call('workbook_get_guidance', {})
        stage9 = guidance['stage9Authoring']
        self.assertIn('A, B, C', stage9['choiceLabels'])
        self.assertIn('전체 문장', stage9['coverage'])
        self.assertIn('answerOrder', stage9['answerKey'])
        self.assertIn('정답 순열', stage9['questionSet'])
        self.assertIn('새 packet', stage9['verification'])

    def test_remote_validation_and_compilation(self):
        from workbook_engine.compiler import compile_workbook
        value = json.loads((ROOT / 'workbooks/chocolate/content.json').read_text(encoding='utf-8'))
        result = self.client.call('workbook_validate_canonical', {'canonical': value})
        self.assertEqual('passed', result['status'])
        self.assertEqual(compile_workbook(value, 'answer'), self.client.call('workbook_compile', {
            'canonical': value, 'edition': 'answer'}))
        invalid = self.client.call('workbook_validate_canonical', {'canonical': {}})
        self.assertEqual('invalid_input', invalid['status'])

    def test_direct_mcp_authoring_verify_and_expand(self):
        # A deliberately empty synthetic input checks tool registration and the
        # validation gate without transmitting a source-derived authoring packet.
        for tool in ('workbook_authoring_verify', 'workbook_authoring_expand'):
            with self.subTest(tool=tool), self.assertRaises(ValueError):
                self.client.call(tool, {'packet': {}})

    def test_all_original_canonical_ir_and_html_bytes(self):
        baseline = json.loads((ROOT / 'reports/remote-mcp/render-baseline.json').read_text(encoding='utf-8'))
        results = []
        for index, record in enumerate(baseline['records']):
            with self.subTest(canonical=record['canonical'], edition=record['edition']):
                ir = self.root / f'{index}.json'
                html = self.root / f'{index}.html'
                args = [record['canonical'], '--edition', record['edition']]
                self.execute('engine', ['compile', *args, '--output', str(ir)])
                self.execute('render', [*args, '--output', str(html)])
                self.assertEqual(record['irSha256'], hashlib.sha256(ir.read_bytes()).hexdigest())
                self.assertEqual(record['htmlSha256'], hashlib.sha256(html.read_bytes()).hexdigest())
                results.append(record | {'status': 'byte-identical'})
        (self.root / 'parity-results.json').write_text(
            json.dumps({'transport': 'authenticated HTTP MCP', 'runtimeId': self.lock['runtimeId'],
                        'records': results}, ensure_ascii=False, indent=2), encoding='utf-8')

    def test_original_input_digests_survive_workspace_binding(self):
        baseline = json.loads((ROOT / 'reports/remote-mcp/render-baseline.json').read_text(encoding='utf-8'))
        code = ('import sys,json; from pathlib import Path; sys.path.insert(0,sys.argv[1]); '
                'from workbook_mcp.runtime_entry import bind_workspace; root=Path(sys.argv[2]); '
                'bind_workspace(root); from workbook_engine.release import _input_digests; '
                'print(json.dumps(_input_digests(root/"workbooks/chocolate/content.json",root/"updates/U-20260710-001.json")))')
        result = subprocess.run([sys.executable, '-I', '-B', '-c', code, str(self.runtime), str(ROOT)],
                                capture_output=True, text=True, encoding='utf-8', timeout=30)
        self.assertEqual(0, result.returncode, result.stderr)
        current = json.loads(result.stdout)
        changed_sources = {'workbook_engine/validator.py', 'workbook_engine/qa.py',
                           'config/versions.json', 'docs/semantic-rubric.md'}
        self.assertEqual(
            {key: value for key, value in baseline['inputDigests'].items() if key not in changed_sources},
            {key: value for key, value in current.items() if key not in changed_sources},
        )
        for changed_source in changed_sources:
            self.assertEqual(hashlib.sha256((ROOT / changed_source).read_bytes()).hexdigest(),
                             current[changed_source])

    def test_workspace_metadata_contract_and_version_gate_survive(self):
        code = '''import sys,json
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from workbook_mcp.runtime_entry import bind_workspace
root=Path(sys.argv[2]); bind_workspace(root)
import workbook_engine.release as r
from workbook_engine.manifest import ManifestBundle
canonical=json.loads((root/'workbooks/chocolate/content.json').read_text(encoding='utf-8'))
previous=r._previous_bundle(canonical['workbookId'])
r._enforce_version_transitions(previous=previous,canonical=canonical,spec=r.load_spec(),versions=r.load_json(r.VERSIONS_PATH))
print(json.dumps({'root':str(r.ROOT),'engine':r.file_manifest(r.ENGINE_INPUT_PATHS,root=r.ROOT)}))
'''
        result = subprocess.run([sys.executable, '-I', '-B', '-c', code, str(self.runtime), str(ROOT)],
                                capture_output=True, text=True, encoding='utf-8', timeout=30)
        self.assertEqual(0, result.returncode, result.stderr)
        value = json.loads(result.stdout)
        self.assertEqual(str(ROOT), value['root'])
        self.assertTrue(all(r['path'].startswith('workbook_engine/') for r in value['engine']['files']))

    def test_cache_has_no_pycache_after_execution(self):
        self.execute('engine', ['validate', 'workbooks/chocolate/content.json'])
        verify_cache(self.runtime, self.lock['manifest'])


if __name__ == '__main__':
    unittest.main()
