from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];out=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1000,'height':700})
 for p in sorted((R/'assets/diagrams').glob('*.svg')):
  page.set_content(p.read_text());x=page.evaluate('''() => {const s=document.querySelector('svg'),v=s.viewBox.baseVal;let ts=[...s.querySelectorAll('text')].map(t=>{let b=t.getBBox();return {text:t.textContent,x:b.x,y:b.y,w:b.width,h:b.height}});let overlap=[];for(let i=0;i<ts.length;i++)for(let j=i+1;j<ts.length;j++){let a=ts[i],b=ts[j];if(Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>2 && Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>2)overlap.push([a.text,b.text]);}return {outside:ts.filter(b=>b.x<0||b.y<0||b.x+b.w>v.width||b.y+b.h>v.height),overlap}}''');out.append({'file':p.name,**x})
 b.close()
(R/'diagram-checks.json').write_text(json.dumps(out,indent=2)+'\n');bad=[x for x in out if x['outside'] or x['overlap']];print(json.dumps(bad,indent=2));print(len(out),'diagrams;',len(bad),'with issues');raise SystemExit(bool(bad))
