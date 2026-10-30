"""Build original ACCESS teaching redraws from verified MS-4 figures/passages."""
from pathlib import Path
from html import escape
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'concepts/assets';OUT.mkdir(parents=True,exist_ok=True)
INK='#1A1512';RED='#D2181F';GOLD='#FFBC00';PAPER='#F7F4F1';MUTED='#625D58'
def text(x,y,s,size=24,fill=INK,weight=400,anchor='start'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>'
def box(x,y,w,h,fill='white',stroke='#d7cec6',r=12):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'
def line(x1,y1,x2,y2,color=INK,width=3,arrow=False):return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>'
def lines(x,y,items,size=23,fill=INK,weight=400,gap=31):return ''.join(text(x,y+i*gap,s,size,fill,weight) for i,s in enumerate(items))
def frame(title,subtitle,body,foot,alt):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(alt)}</desc><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0 0 8 4 0 8" fill="none" stroke="{INK}" stroke-width="1.6"/></marker><pattern id="stone" width="56" height="40" patternUnits="userSpaceOnUse"><path d="m4 12 13-6 14 10-7 13-18-3zM38 28l9-6 8 7-5 9-12-2z" fill="none" stroke="#625D58" stroke-width="2"/></pattern><pattern id="asphalt" width="45" height="34" patternUnits="userSpaceOnUse"><circle cx="8" cy="9" r="3" fill="#fff" opacity=".5"/><path d="m23 13 8-5 7 9-10 6z" fill="#fff" opacity=".25"/></pattern></defs><rect width="1200" height="800" rx="24" fill="{PAPER}"/><g font-family="Arial,sans-serif"><path d="M40 35H1160" stroke="{RED}" stroke-width="6"/>{text(40,76,'ACCESS IS4S · ASPHALT FOUNDATIONS',16,MUTED,700)}{text(40,129,title,40,INK,700)}{text(40,168,subtitle,22,MUTED)}{body}<path d="M40 727H1160" stroke="#d7cec6"/>{text(40,763,foot,18,MUTED)}</g></svg>'''
figures=[]
def save(stem,title,subtitle,body,foot,alt,refs,changes,contributors=None):
 svg=frame(title,subtitle,body,foot,alt);p=OUT/(stem+'.svg');p.write_text(svg)
 figures.append({'id':stem,'file':'assets/'+p.name,'title':title,'alt':alt,'source':'Asphalt Institute. (2007). The asphalt handbook (7th ed., MS-4).',
  'source_sha256':'cb4708d2854d06d492af6dfdf0d39600af0ec45feef4c179c48fcff107da046b','references':refs,'adaptation':changes,
  'original_contributors':contributors or [],'asset_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})

# 1. Qualitative transfer of a wheel load; no design pressures are invented.
b=box(40,200,1120,500)
b+=f'<circle cx="440" cy="326" r="96" fill="{INK}"/><circle cx="440" cy="326" r="62" fill="#d4d0c9"/><circle cx="440" cy="326" r="23" fill="white" stroke="{INK}" stroke-width="4"/>'
for x in range(370,511,20):b+=line(x,244,x-12,263,'#625D58',5)
b+=line(440,205,440,291,RED,7,True)+text(560,267,'Wheel load',29,INK,700)+line(550,277,484,289,MUTED,2)
b+=box(115,427,650,122,INK,INK,0)+f'<rect x="115" y="427" width="650" height="122" fill="url(#asphalt)"/>'
b+=box(115,549,650,111,'#ded4c4','#ded4c4',0)+f'<rect x="115" y="549" width="650" height="111" fill="url(#stone)"/>'
b+=f'<path d="M403 427H477L660 549H220Z" fill="{GOLD}" opacity=".7"/>'
for x in [260,350,440,530,620]:b+=line(x,555,x,610,INK,3,True)
b+=lines(810,455,['Pavement','structure'],25,INK,700)+line(795,478,710,478,MUTED,2)
b+=lines(810,588,['Prepared','subgrade'],25,INK,700)+line(795,607,710,607,MUTED,2)
b+=text(130,686,'The pavement spreads the load before it reaches the subgrade.',23)
save('load-spread','Spread the load','Follow the load from the wheel to the supporting ground.',b,'Conceptual redraw · not to scale · no design thickness or pressure is specified.',
 'A wheel loads the pavement surface. The illustrated load spreads through the pavement structure to a wider region of prepared subgrade. Arrows show transfer, not measured pressure.',
 [{'figure':'1.5','printed_page':13,'pdf_page':47}], 'Simplified qualitative section; replaced pressure profile with a shaded load-transfer area and plain-language labels.')

# 2. One explicitly identified example of the structures in Figure 1.6.
b=box(40,200,1120,500)
layers=[(245,76,INK,'Asphalt surface','The upper asphalt layer.'),(337,92,'#b6ab9b','Granular base','Supports the asphalt surface.'),(445,84,'#d2c5ae','Subbase, where specified','An additional supporting layer.'),(545,112,'#e8decf','Prepared subgrade','The prepared ground beneath the structure.')]
for i,(y,h,c,label,desc) in enumerate(layers,1):
 b+=f'<path d="M90 {y+18} 500 {y+18} 570 {y} 160 {y}Z" fill="{c}" stroke="{INK}"/>'+box(90,y+18,410,h-18,c,INK,0)
 b+=f'<path d="M500 {y+18} 570 {y}V{y+h-18}L500 {y+h}Z" fill="{c}" stroke="{INK}"/>'
 b+=f'<rect x="91" y="{y+20}" width="408" height="{h-21}" fill="url(#{"asphalt" if i==1 else "stone"})"/>'
 b+=line(590,y+36,655,y+36,MUTED,2)+f'<circle cx="687" cy="{y+36}" r="21" fill="{GOLD}"/>'+text(687,y+44,str(i),22,INK,700,'middle')
 b+=text(724,y+35,label,25,INK,700)+text(724,y+66,desc,19,MUTED)
save('pavement-layers','Name the layers','One example: asphalt pavement on an unbound base, with a subbase.',b,'Conceptual section · other pavement structures exist · layer thicknesses are not a design.',
 'Four labelled layers: asphalt surface, granular base, optional subbase where specified, and prepared subgrade. The first three are above the prepared ground. This is one example, not every road structure.',
 [{'figure':'1.6','printed_page':14,'pdf_page':48}], 'Selected the unbound-base example, separated its layers and added functional descriptions. Other structures and design dimensions are not implied.')

# 3. Distinguish production processes, including the dryer in a batch plant.
b=box(40,200,1120,235)+box(40,455,1120,245)
b+=text(65,240,'BATCH',26,RED,700)+text(230,240,'Separate weighed batches',24)
top=[['Cold-feed','bins'],['Dry and','heat'],['Screen +','hot bins'],['Weigh a','batch'],['Mix with','binder'],['Store /','load out']]
for i,label in enumerate(top):
 x=65+i*181;b+=box(x,279,155,89,'#fff5d6','#d7cec6',8)+lines(x+15,315,label,21,gap=29)
 if i<5:b+=line(x+158,324,x+178,324,INK,2,True)
b+=text(65,406,'A batch plant can have a drying drum. The batch mixer defines the process.',21,MUTED)
b+=text(65,495,'DRUM / CONTINUOUS',26,RED,700)
bottom=[['Proportion at','cold-feed bins'],['Measure the','material flow'],['Dry + mix with','metered binder'],['Continuous mix','to storage']]
for i,label in enumerate(bottom):
 x=65+i*278;b+=box(x,535,245,90,'#fff5d6','#d7cec6',8)+lines(x+15,571,label,21,gap=29)
 if i<3:b+=line(x+249,580,x+274,580,INK,2,True)
b+=text(65,669,'Some facilities use a separate dryer and continuous mixer.',21,MUTED)
save('plant-processes','Batch or continuous?','Classify the mixing process, not the presence of one piece of equipment.',b,'Simplified material routes · additives, recycling and detailed controls require their own records.',
 'The batch route shows cold-feed bins, drying and heating, screening and hot bins, weighing a batch, mixing with binder and storage. The continuous route shows proportioning, flow measurement, continuous drying and mixing with metered binder, and storage.',
 [{'figure':'7.2','printed_page':310,'pdf_page':344},{'figure':'7.4','printed_page':312,'pdf_page':346},{'section':'7.1.1–7.1.2','printed_pages':[309,311,312],'pdf_pages':[343,345,346]}],
 'Converted equipment drawings into two simplified process lanes; omitted settings and detailed control systems.',
 [{'figure':'7.2','credit':'Terex Roadbuilding','credit_pdf_page':803},{'figure':'7.4','credit':'National Highway Institute (NHI)','credit_pdf_page':803}])

# 4. A function diagram, not a particular machine assembly drawing.
b=box(40,200,1120,500)+text(76,239,'FRONT · RECEIVING',17,MUTED,700)+text(858,239,'REAR · PLACING',17,MUTED,700)
b+=f'<path d="M85 310H315L278 435H127Z" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>'
for x,y in [(125,330),(165,346),(203,327),(245,353),(155,385),(226,392)]:b+=f'<path d="m{x} {y} 16-7 16 14-10 15-18-4z" fill="{INK}"/>'
b+=box(310,370,370,65,'#d1c9bf',INK,4)
for x in range(330,665,40):b+=line(x,378,x,426,INK,5)
b+=line(325,344,660,344,INK,4,True)
b+=box(716,285,55,236,RED,INK,8)
for y in range(300,510,25):b+=line(720,y,766,y+18,'white',3)
b+=line(695,332,695,278,INK,3,True)+line(695,459,695,516,INK,3,True)
b+=box(830,284,74,238,INK,INK,6)+box(905,296,200,214,'#625D58','#625D58',0)
b+=f'<rect x="905" y="296" width="200" height="214" fill="url(#asphalt)"/>'
b+=line(784,400,817,400,INK,3,True)
for x,heading,desc in [(82,'Hopper',['Receives the','asphalt mixture.']),(330,'Slat conveyor',['Moves mixture','toward the rear.']),(655,'Augers',['Distribute mixture','across the width.']),(935,'Screed',['Places the','shaped mat.'])]:
 b+=text(x,572,heading,25,INK,700)+lines(x,612,desc,21,MUTED,gap=29)
save('paver-material-route','Follow the mixture through the paver','Four trade words connect receiving, conveying, distributing and placing.',b,'Functional schematic · machine geometry and controls vary · not an operating sequence.',
 'Mixture enters the hopper, travels rearward on slat conveyors, is distributed laterally by augers and passes beneath the screed to form the mat. The diagram names functions without prescribing controls or settings.',
 [{'figure':'8.11','printed_page':377,'pdf_page':411},{'section':'8.4.1, component descriptions','printed_page':378,'pdf_page':412}],
 'Replaced the perspective equipment schematic with a labelled functional material route. Not drawn to scale or tied to an actual model.',
 [{'figure':'8.11','credit':'Volvo Construction Equipment','credit_pdf_page':804}])

# 5. The five named interacting factors around the free-floating screed.
b=box(40,200,1120,500)
b+=box(70,230,350,99,'#fff5d6')+text(92,267,'1 · Angle of attack',25,INK,700)+text(92,300,'Screed angle to the paving grade.',18,MUTED)
b+=box(780,230,350,99,'#fff5d6')+text(802,267,'2 · Head of material',25,INK,700)+text(802,300,'Mixture in front of the screed.',18,MUTED)
b+=box(70,570,350,98,'#fff5d6')+text(92,607,'4 · Screed weight',25,INK,700)+text(92,640,'The screed assembly’s weight.',18,MUTED)
b+=box(780,570,350,98,'#fff5d6')+text(802,607,'5 · HMA stability',25,INK,700)+text(802,640,'Temperature and gradation matter.',18,MUTED)
b+=box(430,226,340,91,INK,INK)+text(450,261,'3 · Forward motion',25,'white',700)+text(450,294,'Paving speed',21,GOLD)
b+=line(470,347,730,347,INK,4,True)+text(600,377,'Travel direction',18,MUTED,400,'middle')
b+=box(160,506,850,28,'#625D58','#625D58',0)+f'<path d="M670 505Q730 405 805 506Z" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>'
b+=f'<path d="M405 496 665 468 668 492 405 519Z" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
b+=f'<path d="M510 472V408H620V476M545 408 900 381" fill="none" stroke="{INK}" stroke-width="7"/>'
b+=line(570,379,570,438,INK,4,True)+text(250,476,'Mat',22,INK,700)
b+=line(294,329,405,496,MUTED,2)+line(923,329,760,456,MUTED,2)+line(297,570,552,432,MUTED,2)+line(885,570,789,506,MUTED,2)
save('screed-factors','A free-floating screed responds to a system','Recognize the five interacting factors before discussing a changed result.',b,'Conceptual redraw · arrows identify relationships, not adjustment instructions or setting values.',
 'A simplified free-floating screed with five named factors: angle of attack, head of material, forward motion or paving speed, screed weight, and HMA stability influenced by temperature and gradation. No control setting or adjustment is specified.',
 [{'figure':'8.16','printed_page':383,'pdf_page':417},{'section':'8.4.3, five factors','printed_page':384,'pdf_page':418}],
 'Mirrored and simplified the schematic; grouped the five factors in numbered callouts; omitted adjustment procedures and numeric settings.',
 [{'figure':'8.16','credit':'Volvo Construction Equipment','credit_pdf_page':804}])

# 6. Distinguish point-based passes from coverage of the width.
b=box(40,200,540,300)+box(610,200,550,300)
b+=text(70,245,'PASS',29,RED,700)+lines(70,283,['One crossing over one point','on the mat.'],24)
b+=box(80,350,450,95,'#e5ded5',INK,4)+line(105,397,505,397,INK,5,True)
b+=f'<circle cx="310" cy="397" r="12" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>'+text(310,477,'Point P · count a crossing here',19,INK,400,'middle')
b+=text(640,245,'COVERAGE',29,RED,700)+lines(640,283,['Enough rolling to cover','the complete width of the mat.'],24)
for i in range(3):
 b+=box(655,346+i*37,450,32,['#fff0c4','#ffdc75',GOLD][i],INK,2)+text(880,370+i*37,'✓',22,INK,700,'middle')
b+=text(880,477,'All three schematic bands are included',18,INK,400,'middle')
b+=box(40,525,1120,175,INK,INK)
b+=text(68,565,'TWO RECORDS CAN BOTH BE TRUE',19,GOLD,700)
b+=text(68,611,'Point P: two passes.',30,'white',700)+text(625,611,'Whole mat: one coverage.',30,'white',700)
b+=text(68,660,'Extra travel over one part does not prove a second complete coverage.',23,'white')
save('pass-and-coverage','A pass is not a coverage','Name the area you are counting before interpreting a roller record.',b,'Adapted concept · schematic bands are not a prescribed rolling pattern or roller width.',
 'A pass counts a roller crossing over one point. Coverage concerns the full mat width. A point may receive two passes while the full width has received only one complete coverage. Three coloured bands are conceptual, not an operating pattern.',
 [{'figure':'9.1','printed_page':416,'pdf_page':450}],
 'Replaced the original five-pass pattern with separate point and full-width concepts, plus a new record-reading example. No operating pattern is prescribed.')
(ROOT/'concepts/figure-manifest.json').write_text(json.dumps({'figures':figures,'reference':'Asphalt Institute. (2007). The asphalt handbook (7th ed., MS-4).','source_credit_pages':[803,804,805]},indent=2)+'\n')
print('Built',len(figures),'source-verified teaching SVGs')
