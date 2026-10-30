"""Check generated books, source identities, activity coverage and local navigation."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from collections import Counter
import json,re,hashlib,sys
from bs4 import BeautifulSoup
import fitz
R=Path(__file__).resolve().parents[1];REPO=R.parents[2]
errors=[];links=0;fragments=0;cache={}
def check(ok,message):
 if not ok:errors.append(message)
def soup_for(p):
 if p not in cache:cache[p]=BeautifulSoup(p.read_text(),'html.parser')
 return cache[p]
for path in sorted(R.glob('*.html')):
 soup=soup_for(path);check('@@' not in path.read_text(),f'Unresolved placeholder: {path.name}')
 for el in soup.select('[href],[src]'):
  url=el.get('href',el.get('src'));u=urlsplit(url)
  if u.scheme or u.netloc or not u.path:continue
  target=(path.parent/unquote(u.path)).resolve();links+=1
  check(target.is_file(),f'{path.name}: missing {url}')
  if target.is_file() and u.fragment and target.suffix=='.html':
   fragments+=1;check(soup_for(target).find(id=unquote(u.fragment)) is not None,f'{path.name}: missing fragment {url}')
for f in json.loads((R/'figures.json').read_text())['figures']:
 p=(R/f['file']).resolve();check(p.is_file(),f'Missing figure {f["id"]}')
 if p.is_file():check(hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],f'Figure hash {f["id"]}')
 check(bool(f['alt']) and bool(f['credit']),f'Missing credit/alt {f["id"]}')
for r in json.loads((R/'provenance/consulting.json').read_text())['records']:
 data=(R/r['local_file']).read_bytes();check(hashlib.sha256(data).hexdigest()==r['sha256'],'CONSULTING file hash '+r['path']);check(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==r['git_blob_sha'],'CONSULTING Git blob '+r['path'])
book=soup_for(R/'study-textbook.html');images=book.select('img')
for img in images:
 fig=img.find_parent('figure');check(bool(img.get('alt')),f'Missing image alt {img["src"]}');check(fig is not None and fig.find('figcaption') is not None,f'Missing caption {img["src"]}')
ids=re.findall(r'^### ((?:LA\d|TB\d)-\d\d)\b','\n'.join(p.read_text() for p in sorted(R.glob('0[1-7]-*.md'))),re.M)
check(len(ids)==len(set(ids)),'Duplicate activity identifiers')
answer=soup_for(R/'answers.html').get_text(' ')
for id in ids:check(id in answer,f'Missing answer {id}')
pdfs=[]
for name in ['study-textbook','answers']:
 p=R/(name+'.pdf');doc=fitz.open(p);text='\n'.join(pg.get_text() for pg in doc)
 blank=[];outside=[]
 for i,pg in enumerate(doc):
  if len(pg.get_text().strip())<90:blank.append(i+1)
  for block in pg.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    for span in line['spans']:
     x0,y0,x1,y1=span['bbox']
     if x0<1 or y0<1 or x1>pg.rect.width-1 or y1>pg.rect.height-1:outside.append({'page':i+1,'text':span['text'],'bbox':span['bbox']})
  for l in pg.get_links():
   if l.get('uri'):check('127.0.0.1' not in l['uri'] and 'localhost' not in l['uri'],f'Localhost PDF link {name}')
 check(not blank,f'{name}: near-empty pages {blank}');check(not outside,f'{name}: text outside page {outside[:5]}')
 for id in ids:check(id in text,f'{name}: activity missing in extracted PDF text {id}')
 pdfs.append({'file':p.name,'pages':len(doc),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'near_empty_pages':blank,'text_outside_page':outside})
check(len(json.loads((R/'browser-checks.json').read_text()))==17,'Browser checks absent')
result={'local_targets_checked':links,'html_fragments_checked':fragments,'activity_count':len(ids),'new_activities':len([x for x in ids if x.startswith('TB')]),'image_placements':len(images),'unique_image_files':len({x['src'] for x in images}),'original_new_svgs':len(list((R/'assets').glob('*.svg'))),'pinned_consulting_documents':5,'pdfs':pdfs,'errors':errors}
(R/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(bool(errors))
