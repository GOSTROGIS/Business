"""Create indexed PDF/text context chunks for every available asphalt PDF.

From the repository root:
  python -m pip install -r curriculum/asphalt-paving/tools/requirements.txt
  python curriculum/asphalt-paving/tools/build_context.py
Requires Poppler's pdftotext on PATH (or --pdftotext). Originals are never changed.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,os,re,shutil,subprocess,tempfile
from collections import Counter
from datetime import datetime,timezone
from html import escape
from pathlib import Path
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ArrayObject,NameObject

ASPHALT=Path(__file__).resolve().parents[1]
REPO=ASPHALT.parents[1]
OUT=ASPHALT/'context'
POLICY_VERSION=1
BOOK=ASPHALT/'ms-4'
BOOK_PARTS=json.loads((BOOK/'source-parts.json').read_text()) if (BOOK/'source-parts.json').exists() else None
BOOK_BY_PATH={(BOOK/x['file']).resolve():x for x in BOOK_PARTS['parts']} if BOOK_PARTS else {}
def book_text(path):
 part=BOOK_BY_PATH.get(path.resolve())
 if not part:return None
 pages=[]
 for n in range(part['pdf_start'],part['pdf_end']+1):
  edited=BOOK/'edits'/f'p{n:04d}.txt';raw=BOOK/'text'/f'p{n:04d}.txt'
  pages.append((edited if edited.exists() else raw).read_text())
 return pages,part


def sha_bytes(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def sha_file(p:Path)->str:return sha_bytes(p.read_bytes())
def category(p:Path)->str:
 rel=p.relative_to(ASPHALT)
 return 'original-source' if rel.parts[0]=='sources' or rel.parts[:2]==('ms-4','pdf') else ('manufacturer-original' if rel.parts[:2]==('manuals','pdfs') else 'generated-curriculum')
def priority(p:Path):return ({'original-source':0,'manufacturer-original':1,'generated-curriculum':2}[category(p)],p.as_posix())
def slug(p:Path)->str:return re.sub(r'[^a-z0-9]+','-',p.stem.lower()).strip('-')[:65]
def doc_titles()->dict[str,str]:
 out={}
 for rel in ['sources/manifest.json','manuals/manifest.json']:
  path=ASPHALT/rel
  if not path.exists():continue
  data=json.loads(path.read_text());records=data if isinstance(data,list) else data.get('documents',data.get('sources',[]))
  for r in records:
   h=r.get('sha256');title=r.get('title') or r.get('document_title')
   if h and title:out[h]=title
 if BOOK_PARTS:
  for r in BOOK_PARTS['parts']:out[r['sha256']]=f"MS-4 Seventh Edition · complete scan part, original book PDF pages {r['pdf_start']}–{r['pdf_end']}"
 return out

def chunk_bytes(reader:PdfReader,start:int,end:int,title:str)->tuple[bytes,dict]:
 writer=PdfWriter();removed=0;kept=0
 for page in reader.pages[start-1:end]:
  new=writer.add_page(page)
  if '/Annots' in new:
   refs=[]
   for ref in new['/Annots']:
    ann=ref.get_object()
    if ann.get('/Subtype')=='/Link':
     action=ann.get('/A');action=action.get_object() if action is not None else None
     # Retain external URI actions only; internal page destinations depend on
     # the original document's page tree and are deliberately omitted.
     if not action or action.get('/S')!='/URI' or not action.get('/URI'):
      removed+=1;continue
     ann.pop('/Dest',None);kept+=1
    refs.append(ref)
   if refs:new[NameObject('/Annots')]=ArrayObject(refs)
   else:new.pop('/Annots',None)
 writer.add_metadata({'/Title':f'{title} — original PDF pages {start}–{end}','/Subject':'Context excerpt; original page appearance/content retained. Internal page-link annotations omitted; external URI links retained.','/Creator':'ACCESS IS4S PDF context builder'})
 # Remove objects reached only through discarded internal page links. This
 # does not downsample images or rasterize/rewrite the page content streams.
 writer.compress_identical_objects(remove_duplicates=True,remove_unreferenced=True)
 stream=io.BytesIO();writer.write(stream)
 return stream.getvalue(),{'internal_or_non_uri_link_annotations_removed':removed,'external_uri_link_annotations_retained':kept}

def read_text_pages(path:Path,pages:int,exe:str)->tuple[list[str],dict]:
 book=book_text(path)
 if book:
  text,part=book
  if len(text)!=pages:raise RuntimeError(f'MS-4 part page mismatch: {path}')
  return text,{'status':'ocr-unproofread','warning':'Full source-page images are authoritative for technical values and tables; OCR is not fully proofread.','ocr_performed':True,'method':'Upstream Tesseract English OCR; reviewed text overrides used where present. No changes to source PDF page images.','book_pdf_start':part['pdf_start'],'book_pdf_end':part['pdf_end'],'text_source_sha256':sha_bytes('\f'.join(text).encode())}
 run=subprocess.run([exe,'-layout','-enc','UTF-8',str(path),'-'],capture_output=True)
 if run.returncode:
  return ['']*pages,{'status':'failed','warning':run.stderr.decode(errors='replace')[:3000],'ocr_performed':False}
 parts=run.stdout.decode('utf-8',errors='replace').split('\f')
 if parts and not parts[-1].strip():parts.pop()
 if len(parts)!=pages:
  return ['']*pages,{'status':'failed-page-map','warning':f'Extractor produced {len(parts)} page segments for {pages} PDF pages; text not assigned to possibly incorrect pages.','ocr_performed':False}
 return parts,{'status':'extracted','warning':run.stderr.decode(errors='replace').strip()[:3000] or None,'ocr_performed':False,'method':'pdftotext -layout, UTF-8; PDF page boundaries retained'}

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--max-pages',type=int,default=25)
 parser.add_argument('--max-mib',type=float,default=16)
 parser.add_argument('--pdftotext',default=shutil.which('pdftotext'))
 args=parser.parse_args()
 if not 1<=args.max_pages<=25:parser.error('--max-pages must be between 1 and 25')
 if args.max_mib<=0:parser.error('--max-mib must be positive')
 if not args.pdftotext:parser.error('pdftotext is required; install Poppler or specify --pdftotext')
 limit=int(args.max_mib*1024*1024);OUT.mkdir(parents=True,exist_ok=True)
 paths=sorted((p for p in ASPHALT.rglob('*.pdf') if OUT not in p.parents),key=priority)
 groups={}
 for path in paths:
  data=path.read_bytes()
  if not data.startswith(b'%PDF-'):raise RuntimeError(f'Not a PDF: {path}')
  h=sha_bytes(data);groups.setdefault(h,[]).append(path)
 titles=doc_titles();documents=[]
 config={'policy_version':POLICY_VERSION,'max_pages':args.max_pages,'target_max_bytes':limit,'single_page_over_target_policy':'Preserve the page without image degradation; flag an exception. A chunk at or above 100,000,000 bytes fails the build.'}
 old=json.loads((OUT/'manifest.json').read_text()) if (OUT/'manifest.json').exists() else {}
 cache={x['sha256']:x for x in old.get('documents',[])} if old.get('chunk_policy')==config else {}
 with tempfile.TemporaryDirectory(prefix='.build-',dir=OUT) as staging:
  stage=Path(staging)
  for h,aliases in groups.items():
   source=aliases[0];reader=PdfReader(source)
   encrypted=reader.is_encrypted
   if encrypted and not reader.decrypt(''):raise RuntimeError(f'PDF requires a non-empty password; provide an authorized accessible copy: {source}')
   n=len(reader.pages);rel=source.relative_to(REPO).as_posix();alias_paths=[p.relative_to(REPO).as_posix() for p in aliases]
   title=titles.get(h) or f"{source.parent.name.replace('-',' ').title()} · {source.stem.replace('-',' ').replace('_',' ')}"
   ident='PDF-'+h[:12];folder=slug(source)+'-'+h[:12]
   previous=cache.get(h)
   book=book_text(source)
   book_key=sha_bytes('\f'.join(book[0]).encode()) if book else None
   cached=previous is not None and previous['original_path']==rel and previous['title']==title and all((OUT/c[k]).is_file() and sha_file(OUT/c[k])==c[hashkey] for c in previous['chunks'] for k,hashkey in [('pdf','sha256'),('text','text_sha256')])
   if book and cached:cached=previous['extraction'].get('text_source_sha256')==book_key
   if cached:
    doc=dict(previous);doc.update(original_path=rel,aliases=alias_paths,title=title,category=category(source));documents.append(doc)
    print(f'Cached {n:4} pages / {len(doc["chunks"]):2} chunks: {rel}',flush=True);continue
   pages,extraction=read_text_pages(source,n,args.pdftotext)
   destination=stage/'chunks'/folder;destination.mkdir(parents=True)
   chunks=[];start=1
   while start<=n:
    end=min(n,start+args.max_pages-1)
    while True:
     reuse=bool(book and start==1 and end==n and source.stat().st_size<=limit)
     if reuse:raw=source.read_bytes();links={'source_part_reused':True,'internal_or_non_uri_link_annotations_removed':0,'external_uri_link_annotations_retained':0}
     else:raw,links=chunk_bytes(reader,start,end,title)
     if len(raw)<=limit or end==start:break
     end=start+max(1,(end-start+1)//2)-1
    if len(raw)>=100_000_000:raise RuntimeError(f'Single-page chunk too large for repository: {rel} page {start}')
    stem=f'p{start:04d}-{end:04d}';local=f'chunks/{folder}/{stem}'
    pdf_path=os.path.relpath(source,OUT) if reuse else local+'.pdf'
    if not reuse:(destination/(stem+'.pdf')).write_bytes(raw)
    empty=[i for i in range(start,end+1) if not pages[i-1].strip()]
    sparse=[i for i in range(start,end+1) if 0<len(re.sub(r'\s','',pages[i-1]))<40]
    text=f'SOURCE: {rel}\nSOURCE SHA-256: {h}\nORIGINAL PDF VIEWER PAGES: {start}–{end} (one-based)\nOCR PERFORMED: {"yes (upstream OCR pipeline)" if extraction['ocr_performed'] else "no"}\nEXTRACTION STATUS: {extraction["status"]}\nText is a reading aid; compare tables, figures, symbols and conditions against the PDF.\n\n'
    for i in range(start,end+1):
     book_label=f"=== COMPLETE BOOK PDF PAGE {book[1]['pdf_start']+i-1} ===\n" if book else ''
     missing='[NO OCR WORDS DETECTED; inspect the source scan.]' if book else '[NO EXTRACTABLE TEXT: page may be blank, image-only, or have an unavailable text layer; no OCR was performed.]'
     text+=f'=== ORIGINAL PDF PAGE {i} ===\n'+book_label+(pages[i-1].strip() or missing)+'\n\n'
    txt=text.encode('utf-8');(destination/(stem+'.txt')).write_bytes(txt)
    chunks.append(dict(original_page_start=start,original_page_end=end,page_count=end-start+1,pdf=pdf_path,bytes=len(raw),sha256=sha_bytes(raw),text=local+'.txt',text_bytes=len(txt),text_sha256=sha_bytes(txt),extraction_status=extraction['status'],empty_text_original_pages=empty,sparse_text_original_pages=sparse,ocr_performed=extraction['ocr_performed'],single_page_exceeds_target_bytes=len(raw)>limit,**links))
    start=end+1
   if sha_file(source)!=h:raise RuntimeError(f'Source changed during build; rerun after it stabilizes: {rel}')
   documents.append(dict(id=ident,title=title,category=category(source),original_path=rel,aliases=alias_paths,sha256=h,original_bytes=source.stat().st_size,pdf_pages=n,original_encryption_present=encrypted,opened_with_standard_empty_password=encrypted,extraction=extraction,chunks=chunks))
   print(f'Built  {n:4} pages / {len(chunks):2} chunks: {rel}',flush=True)
  # Publish only after the complete snapshot has been prepared successfully.
  for d in documents:
   for c in d['chunks']:
    for k in ['pdf','text']:
     if k=='pdf' and c.get('source_part_reused'):continue
     p=stage/c[k]
     if p.exists():target=OUT/c[k];target.parent.mkdir(parents=True,exist_ok=True);p.replace(target)
  expected={c[k] for d in documents for c in d['chunks'] for k in ['pdf','text']}
  for p in (OUT/'chunks').rglob('*'):
   if p.is_file() and p.relative_to(OUT).as_posix() not in expected:p.unlink()
  for p in sorted((OUT/'chunks').rglob('*'),reverse=True):
   if p.is_dir() and not any(p.iterdir()):p.rmdir()
  all_chunks=[c for d in documents for c in d['chunks']]
  counts=dict(original_file_paths=len(paths),unique_pdfs=len(documents),duplicate_alias_paths=len(paths)-len(documents),unique_original_pages=sum(d['pdf_pages'] for d in documents),chunks=len(all_chunks),chunk_pdf_bytes=sum(c['bytes'] for c in all_chunks),chunk_text_bytes=sum(c['text_bytes'] for c in all_chunks),largest_chunk_bytes=max(c['bytes'] for c in all_chunks),largest_chunk_pages=max(c['page_count'] for c in all_chunks),empty_text_pages=sum(len(c['empty_text_original_pages']) for c in all_chunks),sparse_text_pages=sum(len(c['sparse_text_original_pages']) for c in all_chunks),single_page_size_exceptions=sum(c['single_page_exceeds_target_bytes'] for c in all_chunks),categories=dict(Counter(d['category'] for d in documents)))
  textbook={'title':'The Asphalt Handbook, MS-4, seventh edition','html':'../ms-4/index.html','pdf_pages':BOOK_PARTS['original_pdf_pages'],'source_parts':len(BOOK_PARTS['parts']),'source_sha256':BOOK_PARTS['original_sha256']} if BOOK_PARTS else None
  manifest=dict(schema_version=2,built_utc=datetime.now(timezone.utc).isoformat(),collection='All available PDFs under curriculum/asphalt-paving, excluding this context directory',originals_preserved=True,chunk_policy=config,processing='Original PDF page appearance retained without image downsampling. MS-4 source parts are referenced directly without duplicate PDF copies; their accompanying text comes from the upstream OCR pipeline. Other texts use pdftotext. Internal/non-URI annotations are omitted from split chunks; full MS-4 image-only source parts have no such links.',counts=counts,documents=documents,primary_textbook=textbook,pending_sources=[] if textbook else [dict(title='The Asphalt Handbook MS-4 — Seventh Edition',status='No accessible full source is registered.',needed='Add an authorized complete source and rebuild.')])
  (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
  write_indexes(manifest)
  print(json.dumps(counts,indent=2),flush=True)

def write_indexes(m):
 c=m['counts'];docs=m['documents']
 pending=m.get('pending_sources',[])
 textbook_heading='Primary textbook available' if m.get('primary_textbook') else 'Primary textbook pending'
 textbook_note=('The complete **834-page MS-4 seventh-edition scan** is available as [searchable HTML](../ms-4/index.html) and 34 small source PDF parts. Every source page is preserved. The context records below reuse those parts directly; their text files include both part-local and complete-book viewer page numbers. OCR remains unproofread except for separately recorded editorial corrections.' if m.get('primary_textbook') else ' '.join(x['status']+' '+x['needed'] for x in pending))
 textbook_html=('<a href="../ms-4/index.html">Open the complete 834-page MS-4 HTML reader</a> · 34 source PDF parts, with original figures and tables retained.' if m.get('primary_textbook') else escape(textbook_note))

 lines=['# Asphalt PDF context library','',f"**{c['original_file_paths']} PDF paths · {c['unique_pdfs']} unique PDFs · {c['unique_original_pages']:,} original pages · {c['chunks']} PDF chunks and {c['chunks']} text extracts.**",'',f"Every available PDF under the asphalt curriculum is indexed here. Originals remain in place, byte-for-byte. Each chunk has no more than {m['chunk_policy']['max_pages']} original pages; the byte target is {m['chunk_policy']['target_max_bytes']:,} bytes (16 MiB by default). The largest current chunk is **{c['largest_chunk_bytes']:,} bytes** and **{c['largest_chunk_pages']} pages**. There are **{c['single_page_size_exceptions']} single-page size exceptions**.",'','[Browse the context index](index.html) · [Complete manifest](manifest.json) · [Chunk index CSV](chunk-index.csv)','','## '+textbook_heading,'',textbook_note,'','## How to use the chunks','','Start with the source title and original PDF page range. Open the chunk PDF to inspect the actual page, then use its text file to search or provide smaller context. Text headings preserve the original one-based viewer page number. Printed page labels inside the document can differ. Tables, columns, symbols and diagrams may not extract faithfully; the PDF remains the visual reference.','','MS-4 text comes from the upstream Tesseract OCR pipeline; other texts use `pdftotext`. OCR does not replace the source image for exact technical wording, figures or tables. Empty-text pages are explicitly marked in the text and manifest. Sparse text is flagged without claiming that a page is unreadable. Missing extracted text does not mean the original page has no information. Current empty-text page count: **'+str(c['empty_text_pages'])+'**; sparse-text page count: **'+str(c['sparse_text_pages'])+'**.','','Internal page-link annotations and original outlines are omitted from chunks so a link cannot point to a missing page. External URI links are retained. Page content is not downsampled or rewritten; original whole PDFs preserve their original navigation. The supplied 2006 specification has two identical repository paths and one shared chunk set.','','## Original documents and chunks','']
 sections=[];toc=[];csvrows=[]
 for d in docs:
  ident=d['id'];orig=os.path.relpath(REPO/d['original_path'],OUT)
  lines += [f"### {d['title']}",'',f"**{ident}** · {d['category']} · {d['pdf_pages']} pages · original SHA-256 `{d['sha256']}`",'',f"Original: [{d['original_path']}]({orig})"]
  if len(d['aliases'])>1:
   lines+=['','Identical aliases:']+[f"- [{a}]({os.path.relpath(REPO/a,OUT)})" for a in d['aliases']]
  lines+=['','| Original PDF pages | Chunk PDF | Text extract | PDF bytes | Text status |','|---|---|---|---:|---|']
  rows=[]
  for x in d['chunks']:
   span=f"{x['original_page_start']}–{x['original_page_end']}";status=('OCR; no words detected: ' if x['ocr_performed'] else 'No OCR; empty: ')+','.join(map(str,x['empty_text_original_pages'])) if x['empty_text_original_pages'] else x['extraction_status']
   if x['extraction_status']!='extracted':status=x['extraction_status']
   lines.append(f"| {span} | [PDF]({x['pdf']}) | [Text]({x['text']}) | {x['bytes']:,} | {status} |")
   rows.append(f"<tr><td>{span}</td><td><a href='{escape(x['pdf'])}'>Open PDF</a></td><td><a href='{escape(x['text'])}'>Read text</a></td><td>{x['bytes']:,}</td><td>{escape(status)}</td></tr>")
   csvrows.append([ident,d['title'],d['category'],d['original_path'],d['sha256'],x['original_page_start'],x['original_page_end'],x['pdf'],x['sha256'],x['text'],x['text_sha256'],x['bytes'],x['extraction_status'],' '.join(map(str,x['empty_text_original_pages']))])
  lines+=[''];toc.append(f"<li><a href='#{ident}'>{escape(d['title'])}</a> · {d['pdf_pages']} pages</li>")
  aliases=''.join(f"<li><a href='{escape(os.path.relpath(REPO/a,OUT))}'>{escape(a)}</a></li>" for a in d['aliases'])
  sections.append(f"<section class='document' id='{ident}' data-search='{escape((d['title']+' '+' '.join(d['aliases'])+' '+d['category']).lower(),quote=True)}'><h2>{escape(d['title'])}</h2><p class='meta'>{ident} · {escape(d['category'])} · {d['pdf_pages']} original pages · {len(d['chunks'])} chunks</p><details><summary>Original file paths and SHA-256</summary><ul>{aliases}</ul><code>{d['sha256']}</code></details><div class='table-wrap' tabindex='0' role='region' aria-label='PDF chunks'><table><thead><tr><th>Original PDF pages</th><th>Chunk</th><th>Context text</th><th>PDF bytes</th><th>Text status</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>")
 lines+=['## Rebuild after PDFs change','','From the repository root:','','```sh','python -m pip install -r curriculum/asphalt-paving/tools/requirements.txt','python curriculum/asphalt-paving/tools/build_context.py','```','','Install Poppler so `pdftotext` is available, or pass `--pdftotext /path/to/pdftotext`. The builder defaults to `--max-pages 25 --max-mib 16`. It discovers PDFs recursively, skips this context directory, deduplicates by SHA-256, prioritizes source/manufacturer originals, and reuses verified unchanged chunks. It opens already-readable PDFs using the standard empty password when their encryption flag is set; it refuses a non-empty-password requirement, malformed PDFs and any chunk at or above 100,000,000 bytes. If a single unchanged page exceeds the preferred byte target, the exception is recorded rather than degrading its images.','','Generated books can change during curriculum development. Rerun this builder after their final export so original hashes, page counts and chunk ranges remain in sync. The manifest records the exact build snapshot.']
 (OUT/'README.md').write_text('\n'.join(lines)+'\n')
 with (OUT/'chunk-index.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator="\n");w.writerow(['source_id','title','category','original_path','original_sha256','original_page_start','original_page_end','chunk_pdf','chunk_sha256','text_file','text_sha256','pdf_bytes','extraction_status','empty_original_pages']);w.writerows(csvrows)
 css="""*{box-sizing:border-box}body{margin:0;background:#F7F4F1;color:#1A1512;font:17px/1.55 Arial,sans-serif}header{background:#1A1512;color:#fff;border-bottom:7px solid #FFBC00;padding:32px}header div,main{max-width:1080px;margin:auto}header p:first-child{color:#FFBC00;letter-spacing:.1em;font-size:13px;font-weight:bold}h1{font-size:38px;line-height:1.2}main{padding:24px}a{color:#a31920;text-underline-offset:3px}a:focus,input:focus{outline:3px solid #D2181F;outline-offset:3px}.document,.note{background:white;border:1px solid #d8d0c9;border-top:4px solid #D2181F;padding:24px;margin:24px 0;border-radius:6px}h2{font-size:24px;line-height:1.3}.meta{color:#5e5045;font-size:14px}code{font-size:13px;overflow-wrap:anywhere}li,p{overflow-wrap:anywhere}input{display:block;width:100%;font:inherit;padding:12px;border:1px solid #92877f;border-radius:4px}table{border-collapse:collapse;width:100%;font-size:14px;margin-top:18px}th,td{padding:9px;border:1px solid #d3c8be;text-align:left;vertical-align:top}th{background:#eee6df}.table-wrap{overflow:auto}details ul{font-size:14px}.small{font-size:14px}.skip{position:absolute;left:-9999px}.skip:focus{left:10px;top:10px;background:white;padding:8px}[hidden]{display:none!important}@media(max-width:600px){main{padding:12px}header{padding:24px 18px}h1{font-size:29px}.document,.note{padding:15px}th,td{padding:6px}}"""
 script="""const input=document.querySelector('#filter');input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();let shown=0;document.querySelectorAll('.document').forEach(s=>{s.hidden=!s.dataset.search.includes(q);if(!s.hidden)shown++});document.querySelector('#result-count').textContent=shown+' documents shown';});"""
 html=f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Asphalt PDF context library | ACCESS IS4S</title><style>{css}</style></head><body><a class='skip' href='#main'>Skip to context files</a><header><div><p>ACCESS · INDIGENOUS SKILLS 4 SUCCESS</p><h1>Asphalt PDF context library</h1><p>{c['unique_pdfs']} unique PDFs · {c['unique_original_pages']:,} original pages · {c['chunks']} smaller chunks with text extracts</p></div></header><main id='main'><p><a href='README.md'>Complete reading record</a> · <a href='manifest.json'>Manifest and checksums</a> · <a href='chunk-index.csv'>Chunk index CSV</a></p><section class='note'><strong>{textbook_heading}: MS-4 Seventh Edition</strong><p>{textbook_html}</p></section><p>Originals stay in place. Each chunk has at most {m['chunk_policy']['max_pages']} original PDF pages; the largest is {c['largest_chunk_bytes']:,} bytes. MS-4 text uses OCR; other text is extracted from PDF text layers. Use the source PDF or page image to check tables, diagrams and symbols.</p><label for='filter'>Find a document by title, filename or category</label><input id='filter' type='search' placeholder='For example: LeeBoy, outline, specifications'><p id='result-count' class='small' aria-live='polite'>{len(docs)} documents shown</p><details><summary>All document titles</summary><ul>{''.join(toc)}</ul></details>{''.join(sections)}<p class='small'>PDF viewer page ranges refer to the original file; printed page labels may differ. Internal page-link annotations are omitted from chunks; external URI links remain. See the manifest for text gaps and complete processing details.</p></main><script>{script}</script></body></html>"
 (OUT/'index.html').write_text(html)

if __name__=='__main__':main()
