"""Package complete publications into independent ZIP volumes below 45 MiB."""
from pathlib import Path
import hashlib,json,zipfile,io,re
from html import escape
from build_collection import html,write
R=Path(__file__).resolve().parents[1];W=R.parent/'whmis';D=json.loads((R/'manifest.json').read_text())['documents'];LIMIT=45*1048576

def add(z,name,data):
 info=zipfile.ZipInfo(name,(2026,10,30,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data)
def make_volume(docs,number):
 out=io.BytesIO()
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  add(z,'index.html',html(docs,f'CAT reference library · volume {number}',volume=True).encode())
  note=f'ACCESS IS4S · CAT reference library · volume {number}\nExtract this entire ZIP, then open index.html in a browser.\nThis volume contains {len(docs)} complete publications in small PDF parts, with extracted text and source records. Keep the folder structure. PDF viewer page numbers in each part restart at 1; each filename and card records the original source range.\nPublisher links require internet access. Local PDF/text links work offline. Original notices remain intact. Parts guides contain selected components; exact-machine operation and complete parts catalogues require model/serial confirmation.\nFull library and illustrated classroom atlas: https://github.com/GOSTROGIS/Business/tree/main/curriculum/asphalt-paving/caterpillar\n'
  add(z,'README-OFFLINE.txt',note.encode());add(z,'manifest.json',(json.dumps({'documents':docs},ensure_ascii=False,indent=2)+'\n').encode())
  files=[R/'assets/library.css',*(R/'assets/fonts').glob('*')]
  for d in docs:
   files.append(R/'records'/f'{d["slug"]}.json')
   for p in d['parts']:files.extend([R/p['file'],R/p['text']])
  for p in sorted(set(files)):
   if p.is_file():add(z,p.relative_to(R).as_posix(),p.read_bytes())
 return out.getvalue()
# Keep meaningful groupings, splitting further only if an actual ZIP exceeds the limit.
groups=[D[:1],D[1:3],D[3:9],D[9:]];ready=[]
while groups:
 docs=groups.pop(0);raw=make_volume(docs,len(ready)+1)
 if len(raw)>LIMIT:
  assert len(docs)>1,'A complete publication exceeds the volume limit';mid=len(docs)//2;groups=[docs[:mid],docs[mid:]]+groups;continue
 ready.append((docs,raw))
records=[]
for i,(docs,raw) in enumerate(ready,1):
 p=R/'downloads'/f'cat-library-volume-{i:02d}.zip';p.parent.mkdir(exist_ok=True);p.write_bytes(raw)
 with zipfile.ZipFile(p) as z:assert z.testzip() is None;members=len(z.namelist())
 records.append(dict(file=p.relative_to(R).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),documents=[d['id'] for d in docs],source_pages=sum(d['original_pages'] for d in docs),members=members))
# WHMIS pack includes its own complete classroom pages, artwork and source PDFs.
out=io.BytesIO()
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(W.rglob('*')):
  if not p.is_file() or 'tools' in p.relative_to(W).parts or p.name in ['whmis-classroom-pack.zip','download.json']:continue
  raw=p.read_bytes()
  if p.suffix=='.html':
   t=raw.decode();t=re.sub(r'(href=")\.\./caterpillar/([^"\s]+)',r'\1https://github.com/GOSTROGIS/Business/blob/main/curriculum/asphalt-paving/caterpillar/\2',t);t=t.replace('<a href="whmis-classroom-pack.zip">Download ZIP</a>','<a href="README-OFFLINE.txt">Offline instructions</a>');raw=t.encode()
  elif p.name=='README.md':raw=raw.replace(b'[Complete classroom ZIP](whmis-classroom-pack.zip)',b'[Offline instructions](README-OFFLINE.txt)').replace(b'../caterpillar/',b'https://github.com/GOSTROGIS/Business/blob/main/curriculum/asphalt-paving/caterpillar/')
  add(z,p.relative_to(W).as_posix(),raw)
 add(z,'README-OFFLINE.txt',b'ACCESS IS4S WHMIS classroom pack\nExtract the entire ZIP. Open index.html. All WHMIS pages, artwork, source PDFs and classroom PDFs are local. External source links and CAT library links require internet access. Printed PDF links point to the repository. The two WorkSafeBC books are historical 2019 editions; the five CCOHS sheets are revised 28 May 2026. Workplace-specific training is also required.\n')
raw=out.getvalue();(W/'whmis-classroom-pack.zip').write_bytes(raw)
with zipfile.ZipFile(io.BytesIO(raw)) as z:assert z.testzip() is None;members=len(z.namelist())
whmis=dict(file='whmis-classroom-pack.zip',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),members=members)
write(W/'download.json',json.dumps(whmis,indent=2)+'\n');write(R/'downloads/manifest.json',json.dumps({'max_volume_bytes':LIMIT,'volumes':records},indent=2)+'\n')
content='<p><a href="index.html">CAT library</a> · <a href="parts-atlas.html">Parts atlas</a> · <a href="../whmis/index.html">WHMIS</a></p><h1>Download the reference library</h1><p>Each ZIP is below 45 MiB. Extract a whole volume and open its index.html. Each included publication is complete across its PDF parts; a publication is never divided between ZIP volumes.</p>'
for i,v in enumerate(records,1):
 names='; '.join(d['title'] for d in D if d['id'] in v['documents']);content+=f'<section class="document"><p class="tag">VOLUME {i:02d} · {v["source_pages"]} SOURCE PAGES</p><h2><a href="{v["file"]}">Download ZIP · {v["bytes"]/1048576:.1f} MiB</a></h2><p>{escape(names)}</p><p class="small">SHA-256: <code style="overflow-wrap:anywhere">{v["sha256"]}</code></p></section>'
content+=f'<section class="document"><h2>WHMIS classroom pack</h2><p><a href="../whmis/whmis-classroom-pack.zip">Download ZIP · {whmis["bytes"]/1048576:.1f} MiB</a></p><p>Official symbols in three formats, seven source PDFs, reference book, six practice tasks and answer guidance, plus complete CAT warning-page images.</p></section><section class="document"><h2>Print the machine-identification books</h2><p><a href="parts-atlas.pdf">Parts atlas</a> · <a href="practice.pdf">Ten learner tasks</a> · <a href="teaching-guide.pdf">Teaching and answer guide</a></p></section><p><a href="downloads/manifest.json">ZIP sizes, hashes and publication membership</a> · <a href="../whmis/download.json">WHMIS ZIP record</a></p>'
write(R/'downloads.html','<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CAT and WHMIS downloads | ACCESS IS4S</title><link rel="stylesheet" href="assets/library.css"></head><body><main>'+content+'</main></body></html>')
print(json.dumps({'cat_volumes':records,'whmis':whmis},indent=2))
