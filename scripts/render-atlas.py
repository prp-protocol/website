#!/usr/bin/env python3
"""Website wrapper for exact approved Atlas files; no editorial code imports."""
from pathlib import Path
from html import escape as esc
import hashlib,json,sys

ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'protocol-atlas'
meta=json.loads((out/'poster-content.json').read_text())
assert meta['version']==2 and meta['language']=='en'
for name,record in meta['files'].items():
    assert name in ('poster.svg','poster.png','poster.pdf')
    raw=(out/name).read_bytes()
    assert len(raw)==record['bytes'] and hashlib.sha256(raw).hexdigest()==record['sha256']
nav=(ROOT/'comparison/navigation.html').read_text().replace('{{ROOT}}','../')
nav=nav.replace('href="../protocol-atlas/"','href="../protocol-atlas/" aria-current="page"')
style='''body{margin:0;background:#f4f2eb;color:#172d36;font:16px/1.6 system-ui}main{max-width:1100px;margin:auto;padding:24px}h1{font-size:clamp(2rem,6vw,3.6rem);line-height:1.1}a{color:#165e70}a:focus-visible{outline:3px solid #a85236;outline-offset:4px}.skip{position:absolute;left:16px;top:-100px;background:white;z-index:20;padding:8px}.skip:focus{top:8px}.downloads{display:flex;flex-wrap:wrap;gap:12px;padding:0;list-style:none}.downloads a,.full-size{display:inline-block;padding:12px;border:1px solid #165e70;border-radius:6px}figure{margin:24px 0}.poster{display:block;width:100%;height:auto;border-radius:8px}.note{padding:16px;background:#e2eae5;border-left:4px solid #165e70}figcaption{margin-top:12px}p{overflow-wrap:anywhere}@media(max-width:600px){main{padding:16px}}@media print{.site-header,.downloads,.skip,.full-size{display:none}main{padding:0}.poster{max-height:90vh;width:auto;max-width:100%;margin:auto}}'''
body='<a class="skip" href="#atlas">Skip to Protocol Atlas</a>'+nav+'<main id="atlas"><p>Technical reference · English poster · Version 2</p><h1>'+esc(meta['title'])+'</h1><p>'+esc(meta['description'])+'</p><p class="note">'+esc(meta['technical_note'])+'</p><p><a class="full-size" href="poster.svg">Open full-size scalable poster</a></p><ul class="downloads">'
for name in ('poster.pdf','poster.png','poster.svg'):
    body+='<li><a href="'+name+'" download>Download '+name.split('.')[-1].upper()+' ('+format(meta['files'][name]['bytes'],',')+' bytes)</a></li>'
body+='</ul><p>'+esc(meta['format_note'])+'</p><figure><a href="poster.png" aria-label="Open full-size PNG of the PRP Protocol Atlas"><img class="poster" src="poster.png" width="2100" height="3500" alt="'+esc(meta['alt'])+'"></a><figcaption>'+esc(meta['credits'])+'</figcaption></figure><p><a href="poster-content.json">Poster description and file hashes (JSON)</a> · <a href="../comparison/">Protocol comparison</a></p></main>'
html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(meta['title'])+'</title><link rel="stylesheet" href="../site-navigation.css"><style>'+style+'</style></head><body>'+body+'</body></html>\n'
pages={'legacy-v2.html':html}
revision='2026-10-26-rcp-v2'
collection=json.loads((out/revision/'atlas.json').read_text())
assert collection['revision']==revision and collection['language']=='en'
assert [p['id'] for p in collection['posters']]==['navigation','connection','relation-control','distribution','cryptography','suites']
for poster in collection['posters']:
    for record in poster['files']:
        assert record['path']==poster['id']+'.'+record['path'].split('.')[-1]
        assert record['path'].split('.')[-1] in ('pdf','png','svg')
        raw=(out/revision/record['path']).read_bytes()
        assert len(raw)==record['bytes'] and hashlib.sha256(raw).hexdigest()==record['sha256']
style+=''' .gallery{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}.tile{padding:20px;background:white;border:1px solid #bdccd1;border-radius:10px;min-width:0}.tile h2{font-size:1.5rem;margin:0 0 8px}.tile img{display:block;width:100%;height:auto}.tile figure{margin:16px 0}.tile .downloads{gap:8px;font-size:.9rem}.tile .downloads a{padding:8px}.section-nav{display:flex;flex-wrap:wrap;gap:10px 20px;padding:0;list-style:none}.poster-frame{background:white;border:1px solid #bdccd1;padding:8px}.poster-frame img{width:100%;height:auto;display:block}.poster-page{max-width:1400px}.history{margin-top:40px;border-top:1px solid #bdccd1;padding-top:20px}h2{line-height:1.25}section[id]{scroll-margin-top:24px}@media(max-width:650px){.gallery{grid-template-columns:1fr}.tile{padding:16px}}@media print{.gallery{display:block}.tile{break-inside:avoid}.section-nav{display:none}}'''
def shell(title,content,poster_page=False):
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+' — PRP Protocol Atlas</title><link rel="stylesheet" href="../site-navigation.css"><style>'+style+'</style></head><body><a class="skip" href="#atlas">Skip to atlas content</a>'+nav+'<main id="atlas"'+(' class="poster-page"' if poster_page else '')+'>'+content+'</main></body></html>\n'
def downloads(p):
    return '<ul class="downloads" aria-label="'+esc(p['title'])+' downloads">'+''.join('<li><a download href="'+revision+'/'+f['path']+'">'+f['path'].split('.')[-1].upper()+' · '+format(f['bytes'],',')+' bytes<span class="sr-only"> — '+esc(p['title'])+'</span></a></li>' for f in p['files'])+'</ul>'
# Full-size original SVG/PNG links complement each responsive preview. No image
# conversion or editorial source/renderer is needed for these website wrappers.
style+=' .sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}'
credit='PRP Editorial · Code-generated vector illustrations.'
intro='<p>Technical reference · English · '+esc(revision)+'</p><h1>PRP Protocol Atlas</h1><p>Five illustrated atlases and a cryptographic suite reference. Choose a plate to inspect its larger preview or download the original files.</p><p class="note">'+esc(collection['scope'])+' These diagrams do not constitute implementation or security certification.</p><p>White backgrounds and outline artwork are intentional for printed boards. Each vector PDF is one page, nominally 360 × 480 mm. SVGs are scalable; PNGs are 1800 × 2400 pixels.</p>'
intro+='<nav aria-label="Atlas sections"><ul class="section-nav">'+''.join('<li><a href="#'+p['id']+'">'+esc(p['title'])+'</a></li>' for p in collection['posters'])+'<li><a href="#historical">Historical atlas</a></li></ul></nav><div class="gallery">'
for p in collection['posters']:
    ident=p['id'];title=esc(p['title']);description=esc(p['description']);alt=esc(p['title']+'. '+p['description'])
    intro+='<section class="tile" id="'+ident+'"><h2><a href="'+ident+'.html">'+title+'</a></h2><p>'+description+'</p><figure><a href="'+ident+'.html" aria-label="View '+title+' poster"><img src="'+revision+'/'+ident+'.png" width="1800" height="2400" loading="lazy" alt="'+alt+'"></a><figcaption><a href="'+ident+'.html">View larger preview and full-size files</a></figcaption></figure>'+downloads(p)+'</section>'
    content='<p><a href="./#'+ident+'">← All atlases</a></p><h1>'+title+'</h1><p>'+description+'</p><p class="note">'+esc(collection['scope'])+'</p><p><a class="full-size" href="'+revision+'/'+ident+'.svg">Open full-size scalable SVG</a> <a class="full-size" href="'+revision+'/'+ident+'.png">Open full-size PNG</a></p><p>Use your browser’s zoom for finer details. The files below are the unchanged approved originals.</p>'+downloads(p)+'<figure class="poster-frame"><img src="'+revision+'/'+ident+'.svg" width="1800" height="2400" alt="'+alt+'"><figcaption>'+credit+'</figcaption></figure><p>English · '+esc(revision)+' · Vector PDF: one page, nominally 360 × 480 mm.</p><p><a href="'+revision+'/atlas.json">Descriptions and original file hashes (JSON)</a> · <a href="./">Protocol Atlas collection</a></p>'
    pages[ident+'.html']=shell(p['title'],content,True)
intro+='</div><p>'+credit+'</p><p><a href="'+revision+'/atlas.json">Collection descriptions and file hashes (JSON)</a> · <a href="../comparison/">Protocol comparison</a></p><section class="history" id="historical"><h2>Historical atlas</h2><p>The earlier unified Protocol Atlas v2 remains available as a historical snapshot, with its original qualifications and unchanged files.</p><p><a href="legacy-v2.html">View historical unified atlas v2</a> · <a href="poster.svg">SVG</a> · <a href="poster.pdf">PDF</a> · <a href="poster.png">PNG</a> · <a href="poster-content.json">Description and hashes</a></p></section>'
pages['index.html']=shell('Collection',intro)
for name,text in pages.items():
    if '--check' in sys.argv:assert (out/name).read_text()==text,'Atlas wrapper drift: '+name
    else:(out/name).write_text(text)
print('Atlas collection and historical wrappers consistent: '+str(len(pages))+' pages')
