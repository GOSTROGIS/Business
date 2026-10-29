"""Extract faithful source regions for the specification-reading lesson.
Run from repository root. Requires PyMuPDF; original PDF bytes are never edited.
"""
from pathlib import Path
import hashlib,json
import fitz
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT.parent/'sources/design_build_standard_specs_2006.pdf'
EXPECTED='0e57525e900390dc04451855039de6daa2b39bae79329d2878800228e69d1c13'
CROPS=[
 ('table-501-e',286,'Section 501, 3 of 13',[48,429,576,780],'Complete Table 501-E, including title, all columns and rows, and original footer.'),
 ('road-checker-introduction',299,'Section 502, 3 of 22',[326,449,583,635],'Clause 502.04.04 heading and both paragraphs; list continues on PDF page 300.'),
 ('road-checker-fields',300,'Section 502, 4 of 22',[45,69,285,223],'Complete continued list (a)–(e), including minimum calculation frequency and examples of appurtenances.')
]
def main():
 raw=SOURCE.read_bytes();sha=hashlib.sha256(raw).hexdigest()
 if sha!=EXPECTED:raise RuntimeError('Source changed: verify source edition and crop coordinates before rebuilding.')
 out=ROOT/'assets/crops';out.mkdir(parents=True,exist_ok=True);doc=fitz.open(SOURCE);assets=[]
 for name,page,printed,bbox,scope in CROPS:
  target=out/(name+'.png');pix=doc[page-1].get_pixmap(matrix=fitz.Matrix(3,3),clip=fitz.Rect(bbox),alpha=False);pix.save(target)
  assets.append(dict(id=name,file=target.relative_to(ROOT).as_posix(),source_file='../sources/design_build_standard_specs_2006.pdf',source_sha256=sha,pdf_page=page,printed_page=printed,crop_bbox_pdf_points=bbox,coordinate_origin='top-left',render_scale=3,width_px=pix.width,height_px=pix.height,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),scope=scope,processing='Unaltered PDF-region rasterization at 216 dpi; no redrawing, recolouring, added labels, OCR, or generative editing.',apa_reference='British Columbia Ministry of Transportation, Construction and Maintenance Branch. (2006). 2006 design build standard specifications for highway construction.',source_url=None,source_origin='User-supplied complete PDF; local source link is the verified retrieval location.'))
 (ROOT/'crop-manifest.json').write_text(json.dumps({'schema_version':1,'source_title':'2006 Design Build Standard Specifications for Highway Construction','source_original_bytes_preserved':True,'figure_count':2,'crop_count':len(assets),'assets':assets},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'figures':2,'crops':len(assets),'bytes':sum((ROOT/a['file']).stat().st_size for a in assets)},indent=2))
if __name__=='__main__':main()
