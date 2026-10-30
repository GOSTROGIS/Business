"""Build editable chapters into a standalone study textbook and worked answers."""
from pathlib import Path
from html import escape
import json,re,argparse
import markdown
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tools"))
from activity_names import readable
from bs4 import BeautifulSoup, NavigableString
R=Path(__file__).resolve().parents[1]
LEARNER=['00-start.md','01-industry-evidence.md','02-history.md','03-technology.md','04-workers.md','05-road-documents.md','06-trends.md','07-safe-work.md','08-reference.md']
ANSWER=[f'answers-{i:02d}.md' for i in range(1,7)]+['answers-new.md','coverage.md']
figs=json.loads((R/'figures.json').read_text())['figures']; F={x['id']:x for x in figs}
order=[]
for name in LEARNER:
 for key in re.findall(r'@@fig:([^@]+)@@',(R/name).read_text()):
  if key not in order:order.append(key)
NUM={key:f'T{n:02d}' for n,key in enumerate(order,1)}
def figure(key):
 f=F[key];extra='manual' if 'cat-' in key or key in ['roller-warning','crane-signals','ms4-structures','ms4-screed'] else ''
 source=f'<a href="{escape(f["source_link"],quote=True)}">Source and context</a>.' if f.get('source_link') else ''
 return f'<figure class="learning-figure {extra}" id="figure-{key}"><p class="figure-number">FIGURE {NUM.get(key,key)}</p><p class="figure-title">{escape(f["title"])}</p><a href="{escape(f["file"],quote=True)}"><img src="{escape(f["file"],quote=True)}" alt="{escape(f["alt"],quote=True)}"></a><figcaption><strong>Note.</strong> {escape(f["credit"])} {source}</figcaption></figure>'
def whmis():
 symbols=[('flame','Flame','Flammability and related hazards'),('flame_circle','Flame over circle','Oxidizing hazard'),('exploding_bomb','Exploding bomb','Explosive / reactive hazards'),('gas_cylinder','Gas cylinder','Gases under pressure'),('corrosion','Corrosion','Corrosive effects'),('skull_crossbones','Skull and crossbones','Severe acute toxicity'),('health_hazard','Health hazard','Serious health effects'),('exclamation_mark','Exclamation mark','Harmful / irritant effects'),('biohazardous','Biohazardous infectious materials','Infectious biological hazard'),('environment','Environment','Aquatic hazard; not mandatory under WHMIS')]
 cells=''.join(f'<div><img src="../whmis/assets/pictograms/{id}.png" alt="Official {escape(title)} pictogram"><strong>{escape(title)}</strong><span>{escape(meaning)}</span></div>' for id,title,meaning in symbols)
 return '<figure class="learning-figure" id="figure-whmis"><p class="figure-number">WHMIS SYMBOL STUDY</p><p class="figure-title">Read the pictogram with the product information</p><div class="pictograms">'+cells+'</div><figcaption><strong>Note.</strong> Official pictograms from Canadian Centre for Occupational Health and Safety. (2026). <em>WHMIS—Pictograms</em> and official symbol kit. Artwork reproduced unchanged. Short meanings are teaching summaries; classification and conditions require the actual product label/SDS. The environmental pictogram is not mandatory under WHMIS. <a href="../whmis/index.html">Complete reference and provenance</a>.</figcaption></figure>'
def body(name):
 text=(R/name).read_text();title=text.splitlines()[0].lstrip('# ')
 text=re.sub(r'@@fig:([^@]+)@@',lambda m:figure(m[1]),text).replace('@@whmis@@',whmis())
 soup=BeautifulSoup(markdown.markdown(text,extensions=['tables','fenced_code','toc','sane_lists']),'html.parser')
 soup=BeautifulSoup(readable(str(soup)),"html.parser")
 for th in soup.select('th'):th['scope']='col'
 for tab in soup.select('table'):
  wrapper=soup.new_tag('div',attrs={'class':'table-wrap','tabindex':'0','role':'region','aria-label':'Study table'});tab.wrap(wrapper)
 return title,str(soup)
def page(title,body,deck='Study textbook · Volume 1',wide=False):
 cover = '<figure class="cover-art"><img src="assets/cover-art.svg" alt="Original conceptual roadbuilding scene with aggregate support, asphalt surface, haul truck, paver and roller."><figcaption>ACCESS IS4S. (2026). Roadbuilding connections [Original cover illustration]. Conceptual scene.</figcaption></figure>' if title=='Asphalt paving · Foundations and safe work' else ''
 coverclass = ' book-cover' if cover else ''
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | ACCESS IS4S</title><link rel="stylesheet" href="assets/book.css"></head><body><a class="skip" href="#content">Skip to content</a><header class="mast{coverclass}"><p class="brand">ACCESS · Indigenous Skills 4 Success</p><h1>{escape(title)}</h1><p class="deck">{escape(deck)}</p><p class="edition">Classroom development edition · 30 October 2026 · Technical review and pilot pending</p>{cover}<nav class="navline" aria-label="Book resources"><a href="index.html">Start</a><a href="study-textbook.html">Read the book</a><a href="study-textbook.pdf">Download PDF</a><a href="plan-desk.html">Plan desk</a><a href="answers.html">Worked answers</a><a href="series/index.html">Complete study series</a></nav></header><main class="page" id="content">{body}</main></body></html>'''
def prefix_ids(html,prefix):
 soup=BeautifulSoup(html,'html.parser'); ids={e['id']:prefix+'-'+e['id'] for e in soup.select('[id]')}
 for e in soup.select('[id]'):e['id']=ids[e['id']]
 for a in soup.select('a[href^="#"]'):
  if a['href'][1:] in ids:a['href']='#'+ids[a['href'][1:]]
 return str(soup)
def build():
 for group,stem,title,deck in [(LEARNER,'study-textbook','Asphalt paving · Foundations and safe work','Study textbook · Volume 1 · A1–A6 and B1'),(ANSWER,'answers','Worked answers and teaching guidance','Volume 1 · Individual evidence, checks and next practice')]:
  chunks=[];toc=[]
  for i,name in enumerate(group):
   title_,html=body(name);anchor='chapter-'+Path(name).stem
   toc.append(f'<li><a href="#{anchor}">{escape(title_)}</a></li>')
   chunks.append(f'<article class="chapter" id="{anchor}">{prefix_ids(html,anchor)}</article>')
   prev=group[i-1].replace('.md','.html') if i else 'index.html';nxt=group[i+1].replace('.md','.html') if i+1<len(group) else 'index.html'
   end=f'<nav class="endnav screen" aria-label="Chapter navigation"><a href="{prev}">← Previous</a><a href="{nxt}">Next →</a></nav>'
   (R/name.replace('.md','.html')).write_text(page(title_,f'<article class="chapter">{html}{end}</article>',deck))
  contents='<nav class="contents" aria-label="Contents"><h2>Contents</h2><ol>'+''.join(toc)+'</ol></nav>'
  (R/(stem+'.html')).write_text(page(title,contents+''.join(chunks),deck))
 title,html=body('README.md');(R/'index.html').write_text(page(title,'<article class="chapter">'+html+'</article>'))
 # A separate register keeps image/crop data reviewable without interrupting the lesson.
 contents=[]
 for key in order:
  f=F[key];contents.append(figure(key)+f'<p class="small">Asset SHA-256: <code>{f["sha256"]}</code></p>')
 (R/'figure-register.html').write_text(page('Figure credits and provenance','<article class="chapter"><p>The six inherited LA figures retain their original captions in the chapters. The official WHMIS symbol study retains its own group credit. Additional figures appear below; the machine-readable register records crop coordinates and source identities.</p><p><a href="figures.json">Figure data</a> · <a href="image-inventory.json">Complete book image inventory</a></p>'+''.join(contents)+'</article>'))
 soup=BeautifulSoup((R/'study-textbook.html').read_text(),'html.parser');inventory=[]
 import hashlib
 for im in soup.select('img'):
  f=im.find_parent('figure');p=(R/im['src']).resolve();inventory.append({'file':im['src'],'alt':im.get('alt',''),'caption':f.find('figcaption').get_text(' ',strip=True) if f and f.find('figcaption') else None,'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None})
 (R/'image-inventory.json').write_text(json.dumps({'placements':len(inventory),'unique_files':len({x['file'] for x in inventory}),'images':inventory},ensure_ascii=False,indent=2)+'\n')
 print('Built chapters, combined book, answers and figure register;',len(inventory),'image placements.')
if __name__=='__main__':build()
