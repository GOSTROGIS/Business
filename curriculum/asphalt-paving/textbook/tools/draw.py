"""Draw original ACCESS teaching diagrams. Dimensions and scenes are illustrative."""
from pathlib import Path
from html import escape
R=Path(__file__).resolve().parents[1]/'assets';R.mkdir(exist_ok=True)
INK='#1a1512';GOLD='#ffbc00';RED='#b71923';CREAM='#f7f4f1';TEAL='#286864'
def t(x,y,s,size=23,fill=INK,weight=400,anchor='start'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>'
def rect(x,y,w,h,fill='white',r=12,stroke='none'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'
def path(d,fill='none',stroke=INK,width=3,extra=''):
 return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'
def line(x,y,x2,y2,stroke=INK,width=3,arrow=False):
 return path(f'M{x} {y}L{x2} {y2}',stroke=stroke,width=width,extra='marker-end="url(#arrow)"' if arrow else '')
def circle(x,y,r,fill):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'
def lines(x,y,ss,size=22,fill=INK,gap=30):return ''.join(t(x,y+i*gap,s,size,fill) for i,s in enumerate(ss))
def start(title,sub,h=760):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="{h}" viewBox="0 0 1400 {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(sub)}</desc><defs><linearGradient id="steel" x2="0.9" y2="1"><stop stop-color="#e1e6e4"/><stop offset=".45" stop-color="#89969b"/><stop offset="1" stop-color="#c1ccce"/></linearGradient><linearGradient id="gold" x2="1" y2="1"><stop stop-color="#ffdc6c"/><stop offset="1" stop-color="#d49312"/></linearGradient><pattern id="stone" width="30" height="24" patternUnits="userSpaceOnUse"><rect width="30" height="24" fill="#d6c9b5"/><path d="M2 6l10-3 5 8-9 6zM20 17l6-5 3 8z" fill="#a7957a"/></pattern><pattern id="asphalt" width="18" height="16" patternUnits="userSpaceOnUse"><rect width="18" height="16" fill="#3f4445"/><path d="M2 3l4 2M12 11l3-2" stroke="#747a79" stroke-width="2"/></pattern><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#b71923"/></marker></defs><style>text{{font-family:Arial,sans-serif}} .dash{{stroke-dasharray:10 8}}</style>'''+rect(0,0,1400,h,CREAM,0)+rect(0,0,1400,147,INK,0)+t(38,43,'ACCESS IS4S  /  ASPHALT STUDY TEXTBOOK',16,GOLD,700)+t(38,103,title,40,'white',700)+rect(0,147,1400,5,GOLD,0)
def save(name,s,h=760,foot='Conceptual teaching illustration · Read the dimensions and conditions in the lesson.'):
 (R/(name+'.svg')).write_text(s+t(38,h-26,foot,17,'#625d58')+'</svg>')
def wheel(x,y,r=25):return circle(x,y,r,INK)+circle(x,y,r*.53,'url(#steel)')+circle(x,y,5,RED)
def truck(x,y,k=1):
 s=path('M5 5H145L130 70H20z','url(#gold)')+path('M148 25h47l25 32v32h-72z',GOLD)+path('M161 32h29l19 23h-48z','#8fb0b9')+line(15,82,214,82,width=10)+wheel(42,91)+wheel(112,91)+wheel(186,91)
 return f'<g transform="translate({x} {y}) scale({k})">{s}</g>'
def paver(x,y,k=1):
 s=rect(45,73,160,34,INK,17)+circle(65,90,11,'#98a1a2')+circle(185,90,11,'#98a1a2')+path('M35 35h100l25 41H44z','url(#gold)')+path('M3 26l27 42h55l18-42z',GOLD)+rect(137,35,50,40,GOLD,3)+line(148,35,148,1,width=7)+line(183,35,183,1,width=7)+rect(126,-5,76,8,INK,3)+path('M187 65l43 17h46v20h-48l-31-14z','url(#steel)')
 return f'<g transform="translate({x} {y}) scale({k})">{s}</g>'
def roller(x,y,k=1):
 s=rect(40,34,145,40,'url(#gold)',8)+path('M85 35V-15h66v50',stroke=INK,width=7)+rect(73,-24,93,9,INK,3)+rect(85,-9,65,40,'#9cb7bc',3)+wheel(58,83,33)+rect(138,59,72,60,'url(#steel)',17)+path('M158 68v43M192 68v43',stroke='#708087',width=2)
 return f'<g transform="translate({x} {y}) scale({k})">{s}</g>'
# 1: material chain with machinery, rather than interchangeable boxes.
s=start('From rock to a road people use','Aggregate and binder travel through production, delivery, placement and compaction. Preparation and inspection support every stage.',850)
s+=path('M0 638Q230 585 460 620T960 607T1400 620V755H0z','#e9e0d4',stroke='none')
s+=path('M48 398l73-126 70 126 60-94 67 94z','url(#stone)',stroke='#8e7c66')+rect(330,285,62,113,'url(#steel)',3)+path('M330 285q31-32 62 0','url(#steel)')+rect(410,309,50,89,GOLD,3)+line(382,331,424,365,RED,9)
s+=truck(565,288,.85)+paver(870,302,.82)+roller(1175,313,.7)
for i,(x,a,b,c) in enumerate([(45,'01  SOURCE','Aggregate + binder','Verify approved supply.'),(329,'02  PRODUCE','Plant + mix record','Make the specified mixture.'),(566,'03  DELIVER','Haul + delivery ticket','Maintain traceability.'),(869,'04  PLACE','Tractor + screed','Feed, spread and shape.'),(1150,'05  COMPACT','Roller + checks','Densify and verify.')]):
 s+=t(x,232,a,19,RED,700)+t(x,455,b,20)+lines(x,489,([c] if len(c)<24 else [c.rsplit(' ',2)[0], ' '.join(c.rsplit(' ',2)[1:])]),18,gap=24)
 if i<4:s+=line(x+190,368,x+242,368,RED,4,True)
s+=rect(40,551,1320,113,'white',12)+t(65,593,'THE FOUNDATION RUNS UNDER EVERY STEP',20,TEAL,700)+t(65,630,'People • prepared support • drainage • approved documents • checks • care for the public',23)
s+=t(45,720,'Explain the handover: what arrives, what changes, and what evidence travels with it?',25,INK,700)
save('road-chain',s,850,'Original illustration · Machine silhouettes show functions; they do not identify a model or safe operating arrangement.')
# 2: road surfaces comparative illustrations
s=start('A road’s purpose does not name its surface','Four surface examples and a seasonal ice-road category. Uses and structures must be established separately.',700)
for i,(name,fill,desc) in enumerate([('Earth','#9b7b56','Shaped ground'),('Gravel','url(#stone)','Unbound mineral surface'),('Asphalt','url(#asphalt)','Aggregate with binder'),('Concrete','#d3d3cc','Cement-based pavement')]):
 x=38+i*341;s+=rect(x,190,316,405,'white')+t(x+22,233,name,27,INK,700)+path(f'M{x+85} 280h140l45 175h-230z',fill,stroke='#9a9289',width=2)
 if i==3:s+=line(x+64,370,x+247,370,'#92938e',2)
 if i==2:s+=path(f'M{x+155} 294v34m0 20v48m0 20v25',stroke=GOLD,width=5)
 s+=t(x+22,506,desc,20)+t(x+22,550,'Purpose must be checked.',19,'#625d58')
s+=t(40,640,'Ice roads are seasonal, authority-controlled routes; appearance cannot establish ice capacity.',22,TEAL,700)
save('road-surfaces',s,700)
# 3 history paired timelines, no misleading linear engineering evolution
s=start('Dates tell different stories','Separate the events on the Alaska Highway timeline from unrelated international road milestones.',720)
s+=t(40,208,'ALASKA HIGHWAY  /  DISTINCT EVENTS',20,RED,700)+line(100,312,1300,312,'#b9ada0',6)
for x,year,ls in [(130,'1942',['Pioneer road','completed']),(490,'1943',['Permanent','location']),(850,'1946',['Canadian portion','transferred to DND']),(1220,'1948',['Civilian non-military','use began'])]:
 s+=circle(x,312,14,RED)+t(x,276,year,33,INK,700,'middle')+''.join(t(x,363+j*30,z,20,INK,400,'middle') for j,z in enumerate(ls))
s+=rect(38,457,1324,172,'white')+t(65,500,'OTHER CONTEXTS — A SEPARATE TIME SCALE',20,TEAL,700)+lines(65,543,['312 BCE onward: Via Appia developed in a Roman military, settlement and trade context.','1956: U.S. Federal-Aid Highway Act — one major step in the Interstate system.'],23)
save('history-timeline',s,720,'Based on PSPC (2025), UNESCO (2024) and FHWA historical accounts cited in Chapter 2. Not to time scale.')
# 4 crew handover loop
s=start('A handover is complete when it is understood','Read back the location, task, limits and change. Record unresolved questions and the person responsible.',720)
for x,label,num in [(55,'STATE THE WORK','01'),(518,'READ IT BACK','02'),(980,'CONFIRM / CORRECT','03')]:
 s+=circle(x+45,235,34,RED)+t(x+45,244,num,23,'white',700,'middle')+t(x,309,label,24,INK,700)
s+=lines(55,364,['Location + document version','Task + people involved','Hazards + agreed controls'],22)+lines(518,364,['Say it in your own words.','Point to the same feature.','Name what is uncertain.'],22)+lines(980,364,['Resolve the mismatch.','Agree the next action.','Keep a usable record.'],22)
s+=line(367,340,480,340,RED,4,True)+line(837,340,945,340,RED,4,True)+path('M1160 470V540H185V470',stroke=TEAL,width=4)+t(700,582,'A changed condition starts a new check.',25,TEAL,700,'middle')
save('handover',s,720,'Communication + Collaboration + Writing · An unheard instruction is not a shared plan.')
# 5 fictional site map, also interactive layer asset
s=start('Cedar Learning Access  /  P-01 revision B','Fictional non-georeferenced plan. An entrance, boundary, utility record and site point have different meanings.',900)
s+=rect(40,185,930,586,'#e7e4d8')+path('M73 220H927V727H73z',stroke='#7f6855',width=4,extra='stroke-dasharray="12 7"')
s+=path('M45 640H960',stroke='#747b7c',width=76)+path('M50 640H950',stroke='white',width=3,extra='stroke-dasharray="17 14"')
s+=rect(280,264,113,375,'url(#asphalt)',0)+rect(232,215,270,64,'#d0b88e',3)+t(367,254,'Learning centre',22,INK,700,'middle')
s+=path('M337 618V302',stroke=GOLD,width=3,extra='stroke-dasharray="10 8"')+line(426,300,426,610,RED,2)+line(419,300,433,300,RED,2)+line(419,610,433,610,RED,2)+t(446,456,'50 m',24,RED,700)+line(283,578,392,578,'white',2)+t(336,563,'6 m',24,'white',700,'middle')
s+=circle(337,635,14,RED)+circle(626,412,12,TEAL)+t(648,419,'Site point',22)+t(355,692,'Confirmed teaching entrance',21,RED,700)
s+=path('M115 493Q280 442 486 474T895 485',stroke='#5766a2',width=6,extra='stroke-dasharray="4 10"')+rect(540,518,335,76,'white')+lines(557,548,['Utility record: approximate','Status / alignment unverified'],18)
s+=t(990,222,'READ THE LEGEND',20,RED,700)+circle(1011,272,10,RED)+t(1038,280,'Entrance point',21)+circle(1011,325,10,TEAL)+t(1038,333,'Site point',21)+path('M998 378h35',stroke='#7f6855',extra='stroke-dasharray="9 6"')+t(1045,385,'Practice boundary',21)+path('M998 431h35',stroke='#5766a2',width=5,extra='stroke-dasharray="3 8"')+t(1045,438,'Utility record',21)+lines(995,512,['Points locate features.','Lines trace features.','Polygons enclose areas.','','A symbol cannot confirm','title, permission or','safe excavation limits.'],20)
s+=line(895,295,895,243,INK,4,True)+t(895,227,'N',22,INK,700,'middle')
s+=t(42,817,'Use written dimensions for calculations. Screen distance is not a measurement scale.',23,TEAL,700)
save('site-plan',s,900,'Fictional classroom geometry · Original ACCESS illustration informed by GOSTROGIS CONSULTING map-reading workflows.')
# 6 plan/profile/section arranged with numerical relationships
s=start('Three views. Three different questions.','Plan gives length and width; profile gives elevation along the route; cross-section identifies transverse form and layers.',860)
s+=t(45,214,'PLAN  /  WHERE AND HOW WIDE?',23,RED,700)+rect(65,263,510,82,'url(#asphalt)',0)+path('M80 304H560',stroke=GOLD,width=3,extra='stroke-dasharray="13 9"')+line(65,372,575,372,RED,2)+t(320,410,'50 m horizontal length',23,INK,400,'middle')+t(594,313,'6 m',23,INK,700)
s+=t(754,214,'PROFILE  /  HOW HIGH?',23,RED,700)+path('M780 365H1310M780 365V260',stroke='#8b8178',width=2)+path('M789 345L1290 278',stroke=RED,width=5)+t(780,401,'0 m  /  100.00 m',20)+t(1120,255,'50 m / 100.50 m',20)+t(816,448,'Rise = 0.50 m   •   Run = 50 m',22)+t(816,486,'0.50 ÷ 50 × 100 = 1% grade',22,TEAL,700)
s+=t(45,500,'CROSS-SECTION  /  WHAT LAYERS?',23,RED,700)+path('M65 589L320 570 575 589V617H65z','url(#asphalt)')+rect(65,618,510,60,'url(#stone)',0)+path('M65 679H575V718H65z','#a98d68',stroke='none')+line(585,590,674,560,RED,2)+t(690,565,'Illustrative surface course',22)+line(585,648,674,648,RED,2)+t(690,654,'Aggregate base',22)+line(585,700,674,725,RED,2)+t(690,732,'Prepared subgrade',22)
save('three-views',s,860,'P-01 revision B is fictional · Vertical scales exaggerated · The section supplies no design dimensions or acceptance criteria.')
# 7 quantity graphic showing dimensional conversion
s=start('Keep each unit attached to its quantity','A fictional rectangular layer is calculated with 50 metres length, 6 metres width and 40 millimetres thickness.',730)
s+=path('M70 335l330-98 226 99-328 107z','url(#asphalt)')+path('M70 335v33l228 109v-34z','#686e6e')+path('M298 443v34l328-107v-34z','#242829')+t(167,519,'Length × width × thickness',24,INK,700)+t(60,268,'50 m',27,RED,700)+t(530,274,'6 m',27,RED,700)+line(636,337,680,307,RED,2)+t(690,309,'40 mm = 0.040 m',26,RED,700)
for y,a,b in [(392,'AREA','50 m × 6 m = 300 m²'),(464,'VOLUME','300 m² × 0.040 m = 12 m³'),(536,'MODEL MASS','12 m³ × 2.00 t/m³ = 24.00 t')]:s+=t(735,y-27,a,16,TEAL,700)+t(735,y,b,26)
s+=rect(40,590,1320,70,'white')+t(65,634,'2.00 t/m³ is an invented teaching factor. It is not a field density or an acceptance value.',23)
save('quantity',s,730,'Original worked diagram · Dimensions exaggerated · No waste, tapers or compaction allowance is included in this model.')
# 8 exposure routes silhouette, all four routes
s=start('A hazard needs a route to reach you','Chemical exposure can occur by inhalation, ingestion, skin absorption or injection. Other hazards have other mechanisms.',850)
s+=circle(690,269,55,'#d1b297')+path('M638 328q52-22 104 0l46 172-56 12-4 194h-35l-9-148-9 148h-35l-4-194-56-12z','#334b54',stroke='none')+path('M644 330l-34 131M738 330l34 131',stroke=GOLD,width=13)
items=[(55,225,'INHALATION',['Airborne contaminant enters','through breathing.'],(608,250,669,266)),(890,225,'INGESTION',['Contamination reaches the','mouth, food or drink.'],(870,270,718,290)),(55,485,'ABSORPTION',['Some substances pass','through the skin.'],(602,519,638,468)),(890,485,'INJECTION',['Pressurized fluid can enter','through a small skin wound.'],(873,521,766,466))]
for x,y,h,ls,lead in items:
 s+=rect(x,y-31,449,165,'white')+t(x+22,y+7,h,24,RED,700)+lines(x+22,y+51,ls,22)+line(*lead,RED,2,True)
s+=t(700,755,'Match the control to the route. Read the product SDS and the task conditions.',23,TEAL,700,'middle')
save('exposure-routes',s,850,'Original concept illustration · A small injection wound can be a medical emergency; report and obtain emergency care promptly.')
# 9 barrier chain
s=start('Control the exposure before it reaches a person','Assess the task, eliminate or reduce the hazard, check the controls and reassess when conditions change.',780)
for i,(a,b,c) in enumerate([('REMOVE / CHANGE','Eliminate the task hazard','or use a safer alternative.'),('CONTROL AT SOURCE','Engineering measures','contain or separate it.'),('ORGANIZE THE WORK','Procedure, timing, access','and training support control.'),('PROTECT THE PERSON','PPE chosen for the hazard','and its remaining exposure.')]):
 x=40+i*340;h=350-i*45;y=232+i*45
 s+=rect(x,y,300,h,['#286864','#477975','#796c52','#8b3d3b'][i])+t(x+20,y+44,'0'+str(i+1),24,'#ffdc75',700)+t(x+20,y+93,a,19,'white',700)+lines(x+20,y+137,[b,c],20,'white')
s+=path('M80 635H1310',stroke=RED,width=4,extra='marker-end="url(#arrow)"')+t(695,684,'Check effectiveness → record → reassess after a change',27,INK,700,'middle')
save('controls',s,780,'Conceptual sequence based on WorkSafeBC OHS Regulation § 5.55 and hazard-assessment principles. Use the applicable clauses.')
# 10 rigging angle graphic no actual load capacities
s=start('Rigging: identify the angle you are reading','The WorkSafeBC Table 15-3 angle is measured from vertical. This picture identifies geometry, not a lift plan or a capacity.',860)
s+=path('M701 220v38q0 25-25 25q-25 0-25-25',stroke='#68767d',width=16)+circle(677,292,12,'url(#steel)')+path('M677 300L421 567M677 300L933 567',stroke='#7f8b8f',width=10)+path('M677 300V588',stroke=TEAL,width=3,extra='stroke-dasharray="10 7"')+rect(398,565,560,85,'url(#steel)',4)+circle(421,574,12,INK)+circle(933,574,12,INK)
s+=path('M677 407A107 107 0 0 0 750 379',stroke=RED,width=4)+line(750,379,840,440,RED,2)+t(850,462,'Angle from vertical',23,RED,700)+t(693,536,'Vertical reference',20,TEAL,700)
s+=lines(48,237,['BEFORE A PLAN:','Known load and lift points','Identified, compatible gear','Legible working load limit','Pre-use inspection','Qualified people'],23,gap=38)+lines(1011,247,['CHECK THE TABLE','Angle convention','Configuration','Manufacturer limits','Complete clauses'],21,gap=39)
s+=rect(40,695,1320,80,'white')+t(65,745,'No load value, rigging selection or capacity is supplied. A qualified rigger must establish the arrangement.',22)
save('rigging-angle',s,860,'Original geometry teaching diagram · WorkSafeBC OHS Regulation §§ 15.2, 15.4–15.5, 15.31 and 15.34.')
# 11 public safe separation site no distances
s=start('Plan the people routes as carefully as the work','A conceptual work-zone plan shows a public route and work area separated with a designed access point.',800)
s+=rect(45,205,920,490,'#deddd3')+rect(85,255,245,388,'#d7e9e5')+path('M210 610V280',stroke=TEAL,width=5)+path('M210 285l-15 20m15-20 15 20',stroke=TEAL,width=5)+t(105,237,'PUBLIC ROUTE',21,TEAL,700)
s+=path('M387 223V654',stroke=RED,width=9)+t(408,246,'Designed separation',21,RED,700)+paver(590,330,1)+roller(620,530,.8)
s+=circle(200,420,14,TEAL)+path('M200 440v45m-20-25 20-15 20 15m-20 25-15 25m15-25 15 25',stroke=TEAL,width=7)
s+=lines(1003,258,['ASK BEFORE SETUP','Where can people go?','Is the route accessible?','Who controls access?','Can drivers see workers?','How is help reached?','','Use the approved traffic','plan and site procedure.'],21,gap=34)
s+=t(45,738,'A cone or drawn line does not establish adequate separation. The site plan must address the actual hazards.',22)
save('public-route',s,800,'Original fictional scene · No traffic-control spacing, clearance or protective-barrier specification is implied.')
# 12 lifecycle bounded diagram
s=start('Follow the whole service, not a single claim','Compare material production, transport, construction, maintenance and end-of-life for an equivalent pavement service.',720)
for i,(h,l) in enumerate([('MATERIALS','Extraction + production'),('TRANSPORT','Distances + loads'),('CONSTRUCTION','Equipment + placement'),('SERVICE LIFE','Maintenance + use'),('END-OF-LIFE','Recovery + disposal')]):
 x=40+i*271;s+=rect(x,244,242,223,'white')+circle(x+39,282,21,RED)+t(x+39,289,str(i+1),20,'white',700,'middle')+t(x+20,343,h,21,INK,700)+t(x+20,389,l,17)
 if i<4:s+=line(x+246,353,x+266,353,RED,2,True)
s+=path('M70 492v55H1325v-55',stroke=TEAL,width=4)+t(700,597,'Same required function • same comparison period • stated quantities and boundaries',23,TEAL,700,'middle')
save('life-cycle',s,720,'Original comparison framework · A production-only percentage does not establish a whole-road advantage.')
# Cover art uses the same material textures and equipment vocabulary without an operating layout.
s=start('Roadbuilding connections','Original conceptual cover art: aggregate support, asphalt surface and paving equipment. No real place or operating arrangement.',620)
s+=path('M0 285l210-103 170 105 220-118 205 117 170-83 225 93v324H0z','#e2e5dc',stroke='none')
s+=path('M90 365l450-139 749 208v35L839 607 90 399z','url(#stone)',stroke='none')
s+=path('M90 365l450-139 749 208-450 139z','url(#asphalt)',stroke='#68706d',width=2)
s+=path('M205 367L553 260 1156 431',stroke=GOLD,width=5,extra='stroke-dasharray="28 20"')
s+=truck(335,269,.68)+paver(706,337,.8)+roller(1058,410,.63)
save('cover-art',s,620,'ACCESS IS4S · People, materials and careful decisions connect the work.')
print('Drew 13 original SVGs, including cover art.')
