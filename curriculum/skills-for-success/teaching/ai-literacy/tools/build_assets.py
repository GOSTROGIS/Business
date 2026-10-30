"""Create the fictional AI practice pack and original accessible SVG teaching diagrams."""
from pathlib import Path
from html import escape as E
import json,hashlib,zipfile
from docx import Document
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
import fitz
R=Path(__file__).resolve().parents[1]; F=R/'fixtures'; A=R.parents[1]/'assets/diagrams'
F.mkdir(exist_ok=True)
ink='#242827';cream='#f7f2e8';red='#a93332';gold='#d5ad62';teal='#276b66';muted='#535c58'
class SVG:
 def __init__(self,title,desc,h=640):
  self.h=h;self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {h}" role="img" aria-labelledby="title desc"><title id="title">{E(title)}</title><desc id="desc">{E(desc)}</desc><defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#e5dfd2" stroke-width=".6"/></pattern><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="none" stroke="{teal}" stroke-width="1.4"/></marker></defs>'];self.rect(0,0,1000,h,cream);self.rect(0,0,1000,h,'url(#grid)');self.rect(0,0,1000,112,ink);self.text(36,39,'ACCESS IS4S  /  DIGITAL + AI',14,gold,700);self.text(36,80,title,30,'white',700)
 def rect(self,x,y,w,h,c,rx=0):self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>')
 def text(self,x,y,t,size=19,c=ink,weight=400):self.s.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{c}">{E(str(t))}</text>')
 def path(self,d,c=teal,width=3,arrow=False):self.s.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
 def lines(self,x,y,ls,size=17,c=muted,gap=27):
  for i,t in enumerate(ls):self.text(x,y+i*gap,t,size,c)
 def file(self,x,y,ext,label,detail,c):
  self.rect(x,y,274,170,'white',12);self.path(f'M{x+20} {y+20}h38l17 17v52h-55z',c,2);self.path(f'M{x+58} {y+20}v17h17',c,2);self.text(x+90,y+49,ext,27,c,700);self.text(x+20,y+120,label,19,ink,700);self.text(x+20,y+149,detail,15,muted)
 def save(self,id,caption):
  self.text(36,self.h-22,caption,15,muted);(A/(id+'.svg')).write_text(''.join(self.s)+'</svg>\n')
a=SVG('Choose a format that keeps the work useful','Six file cards distinguish editable prose, working calculations, page presentation, browser structure, transferable rows and structured data.',650)
for x,y,ext,label,detail,c in [(36,143,'.DOCX','Keep the wording editable','Headings · tables · revisions',red),(363,143,'.XLSX','Keep calculations working','Sheets · formulas · charts',teal),(690,143,'.PDF','Keep the page readable','Check every exported page',ink),(36,350,'.HTML','Make a browser document','Structure · links · access',teal),(363,350,'.CSV','Move a plain data table','Rows and columns, no layout',ink),(690,350,'.JSON','Exchange structured data','Named fields · valid syntax',red)]:a.file(x,y,ext,label,detail,c)
a.rect(36,548,928,52,ink,8);a.text(57,581,'RENAME changes a label.   EXPORT / CONVERT changes a format.',21,'white',700);a.save('ai-file-formats','Original ACCESS IS4S diagram · Open and verify the actual file, not just its name.')
a=SVG('A clear brief becomes checked work','A six-stage workflow connects brief, source, create, audit, verify and handover. A return arrow shows that findings lead to revision.',650)
steps=[('01','BRIEF','Purpose + audience','Output + constraints'),('02','SOURCE','Named files + versions','Facts + permissions'),('03','CREATE','Editable master','Actual saved output'),('04','AUDIT','Claim + location','Evidence + correction'),('05','VERIFY','Open + recalculate','Inspect + compare'),('06','HAND OVER','Version + change log','Limits + next action')]
for i,(n,t,l1,l2) in enumerate(steps):
 x=36+(i%3)*327;y=145+(i//3)*215;a.rect(x,y,274,170,'white',12);a.text(x+20,y+37,n,19,red,700);a.text(x+65,y+37,t,21,ink,700);a.lines(x+20,y+91,[l1,l2],18)
 if i%3<2:a.path(f'M{x+282} {y+80}h36',arrow=True)
a.path('M900 325V340H173V350',arrow=True);a.path('M825 540V570H500V540',red,2);a.text(445,602,'Revise when a check finds a problem.',19,red,700);a.save('ai-workflow','Original ACCESS IS4S diagram · A second AI opinion helps review; source evidence establishes a fact.')
a=SVG('An audit needs a location and evidence','A fictional incorrect notice is compared with the confirmed event brief. Findings identify count, room, cost and unsupported services.',660)
a.rect(36,145,420,220,'white',12);a.rect(514,145,450,220,'white',12);a.text(58,182,'SIMULATED DRAFT',18,red,700);a.lines(58,225,['30 participants · Birch Room','“Budget: $282”','“Transport and childcare included”'],19);a.text(536,182,'CONFIRMED CASE',18,teal,700);a.lines(536,225,['24 participants · Cedar Room','$156 + $78 + $38 = $272','No transport or childcare confirmed'],19);a.path('M466 252h36',arrow=True)
a.rect(36,395,928,174,ink,12);a.text(58,431,'FINDING  →  EVIDENCE  →  CORRECTION  →  RECHECK',22,gold,700);a.lines(58,473,['Location: notice opening.  Claim: 30 participants.','Evidence: confirmed brief says 24.  Correction: use 24.','Recheck the DOCX, PDF and HTML after revision.'],20,'white',31);a.save('ai-audit','Original ACCESS IS4S diagram · Correct facts stay; unsupported promises are removed.')
a=SVG('One change must reach every deliverable','Three budget states distinguish original, refreshments-only practice and full version two. Editable notice, workbook and PDF must agree.',640)
for i,(title,kits,food,total,left,c) in enumerate([('ORIGINAL',24,24,'272.00','28.00',ink),('PRACTICE COPY',24,26,'278.50','21.50',teal),('VERSION 2',26,26,'291.50','8.50',red)]):
 x=36+i*327;a.rect(x,145,274,285,'white',12);a.text(x+20,181,title,20,c,700);a.lines(x+20,222,[f'{kits} kits × $6.50',f'{food} portions × $3.25','Room supplies $38.00'],18);a.path(f'M{x+20} 297h234',gold,2);a.text(x+20,339,'$'+total,34,c,700);a.text(x+20,385,'Remaining $'+left,20,ink,700)
a.rect(36,467,928,105,ink,12);a.text(58,505,'DOCX notice     +     XLSX budget     +     PDF reading copy',23,'white',700);a.text(58,544,'Same version. Same confirmed facts. Different useful formats.',20,gold);a.save('ai-version-check','Original ACCESS IS4S diagram · All amounts CAD; fictional tax-inclusive exercise values.')
# Actual practice formats.
rows=[('Learning kits',24,6.5),('Refreshment portions',24,3.25),('Room supplies',1,38)]
facts='14 November 2026 · 10:00–12:30 · Cedar Room · 24 participants'
notice='Attendance is free. Refreshments are planned. Confirm access or dietary arrangements through the established program coordinator contact. Transportation and childcare are not confirmed. No personal data is included.'
d=Document();d.add_heading('Community Learning Day',0);d.add_paragraph('Fictional classroom case · Version 1');d.add_paragraph(facts);d.add_paragraph('Budget limit: $300 CAD. Prices are tax-inclusive exercise amounts; add no extra tax.')
t=d.add_table(rows=1,cols=3);t.style='Light Shading Accent 1'
for c,v in zip(t.rows[0].cells,['Item','Quantity','Unit cost (CAD)']):c.text=v
for name,q,c in rows:
 for cell,v in zip(t.add_row().cells,[name,str(q),f'${c:.2f}']):cell.text=v
d.add_paragraph(notice);d.save(F/'event-brief.docx')
w=Workbook();s=w.active;s.title='Budget';s.append(['Item','Quantity','Unit cost (CAD)','Line total (CAD)'])
for n,(name,q,c) in enumerate(rows,2):s.append([name,q,c,f'=B{n}*C{n}'])
s.append([]);s.append(['Total','','','=SUM(D2:D4)']);s.append(['Budget limit','','',300]);s.append(['Remaining','','','=D7-D6']);s.append([]);s.append(['Fictional classroom data — version 1; prices tax-inclusive'])
for cell in s[1]:cell.font=Font(color='FFFFFF',bold=True);cell.fill=PatternFill('solid',fgColor='242827')
for row in s.iter_rows(min_row=2,max_row=8,min_col=3,max_col=4):
 for cell in row:cell.number_format='"$"0.00'
for col,width in [('A',37),('B',15),('C',24),('D',24)]:s.column_dimensions[col].width=width
s.freeze_panes='A2';s.print_options.horizontalCentered=True;s.print_area='A1:D10';w.save(F/'event-budget.xlsx')
(F/'event-budget.csv').write_text('Item,Quantity,Unit cost CAD\nLearning kits,24,6.50\nRefreshment portions,24,3.25\nRoom supplies,1,38.00\n')
html='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Community Learning Day — fictional practice</title><style>body{max-width:50rem;margin:2rem auto;padding:1rem;font:1.1rem/1.6 sans-serif;background:#f7f2e8;color:#242827}h1{color:#a93332}table{border-collapse:collapse;width:100%}th,td{text-align:left;padding:.6rem;border-bottom:1px solid #999}caption{text-align:left;font-weight:bold}</style><main><h1>Community Learning Day</h1><p>Fictional classroom case · Version 1</p><p>'+facts+'</p><p>Budget limit: $300 CAD. Tax-inclusive exercise prices; add no extra tax.</p><table><caption>Planning quantities</caption><thead><tr><th scope="col">Item</th><th scope="col">Quantity</th><th scope="col">Unit cost CAD</th></tr></thead><tbody>'+''.join(f'<tr><th scope="row">{E(n)}</th><td>{q}</td><td>${c:.2f}</td></tr>' for n,q,c in rows)+'</tbody></table><p>'+notice+'</p></main></html>'
(F/'event-brief.html').write_text(html)
pdf=fitz.open();p=pdf.new_page(width=612,height=792);p.draw_rect((0,0,612,135),color=None,fill=(.14,.16,.15));p.insert_text((42,58),'COMMUNITY LEARNING DAY',fontsize=23,color=(1,1,1));p.insert_text((42,92),'Fictional classroom case | Version 1',fontsize=12,color=(.84,.68,.38));y=175
for text in ['14 November 2026 | 10:00-12:30','Cedar Room | 24 participants','Budget limit: $300 CAD','Tax-inclusive exercise prices; add no extra tax.','Learning kits: 24 at $6.50 each','Refreshment portions: 24 at $3.25 each','Room supplies: 1 at $38.00','Attendance is free. Refreshments are planned.','Confirm access or dietary arrangements through','the established program coordinator contact.','Transportation and childcare are not confirmed.','No personal data is included.']:
 p.insert_text((42,y),text,fontsize=12);y+=33
pdf.set_metadata({'title':'Community Learning Day — fictional practice brief','author':'ACCESS IS4S'});pdf.save(F/'event-brief.pdf',deflate=True);pdf.close()
(F/'simulated-draft.txt').write_text('SIMULATED AI DRAFT — intentionally contains errors for classroom auditing.\nJoin 30 people in Birch Room on 14 November, 10:00–12:30. The $282 budget includes transport and childcare.\n')
(F/'audit-template.csv').write_text('Finding ID,File and location,Requirement,Observation,Source evidence,Correction or question,Status,Recheck\n')
manifest={'purpose':'Fictional Community Learning Day; no actual event or personal records','files':[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(F.iterdir()) if p.suffix not in ['.zip','.json']]};(F/'file-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(F/'ai-practice-pack.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(F.iterdir()):
  if p.suffix=='.zip':continue
  info=zipfile.ZipInfo(p.name,date_time=(2026,10,30,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
print('Built four diagrams and nine practice files plus ZIP.')
