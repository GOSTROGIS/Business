"""Build the complete, small-part source library from pinned acquired bytes.

python curriculum/asphalt-paving/readiness/tools/build_library.py --downloads PATH
The download directory contains the catalogue's .raw files. No source PDF pages
are discarded or rasterized. Publisher HTML is preserved as inert .txt plus a
readable article with locally archived figures. Network is used only for images
explicitly referenced in the selected article; previously archived images reuse
their recorded bytes.
"""
from pathlib import Path
from html import escape as esc
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
import argparse, hashlib, importlib.util, json, re, shutil
import fitz
from pypdf import PdfReader
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CAT_TOOL = ROOT.parent / 'caterpillar/tools/build_collection.py'
spec = importlib.util.spec_from_file_location('native_collection', CAT_TOOL)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)

def sha(b): return hashlib.sha256(b).hexdigest()
def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def shell(title, body, prefix=''):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)} | ACCESS IS4S</title><link rel="stylesheet" href="{prefix}assets/library.css"></head><body><a class="skip" href="#main">Skip to content</a><header><div><p>ACCESS · INDIGENOUS SKILLS 4 SUCCESS</p><h1>{esc(title)}</h1><p>Understand the tool. Read the requirement. Prepare the work.</p></div></header><main id="main"><nav class="nav"><a href="{prefix}index.html">Source library</a><a href="{prefix}field-guide.html">Tools and rigging guide</a><a href="{prefix}coverage.html">68-competency coverage</a><a href="{prefix}gaps.html">Before practical delivery</a><a href="{prefix}downloads.html">ZIP downloads</a><a href="{prefix}../index.html">Asphalt curriculum</a></nav>{body}</main></body></html>'''

def reference(d):
    return f'{esc(d["author"])}. ({esc(d["edition"])}). <cite>{esc(d["title"])}</cite>. <a href="{esc(d["source_url"],quote=True)}">Publisher/source</a>. Retrieved October 30, 2026.'

def archive_web(d, downloads):
    raw = (downloads / d['download_filename']).read_bytes()
    assert sha(raw) == d['original_sha256'], d['id']
    original = BeautifulSoup(raw, 'html.parser')
    content = original.select_one(d['selector'])
    assert content and len(content.get_text(' ', strip=True)) > 150, (d['id'], d['selector'])
    # Scripts, site forms and UI controls do not belong to the selected reading.
    for x in content.select('script, style, iframe, form, button, noscript, input'):
        x.decompose()
    article_text = content.get_text('\n', strip=True)
    images = []
    for tag in content.find_all(True):
        for key in list(tag.attrs):
            if key.lower().startswith('on') or key in ['style', 'srcset', 'sizes']:
                del tag[key]
        if tag.name == 'a' and tag.get('href') and not tag['href'].startswith('#'):
            tag['href'] = urljoin(d['final_url'], tag['href'])
            if urlsplit(tag['href']).scheme not in ['http', 'https', 'mailto', 'tel']:
                del tag['href']
        if tag.name == 'img' and tag.get('src'):
            url = urljoin(d['final_url'], tag['src'])
            key = hashlib.sha256(url.encode()).hexdigest()[:20]
            ext = Path(urlsplit(url).path).suffix.lower()
            if ext not in ['.png', '.gif', '.jpg', '.jpeg', '.svg', '.webp']: ext = '.img'
            path = ROOT / 'web/images' / (key + ext)
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40) as response:
                    image_bytes = response.read()
                    assert 'image' in response.headers.get('Content-Type', ''), url
                path.write_bytes(image_bytes)
            image_bytes = path.read_bytes()
            images.append(dict(source_url=url, file=path.relative_to(ROOT).as_posix(), bytes=len(image_bytes), sha256=sha(image_bytes), alt=tag.get('alt', '')))
            tag['src'] = 'images/' + path.name
            tag['loading'] = 'lazy'
    # Local styling keeps regulation tables legible without changing their text.
    content['class'] = ['source-article']
    raw_path = ROOT / 'web/raw' / (d['slug'] + '.source.html.txt')
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_bytes(raw)
    text_path = ROOT / 'web/text' / (d['slug'] + '.txt')
    write(text_path, article_text + '\n')
    body = f'<aside class="note"><p>{reference(d)}</p><p>{esc(d["scope"])}</p><p><a href="raw/{d["slug"]}.source.html.txt">Original acquired HTML bytes</a> · <a href="text/{d["slug"]}.txt">Article text</a></p></aside><div class="source-scroll">{content}</div>'
    path = ROOT / 'web' / (d['slug'] + '.html')
    write(path, shell(d['title'], body, '../'))
    d.update(file=path.relative_to(ROOT).as_posix(), raw=raw_path.relative_to(ROOT).as_posix(), text=text_path.relative_to(ROOT).as_posix(), text_sha256=sha((article_text+'\n').encode()), article_characters=len(article_text), images=images)
    return d

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--downloads', required=True, type=Path)
    args = p.parse_args()
    catalogue = json.loads((ROOT / 'catalogue.json').read_text())
    previous = json.loads((ROOT / 'manifest.json').read_text()) if (ROOT / 'manifest.json').exists() else {'documents': []}
    cached = {d['original_sha256']: d for d in previous['documents']}
    for record in (ROOT / 'records').glob('*.json'):
        saved = json.loads(record.read_text())
        cached.setdefault(saved['original_sha256'], saved)
    docs = []; search = []
    for d in catalogue['documents']:
        src = args.downloads / d['download_filename']; raw = src.read_bytes()
        assert sha(raw) == d['original_sha256'], d['id']
        original = fitz.open(stream=raw, filetype='pdf'); assert len(original) == d['original_pages']
        old = cached.get(d['original_sha256'])
        valid = old and all((ROOT / q['file']).exists() and sha((ROOT / q['file']).read_bytes()) == q['sha256'] and (ROOT / q['text']).exists() and sha((ROOT / q['text']).read_bytes()) == q['text_sha256'] for q in old['parts'])
        if valid:
            d['parts'] = old['parts']
        else:
            reader = PdfReader(src); parts = []; start = 1
            while start <= len(original):
                end = min(start + 24, len(original))
                while True:
                    data = raw if start == 1 and end == len(original) else native.native_part(reader, start, end)
                    cleaned = False
                    if len(data) > 10 * 1048576:
                        # Some specification pages share enormous resource maps.
                        # Prune unused resources without resampling any image.
                        clean = fitz.open(stream=data, filetype='pdf')
                        for page in clean: page.clean_contents(sanitize=True)
                        smaller = clean.tobytes(garbage=4, deflate=True)
                        if len(smaller) < len(data): data = smaller; cleaned = True
                    if len(data) <= 10 * 1048576: break
                    assert end > start, f'Single page exceeds limit: {d["id"]} {start}'
                    end = start + max(1, (end-start+1)//2) - 1
                stem = f'{d["slug"]}/p{start:04d}-{end:04d}'
                path = ROOT / 'sources' / (stem + '.pdf'); path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
                text = ''; empty = []
                for n in range(start, end+1):
                    t = original[n-1].get_text(sort=True).strip()
                    text += f'=== SOURCE PDF PAGE {n} ===\n' + (t or '[No extractable text; inspect the original page image.]') + '\n\n'
                    if not t: empty.append(n)
                txt = ROOT / 'text' / (stem+'.txt'); write(txt, text)
                parts.append(dict(file=path.relative_to(ROOT).as_posix(), text=txt.relative_to(ROOT).as_posix(), start=start, end=end, pages=end-start+1, bytes=len(data), sha256=sha(data), text_sha256=sha(text.encode()), empty_text_source_pages=empty, original_bytes_preserved=data == raw, unused_resource_cleanup=cleaned))
                start = end+1
            d['parts'] = parts
        for q in d['parts']:
            for n in range(q['start'], q['end']+1):
                search.append(dict(title=d['title'], page=n, href=q['file']+f'#page={n-q["start"]+1}', text=original[n-1].get_text(sort=True)))
        write(ROOT / 'records' / (d['slug']+'.json'), json.dumps(d, indent=2, ensure_ascii=False)+'\n')
        docs.append(d); print(d['id'], len(original), 'pages', len(d['parts']), 'parts', flush=True)
    webs = []
    for d in catalogue['web_documents']:
        webs.append(archive_web(d, args.downloads)); print(d['id'], 'archived', flush=True)
    expected = {q[k] for d in docs for q in d['parts'] for k in ['file', 'text']}
    for folder in ['sources', 'text']:
        for path in (ROOT / folder).rglob('*'):
            if path.is_file() and path.relative_to(ROOT).as_posix() not in expected: path.unlink()
    counts = dict(pdf_publications=len(docs), source_pages=sum(d['original_pages'] for d in docs), pdf_parts=sum(len(d['parts']) for d in docs), web_sources=len(webs), web_figures=sum(len(d['images']) for d in webs), largest_part_bytes=max(q['bytes'] for d in docs for q in d['parts']))
    manifest = dict(schema_version=1, accessed='2026-10-30', policy={'max_pages':25,'max_bytes':10*1048576,'processing':'Native PDF pages retained without downsampling; split parts omit internal/non-URI page links. Small whole publications retain exact original bytes. Oversized shared resource maps are cleaned without image resampling where recorded. Web articles preserve text, tables and local figures; raw HTML bytes are archived as inert text.'}, counts=counts, documents=docs, web_documents=webs)
    write(ROOT / 'manifest.json', json.dumps(manifest, indent=2, ensure_ascii=False)+'\n')
    cards = []
    for d in docs + webs:
        if d['kind'] == 'pdf':
            links = '<ul class="parts">'+''.join(f'<li><strong>Source pages {q["start"]}–{q["end"]}</strong><br><a href="{q["file"]}">PDF</a> · <a href="{q["text"]}">Text</a><span>{q["bytes"]/1048576:.2f} MiB</span></li>' for q in d['parts'])+'</ul>'
            links = f'<details><summary>{d["original_pages"]} pages · {len(d["parts"])} complete-sequence part(s)</summary>{links}</details>'
        else: links = f'<p><a href="{d["file"]}">Read the complete archived article</a> · <a href="{d["text"]}">Text</a></p>'
        cards.append(f'<section class="document source-card" id="{d["id"]}" data-category="{d["category"]}"><p class="tag">{esc(d["category"])} · {"PDF" if d["kind"]=="pdf" else "WEB ARTICLE"}</p><h2>{esc(d["title"])}</h2><p class="small">{reference(d)}</p><p>{esc(d["scope"])}</p>{links}</section>')
    body = f'<p class="stats"><span>{len(docs)} PDF publications</span><span>{counts["source_pages"]:,} source pages</span><span>{counts["pdf_parts"]} small PDF parts</span><span>{len(webs)} archived web sources</span></p><p class="note">Use the <a href="field-guide.html">tools and rigging guide</a> to find the right reading, then open the actual source. Every page of each listed PDF is retained; parts are at most 25 pages and 10 MiB. Publication dates and model limits stay visible. Current project, machine and site requirements must be confirmed before practical delivery.</p><form class="search" id="search-form"><label for="query">Search the acquired PDF page text</label><input id="query" type="search" placeholder="For example: lute, shackle, screed, propane"><button>Search</button> <button id="clear" type="button">Clear</button><p id="status" role="status">Search the text of every source page. Image-only pages require visual reading.</p></form><ol id="results"></ol><label for="category">Browse a source group</label> <select id="category"><option value="">All groups</option>'+''.join(f'<option>{c}</option>' for c in sorted({d['category'] for d in docs+webs}))+'</select>'+''.join(cards)+'<script src="assets/search-index.js"></script><script src="assets/library.js"></script>'
    write(ROOT / 'index.html', shell('Tools, safety and source library', body))
    css = native.CSS + '\nmain img{max-width:100%;height:auto}select{font:inherit;padding:10px;max-width:100%}.source-scroll{overflow:auto}.source-article{background:white;padding:24px;min-width:0}.source-article img{max-width:100%;height:auto}.source-article table{border-collapse:collapse;min-width:300px}.source-article th,.source-article td{border:1px solid #b6ada5;padding:9px;vertical-align:top}.source-article h1,.source-article h2,.source-article h3{color:#1a1512}.source-article .ohs_table_head,.source-article .ohs_table_body{color:#1a1512}.source-article [id]{scroll-margin-top:20px}figure{margin:24px 0}figure img{width:100%;height:auto}figcaption{font-size:14px;color:#625d58}table{width:100%;border-collapse:collapse}td,th{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #d8d0c9}th{background:#fff4d2}.table-wrap{overflow-x:auto}.guide-grid{display:grid;grid-template-columns:1fr 1fr;gap:22px}.guide-grid>section{padding:22px;background:white;border-top:4px solid #d2181f}blockquote{border-left:4px solid #ffbc00;padding:4px 18px;margin:18px 0;background:white}h2{margin-top:38px}h3{margin-top:26px}@media(max-width:700px){.guide-grid{grid-template-columns:1fr}.source-article{padding:14px}}@media print{.source-article{padding:0}.table-wrap{overflow:visible}figure,blockquote{break-inside:avoid}a{color:#1a1512}h2,h3{break-after:avoid}thead{display:table-header-group}tr{break-inside:avoid}}'
    write(ROOT / 'assets/library.css', css + '\n@media print{.signals img{max-height:175mm;object-fit:contain}#skills-practice{break-before:page}}\n')
    js = native.JS.replace('window.CAT_SEARCH','window.READINESS_SEARCH') + '\ndocument.querySelector("#category")?.addEventListener("change",e=>{document.querySelectorAll(".source-card").forEach(c=>c.hidden=!!e.target.value&&c.dataset.category!==e.target.value)});\n'
    write(ROOT / 'assets/library.js', js)
    write(ROOT / 'assets/search-index.js', 'window.READINESS_SEARCH='+json.dumps(search, ensure_ascii=False,separators=(',',':'))+';\n')
    fonts = ROOT / 'assets/fonts'; fonts.mkdir(exist_ok=True)
    for p in (ROOT.parent / 'caterpillar/assets/fonts').iterdir(): shutil.copyfile(p, fonts/p.name)
    print(json.dumps(counts), flush=True)

if __name__ == '__main__': main()
