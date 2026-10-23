# ACCESS IS4S — the complete nine-skills books

[Download the learner textbook](learner-textbook.pdf) · [Download the practitioner guide](practitioner-guide.pdf)

[Preview eight illustrated pages](visual-sampler.pdf) · [Browse the SVG index](VISUALS.md)

[Read the learner book](learner-textbook.html) · [Read the practitioner book](practitioner-guide.html)

Two substantial companion books expand the complete **148-page Skills for Success Get Started Guide for Practitioners**, revised March 2024, into original ACCESS Indigenous Skills 4 Success teaching prose and practice. The nine Skills for Success are taught in BC learning, work and community contexts, with asphalt paving as the starting trade connection. The colour, type and badge follow the [ACCESS Numeracy Hub](https://github.com/GOSTROGIS/access-trades-numeracy).

## Visual teaching edition

The books now lead with **38 SVG assets**, including a visual map and two case diagrams for every skill. Across the books there are **67 SVG placements** and four people-focused illustrations. Annotated notices, proportional time and cost diagrams, dimensioned layouts, file-version views, equipment sketches, feedback loops, prototype comparisons and lesson diagrams make the reasoning visible. A figure from the supplied guide is also reused with attribution. [Preview the redesign](visual-sampler.pdf).

Worked visual checks provide model responses after practice; use the changed cases for independent evidence. On narrow screens, scroll a diagram within its frame or use its full-size link. PDFs retain vector clarity when enlarged.

## What is included

| Book | Contents |
|---|---|
| **Learner textbook** | Nine full skill chapters, all 54 components, worked examples, complete fictional documents and datasets, 162 numbered skill activities, two integrated projects with 12 further activities, a glossary and a learning portfolio. |
| **Practitioner guide** | Framework and transition from Essential Skills; six teaching approaches; nine skill teaching chapters; three complete 90-minute lessons with handouts and answers; assessment and practitioner development; answer guidance for all 174 learner activities; online research, source coverage and the original bibliography index. |

The practitioner guide reworks the full instructional scope of the supplied guide. It preserves the original bibliography as an attributed index rather than implying that every listed publication was independently read. The [coverage crosswalk](research/source-coverage.md) accounts for all 148 source pages, 54 components, 27 instructional strategy groups, 27 grab-and-go patterns, three appendix lessons and professional-development resources. Content equivalence is demonstrated through this mapping, not by padding the new books to an identical page count.

## Start learning

1. Use [Start here](learner/00-start-here.md) to choose a useful goal and agree supports.
2. Start with [Reading](learner/01-reading.md), [Writing](learner/02-writing.md) or [Numeracy](learner/03-numeracy.md), or choose the skill connected to your goal.
3. Follow the explanation and worked example, complete an activity, then review it using the practitioner answer guidance.
4. Bring the skills together in the [two integrated projects](learner/10-integrated-projects.md), and retain evidence in the [portfolio](learner/11-reference-and-portfolio.md).

| Skill | Editable learner chapter | Answer guidance | Practitioner teaching |
|---|---|---|---|
| Reading | [Chapter](learner/01-reading.md) | [Answers](answers/01-reading.md) | [Teaching](practitioner/03-reading.md) |
| Writing | [Chapter](learner/02-writing.md) | [Answers](answers/02-writing.md) | [Teaching](practitioner/04-writing.md) |
| Numeracy | [Chapter](learner/03-numeracy.md) | [Answers](answers/03-numeracy.md) | [Teaching](practitioner/05-numeracy.md) |
| Digital | [Chapter](learner/04-digital.md) | [Answers](answers/04-digital.md) | [Teaching](practitioner/06-digital.md) |
| Problem solving | [Chapter](learner/05-problem-solving.md) | [Answers](answers/05-problem-solving.md) | [Teaching](practitioner/07-problem-solving.md) |
| Communication | [Chapter](learner/06-communication.md) | [Answers](answers/06-communication.md) | [Teaching](practitioner/08-communication.md) |
| Collaboration | [Chapter](learner/07-collaboration.md) | [Answers](answers/07-collaboration.md) | [Teaching](practitioner/09-collaboration.md) |
| Adaptability | [Chapter](learner/08-adaptability.md) | [Answers](answers/08-adaptability.md) | [Teaching](practitioner/10-adaptability.md) |
| Creativity and innovation | [Chapter](learner/09-creativity-innovation.md) | [Answers](answers/09-creativity-innovation.md) | [Teaching](practitioner/11-creativity-innovation.md) |

For a class sequence, use the [six teaching approaches](practitioner/02-teaching-approaches.md) and [complete integrated lesson plans](practitioner/12-integrated-lesson-plans.md). The existing [SkilledTradesBC asphalt A1 materials](../asphalt-paving/README.md) remain the trade-specific starting unit. These books do not claim to replace the full asphalt trade program.

## Sources and BC Indigenous direction

The original [148-page SkillPlan PDF](../asphalt-paving/sources/SFS-Get-Started-Guide_FINAL_MAR2024.pdf), [asphalt program outline](../asphalt-paving/sources/asphalt-paving-laydown-technician-program-outline-august-2016.pdf) and [program profile](../asphalt-paving/sources/asphalt-paving-laydown-technician-program-profile-nov-2014.pdf) are preserved unchanged in the source folder.

[Online research](research/online-research.md) records current federal Skills for Success pages and verified BC education sources, alongside access limits. [Source metadata](research/sources.json), the [complete original-guide inventory](research/sfs-inventory.json) and [bibliography index](research/original-guide-bibliography.md) make the research traceable.

The teaching voice recognizes adults' existing strengths, individual agency, contemporary Indigenous experiences and responsibilities to people and place. Learners can use fictional cases or choose suitable examples from their lives. No one is required to disclose personal history or cultural knowledge. Local Nations and community partners direct Nation-specific content, language, protocols and knowledge. The books do not invent teachings or claim Indigenous community endorsement.

This is an **instructor-review and pilot edition**, not an approved certification instrument. Feedback describes evidence from a task and the support used; it does not assign official proficiency levels. Digital, Writing and interpersonal evidence retain their own task requirements. Current workplace rules and equipment instruction belong in the supervised trade program.

## Rebuild and review

Editable Markdown is the source of truth. The committed HTML pages support reading in a browser when served locally or hosted as static files; GitHub displays their source. The PDFs can be downloaded directly from GitHub.

```sh
python -m pip install -r curriculum/skills-for-success/tools/requirements.txt
python curriculum/skills-for-success/tools/build_books.py
python curriculum/skills-for-success/tools/verify_books.py --require-generated
```

Chromium must be installed. Set `IS4S_CHROMIUM_PATH` to an alternate Chromium executable if needed. Use `--html-only` to build without PDF export. The builder serves repository files briefly on localhost to render them, uses bundled fonts, and converts PDF links to repository URLs. No external service is required. The [book manifest](book-manifest.json) controls the chapter order and the [visual manifest](assets/visuals-manifest.json) controls managed figure blocks; [design provenance and font licences](assets/README.md) accompany the assets.

See [validation results](VALIDATION.md) for the actual build, content review and artifact checks. Pilot feedback should be recorded against an activity ID, the observed issue, the proposed revision and who reviewed it; do not store identifiable learner work in the public repository.
