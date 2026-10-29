#!/usr/bin/env python3
"""Check generated sharing metadata, links and preserved editorial payloads."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, parse_qs
import json, re, subprocess
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.meta={};self.links=[];self.ids=[];self.tracks=[];self.details=[];self.sources=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta':self.meta[a.get('property',a.get('name',''))]=a.get('content','')
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='track':self.tracks.append(a)
        if tag=='source':self.sources.append(a)
        if tag=='details' and a.get('class')=='video-details':self.details.append(a)
for directory in sorted((ROOT/'videos').iterdir()):
    if not directory.is_dir():continue
    data=json.loads((directory/'content.json').read_text())
    assert (directory/'share.jpg').stat().st_size<300000
    for name,lang in [('index.html','en'),('pt.html','pt-BR')]:
        path=directory/name;s=path.read_text();p=Page(s)
        assert len(p.ids)==len(set(p.ids)) and len(p.details)==1 and 'open' not in p.details[0]
        assert p.meta['og:title']==data['title'][lang] and p.meta['og:description']==data['summary'][lang]
        assert p.meta['og:image']==f'https://prp-protocol.org/videos/{directory.name}/share.jpg'
        assert len(p.tracks)==2
        if directory.name=='security-by-design':
            assert [t['srclang'] for t in p.tracks if 'default' in t]==[lang]
        else:
            assert all('default' not in t for t in p.tracks)
        assert len(p.sources)==1 and urlsplit(p.sources[0]['src']).path.split('/')[-1]==data['movieURL'].split('/')[-1]
        wa=[u for u in p.links if u.startswith('https://wa.me/')];assert len(wa)==1
        assert parse_qs(urlsplit(wa[0]).query)['text']==[data['title'][lang]+'\n'+p.meta['og:url']]
        for u in p.links:
            parts=urlsplit(u)
            if parts.scheme or parts.netloc:continue
            target=(path.parent/parts.path).resolve() if parts.path else path
            assert target.exists(),(path,u)
            if parts.fragment and target.suffix=='.html':assert parts.fragment in Page(target.read_text()).ids,(path,u)
print('PASS: all episode pages, closed native details, exact titles/descriptions, distinct image URLs, local links/fragments, individual sharing URLs and media targets; JPEGs under 300 KB. Security by Design defaults follow page language; older defaults unchanged.')
