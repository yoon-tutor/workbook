"""Exercise the actual thin CLI and private PDF prepare over HTTP MCP."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.run import Client, configuration


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--deployed', action='store_true')
    args = parser.parse_args()
    report_dir = ROOT / 'reports/remote-mcp'
    process = None
    log = None
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    try:
        if args.deployed:
            url, token = configuration()
        else:
            if (ROOT / '.env').exists():
                raise RuntimeError('Local smoke must not override a configured production .env')
            token = secrets.token_urlsafe(32)
            with socket.socket() as probe:
                probe.bind(('127.0.0.1', 0))
                port = probe.getsockname()[1]
            url = f'http://127.0.0.1:{port}/mcp'
            env.update(WORKBOOK_MCP_URL=url, WORKBOOK_MCP_API_TOKEN=token, PORT=str(port), HOST='127.0.0.1')
            log = (report_dir / 'smoke-server.log').open('w', encoding='utf-8')
            process = subprocess.Popen([sys.executable, '-X', 'utf8', '-m', 'workbook_mcp.server'],
                                       cwd=ROOT, env=env, stdout=log, stderr=log,
                                       creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                try:
                    Client(url, token)
                    break
                except OSError:
                    if process.poll() is not None:
                        raise RuntimeError('Smoke server failed')
                    time.sleep(0.2)
            else:
                raise RuntimeError('Smoke server startup timed out')

        records = []
        def cli(*arguments):
            result = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'scripts/run.py'), *arguments],
                                    cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', timeout=180)
            records.append({'command': list(arguments), 'returncode': result.returncode,
                            'stdout': result.stdout, 'stderr': result.stderr})
            if result.returncode:
                raise RuntimeError('Thin CLI failed: ' + arguments[0])
            return json.loads(result.stdout[result.stdout.index('{'):])

        guidance = cli('guide')
        synced = cli('sync')
        cli('validate', 'workbooks/chocolate/content.json')
        prepared = cli('prepare', 'workbooks/chocolate/content.json', '--update', 'updates/U-20260710-001.json',
                       '--output-base', 'mcp_parity_chocolate')
        build = Path(prepared['buildDir'])
        status = cli('status', 'workbooks/chocolate/content.json', '--build-dir', str(build))
        if not status['inputsCurrent'] or not status['artifactsIntact'] or not status['canPublish']:
            raise RuntimeError('Prepared release integrity check failed')
        state = json.loads((build / 'release-state.json').read_text(encoding='utf-8'))
        baseline = json.loads((report_dir / 'render-baseline.json').read_text(encoding='utf-8'))
        if state['inputDigests'] != baseline['inputDigests']:
            raise RuntimeError('Input digest contract changed')
        report = {'status': 'automated-passed-awaiting-visual-review',
                  'transport': 'deployed HTTPS' if args.deployed else 'local authenticated HTTP',
                  'url': url, 'runtimeId': synced['runtimeId'], 'buildDir': str(build),
                  'pageCount': prepared['pageCount'], 'contactSheets': prepared['contactSheets'],
                  'publicOutputsCreated': False, 'inputDigestsIdentical': True,
                  'commands': records}
        destination = report_dir / ('deployed-smoke.json' if args.deployed else 'local-smoke.json')
        destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({key: report[key] for key in ('status', 'buildDir', 'pageCount', 'contactSheets')}, ensure_ascii=False))
    finally:
        if process:
            process.terminate()
            process.wait(timeout=10)
        if log:
            log.close()


if __name__ == '__main__':
    main()
