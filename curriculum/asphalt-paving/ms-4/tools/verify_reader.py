"""Verify complete MS-4 coverage, source fidelity, lesson evidence and browser behaviour.

Run from any directory. Add --browser for local Chromium checks; --original PATH
compares every native part page against the acquired original at 36 dpi.
"""
from __future__ import annotations
import argparse, hashlib, json, re, xml.etree.ElementTree as ET
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import unquote, urlsplit
import fitz
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]
checks=0

def check(condition, message):
 global checks
 if not condition: raise AssertionError(message)
 checks+=1

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

class Page(HTMLParser):
 def __init__(self, path):
  super().__init__(); self.ids=[];self.links=[];self.images=[];self.feed(path.read_text())
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for key in ['href','src']:
   if key in a:self.links.append(a[key])
  if tag=='img':self.images.append(a)


def inventory(original):
 m=json.loads((ROOT/'manifest.json').read_text());parts=json.loads((ROOT/'source-parts.json').read_text())
 check(m['pdf_pages']==834 and m['year']==2007 and m['isbn']=='978-1-934154-27-4','Source identity')
 check(parts['original_sha256']==m['source_sha256'] and parts['original_bytes']==180202618,'Original fingerprint')
 check(len(m['pages'])==834 and len(m['html_sections'])==62 and len(parts['parts'])==34,'Collection extent')
 chapters=[s for s in m['sections'] if s['chapter']]
 check([s['pdf_start'] for s in chapters]==[35,55,143,193,281,315,341,391,447,479,553,603,653,711,737],'Verified chapter boundaries')
 check([n for s in m['sections'] for n in range(s['pdf_start'],s['pdf_end']+1)]==list(range(1,835)),'Contents include all source pages')
 check([n for s in m['html_sections'] for n in range(s['start'],s['end']+1)]==list(range(1,835)),'HTML coverage without gaps or repeats')
 check(all(s['end']-s['start']<16 for s in m['html_sections']),'HTML reading-section limit')
 raw=(ROOT/'assets/search-index.js').read_text();search=json.loads(raw.removeprefix('window.MS4_SEARCH=').removesuffix(';\n'))
 check([r['page'] for r in search]==list(range(1,835)),'Full-book search inventory')
 words=0
 for n,r in enumerate(m['pages'],1):
  d=json.loads((ROOT/'data'/f'p{n:04d}.json').read_text())
  check(r['pdf_page']==n and d['pdf_page']==n and d['source_sha256']==m['source_sha256'],f'Page identity {n}')
  for name in ['text','image','effective_text']:
   check(sha(ROOT/r[name])==r[name+'_sha256'],f'Page {n} {name} integrity')
  check(r['text_sha256']==d['text_sha256'] and r['image_sha256']==d['image_sha256'],f'Raw extraction unchanged {n}')
  check(search[n-1]['text']==(ROOT/r['effective_text']).read_text() and search[n-1]['href']==m['page_locations'][str(n)],f'Search/text location {n}')
  check(r['editorial_override']==(ROOT/'edits'/f'p{n:04d}.txt').exists(),f'Editorial override {n}')
  words+=d['word_count']
 check(words==244217==m['word_count'],'Raw OCR count')
 check(not (ROOT/'text/p0001.txt').read_text() and 'Asphalt' in search[0]['text'],'Cover correction preserves original OCR')
 covered=[];renders=0;source=None
 if original:
  source=fitz.open(original)
  check(sha(original)==m['source_sha256'] and len(source)==834,'Acquired original integrity')
 for part in parts['parts']:
  path=ROOT/part['file'];pdf=fitz.open(path)
  check(sha(path)==part['sha256'] and path.stat().st_size==part['bytes'],f'Part integrity {path.name}')
  check(len(pdf)==part['pages']==part['pdf_end']-part['pdf_start']+1 and len(pdf)<=25,'Part page range')
  check(part['bytes']<=12*1024*1024,'Part size limit')
  covered.extend(range(part['pdf_start'],part['pdf_end']+1))
  for i,page in enumerate(pdf):
   check(not page.get_links(),f'Image-only source has no page-link annotations: {path.name}/{i+1}')
   if source:
    original_page=source[part['pdf_start']+i-1]
    a=page.get_pixmap(matrix=fitz.Matrix(.5,.5),annots=False)
    b=original_page.get_pixmap(matrix=fitz.Matrix(.5,.5),annots=False)
    check(page.rect==original_page.rect and a.width==b.width and a.height==b.height and a.samples==b.samples,f'Original versus part render: {part["pdf_start"]+i}')
    renders+=1
  pdf.close()
 check(covered==list(range(1,835)),'Native parts preserve every original page in order')
 if source:source.close()
 return m, renders


def documents(m):
 paths=[ROOT/'index.html',*(ROOT/'reader').glob('*.html'),*(ROOT/'concepts').glob('*.html')]
 parsed={p.resolve():Page(p) for p in paths};pdf_counts={};anchors=[]
 for path,page in parsed.items():
  check(len(page.ids)==len(set(page.ids)),f'Unique HTML IDs {path.name}')
  anchors.extend(int(x[5:]) for x in page.ids if re.fullmatch(r'page-\d{4}',x))
  for im in page.images:check(bool(im.get('alt','').strip()),f'Image text alternative {path.name}')
  for link in page.links:
   u=urlsplit(link)
   if u.scheme or u.netloc:continue
   target=(path.parent/unquote(u.path)).resolve() if u.path else path
   check(target.is_file(),f'Missing local asset {path.name}: {link}')
   if u.fragment and target.suffix=='.html':
    if target not in parsed:parsed_target=Page(target)
    else:parsed_target=parsed[target]
    check(unquote(u.fragment) in parsed_target.ids,f'Missing HTML anchor {path.name}: {link}')
   if u.fragment.startswith('page=') and target.suffix=='.pdf':
    if target not in pdf_counts:
     with fitz.open(target) as pdf:pdf_counts[target]=len(pdf)
    check(1<=int(u.fragment[5:])<=pdf_counts[target],f'PDF page destination {link}')
 check(sorted(anchors)==list(range(1,835)),'Exactly one displayed article per source page')
 for n,location in m['page_locations'].items():
  u=urlsplit(location);check(f'page-{int(n):04d}' in parsed[(ROOT/u.path).resolve()].ids,'Page location index')
 # Check local CSS/font URLs, which HTML links alone do not cover.
 for css in [ROOT/'assets/reader.css']:
  for match in re.findall(r'url\([\'\"]?([^\)\'\"]+)',css.read_text()):check((css.parent/match).is_file(),f'CSS asset {match}')
 figures=json.loads((ROOT/'concepts/figure-manifest.json').read_text())['figures']
 check(len(figures)==6,'Six instructional redraws')
 expected={'load-spread':47,'pavement-layers':48,'plant-processes':344,'paver-material-route':411,'screed-factors':417,'pass-and-coverage':450}
 for f in figures:
  p=ROOT/'concepts'/f['file'];svg=ET.parse(p).getroot()
  check(sha(p)==f['asset_sha256'] and f['source_sha256']==m['source_sha256'],'Figure source/asset integrity')
  check(svg.tag.endswith('svg') and svg.attrib.get('viewBox')=='0 0 1200 800','SVG drawing coordinates')
  check(f['references'][0]['pdf_page']==expected[f['id']],f'Verified figure source {f["id"]}')
  check(bool(f['alt']) and bool(f['adaptation']),'Figure accessibility and adaptation record')
  for c in f['original_contributors']:check(c['credit_pdf_page'] in [803,804,805] and c['credit'],'Original contributor credit')
 learner=(ROOT/'concepts/learner.md').read_text();teacher=(ROOT/'concepts/instructor.md').read_text()
 ids=[f'MS4-{n:02d}' for n in range(1,13)]
 for text in [learner,teacher]:check(re.findall(r'^### (MS4-\d{2})',text,re.M)==ids,'Twelve ordered activities and full keys')
 for word in ['Reading','Writing','Numeracy','Digital','Problem solving','Communication','Collaboration','Adaptability','Creativity and innovation']:
  check(word.lower() in learner.lower() and word.lower() in teacher.lower(),f'Nine-skills lesson evidence: {word}')
 check(50+120+180==350 and '350' in teacher and '0.350' in teacher,'Fictional layer model key with units')
 for name in ['learner-workbook','teaching-guide']:
  with fitz.open(ROOT/'concepts'/f'{name}.pdf') as pdf:
   check(len(pdf)>1,f'Complete {name} PDF')
   for page in pdf:
    check(len(page.get_text().strip())>40,f'Readable {name} PDF page {page.number+1}')
    for link in page.get_links():check(not any(s in link.get('uri','') for s in ['127.0.0.1','localhost','file://']),f'Portable PDF link {name}')
    for block in page.get_text('dict')['blocks']:
     if block['type']!=0:continue
     for line in block['lines']:
      for span in line['spans']:
       x0,y0,x1,y1=span['bbox'];check(x0>=-1 and y0>=-1 and x1<=page.rect.width+1 and y1<=page.rect.height+1,f'Unclipped PDF text {name}/{page.number+1}')
 return len(paths)


def browser_checks(m):
 from playwright.sync_api import sync_playwright
 class Quiet(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(REPO)))
 Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
 prefix=ROOT.relative_to(REPO).as_posix()+'/';cases=0;errors=[];failures=[]
 try:
  with sync_playwright() as p:
   b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page()
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('requestfailed',lambda r:failures.append(r.url))
   chosen=['index.html','concepts/index.html','concepts/teaching-guide.html',*[m['page_locations'][str(n)].split('#')[0] for n in [1,344,411,450,804]],'../line-a/03-technology.html','../line-a/05-road-documents.html']
   for width in [320,390,1280]:
    page.set_viewport_size({'width':width,'height':900})
    for rel in chosen:
     response=page.goto(base+prefix+rel,wait_until='networkidle');page.evaluate('document.fonts.ready')
     check(response.status==200,f'Browser document {rel}')
     check(page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),f'Mobile overflow {width}: {rel}')
     check(page.locator('img:not([loading="lazy"])').evaluate_all('(els)=>els.every(e=>e.complete&&e.naturalWidth>0)'),f'Figure load {width}: {rel}')
     check(page.locator('img:not([loading="lazy"])').evaluate_all('(els)=>els.every(e=>{const r=e.getBoundingClientRect();return !r.width || ["contain","scale-down"].includes(getComputedStyle(e).objectFit) || Math.abs(r.width/r.height-e.naturalWidth/e.naturalHeight)<0.015})'),f'Undistorted images {width}: {rel}')
     check(page.evaluate('document.fonts.check("17px Plex")'),f'Bundled font {rel}')
     cases+=1
   page.goto(base+prefix+'index.html',wait_until='networkidle')
   page.locator('#search').fill('screed');page.locator('#search').press('Enter')
   check(page.locator('#results li').count()>0,'Full-book keyword search')
   check('matching pages' in page.locator('#search-status').inner_text(),'Announced search count')
   result=page.locator('#results a').first.get_attribute('href');check('#page-' in result,'Search links directly to source page')
   page.locator('#search').fill('zzzxxyy-no-such-term');page.locator('#search').press('Enter')
   check(page.locator('#results li').count()==0 and '0 matching' in page.locator('#search-status').inner_text(),'No-results feedback')
   page.locator('#clear-search').click();check(page.locator('#search').input_value()=='' and page.locator('#search').evaluate('(e)=>e===document.activeElement'),'Clear and keyboard focus')
   rel=m['page_locations']['411'].split('#')[0];page.goto(base+prefix+rel,wait_until='networkidle')
   page.locator('[data-mode="text"]').click();check(page.locator('.scan').first.is_hidden() and page.locator('.transcript').first.is_visible(),'Text reading mode')
   page.locator('[data-mode="scan"]').click();check(page.locator('.transcript').first.is_hidden() and page.locator('.scan').first.is_visible(),'Scan reading mode')
   page.locator('[data-mode="both"]').click();check(page.locator('.transcript').first.is_visible() and page.locator('.scan').first.is_visible(),'Combined reading mode')
   page.select_option('#page-jump','page-0411');check(page.url.endswith('#page-0411'),'Source page jump')
   check(page.locator('.pager a').filter(has_text='Previous section').count()==2 and page.locator('.pager a').filter(has_text='Next section').count()==2,'Section navigation at both ends')
   check(not errors,'Browser script errors: '+str(errors));check(not failures,'Failed browser requests: '+str(failures))
   b.close()
 finally:server.shutdown();server.server_close()
 return cases


def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--original',type=Path);parser.add_argument('--browser',action='store_true');a=parser.parse_args()
 m,renders=inventory(a.original);pages=documents(m);cases=browser_checks(m) if a.browser else 0
 print(json.dumps({'status':'passed','assertions':checks,'source_pages':834,'html_documents_checked':pages,'source_page_render_comparisons':renders,'browser_viewport_cases':cases,'ocr_status':'Unproofread machine transcription; source scans preserved.'},indent=2))
if __name__=='__main__':main()
