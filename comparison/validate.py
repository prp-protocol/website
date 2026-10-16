"""Website-owned schema-v1 validation; standard library, no editorial imports."""
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
import datetime
import hashlib
import json
import re


def require(ok, message):
    if not ok:
        raise ValueError(message)


def public_url(value):
    u = urlsplit(value)
    return (u.scheme in ('http', 'https') and bool(u.hostname)
            and u.hostname not in ('localhost', '127.0.0.1', '201.130.81.10')
            and not u.username and not u.password)


def validate(raw, root):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result
    d = json.loads(raw, object_pairs_hook=unique)
    require(isinstance(d, dict) and set(d) == {'schema_version', 'revision', 'date',
        'language', 'scope', 'criteria', 'columns', 'cells', 'marks'}, 'Unsupported schema fields')
    require(d['schema_version'] == 1, 'Unsupported schema; coordinate separately')
    require(d['language'] == 'en', 'Unsupported primary language')
    require(isinstance(d['revision'], str) and d['revision'], 'Missing revision')
    datetime.date.fromisoformat(d['date'])
    def walk(value):
        if isinstance(value, str):
            require(not any(s in value for s in ('/workspace/', '/opt/agentmux/',
                        '/home/', '/tmp/', '201.130.81.10', '/preview/')), 'Private path in data')
        elif isinstance(value, list):
            for x in value: walk(x)
        elif isinstance(value, dict):
            for x in value.values(): walk(x)
    walk(d)
    def records(key, fields, pattern):
        rows = d[key]
        require(isinstance(rows, list) and rows, 'Empty ' + key)
        result = {}
        for row in rows:
            ident = row['id']
            require(isinstance(ident, str) and re.fullmatch(pattern, ident), 'Unsafe ID')
            require(ident not in result, 'Duplicate ID: ' + ident)
            for field in fields:
                require(isinstance(row[field], str), 'Expected string: ' + field)
            result[ident] = row
        return result
    criteria = records('criteria', ('title', 'definition', 'method', 'research_action'), r'[A-Z][0-9]+')
    columns = records('columns', ('title', 'profile', 'website'), r'[A-Z][A-Z0-9]*')
    cells = records('cells', ('feature', 'stack', 'status', 'reason', 'method',
                    'source_label', 'qualification'), r'[A-Z][0-9]+-[A-Z][A-Z0-9]*')
    require(set(cells) == {r+'-'+c for r in criteria for c in columns}, 'Incomplete grid')
    def asset(name):
        p = Path(name)
        require(not p.is_absolute() and '..' not in p.parts and p.parts[0] == 'logos', 'Unsafe asset')
        target = root / p
        require(target.resolve().is_relative_to(root.resolve()) and target.is_file(), 'Unknown asset: ' + name)
        return target.read_bytes()
    for col in columns.values():
        require(public_url(col['website']), 'Invalid official link')
        if col['logo'] is not None:
            require(Path(col['logo']).name == col['logo'], 'Invalid logo reference')
            asset('logos/' + col['logo'])
    for cell in cells.values():
        require(cell['id'] == cell['feature']+'-'+cell['stack'], 'Cell ID mismatch')
        require(cell['status'] in ('Y', 'N', '?'), 'Invalid status')
        require(isinstance(cell['sources'], list) and all(isinstance(u, str) and public_url(u) for u in cell['sources']), 'Invalid source URL')
        require(isinstance(cell['editorial_references'], list) and all(isinstance(u, str) for u in cell['editorial_references']), 'Invalid unpublished references')
    require(isinstance(d['marks'], list), 'Invalid mark metadata')
    for mark in d['marks']:
        data = asset(mark['file'])
        if mark.get('sha256'):
            require(hashlib.sha256(data).hexdigest() == mark['sha256'], 'Asset hash mismatch')
        if mark.get('bytes') is not None:
            require(len(data) == mark['bytes'], 'Asset size mismatch')
        for field in ('source', 'license_url'):
            if mark.get(field):
                require(isinstance(mark[field], str), 'Invalid credit metadata')
                # Legacy source identifiers are metadata, never emitted as links.
                if field == 'license_url' or urlsplit(mark[field]).scheme:
                    require(public_url(mark[field]), 'Invalid credit link')
    return d


def changes(old, new, allowed_added=None):
    result = {}
    for kind in ('criteria', 'columns', 'cells'):
        before = {x['id']: x for x in old[kind]}
        after = {x['id']: x for x in new[kind]}
        allowed = set((allowed_added or {}).get(kind, []))
        require(set(after)-set(before) == allowed and not set(before)-set(after),
                'ID-set change requires separate coordination: ' + kind)
        result[kind] = sorted(k for k in after if k not in before or before[k] != after[k])
    return result


def check_receipt(raw, root, receipt, old, expansion_r214=False, expansion_r269=False, asset_r321=False):
    require(len(raw) == receipt['bytes'], 'Snapshot size mismatch')
    require(hashlib.sha256(raw).hexdigest() == receipt['sha256'], 'Snapshot hash mismatch')
    new = validate(raw, root)
    require(new['revision'] == receipt['revision'] and new['date'] == receipt['date'], 'Revision/date mismatch')
    require(dict(Counter(c['status'] for c in new['cells'])) == receipt['status_counts'], 'Status counts mismatch')
    added = None
    require(sum((expansion_r214,expansion_r269,asset_r321))<=1, 'Select one coordinated exception')
    if asset_r321:
        require(receipt['sha256']=='85664e3ae45150b5601f5d295d653bbd31bf3f623eaa406557617aaa11d0ad62', 'Asset exception only authorized for exact 3.21 snapshot')
        require(hashlib.sha256((root/'data.json').read_bytes()).hexdigest()=='67d189343b908c17b055952f9d7a13d15e71e19fbee4ef521c0aade520373e51', 'Asset exception baseline must be exact 2.69')
        require(receipt['added_ids']==receipt['removed_ids']==dict(criteria=[],columns=[],cells=[]), 'ID changes not authorized')
        previous={m['file']:m for m in old['marks'] if m['file']!='logos/ccnx.svg'}
        current={m['file']:m for m in new['marks'] if m['file']!='logos/ccnx.jpg'}
        require(previous==current, 'Unrelated credit changes not authorized')
        require([m for m in new['marks'] if m['file']=='logos/ccnx.jpg']==receipt['new_assets'], 'CCNx attribution mismatch')
        require({c['id']:c['logo'] for c in new['columns']}=={c['id']:('ccnx.jpg' if c['id']=='CX' else c['logo']) for c in old['columns']}, 'Unrelated logo changes not authorized')
    if expansion_r269:
        require(receipt['sha256']=='67d189343b908c17b055952f9d7a13d15e71e19fbee4ef521c0aade520373e51', 'Expansion only authorized for exact 2.69 snapshot')
        require(hashlib.sha256((root/'data.json').read_bytes()).hexdigest()=='7c5876e4b797d4094dd9198facca00047e5d36f0bd37976d413679e70c164835', 'Expansion baseline must be exact 2.14')
        old_rows={r['id'] for r in old['criteria']};old_cols={c['id'] for c in old['columns']}
        rows={'F24','F25','S04','D04'};cols={'RI','HP','CX'}
        added=dict(criteria=sorted(rows),columns=sorted(cols),cells=sorted({r+'-'+c for r in old_rows|rows for c in old_cols|cols}-{r+'-'+c for r in old_rows for c in old_cols}))
        require({k:sorted(v) for k,v in receipt['added_ids'].items()}==added, 'Expansion additions mismatch')
        require(receipt['removed_ids']==dict(criteria=[],columns=[],cells=[]), 'Retirement not authorized')
        previous={m['file']:m for m in old['marks']};current={m['file']:m for m in new['marks']}
        require(all(current.get(k)==v for k,v in previous.items()), 'Existing credit changes not authorized')
        require({k:v for k,v in current.items() if k not in previous}=={m['file']:m for m in receipt['new_assets']}, 'New asset metadata mismatch')
        require({c['id']:c['logo'] for c in new['columns'] if c['id'] in old_cols}=={c['id']:c['logo'] for c in old['columns']}, 'Existing logo changes not authorized')
    if expansion_r214:
        require(receipt['sha256']=='7c5876e4b797d4094dd9198facca00047e5d36f0bd37976d413679e70c164835', 'Expansion only authorized for exact 2.14 snapshot')
        require(hashlib.sha256((root/'data.json').read_bytes()).hexdigest()=='0a53746ef35fb705de23a2e5acde20c3ecbfeb37baf565e15408b9febaa6436a', 'Expansion baseline must be exact 1.97')
        criteria = 'D01 D02 D03 E01 E02 E03 E04 E05 K01 L01 L02'.split()
        added = dict(criteria=criteria, columns=[], cells=sorted(r+'-'+c['id'] for r in criteria for c in old['columns']))
        require({k:sorted(v) for k,v in receipt['added_ids'].items()} == added, 'Expansion additions mismatch')
        require(receipt['removed_ids']==dict(criteria=[],columns=[],cells=[]), 'Retirement not authorized')
        require(new['marks']==old['marks'] and [(c['id'],c['logo']) for c in new['columns']]==[(c['id'],c['logo']) for c in old['columns']], 'Asset/credit changes not authorized')
    delta = changes(old, new, added)
    require(delta == {k: sorted(v) for k, v in receipt['changed_ids'].items()}, 'Changed-ID receipt mismatch')
    return new, delta
