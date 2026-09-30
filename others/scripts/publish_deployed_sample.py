"""Publish a reviewed remote sample in a separate workspace, preserving history."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.run import configuration


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', type=Path, required=True)
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    if not workspace.is_relative_to(ROOT / '.build') or workspace == ROOT / '.build':
        raise ValueError('Sample workspace must be a new child of .build')
    if (workspace / '.build').exists():
        raise FileExistsError('Sample workspace already used')
    public_root = (ROOT.parent / 'outputs').resolve()
    if (workspace / 'outputs').resolve() != public_root:
        raise ValueError('Sample outputs must link to the existing public outputs root')
    report = json.loads((ROOT / 'reports/remote-mcp/deployed-smoke.json').read_text(encoding='utf-8'))
    review = json.loads((ROOT / 'reports/remote-mcp/deployed-visual-review.json').read_text(encoding='utf-8'))
    if review['status'] != 'passed' or review['buildDir'] != report['buildDir']:
        raise ValueError('Matching completed visual review is required')
    for relative in ('workbooks/chocolate/content.json', 'updates/U-20260710-001.json',
                     'scripts/run.py', 'runtime.lock.json'):
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
    # Keep the expected input and artifact hashes: the remote publisher checks them.
    state['outputBase'] = 'mcp_chocolate_remote_20260922'
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    url, token = configuration()
    env = dict(os.environ, WORKBOOK_MCP_URL=url, WORKBOOK_MCP_API_TOKEN=token,
               PYTHONDONTWRITEBYTECODE='1')
    result = subprocess.run([sys.executable, '-X', 'utf8', str(workspace / 'scripts/run.py'),
                             'publish', str(build), '--reviewer', 'Codex', '--notes', review['notes']],
                            cwd=workspace, env=env, capture_output=True, text=True, encoding='utf-8', timeout=120)
    if result.returncode:
        raise RuntimeError(result.stderr)
    published = json.loads(result.stdout)
    output = Path(published['outputDir']).resolve()
    if output.parent != public_root:
        raise ValueError('Unexpected publication path')
    files = ['문제.html', '문제.pdf', '해설.html', '해설.pdf']
    if sorted(p.name for p in output.iterdir()) != sorted(files):
        raise ValueError('Public file contract changed')
    for name in files:
        if (output / name).read_bytes() != (Path(report['buildDir']) / name).read_bytes():
            raise ValueError('Published bytes differ from reviewed bytes')
    evidence = {'status': 'published', 'transport': 'deployed HTTPS MCP', 'workspace': str(workspace),
                'sourceBuildDir': report['buildDir'], 'outputDir': str(output),
                'copiedBytesIdentical': True, 'files': files, 'release': published}
    (ROOT / 'reports/remote-mcp/deployed-publish.json').write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(evidence, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
