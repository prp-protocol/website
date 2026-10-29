#!/usr/bin/env python3
"""Pre-import pinned retirement negatives. Inputs and custody receipt stay private."""
from pathlib import Path
import argparse,hashlib,json,runpy,shutil,tempfile
ap=argparse.ArgumentParser();ap.add_argument('snapshot',type=Path);ap.add_argument('receipt',type=Path);ap.add_argument('archive',type=Path);args=ap.parse_args()
root=Path(__file__).resolve().parents[1];dest=root/'comparison';api=runpy.run_path(str(dest/'validate.py'));imp=runpy.run_path(str(root/'scripts/import-comparison.py'))
raw=args.snapshot.read_bytes();receipt=json.loads(args.receipt.read_text());arc=args.archive.read_bytes();old=api['validate']((dest/'data.json').read_bytes(),dest)
def hashes():return {str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.rglob('*') if p.is_file()}
before=hashes();tests=[]
def reject(label,fn):
    try:fn()
    except ValueError:tests.append(label)
    else:raise AssertionError('Accepted '+label)
with tempfile.TemporaryDirectory(prefix='r748-negative-') as tmp:
    stage=Path(tmp)/'comparison';shutil.copytree(dest,stage)
    def check(b=raw,r=receipt,a=arc,**flags):return api['check_receipt'](b,stage,r,old,retirement_r748=True,archive_raw=a,**flags)
    data,delta=check();assert len(data['cells'])==1736
    reject('ordinary retirement',lambda:api['check_receipt'](raw,stage,receipt,old))
    reject('mixed exceptions',lambda:check(expansion_r708=True))
    reject('missing archive',lambda:check(a=None))
    reject('modified archive',lambda:check(a=arc+b' '))
    for field,value in [('removed_ids',dict(criteria=['F01'],columns=[],cells=[])),('added_ids',dict(criteria=['K02'],columns=[],cells=[])),('changed_ids',dict(criteria=[],columns=[],cells=[])),('new_assets',[{'file':'logos/unapproved.svg'}]),('sealed_receipt_sha256','wrong'),('archive_sha256','wrong')]:
        bad=dict(receipt);bad[field]=value;reject('wrong '+field,lambda bad=bad:check(r=bad))
    badraw=raw+b' ';bad=dict(receipt,bytes=len(badraw),sha256=hashlib.sha256(badraw).hexdigest());reject('unapproved snapshot bytes',lambda:check(badraw,bad))
    baseline=(stage/'data.json').read_bytes();(stage/'data.json').write_bytes(baseline+b' ')
    reject('unapproved baseline bytes',lambda:check());(stage/'data.json').write_bytes(baseline)
    for kind in ['remove','expand','renumber']:
        modified=json.loads(raw)
        if kind=='remove':
            modified['criteria']=[r for r in modified['criteria'] if r['id']!='F01'];modified['cells']=[c for c in modified['cells'] if c['feature']!='F01']
        else:
            row=dict(modified['criteria'][0],id='K02');cells=[dict(c,id='K02-'+c['stack'],feature='K02') for c in modified['cells'] if c['feature']==modified['criteria'][0]['id']]
            if kind=='renumber':
                ident=modified['criteria'][0]['id'];modified['criteria']=[r for r in modified['criteria'] if r['id']!=ident];modified['cells']=[c for c in modified['cells'] if c['feature']!=ident]
            modified['criteria'].append(row);modified['cells']+=cells
        reject('arbitrary '+kind,lambda m=modified:api['changes'](old,m))
reject('asset with retirement',lambda:imp['prepare'](raw,receipt,dest,retirement_r748=True,archive_raw=arc,assets={'logos/unapproved.svg':b'<svg/>'}))
reject('archive without exception',lambda:imp['prepare'](raw,receipt,dest,archive_raw=arc))
assert hashes()==before
print(json.dumps(dict(result='PASS',positive='exact baseline/output/archive-bound retirement',rejected=tests,production_unchanged=True)))
