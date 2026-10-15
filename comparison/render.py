"""Export or rebuild the public comparison, using Python's standard library only.

Export: python3 tools/public_comparison.py --source pesquisa/prp-estado-da-arte-v1 --out DIR
Rebuild an exported package: python3 render.py --out DIR
"""
import argparse
import hashlib
from html import escape as esc
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import urlsplit

def public_url(s):
    u=urlsplit(s)
    return u.scheme in ('https','http') and bool(u.hostname) and u.hostname not in ('201.130.81.10','localhost','127.0.0.1')

def clean(s):
    s=re.sub(r'/(?:workspace|opt/agentmux|tmp|home)/[^\s<>"\']+', '[internal evidence path]', s)
    return s

CSS='''body{font:16px/1.5 system-ui;color:#172d36;background:#f4f2eb;margin:0;padding:24px}a{color:#165e70}a:focus-visible,summary:focus-visible{outline:3px solid #165e70}p,li{overflow-wrap:anywhere}.wrap{overflow:auto;max-height:78vh}.matrix{border-spacing:3px;table-layout:fixed}.matrix th,.matrix td{padding:10px;text-align:center;min-width:125px;width:125px}.matrix thead th{position:sticky;top:0;background:#dce5e1;z-index:2;vertical-align:top}.matrix th:first-child{position:sticky;left:0;min-width:270px;width:270px;background:#e9eee9;text-align:left;z-index:1}.matrix thead th:first-child{z-index:3}.Y{background:#b9e5c5}.N{background:#f1bcbc}.U{background:#ffe39c}.matrix td a{display:block;color:#172d36;text-decoration:none}.brand{display:flex;height:64px;align-items:center;justify-content:center;background:white;border-radius:6px;margin-bottom:8px}.brand img{max-width:108px;max-height:58px;object-fit:contain}.dark{background:#59316b}details{padding:8px;background:#e6ebe4;margin:8px 0}summary{cursor:pointer}.content{max-width:1000px;margin:auto}article{margin:24px 0}small{font-size:12px}.legend span{display:inline-block;padding:6px 14px}@media(max-width:600px){body{padding:12px}.matrix th:first-child{min-width:180px;width:180px}}'''
LABEL={'Y':'Yes','N':'No','?':'Pending'}

# Website wrapper: local presentation files travel with every coherent snapshot.
# Scope project-mark styling so it cannot affect the shared site brand.
CSS=CSS.replace('.brand', '.matrix .brand')
CSS+='body{padding:0}.comparison-layout{padding:24px}body .site-header{position:relative}.wrap:focus-visible{outline:3px solid #165e70;outline-offset:3px}@media(max-width:600px){body{padding:0}.comparison-layout{padding:12px}}'
CSS+='''.matrix .brand{height:44px;margin-bottom:4px}.matrix .brand img{max-height:38px;max-width:100%}.stack-heading{display:flex;align-items:center;gap:4px}.project-title{flex:1;min-width:0;overflow-wrap:anywhere}.stack-info{display:inline-flex;align-items:center;justify-content:center;flex:0 0 44px;width:44px;min-height:44px;text-decoration:none;font-size:22px}.stack-info span{display:grid;place-items:center;width:18px;height:18px;border:1.5px solid currentColor;border-radius:50%;font:bold 14px/1 system-ui}.stack-info:hover{background:#c9dad5;border-radius:6px}.matrix td a{display:flex;align-items:center;justify-content:center;min-height:44px}@media(max-width:600px){.matrix th,.matrix td{padding:6px;min-width:110px;width:110px}.matrix th:first-child{min-width:140px;width:140px;font-size:14px;line-height:1.35}.matrix thead th{font-size:14px;line-height:1.25}.matrix .brand{height:36px;min-height:44px;margin-bottom:0}.matrix .brand img{max-width:76px;max-height:30px}.matrix details{padding:4px;margin:6px 0}.matrix summary{min-height:32px;display:list-item;align-content:center}}'''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    out=args.out;out.mkdir(parents=True,exist_ok=True)
    if args.source:
        src=args.source.resolve();sys.path.insert(0,str(src))
        from branding import LOGOS,PROJECT_SITES
        m=json.loads((src/'matrix.json').read_text())
        marks=dict(LOGOS,AX='ax25-netrom.svg',CG='cgr-sabr.svg',LT='ltp.svg')
        provenance=json.loads((src/'logos/provenance.json').read_text())
        d=dict(schema_version=1,revision=m['revision'],date=m['date'],language='en',scope=m['scope'],columns=[],criteria=[],cells=[])
        for ident,title,profile,_ in m['columns']:
            d['columns'].append(dict(id=ident,title=title,profile=clean(profile),website=PROJECT_SITES[ident],logo=marks.get(ident)))
        for fid,title,_,definition,method,action in m['rows']:
            d['criteria'].append(dict(id=fid,title=title,definition=clean(definition),method=method,research_action=clean(action)))
        for cell in m['cells']:
            cid=cell['feature']+'-'+cell['stack'];r=m['resolutions'][cid]
            sources=[r.get('url','')]+r.get('additional_sources',[])
            d['cells'].append(dict(id=cid,feature=cell['feature'],stack=cell['stack'],status=cell['status'],reason=clean(r.get('reason','')),method=clean(r.get('method','')),source_label=clean(r.get('source','')),sources=[u for u in sources if isinstance(u,str) and public_url(u)],editorial_references=[clean(u) for u in sources if isinstance(u,str) and u and not public_url(u)],qualification=clean(r.get('qualification_pending',''))))
        d['marks']=provenance
        (out/'data.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
        (out/'logos').mkdir(exist_ok=True)
        for name in set(marks.values()):shutil.copyfile(src/'logos'/name,out/'logos'/name)
        shutil.copyfile(__file__,out/'render.py')
    else:d=json.loads((out/'data.json').read_text())
    ids={c['id'] for c in d['cells']};assert len(ids)==len(d['columns'])*len(d['criteria'])
    assert all(c['status'] in LABEL for c in d['cells'])
    byid={c['id']:c for c in d['cells']};pending=sum(c['status']=='?' for c in d['cells'])
    def write(name,title,body):
        target=out/name;target.parent.mkdir(parents=True,exist_ok=True)
        depth=len(Path(name).parts)-1
        local='../'*depth
        navigation=(out/'navigation.html').read_text().replace('{{ROOT}}','../'*(depth+1))
        if name=='index.html':body='<main>'+body+'</main>'
        target.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><style>'+CSS+'</style><link rel="stylesheet" href="'+local+'navigation.css"></head><body>'+navigation+'<div class="comparison-layout">'+body+'</div></body></html>')
    intro='<h1>Protocol and stack comparison</h1><p>PRP editorial comparison · Revision '+esc(d['revision'])+' · Updated '+esc(d['date'])+'</p><p>'+str(len(d['criteria']))+' criteria × '+str(len(d['columns']))+' stacks; '+str(pending)+' Pending cells.</p><p><a href="https://prp-protocol.org/">PRP website</a> · <a href="methodology.html">Methodology and limits</a> · <a href="data.json">Download structured data</a> · <a href="logos.html">Logo credits</a></p><p class="legend"><span class="Y">Yes</span> <span class="N">No</span> <span class="U">Pending</span></p><p>Click a cell for evidence and qualifications. Expand a criterion for its definition. Results describe the selected stack and documented capabilities, not implementation certification. Pending means insufficient evidence, not unsupported.</p>'
    body=intro+'<div class="wrap" tabindex="0" role="region" aria-label="Scrollable protocol comparison"><table class="matrix"><caption>Selected protocol stacks and capabilities</caption><thead><tr><th scope="col">Criterion</th>'
    for c in d['columns']:
        mark=('<img src="logos/'+esc(c['logo'])+'" alt="'+esc(c['title'])+' mark">') if c['logo'] else esc(c['title'])
        body+='<th scope="col" id="col-'+c['id']+'"><a class="brand'+(' dark' if c['id']=='TO' else '')+'" href="logos.html#'+c['id']+'">'+mark+'</a><div class="stack-heading"><a class="project-title" href="'+esc(c['website'])+'">'+esc(c['title'])+'</a><a class="stack-info" id="profile-'+c['id']+'" href="stacks/'+c['id']+'.html" aria-label="Selected stack: '+esc(c['title'])+'" title="Read selected stack: '+esc(c['title'])+'"><span aria-hidden="true">i</span></a></div></th>'
    body+='</tr></thead><tbody>'
    for r in d['criteria']:
        body+='<tr><th scope="row" id="row-'+r['id']+'">'+r['id']+' · '+esc(r['title'])+'<details><summary>Definition</summary>'+esc(r['definition'])+'</details></th>'
        for col in d['columns']:
            c=byid[r['id']+'-'+col['id']];status=c['status'];body+='<td class="'+('U' if status=='?' else status)+'"><a href="cells/'+c['id']+'.html" aria-label="'+esc(c['id']+': '+LABEL[status])+'">'+LABEL[status]+'</a></td>'
        body+='</tr>'
    write('index.html','Protocol and stack comparison',body+'</tbody></table></div>')
    for c in d['columns']:
        body='<main class="content"><p><a href="../index.html#col-'+c['id']+'">Back to column</a></p><h1>'+esc(c['title'])+' — selected stack</h1><p>'+esc(c['profile'])+'</p><p><a href="'+esc(c['website'])+'">Official project website</a> · <a href="../logos.html#'+c['id']+'">Logo credits</a> · <a href="../methodology.html">Methodology and limits</a></p></main>'
        write('stacks/'+c['id']+'.html',c['title']+' — selected stack',body)
    for c in d['cells']:
        body='<main class="content"><p><a href="../index.html#row-'+c['feature']+'">Back to matrix</a></p><h1>'+c['id']+': '+LABEL[c['status']]+'</h1>'
        for title,key in [('Rationale','reason'),('Assessment method','method'),('Source context','source_label'),('Outstanding qualification','qualification')]:
            if c[key]:body+='<h2>'+title+'</h2><p>'+esc(c[key])+'</p>'
        body+='<h2>Public sources</h2><ul>'+''.join('<li><a href="'+esc(u)+'">'+esc(u)+'</a></li>' for u in c['sources'])+'</ul>'
        if c['editorial_references']:body+='<h2>Editorial evidence references</h2><p>The following identifiers refer to research records not included in this public package; they are not public links.</p><ul>'+''.join('<li>'+esc(u)+'</li>' for u in c['editorial_references'])+'</ul>'
        write('cells/'+c['id']+'.html',c['id']+' — '+LABEL[c['status']],body+'</main>')
    write('methodology.html','Comparison methodology','<main class="content"><a href="index.html">Matrix</a><h1>Methodology</h1><p>This is an evolving comparison maintained by the PRP editorial project. Each column declares the complete selected stack; each criterion has an explicit scope. Yes means supported in that scope; No means not supported in that scope; Pending means the evidence is not established. Optional mechanisms may qualify where the criterion allows them. A documented capability does not certify an implementation, global scale, interoperability or measured performance.</p><p>Read each cell’s rationale, sources and outstanding qualification together. Some evidence references are internal research records and are identified as such. This package does not make those records public. Revision and date identify the current assessment; stable criterion and stack IDs preserve links across updates. Superseded revisions remain in the website Git history.</p><p>Global scale is assessed against the explicit G05 definition, including contemporary equipment, regional deployment, discovery deadlines, daily destination demand and per-equipment memory. Other positive cells do not imply G05 is satisfied.</p></main>')
    body='<main class="content"><a href="index.html">Matrix</a><h1>Marks and credits</h1><p>Marks identify the compared projects and imply no endorsement. IP, AX.25/NET/ROM, CGR/SABR and LTP use neutral editorial labels.</p>'
    for col in d['columns']:
        body+='<article id="'+col['id']+'"><h2>'+esc(col['title'])+'</h2>'
        for p in d['marks']:
            if col['logo'] and p['file']=='logos/'+col['logo']:
                body+='<p>'+esc(p.get('rights',''))+'</p>'
                for key in ('source','license_url'):
                    if p.get(key) and public_url(p[key]):body+='<p><a href="'+esc(p[key])+'">'+key+'</a></p>'
        body+='</article>'
    write('logos.html','Marks and credits',body+'</main>')
    files={str(f.relative_to(out)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(out.rglob('*')) if f.is_file() and f.name!='manifest.json'}
    (out/'manifest.json').write_text(json.dumps(dict(schema_version=1,revision=d['revision'],files=files),indent=2)+'\n')
    print(json.dumps(dict(revision=d['revision'],cells=len(ids),pending=pending,files=len(files))))

if __name__=='__main__':main()
