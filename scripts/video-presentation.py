#!/usr/bin/env python3
"""Apply website-owned video sharing, metadata and disclosure wrappers.

Run after importing approved episode HTML. --thumbnails derives share.jpg from
an existing poster or a frame at 3 seconds; never modifies the approved MP4.
"""
from pathlib import Path
import argparse, html, json, re, subprocess
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://prp-protocol.org/'
args = argparse.ArgumentParser()
args.add_argument('--check', action='store_true')
args.add_argument('--thumbnails', action='store_true')
opts = args.parse_args()

def share(slug, title, pt=False):
    url = BASE+'videos/'+slug+('/pt.html' if pt else '/index.html')
    label = 'Compartilhar no WhatsApp' if pt else 'Share on WhatsApp'
    copy = 'Copiar link' if pt else 'Copy link'
    return ('<!-- Video sharing -->\n<div class="video-sharing">'
            f'<a href="https://wa.me/?text={quote(title+chr(10)+url, safe="")}" target="_blank" rel="noopener noreferrer">{label}</a> '
            f'<button type="button" data-copy-link="{url}" hidden>{copy}</button>'
            '<span class="share-status" role="status" aria-live="polite"></span></div>\n<!-- End video sharing -->')

def resources(s, prefix):
    if 'href="'+prefix+'video-presentation.css"' not in s:
        s=s.replace('</head>',f'<link rel="stylesheet" href="{prefix}video-presentation.css">\n<script src="{prefix}scripts/video-sharing.js" defer></script>\n</head>')
    return s

changed=[]
for directory in sorted((ROOT/'videos').iterdir()):
    if not directory.is_dir(): continue
    data=json.loads((directory/'content.json').read_text())
    slug=directory.name
    if opts.thumbnails and not (directory/'share.jpg').exists():
        poster=directory/'poster.png'
        source=poster if poster.exists() else ROOT/data['movieURL'].removeprefix(BASE)
        command=['ffmpeg','-v','error']+([] if poster.exists() else ['-ss','3'])
        subprocess.run(command+['-i',str(source),'-frames:v','1','-vf','scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2','-q:v','3',str(directory/'share.jpg')],check=True)
    assert (directory/'share.jpg').exists(),f'Run --thumbnails for {slug}'
    for name,language in [('index.html','en'),('pt.html','pt-BR')]:
        path=directory/name; original=path.read_text(); s=original; pt=language=='pt-BR'
        title=data['title'][language]; summary=data['summary'][language]
        url=BASE+f'videos/{slug}/{name}'; image=BASE+f'videos/{slug}/share.jpg'
        # Replace only our own generated fragments on subsequent runs.
        s=re.sub(r'<!-- Video metadata -->.*?<!-- End video metadata -->\n?', '',s,flags=re.S)
        meta={'og:type':'website','og:site_name':'PRP','og:title':title,'og:description':summary,'og:url':url,'og:locale':'pt_BR' if pt else 'en_US','og:image':image,'og:image:secure_url':image,'og:image:type':'image/jpeg','og:image:width':'960','og:image:height':'540','og:image:alt':title+' — PRP'}
        metadata='<!-- Video metadata -->\n'+f'<link rel="canonical" href="{url}">\n'
        metadata+='\n'.join(f'<meta property="{key}" content="{html.escape(value,quote=True)}">' for key,value in meta.items())+'\n<!-- End video metadata -->\n'
        s=resources(s,'../../')
        s=s.replace('</head>',metadata+'</head>')
        # Native details retains the complete approved HTML, IDs and links.
        if '<!-- Video details -->' not in s:
            end=s.index('</video>')+len('</video>'); close=s.index('</main>',end)
            label='Transcrição, descrição visual, créditos e downloads' if pt else 'Transcript, visual description, credits and downloads'
            s=s[:end]+'\n<!-- Video details -->\n<details class="video-details"><summary>'+label+'</summary><div class="video-details-content">'+s[end:close]+'</div></details>\n<!-- End video details -->\n'+s[close:]
        s=re.sub(r'\n?<!-- Video sharing -->.*?<!-- End video sharing -->\n?', '',s,flags=re.S)
        end=s.index('</video>')+len('</video>');s=s[:end]+'\n'+share(slug,title,pt)+'\n'+s[end:]
        # Set a visible poster on every player, independently of metadata preload.
        s=re.sub(r'<video\b([^>]*)>',lambda m:'<video'+re.sub(r'\s+poster="[^"]*"','',m[1])+' poster="share.jpg">',s,count=1)
        if s!=original:
            changed.append(str(path.relative_to(ROOT)))
            if not opts.check:path.write_text(s)

for name in ['index.html','videos.html','technical-series.html']:
    path=ROOT/name;original=path.read_text();s=original
    s=re.sub(r'\n?<!-- Video sharing -->.*?<!-- End video sharing -->\n?', '',s,flags=re.S)
    def card(m):
        article=m[0]; slug=m[1];datafile=ROOT/'videos'/slug/'content.json'
        if not datafile.exists():return article
        data=json.loads(datafile.read_text())
        # Place within the final text block to preserve the existing subgrid.
        pos=article.rfind('</p>')
        if pos<0:return article
        pos+=4
        return article[:pos]+'\n'+share(slug,data['title']['en'])+'\n'+article[pos:]
    s=re.sub(r'<article\b[^>]*id="([^"]+)".*?</article>',card,s,flags=re.S)
    s=resources(s,'')
    if s!=original:
        changed.append(name)
        if not opts.check:path.write_text(s)
if opts.check and changed:raise SystemExit('Presentation drift: '+', '.join(changed))
print('Video presentation consistent' if not changed else 'Updated '+str(len(changed))+' pages')
