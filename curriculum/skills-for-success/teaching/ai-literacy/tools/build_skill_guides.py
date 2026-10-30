"""Nine concrete visual walkthroughs, with plain-language actions and no task codes."""
from pathlib import Path
from html import escape as E
import json,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[3];A=R/'assets/diagrams'
# Purpose, visible example, three actions, observable result: every guide supplies a complete mini-case.
DATA=[
('01-reading','Reading','Find the detail that changes your action','NOTICE 1: Room 1 at 10:00','UPDATE: Room 2; time unchanged',['Find the current message.','Compare what changed.','Say the room and the time.'],'Meet in Room 2 at 10:00.','Use both messages. The room changes; the time does not.'),
('02-writing','Writing','Write so the next person can act','NEED: 2 calculators by 09:00','RETURN: 11:45; loan not confirmed',['Name the reader and request.','Include quantity and timing.','Ask for confirmation; revise.'],'Please confirm a loan of two calculators.','Include collection and return times. A request is not a confirmed loan.'),
('03-numeracy','Numeracy','Show the calculation and its meaning','ISSUED: 18 folders','RETURNED: 13 folders',['Name the quantity you need.','Calculate: 18 − 13 = 5.','Check: 13 + 5 = 18.'],'Five folders remain outstanding.','Outstanding does not automatically mean lost or damaged.'),
('04-digital','Digital','Make a file you can find and check','SOURCE: 18 issued; 13 returned','UPDATE: 2 more folders returned',['Save an editable first version.','Change returned from 13 to 15.','Reopen and check the new file.'],'Three folders remain outstanding.','Keep the first version. Use AI to help, then verify the actual file.'),
('05-problem-solving','Problem solving','Investigate before deciding the cause','OBSERVED: Two notices disagree','UNKNOWN: Which notice is current?',['State the problem and unknown.','Check dates and authority.','Confirm the action; test it.'],'Use the confirmed current instruction.','A guess about who made the error is not evidence.'),
('06-communication','Communication','Say it. Check it. Switch roles.','SENDER: “Room 2 at 10:00.”','RECEIVER: “Room 2, ten o’clock?”',['Agree a usable way to talk.','Send the message; check it back.','Confirm or clarify, then switch.'],'Both people can state the same plan.','Speech, sign, text or AAC can work. Check meaning, not eye contact.'),
('07-collaboration','Collaboration','Make each person’s contribution clear','PERSON A: Check the source facts','PERSON B: Build the notice',['Agree the goal and roles.','Share progress and ask for help.','Review together; name next steps.'],'One checked notice; two visible contributions.','A shared file alone does not show what each person did.'),
('08-adaptability','Adaptability','Change the plan without losing the goal','ORIGINAL: 24 participants','UPDATE: 26 participants',['Identify what changed.','Update affected quantities.','Check what stays the same.'],'The notice and budget both say 26.','Keep the old version. Do not change the room or time without evidence.'),
('09-creativity-innovation','Creativity and innovation','Make an idea, try it, improve it','NEED: Find the current card quickly','IDEAS: Divider tabs or a labelled tray',['Suggest two useful options.','Make a small prototype.','Ask a user to try it; improve.'],'A tested improvement, with a reason.','Choose a visible measure: correct selection, clear labels or fewer steps.')]
for stem,skill,title,a,b,steps,result,note in DATA:
 id='quick-'+stem[3:];parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 680" role="img" aria-labelledby="title desc"><title id="title">{E(title)}</title><desc id="desc">{E(a+". "+b+". "+" ".join(steps)+" Result: "+result+" "+note)}</desc><defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="none" stroke="#276b66" stroke-width="1.4"/></marker></defs><rect width="1100" height="680" fill="#f7f2e8"/><rect width="1100" height="128" fill="#242827"/><g font-family="Arial,sans-serif"><text x="38" y="40" fill="#d5ad62" font-size="18" font-weight="700">ACCESS IS4S / {E(skill.upper())} / SEE IT IN ACTION</text><text x="38" y="94" fill="white" font-size="35" font-weight="700">{E(title)}</text>']
 def text(x,y,t,size=21,c='#242827',w=400):parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" font-weight="{w}">{E(t)}</text>')
 def rect(x,y,w,h,c,r=12):parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}"/>')
 rect(38,159,1024,143,'white');rect(38,159,9,143,'#a93332',0)
 if skill=='Communication':
  parts.append('<circle cx="85" cy="197" r="17" fill="#d5ad62"/><path d="M62 256v-20q23-30 46 0v20" fill="#276b66"/><circle cx="600" cy="197" r="17" fill="#d5ad62"/><path d="M577 256v-20q23-30 46 0v20" fill="#a93332"/>');text(130,220,a,23);text(645,220,b,22);parts.append('<path d="M145 264H940" stroke="#276b66" stroke-width="3" marker-end="url(#arr)"/>')
 else:text(68,208,a,24,w=700);text(68,263,b,24,c='#276b66')
 for i,step in enumerate(steps):
  x=38+i*347;rect(x,336,330,126,'white');parts.append(f'<circle cx="{x+30}" cy="366" r="16" fill="#a93332"/>');text(x+24,372,str(i+1),18,'white',700)
  import textwrap
  for j,line in enumerate(textwrap.wrap(step,28)):text(x+18,409+j*27,line,21)
 rect(38,500,1024,104,'#242827');text(61,536,'WHAT A GOOD RESULT LOOKS LIKE',16,'#d5ad62',700);text(61,579,result,28,'white',700);text(38,647,note,19,'#535c58');parts.append('</g></svg>');(A/(id+'.svg')).write_text(''.join(parts)+'\n')
 # Source insertions are canonical prose, independent of managed visual blocks.
 for folder,num in [('learner',stem[:2]),('practitioner',f'{int(stem[:2])+2:02d}')]:
  target=R/folder/(stem+'.md' if folder=='learner' else num+'-'+stem[3:]+'.md')
  if not target.exists():raise ValueError(target)
  text_=target.read_text();heading='See it in action · '+skill
  if heading not in text_:
   intro=f'## {heading}\n\nThis small fictional example shows the skill in use. '+a+'. '+b+'.\n\n**Try it:** '+' '.join(steps)+'\n\n**Check your result:** '+result+' '+note+'\n\n'
   pos=text_.find('\n## ');text_=text_[:pos]+'\n\n'+intro+text_[pos:];target.write_text(text_)
  p=R/'assets/visuals-manifest.json';d=json.loads(p.read_text());uid=id+'--'+folder
  d['figures']=[x for x in d['figures'] if x['id']!=uid];d['figures'].append({'id':uid,'file':'assets/diagrams/'+id+'.svg','source':str(target.relative_to(R)),'after_heading':heading,'caption':result+' ACCESS IS4S. (2026). Original fictional teaching diagram.','alt':a+'. '+b+'. '+' '.join(steps)+' '+result+' '+note,'kind':'diagram','placement':'after_heading'});p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
# Remove opaque project codes from the one legacy diagram that displays them.
p=A/'social-project-1-versions.svg';s=p.read_text().replace('FIRST WORK · CP-01–CP-04','FIRST WORK · PLAN + CHECK').replace('REVISED WORK · CP-05–CP-06','REVISED WORK · UPDATE + CHECK').replace('CP01-budget-v1','event-budget-v1').replace('CP01-budget-v2','event-budget-v2').replace('CP01–CP04 produce','The first planning tasks produce').replace('CP05–CP06','revision and verification');p.write_text(s)
print('Built nine concrete guides and integrated 18 placements.')
