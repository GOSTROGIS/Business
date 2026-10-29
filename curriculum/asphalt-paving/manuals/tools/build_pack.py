"""Build self-contained ACCESS manual-navigation pages, lesson PDFs and source ZIP.
From the repository root, install curriculum/asphalt-paving/tools/requirements.txt,
then run python curriculum/asphalt-paving/manuals/tools/build_pack.py.
Original source files are preserved byte-for-byte.
"""
from pathlib import Path
from html import escape
import hashlib,json,re,zipfile,os,shutil
from urllib.parse import urlsplit
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject,TextStringObject
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
import markdown
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
CSS='''
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#F7F4F1;color:#1A1512;font:17px/1.58 Arial,Helvetica,sans-serif}header{background:#1A1512;color:#fff;padding:36px 28px;border-bottom:8px solid #FFBC00}header .inner,main{max-width:1080px;margin:auto}header h1{font-size:clamp(30px,4vw,46px);line-height:1.12;max-width:850px;margin:.3em 0}header p{max-width:820px}.eyebrow{font-size:13px;letter-spacing:.13em;text-transform:uppercase;color:#FFBC00;font-weight:bold}main{padding:30px 24px 60px}h2{font-size:25px;line-height:1.25;margin-top:1.7em}h3{font-size:20px;line-height:1.3;color:#9e171c;margin-top:1.5em}p,li,td{overflow-wrap:anywhere}a{color:#a0181e;text-underline-offset:3px}a:focus-visible{outline:3px solid #D2181F;outline-offset:4px}header a{color:#fff}.lead{font-size:20px}.actions{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}.button{background:#D2181F;color:#fff;padding:11px 17px;text-decoration:none;font-weight:bold;border-radius:5px}.button.light{background:#fff;color:#1A1512;border:1px solid #b9b0a9}.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.card,article,.note{background:#fff;border:1px solid #ddd4cc;border-radius:7px;padding:25px}.card{border-top:5px solid #D2181F}.card h3{margin:.3em 0 .7em}.tag{font-size:13px;text-transform:uppercase;font-weight:bold;letter-spacing:.05em}.scope{font-size:15px}.serial{border-left:4px solid #FFBC00;padding-left:12px}.meta{font-size:14px;color:#51483f}table{border-collapse:collapse;width:100%;margin:20px 0;font-size:.9em}th,td{padding:10px;border:1px solid #cfc6be;text-align:left;vertical-align:top}th{background:#eee7e0}thead{display:table-header-group}.table-wrap{overflow:auto}.table-wrap:focus{outline:2px solid #D2181F}code{font-size:.9em;white-space:normal;overflow-wrap:anywhere;background:#f0ece8;padding:1px 4px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0ece8;padding:18px;font-size:13px;line-height:1.4}pre code{padding:0;background:none}nav{margin:0 0 22px}nav a{margin-right:20px}.skip{position:absolute;left:-9999px}.skip:focus{left:10px;top:10px;background:white;color:#1A1512;padding:10px}.skill{white-space:nowrap}@media(max-width:680px){.cards{grid-template-columns:1fr}main{padding:18px 12px}header{padding:28px 18px}.card,article{padding:18px}th,td{padding:6px}table{font-size:.82em}}
@page{size:Letter;margin:16mm 15mm 18mm}@media print{html{scroll-behavior:auto}body{background:#fff;font-size:10.5pt;line-height:1.43}header{background:#fff;color:#1A1512;border-bottom:3px solid #D2181F;padding:0 0 8mm}header h1{font-size:26pt}.eyebrow{color:#1A1512}main{padding:8mm 0 0;max-width:none}article{border:0;padding:0}nav,.screen,.actions{display:none}h2{font-size:16pt;margin-top:1.3em}h3{font-size:12.5pt}h1,h2,h3{break-after:avoid}p,li{orphans:3;widows:3}table{font-size:8.8pt;table-layout:auto}th,td{padding:6px}tr{break-inside:avoid}.table-wrap{overflow:visible}pre{font-size:9pt}a{color:#1A1512}.card{break-inside:avoid}.cards{display:block}.card{margin-bottom:8mm}}
'''

def page(title,body,tagline='Read the identity. Find the evidence. Explain the limit.'):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | ACCESS IS4S</title><style>{CSS}</style></head><body><a class="skip" href="#main">Skip to content</a><header><div class="inner"><p class="eyebrow">ACCESS · Indigenous Skills 4 Success · Asphalt curriculum</p><h1>{escape(title)}</h1><p>{escape(tagline)}</p></div></header><main id="main">{body}</main></body></html>'''

def md_page(src):
 t=src.read_text();title=t.splitlines()[0].lstrip('# ');body='\n'.join(t.splitlines()[1:])
 body=markdown.markdown(body,extensions=['tables','fenced_code','sane_lists'])
 body=re.sub(r'<table>.*?</table>',lambda m:'<div class="table-wrap" tabindex="0" role="region" aria-label="Reading table">'+m[0]+'</div>',body,flags=re.S)
 body=body.replace('<th>','<th scope="col">')
 body=re.sub(r'(?<![\w"-])((?:OEM|MAN|REF)-\d{2})(?![\w"-])',r'<span class="skill">\1</span>',body)
 return title,body

manifest=json.loads((ROOT/'manifest.json').read_text())
for name in ['lesson','instructor','access-status']:
 title,body=md_page(ROOT/f'{name}.md')
 (ROOT/f'{name}.html').write_text(page(title,'<nav class="screen"><a href="index.html">All manuals</a></nav><article>'+body+'</article>'))
for src in (ROOT/'extracts').glob('*.md'):
 title,body=md_page(src)
 (src.with_suffix('.html')).write_text(page(title,'<nav class="screen"><a href="../index.html">All manuals</a></nav><article>'+body+'</article>'))
cards=[]
for d in manifest['documents']:
 local=escape(d['local_file'],quote=True);size=d['bytes']/1e6
 measure=f"{d['pdf_pages']} PDF pages · {d['bytes']:,} bytes" if d['format']=='PDF' else f"{d['collection_file_count']} local files · {d['collection_bytes']:,} bytes"
 links=f'<a href="{local}">Open complete {"PDF" if d["format"]=="PDF" else "HTML manual"}</a>'
 if d.get('navigation_extract'):links+=f' · <a href="{escape(d["navigation_extract"].replace(".md",".html"))}">Identity and page map</a>'
 if d.get('source_url'):links+=f' · <a href="{escape(d["source_url"],quote=True)}">Official source</a>'
 cards.append(f'''<section class="card"><span class="tag">{escape(d['id'])} · {escape(d['brand'])}</span><h3>{escape(d['title'])}</h3><p class="meta">{escape(d['document_number'])}<br>{escape(d['edition'])}</p><p class="serial">{escape(d.get('serial_scope') or 'Historical specification; no machine serial scope.')}</p><p class="scope">{escape(d['document_scope'])}</p><p class="meta">{measure}</p><p>{links}</p></section>''')
body='''<nav aria-label="Pack navigation"><a href="#documents">Original manuals</a><a href="lesson.html">Learner lesson</a><a href="instructor.html">Teaching guidance</a><a href="access-status.html">Section 4 access status</a><a href="manifest.json">Manifest</a></nav><p class="lead">Seven complete manufacturer references, with the identity and scope kept beside every file.</p><p>Six OEM PDFs contain 650 pages. The John Deere 410G manual is a complete 675-file HTML collection. A separate 441-page historical B.C. specification is also included. Short navigation extracts are clearly separate from the full originals.</p><div class="actions"><a class="button" href="lesson.html">Start the manual-reading lesson</a><a class="button light" href="manual-reading-lesson.pdf">Print learner lesson</a><a class="button light" href="manual-reading-instructor.pdf">Print answer guidance</a></div><section class="note"><strong>Use the document that fits the question.</strong><p>Model, serial/configuration, edition and document type determine what a source can answer. This dated classroom collection does not establish actual-machine applicability. The original six course manuals named by Section 4 were not retrieved; see the <a href="access-status.html">clear resource-status record</a>.</p></section><h2 id="documents">Open an original reference</h2><div class="cards">'''+''.join(cards)+'''</div><h2>Keep a checkable record</h2><p><a href="README-OFFLINE.md">Offline reading instructions</a> · <a href="checksums.sha256">File checksums</a> · <a href="deere-file-manifest.json">Deere per-file source record</a></p><p class="meta">Retrieved 29 October 2026. Original source payload: 60,576,733 bytes. Manufacturer copyright and notices remain intact. External source and purchase links need an internet connection; the local documents and lesson do not.</p>'''
(ROOT/'index.html').write_text(page('Manufacturer manuals for thoughtful practice',body,'Complete originals, clear scope and a practical lesson across all nine Skills for Success.'))
class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/'
with sync_playwright() as p:
 executable=os.environ.get('IS4S_CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome')
 options={'headless':True,'args':['--no-sandbox']}
 if executable: options['executable_path']=executable
 browser=p.chromium.launch(**options)
 for name,stem in [('lesson','manual-reading-lesson'),('instructor','manual-reading-instructor')]:
  tab=browser.new_page();tab.goto(base+f'{name}.html');tab.emulate_media(media='print')
  tab.pdf(path=str(ROOT/f'{stem}.pdf'),print_background=True,prefer_css_page_size=True,tagged=True,outline=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="font:9px Arial;width:100%;padding:0 15mm;color:#51483f;display:flex;justify-content:space-between"><span>ACCESS IS4S · Manual reading</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
  tab.close()
  # Printed links must outlive the temporary local server; preserve page fragments.
  target=ROOT/f'{stem}.pdf';reader=PdfReader(target);writer=PdfWriter();writer.clone_document_from_reader(reader)
  for pdf_page in writer.pages:
   for ref in pdf_page.get('/Annots',[]):
    annotation=ref.get_object();action=annotation.get('/A')
    if action and action.get('/URI'):
     uri=str(action['/URI'])
     if uri.startswith(base):
      parts=urlsplit(uri);stable='https://github.com/GOSTROGIS/Business/blob/main/curriculum/asphalt-paving/manuals/'+parts.path.lstrip('/')
      if parts.query:stable+='?'+parts.query
      if parts.fragment:stable+='#'+parts.fragment
      action[NameObject('/URI')]=TextStringObject(stable)
  temp=target.with_suffix('.tmp.pdf');writer.write(temp);temp.replace(target)
 browser.close()
server.shutdown();server.server_close()
# Checksums cover every packaged file except the checksum list itself.
def members():
 return sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name not in {'README.md','asphalt-manuals-resource-pack.zip','archive-info.json','checksums.sha256'} and 'tools' not in p.relative_to(ROOT).parts)
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix() for p in members()]
(ROOT/'checksums.sha256').write_text('\n'.join(lines)+'\n')
archive=ROOT/'asphalt-manuals-resource-pack.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in members()+[ROOT/'checksums.sha256']:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert all(not n.startswith('/') and '..' not in Path(n).parts for n in z.namelist())
 count=len(z.infolist());expanded=sum(i.file_size for i in z.infolist())
raw=archive.read_bytes();assert len(raw)<100_000_000,'Archive exceeds repository file limit'
info=dict(file=archive.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),entries=count,uncompressed_bytes=expanded,zip_crc_check='passed',relative_paths_check='passed')
(ROOT/'archive-info.json').write_text(json.dumps(info,indent=2)+'\n')
rows=[]
for d in manifest['documents']:
 count_text=f"{d['pdf_pages']} pages" if d['format']=='PDF' else '307 content sections + contents, images and styles'
 rows.append(f"| {d['id']} | [{d['title']}]({d['local_file']}) | {count_text} | {d['document_scope']} |")
readme=f'''# ACCESS IS4S · Asphalt manufacturer manual resource pack

[Download the complete ZIP](asphalt-manuals-resource-pack.zip) — **{len(raw):,} bytes** ({len(raw)/1e6:.2f} MB), **{count} files**, **{expanded:,} bytes** when extracted. ZIP SHA-256: `{info['sha256']}`.

[Open the offline-friendly manual index](index.html) · [Learner lesson](lesson.html) · [Printable learner PDF](manual-reading-lesson.pdf) · [Teaching and answer PDF](manual-reading-instructor.pdf)

The pack contains **seven complete OEM references**: six original PDFs totaling **650 pages**, and the full official John Deere 410G HTML manual with **307 content sections** plus its contents, images and styles. A separate **441-page historical 2006 B.C. Design Build specification** is included from the user-supplied original. Original source payload is **60,576,733 bytes** before authored pages and metadata.

| ID | Original document | Extent | Scope |
|---|---|---|---|
'''+ '\n'.join(rows)+'''

Extract the ZIP and open `index.html`. All local manuals, images, styles, lessons and answer guidance work offline. The archive uses an internal `README-OFFLINE.md`; this repository README and the ZIP itself are excluded to avoid circular download links. External manufacturer/provider links remain online references.

The **pdfs/** files are full originals. The **extracts/** files contain short cover extracts and original identity/navigation notes; they are not complete manuals. The **deere-410g-omt166701-d1/** directory preserves the full retrieved original HTML collection. **manifest.json** identifies each model, serial/configuration scope, publication, source URL, date, size and hash. **deere-file-manifest.json** covers all 675 Deere files. **checksums.sha256** and **archive-info.json** record integrity evidence.

The standalone lesson uses real manual identities and fictional machine records to practise all nine Skills for Success. It includes individual digital actions, inclusive page-range arithmetic, an unresolved serial-range case, a written handover, check-back, shared verification, a changed record and a tested navigation aid. Instructor answers and criteria are separate.

Section 4 of the uploaded outline lists six **course manuals**—Common Core, Raker, Compaction Roller, Screed, Paver and Milling Machine—and other resources. Those exact course publications were not retrieved. The OEM files are not relabelled as them. Read [the precise requirement and access gaps](access-status.md) for the provider route, historical CD titles and MS-4 handbook status. CAT engine/fluids manuals do not replace a complete CAT paving-machine manual; Deere 410G is a backhoe-loader reference for supporting roadbuilding work.

Manufacturer copyright and notices remain intact. This is a dated reference collection, checked 29 October 2026, not a claim that every file is current for any actual machine. Confirm model, serial/configuration, current documentation and authorized training before practical application.

From the repository root, install `python -m pip install -r curriculum/asphalt-paving/tools/requirements.txt`, then run `python curriculum/asphalt-paving/manuals/tools/build_pack.py`. The build uses Markdown, Playwright and pypdf. It detects Chromium on PATH; set `IS4S_CHROMIUM_PATH` to choose another executable, or install the Playwright browser with `python -m playwright install chromium`. Original manufacturer files remain unchanged. Printed lesson links use stable repository URLs; offline navigation remains available through index.html.
'''
(ROOT/'README.md').write_text(readme)
print(json.dumps(info,indent=2))
