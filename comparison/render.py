"""Rebuild approved JSON with website-owned presentation; standard library only."""
import argparse
import hashlib
from html import escape as esc
import json
from pathlib import Path
import re
import runpy
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
CSS=CSS.replace('.dark{', '.matrix .brand.dark{')
CSS+='body{padding:0}.comparison-layout{padding:24px}body .site-header{position:relative}.wrap:focus-visible{outline:3px solid #165e70;outline-offset:3px}@media(max-width:600px){body{padding:0}.comparison-layout{padding:12px}}'
CSS+='''.matrix .brand{height:44px;margin-bottom:4px}.matrix .brand img{max-height:38px;max-width:100%}.stack-heading{display:flex;align-items:center;gap:4px}.project-title{flex:1;min-width:0;overflow-wrap:anywhere}.stack-info{display:inline-flex;align-items:center;justify-content:center;flex:0 0 44px;width:44px;min-height:44px;text-decoration:none;font-size:22px}.stack-info span{display:grid;place-items:center;width:18px;height:18px;border:1.5px solid currentColor;border-radius:50%;font:bold 14px/1 system-ui}.stack-info:hover{background:#c9dad5;border-radius:6px}.matrix td a{display:flex;align-items:center;justify-content:center;min-height:44px}@media(max-width:600px){.matrix th,.matrix td{padding:6px;min-width:110px;width:110px}.matrix th:first-child{min-width:140px;width:140px;font-size:14px;line-height:1.35}.matrix thead th{font-size:14px;line-height:1.25}.matrix .brand{height:36px;min-height:44px;margin-bottom:0}.matrix .brand img{max-width:76px;max-height:30px}.matrix details{padding:4px;margin:6px 0}.matrix summary{min-height:32px;display:list-item;align-content:center}}'''

# The band spans the table; only its nested label follows horizontal scrolling.
# Container-relative sizing keeps even the longest label visible at 390px.
CSS+='''.wrap{container-type:inline-size}.matrix .group-band th{position:static;min-width:0;width:auto;padding:0;text-align:left;background:#cddcd7;z-index:auto}.group-label{display:block;position:sticky;left:0;box-sizing:border-box;width:max-content;max-width:calc(100cqw - 32px);padding:10px;overflow-wrap:anywhere}.archived{padding:16px;border:2px solid #856123;background:#fff0c9}@media print{.wrap{overflow:visible;max-height:none;container-type:normal}.matrix th:first-child,.matrix thead th,.group-label{position:static}.group-label{max-width:700px}.matrix thead{display:table-header-group}.matrix tr{break-inside:avoid}.site-header{display:none}}'''

CSS+='''.wake-scroll{overflow:auto}.wake-scroll:focus-visible{outline:3px solid #165e70}.wake-table{border-collapse:collapse;width:100%;min-width:640px}.wake-table th,.wake-table td{border:1px solid #bac8c1;padding:12px;text-align:left;vertical-align:top}.wake-table thead{background:#dce5e1}.content article{scroll-margin-top:20px}@media print{.wake-scroll{overflow:visible}}'''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    out=args.out;out.mkdir(parents=True,exist_ok=True)
    d=runpy.run_path(str(Path(__file__).with_name('validate.py')))['validate']((out/'data.json').read_bytes(),out)
    ids={c['id'] for c in d['cells']};assert len(ids)==len(d['columns'])*len(d['criteria'])
    assert all(c['status'] in LABEL for c in d['cells'])
    byid={c['id']:c for c in d['cells']};pending=sum(c['status']=='?' for c in d['cells'])
    groups=json.loads((out/'groups.json').read_text())
    assert set(groups)<={r['id'] for r in d['criteria']}, 'Group start missing'
    archives={}
    for ident,rev in [('C08','4.72'),('F25','5.73'),('F35','5.73')]:
        path=out/('archive/'+ident+'-'+rev+'.json')
        if path.exists():
            archives[ident]=json.loads(path.read_text())
            assert ident not in {r['id'] for r in d['criteria']}, 'Retired ID cannot be reused'
    def write(name,title,body):
        target=out/name;target.parent.mkdir(parents=True,exist_ok=True)
        depth=len(Path(name).parts)-1
        local='../'*depth
        navigation=(out/'navigation.html').read_text().replace('{{ROOT}}','../'*(depth+1))
        if name=='index.html':body='<main>'+body+'</main>'
        target.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><style>'+CSS+'</style><link rel="stylesheet" href="'+local+'navigation.css"></head><body>'+navigation+'<div class="comparison-layout">'+body+'</div></body></html>')
    intro='<h1>Protocol and stack comparison</h1><p>PRP editorial comparison · Revision '+esc(d['revision'])+' · Updated '+esc(d['date'])+'</p><p>'+str(len(d['criteria']))+' criteria × '+str(len(d['columns']))+' stacks; '+str(pending)+' Pending cells.</p><p><a href="https://prp-protocol.org/">PRP website</a> · <a href="methodology.html">Methodology and limits</a> · <a href="data.json">Download structured data</a> · <a href="logos.html">Logo credits</a></p><p class="legend"><span class="Y">Yes</span> <span class="N">No</span> <span class="U">Pending</span></p><p>Click a cell for evidence and qualifications. Expand a criterion for its definition. Results describe the selected stack and documented capabilities, not implementation certification. Pending means insufficient evidence, not unsupported.</p>'
    for ident,archive in archives.items(): intro+='<p><a href="archive/'+ident+'.html">'+ident+' — archived previous definition (revision '+esc(archive['revision'])+')</a></p>'
    if (out/'wake-traffic.json').exists(): intro+='<p><a href="wake-traffic.html">Communication recovery traffic — historical inventories</a></p>'
    body=intro+'<div class="wrap" tabindex="0" role="region" aria-label="Scrollable protocol comparison"><table class="matrix"><caption>Selected protocol stacks and capabilities</caption><thead><tr><th scope="col">Criterion</th>'
    for c in d['columns']:
        mark=('<img src="logos/'+esc(c['logo'])+'" alt="'+esc(c['title'])+' mark">') if c['logo'] else esc(c['title'])
        body+='<th scope="col" id="col-'+c['id']+'"><a class="brand'+(' dark' if c['id']=='TO' else '')+'" href="logos.html#'+c['id']+'">'+mark+'</a><div class="stack-heading"><a class="project-title" href="'+esc(c['website'])+'">'+esc(c['title'])+'</a><a class="stack-info" id="profile-'+c['id']+'" href="stacks/'+c['id']+'.html" aria-label="Selected stack: '+esc(c['title'])+'" title="Read selected stack: '+esc(c['title'])+'"><span aria-hidden="true">i</span></a></div></th>'
    body+='</tr></thead><tbody>'
    for r in d['criteria']:
        if r['id'] in groups:
            body+='</tbody><tbody><tr class="group-band"><th scope="rowgroup" colspan="'+str(len(d['columns'])+1)+'"><span class="group-label">'+esc(groups[r['id']])+'</span></th></tr>'
        body+='<tr><th scope="row" id="row-'+r['id']+'">'+r['id']+' · '+esc(r['title'])+'<details><summary>Definition</summary>'+esc(r['definition'])+'</details></th>'
        for col in d['columns']:
            c=byid[r['id']+'-'+col['id']];status=c['status'];body+='<td class="'+('U' if status=='?' else status)+'"><a href="cells/'+c['id']+'.html" aria-label="'+esc(c['id']+': '+LABEL[status])+'">'+LABEL[status]+'</a></td>'
        body+='</tr>'
    write('index.html','Protocol and stack comparison',body+'</tbody></table></div>')
    for c in d['columns']:
        body='<main class="content"><p><a href="../index.html#col-'+c['id']+'">Back to column</a></p><h1>'+esc(c['title'])+' — selected stack</h1><p>'+esc(c['profile'])+'</p><p><a href="'+esc(c['website'])+'">Official project website</a> · <a href="../logos.html#'+c['id']+'">Logo credits</a> · <a href="../methodology.html">Methodology and limits</a></p></main>'
        write('stacks/'+c['id']+'.html',c['title']+' — selected stack',body)
    for ident,archive in archives.items():
        r=archive['criterion']
        body='<main class="content"><p><a href="../index.html">Current matrix</a></p><h1>'+ident+' — archived previous definition</h1><p class="archived">Historical assessment from revision '+esc(archive['revision'])+', retired in '+esc(archive['retired_in'])+'. These 26 cells are excluded from the active grid and counts. '+ident+' is not reused or redirected to a new definition.</p>'
        if ident=='F25': body+='<p><a href="../wake-traffic.html">Historical wake-traffic inventories (cutoff retired)</a></p>'
        body+='<h2>'+esc(r['title'])+'</h2><p>'+esc(r['definition'])+'</p><h2>Assessment method</h2><p>'+esc(r['method'])+'</p><h2>Research action</h2><p>'+esc(r['research_action'])+'</p><p>Original approved data SHA-256: '+esc(archive['source_sha256'])+'</p><p><a href="'+ident+'-'+esc(archive['revision'])+'.json">Historical criterion and cell records</a></p><ul>'
        body+=''.join('<li><a href="../cells/'+c['id']+'.html">'+c['id']+'</a></li>' for c in archive['cells'])+'</ul></main>'
        write('archive/'+ident+'.html',ident+' — archived previous definition',body)
    for c in d['cells']+[c for archive in archives.values() for c in archive['cells']]:
        historical=c['feature'] in archives
        back='../archive/'+c['feature']+'.html' if historical else '../index.html#row-'+c['feature']
        body='<main class="content"><p><a href="'+back+'">'+('Archived criterion' if historical else 'Back to matrix')+'</a></p><h1>'+c['id']+': '+LABEL[c['status']]+'</h1>'
        if historical:
            archive=archives[c['feature']]
            body+='<p class="archived">Archived previous-definition assessment — revision '+esc(archive['revision'])+'. Retired in '+esc(archive['retired_in'])+'; excluded from the active matrix and counts. This historical verdict is not a current assessment.</p>'
            if c['feature']=='F25': body+='<p><a href="../wake-traffic.html#'+c['id']+'">Historical wake-traffic inventory (cutoff retired)</a></p>'
        for title,key in [('Rationale','reason'),('Assessment method','method'),('Source context','source_label'),('Outstanding qualification','qualification')]:
            if c[key]:body+='<h2>'+title+'</h2><p>'+esc(c[key])+'</p>'
        body+='<h2>Public sources</h2><ul>'+''.join('<li><a href="'+esc(u)+'">'+esc(u)+'</a></li>' for u in c['sources'])+'</ul>'
        if c['editorial_references']:body+='<h2>Editorial evidence references</h2><p>The following identifiers refer to research records not included in this public package; they are not public links.</p><ul>'+''.join('<li>'+esc(u)+'</li>' for u in c['editorial_references'])+'</ul>'
        write('cells/'+c['id']+'.html',c['id']+' — '+LABEL[c['status']],body+'</main>')
    write('methodology.html','Comparison methodology','<main class="content"><a href="index.html">Matrix</a><h1>Methodology</h1><p>This is an evolving comparison maintained by the PRP editorial project. Each column declares the complete selected stack; each criterion has an explicit scope. Yes means supported in that scope; No means not supported in that scope; Pending means the evidence is not established. Optional mechanisms may qualify where the criterion allows them. A documented capability does not certify an implementation, global scale, interoperability or measured performance.</p><p>Read each cell’s rationale, sources and outstanding qualification together. Some evidence references are internal research records and are identified as such. This package does not make those records public. Revision and date identify the current assessment; stable criterion and stack IDs preserve links across updates. Superseded revisions remain in the website Git history.</p><p>G05 assesses architectural plausibility within each selected complete stack under the same regional infrastructure, population, access workload and contemporary equipment envelope. Historical numerical targets remain sizing references, not jointly certified pass/fail thresholds or a global-scale benchmark. Read each cell’s evidence and qualifications; other positive cells do not imply G05 is satisfied.</p></main>')
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
    if (out/'wake-traffic.json').exists():
        body=runpy.run_path(str(Path(__file__).with_name('wake.py')))['render'](out)
        write('wake-traffic.html','Communication recovery traffic — historical inventories',body)
    files={str(f.relative_to(out)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(out.rglob('*')) if f.is_file() and f.name!='manifest.json'}
    (out/'manifest.json').write_text(json.dumps(dict(schema_version=1,revision=d['revision'],files=files),indent=2)+'\n')
    print(json.dumps(dict(revision=d['revision'],cells=len(ids),pending=pending,files=len(files))))

if __name__=='__main__':main()
