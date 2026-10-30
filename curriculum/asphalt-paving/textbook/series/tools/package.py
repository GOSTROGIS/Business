"""Create small native manual parts and seven printable study/answer bundles."""
from pathlib import Path
import fitz,json,hashlib,zipfile,sys
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];S=R/'sources';P=S/'rosco-rb50-parts';P.mkdir(exist_ok=True)
sys.path.insert(0,str(R.parents[1]/'tools'))
from build_context import chunk_bytes
source=S/'rosco-rb50-manual.pdf';doc=PdfReader(source);parts=[]
def save(a,b):
 data,notes=chunk_bytes(doc,a+1,b,'Rosco RB50 operation, service and parts manual')
 if len(data)>10*1024**2 and b-a>1:
  m=(a+b)//2;save(a,m);save(m,b);return
 assert len(data)<=10*1024**2
 p=P/f'rosco-rb50-p{a+1:03}-p{b:03}.pdf';p.write_bytes(data);parts.append({'file':str(p.relative_to(R)),'first_pdf_page':a+1,'last_pdf_page':b,'pages':b-a,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
for a in range(0,len(doc.pages),25):save(a,min(a+25,len(doc.pages)))
expected={Path(x['file']).name for x in parts}
for old in P.glob('rosco-rb50-p*.pdf'):
 if old.name not in expected:old.unlink()
(S/'rosco-rb50-parts.json').write_text(json.dumps({'source':'sources/rosco-rb50-manual.pdf','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'parts':parts},indent=2)+'\n')
with zipfile.ZipFile(S/'rosco-rb50-small-parts.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.write(S/'rosco-rb50-parts.json','manifest.json')
 for x in parts:z.write(R/x['file'],Path(x['file']).name)
 z.writestr('READ-ME.txt','Rosco RB50 broom manual 1017258-03 Rev. B, serial 255027 and above. Parts preserve all 314 source pages in order. Page ranges refer to the original PDF. Read the full applicable procedure and warnings. Original publisher: Rosco / LeeBoy. Source URL and SHA-256 are in sources/manifest.json in the curriculum library.\n')
for n in range(2,9):
 with zipfile.ZipFile(R/f'volume-{n}-print-pack.zip','w',zipfile.ZIP_DEFLATED) as z:
  for stem in [f'volume-{n}',f'volume-{n}-answers']:z.write(R/(stem+'.pdf'),stem+'.pdf')
  z.writestr('READ-ME.txt','ACCESS IS4S asphalt study series. Includes the complete study and teaching/answer PDFs for this volume. Figure credits and full-source links are in each book. Classroom authoring does not certify unobserved equipment operation.\n')
print('Created',len(parts),'manual parts and seven print packs.')
