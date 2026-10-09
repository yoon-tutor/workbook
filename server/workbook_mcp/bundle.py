"""Deterministic identity of the engine, rules and templates the server runs.

The identity (``engineId``) changes whenever any allowlisted engine input changes,
so guidance responses and release evidence name the exact rule set in use.
"""
import hashlib
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def runtime_path_key(path):
    """Match Windows ordering explicitly on every server OS."""
    return path.as_posix().casefold()


def engine_paths():
    paths = [*ROOT.glob('workbook_engine/*.py'), *ROOT.glob('workbook_engine/templates/*'),
             *ROOT.glob('workbook_authoring/*.py'), *ROOT.glob('schemas/*.json')]
    paths += [ROOT / name for name in (
        'config/workbook-spec.json', 'config/versions.json', 'docs/semantic-rubric.md',
        'docs/authoring-pipeline.md', 'assets/yonjogyo-logo-footer.png',
        'workbook_mcp/runtime_entry.py')]
    return sorted(paths, key=lambda path: runtime_path_key(path.relative_to(ROOT)))


@lru_cache(maxsize=1)
def engine_identity():
    files = []
    for path in engine_paths():
        if path.is_symlink() or not path.is_file():
            raise ValueError('Engine source must be a regular file')
        data = path.read_bytes()
        files.append({'path': path.relative_to(ROOT).as_posix(), 'size': len(data),
                      'sha256': hashlib.sha256(data).hexdigest()})
    manifest = {'format': 'workbook-engine-v1', 'files': files}
    return {'engineId': hashlib.sha256(canonical(manifest)).hexdigest(), 'manifest': manifest}
