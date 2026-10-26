#!/usr/bin/env python3
"""Pre-import, temporary exact-expansion negatives; private inputs stay external."""
from pathlib import Path
import argparse,copy,hashlib,json,runpy,shutil,tempfile
ap=argparse.ArgumentParser();ap.add_argument('snapshot',type=Path);ap.add_argument('receipt',type=Path);ap.add_argument('objects',type=Path);args=ap.parse_args()
root=Path(__file__).resolve().parents[1];dest=root/'comparison'
api=runpy.run_path(str(dest/'validate.py'));imp=runpy.run_path(str(root/'scripts/import-comparison.py'))
raw=args.snapshot.read_bytes();receipt=json.loads(args.receipt.read_text());old=api['validate']((dest/'data.json').read_bytes(),dest)
assets={k:(args.objects/sha).read_bytes() for k,(sha,size) in imp['ASSETS_R708'].items()}
before={str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.rglob('*') if p.is_file()}
tests=[]
def rejects(label,fn):
    try:fn()
    except ValueError:tests.append(label)
    else:raise AssertionError('Accepted '+label)
with tempfile.TemporaryDirectory(prefix='r708-negative-') as tmp:
    stage=Path(tmp)/'comparison';shutil.copytree(dest,stage)
    for name,b in assets.items():(stage/name).write_bytes(b)
    new,delta=api['check_receipt'](raw,stage,receipt,old,expansion_r708=True)
    assert len(new['cells'])==1792
    rejects('ordinary expansion',lambda:api['check_receipt'](raw,stage,receipt,old))
    rejects('mixed exceptions',lambda:api['check_receipt'](raw,stage,receipt,old,expansion_r708=True,retirement_r582=True))
    for field,value in [('added_ids',dict(criteria=[],columns=[],cells=[])),('removed_ids',dict(criteria=['F01'],columns=[],cells=[])),('changed_ids',dict(criteria=[],columns=[],cells=[])),('new_assets',[]),('sealed_receipt_sha256','wrong')]:
        bad=dict(receipt);bad[field]=value
        rejects('wrong '+field,lambda bad=bad:api['check_receipt'](raw,stage,bad,old,expansion_r708=True))
    badraw=raw+b' ';bad=dict(receipt,bytes=len(badraw),sha256=hashlib.sha256(badraw).hexdigest())
    rejects('different snapshot bytes',lambda:api['check_receipt'](badraw,stage,bad,old,expansion_r708=True))
    baseline=(stage/'data.json').read_bytes();(stage/'data.json').write_bytes(baseline+b' ')
    rejects('different baseline bytes',lambda:api['check_receipt'](raw,stage,receipt,old,expansion_r708=True))
rejects('assets without exception',lambda:imp['prepare'](raw,receipt,dest,assets=assets))
rejects('missing assets',lambda:imp['prepare'](raw,receipt,dest,expansion_r708=True))
badassets=dict(assets);badassets['logos/unapproved.svg']=b'<svg/>'
rejects('extra asset',lambda:imp['prepare'](raw,receipt,dest,assets=badassets,expansion_r708=True))
badassets=dict(assets);badassets['logos/rina-label.svg']+=b' '
rejects('modified asset',lambda:imp['prepare'](raw,receipt,dest,assets=badassets,expansion_r708=True))
after={str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.rglob('*') if p.is_file()}
assert before==after
print(json.dumps(dict(result='PASS',positive='exact pinned snapshot and baseline',rejected=tests,production_unchanged=True)))
