# ACCESS IS4S · Asphalt paving

Read the work, understand the equipment and use the nine Skills for Success to make and explain a sound decision.

**Classroom teaching edition · 29 October 2026**

[Integrated teaching route](teaching-route.html) · [Curriculum review and gaps](review-and-integration.html)

The teaching route connects the occupational sequence to the nine-skills books, manual-picture exercises and specification reading. Teach the exact trade term, locate it in a labelled figure or document, work an example, then keep each learner's explanation and checked work. Figures carry source credits and links to the original pages.

## Primary textbook · MS-4, Seventh Edition

The ACCESS asphalt curriculum uses **The Asphalt Handbook, MS-4, Seventh Edition** as its primary textbook. Section 4 of the trade outline lists this edition among the required resources. The trade outline defines the occupational sequence; the nine Skills for Success guide how learners read, calculate, explain, practise and demonstrate their learning.

[Textbook integration plan](ms-4/README.md) · [Chapter and competency map](ms-4/chapter-map.md) · [Indexed PDF context library](context/README.md)

The handbook's full text and HTML conversion are **pending access**. The original upload exceeds the workspace's 32 MiB transfer limit; the subsequently supplied Google Drive link currently requires sign-in. Existing lessons and figures are attributed to the documents actually read. MS-4 chapter alignment and redrawn handbook figures will be verified after the full file becomes accessible. The historical 2006 specifications support contract-document practice; OEM manuals supply model-specific equipment context.

## Roadbuilding foundations

The six units follow A1–A6 in the SkilledTradesBC Asphalt Paving/Laydown Technician outline. They provide complete readings, worked examples, 37 activities and separate teaching and answer guidance. Current industry evidence, road documents, worker expectations and material-flow diagrams connect the classroom work to British Columbia paving contexts.

| Material | Open it |
|---|---|
| Roadbuilding foundations · learner book | [PDF](line-a/roadbuilding-foundations.pdf) · [Read online](line-a/roadbuilding-foundations.html) |
| Roadbuilding foundations · teaching and answer guide | [PDF](line-a/teaching-guide.pdf) · [Read online](line-a/teaching-guide.html) |
| Six-unit navigation and editable chapters | [Start here](line-a/README.md) |
| Occupational scope and development status | [68-competency map](line-a/competency-status.md) |
| Dated evidence and technical review record | [Research register](line-a/research/source-ledger.md) · [Delivery and review](line-a/technical-handoff.md) |

Use the [complete nine-skills books](../skills-for-success/README.md) for explicit instruction, entry routes, fresh practice, assessment records and the Digital practice desk. Their chapters teach Reading, Writing, Numeracy, Digital, Problem solving, Communication, Collaboration, Adaptability, and Creativity and innovation.

## Specifications and equipment manuals

- [Specifications workshop](specifications/README.md): work with the 2006 Design Build Standard Specifications through asphalt document-reading and decision exercises.
- [2006 Design Build Standard Specifications PDF](sources/design_build_standard_specs_2006.pdf): the complete supplied document, preserved as issued. Its edition is part of every classroom record; current project requirements must be checked separately.
- [Manufacturer manuals and Section 4 resource pack](manuals/README.md): downloaded manuals, exact model and edition details, extracted learning material and the ZIP download. Required course publications and OEM manuals are identified separately.
- [Source library](sources/README.md): the program outline, profile and other source documents with integrity records.

## Opening sessions and reusable handouts

The original three-session A1 sequence remains available for an initial classroom introduction. The Roadbuilding foundations book develops the subsequent industry evidence and A2–A6 work.

| Material | Open it |
|---|---|
| Opening learner workbook | [PDF](unit-01/learner-workbook.pdf) · [Read online](unit-01/index.html) |
| Opening instructor guide | [PDF](unit-01/instructor-guide.pdf) · [Read online](unit-01/instructor.html) |
| Response sheets, change card and process cards | [Classroom materials](unit-01/materials/README.md) |
| Sequence and nine-skills evidence | [Curriculum map](curriculum-map.md) · [Skills map](skills-map.md) |

## Delivery and development

The materials are ready for qualified technical review and a classroom pilot. The [status map](line-a/competency-status.md) records which occupational competencies have authored classroom activities and which remain to be developed. Equipment operation and practical assessment require the applicable machine, current procedures, qualified instruction and authorized observation.

The historical profile, current provider statements and proposed ACCESS classroom practice times are separate records in the [delivery notes](line-a/technical-handoff.md). No classroom timing in these books is presented as an approved program allocation.

Learners choose whether to contribute personal experience. Local people direct any Nation-specific knowledge, language or protocols they wish to include. The supplied cases allow participation without disclosing personal records or cultural knowledge.

## Edit and rebuild

```sh
python -m pip install -r curriculum/asphalt-paving/tools/requirements.txt
python curriculum/asphalt-paving/tools/build_materials.py
python curriculum/asphalt-paving/tools/verify_materials.py
python curriculum/asphalt-paving/tools/build_line_a.py
python curriculum/asphalt-paving/tools/verify_line_a.py
```

Each resource folder records its own build or packaging steps. Chromium is required for PDF export. The HTML pages use bundled fonts and assets; serve the repository locally to open the reading pages. GitHub displays the PDFs and editable Markdown directly.

[Validation record](VALIDATION.md) · [Design assets](assets/README.md)
