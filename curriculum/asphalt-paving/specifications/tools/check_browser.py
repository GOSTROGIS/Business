"""Check five reading pages at phone, tablet and desktop widths using local Chromium."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
import json,os,shutil
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];repo=root.parents[2];errors=[];checks=0
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(repo)));thread=Thread(target=server.serve_forever,daemon=True);thread.start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path=os.environ.get('IS4S_CHROMIUM_PATH') or shutil.which('chromium'))
  page=browser.new_page();bad=[];page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
  for width in [375,768,1280]:
   page.set_viewport_size({'width':width,'height':1000})
   for stem in ['index','learner-workbook','teaching-guide','source-map','source-excerpts']:
    response=page.goto(f'http://127.0.0.1:{server.server_port}/curriculum/asphalt-paving/specifications/{stem}.html',wait_until='networkidle');page.evaluate('document.fonts.ready')
    facts=page.evaluate('''() => ({overflow:document.documentElement.scrollWidth>innerWidth+1,images:Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0),alt:Array.from(document.images).every(i=>i.alt.trim()),headings:document.querySelectorAll('h1').length===1})''')
    for key,value in facts.items():
     checks+=1
     failed=value if key=='overflow' else not value
     if failed:errors.append(f'{stem}@{width}: {key}={value}')
  browser.close()
 checks+=1
 if bad:errors.append({'http_errors':bad})
finally:server.shutdown();thread.join()
report={'checks':checks,'errors':errors,'status':'passed' if not errors else 'failed','widths':[375,768,1280],'html_pages':5}
(root/'browser-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
raise SystemExit(bool(errors))
