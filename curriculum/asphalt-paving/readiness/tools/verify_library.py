"""Check all source pages, pinned bytes, web article integrity and local links."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse, csv, hashlib, json, re, unicodedata
import fitz
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(s):return re.sub(r'\s+','',unicodedata.normalize('NFKC',s).replace('\xad','-'))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--downloads',type=Path,required=True);args=p.parse_args()
    m=json.loads((ROOT/'manifest.json').read_text());pages=0;highres=0;expected=set();parts_count=0;text_variations=[]
    for d in m['documents']:
        raw=(args.downloads/d['download_filename']).read_bytes();assert sha(raw)==d['original_sha256']
        original=fitz.open(stream=raw,filetype='pdf');assert len(original)==d['original_pages'];nextpage=1
        for q in d['parts']:
            assert q['start']==nextpage and q['pages']==q['end']-q['start']+1
            path=ROOT/q['file'];data=path.read_bytes();assert sha(data)==q['sha256'] and len(data)==q['bytes']
            assert q['pages']<=25 and len(data)<=10*1048576
            t=(ROOT/q['text']).read_bytes();assert sha(t)==q['text_sha256']
            assert list(map(int,re.findall(r'^=== SOURCE PDF PAGE (\d+) ===$',t.decode(),re.M)))==list(range(q['start'],q['end']+1))
            part=fitz.open(stream=data,filetype='pdf');assert len(part)==q['pages']
            for i,page in enumerate(part):
                n=q['start']+i;source=original[n-1]
                assert page.rect==source.rect,(d['id'],n,'page geometry')
                same_text=norm(page.get_text(sort=True))==norm(source.get_text(sort=True))
                a=page.get_pixmap(dpi=36,annots=False);b=source.get_pixmap(dpi=36,annots=False)
                if a.samples!=b.samples or not same_text:
                    a=page.get_pixmap(dpi=100,annots=False);b=source.get_pixmap(dpi=100,annots=False);highres+=1
                    assert a.width==b.width and a.height==b.height and a.samples==b.samples,(d['id'],n,'render')
                if not same_text:
                    # Splitting tagged PDFs can change extraction of alternate
                    # text while preserving the visible page. Keep the original
                    # source extraction and explicitly report every such page.
                    text_variations.append(dict(source_id=d['id'],source_pdf_page=n,render_identical_at_100dpi=True,original_source_text_retained=q['text']))
                for link in page.get_links():
                    if link['kind']==fitz.LINK_GOTO: assert 0<=link['page']<len(part),(d['id'],n,'destination')
                pages+=1
            expected.add(path.resolve());nextpage=q['end']+1;parts_count+=1
        assert nextpage==len(original)+1
        print('Verified',d['id'],len(original),'pages',flush=True)
    assert expected=={p.resolve() for p in (ROOT/'sources').rglob('*.pdf')}
    # Preserve the completed expensive PDF phase even if a later link/article
    # check fails. Its report is independently reviewable.
    pdf_report=dict(status='passed',source_pages=pages,pdf_parts=parts_count,render_dpi=36,render_rechecks_at_100dpi=highres,text_layer_variations=text_variations)
    (ROOT/'pdf-page-checks.json').write_text(json.dumps(pdf_report,indent=2)+'\n')
    images=0;html_whitespace_variations=[]
    for d in m['web_documents']:
        raw=(ROOT/d['raw']).read_bytes();assert sha(raw)==d['original_sha256']
        original=BeautifulSoup(raw,'html.parser').select_one(d['selector']);assert original
        for x in original.select('script, style, iframe, form, button, noscript, input'):x.decompose()
        t=(ROOT/d['text']).read_bytes();assert sha(t)==d['text_sha256']
        assert original.get_text('\n',strip=True)+'\n'==t.decode(),d['id']
        local=BeautifulSoup((ROOT/d['file']).read_text(),'html.parser');article=local.select_one('.source-article')
        original_text=original.get_text('\n',strip=True);rendered_text=article.get_text('\n',strip=True)
        # Serializing malformed publisher HTML can merge adjacent text nodes.
        # The pinned text file remains byte-exact to the original extraction;
        # the readable DOM must preserve all non-whitespace characters in order.
        assert re.sub(r'\s+','',rendered_text)==re.sub(r'\s+','',original_text),d['id']
        if original_text!=rendered_text:html_whitespace_variations.append(d['id'])
        assert not article.select('script, iframe, form')
        for im in d['images']:
            b=(ROOT/im['file']).read_bytes();assert sha(b)==im['sha256'] and len(b)==im['bytes'];images+=1
        assert len(article.select('img[src]'))==len(d['images'])
        for tag in article.select('img[src]'):assert not urlsplit(tag['src']).scheme
    local_links=0
    for file in ROOT.rglob('*.html'):
        soup=BeautifulSoup(file.read_text(),'html.parser')
        for tag in soup.select('[href],img[src],script[src]'):
            value=tag.get('href') or tag.get('src');u=urlsplit(value)
            if u.scheme or u.netloc or not u.path:continue
            target=(file.parent/unquote(u.path)).resolve();assert target.exists(),(file,value)
            local_links+=1
    assert len(list(csv.DictReader((ROOT/'coverage.csv').open())))==68
    assert len(list(csv.DictReader((ROOT/'tools.csv').open())))==32
    report=dict(status='passed',pdf_publications=len(m['documents']),all_source_pages_compared=pages,pdf_parts=parts_count,render_dpi=36,render_rechecks_at_100dpi=highres,text_layer_variations=text_variations,web_articles=len(m['web_documents']),html_whitespace_variations=html_whitespace_variations,web_figures=images,local_links=local_links,checks='Pinned original/part/text hashes; complete contiguous page ranges; native page geometry and every-page rendering; normalized text with explicitly recorded alternate-text variations checked visually at 100 dpi; original source extracts retained; valid internal PDF destinations; full selected web article text and all archived images; HTML local targets; competency/tool row counts.')
    (ROOT/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
