"""Record original deterministic IR/HTML bytes, before transport."""
import hashlib
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workbook_engine.compiler import compile_workbook
from workbook_engine.render import build_html
from workbook_engine.release import _input_digests
records = []
for path in sorted((ROOT / 'workbooks').glob('*/content.json')):
    value = json.loads(path.read_text(encoding='utf-8'))
    for edition in ('student', 'answer'):
        compiled = compile_workbook(value, edition)
        ir = (json.dumps(compiled, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n' if sys.platform == 'win32' else '\n').encode('utf-8')
        html = build_html(compiled).replace('\n', '\r\n' if sys.platform == 'win32' else '\n').encode('utf-8')
        records.append({'canonical': path.relative_to(ROOT).as_posix(), 'edition': edition,
                        'pages': len(compiled['pages']), 'irSha256': hashlib.sha256(ir).hexdigest(),
                        'htmlSha256': hashlib.sha256(html).hexdigest()})
baseline = ROOT / 'reports/remote-mcp/render-baseline.json'
baseline.parent.mkdir(parents=True, exist_ok=True)
with baseline.open('x', encoding='utf-8') as stream:
    json.dump({'records': records, 'inputDigests': _input_digests(
        ROOT / 'workbooks/chocolate/content.json', ROOT / 'updates/U-20260710-001.json')},
        stream, ensure_ascii=False, indent=2)
print(json.dumps({'editions': len(records), 'status': 'captured'}))
