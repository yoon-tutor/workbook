"""Capture once and verify original workspace bytes; never rewrite a baseline."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / 'others/reports/remote-mcp/original-files.json'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['capture', 'verify'])
    args = parser.parse_args()
    if args.command == 'capture':
        files = {}
        for path in ROOT.rglob('*'):
            if not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(ROOT).as_posix()
            if '__pycache__' in path.parts or relative.startswith(('others/reports/remote-mcp/', 'others/.runtime/')):
                continue
            files[relative] = digest(path)
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        with BASELINE.open('x', encoding='utf-8') as stream:
            json.dump({'files': files, 'allowedRoutingChanges': ['others/AGENTS.md']}, stream, ensure_ascii=False, indent=2)
        print(json.dumps({'status': 'captured', 'files': len(files)}))
    else:
        baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
        changes = [name for name, expected in baseline['files'].items()
                   if not (ROOT / name).is_file() or digest(ROOT / name) != expected]
        unexpected = [name for name in changes if name not in baseline['allowedRoutingChanges']
                      and name != 'others/docs/remote-mcp-migration.md']
        result = {'status': 'passed' if not unexpected else 'failed',
                  'checked': len(baseline['files']), 'intentionalRoutingChanges': changes,
                  'unexpectedChanges': unexpected}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(bool(unexpected))


if __name__ == '__main__':
    main()
