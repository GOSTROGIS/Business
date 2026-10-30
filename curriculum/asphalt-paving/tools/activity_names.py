"""Keep activity identifiers as metadata while showing useful task names."""
from pathlib import Path
import re
from bs4 import BeautifulSoup,NavigableString
R=Path(__file__).resolve().parents[1]
PATTERN=r'(?:LA|TB)\d-\d{2}'
def names():
 result={}
 for root in ['line-a','textbook']:
  for p in sorted((R/root).glob('0[1-7]-*.md')):
   for m in re.finditer(r'^### ('+PATTERN+r')\s*·\s*(.+)$',p.read_text(),re.M):result[m[1]]=m[2]
 return result
NAMES=names()
def readable(html):
 s=BeautifulSoup(html,'html.parser')
 for table in list(s.select('table')):
  rows=table.select('tr');heads=[c.get_text(' ',strip=True) for c in rows[0].select('th,td')] if rows else []
  if not heads or heads[0] not in ['Task','Activity']:continue
  if not any(re.fullmatch(PATTERN,row.select('td')[0].get_text(strip=True)) for row in rows[1:] if row.select('td')):continue
  group=s.new_tag('div',attrs={'class':'answer-tasks'})
  for row in rows[1:]:
   cells=row.select('td');
   if not cells:continue
   code=cells[0].get_text(strip=True);card=s.new_tag('section',attrs={'class':'answer-task','data-activity-id':code});h=s.new_tag('h3');h.string=NAMES.get(code,code);card.append(h)
   for i,cell in enumerate(cells[1:],1):
    label=s.new_tag('p');strong=s.new_tag('strong');strong.string=heads[i]+': ';label.append(strong)
    for child in list(cell.contents):label.append(child.extract())
    card.append(label)
   group.append(card)
  table.replace_with(group)
 for h in s.select('h1,h2,h3,h4'):
  m=re.match(r'^('+PATTERN+r')\s*·\s*(.+)',h.get_text(' ',strip=True))
  if m:h['data-activity-id']=m[1];h.clear();h.append(NAMES.get(m[1],m[2]))
 for node in list(s.find_all(string=True)):
  if node.parent.name in ['script','style'] or type(node).__name__=='Comment':continue
  text=re.sub(r'\b((?:LA|TB)\d)-(\d{2})[–—](\d{2})\b',lambda m:m[1]+'-'+m[2]+' through '+m[1]+'-'+m[3],str(node));new=re.sub(r'\b'+PATTERN+r'\b',lambda m:'“'+NAMES.get(m[0],'Practice task')+'”',text)
  if new!=text:node.replace_with(NavigableString(new))
 return str(s)
