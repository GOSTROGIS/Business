"""Build standalone Roadbuilding foundations reading pages and two printable books."""
from __future__ import annotations

import argparse
from functools import partial
from html import escape, unescape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import re
import shutil
from threading import Thread
from urllib.parse import urlsplit, unquote

import markdown

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'line-a'
REPO = ROOT.parents[1]
LEARNER = ['00-start.md', '01-industry-evidence.md', '02-history.md', '03-technology.md',
           '04-workers.md', '05-road-documents.md', '06-trends.md', '07-reference.md']
TEACHER = [f'answers-{i:02d}.md' for i in range(1, 7)] + ['technical-handoff.md']
CSS = '''
@font-face{font-family:Plex;src:url('../assets/fonts/ibm-plex-sans-latin-400-normal.woff2')}
@font-face{font-family:Plex;src:url('../assets/fonts/ibm-plex-sans-latin-600-normal.woff2');font-weight:600}
*{box-sizing:border-box}body{margin:0;color:#173b3a;background:#f4f0e7;font-family:Plex,Arial,sans-serif;line-height:1.58}
main{max-width:960px;margin:auto;padding:32px}header{background:#143d3b;color:white;padding:36px 32px}
header div{max-width:896px;margin:auto}h1{font-size:2.1rem;line-height:1.2}h2{margin-top:1.6em;color:#175f5c;font-size:1.42rem;line-height:1.25}
h3{font-size:1.13rem;color:#954d32;line-height:1.3}a{color:#146b68}header a{color:#fff}article{background:#fff;padding:28px;margin-bottom:28px;border-top:5px solid #b7754b}
table{border-collapse:collapse;width:100%;font-size:.91em;margin:1.2em 0}th,td{border:1px solid #bccdca;padding:9px;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#e4eeeb}
.table-wrap{max-width:100%;overflow-x:auto}.table-wrap:focus{outline:2px solid #146b68;outline-offset:3px}
img{max-width:100%;height:auto}code{background:#edf4f1;padding:1px 3px;white-space:normal}.activity-id{white-space:nowrap}nav li{margin:8px 0}p,li{overflow-wrap:break-word}.edition{font-size:.9rem}.skip{position:absolute;left:-9999px}.skip:focus{left:8px;top:8px;background:white;padding:8px}
@media(max-width:600px){main{padding:12px}article{padding:16px}header{padding:24px 16px}table{font-size:.78rem}th,td{padding:5px}}
@media print{body{background:white;font-size:10.3pt;line-height:1.45}main{max-width:none;padding:0}header{background:white;color:#173b3a;padding:12mm 0;break-after:page}header a{color:#173b3a}article{padding:0;border:0;margin:0;break-before:page}h1{font-size:23pt}h2{font-size:15pt}h3{font-size:12pt}h1,h2,h3{break-after:avoid}p,li{orphans:3;widows:3}thead{display:table-header-group}tr,img{break-inside:avoid}table{font-size:9pt}th,td{padding:6px}.screen{display:none}nav{break-after:page}.chapter-nav{display:none}}
@media print{.table-wrap{overflow:visible}}
'''

def body_for(name: str) -> tuple[str, str]:
    text = (BOOK / name).read_text(encoding='utf-8')
    title = text.splitlines()[0].lstrip('# ').strip()
    body = markdown.markdown(text, extensions=['tables', 'fenced_code', 'toc', 'sane_lists'])
    body = re.sub(r'(?<![\w"-])(LA[1-6]-\d{2})(?![\w"-])', r'<span class="activity-id">\1</span>', body)
    body = body.replace('<th>', '<th scope="col">').replace('<th style=', '<th scope="col" style=')
    body = re.sub(r'<table>.*?</table>', lambda m: '<div class="table-wrap" tabindex="0" role="region" aria-label="Data table">' + m[0] + '</div>', body, flags=re.S)
    return title, body

def page(title: str, body: str, tagline: str) -> str:
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | ACCESS IS4S</title><style>{CSS}</style></head><body><a class="skip" href="#content">Skip to content</a><header><div><p>ACCESS · Indigenous Skills 4 Success</p><h1>{escape(title)}</h1><p>{escape(tagline)}</p><p class="edition">Classroom teaching edition · 29 October 2026 · Technical review and pilot pending</p></div></header><main id="content">{body}</main></body></html>'''

def build_html():
    title, body = body_for('README.md')
    (BOOK / 'index.html').write_text(page(title, f'<article>{body}</article>', 'Choose a book, unit or teaching resource.'), encoding='utf-8')
    for name in LEARNER + TEACHER:
        title, body = body_for(name)
        target = BOOK / name.replace('.md', '.html')
        target.write_text(page(title, f'<article>{body}</article>', 'Read, practise, check and explain.'), encoding='utf-8')
    for names, stem, title, tagline in [
        (LEARNER, 'roadbuilding-foundations', 'Asphalt paving · Roadbuilding foundations', 'Industry, materials, people, road documents and evidence.'),
        (TEACHER, 'teaching-guide', 'Roadbuilding foundations · Teaching and answer guide', 'Lesson sequences, answer guidance, evidence criteria and technical handoff.')]:
        parts, entries = [], []
        for index, name in enumerate(names, 1):
            heading, body = body_for(name)
            anchor = f'chapter-{index}'
            entries.append(f'<li><a href="#{anchor}">{escape(heading)}</a></li>')
            parts.append(f'<article id="{anchor}">{body}</article>')
        contents = '<nav aria-label="Contents"><h2>Contents</h2><ol>' + ''.join(entries) + '</ol></nav>'
        (BOOK / f'{stem}.html').write_text(page(title, contents + ''.join(parts), tagline), encoding='utf-8')

def public_pdf_links(path: Path):
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, TextStringObject
    reader, writer = PdfReader(path), PdfWriter()
    for page_ in reader.pages:
        for ref in page_.get('/Annots', []):
            annotation = ref.get_object()
            action = annotation.get('/A')
            if not action or not action.get('/URI'):
                continue
            uri = str(action['/URI'])
            parsed = urlsplit(uri)
            if parsed.hostname in {'localhost', '127.0.0.1'}:
                relative = unquote(parsed.path).lstrip('/')
                action[NameObject('/URI')] = TextStringObject('https://github.com/GOSTROGIS/Business/blob/main/' + relative + (('#' + parsed.fragment) if parsed.fragment else ''))
        writer.add_page(page_)
    writer.add_metadata({'/Title': path.stem.replace('-', ' '), '/Author': 'ACCESS IS4S curriculum development'})
    with path.open('wb') as out:
        writer.write(out)

def build_pdf():
    from playwright.sync_api import sync_playwright
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(REPO)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as p:
            executable = os.environ.get('IS4S_CHROMIUM_PATH') or shutil.which('chromium')
            browser = p.chromium.launch(headless=True, **({'executable_path': executable} if executable else {}))
            page_ = browser.new_page(viewport={'width': 1200, 'height': 900})
            for stem in ['roadbuilding-foundations', 'teaching-guide']:
                relative = (BOOK / f'{stem}.html').relative_to(REPO).as_posix()
                page_.goto(f'http://127.0.0.1:{server.server_port}/{relative}', wait_until='networkidle')
                page_.evaluate('document.fonts.ready')
                page_.pdf(path=str(BOOK / f'{stem}.pdf'), format='A4', print_background=True,
                          margin={'top':'16mm','bottom':'19mm','left':'16mm','right':'16mm'},
                          display_header_footer=True, header_template='<span></span>',
                          footer_template='<div style="width:100%;font-size:8px;text-align:center;color:#555">ACCESS IS4S · Roadbuilding foundations · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
                public_pdf_links(BOOK / f'{stem}.pdf')
            browser.close()
    finally:
        server.shutdown()
        thread.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--html-only', action='store_true')
    args = parser.parse_args()
    build_html()
    if not args.html_only:
        build_pdf()
    print('Built Line A reading pages' + (' and two PDFs.' if not args.html_only else '.'))
