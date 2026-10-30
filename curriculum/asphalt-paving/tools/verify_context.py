"""Check context inventory, hashes, page maps, source reuse and representative fidelity."""
from pathlib import Path
import csv,hashlib,json,re
import fitz
from pypdf import PdfReader
A=Path(__file__).resolve().parents[1];R=A.parents[1];B=A/'context'
m=json.loads((B/'manifest.json').read_text());count=0;renders=0;links=0;seen=[];seen_text=[];aliases=[];reused=0
for d in m['documents']:
 for alias in d['aliases']:
  p=R/alias;assert hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256'],alias;aliases.append(p.resolve())
 with fitz.open(R/d['original_path']) as original:
  assert len(original)==d['pdf_pages'];expected=1
  for c in d['chunks']:
   assert c['original_page_start']==expected and c['page_count']==c['original_page_end']-expected+1
   expected=c['original_page_end']+1
   pdf=(B/c['pdf']).resolve();text=(B/c['text']).resolve();raw=pdf.read_bytes();txt=text.read_bytes()
   assert len(raw)==c['bytes'] and hashlib.sha256(raw).hexdigest()==c['sha256']
   assert len(txt)==c['text_bytes'] and hashlib.sha256(txt).hexdigest()==c['text_sha256']
   assert c['page_count']<=m['chunk_policy']['max_pages'] and c['bytes']<=m['chunk_policy']['target_max_bytes']
   page_map=list(map(int,re.findall(r'^=== ORIGINAL PDF PAGE (\d+) ===$',txt.decode(),re.M)))
   assert page_map==list(range(c['original_page_start'],c['original_page_end']+1))
   if c.get('source_part_reused'):
    assert pdf==(R/d['original_path']).resolve() and pdf.parent==A/'ms-4/pdf'
    assert d['extraction']['status']=='ocr-unproofread' and c['ocr_performed']
    global_pages=list(map(int,re.findall(r'^=== COMPLETE BOOK PDF PAGE (\d+) ===$',txt.decode(),re.M)))
    assert global_pages==list(range(d['extraction']['book_pdf_start'],d['extraction']['book_pdf_end']+1))
    upstream=[]
    for n in global_pages:
     edited=A/'ms-4/edits'/f'p{n:04d}.txt';p=edited if edited.exists() else A/'ms-4/text'/f'p{n:04d}.txt';upstream.append(p.read_text())
    assert hashlib.sha256('\f'.join(upstream).encode()).hexdigest()==d['extraction']['text_source_sha256']
    reused+=1
   else:assert B/'chunks' in pdf.parents
   reader=PdfReader(pdf);assert len(reader.pages)==c['page_count']
   for p in reader.pages:
    for ref in p.get('/Annots',[]):
     ann=ref.get_object()
     if ann.get('/Subtype')=='/Link':
      assert '/Dest' not in ann
      act=ann.get('/A');assert act and act.get('/S')=='/URI' and act.get('/URI');links+=1
   count+=1;seen.append(pdf);seen_text.append(text)
  assert expected==d['pdf_pages']+1
  if not all(c.get('source_part_reused') for c in d['chunks']):
   for n in sorted({1,max(1,d['pdf_pages']//2),d['pdf_pages']}):
    c=next(c for c in d['chunks'] if c['original_page_start']<=n<=c['original_page_end'])
    with fitz.open(B/c['pdf']) as part:
     a=original[n-1].get_pixmap(matrix=fitz.Matrix(.4,.4),annots=False)
     b=part[n-c['original_page_start']].get_pixmap(matrix=fitz.Matrix(.4,.4),annots=False)
     assert a.width==b.width and a.height==b.height and a.samples==b.samples,(d['original_path'],n)
     renders+=1
assert len(seen)==len(set(seen))==m['counts']['chunks']
actual={p.resolve() for p in A.rglob('*.pdf') if B not in p.parents}
assert actual==set(aliases) and len(aliases)==m['counts']['original_file_paths']
assert sum(d['pdf_pages'] for d in m['documents'])==m['counts']['unique_original_pages']
assert len(m['documents'])==m['counts']['unique_pdfs']
assert {p.resolve() for p in (B/'chunks').rglob('*.pdf')}=={p for p in seen if B/'chunks' in p.parents}
assert {p.resolve() for p in (B/'chunks').rglob('*.txt')}==set(seen_text)
assert len(list(csv.DictReader((B/'chunk-index.csv').open())))==count
assert reused==34 and m['primary_textbook']['pdf_pages']==834 and not m['pending_sources']
print(json.dumps({'status':'passed','documents':len(m['documents']),'chunks':count,'reused_ms4_source_parts':reused,'representative_render_comparisons':renders,'retained_URI_links':links,'checks':'Source aliases, complete inventory, hashes, size/page limits, local/global text page maps, OCR cache fingerprints, source reuse, PDF page counts, link annotations, CSV and rendering.'},indent=2))
