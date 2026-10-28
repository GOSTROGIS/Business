# Book review and gap analysis · 28 October 2026

[Books and downloads](../README.md) · [Action register](book-gap-analysis-2026-10-28-actions.csv) · [Review evidence](book-gap-analysis-2026-10-28-evidence.json)

## Overall assessment

The books provide a substantial foundation for teaching the nine Skills for Success. The next improvement should make that foundation easier to teach, assess and apply to asphalt work. Adding more pages or more decorative images would have less value than supplying usable assessment cases, instructional supports, classroom materials and trade documents.

The strongest features are the explicit skill routines, worked examples, complete fictional case inputs, answer guidance, SVG explanations and careful distinction between an individual's evidence and a group product. The books respect learner choice, avoid compulsory cultural disclosure and distinguish accessibility tools from someone else doing the task. Those features should remain.

The largest gaps are operational. Instructors still need to create some entry-level teaching sequences, unfamiliar assessment cases, observation tools and Digital practice environments. Local co-design and classroom evaluation are described, but the edition contains no completed records of that work. The foundation books also do not complete the separate asphalt curriculum: A1 has acknowledged unfinished source supplements, and A2 onward needs development.

Specific editorial defects need correction: eight crosswalk headings render inside tables, a 27-row strategy table renders as raw Markdown, and CL-14 requires a revision even when a reader test may confirm that the product works. The claim that a source mapping demonstrates “content equivalence” also needs narrowing: an inventory establishes coverage locations, not equivalent depth, performance opportunities or effectiveness.

## Scope and evidence

This review applies to [revision 928cda6](https://github.com/GOSTROGIS/Business/commit/928cda6f6e7434a10a25d5bb204725282be9495f): the **129-page learner textbook**, **185-page practitioner guide**, their editable chapters and answer keys, the supplied **148-page SkillPlan guide**, and the existing asphalt curriculum/source maps. PDF references below use viewer page numbers in that revision. Later pagination may differ.

The review combined separate passes for pedagogy and assessment, Indigenous context and facilitation, source fidelity, asphalt alignment, and visual/accessibility design. It included source-to-chapter comparisons, visual inspection of 51 sampled PDF pages with selected details enlarged, and targeted Chromium checks at 320, 390 and 1280 pixels. The existing structural verifier passed on 28 October 2026: all 174 learner activities have corresponding answers and appear in both PDFs; 54 components, 69 body figure placements and 38 SVG assets remain accounted for. That check did **not** detect the malformed crosswalk headings or strategy table.

This is a document and implementation review. It is not learner testing, an Indigenous community review, an occupational competency assessment or a completed assistive-technology evaluation. Recommendations below distinguish observable defects, development opportunities and validation still to be carried out. The findings do not imply that the books have no assessment, no progression or no Indigenous direction; those foundations already exist.

## Priorities

**P1** means address before wider delivery, before relying on the affected evidence, or before publishing the associated program claim. **P2** means a substantive next-edition improvement. These are development priorities, not official assessment levels. All findings are open at the reviewed revision; this review does not mark proposed changes as implemented.

| ID | Priority | Improvement | Type |
|---|---|---|---|
| G01 | P1 | Repair crosswalk headings and check their rendered structure | Publishing defect |
| G02 | P1 | Qualify equivalence claims and close the leadership-adaptation coverage gap | Claim precision / content depth |
| G03 | P1 | Package unfamiliar checks, criterion anchors and observation records | Assessment delivery |
| G04 | P2 | Connect problem-solving plans to an observed trial and result | Learning opportunity |
| G05 | P2 | Supply short entry bridges and explicit learning routes | Differentiation |
| G06 | P1 | Supply a runnable Digital practice environment | Practical evidence |
| G07 | P1 | Pilot a realistic teaching and observation schedule | Delivery validation |
| G08 | P1 | Turn local Indigenous participation principles into an actual review process | Context validation |
| G09 | P2 | Improve response space, narrow-screen tables and accessible format testing | Learner usability |
| G10 | P1 | Complete A1's outstanding source-backed trade content | Asphalt development |
| G11 | P2 | Develop A2–A6 and a staged path through the remaining trade outline | Asphalt development |
| G12 | P1 | Reconcile current provider information with historical program hours | Program information |
| G13 | P2 | Permit an evidenced “no change needed” outcome in CL-14 | Instruction defect |
| G14 | P2 | Add printed contents destinations and keep short task documents together | Print navigation |

## Findings and acceptance checks

### G01 · Repair the source crosswalk's rendered headings

**Evidence.** In [source-coverage.md](source-coverage.md), no blank line separates the Reading-through-Adaptability component tables from the following `###` skill headings. The generated [crosswalk](source-coverage.html) contains eight table cells such as `<td>### Writing</td>`. The same literal markers appear in [practitioner PDF pp.156–159](../practitioner-guide.pdf#page=156). Reading remains a heading; Writing through Creativity and Innovation do not render as intended. In addition, the four-column strategy table has only three delimiter cells. Its header and all 27 rows appear as a raw pipe-delimited paragraph in HTML and [practitioner pp.159–160](../practitioner-guide.pdf#page=159).

**Impact and improvement.** This weakens scanning and heading navigation in the very section intended to make coverage auditable. Add the missing block separation and fourth delimiter cell, rebuild the crosswalk page and practitioner PDF, and check the output rather than only the Markdown heading inventory.

**Done when:** all nine skill names are actual headings in the generated crosswalk; no table cell starts with `###`; the strategy table has four columns and 27 body rows; PDF text and bookmarks are inspected after rebuilding. Add a focused generated-structure check so this failure cannot pass unnoticed again.

### G02 · Separate source coverage from equivalent instructional depth

**Evidence.** The [books README](../README.md) says “Content equivalence is demonstrated through this mapping.” The [crosswalk](source-coverage.md) accurately accounts for page ranges, but some material is historical, indexed, summarized or replaced. A concrete partial match is the source guide's leadership-adaptation teaching on pp.102 and 105: the target [Adaptability teaching chapter](../practitioner/10-adaptability.md) discusses varying situations, while the learner's main case is personal folder planning. General flexible-teaching guidance is useful, but it is not the same supplied activity in which a leader adapts training to workers' changing needs.

**Impact and improvement.** Describe the books as a comprehensive adaptation with an explicit coverage crosswalk. Mark each source item as retained, adapted, partially addressed, indexed or intentionally deferred, with a reason. Add a practitioner case where a facilitator revises a training plan after access needs, tool availability or participants' experience change. Preserve the source's purpose without inventing cultural needs or diagnosing learners.

**Done when:** coverage claims match the treatment labels; the leadership case includes an initial plan, changed information, a justified revision and evidence criteria. Prioritize unresolved federal proficiency-development and primary BC resource leads already recorded in [online research](online-research.md); record what was actually read before changing claims. This does not require turning the books into an official proficiency test.

### G03 · Make assessment materials ready to use

**Evidence.** [Teaching approaches](../practitioner/02-teaching-approaches.md) already explains criteria, supports, moderation and transfer, and supplies a changed-date Reading check. The [portfolio](../learner/11-reference-and-portfolio.md) has evidence and transfer templates. Skill answer keys contain useful criteria. However, comparable unfamiliar checks and compact criterion-by-criterion recording tools are not consistently supplied across the nine skills. [Communication teaching](../practitioner/08-communication.md) appropriately warns against treating a familiar script as independent evidence; creating a fresh equivalent message remains an instructor task.

**Impact and improvement.** Assemble a separate assessment packet: new case inputs, conditions, observable criteria, acceptable variations, common errors, recording sheets and a later retry for each skill. Keep the existing worked visual checks as teaching aids. Their answers are appropriate for practice; an unfamiliar check should use different inputs and keep its key separate.

For example, CM-04's “at least four relevant details” should identify essential information such as room and time, so four correct minor details cannot compensate for a wrong destination. CL-12 needs separate observations of inviting and using a contribution. CI-15 should distinguish support given to the learner-designer from prompts given to the test user. The existing keys provide the starting point.

**Done when:** another instructor can deliver one unfamiliar check per skill without inventing documents; two instructors compare sample judgments, document disagreements and refine the anchors. Record actual moderation when it occurs. Retain the four local feedback statuses and the distinction between agreed access tools and task-solving prompts.

### G04 · Add an observed problem-solving trial

**Evidence.** [PS-13–15](../learner/05-problem-solving.md) develops an action plan and permissions; PS-16–17 interprets supplied results (learner pp.65–67). The practitioner integrated lesson also clearly labels its trial data as simulated. These are valid decision-making and evaluation tasks. [CI-10–15](../learner/09-creativity-innovation.md) already provides a useful prototype-and-test route.

**Impact and improvement.** Extend or cross-map that existing practical work so a learner implements one low-risk classroom improvement, collects an observation, compares it with an agreed criterion and decides what to change. This strengthens evidence of acting and evaluating without duplicating an entire chapter.

**Done when:** the record distinguishes a proposed action, an action actually taken, learner-collected observations and supplied example data; both PS and Creativity claims identify the relevant individual actions. A plan alone remains labelled as planning evidence.

### G05 · Supply entry bridges and purposeful routes through the chapters

**Evidence.** Reading teaching recognizes alphabetics and fluency needs (practitioner p.28); Writing identifies sentence-level teaching (p.32); Numeracy's integrated M-03/M-04 fraction tasks include unlike-denominator operations (p.80). The chapters and [teaching approaches](../practitioner/02-teaching-approaches.md) offer support and complexity guidance. They do not consistently supply the short instructional sequences needed when a learner is not yet ready for the main task.

**Impact and improvement.** Build short, adult-relevant bridges: vocabulary and phrase reading; sentence boundaries and sequencing; fraction meaning, equivalent fractions and unit conversion; file and device controls. Add a route card for each skill: a brief starting task, the relevant bridge or core case, a retry and an extension. Avoid assuming a reading level or requiring everyone to complete all 18 activities in order.

**Done when:** every route identifies what starting evidence selects it, the materials and demonstration it needs, and a task showing when the learner can return to the main case. Pilot the language and pacing with learners; a readability score alone cannot establish suitability.

### G06 · Provide the Digital environment the tasks require

**Evidence.** [DG-10–14 and “Use online tools with a clear boundary”](../learner/04-digital.md) correctly distinguish discussion or a paper mock-up from observed digital action. DG-14's platform demonstration is conditional. The books do not supply a runnable dummy form/permission workflow and corresponding setup sheet. Core spreadsheet creation is already possible from the complete supplied Case A data; it should not be described as missing. This P1 dependency applies before claiming the affected practical evidence, not before teaching every Digital activity.

**Impact and improvement.** Provide a local practice form, safe fictional files, clear reset instructions and a practitioner setup/check sheet. Give each learner a turn controlling the interface. A local mock-up demonstrates simulated actions; it does not demonstrate real online permission-setting. Use a separate approved platform when that performance is intended. Keep offline content practice available, while recording which online or permission actions remain unobserved.

**Done when:** a practitioner can prepare and reset the exercise on the intended devices; learners demonstrate the specified actions using fictional information; the observation record distinguishes simulation, actual online performance, explanations and blocked opportunities. An actual permission-setting claim requires the learner to change the intended recipient/access setting on the approved platform and check the resulting access; otherwise that performance remains Not observed. Include keyboard and assistive-tool use in the device check.

### G07 · Pilot the teaching schedule and observation workload

**Evidence.** The practitioner book supplies a 45-minute sequence and three complete 90-minute lessons. [Practitioner development](../practitioner/13-practitioner-development.md), pp.94–97, explains coaching, moderation and pilot evaluation. Full skill chapters and the integrated projects still require a cohort delivery plan. Individual digital turns, partner exchanges and CP-03/CP-09 group work need observation time as well as activity time.

**Impact and improvement.** Prepare a session sequence, materials checklist, observer rotation and simple planned-versus-actual timing record. Trial a manageable portion with the delivery team, learners and agreed local partners. Do not infer delivery feasibility from the arithmetic of a proposed timetable.

Include a locally completed cohort insert for actual support contacts, private concerns, recording choices and learning-record arrangements. Agree language, communication mode and access time in the plan; an approximate one-minute message model should not become a speed requirement for an interpreted or AAC exchange. The delivery lead must supply the real arrangements; the author should not invent ACCESS policies or contacts.

**Done when:** one observer is never assigned simultaneous live observations; each selected learner has sender/receiver/tool turns as applicable; missed turns have a recovery slot. A pilot records who had an opportunity, what remained unobserved, task time, access barriers, useful supports and changes for the next version. Include a later unfamiliar task where transfer is being claimed. Record actual results; do not pre-fill successful outcomes.

### G08 · Make local Indigenous participation concrete

**Evidence.** [Start here](../learner/00-start-here.md), [teaching approaches](../practitioner/02-teaching-approaches.md) and [online research](online-research.md) consistently protect choice, privacy and local authority. The online research note explicitly records that no such consultation or cultural review was completed by that research task. Most practice contexts remain generic fictional learning-room scenarios.

**Impact and improvement.** Agree a local review process with ACCESS and appropriate participating people and partners. Identify which examples feel useful, which should change, and whether any locally contributed case is wanted. Record purpose, attribution, review, compensation arrangements where applicable, sharing boundaries and future reuse. A contributor can choose a limited classroom use. More Indigenous-looking decoration would not resolve this gap.

**Done when:** an actual review and response log identifies the reviewed version, agreed scope, changes and unresolved issues. Any endorsement wording stays within that scope. Learners retain fictional alternatives and can decline personal or cultural disclosure. Authoring templates can begin now; participation and approval cannot be fabricated by the author.

### G09 · Improve writing space and format usability

**Evidence.** The learning-plan table on [learner p.7](../learner-textbook.pdf#page=7) provides a narrow response column and short underscore fragments. The books direct learners to notebooks or digital documents, so this is not a missing-workbook claim; a separate response pack would make print delivery easier. Targeted mobile checks also found that two-column project timetable tables retain a 540-pixel minimum width at a 390-pixel viewport, pushing the time column out of initial view. Scrolling works, including by keyboard, but these simple tables could fit more naturally.

**Impact and improvement.** Supply spacious reusable response pages and editable equivalents. Reflow simple tables while preserving horizontal scrolling for genuinely wide datasets and diagrams. A fit/zoom viewer with a clear return path, specific figure-region names and visible text descriptions would make the existing SVGs easier to use on phones. Check key SVGs at normal print size, in greyscale and with their textual alternatives. Tagged PDFs and existing alt text are useful foundations, but they do not establish a completed screen-reader or PDF accessibility evaluation. Sampled contrast and keyboard diagram scrolling worked; this review did not establish a blanket accessibility failure.

**Done when:** the learning plan can hold meaningful handwritten responses; a short timetable is readable without sideways navigation at the tested phone width; users can still inspect complex diagrams at full size; a documented keyboard, text-alternative and representative assistive-technology check records results and unresolved barriers.

### G10 · Finish A1's source-backed trade content

**Evidence.** The [asphalt curriculum map](../../asphalt-paving/curriculum-map.md) and A1 instructor material explicitly leave three substantive areas incomplete: **A1.6** real BC industry/economic statistics, **A1.8** applicable regulations/funding documents, and **A1.9** an evidenced asphalt/concrete environmental comparison. Fictional tables teach the foundational skills well; they cannot supply those trade facts.

**Impact and improvement.** Create dated, source-backed document sets with defined geography, measures, project conditions and uncertainty. For the environmental comparison, specify the functional comparison, life-cycle boundary and conditions rather than ranking one material universally. Pair each document with a reading task, a numerical interpretation and a short audience-focused explanation.

**Done when:** every factual claim has a traceable source and applicable date/context; a trade reviewer checks interpretation; each A1 task has an honest introduced/practised/completed status. Complete these gaps before describing A1 as finished trade instruction.

### G11 · Extend from foundations into the asphalt sequence

**Evidence.** [A2–A6](../../asphalt-paving/curriculum-map.md) is mapped but not authored. The supplied outline contains 68 competencies across Lines A–L; much of that technical and practical scope remains undeveloped. Current numeracy focuses on classroom supplies, travel and a board layout, with additional measurement and volume teaching in the practitioner guide. These are useful foundations, not yet a full road-profile, quantities, specifications or quality-record pathway.

**Impact and improvement.** Write A2 history and A3 paving technology next, then A4 worker expectations, A5 road/highway profiles and A6 evidence-based trends. Develop a whole-outline status map before moving into later technical lines. Add authentic or clearly labelled training documents and technical diagrams as each unit needs them, with trade review and suitable supervised practice. Do not compress all nine skills artificially into every activity.

**Done when:** each developed competency has outcomes, source documents, teaching tasks, evidence criteria, an answer/observation guide and review status. Practical performance has its own conditions and qualified supervision. The foundation books continue to be companions rather than evidence that the entire trade curriculum is complete.

### G12 · Reconcile program hours before publishing a current schedule

**Evidence.** The supplied 2014 profile uses **120 technical hours**. The supplied outline allocates **3% to all A1–A6**, giving 3.6 historical hours for Line A, not for A1 alone. A live check of the [IUOE training page](https://iuoe115.ca/asphalt-laydown-operator/) on 28 October 2026 returned **four weeks**, dates to be announced and “Total accumulated hours equivalent to 140.” That page also contains credential/pathway wording requiring provider clarification. One guessed SkilledTradesBC URL returned HTTP 403; it was not an officially linked trade-page route. This failed request does not establish general site unavailability or a change to the standard. No current regulator confirmation was obtained.

**Impact and improvement.** Keep the historical outline as the stated curriculum-development basis, and verify the current delivery version directly with the responsible provider/authority before adopting hours, qualification wording or an ACCESS timetable. The provider-page difference is an unresolved discrepancy, not proof that either source should simply overwrite the other.

**Done when:** a dated source/confirmation record distinguishes technical hours, added IS4S preparation, practical/workplace requirements and local delivery decisions. Update program statements only to the extent that confirmation supports them.

### G13 · Allow a successful reader check without an invented revision

**Evidence.** [CL-14](../learner/07-collaboration.md) requires learners to “record the reader's answers and one useful change”; its [answer guidance](../answers/07-collaboration.md) expects a reasoned revision. In contrast, CL-11 explicitly accepts an accurate draft and says not to manufacture a mistake.

**Impact and improvement.** Allow either a justified improvement or an evidenced decision to retain the tested version. This aligns the task with the books' otherwise careful treatment of truthful evidence. Keep required changes when the case's actual requirements change.

**Done when:** the prompt and key agree, and both a useful revision and a successful no-change test have acceptable evidence examples.

### G14 · Make the printed books easier to navigate and compare

**Evidence.** The learner contents on p.2 and practitioner contents on pp.2–3 have electronic links but no printed destination page numbers. Electronic bookmarks already work. Short task documents also split across pages: the six-row Project 2 schedule spans [learner pp.119–120](../learner-textbook.pdf#page=119), its change card spans pp.121–122, and the revised Project 1 answer schedule spans practitioner pp.143–144. Table headers repeat correctly, but readers must turn a page to see a short complete set of conditions.

**Impact and improvement.** Generate page-numbered contents after pagination, consider an activity-to-answer locator, and keep short schedules and change-card blocks together when they fit. Preserve normal pagination for genuinely long tables rather than applying a blanket no-break rule. Rebalance the sparse third contents page without reducing type size.

**Done when:** a reader can find a named skill and its answer guidance from paper alone; contents destinations match the final PDF; the cited short documents appear as complete units; adjacent pages have no clipping or excessive gaps; electronic links and bookmarks still work.

## The next improvement for each skill

| Skill | Keep | Most useful addition |
|---|---|---|
| Reading | Version comparison, source evidence and an explicit strategy | Short vocabulary/fluency bridges and an unfamiliar trade-document check |
| Writing | Audience, drafting, reader testing and revision | Sentence/paragraph entry support plus fresh writing tasks with annotated criterion examples |
| Numeracy | Whole-pack, time, measurement and checking diagrams | Fraction/unit bridges followed by reviewed road-profile and quantity-document transfer |
| Digital | Actual tool control, file versions and explicit evidence limits | Runnable practice forms/permissions, setup instructions and individual-turn records |
| Problem solving | Bounded questions, evidence limits and option comparison | An enacted low-risk trial with learner-collected observations |
| Communication | Check-backs and accessible interaction modes | Fresh message cards and compact listener/speaker observation anchors |
| Collaboration | Shared decisions, visible contributions and handovers | Observer rotation tools and a valid no-change outcome after reader testing |
| Adaptability | Original/revised plans and task-focused feedback | A facilitator/leader case adapting training for changed participant needs |
| Creativity and innovation | Alternative ideas, prototypes and testing | Reuse its practical test evidence across Problem solving; test again with an unfamiliar constraint |

## Where further SVG work would help most

Keep the Numeracy Hub palette and the existing vector approach. Each new graphic should explain a decision, relationship or action the learner needs to use.

| Proposed visual | Teaching purpose | Release check |
|---|---|---|
| Annotated road cross-section with a paired blank diagram | Connect A5 vocabulary, dimensions and units | Trade-reviewed labels, scale/units and a matching text explanation |
| Annotated training load/quantity record and a changed-version partner | Connect Reading, Numeracy, Digital and Writing | Fully supplied fictional or appropriately sourced inputs; no implied operational authority |
| Worked diagram paired with an unfamiliar learner version | Preserve visual teaching while enabling independent evidence | Distinct inputs and a separate answer key |
| Plan → trial → observation → revision evidence diagram | Connect Problem solving with prototype testing | Distinguish proposed actions from actual observations and simulated results |
| Chapter route card and printable observation grid | Help learners and instructors choose the next task | Tested with users; readable without colour alone |

## Recommended sequence

1. **Correct and clarify:** repair the crosswalk, narrow equivalence wording and align CL-14 with truthful evidence. Check the regenerated outputs.
2. **Prepare a usable teaching slice:** begin with Reading, Writing and Numeracy entry bridges, fresh checks, response sheets and criterion anchors. Add the Digital practice environment and observation rotation.
3. **Complete the opening asphalt content:** finish A1.6/A1.8/A1.9 and develop A2/A3 with reviewed documents and purposeful SVGs. Resolve current program information before using a published timetable.
4. **Review locally and pilot:** start relationship and review arrangements early, then test the prepared teaching slice, timing, formats and evidence collection. Revise from recorded feedback.
5. **Expand with evidence:** extend the successful approach across the remaining skills and trade competencies. Maintain a versioned coverage map and publish only the review/validation actually completed.

The [action register](book-gap-analysis-2026-10-28-actions.csv) assigns proposed responsible roles, dependencies and acceptance checks. Roles are recommendations, not appointments or records of consultation. The next edition should be judged by whether learners can use the materials and instructors can teach and interpret evidence consistently, as well as by its coverage and visual quality.
