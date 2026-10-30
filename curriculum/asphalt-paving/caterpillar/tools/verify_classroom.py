"""Check local navigation, source asset integrity, print content and browser behaviour."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import csv,hashlib,json,re,zipfile,xml.etree.ElementTree as ET,fitz
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R.parent/'whmis';m=json.loads((R/'manifest.json').read_text());a=json.loads((R/'atlas.json').read_text());h=json.loads((W/'manifest.json').read_text());links=0
class Links(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.add(d['id'])
  for k in ['href','src']:
   if k in d:self.refs.append(d[k])
for root in [R,W]:
 for p in root.glob('*.html'):
  parser=Links();parser.feed(p.read_text())
  for raw in parser.refs:
   u=urlsplit(raw)
   if u.scheme or u.netloc:continue
   path=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve();assert path.exists(),(p,raw);links+=1
   if u.fragment and path.suffix=='.pdf' and u.fragment.startswith('page='):
    with fitz.open(path) as doc:assert 1<=int(u.fragment[5:])<=len(doc)
   elif u.fragment and path.suffix=='.html':
    other=Links();other.feed(path.read_text());assert unquote(u.fragment) in other.ids,(p,raw)
assert len(a['figures'])==20 and sum(len(f['components']) for f in a['figures'])==89
assert len(list(csv.DictReader((R/'component-register.csv').open())))==89
for f in a['figures']:
 assert hashlib.sha256((R/f['file']).read_bytes()).hexdigest()==f['sha256']
 doc=next(d for d in m['documents'] if d['id']==f['document']);assert f['source_sha256']==doc['original_sha256'] and 1<=f['source_page']<=doc['original_pages']
for id,expected in [('milling-conveyor',set(map(str,range(1,8)))),('milling-undercarriage',set(map(str,range(1,7)))),('roller-controls',set(map(str,range(1,20)))),('loader-linkage',{'A','B','C','D','E','F','G','K','Y','S1','S2'})]:assert {c['locator'] for c in next(f for f in a['figures'] if f['id']==id)['components']}==expected
for d in h['documents']:
 raw=(W/d['file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==d['sha256'];assert len(fitz.open(stream=raw,filetype='pdf'))==d['pages']
with zipfile.ZipFile(W/h['pictogram_kit']['file']) as z:
 for p in h['pictograms']:
  for fmt,record in p['files'].items():
   raw=(W/record['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==record['sha256']
   if fmt in ['png','eps']:
    matching=[n for n in z.namelist() if not n.startswith('__MACOSX') and n.rsplit('/',1)[-1]==p['id']+'.'+fmt];assert len(matching)==1;assert raw==z.read(matching[0])
   else:
    node=ET.fromstring(raw);assert node.tag.endswith('svg') and not any(n.tag.endswith('script') for n in node.iter())
assert sum(p['part_of_whmis_pictogram_set'] for p in h['pictograms'])==9
vols=json.loads((R/'downloads/manifest.json').read_text());ids=[]
for v in vols['volumes']:
 raw=(R/v['file']).read_bytes();assert len(raw)==v['bytes']<45*1048576;assert hashlib.sha256(raw).hexdigest()==v['sha256'];ids+=v['documents']
 with zipfile.ZipFile(R/v['file']) as z:
  assert z.testzip() is None;names=set(z.namelist());record=json.loads(z.read('manifest.json'))
  parser=Links();parser.feed(z.read('index.html').decode())
  for link in parser.refs:
   u=urlsplit(link)
   if not u.scheme and u.path:assert u.path in names,(v['file'],link)
  for d in record['documents']:
   for part in d['parts']:
    assert z.read(part['file'])==(R/part['file']).read_bytes();assert z.read(part['text'])==(R/part['text']).read_bytes()
assert len(ids)==len(set(ids))==22
with zipfile.ZipFile(W/'whmis-classroom-pack.zip') as z:
 assert z.testzip() is None;names=set(z.namelist())
 for name in names:
  if not name.endswith('.html'):continue
  parser=Links();parser.feed(z.read(name).decode())
  for link in parser.refs:
   u=urlsplit(link)
   if not u.scheme and u.path:assert u.path in names,(name,link)
books={}
for root in [R,W]:
 for path in root.glob('*.pdf'):
  doc=fitz.open(path);text='\n'.join(p.get_text() for p in doc);assert len(text)>300
  for page in doc:
   assert page.get_text().strip()
   for l in page.get_links():assert '127.0.0.1' not in l.get('uri','')
  books[str(path.relative_to(R.parent))]=len(doc)
# Requires the repository served at http://127.0.0.1:8765.
base='http://127.0.0.1:8765/curriculum/asphalt-paving/';cases=0
pages=['caterpillar/index.html','caterpillar/parts-atlas.html','caterpillar/practice.html','caterpillar/teaching-guide.html','caterpillar/downloads.html','whmis/index.html','whmis/practice.html','whmis/teaching-guide.html']
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in [320,390,1280]:
  tab=browser.new_page(viewport={'width':width,'height':900});errors=[];tab.on('pageerror',lambda e:errors.append(str(e)))
  for path in pages:
   tab.goto(base+path,wait_until='networkidle');tab.evaluate('document.fonts.ready');assert not errors,errors
   assert tab.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(path,width,'overflow')
   assert tab.evaluate('[...document.images].every(i=>i.complete&&i.naturalWidth>0)'),(path,width,'image')
   assert tab.evaluate('document.fonts.check("17px Plex")'),(path,width,'font')
   cases+=1
  tab.close()
 tab=browser.new_page();tab.goto(base+'caterpillar/parts-atlas.html');tab.fill('#part-filter','tail pulley');assert tab.locator('.atlas-card:visible').count()==1;assert tab.locator('#milling-conveyor').is_visible();tab.fill('#part-filter','unfindablexyz');assert tab.locator('.atlas-card:visible').count()==0
 tab.goto(base+'caterpillar/index.html');tab.fill('#query','tail pulley');tab.locator('#search-form button').first.click();assert tab.locator('#results li').count()>0;assert 'page=25' in tab.locator('#results a').first.get_attribute('href') or tab.locator('#results li').count()>1
 browser.close()
print(json.dumps(dict(status='passed',local_links=links,browser_cases=cases,atlas_figures=20,component_rows=89,official_pictograms=10,cat_zip_volumes=len(vols['volumes']),cat_source_pages=1883,whmis_source_pages=sum(d['pages'] for d in h['documents']),books=books),indent=2))
