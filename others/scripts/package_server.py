"""Build an allowlisted deployment context without local data or credentials."""
import argparse
import base64
from pathlib import Path
import shutil
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workbook_mcp.bundle import runtime_bundle
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
target = args.output.resolve()
if target.exists():
    raise SystemExit('Deployment context exists; choose a new directory')
target.mkdir(parents=True)
for artifact in runtime_bundle()['artifacts']:
    path = target / artifact['path']
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(artifact['base64'], validate=True))
for name in ('__init__.py', 'server.py', 'direct_release.py', 'bundle.py', 'requirements.txt'):
    shutil.copyfile(ROOT / 'workbook_mcp' / name, target / 'workbook_mcp' / name)
shutil.copyfile(ROOT / 'workbook_mcp/Dockerfile', target / 'Dockerfile')
print(target)
