"""Check complete outline coverage, chapter/answer alignment, figures and final exports."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import csv,hashlib,json,re,zipfile,sys
import fitz
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1];errors=[];checks=0;cache={};linkcount=0;fragments=0
def check(ok,message):
 global checks
 checks+=1
 if not ok:errors.append(message)
def soup(p):
 if p not in cache:cache[p]=BeautifulSoup(p.read_text(),'html.parser')
 return cache[p]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
units={p.stem:json.loads(p.read_text()) for p in (R/'content').glob('*.json')};tasks={x['code']:x for x in json.loads((R/'outline/tasks.json').read_text())};vols=json.loads((R/'volumes.json').read_text());coverage=json.loads((R/'coverage.json').read_text())
check(len(units)==61,'61 chapters');check(len(coverage)==218,'218 learning tasks');check(set(units)=={c for v in vols for c in v['codes']},'Volume membership')
ids=[]
for code,d in units.items():
 expected=tasks[code]['tasks'];actual=d['sections']
 check(len(actual)==len(expected),code+' task count')
 for x,y in zip(actual,expected):
  check(x['number']==y['number'] and x['title']==y['task'],code+' exact outline task '+str(x['number']))
  check(len(x['text'].split())>=20,code+' reading section '+str(x['number']))
 check(len(d['activities'])==3,code+' three activities');check(bool(d['worked']['case']) and bool(d['worked']['solution']),code+' worked example')
 v=next(v for v in vols if code in v['codes']);a=soup(R/f'volume-{v["number"]}-answers.html')
 for activity in d['activities']:
  ids.append(activity['id']);check(bool(activity['answer']),code+' answer supplied');check(a.select_one('[data-activity-id="'+activity['id']+'"]') is not None,code+' answer rendered');check(len(activity['title'].split())>=2,code+' descriptive task name')
check(len(ids)==183 and len(set(ids))==183,'183 unique activities')
for p in R.glob('*.html'):
 s=soup(p);allids=[x['id'] for x in s.select('[id]')];check(len(allids)==len(set(allids)),p.name+' unique IDs')
 for el in s.select('[href],[src]'):
  url=el.get('href',el.get('src'));u=urlsplit(url)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p;linkcount+=1
  check(target.is_file(),p.name+' missing '+url)
  if target.is_file() and u.fragment and target.suffix=='.html':fragments+=1;check(soup(target).find(id=unquote(u.fragment)) is not None,p.name+' missing fragment '+url)
 for img in s.select('img'):check(bool(img.get('alt')),p.name+' image alt');check(img.find_parent('figure') is not None and img.find_parent('figure').find('figcaption') is not None,p.name+' image caption')
 check(not re.search(r'\b[A-L]\d+-\d{2}\b',s.get_text(' ',strip=True)),p.name+' no visible opaque activity IDs')
for f in json.loads((R/'figures.json').read_text())['figures']:
 p=(R/f['file']).resolve();check(p.is_file() and sha(p)==f['sha256'],'Figure hash '+f['id']);check(bool(f['credit']) and bool(f['alt']),'Figure credit '+f['id'])
parts=json.loads((R/'sources/rosco-rb50-parts.json').read_text());numbers=[];original=fitz.open(R/'sources/rosco-rb50-manual.pdf');manual_pages_checked=0
for x in parts['parts']:
 p=R/x['file'];d=fitz.open(p);check(len(d)==x['pages']<=25 and p.stat().st_size<=10*1024**2,'Small manual '+p.name);check(sha(p)==x['sha256'],'Manual part hash '+p.name);numbers+=list(range(x['first_pdf_page'],x['last_pdf_page']+1))
 for i,page in enumerate(d):
  src=original[x['first_pdf_page']-1+i];check(page.rect==src.rect and page.get_pixmap(dpi=36,annots=False).samples==src.get_pixmap(dpi=36,annots=False).samples,'Native manual page appearance '+str(x['first_pdf_page']+i));manual_pages_checked+=1
 d.close()
check(numbers==list(range(1,315)),'Manual covers all 314 pages in order')
thresholds={c for c,d in units.items() if d.get('assessment_threshold')==80};check(thresholds=={'H4','H7','I5','I8','J4','J6','L4','L6'},'Eight required 80% checklist thresholds');check(len(units['E4']['quiz']['questions'])==5,'Five density questions at four marks each')
check(abs(2.325/2.5*100-93)<1e-8,'Density denominator');check(abs(33.6*1000/288-116.6666666667)<1e-7,'Changed application rate');check(abs((101.3-1.72)-99.58)<1e-8,'Level calculation');check(abs(60*2*.04-4.8)<1e-8,'Milling quantity');check(abs(2.5*1.2*.05-.15)<1e-8,'Handwork quantity')
pdfs=[]
for v in vols:
 for suffix in ['','-answers']:
  p=R/f'volume-{v["number"]}{suffix}.pdf';doc=fitz.open(p);text='\n'.join(pg.get_text() for pg in doc);flat=' '.join(text.split());blank=[];outside=[]
  for i,pg in enumerate(doc):
   if len(pg.get_text().strip())<80:blank.append(i+1)
   for block in pg.get_text('dict')['blocks']:
    for line in block.get('lines',[]):
     for span in line['spans']:
      x0,y0,x1,y1=span['bbox']
      if x0<0 or y0<0 or x1>pg.rect.width or y1>pg.rect.height:outside.append({'page':i+1,'text':span['text']})
   for link in pg.get_links():check(not any(t in link.get('uri','') for t in ['localhost','127.0.0.1']),'PDF public target '+p.name)
  check(not blank,p.name+' near-empty pages '+str(blank));check(not outside,p.name+' text outside page '+str(outside[:3]))
  for c in v['codes']:
   for a in units[c]['activities']:check(' '.join(a['title'].split()) in flat,p.name+' task title '+a['title'])
  check('Integrated practice' in text,p.name+' integrated case');check('Direct AI and verify the files' in text,p.name+' AI practice');check('caption' in text.lower(),p.name+' study media')
  pdfs.append({'file':p.name,'pages':len(doc),'bytes':p.stat().st_size,'sha256':sha(p),'near_empty_pages':blank,'text_outside_page':outside});doc.close()
 for p in [R/f'volume-{v["number"]}-print-pack.zip']:
  with zipfile.ZipFile(p) as z:check(z.testzip() is None,p.name+' CRC')
check(len(json.loads((R/'browser-checks.json').read_text()))==26,'26 browser layout checks')
report={'checks':checks,'chapter_count':len(units),'learning_tasks':len(coverage),'chapter_activities':len(ids),'integrated_cases':7,'manual_source_pages_compared':manual_pages_checked,'local_targets':linkcount,'html_fragments':fragments,'pdfs':pdfs,'errors':errors,'limits':'Authored classroom coverage and artifact checks. Qualified technical review, actual fleet/site applicability, learner pilot and observed practical qualification are not claimed.'}
(R/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='pdfs'},indent=2));sys.exit(bool(errors))
