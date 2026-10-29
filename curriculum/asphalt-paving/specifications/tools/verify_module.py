"""Offline integrity, mathematics, accessibility and generated-document checks."""
from __future__ import annotations
import csv, hashlib, json, re, sys
from decimal import Decimal as D
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
errors=[];checks=0;stats={}
def check(ok,message):
    global checks
    checks+=1
    if not ok:errors.append(message)
def readcsv(name):
    with (ROOT/'data'/name).open(newline='') as f:return list(csv.DictReader(f))
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.images=[];self.ids=set();self.toc={};self.active=None;self.tables=0;self.figures=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for key in ('href','src'):
            if a.get(key):self.links.append(a[key])
        if tag=='img':self.images.append(a)
        if tag=='table':self.tables+=1
        if tag=='figure':self.figures+=1
        if tag=='span' and a.get('data-toc-target'):self.active=a['data-toc-target'];self.toc[self.active]=''
    def handle_data(self,data):
        if self.active:self.toc[self.active]+=data
    def handle_endtag(self,tag):
        if tag=='span':self.active=None

def verify_source():
    m=json.loads((ROOT/'source-metadata.json').read_text());p=(ROOT/m['file']).resolve();data=p.read_bytes();r=PdfReader(p)
    check(hashlib.sha256(data).hexdigest()==m['sha256'],'Original specification hash changed')
    check(len(data)==m['bytes'],'Original specification byte count changed')
    check(len(r.pages)==m['pdf_pages']==441,'Original specification page count mismatch')
    manifest=json.loads((ROOT.parent/'sources/manifest.json').read_text());entries=[v for v in manifest if v['source_id']=='BC-MOT-DBSS-2006']
    check(len(entries)==1 and entries[0]['sha256']==m['sha256'],'Source library manifest entry mismatch')
    check('2006' in r.pages[0].extract_text() and 'FEBUARY 20, 2006' in r.pages[0].extract_text(),'Cover edition/adoption text not found')
    for n,markers in {286:['TABLE 501-E','501.15.03'],287:['TABLE 501-F','running average of four consecutive tests'],299:['502.04.04','Road Checker'],300:['every 10 loads','Net Weight'],309:['502.14.01','tonnage delivered']}.items():
        text=' '.join(r.pages[n-1].extract_text().split())
        check(all(marker in text for marker in markers),f'Source location changed: PDF {n}')
    stats['source_pages']=len(r.pages)

def verify_math():
    grading=readcsv('gradation.csv')
    expected=[('12.5',84,95),('9.50',73,90),('4.75',50,75),('2.36',35,57),('0.600',18,34),('0.075',3,7)]
    check([(x['Sieve_mm'],int(x['Historical_lower_pct']),int(x['Historical_upper_pct'])) for x in grading]==expected,'Selected Table 501-E transcription changed')
    a_bad=[];b_bad=[]
    for x in grading:
        lo,hi=D(x['Historical_lower_pct']),D(x['Historical_upper_pct'])
        for col,out in [('Fictional_sample_A_pct',a_bad),('Fictional_sample_B_pct',b_bad)]:
            v=D(x[col])
            if not lo<=v<=hi:out.append((x['Sieve_mm'],min(abs(v-lo),abs(v-hi))))
    check(not a_bad and b_bad==[('12.5',D(1)),('4.75',D(1))],'Sample comparisons disagree with key')
    check(D(grading[0]['Fictional_sample_A_pct'])/100*1000==900 and D(grading[-1]['Fictional_sample_A_pct'])/100*1000==50,'Passing-mass examples disagree')
    means=readcsv('running-means.csv');m=means[0];vals=[D(m[f'Test_{i}_pct']) for i in range(1,6)]
    check(sum(vals[:4])/4==63 and sum(vals[1:])/4==65,'Moving means disagree with key')
    e=means[1];mean=sum(D(e[f'Test_{i}_pct']) for i in range(1,5))/4
    check(mean==D('49.5') and mean-D(e['Curve_pct'])==D('-1.5') and mean<D(e['Historical_lower_pct']),'Two-constraint example disagrees')
    check(all(D(row['Historical_tolerance_pp'])==D('4.5') and D(row['Historical_lower_pct'])==50 and D(row['Historical_upper_pct'])==75 for row in means),'Table 501-F or interval input changed')
    loads=readcsv('load-register-v1.csv');ids=[r['Ticket'] for r in loads]
    check(len(ids)==len(set(ids))==10 and ids==[f'T{i:04}' for i in range(601,611)],'Ticket set changed or duplicated')
    total=sum(D(x['Net_load_t']) for x in loads);check(total==200,'Version 1 total disagrees with key')
    times=[int(x['Delivery_time'].split(':')[0])*60+int(x['Delivery_time'].split(':')[1]) for x in loads]
    check(times[-1]-times[0]==90 and all(b-a==10 for a,b in zip(times,times[1:])),'Delivery time/elapsed example disagrees')
    check(loads[5]['Ticket']=='T0606' and D(loads[5]['Net_load_t'])==20,'T0606 spreadsheet row mapping changed')
    changes=readcsv('corrections-v2.csv');check(len(changes)==2,'Correction count changed')
    c=next(x for x in changes if x['Record']=='T0606');total2=total-D(c['Old_value'])+D(c['New_value']);check(total2==198,'Version 2 corrected mass disagrees')
    areas={}
    for row in readcsv('area-records.csv'):
        areas[(row['Version'],row['Component'])]=D(row['Length_m'])*D(row['Width_m'])
    check(areas=={('1','Main'):D(800),('1','Letdown'):D(200),('2','Main'):D(800),('2','Letdown'):D(300)},'Area component data disagrees')
    a1=sum(v for (ver,_),v in areas.items() if ver=='1');a2=sum(v for (ver,_),v in areas.items() if ver=='2')
    rate1=total*1000/a1;rate2=total2*1000/a2
    check((a1,a2,rate1,rate2)==(1000,1100,200,180),'Area/rate answers disagree')
    check(rate2/rate1*100==90 and (rate2-rate1)/rate1*100==-10,'Ratio/relative change answers disagree')
    check(total+18==218 and total2*1000/800==D('247.5') and total2/a2==D('.18'),'SP-16 flawed-input calculations changed')
    key=(ROOT/'instructor.md').read_text()
    for token in ['200,000 kg','198,000 kg','1,100 m²','180 kg/m²','49.5%','247.5 kg/m²','−10%']:
        check(token in key,'Worked answer missing: '+token)
    stats['csv_datasets']=5;stats['activity_ids']=18;stats['skills']=9

def verify_content():
    expected={f'SP-{i:02}' for i in range(1,19)}
    for name in ['learner.md','instructor.md']:
        text=(ROOT/name).read_text();ids=re.findall(r'^### (SP-\d{2})\b',text,re.M)
        check(set(ids)==expected and len(ids)==18,f'{name}: expected 18 unique task/key headings')
    key=(ROOT/'instructor.md').read_text()
    for skill in ['Reading','Writing','Numeracy','Digital','Problem solving','Communication','Collaboration','Adaptability','Creativity and innovation']:
        check('| '+skill+' |' in key,f'Missing skill evidence row: {skill}')
    session_rows=[line for line in key.splitlines() if re.match(r'\| [1-4] · ',line)]
    check(len(session_rows)==4,'Expected four session allocation rows')
    for row in session_rows:
        cells=[x.strip() for x in row.split('|')[1:-1]]
        minutes=[int(n) for n in re.findall(r'(?:^|\s)(\d+)(?=;|$)',cells[1])]
        check(sum(minutes)==int(cells[2])==90,'Printed session allocation does not total 90: '+cells[0])
    for name in ['learner.md','instructor.md','source-map.md']:
        text=(ROOT/name).read_text()
        check('2006' in text and 'Lot' in text,f'{name}: edition/Lot boundary absent')

def verify_assets():
    svgpaths=list((ROOT/'assets/diagrams').glob('*.svg'));check(len(svgpaths)==5,'Expected five teaching diagrams')
    for p in svgpaths:
        root=ET.parse(p).getroot();tags=[x.tag.rsplit('}',1)[-1] for x in root.iter()]
        check(root.tag.endswith('svg') and bool(root.get('viewBox')),f'{p.name}: SVG root/viewBox')
        check(any(x.tag.endswith('title') and ''.join(x.itertext()).strip() for x in root) and any(x.tag.endswith('desc') and ''.join(x.itertext()).strip() for x in root),f'{p.name}: title/desc')
        check(not any(t in {'script','foreignObject'} for t in tags),f'{p.name}: script/foreignObject')
        refs=[v for node in root.iter() for k,v in node.attrib.items() if k.rsplit('}',1)[-1] in {'href','src'}]
        check(all(v.startswith('#') for v in refs),f'{p.name}: external references')
    css=ROOT/'assets/module.css'
    for ref in re.findall(r'url\([\'"]?([^\)\'\"]+)',css.read_text()):check((css.parent/ref).resolve().is_file(),'Missing font: '+ref)
    stats['svg_figures']=len(svgpaths)

def verify_generated():
    parsed={}
    for name in ['index','learner-workbook','teaching-guide','source-map','source-excerpts']:
        path=ROOT/f'{name}.html';check(path.is_file(),f'Missing HTML: {name}')
        if not path.exists():continue
        p=Page();p.feed(path.read_text());parsed[name]=p
        for ref in p.links:
            url=urlsplit(ref)
            if url.scheme or url.netloc:continue
            target=(path.parent/unquote(url.path)).resolve() if url.path else path
            if target==ROOT/'validation.json':continue  # This verifier writes that report after all checks.
            check(target.is_file(),f'{name}: missing local target {ref}')
            if target.suffix=='.pdf' and url.fragment.startswith('page=') and target.is_file():
                number=int(url.fragment.split('=')[1]);check(1<=number<=len(PdfReader(target).pages),f'{name}: source page outside PDF {ref}')
            if not url.path and url.fragment:check(unquote(url.fragment) in p.ids,f'{name}: missing local anchor {ref}')
        for img in p.images:check(bool(img.get('alt','').strip()),f'{name}: empty image alt')
        html=path.read_text()
        check(html.count('<figure')==html.count('<figcaption>'),f'{name}: figure/caption mismatch')
        check(not re.search(r'<td[^>]*>\s*#{2,}',html),f'{name}: heading swallowed by table')
    for stem in ['learner-workbook','teaching-guide']:
        path=ROOT/f'{stem}.pdf';check(path.is_file(),f'Missing PDF: {stem}')
        if not path.exists():continue
        r=PdfReader(path);texts=[p.extract_text() or '' for p in r.pages];combined='\n'.join(texts)
        check(all(len(t.strip())>30 for t in texts),f'{stem}: empty/unreadable page')
        for i in range(1,19):check(f'SP-{i:02}' in combined,f'{stem}: missing printed activity SP-{i:02}')
        for page in r.pages:
            for ref in page.get('/Annots',[]):
                action=ref.get_object().get('/A')
                if action and action.get('/URI'):
                    uri=str(action['/URI']);check(not any(v in uri for v in ['localhost','127.0.0.1','file://','/workspace/']),f'{stem}: local-only PDF annotation')
        names={str(k).lstrip('/'):r.get_destination_page_number(v)+1 for k,v in r.named_destinations.items()}
        for anchor,label in parsed.get(stem,Page()).toc.items():
            check(label.strip().isdigit() and names.get(anchor)==int(label.strip()),f'{stem}: printed TOC page mismatch for {anchor}')
        stats[stem+'_pages']=len(r.pages)

def main():
    for fn in [verify_source,verify_math,verify_content,verify_assets,verify_generated]:
        try:fn()
        except Exception as e:check(False,f'{fn.__name__}: {type(e).__name__}: {e}')
    report={'checks':checks,'errors':errors,'status':'passed' if not errors else 'failed','counts':stats,'scope':'Offline source integrity, selected table data, arithmetic, activity/skill coverage, local assets, HTML/PDF links and PDF TOC destinations; not technical sign-off or a classroom pilot.'}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
