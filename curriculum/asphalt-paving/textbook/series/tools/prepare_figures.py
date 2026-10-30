"""Retain source identities and exact crop coordinates for all manual figures."""
from pathlib import Path
import json,hashlib,os
import fitz
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R.parents[1];OUT=R/'assets/crops';OUT.mkdir(exist_ok=True)
figs={};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def add(id,path,title,alt,credit,link=None,provenance=None):
 figs[id]={'id':id,'file':os.path.relpath(path,R),'title':title,'alt':alt,'credit':credit,'source_link':link,'sha256':sha(path),'provenance':provenance or {}}
for x in json.loads((R.parent/'figures.json').read_text())['figures']:
 add(x['id'],R.parent/x['file'],x['title'],x['alt'],x['credit'],os.path.relpath((R.parent/x['source_link']).resolve(),R) if x.get('source_link') and not x['source_link'].startswith('http') else x.get('source_link'),x.get('provenance'))
cat={x['id']:x for x in json.loads((A/'caterpillar/catalogue.json').read_text())['documents']}
for x in json.loads((A/'caterpillar/atlas.json').read_text())['figures']:
 d=cat[x['document']];year=d.get('publication_year') or 'n.d.';credit=f"Caterpillar. ({year}). {d['title']} ({d.get('publication','publication identity in source')}, source PDF p. {x['source_page']}). Faithful crop; original labels retained. {x['scope']}"
 add('cat-'+x['id'],A/'caterpillar'/x['file'],x['title'],x['title']+'. '+x['scope'],credit,'../../caterpillar/parts-atlas.html#'+x['id'],x)
# Existing MS-4 redraws retain their adaptation/contributor records.
for x in json.loads((A/'ms-4/concepts/figure-manifest.json').read_text())['figures']:
 credit=x['source']+' Original instructional adaptation by ACCESS IS4S (2026). '+x['adaptation']+' Source locations: '+json.dumps(x['references'],ensure_ascii=False)+'. Original contributors: '+('; '.join(c['credit'] for c in x.get('original_contributors',[])) or 'No separate contributor listed for this figure.')
 add(x['id'],A/'ms-4/concepts'/x['file'],x['title'],x['alt'],credit,'../../ms-4/concepts/index.html',x)
# Road layers and screed factors reuse verified conceptual redraws.
figs['road-layers']={**figs['pavement-layers'],'id':'road-layers'}
for x in json.loads((A/'readiness/figure-manifest.json').read_text()):
 id=Path(x['file']).stem
 add(id,A/'readiness'/x['file'],id.replace('-',' ').title(),'Original manufacturer illustrations with labels retained; inspect the full-size figure.',x['citation']+' Faithful source crop.','../../readiness/index.html',x)
add('handwork-tools',A/'readiness/assets/handwork-anatomy.svg','Name the parts of a handwork tool','Lute and handwork tool anatomy with head, working edge, handle and connection points.','ACCESS IS4S. (2026). Handwork tool anatomy [Original instructional SVG]. Based on the Seymour Midwest tool information retained in the tool library.','../../readiness/tools.html')
def pdfcrop(id,path,n,rect,title,credit,link,alt=None):
 d=fitz.open(path);p=d[n-1];box=fitz.Rect(rect) if rect else p.rect;out=OUT/(id+'.png');p.get_pixmap(matrix=fitz.Matrix(2,2),clip=box,alpha=False).save(out)
 add(id,out,title,alt or title,credit,link,{'source_sha256':sha(path),'pdf_page':n,'crop_pdf_points':list(box),'processing':'Faithful 144 dpi crop; source labels retained.'});d.close()
leeboy=A/'manuals/pdfs/leeboy-8680-safety-operations-1033428-sop.pdf'
for id,n,rect,title,printed in [('leeboy-starter-blocks',125,(59,499,307,741),'LeeBoy 8680 starter blocks and screed locks','4-57'),('leeboy-screed-lock',72,None,'LeeBoy 8680 screed locks and hopper lock valves','4-4'),('leeboy-loading',132,(299,550,553,709),'LeeBoy 8680 loading arrangement','4-64')]:
 pdfcrop(id,leeboy,n,rect,title,f'LeeBoy. (2026). 8680 Commercial Paver: Safety and operations manual (1033428-SOP, p. {printed}; PDF p. {n}). Serial 365152 and above. Faithful crop; use the complete matching procedure.','../../manuals/pdfs/'+leeboy.name+f'#page={n}')
p=R/'sources/rosco-rb50-manual.pdf';pdfcrop('rb50-components',p,43,(55,83,575,737),'Rosco RB50 machine overview and component key','Rosco / LeeBoy. (n.d.). RB50 Broom: Operations, service and parts manual (1017258-03, Rev. B, Fig. 3-1, p. 3-5; PDF p. 43). Serial 255027 and above.','sources/rosco-rb50-manual.pdf#page=43')
for id,slug,n,rect,title,credit in [
('cp-breaker','cp-breaker-manual-alt',12,(303,55,545,697),'CP breaker main parts and letter key','Atlas Copco Construction Tools / Chicago Pneumatic. (2010). CP 1210, CP 1230, CP 1240: Safety and operating instructions (9800 0608 90d, p. 12).'),
('torch-instructions','fairview-tiger-torch',1,None,'Tiger Torch 95-B and 445 instruction sheet','Tiger Torch Ltd. (n.d.). Operating instruction and safety procedures: Models 95-B and 445 [Bilingual instruction sheet, Fairview-hosted].'),
('troxler-gauge','troxler-3430-manual',19,(20,48,380,530),'Troxler 3430 gauge and accessories','Troxler Electronic Laboratories. (2021). RoadReader Model 3430: Manual of operation and instruction (Ed. 1.3, Fig. 1, p. 1-5; PDF p. 19). Identification only; Canadian use requires applicable CNSC authorization.')]:
 path=Path('/workspace/scratch/asphalt-readiness')/(slug+'.raw')
 # Builder can reconstruct the original from the retained source parts when scratch is absent.
 if not path.exists():
  parts=sorted((A/'readiness/sources'/slug).glob('*.pdf'));merged=fitz.open()
  for part in parts:
   d=fitz.open(part);merged.insert_pdf(d);d.close()
  path=OUT/(slug+'-temporary.pdf');merged.save(path);merged.close()
 pdfcrop(id,path,n,rect,title,credit,'../../readiness/index.html');
 if path.parent==OUT:path.unlink()
# MS-4 original scan crops; coordinates are fractions of the retained page image.
ms=[('ms4-gradation',168,(.21,.59,.81,.86),'Gradation types','3.9',134,None),('ms4-marshall',233,(.18,.08,.81,.76),'Marshall compaction hammer','4.18',199,None),('ms4-baghouse',358,(.19,.47,.82,.84),'Internal components of a baghouse','7.13',324,'Terex Roadbuilding'),('ms4-segregation',436,(.20,.43,.82,.88),'Segregation along the outside edge of a mat','8.26',402,'James A. Scherocman, P.E., Consulting Engineer'),('ms4-vibratory-roller',464,(.18,.08,.83,.44),'Vibratory roller','9.7',430,None)]
for id,n,box,title,fig,printed,contributor in ms:
 p=A/'ms-4/assets/pages'/f'p{n:04}.webp';im=Image.open(p);rect=[round(box[0]*im.width),round(box[1]*im.height),round(box[2]*im.width),round(box[3]*im.height)];out=OUT/(id+'.png');im.crop(rect).save(out)
 credit=f'Asphalt Institute. (2007). The asphalt handbook (7th ed., MS-4, Fig. {fig}, p. {printed}; PDF p. {n}). Faithful scan crop; original figure caption retained.'+(f' Original image contributor: {contributor}; credit register, PDF pp. 803–805.' if contributor else '')
 add(id,out,title,title+'; original labels and caption retained in the source crop.',credit,f'../../ms-4/assets/pages/p{n:04}.webp',{'source_sha256':'cb4708d2854d06d492af6dfdf0d39600af0ec45feef4c179c48fcff107da046b','source_page_image_sha256':sha(p),'pdf_page':n,'printed_page':printed,'figure':fig,'crop_pixels':rect,'source_image_pixels':[im.width,im.height],'contributor':contributor})
spec=A/'sources/design_build_standard_specs_2006.pdf'
for id,n,rect,title in [('spec-binder',308,(34,462,487,724),'2006 Table 502-F: binder-content adjustment'),('spec-application',310,(34,70,535,405),'2006 Table 502-H: application-rate adjustment'),('spec-density',307,(62,75,540,510),'2006 Tables 502-E-1 and E-2: different density bases'),('spec-smoothness',312,(10,70,292,735),'2006 Tables 502-J and J-2: smoothness')]:
 pdfcrop(id,spec,n,rect,title,f'British Columbia Ministry of Transportation. (2006). Design build standard specifications, Section 502 (section p. {n-296}; PDF p. {n}). Historical contract-reading example; complete clauses and actual project adoption govern.','../../sources/'+spec.name+f'#page={n}')
(R/'source-figures.json').write_text(json.dumps({'figures':list(figs.values())},indent=2,ensure_ascii=False)+'\n');print('Prepared',len(figs),'source/reused figures')
