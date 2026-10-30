"""Package every source part and the web/guide collection in small offline ZIPs."""
from pathlib import Path
from html import escape as esc
from urllib.parse import urlsplit,unquote
import hashlib,io,json,zipfile
from bs4 import BeautifulSoup
from build_library import ROOT,shell,write,reference
PUBLIC='https://github.com/GOSTROGIS/Business/blob/main/curriculum/asphalt-paving/readiness/'
MAX=40*1048576
def sha(b):return hashlib.sha256(b).hexdigest()
def zipbytes(files):
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,(2026,10,30,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,data)
    return out.getvalue()
def save(name,files,record):
    data=zipbytes(files);assert len(data)<MAX,(name,len(data))
    path=ROOT/'downloads'/name;path.parent.mkdir(exist_ok=True);path.write_bytes(data)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None
        assert set(z.namelist())==set(files)
        for key,value in files.items():assert z.read(key)==value
    return dict(file=path.relative_to(ROOT).as_posix(),bytes=len(data),sha256=sha(data),members=len(files),**record)

def main():
    m=json.loads((ROOT/'manifest.json').read_text());assets={p.relative_to(ROOT).as_posix():p.read_bytes() for p in (ROOT/'assets/fonts').iterdir()};assets['assets/library.css']=(ROOT/'assets/library.css').read_bytes()
    volumes=[];batch=[];size=0
    # 38 MiB uncompressed leaves space for indices/fonts and guarantees small ZIPs.
    for d in m['documents']:
        for q in d['parts']:
            amount=q['bytes']+(ROOT/q['text']).stat().st_size
            if batch and size+amount>38*1048576:volumes.append(batch);batch=[];size=0
            batch.append((d,q));size+=amount
    if batch:volumes.append(batch)
    results=[]
    for n,batch in enumerate(volumes,1):
        files=dict(assets);cards=[];included=[]
        for d,q in batch:
            for key in ['file','text']:files[q[key]]=(ROOT/q[key]).read_bytes()
            record='records/'+d['slug']+'.json';files[record]=(ROOT/record).read_bytes()
            included.append(dict(source_id=d['id'],start=q['start'],end=q['end'],file=q['file'],sha256=q['sha256']))
            cards.append(f'<section class="document"><h2>{esc(d["title"])}</h2><p>{reference(d)}</p><p>{esc(d["scope"])}</p><p><strong>Original source PDF pages {q["start"]}–{q["end"]}</strong> · <a href="{q["file"]}">Open PDF</a> · <a href="{q["text"]}">Text</a></p></section>')
        title=f'Asphalt source PDFs · volume {n:02d} of {len(volumes):02d}'
        files['index.html']=(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><link rel="stylesheet" href="assets/library.css"></head><body><header><div><p>ACCESS · INDIGENOUS SKILLS 4 SUCCESS</p><h1>{title}</h1></div></header><main><p class="note">This volume contains the exact source-page ranges listed below. Publications may continue in another volume. Download all PDF volumes to obtain all 41 publications and 3,240 pages. The separate web/guide volume contains the illustrated guide, tool register, competency map and archived regulatory articles.</p>'+''.join(cards)+'</main></body></html>').encode()
        files['README-OFFLINE.txt']=(title+'\n\nExtract this ZIP into its own folder and open index.html. PDF parts and text open locally. Publisher links require internet. Page ranges are original source PDF viewer pages, not printed page labels. All original publication notices are retained. Model/edition applicability still needs verification. Other volumes contain the rest of the collection; consult the repository downloads page for checksums and ranges.\n').encode()
        files['volume-manifest.json']=json.dumps(dict(volume=n,volumes=len(volumes),parts=included),indent=2).encode()
        results.append(save(f'asphalt-context-pdfs-{n:02d}.zip',files,dict(type='pdf-volume',title=title,parts=included,pages=sum(q['pages'] for d,q in batch))))
    # The complete web articles and guide are usable offline. Links to PDFs in
    # other ZIPs and other curriculum collections point to their repository files.
    keep=[]
    for folder in ['assets','web']:
        keep.extend(p for p in (ROOT/folder).rglob('*') if p.is_file())
    keep.extend(p for p in ROOT.iterdir() if p.is_file() and p.suffix in ['.html','.md','.csv','.json','.pdf','.psv'] and p.name not in ['downloads.html','downloads.json','archive-checks.json','pdf-page-checks.json','VALIDATION.md','verification.json'])
    paths={p.resolve() for p in keep};files={}
    for p in keep:
        data=p.read_bytes()
        if p.suffix=='.html':
            s=BeautifulSoup(data,'html.parser')
            for a in s.select('a[href]'):
                u=urlsplit(a['href'])
                if u.scheme or u.netloc or not u.path:continue
                target=(p.parent/unquote(u.path)).resolve()
                if target not in paths:
                    repo=ROOT.parents[2];rel=target.relative_to(repo).as_posix()
                    a['href']='https://github.com/GOSTROGIS/Business/blob/main/'+rel+('?' +u.query if u.query else '')+('#'+u.fragment if u.fragment else '')
            data=str(s).encode()
        files[p.relative_to(ROOT).as_posix()]=data
    files['README-OFFLINE.txt']=b'ACCESS IS4S asphalt tools, safety and preparation\n\nOpen field-guide.html for the illustrated route, tools.html for all equipment groups, coverage.html for all 68 competencies, gaps.html for remaining provider requirements, or index.html for the catalogue. Regulatory articles and their figures are included locally. Links to source PDF parts and other curriculum collections open GitHub; use the separate PDF ZIP volumes for offline PDFs. Raw publisher HTML is preserved as inert .txt. Technical dates and model limits remain part of each record.\n'
    results.append(save('asphalt-context-web-and-guides.zip',files,dict(type='web-and-guides',title='Visual guide, 68-competency map, tool register and 30 complete web articles')))
    write(ROOT/'downloads.json',json.dumps(dict(limit_bytes=MAX,archives=results),indent=2)+'\n')
    body='<p class="note">Download all PDF volumes for the complete 41-publication / 3,240-page addition. Each ZIP is below 40 MiB. Extract volumes into separate folders and open their index.html files. Each PDF part is at most 25 pages and 10 MiB. The web/guide ZIP contains all 30 archived web articles and their figures; it links to GitHub for PDFs that are in the other ZIPs.</p>'
    for r in results:
        body+=f'<section class="document"><h2>{esc(r["title"])}</h2><p><a href="{r["file"]}">Download ZIP</a> · {r["bytes"]/1048576:.2f} MiB · {r["members"]} files</p><p class="small">SHA-256: {r["sha256"]}</p>'
        if r['type']=='pdf-volume':
            body+='<details><summary>Included original source page ranges</summary><ul>'+''.join(f'<li>{esc(p["source_id"])} · pages {p["start"]}–{p["end"]}</li>' for p in r['parts'])+'</ul></details>'
        body+='</section>'
    write(ROOT/'downloads.html',shell('Download the source collection',body))
    print(json.dumps([dict(file=r['file'],bytes=r['bytes'],members=r['members']) for r in results],indent=2))
if __name__=='__main__':main()
