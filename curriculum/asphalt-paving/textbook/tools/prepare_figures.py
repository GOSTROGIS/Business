"""Prepare credited figures without changing the underlying manual artwork."""
from pathlib import Path
from PIL import Image
import json,hashlib
from html import escape
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]; A=R.parent
rows=[]
def add(id,file,title,alt,credit,link=None,provenance=None):
 p=(R/file).resolve(); row={'id':id,'file':file,'title':title,'alt':alt,'credit':credit,'source_link':link,'provenance':provenance,'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None};rows.append(row)
notes={'history-timeline':'Based on the public historical accounts by Public Services and Procurement Canada (2025), UNESCO (2024) and FHWA listed in the references. Separate time scales; no universal sequence implied.','site-plan':'Informed by GOSTROGIS. (2026). Site planner, parcel site planner, map symbology and utility-network documentation (commit 9e409ba). All geometry is fictional and not georeferenced.','controls':'Based on WorkSafeBC. (2026 retrieved consolidation). Occupational Health and Safety Regulation, § 5.55. Conceptual teaching sequence; use the complete applicable clauses.','rigging-angle':'Based on WorkSafeBC. (2026 retrieved consolidation). Occupational Health and Safety Regulation, Part 15, especially §§ 15.2, 15.31 and 15.34. Identifies the angle from vertical; no working load limit or lift arrangement is prescribed.'}
for p in sorted((R/'assets').glob('*.svg')):
 root=ET.parse(p).getroot();ns={'s':'http://www.w3.org/2000/svg'};title=root.find('s:title',ns).text;alt=root.find('s:desc',ns).text
 add(p.stem,'assets/'+p.name,title,alt,'ACCESS IS4S. (2026). '+title+' [Original instructional SVG]. '+notes.get(p.stem,'Conceptual illustration; read the stated conditions in the lesson.'),provenance={'generator':'tools/draw.py','type':'original'})
# Two faithful crops from the supplied book scans, with original callouts and caption retained.
for id,pageno,box,title,printed,figure,contributor in [('ms4-structures',48,(250,615,1030,1430),'Compare the handbook’s pavement structures',14,'1.6',''),('ms4-screed',417,(235,999,1005,1424),'Read the forces around a free-floating screed',383,'8.16',' Original figure contributor: Volvo Construction Equipment (credit on PDF 804).')]:
 source=A/f'ms-4/assets/pages/p{pageno:04d}.webp'; out=R/f'assets/{id}.png';im=Image.open(source);im.crop(box).save(out,optimize=True)
 chapter='chapter-01-01' if pageno==48 else 'chapter-08-02'
 add(id,'assets/'+out.name,title,'Original MS-4 Figure '+figure+' with its original labels and caption.',f'From The asphalt handbook (7th ed., MS-4, Figure {figure}, p. {printed}; source PDF {pageno}), by Asphalt Institute, 2007. Copyright 2007 by Asphalt Institute. Faithful crop from the supplied scan; no labels altered.'+contributor,f'../ms-4/reader/{chapter}.html#page-{pageno:04d}',{'type':'source crop','source_file':str(source.relative_to(A)),'source_asset_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'crop_pixels':box,'source_pdf_page':pageno,'printed_page':printed})
# Reuse verified redraws and retain all original source/contributor details.
ms=json.loads((A/'ms-4/concepts/figure-manifest.json').read_text())
for f in ms['figures']:
 if f['id'] not in ['load-spread','screed-factors','pass-and-coverage']:continue
 refs='; '.join('Figure '+x['figure']+', p. '+str(x['printed_page'])+' / PDF '+str(x['pdf_page']) for x in f['references'] if 'figure' in x)
 contributors=' '.join('Original contributor: '+x['credit']+'.' for x in f['original_contributors'])
 add('ms4-'+f['id'],'../ms-4/concepts/'+f['file'],f['title'],f['alt'],'Adapted from '+f['source']+' '+refs+'. '+f['adaptation']+' '+contributors+' Copyright 2007 by Asphalt Institute. ACCESS redraw (2026).','../ms-4/concepts/index.html',f)
cat=json.loads((A/'caterpillar/atlas.json').read_text());docs={x['id']:x for x in json.loads((A/'caterpillar/catalogue.json').read_text())['documents']}
for f in cat['figures']:
 if f['id'] not in ['paver-sections','feeder-system','auger-assembly','roller-controls','steering-frame-lock']:continue
 d=docs[f['document']];terms=', '.join(c['name'] for c in f['components'])
 add('cat-'+f['id'],'../caterpillar/'+f['file'],f['title'],'Manufacturer illustration identifying '+terms+'.',f'From {d["title"]} ({d["publication"]}, source PDF p. {f["source_page"]}), by Caterpillar, {d["publication_year"]}. Copyright Caterpillar. {f["processing"]} Scope: {f["scope"]}','../caterpillar/parts-atlas.html#'+f['id'],f)
for id,file,title,alt,credit,link in [
 ('hand-tools','handwork-anatomy.svg','Name the parts of the handwork kit','Labelled original illustrations of a lute, rake, shovel and wheelbarrow.','ACCESS IS4S. (2026). The small tools that shape the work [Original instructional SVG]. Illustrative anatomy; confirm the actual model and parts list.','../readiness/field-guide.html'),
 ('rake-products','rakes-and-handwork.png','Match the drawing to real tools','Seymour catalogue photographs of an asphalt rake, cleaning tool and blacktop brushes.','From Partner Resource Guide (source PDF p. 156; printed p. 155), by Seymour Midwest, 2026 publisher download. Copyright Seymour Midwest. Upper illustration area cropped; original product relationships retained.','../readiness/index.html#seymour-tool-catalogue-2026'),
 ('crane-signals','crane-signals.png','Read the established crane signals','Complete WorkSafeBC hand-signals sheet with the original illustrations and labels.','From Hand signals for hoist and crane operations (TG07-29, p. 1), by WorkSafeBC, n.d. Copyright WorkSafeBC. Complete first page reproduced. Compare the regulation’s Figure 15-1 and the applicable lift plan.','../readiness/index.html#wsbc-crane-signals')]:
 add(id,'../readiness/assets/'+file,title,alt,credit,link,{'source_manifest':'../readiness/manifest.json','type':'existing verified figure'})
# Full manual warning page: unaltered safety illustration, actual model context in caption.
m=json.loads((A/'whmis/manifest.json').read_text())
for f in m['machine_warning_figures']:
 if 'p09' in str(f):
  add('roller-warning','../whmis/assets/cat-roller-safety-p09.png','Find the warning before the control','Actual Cat roller safety page with manufacturer hazard warning illustrations.','Caterpillar. (2022). CB2.5 GC, CB2.7 GC, CC2.7 GC utility compactors: Operation and maintenance manual (M0130633-02, source PDF p. 9). Complete source-page render. Confirm the publication and serial-number applicability before operating.','../whmis/index.html',f)
  break
add('plan-desk-screen','assets/plan-desk-screen.png','Inspect the record behind the map symbol','Screenshot of the actual Cedar plan desk showing revision B, fictional map layers and the entrance record.','ACCESS IS4S. (2026). Cedar Learning Access plan desk [Actual interface screenshot]. Fictional classroom geometry. Map-reading concepts adapted from GOSTROGIS CONSULTING documentation, commit 9e409ba, with owner authorization.','plan-desk.html',{'type':'browser screenshot','generator':'tools/export.py --desk-only','viewport':[1440,1100]})
(R/'figures.json').write_text(json.dumps({'figures':rows},indent=2,ensure_ascii=False)+'\n')
print(len(rows),'new or integrated figures prepared')
