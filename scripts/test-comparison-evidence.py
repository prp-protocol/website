#!/usr/bin/env python3
"""Schema2 annotation negatives and escaped output; temporary fixtures only."""
import copy,hashlib,json,runpy,subprocess,tempfile,shutil
from pathlib import Path
from collections import Counter
from html import escape
root=Path(__file__).resolve().parents[1];out=root/'comparison'
api=runpy.run_path(str(out/'validate.py'));raw=(out/'data.json').read_bytes();d=api['validate'](raw,out)
assert d['schema_version']==2
assert Counter(c['evidence']['level'] for c in d['cells'])==dict(assumed=98,reported=52,documented=1578,demonstrated=8)
cases=[]
for key,value in [('level','unclassified'),('basis',''),('scope',[]),('attribution',None),('coverage',False),('reviewed_at','2026-02-30'),('basis_sha256','invalid'),('references','index.html#private')]:
    bad=copy.deepcopy(d);bad['cells'][0]['evidence'][key]=value;cases.append(bad)
bad=copy.deepcopy(d);del bad['cells'][0]['evidence'];cases.append(bad)
bad=copy.deepcopy(d);bad['cells'][0]['evidence']['extra']='unknown';cases.append(bad)
bad=copy.deepcopy(d);bad['evidence_policy']['levels']['unknown']={};cases.append(bad)
bad=copy.deepcopy(d);bad['evidence_policy']['version']=2;cases.append(bad)
for bad in cases:
    try:api['validate'](json.dumps(bad).encode(),out)
    except (ValueError,TypeError,KeyError):pass
    else:raise AssertionError('Malformed annotation accepted')
base=subprocess.check_output(['git','show','4f27d5d5d0c35ce35c56f4c2316d9c7d37bf0f13:comparison/data.json'])
old=json.loads(base)
receipt=dict(revision=d['revision'],date=d['date'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),status_counts=dict(Counter(c['status'] for c in d['cells'])),changed_ids=api['changes'](old,d))
for flags in ({},{'schema_r796':True}):
    try:api['check_receipt'](raw,out,receipt,old,**flags)
    except ValueError:pass
    else:raise AssertionError('Schema transition without exact authority pins accepted')
# An existing valid logo cannot be selected as an uncoordinated asset change.
bad=copy.deepcopy(d);bad['columns'][0]['logo']=next(c['logo'] for c in bad['columns'] if c['logo']!=bad['columns'][0]['logo'])
altered=json.dumps(bad).encode();r=dict(receipt,bytes=len(altered),sha256=hashlib.sha256(altered).hexdigest(),changed_ids=api['changes'](d,bad))
try:api['check_receipt'](altered,out,r,d)
except ValueError:pass
else:raise AssertionError('Uncoordinated logo selection accepted')
fixture=copy.deepcopy(d);sentinel='<script>alert("evidence")</script> & "quote"'
for key in ('basis','scope','attribution','coverage'):fixture['cells'][0]['evidence'][key]=sentinel
fixture['cells'][0]['evidence']['references']=[sentinel,'index.html#non-public-record']
fixture['evidence_policy']['interpretation']=sentinel
with tempfile.TemporaryDirectory(prefix='evidence-fixture-') as tmp:
    dest=Path(tmp)/'comparison';shutil.copytree(out,dest)
    (dest/'data.json').write_text(json.dumps(fixture))
    subprocess.run(['python3','-I',str(dest/'render.py'),'--out',str(dest)],check=True,capture_output=True)
    page=(dest/'cells'/f"{fixture['cells'][0]['id']}.html").read_text()
    assert sentinel not in page and escape(sentinel) in page
    assert 'href="index.html#non-public-record"' not in page
    assert escape(sentinel) in (dest/'index.html').read_text()
    assert escape(sentinel) in (dest/'methodology.html').read_text()
assert raw==(out/'data.json').read_bytes()
for c in d['cells']:
    page=(out/'cells'/f"{c['id']}.html").read_text()
    for key in ('basis','scope','attribution','coverage','reviewed_at','basis_sha256'):
        assert escape(c['evidence'][key]) in page,(c['id'],key)
print(json.dumps(dict(result='PASS',malformed_cases=len(cases),transition_negatives=2,asset_negative=True,escaping=True,detail_pages=len(d['cells']),production_unchanged=True)))
