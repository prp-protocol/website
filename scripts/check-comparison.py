#!/usr/bin/env python3
"""Check static comparison content, safe links and reproducible standalone rendering."""
from collections import Counter
from html.parser import HTMLParser
from html import escape
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib,json,shutil,subprocess,tempfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'comparison'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.links=[];self.scripts=0;self.details=0;self.open_details=0;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids,a['id'];self.ids.add(a['id'])
        if tag=='script':self.scripts+=1
        if tag=='details':self.details+=1;self.open_details+=('open' in a)
        for key in ('href','src'):
            if key in a:self.links.append(a[key])

d=json.loads((OUT/'data.json').read_text())
expected={r['id']+'-'+c['id'] for r in d['criteria'] for c in d['columns']}
assert len(d['criteria'])==38 and len(d['columns'])==21
assert len(d['cells'])==798 and {c['id'] for c in d['cells']}==expected
assert all(c['status'] in ['Y','N','?'] for c in d['cells'])
assert sum(c['status']=='?' for c in d['cells'])==72
pages={p:Page(p.read_text()) for p in OUT.rglob('*.html') if p.name!='navigation.html'}
assert pages[OUT/'index.html'].details==38 and pages[OUT/'index.html'].open_details==0
for p,page in pages.items():
    assert not page.scripts,p
    for link in page.links:
        u=urlsplit(link)
        assert not any(x in link for x in ['/workspace/','/opt/agentmux/','201.130.81.10','/preview/','localhost']),link
        if u.scheme:
            assert u.scheme in ['https','http'],link
            continue
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        assert target.is_relative_to(ROOT),link
        if target.is_dir():target=target/'index.html'
        assert target.is_file(),(p,link)
        if u.fragment:
            other=pages.get(target) or Page(target.read_text())
            assert unquote(u.fragment) in other.ids,(p,link)
for c in d['cells']:
    p=OUT/'cells'/(c['id']+'.html');assert p in pages
    for url in c['sources']:assert url in pages[p].links,(p,url)
assert '<h2>Selected stacks</h2>' not in (OUT/'index.html').read_text()
assert (OUT/'index.html').read_text().count('class="stack-info"')==len(d['columns'])
for c in d['columns']:
    assert c['website'] in pages[OUT/'index.html'].links
    assert 'stacks/'+c['id']+'.html' in pages[OUT/'index.html'].links
    profile=OUT/'stacks'/(c['id']+'.html')
    assert profile in pages and escape(c['profile']) in profile.read_text()
    assert '../index.html#col-'+c['id'] in pages[profile].links
manifest=json.loads((OUT/'manifest.json').read_text())
assert set(manifest['files'])=={str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file() and p.name!='manifest.json'}
for name,digest in manifest['files'].items():assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==digest,name
with tempfile.TemporaryDirectory(prefix='prp-comparison-check-') as temp:
    dest=Path(temp)/'comparison';shutil.copytree(OUT,dest)
    for _ in range(2):
        subprocess.run(['python3','-I',str(dest/'render.py'),'--out',str(dest)],cwd=temp,check=True,capture_output=True)
        assert (dest/'manifest.json').read_bytes()==(OUT/'manifest.json').read_bytes()
print(json.dumps(dict(result='PASS',revision=d['revision'],cells=len(expected),statuses=dict(Counter(c['status'] for c in d['cells'])),pages=len(pages),standalone_rebuilds=2)))
