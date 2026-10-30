"""Preserve every original scanned page in small PDFs without rasterizing it."""
from pathlib import Path
import argparse, hashlib, json
import fitz
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('pdf',type=Path);args=a.parse_args()
 original=args.pdf.resolve();h=sha(original);d=fitz.open(original);target=ROOT/'pdf';target.mkdir(exist_ok=True)
 manifest=ROOT/'source-parts.json'
 if manifest.exists():
  old=json.loads(manifest.read_text())
  if old['original_sha256']==h and all((ROOT/x['file']).is_file() and sha(ROOT/x['file'])==x['sha256'] for x in old['parts']):
   print('Verified existing source parts',len(old['parts']));return
 parts=[];start=1
 while start<=len(d):
  end=min(start+24,len(d))
  while True:
   w=fitz.open();w.insert_pdf(d,from_page=start-1,to_page=end-1)
   w.set_metadata({'title':f'The Asphalt Handbook MS-4, seventh edition — source PDF pages {start}–{end}',
                   'author':'Asphalt Institute','subject':f'Unaltered page content from the supplied scan. Original SHA-256 {h}.',
                   'creator':'ACCESS IS4S source-page splitter'})
   raw=w.tobytes(garbage=3,deflate=True);w.close()
   if len(raw)<=12*1024*1024 or end==start:break
   end=start+max(1,(end-start+1)//2)-1
  name=f'pdf/p{start:04d}-{end:04d}.pdf';p=ROOT/name;p.write_bytes(raw)
  parts.append({'file':name,'pdf_start':start,'pdf_end':end,'pages':end-start+1,'bytes':len(raw),'sha256':sha(p)})
  print(name,len(raw),flush=True);start=end+1
 manifest.write_text(json.dumps({'original_filename':'the-asphalt-handbook -MS-4-7th-ed.pdf',
  'original_sha256':h,'original_bytes':original.stat().st_size,'original_pdf_pages':len(d),
  'processing':'Pages copied without image resampling or OCR changes. Full original scan retained outside git; these parts collectively preserve all source pages.',
  'parts':parts},indent=2)+'\n')
 print(f'{len(parts)} parts; {len(d)} pages preserved; largest {max(x["bytes"] for x in parts):,} bytes')
if __name__=='__main__':main()
