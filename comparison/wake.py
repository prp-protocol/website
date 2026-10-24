"""Website-owned static rendering of the approved historical inventory JSON."""
import json
import re
from html import escape as esc
from urllib.parse import urlsplit

def render(root):
    d=json.loads((root/'wake-traffic.json').read_text())
    assert set(d)=={'title','revision','method','publication_note','records'}
    records=d['records'];assert len(records)==26
    assert len({r['id'] for r in records})==26
    assert sum(r['total'] is not None for r in records)==19
    assert {r['id'] for r in records}=={c['id'] for c in json.loads((root/'archive/F25-5.73.json').read_text())['cells']}
    for r in records:
        assert set(r)=={'id','stack','total','unit','evidence_kind','inventory','conditions','sources','source_revision','historical_cell','editorial_references'}
        assert re.fullmatch(r'F25-[A-Z0-9]+',r['id'])
        assert r['historical_cell']=='cells/'+r['id']+'.html'
        assert (root/r['historical_cell']).is_file()
        for ref in r['editorial_references']:
            assert set(ref)=={'label','public_evidence'} and ref['public_evidence']==r['historical_cell']
        for u in r['sources']:
            p=urlsplit(u);assert p.scheme in ('https','http') and p.hostname and not p.username and p.hostname not in ('localhost','127.0.0.1','201.130.81.10')
    # No sort or score: retain editorial order and dissimilar accounting scopes.
    body='<main class="content"><p><a href="index.html">Current comparison</a> · <a href="archive/F25.html">Archived F25 definition</a> · <a href="wake-traffic.json" download>Download inventory JSON</a></p><h1>'+esc(d['title'])+'</h1><p>Auxiliary source revision '+esc(d['revision'])+' · 26 historical inventories · 19 conditional totals · 7 incomplete accounts</p><p>'+esc(d['method'])+'</p><p class="archived">'+esc(d['publication_note'])+'</p>'
    body+='<div class="wake-scroll" tabindex="0" role="region" aria-label="Historical traffic inventory summary"><table class="wake-table"><caption>Historical inventories — unlike scopes, not a ranking</caption><thead><tr><th scope="col">Selected stack</th><th scope="col">Conditional total / unit</th><th scope="col">Evidence kind</th><th scope="col">Source revision</th></tr></thead><tbody>'
    for r in records:
        total=esc(str(r['total']))+' '+esc(r['unit'] or '') if r['total'] is not None else 'No total established'
        body+='<tr><th scope="row"><a href="#'+r['id']+'">'+esc(r['stack'])+'</a></th><td>'+total+'</td><td>'+esc(r['evidence_kind'])+'</td><td>'+esc(r['source_revision'])+'</td></tr>'
    body+='</tbody></table></div>'
    for r in records:
        body+='<article id="'+r['id']+'"><h2>'+esc(r['stack'])+' — '+r['id']+'</h2><p><a href="'+r['historical_cell']+'">Archived cell evidence</a> · Source revision '+esc(r['source_revision'])+'</p><h3>Inventory</h3><p>'+esc(r['inventory'])+'</p><h3>Conditions and security scope</h3><p>'+esc(r['conditions'])+'</p><h3>Public sources</h3><ul>'+''.join('<li><a href="'+esc(u)+'">'+esc(u)+'</a></li>' for u in r['sources'])+'</ul>'
        body+='<h3>Historical research labels</h3><p>Labels below link to public archived cell evidence, not to private research files.</p><ul>'+''.join('<li><a href="'+esc(ref['public_evidence'])+'">'+esc(ref['label'])+'</a></li>' for ref in r['editorial_references'])+'</ul></article>'
    return body+'</main>'
