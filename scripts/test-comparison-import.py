#!/usr/bin/env python3
"""Temporary content-only fixtures: never import into the production checkout."""
from collections import Counter
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import copy
import hashlib
import json
import runpy
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'comparison'
api = runpy.run_path(str(OUT/'validate.py'))
prepare = runpy.run_path(str(ROOT/'scripts/import-comparison.py'))['prepare']
raw = (OUT/'data.json').read_bytes()
original = api['validate'](raw, OUT)
before = {str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in OUT.rglob('*') if p.is_file()}
fixture = copy.deepcopy(original)
criterion = next(c for c in fixture['criteria'] if c['id'] == 'F13')
criterion['title'] = 'Temporary <group> & "multiple senders"'
criterion['definition'] = 'Fixture <script>alert("no")</script> & unchanged stable IDs.'
payload = (json.dumps(fixture, ensure_ascii=False, indent=2)+'\n').encode()
receipt = dict(revision=fixture['revision'],date=fixture['date'],bytes=len(payload),
    sha256=hashlib.sha256(payload).hexdigest(),
    status_counts=dict(Counter(c['status'] for c in fixture['cells'])),
    changed_ids=dict(criteria=['F13'],columns=[],cells=[]))
outputs, delta = prepare(payload, receipt, OUT)

class View(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=[]; self.links=[]; self.scripts=0; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if 'href' in a: self.links.append(a['href'])
        self.scripts += tag == 'script'

index = outputs['index.html'].decode()
assert escape(criterion['title']) in index and escape(criterion['definition']) in index
old_view, new_view = View((OUT/'index.html').read_text()), View(index)
assert old_view.ids == new_view.ids and old_view.links == new_view.links and not new_view.scripts
assert len([x for x in new_view.links if x.startswith('cells/')]) == 798
assert 'row-F13' in new_view.ids and 'cells/F13-PN.html' in new_view.links
# Current criterion-label views are matrix row titles/definitions. Cell pages
# deliberately use stable IDs (not copied mutable criterion labels); profiles
# use column labels. All 798 cell pages and all 21 profiles remain byte-identical.
for name, data in outputs.items():
    if name not in ('data.json', 'manifest.json', 'index.html'):
        assert data == (OUT/name).read_bytes(), name
assert outputs['data.json'] == payload
assert delta == receipt['changed_ids']

def reject(data, reason):
    try: api['validate'](json.dumps(data).encode(), OUT)
    except (ValueError, KeyError, TypeError): return
    raise AssertionError('Accepted invalid fixture: '+reason)

bad=copy.deepcopy(original);bad['schema_version']=2;reject(bad,'schema')
bad=copy.deepcopy(original);bad['cells'].pop();reject(bad,'incomplete grid')
bad=copy.deepcopy(original);bad['cells'].append(bad['cells'][0]);reject(bad,'duplicate cell')
bad=copy.deepcopy(original);bad['cells'][0]['status']='MAYBE';reject(bad,'status')
bad=copy.deepcopy(original);bad['cells'][0]['sources']=['javascript:alert(1)'];reject(bad,'source')
bad=copy.deepcopy(original);bad['columns'][0]['logo']='missing.svg';reject(bad,'unknown logo')
bad=copy.deepcopy(original);bad['columns'][0]['logo']='../data.json';reject(bad,'asset traversal')
bad=copy.deepcopy(original);bad['cells'][0]['qualification']='/workspace/private';reject(bad,'private content')
for field, value in [('bytes',0),('sha256','bad'),('status_counts',{}),('changed_ids',dict(criteria=[],columns=[],cells=[]))]:
    broken=dict(receipt);broken[field]=value
    try: api['check_receipt'](payload,OUT,broken,original)
    except ValueError: pass
    else: raise AssertionError('Accepted wrong receipt: '+field)
bad=copy.deepcopy(original);bad['criteria'][0]['id']='F99'
try: api['changes'](original,bad)
except ValueError: pass
else: raise AssertionError('Accepted ID-set change')
with tempfile.TemporaryDirectory(prefix='comparison-bad-signature-') as tmp:
    tmp=Path(tmp)
    (tmp/'data.json').write_bytes(payload)
    (tmp/'receipt.json').write_text(json.dumps(dict(receipt,authority='fixture only',catalog_receipt='fixture only')))
    (tmp/'bad.asc').write_text('not a signature')
    rejected=subprocess.run(['python3',str(ROOT/'scripts/import-comparison.py'),
        str(tmp/'data.json'),'--receipt',str(tmp/'receipt.json'),
        '--signature',str(tmp/'bad.asc'),'--apply'],capture_output=True,text=True)
    assert rejected.returncode != 0 and 'Signature verification failed' in rejected.stderr
after = {str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in OUT.rglob('*') if p.is_file()}
assert before == after, 'Fixture modified production content or website assets'
print(json.dumps(dict(result='PASS',fixture='temporary F13 rename and escaping',
    stable_cells=798,stable_profiles=21,negative_cases=14,
    exact_json=True,website_ownership_preserved=True,production_unchanged=True,
    signature_note='Fixture tests staging only; no sealed input or signature verification claimed.')))
