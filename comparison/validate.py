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


def changes(old, new):
    result = {}
    for kind in ('criteria', 'columns', 'cells'):
        before = {x['id']: x for x in old[kind]}
        after = {x['id']: x for x in new[kind]}
        require(before.keys() == after.keys(), 'ID-set change requires separate coordination: ' + kind)
        result[kind] = sorted(k for k in before if before[k] != after[k])
    return result


def check_receipt(raw, root, receipt, old):
    require(len(raw) == receipt['bytes'], 'Snapshot size mismatch')
    require(hashlib.sha256(raw).hexdigest() == receipt['sha256'], 'Snapshot hash mismatch')
    new = validate(raw, root)
    require(new['revision'] == receipt['revision'] and new['date'] == receipt['date'], 'Revision/date mismatch')
    require(dict(Counter(c['status'] for c in new['cells'])) == receipt['status_counts'], 'Status counts mismatch')
    delta = changes(old, new)
    require(delta == {k: sorted(v) for k, v in receipt['changed_ids'].items()}, 'Changed-ID receipt mismatch')
    return new, delta
