"""Draw original, accessible SVG information graphics; no operating settings."""
from pathlib import Path
from html import escape
R=Path(__file__).resolve().parents[1]/'assets'
R.mkdir(exist_ok=True)
def start(w,h,title,desc):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><defs><linearGradient id="steel" x1="0" x2="1"><stop stop-color="#6c747a"/><stop offset=".42" stop-color="#e3e7e8"/><stop offset=".7" stop-color="#a0a9ae"/><stop offset="1" stop-color="#4d555b"/></linearGradient><linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ffce52"/><stop offset="1" stop-color="#d68b00"/></linearGradient><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#c8bfb5"/></pattern></defs><style>text{{font-family:Arial,sans-serif}}.title{{font-size:42px;font-weight:700;fill:#fff}}.eyebrow{{font-size:15px;font-weight:700;letter-spacing:2px;fill:#ffbc00}}.head{{font-size:26px;font-weight:700;fill:#1a1512}}.label{{font-size:22px;fill:#1a1512}}.small{{font-size:18px;fill:#625d58}}.leader{{fill:none;stroke:#a71920;stroke-width:1.8;stroke-linecap:round}}.part{{stroke:#44423d;stroke-width:2;stroke-linejoin:round}}</style><rect width="{w}" height="{h}" rx="18" fill="#f7f4f1"/><path d="M18 0H{w-18}Q{w} 0 {w} 18V150H0V18Q0 0 18 0" fill="#1a1512"/><rect y="148" width="{w}" height="5" fill="#ffbc00"/>'''
def text(x,y,s,cls='label',extra=''):return f'<text x="{x}" y="{y}" class="{cls}" {extra}>{escape(s)}</text>'
def line(points):return f'<polyline points="{points}" class="leader"/>'
def label(x,y,s,points):return line(points)+text(x,y,s)
def panel(x,y,w,h,num,title):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="white" stroke="#d8d0c9"/><rect x="{x+1}" y="{y+1}" width="{w-2}" height="48" rx="13" fill="#fff4d2"/>'+text(x+20,y+33,num+'  /  '+title,'head')
s=start(1440,1040,'The handwork kit: name the parts','Four original schematics identify the components of a lute, rake, shovel and wheelbarrow. They are illustrative, not model-specific assembly drawings.')
s+=text(38,43,'ACCESS IS4S · ASPHALT HANDWORK','eyebrow')+text(38,99,'The small tools that shape the work','title')
s+=panel(28,180,680,382,'01','LUTE')+panel(732,180,680,382,'02','RAKE')+panel(28,582,680,382,'03','SHOVEL')+panel(732,582,680,382,'04','WHEELBARROW')
# Lute: handle, two braces, head and fasteners. One side toothed; straight edge is identified as the reverse edge.
s+='<ellipse cx="341" cy="514" rx="158" ry="10" fill="#eee9e2"/><path d="M332 257h14v229h-14z" fill="url(#steel)" class="part"/><rect x="331" y="250" width="16" height="60" rx="6" fill="#1a1512"/><path d="M339 388L241 477M339 388L438 477" fill="none" stroke="#767d81" stroke-width="8"/><rect x="184" y="476" width="310" height="20" rx="3" fill="url(#steel)" class="part"/>'
for x in range(192,492,16):s+=f'<path d="M{x} 496v12h6v-12" fill="#7c858a"/>'
for x,y in [(339,388),(241,484),(438,484)]:s+=f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="#444" stroke-width="2"/>'
s+=label(460,287,'Grip','347,275 430,275 450,282')+label(72,345,'Handle','332,333 244,333 220,340')+label(460,406,'Brace','410,451 445,411')+label(72,454,'Head','191,485 159,459')+label(460,538,'Teeth','455,502 455,525')+text(60,541,'Reverse edge: straight','small')
# Rake.
s+='<ellipse cx="1082" cy="514" rx="150" ry="10" fill="#eee9e2"/><path d="M1073 254h16v220h-16z" fill="url(#gold)" class="part"/><rect x="1071" y="251" width="20" height="52" rx="7" fill="#1a1512"/><path d="M1077 448h9v35h-9z" fill="url(#steel)"/><rect x="946" y="477" width="272" height="12" rx="4" fill="url(#steel)" class="part"/>'
for x in range(951,1215,24):s+=f'<path d="M{x} 486v24q0 7 7 7h3v-7h-3v-24" fill="#626b70"/>'
s+=label(1190,302,'Handle','1089,320 1167,320 1182,298')+label(775,405,'Connection','1078,458 976,404 948,404')+label(1235,471,'Head','1217,481 1230,468')+label(1180,545,'Teeth','1168,514 1173,531')
# Shovel with D grip, wooden shaft, ferrule and a scoop blade.
s+='<ellipse cx="339" cy="926" rx="95" ry="9" fill="#eee9e2"/><path d="M307 657Q339 637 371 657v39q-32 30-64 0z" fill="none" stroke="#1a1512" stroke-width="11"/><path d="M332 708h14v145h-14z" fill="url(#gold)" class="part"/><path d="M329 826h20v44h-20z" fill="url(#steel)" class="part"/><path d="M302 853q37 16 74 0l32 58q-69 30-138 0z" fill="url(#steel)" class="part"/><path d="M339 858v56" stroke="#eef0ee" stroke-width="3"/>'
s+=label(465,685,'Grip','376,671 440,671 456,680')+label(68,769,'Shaft','332,760 230,760 220,766')+label(460,843,'Socket','350,840 437,840 450,839')+label(72,891,'Blade','273,894 206,885')
# Wheelbarrow side perspective; frame, tray, paired handles/legs, wheel and axle.
s+='<ellipse cx="1100" cy="918" rx="218" ry="12" fill="#eee9e2"/><path d="M908 753l48 81h217l65-95z" fill="url(#gold)" class="part"/><path d="M908 753l70-25 260 11-73 28z" fill="#ffe09b" class="part"/><path d="M967 836l-23 67h41l31-67M1005 835l-15 67h40l22-67" fill="none" stroke="#6b7378" stroke-width="9"/><path d="M858 795l289 68M875 770l292 66" fill="none" stroke="#41484c" stroke-width="9"/><path d="M1100 840l63 47 37-65" fill="none" stroke="#656d71" stroke-width="9"/><circle cx="1161" cy="884" r="38" fill="#1a1512"/><circle cx="1161" cy="884" r="22" fill="url(#steel)"/><circle cx="1161" cy="884" r="6" fill="#d2181f"/>'
s+=label(1215,705,'Tray','1195,749 1207,715')+label(770,730,'Handles','868,778 829,739')+label(768,864,'Frame','981,853 882,853')+label(982,944,'Legs','1010,903 1010,927')+label(1250,884,'Wheel','1199,884 1240,879')+label(1240,933,'Axle','1161,884 1212,923 1230,923')
s+=text(38,1008,'ILLUSTRATIVE PART NAMES · Verify the actual model, parts list and condition before use.','small')+'</svg>'
(R/'handwork-anatomy.svg').write_text(s)

s=start(1440,760,'Rigging: six questions before practical planning','Six reading checkpoints point to WorkSafeBC Part 15: qualified people, known load, identified gear, configuration, communication and inspection. No lifting capacities are prescribed.')
s+=text(38,43,'B1 · WORKSAFEBC PART 15','eyebrow')+text(38,99,'Build the evidence for the lift','title')
cards=[('01','Qualified people','Who is qualified to rig','and supervise this work?','§ 15.2'),('02','Known load','What is the load and','which lift points apply?','§§ 15.4–15.5'),('03','Identified gear','Can we verify the gear,','its WLL and compatibility?','§§ 15.5, 15.30–15.33'),('04','Configuration','Which sling arrangement','and angle are planned?','§ 15.34 · from vertical'),('05','Communication','Who signals, and which','regulated signals apply?','§ 15.20 · Figure 15-1'),('06','Inspection','Is the actual equipment','fit for the proposed use?','§§ 15.31, 15.39–15.54')]
for i,(num,head,l1,l2,clause) in enumerate(cards):
 x=28+(i%3)*474;y=185+(i//3)*255
 s+=f'<rect x="{x}" y="{y}" width="450" height="230" rx="14" fill="white" stroke="#d8d0c9"/><circle cx="{x+42}" cy="{y+42}" r="24" fill="#d2181f"/>'+text(x+42,y+49,num,'label','text-anchor="middle" style="fill:white;font-weight:700"')+text(x+80,y+49,head,'head')+text(x+28,y+104,l1)+text(x+28,y+134,l2)+f'<path d="M{x+28} {y+158}h390" stroke="#ddd4cc"/>'+text(x+28,y+193,clause,'small')
s+=text(38,725,'READING ROUTE · Use complete clauses, actual manufacturer instructions and a qualified plan.','small')+'</svg>'
(R/'rigging-reading-route.svg').write_text(s)

s=start(1440,800,'Choose the measurement before choosing the instrument','Four parallel routes connect distance, grade, temperature and density to actual instruments and evidence. Surface temperature and internal temperature are distinguished. Nuclear gauges require Canadian licensing arrangements.')
s+=text(38,43,'F2 · E4 · J5 · L5','eyebrow')+text(38,99,'What does this number need to tell us?','title')
routes=[('01','Distance','Tape · wheel','Length and unit','Instrument check','and measurement route'),('02','Grade','Level · staff · sensor','Height / slope / datum','Reference point','and survey procedure'),('03','Temperature','IR sensor · probe','Surface or internal?','Required method,','location and unit'),('04','Density','Specified test / gauge','Density and test basis','Authorized people,','method and records')]
for i,(num,head,tool,meaning,e1,e2) in enumerate(routes):
 x=28+i*354
 s+=f'<rect x="{x}" y="190" width="326" height="528" rx="15" fill="white" stroke="#d8d0c9"/><rect x="{x}" y="190" width="326" height="8" rx="4" fill="#d2181f"/>'+text(x+24,240,num,'small')+text(x+24,282,head,'head')+text(x+24,333,tool)+f'<path d="M{x+25} 368h275" stroke="#d8d0c9"/>'+text(x+24,412,'READ THE RESULT','small')+text(x+24,453,meaning)+f'<path d="M{x+164} 486v45m-7-8 7 8 7-8" fill="none" stroke="#d2181f" stroke-width="2"/>'+text(x+24,575,'KEEP THE EVIDENCE','small')+text(x+24,617,e1)+text(x+24,646,e2)
s+=text(38,765,'Before measuring: confirm the task, instrument, method, checks and acceptance requirement.','small')+'</svg>'
(R/'measurement-route.svg').write_text(s)
print('Wrote 3 accessible original SVGs')
