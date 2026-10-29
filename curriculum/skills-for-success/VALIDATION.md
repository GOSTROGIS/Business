# Build and content validation

**Edition 3 · 29 October 2026.** These checks cover authored content, generated artifacts, software behaviour and sampled visual presentation. Qualified teaching review, a classroom pilot and local Indigenous community participation remain delivery work; this record does not claim they have occurred.

## Delivered books

| Artifact | Pages | Contents |
|---|---|---|
| [Learner textbook](learner-textbook.pdf) | 186 | 12 chapters: nine skills, entry teaching, fresh practice, two projects, learning reference and portfolio. |
| [Practitioner guide](practitioner-guide.pdf) | 248 | 14 teaching and delivery chapters, integrated fresh cases and keys, and 10 core answer sections. |
| [Visual preview](visual-sampler.pdf) | 8 | Actual pages selected from the complete books. |

Both PDFs contain selectable text, tagged structure, bookmarks and clickable contents. Printed chapter page numbers were checked against the final PDF destinations; both books stabilized after two export passes. Companion-book links resolve to the intended chapter or heading page. No temporary localhost URLs remain in PDF annotations.

The books teach as standalone ACCESS IS4S documents. Automated checks reject original-guide comparison language in their text. Editorial research and coverage records remain outside both books.

## Content and activity checks

- All nine skills and 54 framework components have mapped learning opportunities. The 174 core learner activities retain matching answer guidance: 18 per skill and 12 integrated-project activities.
- The five foundation skills add 38 individually identified practice checks, complete case inputs, separate answer guidance, entry routes and observation criteria. Reading, Writing, Numeracy, Digital and Problem solving each provide changed tasks for a fresh attempt.
- Communication, Collaboration, Adaptability, and Creativity and innovation add complete new cases, role cards or changed conditions, separate keys, evidence criteria and teaching routes. Individual performance is distinguished from group discussion or a proposed action.
- Independent reviews checked fresh-task arithmetic, case totals, changed requirements and key alignment. Fraction regrouping, whole packs, stock updates, transport connections and trial percentages were checked against the actual inputs.
- CL-14 and its answer accept an evidenced successful reader check without requiring an invented revision. Communication timing permits interpretation, signing, AAC and processing time.
- Delivery tools include sequential observer assignments, fresh-attempt and recovery arrangements, reusable local-review records and task-specific evidence prompts. They contain no prefilled approvals or invented learner results.
- The editorial crosswalk now renders its eight intended headings and a consistent 27-row strategy table. Its structural checks pass; it is excluded from the published books.

## Visuals and print

The core books use **41 unique SVGs**, with **73 SVG placements including the two covers**, plus four contextual illustrations. Two further SVGs support Roadbuilding foundations. The canonical manifest has 77 body placements, including two in separate authoring material; 75 body placements occur in the books (71 SVGs and four illustrations).

All 36 existing teaching SVGs and the cover were redesigned. Four new core figures explain choosing a learning route, fraction equivalence and regrouping, a quantity check, and a prediction/trial cycle. The two roadbuilding figures explain road structure and material flow. SVG titles, descriptions and chapter alternative text were synchronized.

Independent visual review rendered all 41 core SVGs and checked text bounds, labels, arithmetic and connector meaning. Two connector collisions were repaired. Inspection of final PDF pages confirms the corrected evidence cycle, fraction diagram and tall quantity check are captured, readable and contained with their captions. The eight-page preview was rendered and inspected for the cover, reading map, budget, board layout, equipment roles, fractions, cause map and annotated email. The drawings remain vectors in the PDFs.

Actual-book browser checks at **320, 390 and 1280 pixels** found no page-level horizontal overflow, failed images or overflowing two-column tables. Wider tables scroll inside labelled regions. Table regions have unique descriptive labels. Print inspection confirmed usable learning-plan response space and clear cover/contents pages. The visual viewer offers fit/zoom controls, keyboard panning, a text description and a return link; its print layout accommodates tall figures.

These checks are bounded presentation reviews, not a full assistive-technology or PDF accessibility certification.

## Digital practice desk

The [practice desk](teaching/digital-lab/index.html) was exercised in Chromium using fictional records. Checks covered invalid input, calculated totals, removal of the dummy contact column, stale-preview detection, saving two versions, reopening the earlier version, JSON download, persistence after reload, narrow-screen layout and reset. Reset preserved unrelated browser storage. No JavaScript errors or external network requests occurred in the tested workflow.

Recipient and access choices are explicitly simulated. Real account permissions must be observed in an approved platform when that is the learning objective. A supplied total is not evidence that a learner constructed a spreadsheet formula.

## Reproduce the checks

```sh
python -m pip install -r curriculum/skills-for-success/tools/requirements.txt
python curriculum/skills-for-success/tools/build_books.py
python curriculum/skills-for-success/tools/verify_books.py --require-generated --report /tmp/is4s-book-verification.json
```

The final structural run passed **39,046 checks** at this revision of the documentation. Counts may grow when linked editorial records are added. Checks cover source integrity, coverage inventory, activity/answer IDs, book membership, standalone prose, fresh-practice presence, local links and fragments, contents destinations, companion PDF targets, nonempty PDF pages, figures, alternative descriptions and SVG self-containment. External URLs are outside this offline verifier.

Running the teaching and visual installers twice produced identical Markdown hashes across all 69 authoring and editorial files. Build tools preserve unmarked prose and replace only their declared managed blocks. Python bytecode is excluded from version control; PDF and ZIP artifacts are tracked as binary files.

For asphalt-specific validation and remaining technical review, see the [asphalt record](../asphalt-paving/VALIDATION.md) and [Roadbuilding delivery record](../asphalt-paving/line-a/technical-handoff.md).
