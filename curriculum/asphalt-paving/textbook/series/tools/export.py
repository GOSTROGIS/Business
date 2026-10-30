"""Export seven study/answer pairs and check desktop/mobile rendering."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
from urllib.parse import urlsplit,unquote
import json,shutil,argparse
import fitz
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];REPO=R.parents[3]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(REPO)));Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'+R.relative_to(REPO).as_posix()+'/'
parser=argparse.ArgumentParser();parser.add_argument("--volumes",nargs="+",type=int,default=list(range(2,9)));args=parser.parse_args()
checks=[];pdfs=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox']);page=browser.new_page()
  for width in [390,1280]:
   page.set_viewport_size({'width':width,'height':1000})
   for name in ['index.html','B3.html','B4.html','C2.html','E4.html','F2.html','G6.html','H2.html','I4.html','J2.html','K3.html','L3.html','volume-8-answers.html']:
    page.goto(base+name,wait_until='networkidle');page.evaluate('document.fonts.ready');page.evaluate("async()=>{for(const i of document.images)i.loading='eager';await Promise.all([...document.images].map(i=>i.decode()));}")
    bad=page.evaluate('''() => ({overflow:document.documentElement.scrollWidth>innerWidth+1,images:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src),duplicateIds:[...document.querySelectorAll('[id]')].map(e=>e.id).filter((id,i,a)=>a.indexOf(id)!==i)})''')
    checks.append({'file':name,'width':width,**bad});assert not any(bad.values()),(name,width,bad)
  page.set_viewport_size({'width':1280,'height':1000})
  for n in args.volumes:
   for suffix in ['','-answers']:
    stem=f'volume-{n}{suffix}';page.goto(base+stem+'.html',wait_until='networkidle');page.evaluate('document.fonts.ready');page.evaluate("async()=>{for(const i of document.images)i.loading='eager';await Promise.all([...document.images].map(i=>i.decode()));}")
    target=R/(stem+'.pdf');page.pdf(path=str(target),format='A4',print_background=True,prefer_css_page_size=True,tagged=True,outline=True,display_header_footer=True,header_template='<span></span>',footer_template=f'<div style="width:100%;font-size:8px;text-align:center;color:#625d58">ACCESS IS4S · Volume {n}'+(' · Teaching and answers' if suffix else '')+' · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
    # Rewrite only external local-server links; preserve tagged structure, outlines and internal destinations.
    doc=fitz.open(target)
    for pg in doc:
     for link in pg.get_links():
      u=urlsplit(link.get('uri',''))
      if u.hostname in {'127.0.0.1','localhost'}:
       link['uri']='https://github.com/GOSTROGIS/Business/blob/main/'+unquote(u.path).lstrip('/')+('#'+u.fragment if u.fragment else '');pg.update_link(link)
    count=len(doc);doc.saveIncr();doc.close();pdfs.append({'file':target.name,'pages':count,'bytes':target.stat().st_size});print(stem,count,'pages',flush=True)
  browser.close()
finally:server.shutdown();server.server_close()
if (R/'pdf-inventory.json').exists():
 previous=json.loads((R/'pdf-inventory.json').read_text());changed={x['file'] for x in pdfs};pdfs+= [x for x in previous if x['file'] not in changed];pdfs.sort(key=lambda x:x['file'])
(R/'browser-checks.json').write_text(json.dumps(checks,indent=2)+'\n');(R/'pdf-inventory.json').write_text(json.dumps(pdfs,indent=2)+'\n');print('Exported',len(args.volumes)*2,'PDFs;',len(checks),'browser checks passed.')
