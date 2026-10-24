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
if '--check' in sys.argv: assert (out/'index.html').read_text()==html,'Atlas wrapper drift'
else: (out/'index.html').write_text(html)
print('Atlas wrapper consistent')
