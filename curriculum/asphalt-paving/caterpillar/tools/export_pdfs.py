"""Export classroom HTML through a temporary local HTTP server and Chromium."""
from pathlib import Path
import http.server,socketserver,threading,functools,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[4]
A=R/'curriculum/asphalt-paving'
handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(R))
class Quiet(handler.func):
 def log_message(self,*args):pass
handler=functools.partial(Quiet,directory=str(R))
server=socketserver.TCPServer(('127.0.0.1',0),handler);threading.Thread(target=server.serve_forever,daemon=True).start();port=server.server_address[1]
pages={'caterpillar/parts-atlas.html':'caterpillar/parts-atlas.pdf','caterpillar/practice.html':'caterpillar/practice.pdf','caterpillar/teaching-guide.html':'caterpillar/teaching-guide.pdf','whmis/index.html':'whmis/whmis-reference.pdf','whmis/practice.html':'whmis/practice.pdf','whmis/teaching-guide.html':'whmis/teaching-guide.pdf'}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page()
  for html,pdf in pages.items():
   page.goto(f'http://127.0.0.1:{port}/curriculum/asphalt-paving/{html}',wait_until='networkidle');page.evaluate('document.fonts.ready');page.evaluate("Promise.all([...document.images].map(i=>i.decode()))")
   # PDF local links must remain useful after a download: point to repository files.
   page.evaluate("""()=>{document.querySelectorAll('a[href]').forEach(a=>{const u=new URL(a.href);if(u.hostname==='127.0.0.1')a.href='https://github.com/GOSTROGIS/Business/blob/main'+u.pathname+u.hash})}""")
   page.pdf(path=str(A/pdf),prefer_css_page_size=True,print_background=True,tagged=True,outline=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="width:100%;font:8px Arial;color:#625D58;padding:0 13mm;display:flex;justify-content:space-between"><span>ACCESS IS4S · Asphalt · 30 October 2026</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
   print(pdf,flush=True)
  browser.close()
finally:server.shutdown();server.server_close()
