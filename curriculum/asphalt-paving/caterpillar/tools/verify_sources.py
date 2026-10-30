"""Check native page fidelity against the pinned downloaded originals."""
from pathlib import Path
import argparse,hashlib,json,re,fitz,unicodedata
from PIL import Image,ImageChops
p=argparse.ArgumentParser();p.add_argument('--downloads',type=Path,required=True);a=p.parse_args();R=Path(__file__).resolve().parents[1];m=json.loads((R/'manifest.json').read_text());renders=0;count=0;rounding=[]
def normalized_text(s):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s).replace('\u00ad','-')).strip()
for d in m['documents']:
 raw=(a.downloads/d['download_filename']).read_bytes();assert hashlib.sha256(raw).hexdigest()==d['original_sha256'];original=fitz.open(stream=raw,filetype='pdf');assert len(original)==d['original_pages'];n=1
 for part in d['parts']:
  assert part['start']==n;pdf=R/part['file'];data=pdf.read_bytes();text=(R/part['text']).read_bytes();assert len(data)==part['bytes']<=10*1048576;assert hashlib.sha256(data).hexdigest()==part['sha256'];assert hashlib.sha256(text).hexdigest()==part['text_sha256'];assert list(map(int,re.findall(r'^=== SOURCE PDF PAGE (\d+) ===$',text.decode(),re.M)))==list(range(part['start'],part['end']+1))
  with fitz.open(pdf) as split:
   assert len(split)==part['pages']<=25
   for j,page in enumerate(split):
    x=original[part['start']-1+j].get_pixmap(matrix=fitz.Matrix(.5,.5),annots=False);y=page.get_pixmap(matrix=fitz.Matrix(.5,.5),annots=False);assert (x.width,x.height)==(y.width,y.height);
    assert original[part['start']-1+j].read_contents()==page.read_contents(),('content stream',d['id'],part['start']+j)
    if x.samples!=y.samples:
     # Low-resolution transparency/gradient sampling can depend on copied object IDs.
     # Recheck non-identical pages at 100 dpi, with exact native content/text checks.
     xx=original[part['start']-1+j].get_pixmap(dpi=100,annots=False);yy=page.get_pixmap(dpi=100,annots=False)
     diff=ImageChops.difference(Image.frombytes('RGB',(xx.width,xx.height),xx.samples),Image.frombytes('RGB',(yy.width,yy.height),yy.samples))
     delta=max(v[1] for v in diff.getextrema());assert delta<=3,(d['id'],part['start']+j,delta)
     rounding.append([d['id'],part['start']+j,delta])
    assert normalized_text(original[part['start']-1+j].get_text())==normalized_text(page.get_text()),('text',d['id'],part['start']+j);renders+=1
    for link in page.get_links():
     if link['kind']==fitz.LINK_GOTO:assert 0<=link['page']<len(split)
  n=part['end']+1;count+=1
 assert n==d['original_pages']+1;original.close();print(d['id'],'all pages match',flush=True)
assert renders==1883 and count==88
print(json.dumps({'documents':len(m['documents']),'parts':count,'all_source_page_render_matches':renders,'comparison_dpi':36,'nonidentical_pages_rechecked_dpi':100,'maximum_allowed_channel_delta':3,'rounding_pages':rounding,'status':'passed'}))
