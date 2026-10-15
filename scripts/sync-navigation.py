#!/usr/bin/env python3
"""Render the shared static header; --check detects navigation drift."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ITEMS = [('About', 'index.html#model'), ('Videos', 'videos.html'),
         ('Architecture', 'architecture.html'), ('Technical series', 'technical-series.html'),
         ('Comparison', 'comparison/'),
         ('Roadmap', 'index.html#roadmap'), ('Sponsors', 'index.html#sponsors'),
         ('Journal', 'https://journal.prp-protocol.org/')]
START, END = '<!-- Shared navigation -->', '<!-- End shared navigation -->'

def render(path, prefix=None):
    if prefix is None:
        prefix = '../../' if path.parent != ROOT else ''
    links = []
    for label, target in ITEMS:
        current = ' aria-current="page"' if path.parent == ROOT and target == path.name else ''
        href = target if target.startswith('https:') else prefix + target
        links.append(f'        <a href="{href}"{current}>{label}</a>')
    return f'''{START}
    <header class="site-header" lang="en">
      <a class="brand" href="{prefix}index.html#top" aria-label="Participant Relationship Protocol home">
        <span class="brand-mark" aria-hidden="true"><img src="{prefix}assets/prp_minilogo.svg" alt=""></span>
        <span>Participant Relationship Protocol</span>
      </a>
      <nav class="nav" aria-label="Primary navigation">
{chr(10).join(links)}
      </nav>
    </header>
    {END}'''

changed = []
for path in sorted(ROOT.glob('*.html')) + sorted((ROOT/'videos').glob('*/*.html')):
    source = path.read_text()
    text = source
    episode = path.parent != ROOT
    if episode and '<head>' not in text:
        text = re.sub(r'(<html\b[^>]*>)', r'\1<head>', text, count=1)
    if episode and '</head>' not in text:
        text = text.replace('</style>', '</style></head><body class="episode-page">', 1)
        text = text.replace('</html>', '</body></html>')
    elif episode:
        text = text.replace('<body>', '<body class="episode-page">', 1)
    css = ('../../' if episode else '') + 'site-navigation.css'
    if 'href="'+css+'"' not in text:
        text = text.replace('</head>', f'<link rel="stylesheet" href="{css}"></head>', 1)
    header = render(path)
    if START in text:
        text = re.sub(re.escape(START)+r'.*?'+re.escape(END), lambda _: header, text, count=1, flags=re.S)
    elif not episode:
        text = re.sub(r'<header class="site-header".*?</header>', lambda _: header, text, count=1, flags=re.S)
    else:
        # Preserve the original skip link and all language/chapter navigation.
        text = re.sub(r'(<body\b[^>]*>\s*(?:<a class="skip".*?</a>)?)', lambda m: m[0]+'\n'+header+'\n', text, count=1, flags=re.S)
    if text != source:
        changed.append(str(path.relative_to(ROOT)))
        if '--check' not in sys.argv:
            path.write_text(text)
if (ROOT/'comparison').is_dir():
    for path, text in [(ROOT/'comparison/navigation.html', render(ROOT/'comparison/index.html', '{{ROOT}}')),
                       (ROOT/'comparison/navigation.css', (ROOT/'site-navigation.css').read_text())]:
        if not path.exists() or path.read_text() != text:
            changed.append(str(path.relative_to(ROOT)))
            if '--check' not in sys.argv:
                path.write_text(text)
if '--check' in sys.argv and changed:
    sys.exit('Navigation drift: '+', '.join(changed))
print('Navigation consistent' if not changed else 'Updated '+str(len(changed))+' pages')
