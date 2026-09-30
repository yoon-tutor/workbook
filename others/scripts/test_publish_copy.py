"""Publish an already visually reviewed smoke build only in an isolated workspace."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
report = json.loads((ROOT / 'reports/remote-mcp/local-smoke.json').read_text(encoding='utf-8'))
review = json.loads((ROOT / 'reports/remote-mcp/visual-review.json').read_text(encoding='utf-8'))
if review['status'] != 'passed' or review['buildDir'] != report['buildDir']:
    raise SystemExit('Matching completed visual review is required')
runtime = ROOT / '.runtime' / report['runtimeId']
sys.dont_write_bytecode = True
sys.path.insert(0, str(runtime))
from workbook_mcp.runtime_entry import bind_workspace
from workbook_engine.release import PUBLIC_FILENAMES

with tempfile.TemporaryDirectory(dir=ROOT / '.build', prefix='publish-integration-') as folder:
    workspace = Path(folder)
    for relative in ('workbooks/chocolate/content.json', 'updates/U-20260710-001.json'):
        destination = workspace / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)
    build = workspace / '.build/reviewed'
    shutil.copytree(report['buildDir'], build)
    state_path = build / 'release-state.json'
    state = json.loads(state_path.read_text(encoding='utf-8'))
    state['canonicalPath'] = str(workspace / 'workbooks/chocolate/content.json')
    state['updatePath'] = str(workspace / 'updates/U-20260710-001.json')
    state['contactSheets'] = [str(build / Path(p).relative_to(report['buildDir'])) for p in state['contactSheets']]
    bind_workspace(workspace)
    from workbook_engine.release import _input_digests
    state['inputDigests'] = _input_digests(Path(state['canonicalPath']), Path(state['updatePath']))
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    completed = subprocess.run([sys.executable, '-I', '-B', '-X', 'utf8',
        str(runtime / 'workbook_mcp/runtime_entry.py'), '--workspace', str(workspace),
        'engine', 'publish', str(build), '--reviewer', 'Codex', '--notes', review['notes']],
        capture_output=True, text=True, encoding='utf-8', timeout=60)
    if completed.returncode:
        raise RuntimeError(completed.stderr)
    published = json.loads(completed.stdout)
    output = Path(published['outputDir'])
    assert output.is_relative_to(workspace)
    assert sorted(p.name for p in output.iterdir()) == sorted(PUBLIC_FILENAMES)
    for name in PUBLIC_FILENAMES:
        assert (output / name).read_bytes() == (build / name).read_bytes()
    assert all(Path(published[key]).is_file() for key in ('report', 'updateIndex', 'manifest'))
    result = {'status': 'passed', 'scope': 'temporary isolated workspace only',
              'files': list(PUBLIC_FILENAMES), 'copiedBytesIdentical': True,
              'reportAndIndexCreated': True, 'userOutputsChanged': False}
    (ROOT / 'reports/remote-mcp/publish-integration.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
