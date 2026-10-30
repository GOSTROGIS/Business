"""Expose task names and visual learning cards; keep authoring IDs in HTML metadata only."""
from pathlib import Path
from functools import lru_cache
from html import escape
import re
from bs4 import BeautifulSoup, NavigableString
ROOT=Path(__file__).resolve().parents[1]
SKILLS={'RD':'Reading','WR':'Writing','NU':'Numeracy','DG':'Digital','PS':'Problem solving','CM':'Communication','CL':'Collaboration','AD':'Adaptability','CI':'Creativity and innovation','CP':'Integrated project','AI':'AI literacy'}
CODE=r'(?:(?:CK-)?(?:RD|WR|NU|DG|PS|CM|CL|AD|CI|CP|AI)-[ABCR]?\d{2}|CK-(?:RD|WR|NU|DG|PS|CM|CL|AD|CI))'
TOKEN=re.compile(r'\b'+CODE+r'\b')
@lru_cache(maxsize=1)
def task_names():
 names={}
 files=sorted((ROOT/'learner').glob('*.md'))+sorted((ROOT/'teaching').rglob('*.md'))+sorted((ROOT/'answers').glob('*.md'))
 for p in files:
  for m in re.finditer(r'^#{1,6}\s+('+CODE+r')\s*[•·—:]\s*(.+)$',p.read_text(),re.M):
   name=m[2].strip('* ')
   if m[1].startswith('CK-'):
    parts=m[1].split('-');name=SKILLS[parts[1]]+' practice '+(parts[-1][0] if parts[-1][0].isalpha() else '')+' · '+name
   names.setdefault(m[1],name)
 for code,name in SKILLS.items():
  names.setdefault('CK-'+code,name+' individual practice check')
 return names

def expand_abbreviations(text):
 # A slash list omits repeated prefixes in legacy authoring references.
 def slash(m):
  prefix=m[1];return '/'.join(prefix+'-'+n for n in m[2].split('/'))
 return re.sub(r'\b((?:CK-)?(?:RD|WR|NU|DG|PS|CM|CL|AD|CI|CP|AI))-([ABCR]?\d{2}(?:/[ABCR]?\d{2})+)\b',slash,text)

def readable(text):
 text=expand_abbreviations(text);names=task_names()
 text=re.sub(r'\b((?:RD|WR|NU|DG|PS|CM|CL|AD|CI|CP|AI))-(\d{2})[–—](\d{2})\b',lambda m:m[1]+'-'+m[2]+'–'+m[1]+'-'+m[3],text)
 def replace(m):
  token=m[0]
  # Bare skill abbreviations in identifiers are not rendered as unexplained labels.
  if token in names:return '“'+names[token]+'”'
  if token.startswith('CK-'):return SKILLS.get(token.split('-')[1],token)+' practice check'
  if '-' not in token:return SKILLS.get(token,token)
  return SKILLS.get(token.split('-')[0],token)+' practice task'
 text=TOKEN.sub(replace,text)
 text=re.sub(r'”\s*[–—]\s*“','” through “',text)
 text=text.replace('”/“','”; “')
 return text

def transform(body, convert_cards=True):
 soup=BeautifulSoup(body,'html.parser')
 for h in soup.select('h1,h2,h3,h4,h5,h6'):
  m=re.match(r'^('+CODE+r')\s*[•·—:]\s*(.+)$',h.get_text(' ',strip=True))
  if m:
   h['data-activity-id']=m[1];h['class']=list(set(h.get('class',[])+['activity']))
   h.clear();h.append(task_names().get(m[1],m[2]))
 for node in list(soup.find_all(string=True)):
  if node.parent.name in ['script','style'] or type(node).__name__=='Comment':continue
  s=str(node);new=readable(s)
  if new!=s:node.replace_with(NavigableString(new))
 for tag in soup.select('[alt], [aria-label]'):
  for attr in ['alt','aria-label']:
   if tag.has_attr(attr):tag[attr]=readable(tag[attr])
 if not convert_cards:return str(soup)
 # Component/evidence tables become large labelled learning cards.
 for table in list(soup.select('table')):
  rows=table.find_all('tr');heads=[x.get_text(' ',strip=True) for x in rows[0].find_all(['th','td'])] if rows else []
  if not heads or not re.search(r'component',heads[0],re.I):continue
  cards=soup.new_tag('div',attrs={'class':'skill-cards','role':'list','aria-label':'What to practise and how to show it'})
  for n,row in enumerate(rows[1:],1):
   cells=row.find_all(['td','th']);
   if len(cells)<2:continue
   card=soup.new_tag('section',attrs={'class':'skill-card','role':'listitem'});number=soup.new_tag('span',attrs={'class':'card-number','aria-hidden':'true'});number.string=f'{n:02d}';card.append(number)
   h=soup.new_tag('h4');h.string=re.sub(r'^\d+\.\s*','',cells[0].get_text(' ',strip=True));card.append(h)
   p=soup.new_tag('p');p.string=cells[1].get_text(' ',strip=True);card.append(p)
   if len(cells)>2:
    practice=soup.new_tag('p',attrs={'class':'card-practice'});strong=soup.new_tag('strong');strong.string='Practise with: ';practice.append(strong);practice.append(cells[2].get_text(' ',strip=True));card.append(practice)
   cards.append(card)
  table.replace_with(cards)
 return str(soup)
