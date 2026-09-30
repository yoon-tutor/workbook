"""Deterministic, allowlisted runtime distribution; no user data or secrets."""
import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def runtime_path_key(path):
    """Match Windows ordering explicitly on every server OS."""
    return path.as_posix().casefold()


def runtime_bundle():
    paths = [*ROOT.glob('workbook_engine/*.py'), *ROOT.glob('workbook_engine/templates/*'),
             *ROOT.glob('workbook_authoring/*.py'), *ROOT.glob('schemas/*.json')]
    paths += [ROOT / name for name in (
        'config/workbook-spec.json', 'config/versions.json', 'docs/semantic-rubric.md',
        'docs/authoring-pipeline.md', 'assets/yonjogyo-logo-footer.png',
        'scripts/authoring_packet.py', 'workbook_mcp/runtime_entry.py')]
    files = []
    for path in sorted(paths, key=runtime_path_key):
        if path.is_symlink() or not path.is_file():
            raise ValueError('Runtime source must be a regular file')
        data = path.read_bytes()
        files.append({'path': path.relative_to(ROOT).as_posix(), 'size': len(data),
                      'sha256': hashlib.sha256(data).hexdigest(),
                      'base64': base64.b64encode(data).decode('ascii')})
    manifest = {'format': 'workbook-runtime-v1', 'files': [
        {k: v for k, v in item.items() if k != 'base64'} for item in files]}
    return {'runtimeId': hashlib.sha256(canonical(manifest)).hexdigest(),
            'manifest': manifest, 'artifacts': files}


def write_lock(path):
    bundle = runtime_bundle()
    value = {'runtimeId': bundle['runtimeId'], 'manifest': bundle['manifest']}
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return value


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--lock', type=Path, required=True)
    args = parser.parse_args()
    print(write_lock(args.lock)['runtimeId'])
