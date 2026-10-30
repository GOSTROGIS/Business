"""Extract the supplied scanned MS-4 into page images and editable OCR text.

python tools/extract_book.py /path/to/original.pdf --workers 4
Requires PyMuPDF, Pillow and Tesseract with English language data. The original
PDF is never changed. Page numbers here are one-based PDF viewer pages.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, os, subprocess, tempfile, time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
POLICY = {'version': 1, 'ocr_dpi': 250, 'display_dpi': 150,
          'display_encoding': 'lossless WebP', 'language': 'eng', 'psm': 3}

def digest(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''): h.update(b)
    return h.hexdigest()

def extract(job):
    source, source_sha, number, force = job
    stem = f'p{number:04d}'
    record = ROOT / 'data' / (stem + '.json')
    txt = ROOT / 'text' / (stem + '.txt')
    asset = ROOT / 'assets/pages' / (stem + '.webp')
    if not force and record.exists() and txt.exists() and asset.exists():
        r = json.loads(record.read_text())
        if (r.get('source_sha256') == source_sha and r.get('policy') == POLICY
                and r['text_sha256'] == digest(txt) and r['image_sha256'] == digest(asset)):
            return number, r['word_count'], 'cached'
    doc = fitz.open(source); page = doc[number - 1]
    with tempfile.TemporaryDirectory(prefix='ms4-ocr-') as tmp:
        temp = Path(tmp); png = temp/'page.png'; base = temp/'ocr'
        pix = page.get_pixmap(dpi=POLICY['ocr_dpi'], colorspace=fitz.csGRAY, alpha=False)
        pix.save(png)
        run = subprocess.run(['tesseract', str(png), str(base), '-l', 'eng', '--psm', '3', 'txt', 'tsv'],
                             env={**os.environ, 'OMP_THREAD_LIMIT': '1'}, capture_output=True, timeout=180)
        if run.returncode: raise RuntimeError(f'Page {number}: {run.stderr.decode(errors="replace")}')
        text = base.with_suffix('.txt').read_text(encoding='utf-8')
        rows = list(csv.DictReader(io.StringIO(base.with_suffix('.tsv').read_text()), delimiter='\t', quoting=csv.QUOTE_NONE))
        words = []
        for row in rows:
            token = (row.get('text') or '').strip()
            if row.get('level') == '5' and token:
                words.append({'text': token, 'confidence': float(row['conf']),
                              'box': [int(row[k]) for k in ['left','top','width','height']],
                              'block': int(row['block_num']), 'paragraph': int(row['par_num']), 'line': int(row['line_num'])})
        ocr_width, ocr_height = pix.width, pix.height
    display = page.get_pixmap(dpi=POLICY['display_dpi'], colorspace=fitz.csGRAY, alpha=False)
    im = Image.frombytes('L', (display.width,display.height), display.samples)
    asset.parent.mkdir(parents=True,exist_ok=True);txt.parent.mkdir(parents=True,exist_ok=True)
    im.save(asset, format='WEBP', lossless=True, method=4)
    txt.write_text(text,encoding='utf-8')
    confidence = sum(w['confidence'] for w in words)/len(words) if words else None
    r = {'pdf_page': number, 'source_sha256': source_sha, 'policy': POLICY,
         'source_page_size_points': [page.rect.width,page.rect.height],
         'text': txt.relative_to(ROOT).as_posix(), 'text_sha256': digest(txt),
         'image': asset.relative_to(ROOT).as_posix(), 'image_sha256': digest(asset),
         'image_pixels': [display.width,display.height], 'image_bytes': asset.stat().st_size,
         'ocr_pixels': [ocr_width,ocr_height], 'word_count': len(words),
         'mean_word_confidence': round(confidence,2) if confidence is not None else None,
         'low_confidence_word_count': sum(w['confidence'] < 75 for w in words),
         'status': 'no-words-detected' if not words else 'ocr-unproofread', 'words': words}
    record.parent.mkdir(parents=True,exist_ok=True)
    record.write_text(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n')
    doc.close()
    return number,len(words),'extracted'

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('pdf',type=Path)
    a.add_argument('--workers',type=int,default=4);a.add_argument('--first',type=int,default=1)
    a.add_argument('--last',type=int);a.add_argument('--force',action='store_true');args=a.parse_args()
    source=args.pdf.resolve();doc=fitz.open(source);n=len(doc)
    if doc.needs_pass: raise SystemExit('An authorized readable PDF is required.')
    sha=digest(source);last=args.last or n
    if not 1<=args.first<=last<=n: a.error('Invalid page range')
    print(f'Source {sha}; {n} pages; extracting {args.first}–{last}',flush=True)
    started=time.monotonic();completed=0
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(extract,(str(source),sha,i,args.force)) for i in range(args.first,last+1)]
        for future in as_completed(futures):
            number,words,status=future.result();completed+=1
            if completed%10==0 or completed==last-args.first+1:
                print(f'{completed}/{last-args.first+1} pages · latest {number} ({words} words, {status}) · {time.monotonic()-started:.0f}s',flush=True)
    print('Complete',flush=True)

if __name__=='__main__':main()
