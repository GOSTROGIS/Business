"""Preserve official WHMIS publications and pictograms; convert official EPS to SVG."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,tempfile,zipfile,xml.etree.ElementTree as ET
import fitz
ROOT=Path(__file__).resolve().parents[1]
ROWS=[('pictograms','WHMIS — Pictograms',2026),('general','WHMIS — General',2026),('labels','WHMIS — Labels',2026),('sds','WHMIS — Safety Data Sheet (SDS)',2026),('training','WHMIS — Education and Training',2026)]
NAMES={'flame_circle':'Flame over circle','flame':'Flame','exploding_bomb':'Exploding bomb','gas_cylinder':'Gas cylinder','skull_crossbones':'Skull and crossbones','corrosion':'Corrosion','exclamation_mark':'Exclamation mark','health_hazard':'Health hazard','biohazardous':'Biohazardous infectious materials','environment':'Environment'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--downloads',type=Path,required=True);a=ap.parse_args();R=a.downloads
 docs=[];(ROOT/'sources').mkdir(parents=True,exist_ok=True)
 for key,title,year in ROWS:
  name=f'ccohs-{key}.pdf';source=R/name;target=ROOT/'sources'/name;shutil.copyfile(source,target)
  meta=R/(name+'.source.json')
  url=json.loads(meta.read_text())['source_url'] if meta.exists() else 'https://www.ccohs.ca/oshanswers/chemicals/whmis_ghs/CCOHS_'+('education_training' if key=='training' else key)+'.pdf'
  with fitz.open(source) as pdf:
   alltext='\n'.join(p.get_text() for p in pdf);last_date=__import__('re').findall(r'Fact sheet last revised:\s*(\d{4}-\d{2}-\d{2})',alltext)
   docs.append({'id':'WHMIS-'+key.upper(),'title':title,'publisher':'Canadian Centre for Occupational Health and Safety','year':year,'revision_date':last_date[-1] if last_date else None,'role':'Current CCOHS fact sheet reflecting the December 2022 Hazardous Products Regulations amendments.','file':target.relative_to(ROOT).as_posix(),'source_url':url,'bytes':target.stat().st_size,'sha256':sha(target),'pages':len(pdf)})
 for name,title,revision in [('worksafebc-whmis-at-work.pdf','WHMIS 2015: At Work','R04/19'),('worksafebc-whmis-basics.pdf','WHMIS 2015: The Basics','R03/19')]:
  source=R/name;target=ROOT/'sources'/name;shutil.copyfile(source,target);meta=json.loads((R/(name+'.source.json')).read_text())
  with fitz.open(source) as pdf:docs.append({'id':'BC-'+revision.replace('/','-'),'title':title,'publisher':'WorkSafeBC','year':2019,'revision':revision,'role':'Historical B.C. explanatory book. Predates the December 2022 amendments; use the current CCOHS sheets and current B.C. requirements for changes.','file':target.relative_to(ROOT).as_posix(),'source_url':meta['source_url'],'bytes':target.stat().st_size,'sha256':sha(target),'pages':len(pdf)})
 zip_src=R/'ccohs-pictogram-kit.zip';zip_dst=ROOT/'sources/ccohs-official-pictograms.zip';shutil.copyfile(zip_src,zip_dst)
 icons=[];folder=ROOT/'assets/pictograms';folder.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(zip_src) as z:
  assert z.testzip() is None
  for key,title in NAMES.items():
   for ext in ['png','eps']:(folder/f'{key}.{ext}').write_bytes(z.read(f'{key}.{ext}'))
   with tempfile.TemporaryDirectory(prefix='whmis-vectors-') as td:
    pdf=Path(td)/'symbol.pdf';svg=folder/f'{key}.svg'
    subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-dEPSCrop','-sDEVICE=pdfwrite','-sOutputFile='+str(pdf),str(folder/f'{key}.eps')],check=True,capture_output=True)
    subprocess.run(['pdftocairo','-svg',str(pdf),str(svg)],check=True,capture_output=True)
    text=svg.read_text();pos=text.index('>')+1
    # pdftocairo emits XML declaration before the SVG element.
    pos=text.index('>',text.index('<svg'))+1
    text=text[:pos]+f'<title>{title}</title><desc>Official CCOHS downloadable pictogram, converted from EPS without redesigning the symbol. {"Environmental hazards pictogram; not mandatory under Canadian WHMIS." if key=="environment" else "Read the product label and safety data sheet for the actual hazard classification."}</desc>'+text[pos:]
    svg.write_text(text)
   icons.append({'id':key,'name':title,'source_url':'https://www.ccohs.ca/WHMISpictograms.html','source_member':f'{key}.eps','part_of_whmis_pictogram_set':key!='environment','files':{ext:{'path':(folder/f'{key}.{ext}').relative_to(ROOT).as_posix(),'sha256':sha(folder/f'{key}.{ext}')} for ext in ['png','eps','svg']},'processing':'PNG and EPS preserved byte for byte from official ZIP. SVG is a vector conversion through Ghostscript and pdftocairo; only accessible title/description added. No recolouring or redrawing.'})
 manifest={'accessed':'2026-10-30','documents':docs,'pictogram_kit':{'source_url':'https://www.ccohs.ca/images/whmis2015/for_download/all_whmis2015_pictograms.zip','file':zip_dst.relative_to(ROOT).as_posix(),'sha256':sha(zip_dst),'bytes':zip_dst.stat().st_size,'members_retained':'Original ZIP unchanged; ten EPS and ten PNG files extracted without the ZIP metadata folders.'},'pictograms':icons}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(len(docs),'source PDFs',sum(d['pages'] for d in docs),'pages;',len(icons),'official symbols in PNG, EPS and SVG')
if __name__=='__main__':main()
