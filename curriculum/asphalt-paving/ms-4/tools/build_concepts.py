"""Build complete learner and instructor concept books with credited SVG redraws."""
from pathlib import Path
from html import escape
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from urllib.parse import urlsplit
import json,markdown,re
from playwright.sync_api import sync_playwright
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject,TextStringObject
ROOT=Path(__file__).resolve().parents[1];BOOK=ROOT/'concepts';REPO=ROOT.parents[2]
figs=json.loads((BOOK/'figure-manifest.json').read_text())['figures']
manifest=json.loads((ROOT/'manifest.json').read_text());locations=manifest['page_locations']
CSS='''@font-face{font-family:Plex;src:url('../../assets/fonts/ibm-plex-sans-latin-400-normal.woff2')}@font-face{font-family:Plex;src:url('../../assets/fonts/ibm-plex-sans-latin-600-normal.woff2');font-weight:600}*{box-sizing:border-box}body{margin:0;background:#F7F4F1;color:#1A1512;font:17px/1.6 Plex,Arial,sans-serif}header{background:#1A1512;color:white;border-bottom:6px solid #FFBC00;padding:35px 24px}header>div,main{max-width:1000px;margin:auto}header h1{font-size:42px;line-height:1.12}header p{color:#FFBC00}main{padding:28px}article{padding:30px;background:white;border-top:5px solid #D2181F}h2{font-size:29px;line-height:1.25;color:#a71920;margin-top:1.6em}h3{font-size:22px;line-height:1.3}a{color:#a71920;text-underline-offset:3px}a:focus-visible{outline:3px solid #D2181F;outline-offset:4px}.teaching-figure{margin:24px 0;border:1px solid #d8d0c9;border-radius:10px;padding:12px;background:#F7F4F1}.teaching-figure img{display:block;width:100%;height:auto}.teaching-figure figcaption{font-size:13px;line-height:1.5;margin:12px 3px 3px}table{width:100%;border-collapse:collapse;font-size:15px}th,td{padding:10px;border:1px solid #d8d0c9;text-align:left;vertical-align:top}th{background:#fff4d2}.table-wrap{overflow:auto}p,li,td{overflow-wrap:anywhere}code{white-space:normal}.skip{position:absolute;left:-10000px}.skip:focus{left:12px;top:8px;background:white;padding:10px}.nav{display:flex;flex-wrap:wrap;gap:18px;margin-bottom:20px}.answer-space{height:48px;border-bottom:1px solid #b3aaa3;margin:8px 0 20px}@media(max-width:650px){main{padding:12px}article{padding:16px}header h1{font-size:32px}h2{font-size:26px}th,td{padding:6px}}@page{size:Letter;margin:15mm 14mm 18mm}@media print{body{background:white;font-size:10.5pt;line-height:1.45}header{padding:10mm 0;background:white;color:#1A1512;border-color:#D2181F;break-after:page}header h1{font-size:28pt}header p{color:#625D58}main{padding:0;max-width:none}article{padding:0;border:0}.nav,.skip{display:none}h2{font-size:18pt;break-before:page}h3{font-size:13pt}h1,h2,h3{break-after:avoid}p,li{orphans:3;widows:3}.teaching-figure{break-inside:avoid;padding:5px}.teaching-figure figcaption{font-size:8pt}table{font-size:9pt}tr{break-inside:avoid}.table-wrap{overflow:visible}thead{display:table-header-group}.instructor h2{break-before:auto}.answer-space{height:30px}}
'''
def figure(f,i):
 refs=[]
 for r in f['references']:
  if 'pdf_page' in r:
   label=(f"Figure {r['figure']}" if 'figure' in r else r.get('section','Passage'))+f", p. {r.get('printed_page')} (PDF {r['pdf_page']})"
   refs.append(f'<a href="../{locations[str(r["pdf_page"])]}">{escape(label)}</a>')
  else:
   refs.append(escape(r['section'])+', pp. '+', '.join(map(str,r['printed_pages'])))
 credits=' '.join(f"Original Figure {x['figure']} is credited to {x['credit']} in the handbook's contributor list." for x in f['original_contributors'])
 note=f"Adapted from <em>The asphalt handbook</em> (7th ed., MS-4; {'; '.join(refs)}), by Asphalt Institute, 2007. {escape(f['adaptation'])} {escape(credits)} Copyright 2007 by Asphalt Institute; original contributor credits retained."
 return f'<figure class="teaching-figure"><a href="{f["file"]}"><img src="{f["file"]}" alt="{escape(f["alt"],quote=True)}"></a><figcaption><strong>Figure {i}. <em>{escape(f["title"])}</em></strong><br><em>Note.</em> {note}</figcaption></figure>'
def main():
 for name,stem,title in [('learner','index','Understanding asphalt: materials, machines and records'),('instructor','teaching-guide','Understanding asphalt · Teaching and answer guide')]:
  s=(BOOK/f'{name}.md').read_text()
  for i,f in enumerate(figs,1):s=s.replace('{{'+f['id']+'}}',figure(f,i))
  assert '{{' not in s
  body=markdown.markdown(s,extensions=['tables','fenced_code','toc','sane_lists']);body=re.sub(r'<h1[^>]*>.*?</h1>','',body,count=1,flags=re.S)
  body=body.replace('<th>','<th scope="col">');body=re.sub(r'<table>.*?</table>',lambda m:'<div class="table-wrap" tabindex="0" role="region" aria-label="Learning table">'+m[0]+'</div>',body,flags=re.S)
  html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | ACCESS IS4S</title><style>{CSS}</style></head><body class="{name}"><a class="skip" href="#main">Skip to lesson</a><header><div><p>ACCESS · INDIGENOUS SKILLS 4 SUCCESS</p><h1>{escape(title)}</h1><p>Trade words · clear pictures · checked explanations</p></div></header><main id="main"><nav class="nav"><a href="../index.html">Complete MS-4 reader</a><a href="index.html">Learner book</a><a href="teaching-guide.html">Teaching guidance</a><a href="{'learner-workbook' if name=='learner' else 'teaching-guide'}.pdf">Print book</a></nav><article>{body}</article></main></body></html>'''
  (BOOK/f'{stem}.html').write_text(html)
 class Quiet(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(REPO)));Thread(target=server.serve_forever,daemon=True).start()
 base=f'http://127.0.0.1:{server.server_port}/'
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);tab=browser.new_page()
   for src,stem in [('index','learner-workbook'),('teaching-guide','teaching-guide')]:
    tab.goto(base+(BOOK/f'{src}.html').relative_to(REPO).as_posix());tab.evaluate('document.fonts.ready')
    target=BOOK/f'{stem}.pdf';tab.pdf(path=str(target),print_background=True,prefer_css_page_size=True,tagged=True,outline=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="font:9px Arial;width:100%;text-align:center;color:#625D58">ACCESS IS4S · Understanding asphalt · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
    r=PdfReader(target);w=PdfWriter();w.clone_document_from_reader(r)
    for page in w.pages:
     for ref in page.get('/Annots',[]):
      action=ref.get_object().get('/A')
      if action and str(action.get('/URI','')).startswith(base):
       u=urlsplit(str(action['/URI']));action[NameObject('/URI')]=TextStringObject('https://github.com/GOSTROGIS/Business/blob/main'+u.path+('#'+u.fragment if u.fragment else ''))
    tmp=target.with_suffix('.tmp.pdf');w.write(tmp);tmp.replace(target);print(stem,len(r.pages),'pages')
   browser.close()
 finally:server.shutdown();server.server_close()
if __name__=='__main__':main()
