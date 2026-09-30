"""Thin MCP client: pinned remote scripts, local files, no engine fallback."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.error
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[1]
MAX_RESPONSE = 32 * 1024 * 1024


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def configuration(root=ROOT):
    values = {}
    path = root / '.env'
    if path.is_file():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                values[key.strip()] = value.strip().strip('\"').strip("'")
    url = values.get('WORKBOOK_MCP_URL', os.environ.get('WORKBOOK_MCP_URL', '')).strip()
    token = values.get('WORKBOOK_MCP_API_TOKEN', os.environ.get('WORKBOOK_MCP_API_TOKEN', '')).strip()
    parsed = urllib.parse.urlsplit(url)
    if (parsed.username or parsed.password or parsed.query or parsed.fragment or not parsed.hostname
        or (parsed.scheme != 'https' and not (parsed.scheme == 'http' and parsed.hostname in
                                               ('localhost', '127.0.0.1', '::1')))):
        raise ValueError('Configure an HTTPS WORKBOOK_MCP_URL in others/.env')
    if not token:
        raise ValueError('Configure WORKBOOK_MCP_API_TOKEN in others/.env')
    return url, token


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('MCP redirects are not allowed')


class Client:
    def __init__(self, url, token):
        self.url = url
        self.opener = urllib.request.build_opener(NoRedirect())
        self.headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json',
                        'Accept': 'application/json, text/event-stream'}
        initialized = self.rpc('initialize', {'protocolVersion': '2025-03-26', 'capabilities': {},
                               'clientInfo': {'name': 'workbook-local', 'version': '1.0'}}, 1)
        self.headers['MCP-Protocol-Version'] = initialized['protocolVersion']
        self.rpc('notifications/initialized', {})

    def rpc(self, method, params, identity=None):
        body = {'jsonrpc': '2.0', 'method': method, 'params': params}
        if identity is not None:
            body['id'] = identity
        request = urllib.request.Request(self.url, data=canonical(body), headers=self.headers)
        for attempt in range(3):
            try:
                with self.opener.open(request, timeout=60) as response:
                    session = response.headers.get('Mcp-Session-Id')
                    if session:
                        self.headers['Mcp-Session-Id'] = session
                    data = response.read(MAX_RESPONSE + 1)
                break
            except urllib.error.HTTPError:
                raise
            except urllib.error.URLError:
                if attempt == 2:
                    raise
                time.sleep((0.25, 0.75)[attempt])
        if len(data) > MAX_RESPONSE:
            raise ValueError('MCP response exceeds size limit')
        if not data:
            if identity is not None:
                raise ValueError('Empty MCP response')
            return {}
        result = json.loads(data)
        if result.get('jsonrpc') != '2.0' or result.get('id') != identity or 'error' in result:
            raise ValueError('MCP protocol error')
        return result['result']

    def call(self, name, arguments):
        result = self.rpc('tools/call', {'name': name, 'arguments': arguments}, 2)
        if result.get('isError'):
            raise ValueError('MCP tool failed; no local fallback')
        if 'structuredContent' in result:
            return result['structuredContent']
        return json.loads(next(item['text'] for item in result['content'] if item['type'] == 'text'))


def safe_path(value):
    if (not isinstance(value, str) or not value or '\\' in value or ':' in value
        or PurePosixPath(value).is_absolute()):
        raise ValueError('Invalid runtime path')
    for part in value.split('/'):
        if (part in ('', '.', '..') or part.endswith(('.', ' '))
            or re.search(r'[<>"|?*\x00-\x1f]', part)
            or part.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL',
                                            *('COM' + str(n) for n in range(1, 10)),
                                            *('LPT' + str(n) for n in range(1, 10))}):
            raise ValueError('Invalid runtime path')
    return value


def validate_lock(lock):
    manifest = lock['manifest']
    if manifest.get('format') != 'workbook-runtime-v1':
        raise ValueError('Unsupported runtime format')
    if hashlib.sha256(canonical(manifest)).hexdigest() != lock['runtimeId']:
        raise ValueError('Runtime lock hash mismatch')
    seen = set()
    for record in manifest['files']:
        name = safe_path(record['path'])
        if name.casefold() in seen or not re.fullmatch('[0-9a-f]{64}', record['sha256']):
            raise ValueError('Invalid runtime manifest')
        seen.add(name.casefold())
    return manifest


def verify_cache(target, manifest):
    if target.is_symlink() or not target.is_dir():
        raise ValueError('Invalid runtime cache')
    expected = {record['path']: record for record in manifest['files']}
    actual = set()
    for path in target.rglob('*'):
        if path.is_symlink():
            raise ValueError('Runtime cache must not contain links')
        if path.is_file():
            name = path.relative_to(target).as_posix()
            actual.add(name)
            record = expected.get(name)
            data = path.read_bytes()
            if not record or len(data) != record['size'] or hashlib.sha256(data).hexdigest() != record['sha256']:
                raise ValueError('Runtime cache was modified')
    if actual != set(expected):
        raise ValueError('Runtime cache is incomplete')


def install_runtime(result, lock, cache_root):
    manifest = validate_lock(lock)
    if result['runtimeId'] != lock['runtimeId'] or result['manifest'] != manifest:
        raise ValueError('Server runtime differs from the reviewed local lock')
    cache_root.mkdir(parents=True, exist_ok=True)
    if cache_root.is_symlink():
        raise ValueError('Cache root cannot be a link')
    target = cache_root / lock['runtimeId']
    expected = {record['path']: record for record in manifest['files']}
    decoded = {}
    for artifact in result['artifacts']:
        name = safe_path(artifact['path'])
        if name in decoded or {k: v for k, v in artifact.items() if k != 'base64'} != expected.get(name):
            raise ValueError('Runtime artifact does not match lock')
        data = base64.b64decode(artifact['base64'], validate=True)
        if len(data) != expected[name]['size'] or hashlib.sha256(data).hexdigest() != expected[name]['sha256']:
            raise ValueError('Runtime artifact hash mismatch')
        decoded[name] = data
    if set(decoded) != set(expected):
        raise ValueError('Runtime artifacts are incomplete')
    if target.exists() or target.is_symlink():
        if target.is_symlink() or target.resolve().parent != cache_root.resolve():
            raise ValueError('Invalid runtime cache')
        try:
            verify_cache(target, manifest)
        except ValueError:
            # Keep unexpected cache contents for inspection, then restore the exact pinned runtime.
            quarantine = cache_root / f'.invalid-{lock["runtimeId"]}-{uuid.uuid4().hex}'
            try:
                target.rename(quarantine)
            except FileNotFoundError:
                pass  # Another process already moved the invalid cache.
        else:
            return target
    staging = Path(tempfile.mkdtemp(prefix='.install-', dir=cache_root))
    try:
        for name, data in decoded.items():
            destination = staging.joinpath(*PurePosixPath(name).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        verify_cache(staging, manifest)
        try:
            staging.rename(target)
        except FileExistsError:
            verify_cache(target, manifest)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['guide', 'sync', 'validate', 'inspect', 'compile',
                                          'render', 'prepare', 'status', 'publish', 'authoring', 'migrate-legacy'])
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    client = Client(*configuration())
    if args.command == 'guide':
        print(json.dumps(client.call('workbook_get_guidance', {}), ensure_ascii=False, indent=2))
        return 0
    lock = json.loads((ROOT / 'runtime.lock.json').read_text(encoding='utf-8'))
    validate_lock(lock)
    result = client.call('workbook_get_runtime', {'runtime_id': lock['runtimeId']})
    runtime = install_runtime(result, lock, ROOT / '.runtime')
    if args.command == 'sync':
        print(json.dumps({'status': 'verified', 'runtimeId': lock['runtimeId'], 'cache': str(runtime)}))
        return 0
    mode = args.command if args.command in ('authoring', 'render') else 'engine'
    arguments = args.arguments if mode != 'engine' else [args.command, *args.arguments]
    # The server never chooses a command, working directory, or user arguments.
    env = dict(os.environ)
    env.pop('WORKBOOK_MCP_API_TOKEN', None)
    env.pop('PYTHONPATH', None)
    return subprocess.run([sys.executable, '-I', '-B', '-X', 'utf8',
                           str(runtime / 'workbook_mcp/runtime_entry.py'),
                           '--workspace', str(ROOT), mode, *arguments], cwd=ROOT, env=env).returncode


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as error:
        result = {'status': 'error', 'type': type(error).__name__,
                  'message': 'MCP 연결, .env 및 runtime.lock.json을 확인하세요. 로컬 대체 실행은 하지 않았습니다.'}
        if isinstance(error, urllib.error.URLError):
            reason = error.reason
            result['cause'] = type(reason).__name__
            if isinstance(getattr(reason, 'errno', None), int):
                result['errno'] = reason.errno
            if isinstance(getattr(reason, 'verify_code', None), int):
                result['verifyCode'] = reason.verify_code
        elif isinstance(error, ValueError) and str(error) in {
            'Invalid runtime cache', 'Runtime cache must not contain links',
            'Runtime cache was modified', 'Runtime cache is incomplete',
            'Server runtime differs from the reviewed local lock',
            'Runtime lock hash mismatch', 'MCP protocol error',
            'MCP tool failed; no local fallback',
        }:
            result['cause'] = str(error)
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
