"""Check all original SVG text bounds and intersections in the browser renderer."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,shutil
R=Path(__file__).resolve().parents[1];results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True);pg=b.new_page()
 for f in sorted((R/'assets').glob('*.svg')):
  pg.set_content(f.read_text());result=pg.evaluate('''() => {const svg=document.querySelector('svg'),v=svg.viewBox.baseVal;const texts=[...svg.querySelectorAll('text')].map(e=>{let b=e.getBBox();return {text:e.textContent,x:b.x,y:b.y,w:b.width,h:b.height};});const outside=texts.filter(b=>b.x<0||b.y<0||b.x+b.w>v.width||b.y+b.h>v.height);const overlaps=[];for(let i=0;i<texts.length;i++)for(let j=i+1;j<texts.length;j++){let a=texts[i],b=texts[j];if(Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>2&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>2)overlaps.push([a.text,b.text]);}return {text_nodes:texts.length,outside,overlaps};}''');results.append({'file':f.name,**result})
 b.close()
(R/'diagram-checks.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(not x['outside'] and not x['overlaps'] for x in results),results
print('Passed all',len(results),'SVG text-layout checks.')
