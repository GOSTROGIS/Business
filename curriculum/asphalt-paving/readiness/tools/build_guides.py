"""Render the editable guide, tool register and complete competency/source map."""
from pathlib import Path
from html import escape as esc
import argparse, csv, hashlib, io, json, re
import fitz, markdown
from bs4 import BeautifulSoup
from build_library import shell, write, ROOT

def readpsv(name): return list(csv.DictReader((ROOT/name).open(), delimiter='|'))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--downloads',type=Path)
    args=parser.parse_args()
    m=json.loads((ROOT/'catalogue.json').read_text())
    sources={d['id']:d for d in m['documents']+m['web_documents']}
    fixed={'cat-library':('CAT source library','../caterpillar/index.html'),'cat-atlas':('Machine parts atlas','../caterpillar/parts-atlas.html'),'whmis':('WHMIS and official symbols','../whmis/index.html'),'outline':('2016 trade outline','../sources/asphalt-paving-laydown-technician-program-outline-august-2016.pdf'),'spec2006':('2006 BC specification','../sources/design_build_standard_specs_2006.pdf')}
    def link(key):
        if key in sources: title,href=sources[key]['title'],'index.html#'+key
        elif key.startswith('ms4:'):
            n=key.split(':')[1];title,href='MS-4 chapter '+str(int(n)),f'../ms-4/reader/chapter-{n}-01.html'
        elif key.startswith('cat:'):title,href='CAT publication '+key[4:],'../caterpillar/index.html#CAT-'+key[4:]
        else:title,href=fixed[key]
        return f'[{title}]({href})'
    def links(s): return '<br>'.join(link(k) for k in s.split(','))
    competencies=list(csv.DictReader((ROOT.parent/'line-a/competency-status.csv').open()))
    mappings=readpsv('coverage-data.psv');bycode={r['code']:r for r in mappings}
    assert len(mappings)==68 and set(bycode)=={r['code'] for r in competencies}
    text='# All 68 competencies: source coverage\n\nEvery row identifies acquired supporting context and the remaining technical or delivery work. This is a source map, not a declaration that all competencies have complete lessons or practical approval. Read the [delivery gap register](gaps.html), [tool register](tools.html) and [visual guide](field-guide.html).\n\n**Scope:** August 2016 outline, source PDF pp. 22–103; Section 4 is audited separately in the delivery gap register. PDF viewer pages are two greater than printed outline pages.\n\n[Download the full CSV](coverage.csv).\n\n'
    rows=[]
    for i,c in enumerate(competencies):
        r=bycode[c['code']];end=int(competencies[i+1]['pdf_page'])-1 if i+1<len(competencies) else 103
        row=dict(code=c['code'],title=c['title'],outline_pdf_start=int(c['pdf_page']),outline_pdf_end=end,topics=r['topics'],source_ids=r['sources'],coverage_status='Supporting context acquired; equipment/site applicability and technical approval pending',remaining=r['remaining'],authoring_status=c['authoring_status'])
        rows.append(row)
        text+=f'## {c["code"]} · {c["title"]}\n\n[Outline source PDF pp. {c["pdf_page"]}–{end}](../sources/asphalt-paving-laydown-technician-program-outline-august-2016.pdf#page={c["pdf_page"]})\n\n**Required context:** {r["topics"]}.\n\n**Acquired sources:** {links(r["sources"])}\n\n**Remaining:** {r["remaining"]}.\n\n**Lesson status:** {c["authoring_status"]}.\n\n'
    write(ROOT/'coverage.md',text.rstrip()+'\n')
    with (ROOT/'coverage.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    toolrows=readpsv('tools-data.psv');assert len(toolrows)==32
    text='# Tools and equipment: complete acquisition register\n\nEvery item named in Section 4 has a row below. Additional items are labelled as task-implied or conditional; they do not silently expand the trade requirements. Manufacturer catalogues and data sheets provide actual identification/specification context where a full operating manual is not acquired. The last column preserves that distinction.\n\n[Download CSV](tools.csv) · [Visual guide](field-guide.html) · [Practical readiness](gaps.html)\n\n| Tool / equipment | Why included; competencies | Components to identify | Actual sources and locator | Remaining equipment information |\n|---|---|---|---|---|\n'
    for r in toolrows:text+=f'| {r["item"]} | {r["basis"]}; {r["codes"]} | {r["identify"]} | {links(r["sources"])}<br>{r["locator"]} | {r["remaining"]} |\n'
    write(ROOT/'tools.md',text)
    with (ROOT/'tools.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(toolrows[0]),lineterminator='\n');w.writeheader();w.writerows(toolrows)
    if args.downloads:
        figures=[]
        for slug,page,clip,name in [('seymour-tool-catalogue-2026',156,(0,0,1,.67),'rakes-and-handwork'),('seymour-tool-catalogue-2026',91,(0,0,1,.57),'tampers'),('seymour-tool-catalogue-2026',94,(0,0,1,.72),'wheelbarrows'),('wsbc-crane-signals',1,(0,0,1,1),'crane-signals')]:
            d=sources[slug];raw=(args.downloads/d['download_filename']).read_bytes();assert hashlib.sha256(raw).hexdigest()==d['original_sha256']
            pdf=fitz.open(stream=raw,filetype='pdf');p=pdf[page-1];r=fitz.Rect(clip[0]*p.rect.width,clip[1]*p.rect.height,clip[2]*p.rect.width,clip[3]*p.rect.height)
            path=ROOT/'assets'/f'{name}.png';p.get_pixmap(dpi=150,clip=r,alpha=False).save(path)
            figures.append(dict(file=path.relative_to(ROOT).as_posix(),source_id=slug,source_sha256=d['original_sha256'],source_pdf_page=page,clip_pdf_points=list(r),processing='PDF page rendered at 150 dpi; stated crop only, no labels removed from the selected illustrations or redrawn.',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),citation=f'{d["author"]}. ({d["edition"]}). {d["title"]} (source PDF p. {page}). {d["source_url"]}'))
        write(ROOT/'figure-manifest.json',json.dumps(figures,indent=2,ensure_ascii=False)+'\n')
    for name in ['field-guide','gaps','coverage','tools']:
        md=(ROOT/(name+'.md')).read_text();title=md.splitlines()[0].lstrip('# ')
        body=markdown.markdown('\n'.join(md.splitlines()[1:]),extensions=['tables','fenced_code','sane_lists'])
        soup=BeautifulSoup(body,'html.parser')
        for t in soup.select('table'):
            wrapper=soup.new_tag('div',attrs={'class':'table-wrap'});t.wrap(wrapper)
        # Ordinary Markdown illustrations have the same responsive behaviour as figures.
        write(ROOT/(name+'.html'),shell(title,str(soup)))
    checks=['Exact six course manuals and instructor package','Actual fleet/model/serial and matching OMM/parts','Site and facility review','Qualified instructors and assessment authority','Rigging gear/load data and qualified lift planning','Propane assembly/SDS and hot-work arrangements','Instrument manuals/checks and prescribed test methods','Nuclear gauge licence/training/transport arrangements','Traffic plan and TCP evidence','Locate ticket and utility responses','Plant/pit jurisdiction and machine documents','Product SDS inventory','First-aid/emergency/exposure/PPE plans','Actual contract and licensed MMCD if used']
    path=ROOT/'delivery-checklist.csv'
    if not path.exists():
        with path.open('w',newline='') as f:
            w=csv.writer(f,lineterminator='\n');w.writerow(['requirement','status','owner','evidence_path','reviewer','review_date','disposition']);w.writerows([[x,'Pending','','','','',''] for x in checks])
    print(json.dumps({'competencies':len(rows),'tool_groups':len(toolrows),'guides':4}))

if __name__=='__main__':main()
