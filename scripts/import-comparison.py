#!/usr/bin/env python3
"""Validate one approved sealed JSON; stage a coherent build. Dry-run by default."""
from pathlib import Path
import argparse
import hashlib
import json
import runpy
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SIGNER = 'BDF794EB7E1CBDE115BDC13B29F9A1FA8EA34B8A'
ASSETS_R269 = {
    'logos/hipv2.svg': ('d836317b845bf765811c594420841ae5c1d4e480bc20c5d07b2774917e66174e',328),
    'logos/ccnx.svg': ('b6fe33cda3f2bf2162015577d7a97d7b77d2940b7d2d9c6a5373e8f0c8b3c644',327),
    'logos/iot-rpl.svg': ('fff20dd148fd75e85bddfe45c8766dadc94afa56040ed4c7dac5ef2837548bae',330),
}


def prepare(snapshot, receipt, destination, expansion_r214=False, expansion_r269=False, assets=None):
    api = runpy.run_path(str(destination/'validate.py'))
    old = api['validate']((destination/'data.json').read_bytes(), destination)
    assets = assets or {}
    if assets and not expansion_r269: raise ValueError('Assets require coordinated expansion')
    if expansion_r269:
        if set(assets)!=set(ASSETS_R269): raise ValueError('Exact 2.69 assets required')
        for name,raw in assets.items():
            digest,size=ASSETS_R269[name]
            if len(raw)!=size or hashlib.sha256(raw).hexdigest()!=digest: raise ValueError('Unapproved asset bytes')
    with tempfile.TemporaryDirectory(prefix='comparison-import-') as tmp:
        stage = Path(tmp)/'comparison'
        shutil.copytree(destination, stage)
        for name,raw in assets.items():
            if (destination/name).exists(): raise ValueError('Refusing to overwrite existing asset')
            (stage/name).write_bytes(raw)
        data, delta = api['check_receipt'](snapshot, stage, receipt, old, expansion_r214, expansion_r269)
        (stage/'data.json').write_bytes(snapshot)
        subprocess.run(['python3', '-I', str(stage/'render.py'), '--out', str(stage)], check=True, capture_output=True)
        first = (stage/'manifest.json').read_bytes()
        subprocess.run(['python3', '-I', str(stage/'render.py'), '--out', str(stage)], check=True, capture_output=True)
        if (stage/'manifest.json').read_bytes() != first:
            raise ValueError('Non-reproducible build')
        # Only approved JSON, generated HTML and manifest can leave staging.
        outputs = {'data.json', 'manifest.json', 'index.html', 'methodology.html', 'logos.html'}
        outputs |= set(assets)
        outputs |= {'cells/'+c['id']+'.html' for c in data['cells']}
        outputs |= {'stacks/'+c['id']+'.html' for c in data['columns']}
        for p in destination.rglob('*'):
            if p.is_file() and str(p.relative_to(destination)) not in outputs:
                if p.read_bytes() != (stage/p.relative_to(destination)).read_bytes():
                    raise ValueError('Website-owned file changed: ' + str(p))
        return {name: (stage/name).read_bytes() for name in outputs}, delta


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('snapshot', type=Path)
    ap.add_argument('--receipt', required=True, type=Path)
    ap.add_argument('--signature', required=True, type=Path)
    ap.add_argument('--gnupghome', type=Path, help='Explicit public verification key store, if required')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--expansion-r214', action='store_true', help='REPORT 4a3e8be9a797f116: exact approved 1.97 to 2.14 expansion only')
    ap.add_argument('--expansion-r269', action='store_true', help='REPORT 3436707b2335a963: exact 2.14 to 2.69 expansion only')
    ap.add_argument('--asset-objects', type=Path, help='Verified sealed object directory; 2.69 only')
    args = ap.parse_args()
    receipt = json.loads(args.receipt.read_text())
    if not receipt.get('authority') or not receipt.get('catalog_receipt'):
        raise ValueError('Record explicit authority and independently checked catalog receipt')
    command = ['gpg', '--batch', '--status-fd=1']
    if args.gnupghome: command += ['--homedir', str(args.gnupghome)]
    signature = subprocess.run(command + ['--verify', str(args.signature), str(args.snapshot)], capture_output=True, text=True)
    if signature.returncode or not any(line.startswith('[GNUPG:] VALIDSIG '+SIGNER+' ') for line in signature.stdout.splitlines()):
        raise ValueError('Signature verification failed for approved broker signer')
    raw = args.snapshot.read_bytes()
    assets={}
    if args.asset_objects:
        if not args.expansion_r269: raise ValueError('Asset import not authorized')
        assets={name:(args.asset_objects/digest).read_bytes() for name,(digest,size) in ASSETS_R269.items()}
    outputs, delta = prepare(raw, receipt, ROOT/'comparison', args.expansion_r214,args.expansion_r269,assets)
    if args.apply:
        # Repository staging only; publication is separately authorized and managed.
        for name, data in outputs.items():
            (ROOT/'comparison'/name).write_bytes(data)
        (ROOT/'scripts/comparison-approved.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(dict(result='PASS',applied=args.apply,revision=receipt['revision'],
        sha256=hashlib.sha256(raw).hexdigest(),changed_ids=delta,signature=SIGNER,
        note='Cryptographic verification; key identity follows broker custody, not external web-of-trust certification.')))


if __name__ == '__main__': main()
