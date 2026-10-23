# ACCESS | Asphalt curriculum

**First unit · Teaching draft · 23 October 2026**

Start with the paving industry. Read a useful document, explain an equipment role, check a number and work through a change with a partner.

This curriculum follows the supplied **SkilledTradesBC Asphalt Paving/Laydown Technician outline**. The **SkillPlan Skills for Success Get Started Guide, revised March 2024**, provides the teaching and assessment framework. The visual and writing direction comes from the existing ACCESS Numeracy Hub.

## Start with A1

**A1: Introduction to the paving industry and paving equipment** is the first competency in Line A, **Road Building Principles and Introduction to Paving**. The outline's A1 objective also includes road-construction history and the relationship between governing bodies and contractors.

| Material | Open it |
|---|---|
| Learner workbook: readings, cards, practice data and activities | [HTML version](unit-01/index.html) · [Print PDF](unit-01/learner-workbook.pdf) · [Edit Markdown](unit-01/learner.md) |
| Instructor guide: session plans, answer guidance and observation prompts | [HTML version](unit-01/instructor.html) · [Print PDF](unit-01/instructor-guide.pdf) · [Edit Markdown](unit-01/instructor.md) |
| A1–A6 sequence and scope | [Curriculum map](curriculum-map.md) |
| Nine skills, source components and evidence | [Skills map](skills-map.md) |
| Original source PDFs and precise page references | [Source library](sources/README.md) |
| Reusable practice files | [Learning materials](unit-01/materials/README.md) |

## Three opening sessions

| Session | Learner work | Focus Skills for Success |
|---|---|---|
| 1 · Understand the industry | Read the short introduction, sort equipment/functions, sequence the material flow and explain who uses roads. | Reading, Communication, Collaboration |
| 2 · Read and share the numbers | Interpret clearly labelled fictional industry data, check calculations, create a digital record and write a short summary. | Numeracy, Digital, Writing |
| 3 · Respond to a changed brief | Check an environmental claim, identify missing evidence and improve an information sheet when the audience requirements change. | Problem solving, Adaptability, Creativity and innovation |

The proposed design uses **three 60-minute sessions of expanded IS4S preparation**. It is not an official A1 training allocation. The supplied outline allocates 3% of technical-training time to all of A1–A6; the supplied profile specifies 120 technical-training hours. See the [source timing note](sources/README.md#scheduling-distinction).

## What is ready, and what remains

The opening unit contains the reading passages, equipment/function cards, fictional project brief, practice numbers, learner questions and instructor guidance needed for a classroom pilot. These are original teaching materials, with source references.

All nine A1 learning tasks are mapped. Some are introduced rather than completed: real B.C. industry statistics, current applicable regulations/funding and a sourced environmental comparison still need a current source or instructor supplement. Fictional practice data supports learning a method; it does not establish actual industry facts. Completing this workbook does not itself demonstrate all A1 outcomes or establish a trade credential.

All nine Skills for Success have explicit activity and observation evidence across the sequence. Each session concentrates feedback on three skills. If an alternate response mode changes the skill being observed, record that distinction; for example, a paper table does not by itself demonstrate Digital.

## Continue through Line A

After the A1 pilot and source supplements, develop **A2: Describe history of asphalt pavement**. The [curriculum map](curriculum-map.md) preserves A2–A6 in outline order and identifies suitable Skills for Success applications. The A2–A6 lessons are not yet written. Safety orientation and equipment-specific instruction remain distinct parts of the trade sequence.

## Edit and rebuild

Edit `unit-01/learner.md`, `unit-01/instructor.md`, the Markdown files in `unit-01/materials/`, `curriculum-map.md` or `skills-map.md`. Rebuild the reading pages and PDFs with:

```sh
python -m pip install -r tools/requirements.txt
python tools/build_materials.py
python tools/verify_materials.py
```

Run those commands from this folder. The builder can also run from another directory using its full path. It uses an installed `chromium` executable, `IS4S_CHROMIUM_PATH`, or Playwright's installed Chromium. If needed, install the latter with `python -m playwright install chromium`. Use `--html-only` to build reading pages without a browser. The build script starts and stops its own local rendering server; public document links in the PDFs point to this GitHub repository.

The reading pages, fonts and badge work from a downloaded folder without a network connection. Source hyperlinks require the included PDFs or an internet connection for GitHub references. The [design asset notes](assets/README.md) record the Numeracy Hub source and font licences.

[Validation notes](VALIDATION.md) record the checks completed for this draft and the remaining instructor review.
