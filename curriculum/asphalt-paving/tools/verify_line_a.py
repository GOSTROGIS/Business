"""Offline structural, evidence-data, arithmetic and PDF checks for Line A books."""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / 'line-a'
errors: list[str] = []
checks = 0

def check(condition, label):
    global checks
    checks += 1
    if not condition:
        errors.append(label)

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in {'href', 'src'} and value:
                self.links.append(value)

from activity_names import NAMES

def main(require_generated=False):
    chapters = sorted(p for p in ROOT.glob('0[1-6]-*.md'))
    all_ids = []
    for p in chapters:
        ids = re.findall(r'^### (LA[1-6]-\d{2})\b', p.read_text(), re.M)
        unit = int(p.name[:2])
        expected = 7 if unit == 3 else 6
        check(len(ids) == expected, f'{p.name}: activity count')
        key = (ROOT / f'answers-{unit:02d}.md').read_text()
        for activity in ids:
            check(bool(re.search(r'\|\s*' + re.escape(activity) + r'\s*\|', key)), f'{activity}: missing keyed answer row')
        all_ids.extend(ids)
    check(len(all_ids) == len(set(all_ids)) == 37, '37 unique learner activities')
    criteria = set()
    for p in ROOT.glob('answers-*.md'):
        criteria.update(re.findall(r'\|\s*(A[1-6]\.\d+)\s*·', p.read_text()))
    wanted = {'A1.6','A1.8','A1.9'} | {f'A{u}.{n}' for u,total in [(2,5),(3,6),(4,9),(5,5),(6,5)] for n in range(1,total+1)}
    check(criteria == wanted, '33 occupational learning-task criteria mapped')
    rows = list(csv.DictReader((ROOT / 'competency-status.csv').open()))
    expected_codes = {f'{letter}{n}' for letter,total in zip('ABCDEFGHIJKL',[6,10,4,3,4,3,6,8,9,6,3,6]) for n in range(1,total+1)}
    check(len(rows) == 68 and {r['code'] for r in rows} == expected_codes, '68 unique occupational competency codes')
    check(all(r['technical_review'] == 'Pending' and r['practical_assessment'] == 'Not claimed' for r in rows), 'uncompleted technical/practical reviews not prefilled')
    evidence = json.loads((ROOT / 'research/public-evidence.json').read_text())['records']
    check(len(evidence) == 20 and len({r['evidence_id'] for r in evidence}) == 20, '20 curated public evidence records')
    for r in evidence:
        check(bool(re.fullmatch('[0-9a-f]{64}', r['retrieved_sha256'])), f"{r['evidence_id']}: source hash format")
        check(r['url'].startswith('https://'), f"{r['evidence_id']}: public URL")
    data = json.loads((ROOT / 'research/statcan-road-businesses.json').read_text())
    source_rows = data['rows']
    total = next(int(r['VALUE']) for r in source_rows if r['Employment size'] == 'Total, with employees')
    bands = [int(r['VALUE']) for r in source_rows if r['Employment size'] != 'Total, with employees']
    check(total == sum(bands) == 427, 'Statistics Canada category sum and total')
    check(all(r['GEO']=='British Columbia' and '[237310]' in r['North American Industry Classification System (NAICS)'] for r in source_rows), 'Statistics Canada source scope')
    check(all(r['REF_DATE']=='2025-07' for r in source_rows) and 'December 2025' in data['source_title'], 'published title and raw period both retained')
    D=Decimal
    arithmetic = [
        (D(92)-D(80), D(12)), (D(246750)*D('.08'),D(19740)),
        (D(175)-D(63),D(112)), ((D(175)/D(427)*100).quantize(D('.01'),rounding=ROUND_HALF_UP),D('40.98')),
        (D('215.19')+D('385.58'),D('600.77')),
        ((D('215.19')/D('600.77')*100).quantize(D('.01'),rounding=ROUND_HALF_UP),D('35.82')),
        (D(1948)-D(1942),D(6)), (D(80)+D(15)+D(5),D(100)),
        (D(8)-D('.5')+D(6),D('13.5')), (D(40)/1000,D('.040')),
        (D(50)*6,D(300)), (D(50)*6*D('.040'),D(12)),
        (D(12)*D('2.00'),D(24)), (D(8)+D(8)+D('7.60'),D('23.60')),
        (D(24)-D('23.60'),D('.40')), (D(60)*6*D('.040'),D('14.4')),
        (D('14.4')*2,D('28.8')), (D('28.8')-D('23.6'),D('5.2')),
        (D('.50')/50*100,D(1)),(D('.60')/60*100,D(1)),
        (D(1145000)-D(633000),D(512000)),(D(633000)-D(563000),D(70000)),
        (D(90+75+90+90+120+90)/60,D('9.25')),
    ]
    for i,(actual,expected) in enumerate(arithmetic,1):
        check(actual==expected,f'arithmetic check {i}')
    for filename,tokens in {'answers-01.md':['35.82%','40.98%','427','112'],'answers-04.md':['13.5'],'answers-05.md':['14.4','28.8','23.6','5.2'],'answers-06.md':['512,000']}.items():
        text=(ROOT/filename).read_text()
        for token in tokens:
            check(token in text,f'{filename}: checked result {token} present')
    for path in ROOT.glob('*.html'):
        parser=Links();parser.feed(path.read_text())
        for href in parser.links:
            parsed=urlsplit(href)
            if parsed.scheme or href.startswith(('#','//')):
                continue
            check((path.parent/unquote(parsed.path)).resolve().is_file(),f'{path.name}: missing local link {href}')
    pdf_pages={}
    for name in ['roadbuilding-foundations','teaching-guide']:
        pdf=ROOT/f'{name}.pdf'
        if not pdf.exists():
            check(not require_generated,f'{pdf.name}: missing generated PDF')
            continue
        from pypdf import PdfReader
        reader=PdfReader(pdf)
        check(len(reader.pages)>5,f'{pdf.name}: readable multi-page PDF')
        pdf_pages[name]=len(reader.pages)
        text='\n'.join(p.extract_text() or '' for p in reader.pages)
        for activity in all_ids:
            check(NAMES[activity] in " ".join(text.split()),f'{pdf.name}: missing activity {activity}')
        for p in reader.pages:
            for ref in p.get('/Annots',[]):
                action=ref.get_object().get('/A',{})
                uri=str(action.get('/URI',''))
                check(not any(x in uri for x in ['localhost','127.0.0.1','file://','/workspace/']),f'{pdf.name}: local-only URI')
    print(f'{checks} checks; {len(errors)} errors; PDFs: {pdf_pages}')
    for error in errors:
        print('ERROR:',error)
    raise SystemExit(bool(errors))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--require-generated',action='store_true')
    main(parser.parse_args().require_generated)
