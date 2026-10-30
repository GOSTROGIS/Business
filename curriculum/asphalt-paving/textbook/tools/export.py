"""Capture the actual plan desk, export printable books and exercise the interface."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
from urllib.parse import urlsplit,unquote
import argparse,json,shutil,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];REPO=R.parents[2]
sys.path.insert(0,str(R.parent/'tools'))
from build_line_a import public_pdf_links
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
parser=argparse.ArgumentParser();parser.add_argument('--desk-only',action='store_true');args=parser.parse_args()
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(REPO)));Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'+str(R.relative_to(REPO))+'/'
checks=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True)
  page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
  page.goto(base+'plan-desk.html',wait_until='networkidle');page.evaluate('document.fonts.ready')
  page.locator('#learning-desk').screenshot(path=str(R/'assets/plan-desk-screen.png'))
  if args.desk_only:print('Captured plan desk screenshot.');browser.close();sys.exit(0)
  for width in [390,1280]:
   page.set_viewport_size({'width':width,'height':900})
   for name in ['index.html','01-industry-evidence.html','03-technology.html','05-road-documents.html','07-safe-work.html','plan-desk.html','study-textbook.html','answers.html']:
    errors=[];listener=lambda e:errors.append(str(e));page.on('pageerror',listener)
    page.goto(base+name,wait_until='networkidle');page.evaluate('document.fonts.ready')
    bad=page.evaluate('''() => ({overflow:document.documentElement.scrollWidth>innerWidth+1,images:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src),duplicateIds:[...document.querySelectorAll('[id]')].map(e=>e.id).filter((id,i,a)=>a.indexOf(id)!==i)})''')
    checks.append({'file':name,'width':width,**bad,'page_errors':errors});page.remove_listener('pageerror',listener)
    assert not bad['overflow'] and not bad['images'] and not bad['duplicateIds'] and not errors,(name,width,bad,errors)
  # Behaviour, download contents and offline reload. Text remains text in the exported file.
  page.goto(base+'plan-desk.html',wait_until='networkidle')
  page.locator('#revision').select_option('C');assert '28.80' in page.locator('#math-result').inner_text()
  page.locator('[data-record="utility"]').click();assert 'unverified' in page.locator('#record-fields').inner_text()
  page.locator('[data-layer="utility"]').uncheck();assert page.locator('#layer-utility').evaluate('e=>getComputedStyle(e).display')=='none'
  page.locator('#note').fill('Utility alignment is unverified. <script>study text</script>')
  with page.expect_download() as info:page.locator('#export').click()
  dl=info.value;data=json.loads(Path(dl.path()).read_text());assert data['drawing']['revision']=='C' and abs(data['drawing']['volume_m3']-14.4)<1e-9 and data['selected_record']=='utility' and data['visible_layers']['utility']==False and '<script>' in data['learner_note']
  page.route('**/*',lambda route: route.continue_() if urlsplit(route.request.url).hostname=='127.0.0.1' else route.abort())
  page.goto(base+'plan-desk.html',wait_until='networkidle');page.locator('#revision').select_option('C');assert '28.80' in page.locator('#math-result').inner_text()
  checks.append({'test':'revision C, selected record, hidden utility, exported/reopened JSON and local-server load with external network blocked','passed':True})
  page.set_viewport_size({'width':1280,'height':1000})
  for stem in ['study-textbook','answers']:
   page.goto(base+stem+'.html',wait_until='networkidle');page.evaluate('document.fonts.ready')
   page.evaluate("async()=>{for(const i of document.images)i.loading='eager';await Promise.all([...document.images].map(i=>i.decode()));}")
   page.pdf(path=str(R/(stem+'.pdf')),format='A4',print_background=True,prefer_css_page_size=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="width:100%;font-size:8px;text-align:center;color:#625d58">ACCESS IS4S · Asphalt study textbook · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
   public_pdf_links(R/(stem+'.pdf'))
  browser.close()
 (R/'browser-checks.json').write_text(json.dumps(checks,indent=2)+'\n');print('Exported two PDFs;',len(checks),'browser/interaction checks passed.')
finally:server.shutdown()
