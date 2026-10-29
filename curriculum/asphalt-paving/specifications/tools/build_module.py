"""Build self-contained reading pages and two print books for the specifications module."""
from __future__ import annotations
import argparse
from functools import partial
from html import escape, unescape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json, os, re, shutil
from pathlib import Path
from threading import Thread
from urllib.parse import unquote, urlsplit
import markdown

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BOOKS = [('learner.md','learner-workbook','Learner workbook'),('instructor.md','teaching-guide','Teaching and answer guide')]
SKILLS = ['Reading','Writing','Numeracy','Digital','Problem solving','Communication','Collaboration','Adaptability','Creativity and innovation']

def render(name):
    source = (ROOT/name).read_text(encoding='utf-8')
    title=source.splitlines()[0].removeprefix('# ').strip()
    source=re.sub(r'_{5,}',lambda m:'<span class="'+('response-line' if len(m[0])>=45 else 'write-in')+'" aria-hidden="true"></span>',source)
    html=markdown.markdown(source,extensions=['tables','fenced_code','toc','sane_lists'])
    html=re.sub(r'^<h1[^>]*>.*?</h1>\s*','',html,count=1,flags=re.S)
    html=re.sub(r'^<p><strong>ACCESS · Indigenous Skills 4 Success</strong></p>\s*','',html,count=1)
    html=html.replace('<th>','<th scope="col">').replace('<th style=','<th scope="col" style=')
    html=re.sub(r'<table>.*?</table>',lambda m:'<div class="table-wrap" role="region" tabindex="0" aria-label="Data table">'+m[0]+'</div>',html,flags=re.S)
    # Keep authoring links to editable Markdown files intact; they are valid local assets.
    html=re.sub(r'(<h3 id="finish-with-evidence-and-a-next-step">.*)$',r'<section class="final-reflection">\1</section>',html,flags=re.S)
    return title,html

def page(title,body,label,book=False):
    cover=f'''<header class="cover"><p class="brand">ACCESS · INDIGENOUS SKILLS 4 SUCCESS</p><p class="eyebrow">{escape(label.upper())}</p><h1>Asphalt specifications</h1><p class="subtitle">Read, calculate, check</p><p class="intro">Follow a technical table. Reconcile a delivery record. Explain a decision another person can check.</p><div class="skill-strip">{''.join('<span>'+escape(s)+'</span>' for s in SKILLS)}</div><p class="edition">Classroom teaching edition · 29 October 2026<br>Selected reading from the historical 2006 design-build specifications.<br>Fictional exercise data · Technical review and classroom pilot pending.</p></header>'''
    if not book:
        cover=f'<header class="cover"><p class="brand">ACCESS · INDIGENOUS SKILLS 4 SUCCESS</p><h1>{escape(title)}</h1><p class="edition">Read, calculate, check · Classroom teaching edition · 29 October 2026</p></header>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | ACCESS IS4S</title><link rel="stylesheet" href="assets/module.css"></head><body class="{'teacher' if label=='Teaching and answer guide' else 'learner'}"><a class="skip" href="#content">Skip to content</a><main><div class="screen-nav"><a href="index.html">Module home</a> · <a href="learner-workbook.pdf">Learner PDF</a> · <a href="teaching-guide.pdf">Teaching PDF</a> · <a href="source-map.html">Source map</a></div>{cover}{body}<p class="footer-note">ACCESS IS4S · Local teaching criteria; no official proficiency or trade-certification claim.</p></main></body></html>'''

def build_html():
    for name,stem,label in BOOKS:
        title,body=render(name)
        headings=re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',body,re.S)
        entries=[]
        for anchor,heading in headings:
            text=unescape(re.sub('<[^>]+>','',heading))
            entries.append(f'<li><a href="#{escape(anchor)}"><span class="toc-label">{escape(text)}</span><span class="toc-page" data-toc-target="{escape(anchor)}">—</span></a></li>')
        toc='<nav class="contents" aria-label="Contents"><h2>Contents</h2><ol>'+''.join(entries)+'</ol></nav>'
        (ROOT/f'{stem}.html').write_text(page(title,toc+'<article id="content">'+body+'</article>',label,True),encoding='utf-8')
    for name,stem in [('README.md','index'),('source-map.md','source-map'),('source-excerpts.md','source-excerpts')]:
        title,body=render(name)
        (ROOT/f'{stem}.html').write_text(page(title,'<article id="content">'+body+'</article>',title),encoding='utf-8')

def destinations(path):
    from pypdf import PdfReader
    reader=PdfReader(path)
    return {str(k).lstrip('/'):reader.get_destination_page_number(v)+1 for k,v in reader.named_destinations.items()}

def public_pdf_links(path,title):
    from pypdf import PdfReader,PdfWriter
    from pypdf.generic import NameObject,TextStringObject
    writer=PdfWriter(clone_from=PdfReader(path))
    for page_ in writer.pages:
        for ref in page_.get('/Annots',[]):
            action=ref.get_object().get('/A')
            if not action or not action.get('/URI'):continue
            parsed=urlsplit(str(action['/URI']))
            if parsed.hostname in {'localhost','127.0.0.1'}:
                action[NameObject('/URI')]=TextStringObject('https://github.com/GOSTROGIS/Business/blob/main/'+unquote(parsed.path).lstrip('/')+(('#'+parsed.fragment) if parsed.fragment else ''))
    writer.add_metadata({'/Title':title,'/Author':'ACCESS IS4S curriculum development','/Subject':'Historical specification reading and fictional classroom record calculations'})
    with path.open('wb') as f:writer.write(f)

def build_pdf():
    from playwright.sync_api import sync_playwright
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(REPO)))
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    results={}
    try:
        with sync_playwright() as p:
            executable=os.environ.get('IS4S_CHROMIUM_PATH') or shutil.which('chromium')
            browser=p.chromium.launch(headless=True,**({'executable_path':executable} if executable else {}))
            page_=browser.new_page(viewport={'width':1200,'height':1000})
            for name,stem,label in BOOKS:
                target=ROOT/f'{stem}.html';pdf=ROOT/f'{stem}.pdf'
                for attempt in range(1,6):
                    page_.goto(f'http://127.0.0.1:{server.server_port}/'+target.relative_to(REPO).as_posix(),wait_until='networkidle')
                    page_.evaluate('document.fonts.ready')
                    page_.evaluate('Promise.all(Array.from(document.images).map(i => i.decode()))')
                    page_.pdf(path=str(pdf),format='A4',print_background=True,prefer_css_page_size=True,tagged=True,outline=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="width:100%;font-family:Arial;font-size:8px;text-align:center;color:#62564c">ACCESS IS4S · Asphalt specifications · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
                    mapping=destinations(pdf);html=target.read_text()
                    def repl(m):
                        anchor=unescape(m[2]);number=mapping.get(anchor)
                        if number is None:raise RuntimeError(f'Missing PDF destination: {anchor}')
                        return m[1]+str(number)+m[4]
                    updated=re.sub(r'(<span class="toc-page" data-toc-target="([^"]+)">)(.*?)(</span>)',repl,html)
                    if updated==html:break
                    target.write_text(updated)
                else:raise RuntimeError(f'TOC pagination did not converge: {stem}')
                public_pdf_links(pdf,'Asphalt specifications · '+label)
                from pypdf import PdfReader
                results[stem]={'pages':len(PdfReader(pdf).pages),'pagination_passes':attempt}
            browser.close()
    finally:server.shutdown();thread.join()
    (ROOT/'build-metadata.json').write_text(json.dumps(results,indent=2)+'\n')
    return results

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--html-only',action='store_true');args=parser.parse_args()
    build_html()
    print(json.dumps({'html_pages':5,'pdf':{} if args.html_only else build_pdf()},indent=2))
