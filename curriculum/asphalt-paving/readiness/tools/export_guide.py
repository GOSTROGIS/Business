"""Export the illustrated preparation guide and check desktop/mobile rendering."""
from pathlib import Path
import functools,http.server,json,socketserver,threading
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[4];A=R/'curriculum/asphalt-paving/readiness'
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=socketserver.TCPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)))
threading.Thread(target=server.serve_forever,daemon=True).start();port=server.server_address[1]
base=f'http://127.0.0.1:{port}/curriculum/asphalt-paving/readiness/'
try:
 with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page();checks=[];errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    for name in ['index.html','field-guide.html','tools.html','coverage.html','gaps.html','web/ohs-15.html']:
      for width in [390,1280]:
        page.set_viewport_size({'width':width,'height':900});response=page.goto(base+name,wait_until='networkidle');assert response.ok
        page.evaluate('document.fonts.ready');page.evaluate('Promise.all([...document.images].map(i=>{i.loading="eager";return i.decode()}))')
        assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+1'),(name,width,'overflow')
        assert page.locator('h1').count()>=1
        checks.append(dict(page=name,width=width,result='passed'))
    page.goto(base+'index.html');page.fill('#query','shackle');page.click('#search-form button');assert page.locator('#results li').count()>0
    page.select_option('#category','rigging');assert page.locator('.source-card:visible').count()==3
    page.goto(base+'field-guide.html',wait_until='networkidle');page.evaluate('Promise.all([...document.images].map(i=>{i.loading="eager";return i.decode()}))')
    page.screenshot(path='/workspace/scratch/asphalt-readiness/field-guide-desktop.png',full_page=True)
    page.goto(base+'assets/handwork-anatomy.svg');page.screenshot(path='/workspace/scratch/asphalt-readiness/handwork-svg.png')
    page.goto(base+'field-guide.html',wait_until='networkidle');page.evaluate('document.fonts.ready')
    page.evaluate("""()=>document.querySelectorAll('a[href]').forEach(a=>{const u=new URL(a.href);if(u.hostname==='127.0.0.1')a.href='https://github.com/GOSTROGIS/Business/blob/main'+u.pathname+u.hash})""")
    page.pdf(path=str(A/'field-guide.pdf'),format='Letter',margin={'top':'14mm','bottom':'18mm','left':'14mm','right':'14mm'},print_background=True,tagged=True,outline=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="font:8px Arial;color:#625d58;width:100%;padding:0 14mm;display:flex;justify-content:space-between"><span>ACCESS IS4S · Tools, rigging and preparation</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    assert not errors,errors
    (A/'browser-checks.json').write_text(json.dumps(dict(status='passed',cases=checks,pdf_search='shackle returns source-page matches',category_filter='rigging: 3 publications',page_errors=errors),indent=2)+'\n')
    browser.close();print('Passed',len(checks),'page/viewport cases; exported field-guide.pdf')
finally:server.shutdown();server.server_close()
