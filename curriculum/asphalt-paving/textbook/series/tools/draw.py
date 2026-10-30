"""Original SVG explanations for the complete asphalt study series; no operating settings implied."""
from pathlib import Path
from html import escape as E
import math,json,hashlib,random
R=Path(__file__).resolve().parents[1];OUT=R/'assets/diagrams';OUT.mkdir(exist_ok=True)
INK='#242827';CREAM='#f7f2e8';RED='#a93332';GOLD='#d5ad62';TEAL='#276b66';MUTED='#59635d';PALE='#e5ddcc';WHITE='#fffdf8'
registry=[]
class Art:
 def __init__(self,id,title,subtitle,desc=None,h=620):
  self.id=id;self.title=title;self.desc=desc or subtitle;self.h=h
  self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {h}" role="img" aria-labelledby="title desc"><title id="title">{E(title)}</title><desc id="desc">{E(self.desc)}</desc><defs><pattern id="grain" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="4" cy="7" r="1.2" fill="#b9aa8e" opacity=".45"/><circle cx="19" cy="18" r="1" fill="#b9aa8e" opacity=".3"/></pattern><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="none" stroke="{TEAL}" stroke-width="1.4"/></marker><pattern id="hatch" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M-2 12L12-2M4 16L16 4" stroke="{RED}" stroke-width="2" opacity=".22"/></pattern></defs>'];self.rect(0,0,1000,h,CREAM);self.rect(0,0,1000,106,INK);self.text(32,32,'ACCESS IS4S  /  ASPHALT STUDY',13,GOLD,700);self.text(32,76,title,29,WHITE,700);self.text(32,140,subtitle,18,MUTED)
 def rect(self,x,y,w,h,c=WHITE,r=0,stroke=None):self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}"'+(f' stroke="{stroke}" stroke-width="2"' if stroke else '')+'/>')
 def text(self,x,y,t,size=19,c=INK,w=400,anchor=None):self.s.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{w}" fill="{c}"'+(f' text-anchor="{anchor}"' if anchor else '')+f'>{E(str(t))}</text>')
 def lines(self,x,y,lines,size=18,c=MUTED,gap=27):
  for i,t in enumerate(lines):self.text(x,y+i*gap,t,size,c)
 def path(self,d,c=TEAL,w=3,arrow=False,fill='none',dash=None):self.s.append(f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{w}"'+(' marker-end="url(#arrow)"' if arrow else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def circle(self,x,y,r,c=GOLD,stroke=None):self.s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"'+(f' stroke="{stroke}" stroke-width="2"' if stroke else '')+'/>')
 def note(self,t):self.rect(32,self.h-83,936,48,INK,7);self.text(49,self.h-52,t,18,WHITE,700)
 def card(self,x,y,w,title,lines,c=TEAL,h=122):self.rect(x,y,w,h,WHITE,10);self.rect(x,y,6,h,c);self.text(x+18,y+31,title,21,c,700);self.lines(x+18,y+66,lines,17)
 def machine(self,x,y,kind='paver',scale=1):
  # Simplified side-view silhouettes support identification, not model-specific procedures.
  self.s.append(f'<g transform="translate({x} {y}) scale({scale})">')
  if kind=='truck':
   self.path('M10 35H175L159 98H18Z',INK,2,fill=GOLD);self.rect(178,58,68,53,TEAL,4);self.rect(191,65,35,23,WHITE,2);self.rect(17,105,228,14,INK)
   for xx in [43,83,210]:self.circle(xx,123,20,INK);self.circle(xx,123,9,PALE)
  elif kind=='roller':
   self.rect(40,45,140,66,GOLD,6);self.rect(81,4,77,10,INK,2);self.path('M89 15V69M150 15V69',INK,5);self.rect(97,49,30,22,TEAL,3)
   for xx in [55,178]:self.circle(xx,119,38,INK);self.circle(xx,119,29,PALE);self.circle(xx,119,9,MUTED)
  elif kind=='mill':
   self.path('M28 62H205V115H20Z',INK,2,fill=GOLD);self.rect(72,18,88,8,INK);self.path('M80 26V63M152 26V63',INK,4);self.path('M175 65L302-10L310 5L185 85Z',INK,2,fill=TEAL);self.rect(18,113,70,28,INK,12);self.rect(152,113,70,28,INK,12);self.circle(120,122,27,MUTED)
  elif kind=='broom':
   self.rect(20,55,170,68,GOLD,6);self.rect(77,3,89,70,TEAL,5);self.rect(87,13,68,43,WHITE,4)
   for xx in [49,171]:self.circle(xx,128,24,INK);self.circle(xx,128,11,PALE)
   self.path('M175 92L245 125',INK,10);self.rect(223,113,59,35,TEAL,12)
   for xx in range(228,280,8):self.path(f'M{xx} 116v30',GOLD,2)
  else:
   self.path('M18 61H108L92 111H30Z',INK,2,fill=GOLD);self.rect(102,48,110,63,GOLD,5);self.rect(136,8,72,9,INK,2);self.path('M144 17V53M198 17V53',INK,4);self.rect(103,109,112,35,INK,15);self.path('M200 89L274 123',TEAL,8);self.path('M240 126H302L293 142H228Z',INK,2,fill=TEAL)
  self.s.append('</g>')
 def save(self,credit=None):
  self.text(32,self.h-13,'Conceptual teaching diagram · Use the stated case and actual project/machine requirements.',13,MUTED)
  p=OUT/(self.id+'.svg');p.write_text(''.join(self.s)+'</svg>\n');registry.append({'id':self.id,'file':'assets/diagrams/'+p.name,'title':self.title,'alt':self.desc,'credit':credit or 'ACCESS IS4S. (2026). '+self.title+' [Original instructional SVG]. Conceptual explanation based on the cited chapter readings; geometry and operating arrangements are illustrative, not prescribed settings.','source_link':None,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'provenance':{'type':'original SVG','generator':'tools/draw.py'}})
# Movement plans: the conflict is physically visible.
for id,title,kind,label in [('truck-interface','Keep the truck–paver interface clear','truck','TRUCK + PAVER'),('traffic-zones','Give people a protected route','paver','MOVING WORK AREA'),('roller-safe-zones','See the whole roller movement','roller','TRAVEL + ARTICULATION'),('screed-safe-zones','Plan for the moving screed width','paver','EXTENSION + ROLLER PATH'),('handwork-zone','The tool needs room too','paver','HANDWORK + MACHINE ROUTE')]:
 a=Art(id,title,'Plan view concepts and side-view symbols · no clearance distances are prescribed.')
 a.rect(40,184,920,280,PALE,12);a.rect(40,198,920,55,TEAL,8);a.text(62,233,'PROTECTED PEOPLE ROUTE',20,WHITE,700);a.path('M66 266H933',RED,4,dash='10 7');a.machine(120,282,kind,.9)
 if id=='truck-interface':a.machine(500,282,'paver',.9)
 else:a.machine(620,287,'roller',.8)
 a.rect(395,292,170,145,'url(#hatch)',12,RED);a.text(413,326,'CONFLICT',18,RED,700);a.lines(413,357,['Keep clear','Stop if entry'],17,RED)
 a.text(62,493,label,17,TEAL,700);a.text(594,493,'Confirm signals before movement.',17,MUTED);a.note('A warning signal does not replace a controlled route and acknowledged communication.');a.save()
a=Art('broom-anatomy','Follow the broom’s working systems','Identify the actual model and options before operating or servicing.')
a.machine(270,245,'broom',1.7)
for x,y,tx,ty,label in [(90,212,425,273,'Operator station'),(75,437,340,427,'Travel system'),(650,214,594,364,'Engine + hydraulics'),(770,425,695,470,'Rotating brush')]:a.text(x,y,label,21,TEAL,700);a.path(f'M{x+25} {y+10}L{tx} {ty}',MUTED,2)
a.note('Brush, drive and dust-control functions must be checked on the actual machine.');a.save()
a=Art('pneumatic-system','Air power has a path—and stored energy','Trace the system from supply to the tool. Identify every connection.')
a.rect(65,235,170,100,GOLD,40);a.circle(106,355,22,INK);a.circle(196,355,22,INK);a.text(83,285,'AIR SUPPLY',20,INK,700);a.path('M238 285C330 285 300 385 409 385S520 285 625 285',TEAL,12);a.rect(625,261,50,48,INK,8);a.path('M738 235v160M699 240H777',INK,19);a.path('M738 395v66',MUTED,10);a.circle(738,310,29,GOLD)
a.lines(70,431,['Supply and controls','Use the specified pressure.'],18);a.lines(337,220,['Hose + couplings','Inspect and restrain as required.'],18);a.lines(755,353,['Tool body','Retainer + steel'],18);a.note('Stop, isolate and release pressure through the approved procedure before disconnection.');a.save()
a=Art('propane-assembly','Match every part of the fuel system','Conceptual vapour-withdrawal arrangement · use the actual product instructions.')
a.rect(95,245,140,210,GOLD,35,INK);a.rect(135,215,60,38,INK,7);a.path('M145 208V181H187V208',INK,5);a.circle(270,235,28,TEAL);a.path('M195 230H243M298 235C420 235 366 420 510 420S620 250 715 250',TEAL,10);a.path('M714 250H820L880 220V280L820 250',INK,10)
a.lines(65,488,['Cylinder + valve'],20,TEAL);a.lines(310,194,['Compatible regulator'],20,TEAL);a.lines(370,478,['Rated hose + fittings'],20,TEAL);a.lines(707,330,['Torch + controls'],20,TEAL);a.note('Confirm identity, compatibility and approved leak testing. Never use a flame to test leaks.');a.save()
a=Art('heat-response','Recognize heat strain and act early','A change in a person’s condition matters more than keeping the schedule.')
a.rect(55,190,255,292,WHITE,12);a.circle(181,262,37,GOLD);a.path('M122 413V341Q181 286 240 341V413',TEAL,3,fill=TEAL);a.path('M230 219q24-30 32 4q8 25-16 31q-26 1-16-35',RED,2,fill=RED);a.lines(80,449,['Notice a change.'],22,RED)
a.card(350,190,595,'STOP + GET HELP',['Confusion, collapse or severe symptoms:','activate the emergency response and first aid.'],RED,130);a.card(350,346,595,'PROTECT + REASSESS',['Follow trained first-aid/cooling directions.','Review exposure, breaks, water and work plan.'],TEAL,130);a.note('Do not leave a seriously affected person alone or send them back to work without assessment.');a.save()
a=Art('fatigue-clock','Time off is not all sleep time','Fictional example: a 20:00 finish and 06:00 start leave 10 hours between shifts.')
a.path('M70 300H930',MUTED,2)
segments=[('Travel',2,TEAL),('Meals + care',1.5,GOLD),('Call',.5,RED),('Sleep opportunity',6,INK)];x=70
for label,h,c in segments:
 w=h*86;a.rect(x,243,w,80,c,3);a.text(x+w/2,355,f'{h:g} h',23,c,700,'middle');a.text(x+w/2,216,label,17,c,700,'middle');x+=w
a.lines(70,416,['10 − 2 − 1.5 − 0.5 = 6 hours of sleep opportunity','A further 1.5-hour delay leaves 4.5 hours—not a safe-work approval.'],24,INK,42);a.note('Plan fatigue controls around actual sleep opportunity, workload and reported condition.');a.save()
a=Art('transport-budget','Add the whole load before comparing ratings','Fictional trailer example · all values are mass, in kilograms.')
a.text(65,203,'3,500 kg trailer rating',24,INK,700);x=65
for label,m,c in [('Trailer',900,TEAL),('Machine',2300,GOLD),('Tools',420,RED)]:
 w=m/4;a.rect(x,258,w,88,c);a.text(x+w/2,385,str(m)+' kg',21,INK,700,'middle');a.text(x+w/2,231,label,19,INK,700,'middle');x+=w
a.path('M940 215V400',RED,3,dash='7 5');a.text(65,449,'900 + 2,300 + 420 = 3,620 kg',29,INK,700);a.text(65,489,'120 kg over this rating. Check all other limits too.',24,RED,700);a.note('Axle, tire, hitch, vehicle, ramp and route requirements also matter.');a.save()
# Material routes and systems.
a=Art('aggregate-process','Follow aggregate through the plant','Processing changes size and separates material; moving systems need controlled access.')
for x,title,lines in [(40,'FEED',['Raw material','Controlled supply']),(280,'CRUSH',['Jaw / cone / impact','Reduce particle size']),(520,'SCREEN',['Separate by size','Check screen condition']),(760,'STORE',['Keep products apart','Prevent contamination'])]:a.card(x,205,200,title,lines,TEAL,140)
for x in [248,488,728]:a.path(f'M{x} 275h24',arrow=True)
a.path('M620 350V400H380V354',RED,3,arrow=False);a.text(411,435,'Oversize may return for more crushing.',20,RED);a.text(66,485,'Conveyors connect the process. Wash systems may remove unwanted fines.',21,INK);a.note('A stopped belt is not an isolated belt. Use the actual energy-control procedure.');a.save()
a=Art('gradation-curve','A gradation curve shows what passes','Fictional 1,000 g sample · sieve sizes shown for calculation practice only.')
for yy,val in [(440,0),(375,25),(310,50),(245,75),(180,100)]:a.path(f'M95 {yy}H610',PALE,1);a.text(49,yy+6,str(val),17,MUTED)
a.path('M95 180V440H610',INK,3);a.text(42,165,'% passing',16,TEAL,700)
pts=[(145,388,20,'0.6'),(300,310,50,'2.36'),(455,219,85,'4.75'),(595,180,100,'9.5')];a.path('M145 388L300 310L455 219L595 180',TEAL,4)
for x,y,v,l in pts:a.circle(x,y,6,RED);a.text(x,467,l,18,INK,400,'middle');a.text(x+10,y-10,str(v)+'%',17,TEAL,700)
a.text(174,500,'Sieve opening, mm · spaced schematically',17,MUTED);a.card(658,207,305,'MASS CHECK',['150 + 350 + 300 + 200','= 1,000 g retained total','Passing = 100% −','cumulative retained %'],RED,205);a.note('Check the sample total, units and cumulative calculation before plotting.');a.save()
a=Art('material-cycle','Reuse materials through a verified process','RAP means reclaimed asphalt pavement. Suitability depends on the designed use.')
for x,y,title,ls in [(55,195,'EXISTING ROAD',['Assess condition','Plan recovery']),(560,195,'RECOVER + SORT',['Mill / process','Keep traceability']),(560,370,'DESIGN + TEST',['Confirm material suitability','Approve the mixture/layer']),(55,370,'PLACE + MAINTAIN',['Build to the accepted plan','Review service performance'])]:a.card(x,y,385,title,ls,TEAL,130)
a.path('M450 257H545',arrow=True);a.path('M755 330V356',arrow=True);a.path('M545 435H455',arrow=True);a.path('M246 357V336',arrow=True);a.note('A recycled percentage is not the same as an emissions-reduction percentage.');a.save()
a=Art('containment','A container and its containment do different jobs','Conceptual section · capacity and materials must meet the actual requirements.')
a.rect(95,420,800,40,TEAL);a.rect(95,260,35,200,TEAL);a.rect(860,260,35,200,TEAL);a.rect(130,376,730,44,'#b8d4cd');a.rect(300,220,375,150,GOLD,22,INK);a.rect(340,370,40,50,INK);a.rect(590,370,40,50,INK);a.text(353,288,'PRIMARY TANK',23,INK,700);a.path('M480 370v36',RED,4,arrow=False);a.text(370,493,'Secondary containment catches a release.',22,TEAL,700);a.lines(68,203,['Inspect the tank.'],19);a.lines(697,203,['Protect drains.'],19);a.note('Confirm compatibility, capacity, inspection and waste handling for the actual product and site.');a.save()
a=Art('baghouse','Separate the gas path from collected solids','Conceptual baghouse section · particle collection is not proof of total emission control.')
a.rect(295,195,405,255,WHITE,4,INK)
for x in range(340,670,65):a.rect(x,245,26,150,PALE,12,TEAL)
a.path('M75 345H285',TEAL,8,True);a.text(60,307,'Gas + particles',21,TEAL,700);a.path('M700 223H910',TEAL,8,True);a.lines(741,178,['Gas outlet'],21,TEAL)
a.path('M295 450L500 515L700 450',INK,3,fill=PALE);a.path('M500 515v35',RED,7);a.text(710,467,'Collected solids',20,RED,700);a.path('M698 475L550 505',RED,2);a.note('Inspect the actual system, monitoring and permit conditions; control worker exposure separately.');a.save()
a=Art('mix-phases','A compacted mixture still contains air voids','Conceptual cross-section · particle sizes and proportions are illustrative.')
a.rect(55,190,530,300,INK,16);rng=random.Random(8)
for i in range(35):
 x=rng.randint(83,554);y=rng.randint(217,462);r=rng.randint(10,28);a.path(f'M{x-r} {y}L{x-r/2} {y-r}L{x+r} {y-r/3}L{x+r/2} {y+r}L{x-r} {y}Z',GOLD,6,fill=PALE)
for x,y in [(195,265),(400,425),(505,290)]:a.circle(x,y,13,WHITE)
a.card(635,190,310,'AGGREGATE',['Solid mineral skeleton'],TEAL,88);a.card(635,296,310,'BINDER',['Coats and binds particles'],RED,88);a.card(635,402,310,'AIR VOIDS',['Part of mixture structure'],INK,88);a.note('The illustration explains phases. Mix design and testing establish actual properties.');a.save()
# Calculation bases shown spatially, with exact fictional values.
a=Art('binder-basis','The denominator changes the percentage','Fictional mixture: 100 kg dry aggregate plus 5 kg binder.')
a.rect(70,220,660,100,PALE,6);a.rect(730,220,80,100,RED,6);a.text(260,280,'100 kg aggregate',27,INK,700);a.text(745,283,'5 kg',22,WHITE,700)
a.card(65,370,415,'ON AGGREGATE MASS',['5 ÷ 100 × 100 = 5.00%'],TEAL,116);a.card(520,370,415,'ON TOTAL MIX MASS',['5 ÷ 105 × 100 = 4.76%'],RED,116);a.note('Compare results only after confirming the same reporting basis and method.');a.save()
a=Art('density-bases','One in-place result, two reference bases','Fictional in-place density: 2.340 Mg/m³. Choose the required reference.')
a.card(55,192,420,'PLANT BRIQUETTE',['Reference: 2.400 Mg/m³','2.340 ÷ 2.400 × 100'],TEAL,160);a.card(525,192,420,'MAXIMUM THEORETICAL',['Reference: 2.500 Mg/m³','2.340 ÷ 2.500 × 100'],RED,160);a.text(115,435,'97.50%',56,TEAL,700);a.text(590,435,'93.60%',56,RED,700);a.text(75,488,'Marshall-style comparison',21,MUTED);a.text(550,488,'Maximum-theoretical comparison',21,MUTED);a.note('Neither percentage can be interpreted without the actual method, lot and contract requirements.');a.save()
a=Art('application-rate','Mass divided by area gives application rate','Fictional lot: 288 t over 2,400 m²; specified rate 120 kg/m².')
a.path('M80 330L385 210L590 310L285 435Z',INK,3,fill=PALE);a.path('M80 350L285 455L590 330',TEAL,3);a.text(220,330,'2,400 m²',27,INK,700);a.card(635,210,315,'CALCULATE',['288 t = 288,000 kg','288,000 ÷ 2,400','= 120 kg/m²'],TEAL,175);a.text(90,492,'120 ÷ 120 × 100 = 100% of the specified rate',27,RED,700);a.note('An average rate does not prove uniform thickness or full acceptance.');a.save()
a=Art('level-book','Keep the benchmark in the calculation','Fictional level run · elevations and instrument readings are in metres.')
a.path('M70 430H920',MUTED,4);a.path('M110 260V430M825 310V430',INK,5);a.path('M425 265L365 430M425 265L480 430',TEAL,5);a.rect(390,245,85,25,TEAL,5);a.path('M110 258H825',RED,2,dash='8 5');a.lines(65,199,['BM EL 100.000','Backsight 1.250'],20,INK);a.lines(655,199,['Foresight 1.670','Point EL 99.580'],20,INK);a.text(271,480,'HI = 100.000 + 1.250 = 101.250',25,TEAL,700);a.note('Point elevation = HI − foresight. Target 99.650 means 70 mm fill at this point.');a.save()
a=Art('grade-stakes','Read the mark, the offset and the datum','Fictional training stake · confirm the actual project legend before use.')
a.path('M125 185H440V430L280 500L125 430Z',INK,3,fill=GOLD);a.lines(154,231,['STA 0+125','2.0 m RT OFFSET','FG EL 102.400','C 0.060'],27,INK,53)
a.card(505,185,435,'LOCATION',['Station: 125 m along the alignment','Offset: reference away from the work'],TEAL,130);a.card(505,340,435,'LEVEL',['FG: finished-grade elevation','Cut: 60 mm from the defined mark'],RED,130);a.note('A stake’s top is not automatically the reference mark. Protect survey control.');a.save()
a=Art('smoothness-profile','Smoothness and crossfall answer different questions','Conceptual profiles · no acceptance limit or scale is implied.')
a.text(65,200,'ALONG THE ROAD',20,TEAL,700);a.path('M65 310C170 310 180 260 265 277S375 342 470 290S590 282 640 310',RED,5);a.path('M65 335H640',MUTED,2,True);a.text(155,383,'Longitudinal profile → IRI / local defects',19,INK)
a.text(706,200,'ACROSS THE ROAD',20,TEAL,700);a.path('M705 315L820 278L940 315',INK,5);a.path('M705 340H940',MUTED,2);a.text(736,383,'Crown / crossfall',19,INK);a.text(65,470,'Density is another measurement again: compaction relative to a stated reference.',21,INK);a.note('A good result for one property does not prove the others meet specification.');a.save()
a=Art('segregation','Look at distribution, then investigate the cause','Conceptual particle patterns · field classification uses agreed project criteria.')
for x,title,coarse in [(55,'MORE UNIFORM',False),(525,'COARSE CONCENTRATION',True)]:
 a.rect(x,218,420,230,INK,12);a.text(x,194,title,22,TEAL if not coarse else RED,700);rng=random.Random(20)
 for i in range(65):
  xx=x+rng.randint(20,400);yy=rng.randint(237,426);r=rng.randint(3,8) if not coarse or xx<x+215 else rng.randint(10,18);a.circle(xx,yy,r,PALE)
a.text(75,488,'Describe texture, location and timing. Do not assign blame from a picture.',22,INK);a.note('A suspected defect needs traceable evidence and an authorized disposition.');a.save()
# Process records: concrete decisions and evidence, with alternating shapes/paths.
flowdata={
'document-authority':('Find the document that governs the task','Check adoption and revision before applying a number.', [('CONTRACT','Edition + special provisions'),('DRAWING','Revision + location'),('METHOD','Approved procedure + roles'),('RECORD','Actual result + disposition')],'A historical table is useful for learning; the adopted project requirements govern work.'),
'quality-chain':('A quality result needs a traceable chain','One lot identifier connects the work to its evidence.', [('PLAN','Accepted material + method'),('SAMPLE','Location + time + identity'),('RESULT','Method + units + reference'),('DECISION','Authorized acceptance / hold')],'A missing link is a question to resolve, not a space to fill with an invented fact.'),
'sample-chain':('Keep the sample and its record together','Representative sampling and identification are different requirements.', [('PLAN','Method + random selection'),('COLLECT','Authorized safe access'),('LABEL','Mix + lot + station + time'),('TRANSFER','Seal / storage + custody')],'A large sample is not automatically representative. Preserve the approved selection.'),
'crew-communication':('A movement instruction needs a check-back','Use one designated movement signaller and a clear stop response.', [('IDENTIFY','Machine + location'),('INSTRUCT','Direction + limit'),('ACKNOWLEDGE','Repeat the key meaning'),('ACT / STOP','Stop if unclear or lost')],'Anyone can give an emergency stop. Restore shared understanding before resuming.'),
'isolation-states':('Stopped is not the same as isolated','Use the machine-specific procedure and verify the safe state.', [('STOP','End the task safely'),('ISOLATE','All hazardous energies'),('SECURE','Locks + stored-energy control'),('VERIFY','Confirm protection before work')],'Electrical, hydraulic, gravity, heat and stored energy may remain after shutdown.'),
'shutdown-state':('Leave a known safe state for the next person','Parking, inspection and handover are parts of the task.', [('POSITION','Stable ground + clear access'),('SHUT DOWN','Actual OMM sequence'),('SECURE','Supports + parking + access'),('HAND OVER','Defects + status + next action')],'Shutdown does not replace the full lockout required for hazardous access or service.'),
'maintenance-record':('Record the condition, not just a tick','The next operator needs to know what was actually checked.', [('IDENTIFY','Model / serial + meter'),('SERVICE','Chart + product + interval'),('INSPECT','Observation + location'),('RELEASE / HOLD','Authorized action + status')],'Mark completed, not applicable with a reason, or held for correction.'),
}
for id,(title,sub,items,note) in flowdata.items():
 a=Art(id,title,sub)
 for i,(h,l) in enumerate(items):
  x=45+(i%2)*490;y=205+(i//2)*165;a.card(x,y,420,h,[l],TEAL if i%2==0 else RED,125);a.circle(x+382,y+28,15,GOLD);a.text(x+377,y+34,str(i+1),17,INK,700)
 a.path('M475 266H521',arrow=True);a.path('M745 334V357',arrow=True);a.path('M521 431H475',arrow=True);a.note(note);a.save()
a=Art('truck-sample','A selected load keeps its identity','Fictional sampling plan · no truck access method is prescribed.')
a.machine(80,215,'truck',1.3);a.card(505,185,440,'PLAN',['Selected loads: 3 and 8','Collection method: approved procedure'],TEAL,125);a.card(505,340,440,'LABEL',['Load 8 · mix / lot / location / time','Record any missed selection or change'],RED,130);a.text(75,465,'Do not silently replace load 8 with load 7.',22,RED,700);a.note('Random selection, safe collection and traceable labelling all need to be satisfied.');a.save()
a=Art('temperature-reading','Surface and contact readings are different','Use the specified instrument, location, timing and units.')
a.rect(60,380,875,75,INK);a.rect(60,455,875,32,PALE);a.path('M218 215L180 380L290 380Z',GOLD,2,fill='#e8cf9d');a.rect(185,195,83,40,TEAL,6);a.path('M725 215V426',RED,8);a.rect(690,190,70,40,INK,5);a.lines(70,294,['INFRARED','Surface / emissivity / spot size'],20,TEAL);a.lines(590,294,['PROBE','Contact method / depth / response'],20,RED);a.note('Record how and where the value was obtained before comparing two readings.');a.save()
a=Art('milling-cut','Control the cut from a verified reference','Conceptual side section · the actual rotor and controls vary by model.')
a.rect(45,417,500,70,INK);a.rect(545,452,410,35,INK);a.rect(45,487,910,25,PALE);a.circle(530,405,73,GOLD,INK)
for deg in range(0,360,30):
 x=530+72*math.cos(math.radians(deg));y=405+72*math.sin(math.radians(deg));a.path(f'M{x} {y}l8 8',INK,5)
a.machine(350,212,'mill',1.1);a.path('M650 417v35M638 417h24M638 452h24',RED,3);a.text(680,441,'Cut depth',21,RED,700);a.text(85,387,'Existing surface',21,INK,700);a.text(690,492,'Milled profile',18,WHITE);a.note('Measure at authorized safe locations. An average depth does not prove a uniform profile.');a.save()
a=Art('paving-train','Coordinate the whole paving train','Conceptual roles · spacing and movement follow the actual site plan.')
a.machine(45,250,'truck',1);a.machine(335,250,'paver',1);a.machine(730,250,'roller',.9)
for x,t in [(70,'DELIVER'),(380,'PLACE + FORM'),(735,'COMPACT')]:a.text(x,218,t,23,TEAL,700)
a.path('M292 327H330',TEAL,4,True);a.path('M643 327H716',TEAL,4,True);a.lines(80,460,['Delivery continuity','Clear truck interface'],19);a.lines(382,460,['Steady feed + speed','Measured mat checks'],19);a.lines(735,460,['Approved pattern','Quality feedback'],19);a.note('Handwork and testing need coordinated safe access within the same plan.');a.save()
a=Art('screed-response','Allow the screed’s response to develop','Conceptual response curve · no universal distance or control increment is implied.')
a.path('M80 445H920M80 445V195',INK,3);a.path('M90 390H235C335 390 350 270 505 257S750 250 910 250',TEAL,5);a.path('M235 205V445',RED,2,dash='7 5');a.text(119,185,'Controlled change',20,RED,700);a.text(534,222,'New steady condition',20,TEAL,700);a.text(362,485,'Travel distance → observe → measure',23,INK,700);a.note('Repeated immediate corrections can obscure the cause and create an uneven mat.');a.save()
a=Art('handwork-patch','Plan the patch in three dimensions','Fictional rectangle: 1.2 m × 0.8 m × 0.06 m compacted depth.')
a.path('M95 295L450 195L675 320L320 430Z',INK,3,fill=INK);a.path('M95 295V343L320 478V430M320 478L675 366V320',TEAL,3,fill=PALE);a.path('M95 278L450 178M695 320L472 194',GOLD,3);a.text(220,215,'1.2 m',25,TEAL,700);a.text(590,242,'0.8 m',25,TEAL,700);a.lines(728,337,['0.06 m','compacted'],22,RED);a.text(98,510,'Volume = 1.2 × 0.8 × 0.06 = 0.0576 m³',27,INK,700);a.note('This is geometry. The repair detail determines materials, lift method and compaction.');a.save()
a=Art('roller-types','Different contact systems, different actions','Identify the fitted machine and modes before choosing the rolling plan.')
for i,(title,label) in enumerate([('STEEL DRUM','Static / fitted dynamic mode'),('PNEUMATIC','Tires / load / pressure'),('COMBINATION','Drum + tires')]):
 x=40+i*325;a.rect(x,187,295,310,WHITE,12);a.text(x+18,223,title,21,TEAL,700);a.rect(x+39,287,215,45,GOLD,7)
 if i==0:
  a.circle(x+79,358,42,INK);a.circle(x+213,358,42,INK);a.circle(x+79,358,32,PALE);a.circle(x+213,358,32,PALE)
 elif i==1:
  for xx in [74,119,170,215]:a.rect(x+xx-16,325,32,73,INK,13)
 else:
  a.circle(x+79,358,42,INK);a.circle(x+79,358,32,PALE)
  for xx in [190,233]:a.rect(x+xx-16,325,32,73,INK,13)
 a.text(x+17,459,label,17,MUTED)
a.note('Breakdown, intermediate and finish describe roles; they do not prescribe a universal fleet.');a.save()
a=Art('roller-water-system','Keep the contact surface working consistently','Conceptual spray and scraper arrangement · service only in the required safe state.')
a.circle(405,348,130,INK);a.circle(405,348,112,PALE);a.circle(405,348,30,MUTED);a.path('M245 195H565',TEAL,13)
for x in range(280,540,50):a.path(f'M{x} 205l-11 39M{x} 205l11 39',TEAL,2)
a.path('M535 380L600 427',RED,12);a.card(640,190,315,'SPRAY SYSTEM',['Tank / filter / lines','Nozzles and coverage'],TEAL,135);a.card(640,350,315,'SCRAPER',['Condition + adjustment','Clean contact surface'],RED,135);a.lines(60,253,['Drum'],23,INK);a.note('A dry stripe or pickup needs investigation. Winterize every affected component as instructed.');a.save()
a=Art('rolling-coverage','Count coverage across the whole width','Conceptual record map · this is not a prescribed field rolling pattern.')
for i,(c,t) in enumerate([(TEAL,'Strip A · checked'),(GOLD,'Strip B · checked'),(RED,'Strip C · needs review')]):
 y=195+i*92;a.rect(65,y,635,70,c,5);a.path(f'M100 {y+35}H660',WHITE,3);a.text(728,y+41,t,18,INK,700)
a.path('M65 488H700',INK,2);a.text(224,514,'Full mat width must be accounted for.',23,TEAL,700);a.note('A high movement count can still leave a strip untreated. Keep location and pattern records.');a.save()
a=Art('compaction-curve','Use measured feedback to evaluate the pattern','Illustrative trend only · no pass count or acceptance value is prescribed.')
a.path('M90 455H920M90 455V190',INK,3)
for y in [255,320,385]:a.path(f'M90 {y}H920',PALE,1)
a.path('M120 425C210 350 300 283 420 249S650 230 880 231',TEAL,5)
for x,y in [(120,425),(260,309),(420,249),(600,233),(800,231)]:a.circle(x,y,7,RED)
a.text(110,181,'Measured density',20,TEAL,700);a.text(415,496,'Recorded rolling effort →',23,INK,700);a.lines(600,355,['A plateau needs interpretation.','More passes are not always better.'],21,RED);a.note('Read results with temperature, mixture, support, method and the required reference density.');a.save('ACCESS IS4S. (2026). Use measured feedback to evaluate the pattern [Original conceptual SVG]. Informed by Asphalt Institute (2007), The asphalt handbook, 7th ed., Chapter 9, including Fig. 9.9 (p. 435; PDF p. 469). New schematic trend; numerical axes and acceptance line omitted; no operating pattern prescribed.')
a=Art('transport-plan','Loading needs a shared plan','Conceptual carrier arrangement · no loading direction or restraint design is prescribed.')
a.rect(60,397,670,35,INK);a.path('M730 397L939 476L939 494L730 432Z',INK,3,fill=PALE)
for x in [130,192,580,640]:a.circle(x,453,30,INK);a.circle(x,453,14,PALE)
a.machine(260,245,'paver',1);a.path('M300 370L245 395M490 373L550 395',RED,7);a.text(60,205,'RATED CARRIER + RAMPS',23,TEAL,700);a.lines(680,245,['Verify configuration.','Assign operator + guide.','Use designated points.','Check route + securement.'],20,INK,36);a.note('Stop if alignment or communication is lost. The actual OMM controls the loading sequence.');a.save()
(R/'original-figures.json').write_text(json.dumps({'figures':registry},indent=2,ensure_ascii=False)+'\n');print('Built',len(registry),'original diagrams')
