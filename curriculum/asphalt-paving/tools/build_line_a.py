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
from activity_names import readable

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'line-a'
REPO = ROOT.parents[1]
LEARNER = ['00-start.md', '01-industry-evidence.md', '02-history.md', '03-technology.md',
           '04-workers.md', '05-road-documents.md', '06-trends.md', '07-reference.md']
TEACHER = [f'answers-{i:02d}.md' for i in range(1, 7)] + ['technical-handoff.md']
CSS = '''
@font-face{font-family:Plex;src:url('../assets/fonts/ibm-plex-sans-latin-400-normal.woff2')}
@font-face{font-family:Plex;src:url('../assets/fonts/ibm-plex-sans-latin-600-normal.woff2');font-weight:600}
:root{--paper:#F7F4F1;--ink:#1A1512;--red:#D2181F;--gold:#FFBC00;--muted:#625D58;--line:#d8cdc3}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:var(--paper);font-family:Plex,Arial,sans-serif;line-height:1.6}
main{max-width:1040px;margin:auto;padding:36px 32px}header{background:var(--ink);color:white;padding:42px 32px;border-bottom:8px solid var(--gold)}
header div{max-width:920px;margin:auto}header div>p:first-child{color:var(--gold);font-size:.85rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase}h1{font-size:2.35rem;line-height:1.16;letter-spacing:-.025em;max-width:25ch}h2{margin-top:1.6em;color:var(--ink);font-size:1.5rem;line-height:1.25}
h3{font-size:1.16rem;color:#a3141a;line-height:1.32}a{color:#a3141a;text-underline-offset:3px}a:focus-visible{outline:3px solid var(--red);outline-offset:4px}header a{color:#fff}article{background:#fff;padding:32px;margin-bottom:28px;border-top:5px solid var(--red)}
table{border-collapse:collapse;width:100%;font-size:.91em;margin:1.2em 0}th,td{border:1px solid var(--line);padding:10px;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#eee6df;color:var(--ink)}tbody tr:nth-child(even){background:#fcfaf8}
.table-wrap{max-width:100%;overflow-x:auto}.table-wrap:focus{outline:3px solid var(--red);outline-offset:3px}
img{max-width:100%;height:auto}code{background:#f0eae4;padding:1px 3px;white-space:normal}.activity-id{white-space:nowrap}nav li{margin:8px 0}p,li{overflow-wrap:break-word}.edition{font-size:.9rem}.skip{position:absolute;left:-9999px}.skip:focus{left:8px;top:8px;background:white;padding:8px;color:var(--ink)}
.competency{border-left:5px solid var(--gold);background:var(--paper);padding:20px 24px;margin:24px 0}.competency h2{margin:.4em 0;font-size:1.3rem}.competency p{margin:.4em 0 0}.eyebrow{font-size:.76rem;letter-spacing:.1em;font-weight:600;color:#a3141a}
.learning-figure{margin:28px 0;padding:20px;border:1px solid var(--line);border-top:4px solid var(--gold);background:var(--paper)}.learning-figure img{display:block;width:100%;object-fit:contain;max-height:750px;margin:14px auto;background:white}.figure-number{font-size:.8rem;color:#a3141a;font-weight:600;letter-spacing:.07em;margin:0}.figure-title{font-size:1.12rem;margin:4px 0 10px;font-weight:600}.learning-figure figcaption{font-size:.83rem;line-height:1.45;color:#51483f;overflow-wrap:anywhere}.learning-figure figcaption a{color:inherit}.learning-figure.manual img{max-height:510px}.learning-figure .scope{font-weight:600;margin:10px 0}
@media(max-width:600px){main{padding:12px}article{padding:17px}header{padding:28px 18px}h1{font-size:1.85rem}table{font-size:.83rem}.table-wrap table:has(thead th:nth-child(3)){min-width:540px}th,td{padding:7px}.competency{padding:16px}.learning-figure{padding:12px;margin:22px 0}.learning-figure figcaption{font-size:.82rem}.learning-figure img{max-height:none}}
@media print{body{background:white;font-size:10.3pt;line-height:1.45}main{max-width:none;padding:0}header{background:white;color:var(--ink);padding:12mm 0;break-after:page;border-bottom:3px solid var(--red)}header div>p:first-child{color:var(--ink)}header a{color:var(--ink)}article{padding:0;border:0;margin:0;break-before:page}h1{font-size:25pt}h2{font-size:15pt}h3{font-size:12pt}h1,h2,h3{break-after:avoid}p,li{orphans:3;widows:3}thead{display:table-header-group}tr,img{break-inside:avoid}table{font-size:8.8pt}th,td{padding:6px}.screen{display:none}nav{break-after:page}.chapter-nav{display:none}.table-wrap{overflow:visible}.competency{padding:10px 14px;margin:12px 0;break-inside:avoid}.competency h2{font-size:13pt}.eyebrow{font-size:8pt}.learning-figure{break-inside:avoid;padding:10px;margin:16px 0}.learning-figure img{max-height:165mm;width:100%;margin:8px auto}.learning-figure.manual img{max-height:130mm}.figure-number{font-size:8pt}.figure-title{font-size:11pt}.learning-figure figcaption{font-size:8pt;line-height:1.35}.learning-figure .scope{font-size:8.5pt}}
'''

def body_for(name: str) -> tuple[str, str]:
    text = (BOOK / name).read_text(encoding='utf-8')
    title = text.splitlines()[0].lstrip('# ').strip()
    body = markdown.markdown(text, extensions=['tables', 'fenced_code', 'toc', 'sane_lists'])
    body = readable(body)
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
