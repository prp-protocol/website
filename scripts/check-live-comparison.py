"""Data-free source tree checks; live research has separate transient validation."""
from pathlib import Path
import json,hashlib,runpy,subprocess
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'comparison'
c=json.loads((out/'live-config.json').read_text())
assert c['schema_version']==1 and len(c['cells'])==len(set(c['cells']))
for name,record in c['assets'].items():
 p=out/name;assert p.resolve().is_relative_to(out.resolve())
 b=p.read_bytes();assert len(b)==record['bytes'] and hashlib.sha256(b).hexdigest()==record['sha256']
runpy.run_path(str(out/'validate.py'))['validate_public_tree'](out)
assert not (out/'data.json').exists(),'Research source duplication'
assert not (out/'manifest.json').exists(),'Obsolete generated snapshot manifest'
for _ in range(2):subprocess.run(['python3',str(ROOT/'scripts/render-live-comparison.py'),'--check'],check=True)
subprocess.run(['python3',str(ROOT/'scripts/render-atlas.py'),'--check'],check=True)
for path in [out/'index.html',out/'methodology.html',out/'logos.html',*[out/'cells'/f'{id}.html' for id in c['cells']],*[out/'stacks'/f'{id}.html' for id in c['stacks']]]:
 text=path.read_text();assert 'live.js' in text and '<noscript>' in text and 'navigation.css' in text
print(json.dumps({'result':'PASS','stable_cells':len(c['cells']),'stable_stacks':len(c['stacks']),'research_source_copy':False,'deterministic_shell_checks':2,'asset_pins':len(c['assets'])}))
