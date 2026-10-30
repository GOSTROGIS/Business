"""Preserve every CAT source page in small native PDF parts and a searchable index.
Run with --downloads PATH containing catalogue download filenames. Source hashes
are pinned; a changed download must be reviewed before updating catalogue.json.
"""
from pathlib import Path
from html import escape
import argparse,hashlib,json,shutil,fitz,io
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ArrayObject,NameObject
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
CSS="""@font-face{font-family:Plex;src:url('fonts/ibm-plex-sans-latin-400-normal.woff2')}@font-face{font-family:Plex;src:url('fonts/ibm-plex-sans-latin-600-normal.woff2');font-weight:600}*{box-sizing:border-box}body{margin:0;background:#F7F4F1;color:#1A1512;font:17px/1.6 Plex,Arial,sans-serif}header{background:#1A1512;color:white;border-bottom:6px solid #FFBC00;padding:38px 24px}header>div,main{max-width:1160px;margin:auto}header p{color:#FFBC00}h1{font-size:clamp(34px,5vw,54px);line-height:1.1;letter-spacing:-.025em}h2{line-height:1.25}main{padding:26px 24px}a{color:#a71920;text-underline-offset:3px}a:focus-visible,input:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #D2181F;outline-offset:4px}.nav{display:flex;gap:18px;flex-wrap:wrap}.note{background:white;padding:16px 20px;border-left:5px solid #FFBC00}.stats{display:flex;gap:10px;flex-wrap:wrap}.stats span{background:#fff4d2;padding:8px 13px;border-bottom:3px solid #FFBC00}.document{background:white;border:1px solid #d8d0c9;border-top:4px solid #D2181F;border-radius:8px;padding:24px;margin:22px 0;scroll-margin-top:16px}.tag{color:#a71920;font-weight:600;font-size:13px;letter-spacing:.07em}.document h2{margin:9px 0 14px}.scope,.small{font-size:14px;color:#625D58}.parts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;list-style:none;padding:0}.parts li{background:#F7F4F1;border:1px solid #ddd4cc;border-radius:5px;padding:12px}.parts a{display:inline-block;margin-right:12px}.parts span{display:block;font-size:13px;color:#625D58}.search{background:#1A1512;color:white;padding:24px;border-radius:8px}.search input{font:inherit;width:100%;padding:12px;border:2px solid #FFBC00;border-radius:5px;display:block;margin:12px 0}.search button{font:inherit;padding:10px 18px;border:1px solid #FFBC00;border-radius:5px;background:#FFBC00;cursor:pointer}.search p{font-size:14px}#results li{padding:10px;border-bottom:1px solid #ddd4cc}#results p{margin:5px 0;font-size:14px}.skip{position:absolute;left:-10000px}.skip:focus{left:10px;top:8px;background:white;padding:10px}p,li{overflow-wrap:anywhere}[hidden]{display:none!important}@media(max-width:760px){.parts{grid-template-columns:repeat(2,minmax(0,1fr))}main{padding:18px 12px}.document{padding:17px}}@media(max-width:440px){.parts{grid-template-columns:1fr}}@media print{body{background:white;font-size:10pt}.search,.nav,.skip{display:none}.document{break-before:page}.parts{display:block}.parts li{margin:7px 0}header{background:white;color:#1A1512}header p{color:#625D58}}
"""
JS="""(()=>{'use strict';const f=document.querySelector('#search-form');if(!f)return;const input=document.querySelector('#query'),status=document.querySelector('#status'),list=document.querySelector('#results');function run(e){if(e)e.preventDefault();list.replaceChildren();const q=input.value.trim().toLowerCase();if(q.length<2){status.textContent='Enter at least two characters.';return}const words=q.split(/\\s+/),hits=window.CAT_SEARCH.filter(r=>words.every(w=>r.text.toLowerCase().includes(w)));status.textContent=hits.length+' source pages match'+(hits.length>50?' · first 50 shown':'');hits.slice(0,50).forEach(r=>{const li=document.createElement('li'),a=document.createElement('a'),p=document.createElement('p');a.href=r.href;a.textContent=r.title+' · original PDF page '+r.page;const i=r.text.toLowerCase().indexOf(words[0]);p.textContent=r.text.slice(Math.max(0,i-60),i+200).replace(/\\s+/g,' ')+'…';li.append(a,p);list.append(li)})}f.addEventListener('submit',run);document.querySelector('#clear').addEventListener('click',()=>{input.value='';list.replaceChildren();status.textContent='Search the text of every source page.';input.focus()})})();"""
def cards(docs):
 out=[]
 for d in docs:
  parts=''.join(f'<li><strong>PDF pages {p["start"]}–{p["end"]}</strong><br><a href="{p["file"]}">PDF</a><a href="{p["text"]}">Text</a><span>{p["bytes"]/1048576:.2f} MiB · {p["pages"]} pages</span></li>' for p in d['parts'])
  pub=escape(d.get('publication') or 'Publication number not transcribed');year=str(d['publication_year']) if d['publication_year'] else 'Year not verified'
  out.append(f'<section class="document" id="{d["id"]}"><p class="tag">{d["id"]} · {escape(d["type"].upper())}</p><h2>{escape(d["title"])}</h2><p>{pub} · {year} · {d["original_pages"]} original pages</p><p class="scope">{escape(d["model_scope"])}</p><p><a href="{escape(d["source_url"],quote=True)}">Publisher/source download</a> · <a href="records/{d["slug"]}.json">Identity, source hash and part record</a></p><details><summary>{len(d["parts"])} small PDF part(s) · complete page sequence</summary><ul class="parts">{parts}</ul></details></section>')
 return ''.join(out)
def html(docs,title='CAT equipment reference library',volume=False):
 n=sum(d['original_pages'] for d in docs);parts=sum(len(d['parts']) for d in docs)
 nav='<a href="README.md">Collection record</a><a href="parts-atlas.html">Identify machine parts</a><a href="../whmis/index.html">WHMIS and hazard symbols</a><a href="downloads.html">ZIP downloads</a>' if not volume else '<a href="README-OFFLINE.txt">Read this volume offline</a>'
 search='' if volume else '<form class="search" id="search-form"><label for="query">Search parts, components and manual text</label><input id="query" type="search" placeholder="For example: auger shaft, sidegate, brake"><button>Search</button> <button id="clear" type="button">Clear</button><p id="status" role="status">Search the text of every source page.</p></form><ol id="results"></ol>'
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | ACCESS IS4S</title><link rel="stylesheet" href="assets/library.css"></head><body><a class="skip" href="#main">Skip to publications</a><header><div><p>ACCESS · INDIGENOUS SKILLS 4 SUCCESS</p><h1>{escape(title)}</h1><p>Find the machine. Name the component. Check the source.</p></div></header><main id="main"><nav class="nav">{nav}</nav><p class="stats"><span>{len(docs)} publications</span><span>{n:,} source pages</span><span>{parts} small PDF parts</span></p><p class="note">Every page of each listed source is retained. Parts are at most 25 pages and 10 MiB, with original page appearance preserved. Each card identifies the publication type and model scope. A parts reference guide contains selected parts; a complete serial-specific parts manual and the applicable operation manual answer different questions.</p>{search}<nav aria-label="Publication contents"><ul>{''.join(f'<li><a href="#{d["id"]}">{d["id"]} · {escape(d["title"])}</a></li>' for d in docs)}</ul></nav>{cards(docs)}<p class="small">Source text is a navigation aid. Check tables, illustrations, notices and model conditions in the native PDF. Accessed 30 October 2026; publication dates are recorded separately.</p></main>{'' if volume else '<script src="assets/search-index.js"></script><script src="assets/library.js"></script>'}</body></html>'''
def native_part(reader,start,end):
 writer=PdfWriter()
 for old in reader.pages[start-1:end]:
  page=writer.add_page(old)
  if '/Annots' in page:
   kept=[]
   for ref in page['/Annots']:
    ann=ref.get_object()
    if ann.get('/Subtype')=='/Link':
     act=ann.get('/A');act=act.get_object() if act else None
     if not act or act.get('/S')!='/URI' or not act.get('/URI'):continue
     ann.pop('/Dest',None)
    kept.append(ref)
   if kept:page[NameObject('/Annots')]=ArrayObject(kept)
   else:page.pop('/Annots',None)
 writer.compress_identical_objects(remove_duplicates=True,remove_unreferenced=True)
 out=io.BytesIO();writer.write(out);return out.getvalue()
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--downloads',type=Path,required=True);a=parser.parse_args()
 docs=json.loads((ROOT/'catalogue.json').read_text())['documents'];search=[]
 previous=json.loads((ROOT/'manifest.json').read_text()) if (ROOT/'manifest.json').exists() else {'documents':[]}
 boundaries={(d['original_sha256'],p['start']):p['end'] for d in previous['documents'] for p in d['parts']}
 for d in docs:
  src=a.downloads/d['download_filename'];raw=src.read_bytes();assert sha(raw)==d['original_sha256'],d['id']
  original=fitz.open(src);reader=PdfReader(src);assert len(original)==d['original_pages'];parts=[];start=1
  while start<=len(original):
   end=boundaries.get((d['original_sha256'],start),min(start+24,len(original)));part=None
   while True:
    if start==1 and end==len(original):data=raw
    else:
     data=native_part(reader,start,end)
    if len(data)<=10*1048576:break
    assert end>start,'Single source page exceeds size target';end=start+max(1,(end-start+1)//2)-1
   stem=f'{d["slug"]}/p{start:04d}-{end:04d}';pdfpath=ROOT/'sources'/f'{stem}.pdf';pdfpath.parent.mkdir(parents=True,exist_ok=True);pdfpath.write_bytes(data)
   text='';empty=[]
   for n in range(start,end+1):
    t=original[n-1].get_text(sort=True);text+=f'=== SOURCE PDF PAGE {n} ===\n'+(t.strip() or '[No extractable text on this page; inspect the original PDF image.]')+'\n\n'
    if not t.strip():empty.append(n)
    search.append({'document':d['id'],'title':d['title'],'page':n,'href':pdfpath.relative_to(ROOT).as_posix()+f'#page={n-start+1}','text':t})
   textpath=ROOT/'text'/f'{stem}.txt';write(textpath,text)
   parts.append({'file':pdfpath.relative_to(ROOT).as_posix(),'text':textpath.relative_to(ROOT).as_posix(),'start':start,'end':end,'pages':end-start+1,'bytes':len(data),'sha256':sha(data),'text_sha256':sha(text.encode()),'empty_text_source_pages':empty,'original_bytes_preserved':data==raw})
   start=end+1
  d['parts']=parts;write(ROOT/'records'/f'{d["slug"]}.json',json.dumps(d,ensure_ascii=False,indent=2)+'\n');original.close();print(d['id'],d['original_pages'],'pages',len(parts),'parts',flush=True)
 manifest={'schema_version':1,'accessed':'2026-10-30','policy':{'max_pages':25,'max_bytes':10*1048576,'processing':'Native PDF pages copied without image resampling. All pages retained, including covers, contents, notices and blank pages. Internal/non-URI link annotations omitted from split parts; external URI links and source whole-file URL retained. Native page resources and image streams preserved using pypdf.'},'counts':{'documents':len(docs),'source_pages':sum(d['original_pages'] for d in docs),'pdf_parts':sum(len(d['parts']) for d in docs),'largest_part_bytes':max(p['bytes'] for d in docs for p in d['parts'])},'documents':docs}
 write(ROOT/'manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');write(ROOT/'index.html',html(docs));write(ROOT/'assets/library.css',CSS);write(ROOT/'assets/library.js',JS);write(ROOT/'assets/search-index.js','window.CAT_SEARCH='+json.dumps(search,ensure_ascii=False,separators=(',',':'))+';\n')
 target=ROOT/'assets/fonts';target.mkdir(exist_ok=True)
 for p in (ROOT.parent/'assets/fonts').iterdir():
  if p.name in ['ibm-plex-sans-latin-400-normal.woff2','ibm-plex-sans-latin-600-normal.woff2'] or p.suffix in ['.txt','.md']:shutil.copyfile(p,target/p.name)
 print(json.dumps(manifest['counts']))
if __name__=='__main__':main()
