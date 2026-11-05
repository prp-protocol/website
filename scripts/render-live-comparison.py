"""Build thin, data-free comparison routes; initial activation preserves fallback files.

--activate only adds the live loader to existing pages. --shells is authorized
only after public live-source replacement has been observed. No network access.
"""
import argparse,json,hashlib,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'comparison'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--activate',action='store_true');ap.add_argument('--shells',action='store_true');args=ap.parse_args()
    assert args.activate != args.shells
    configpath=OUT/'live-config.json'
    if not configpath.exists():
        d=json.loads((OUT/'data.json').read_text())
        config={'schema_version':1,'cells':[c['id'] for c in d['cells']], 'stacks':[c['id'] for c in d['columns']],
            'groups':json.loads((OUT/'groups.json').read_text()),
            'assets':{str(p.relative_to(OUT)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted((OUT/'logos').iterdir()) if p.is_file()}}
        configpath.write_text(json.dumps(config,indent=2)+'\n')
    config=json.loads(configpath.read_text())
    presentation=runpy.run_path(str(OUT/'render.py'))
    css=presentation['CSS']+presentation['EVIDENCE_CSS']+'\n.live-source-status{margin:16px 24px;padding:12px;border:1px solid #165e70;overflow-wrap:anywhere}.live-source-status[data-state="stale"],.live-source-status[data-state="error"]{background:#fff0c9}.live-source-status button{min-height:44px}.comparison-layout[hidden]{display:none!important}'
    (OUT/'live.css').write_text(css+'\n')
    routes=['index.html','methodology.html','logos.html','cell.html','stack.html']+[f'cells/{c}.html' for c in config['cells']]+[f'stacks/{c}.html' for c in config['stacks']]
    for route in routes:
        path=OUT/route;depth=len(Path(route).parts)-1;prefix='../'*depth
        includes=f'<link rel="stylesheet" href="{prefix}live.css"><link rel="stylesheet" href="{prefix}yes-filter.css"><script src="{prefix}live.js" defer></script>'
        if args.activate and path.exists():
            html=path.read_text()
            if 'live.js' not in html:
                # The original index already includes the filter; other routes need it.
                if 'yes-filter.js' not in html:includes+=f'<script src="{prefix}yes-filter.js" defer></script>'
                html=html.replace('</head>',includes+'</head>')
                html=html.replace('<body>','<body><noscript><p>Automatic comparison updates require JavaScript. The fallback below is historical7.96, not the latest research. <a href="https://github.com/prp-protocol/prp-comparative-analysis">Read the research publication</a>.</p></noscript>')
                path.write_text(html)
        else:
            nav=(OUT/'navigation.html').read_text().replace('{{ROOT}}','../'*(depth+1))
            html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Protocol comparison — PRP</title><link rel="stylesheet" href="'+prefix+'navigation.css">'+includes+f'<script src="{prefix}yes-filter.js" defer></script></head><body>'+nav+'<noscript><p>This comparison loads the current public research using JavaScript. <a href="https://github.com/prp-protocol/prp-comparative-analysis">Read the source publication without JavaScript</a>.</p></noscript><div class="comparison-layout"><main><h1>Protocol and stack comparison</h1><p>Loading verified research…</p></main></div></body></html>\n'
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(html)
    print(json.dumps({'mode':'activation' if args.activate else 'shells','routes':len(routes),'research_embedded':args.activate}))
if __name__=='__main__':main()
