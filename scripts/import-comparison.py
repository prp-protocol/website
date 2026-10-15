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


def prepare(snapshot, receipt, destination):
    api = runpy.run_path(str(destination/'validate.py'))
    old = api['validate']((destination/'data.json').read_bytes(), destination)
    data, delta = api['check_receipt'](snapshot, destination, receipt, old)
    with tempfile.TemporaryDirectory(prefix='comparison-import-') as tmp:
        stage = Path(tmp)/'comparison'
        shutil.copytree(destination, stage)
        (stage/'data.json').write_bytes(snapshot)
        subprocess.run(['python3', '-I', str(stage/'render.py'), '--out', str(stage)], check=True, capture_output=True)
        first = (stage/'manifest.json').read_bytes()
        subprocess.run(['python3', '-I', str(stage/'render.py'), '--out', str(stage)], check=True, capture_output=True)
        if (stage/'manifest.json').read_bytes() != first:
            raise ValueError('Non-reproducible build')
        # Only approved JSON, generated HTML and manifest can leave staging.
        outputs = {'data.json', 'manifest.json', 'index.html', 'methodology.html', 'logos.html'}
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
    outputs, delta = prepare(raw, receipt, ROOT/'comparison')
    if args.apply:
        # Repository staging only; publication is separately authorized and managed.
        for name, data in outputs.items():
            (ROOT/'comparison'/name).write_bytes(data)
        (ROOT/'scripts/comparison-approved.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(dict(result='PASS',applied=args.apply,revision=receipt['revision'],
        sha256=hashlib.sha256(raw).hexdigest(),changed_ids=delta,signature=SIGNER,
        note='Cryptographic verification; key identity follows broker custody, not external web-of-trust certification.')))


if __name__ == '__main__': main()
