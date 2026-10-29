# Edition 3 · Implementation record

**29 October 2026.** This editorial record tracks the work following the 28 October review. It is outside the learner and practitioner books.

The books now teach directly as standalone ACCESS IS4S materials. Source-comparison passages, original-guide page references and adaptation commentary have been removed from their instructional text. Research provenance remains in the repository's editorial records. Complete fresh exercises, entry teaching and answer guidance are integrated into the relevant chapters rather than presented as a lesser or supplementary version.

## Changes against the review

| ID | Implemented work | Remaining evidence or decision |
|---|---|---|
| G01 | Repaired the eight crosswalk headings and the 27-row strategy table; added generated-structure checks. The crosswalk is editorial material outside the books. | Final generated-output checks are recorded in VALIDATION. |
| G02 | Removed equivalence claims from book-facing prose; made editorial treatment labels precise; added a complete facilitator-adaptation case and answer guidance. | The editorial inventory explicitly identifies partial treatment where appropriate. |
| G03 | Added fresh cases across all nine skills, separate keys, criterion anchors, sample judgments and observation records. | Actual practitioner moderation of learner evidence remains field work. |
| G04 | Added an enacted problem-solving cycle with a prediction, actual trial, observed result and next decision; connected appropriate prototype work across skills. | Individual performance is recorded when the activity is delivered. |
| G05 | Added step-by-step entry teaching for Reading, Writing, Numeracy, Digital and Problem solving, plus routes for all nine skills. | Learner feedback and actual pacing remain to be observed. |
| G06 | Supplied and functionally checked the Digital practice desk, local version workflow, download and reset, setup instructions and observation record. | Real online permission-setting requires an approved platform and actual access verification. |
| G07 | Supplied complete teaching schedules, sequential observer assignments, individual turns, recovery slots and planned-versus-actual records. | A classroom pilot has not been conducted by this development work. |
| G08 | Supplied local review, support, contribution-permission, response and change-record templates. | Actual ACCESS/local partner participation, approved contacts and scoped decisions must be completed by the delivery team. |
| G09 | Improved handwriting space, simple-table reflow, figure labels, visible descriptions and a keyboard-operable visual viewer. | Human assistive-technology and physical-print evaluation remain distinct from automated/browser checks. |
| G10 | Added source-backed A1 industry, project/regulatory and bounded environmental-comparison teaching, with full cases and keys. | Trade review of delivery use remains required; the dated ledger identifies the scope of each public fact. |
| G11 | Authored the A2–A6 Roadbuilding foundations units, full task inputs and keys, technical diagrams, a 68-competency status map and practical-training handoff. | Later technical competencies and practical delivery are identified separately in that map. |
| G12 | Updated the dated program-information record and distinguished historical technical hours, the current provider-page statement and local delivery decisions. | Current regulator/provider reconciliation and an ACCESS-specific timetable are not claimed complete. |
| G13 | Updated CL-14 and its key to accept an evidenced successful reader check without manufacturing a revision. | Check the task in actual delivery. |
| G14 | Added final-PDF page numbers to printed contents and checks against named destinations; improved short-document pagination and deep links. | Recheck destinations after future content or font changes. |

## Visual direction

The existing teaching diagrams and cover have been redesigned with a consistent cream, ink, red and gold palette, stronger type hierarchy, custom vector illustrations, larger labels and precise callouts. New diagrams explain fraction regrouping, choosing a learning route, testing an idea, checking quantities, road structure and material flow. The artwork preserves the teaching facts and calculations.

The canonical visual manifest controls figure placements. Its alternative text and the SVG descriptions must agree with the current drawing. Both book PDFs, the visual preview and the Roadbuilding files are rebuilt from the final artwork.

## Reproducible authoring

- `tools/install_teaching.py` integrates the complete authoring inputs listed in `teaching-manifest.json` into editable chapter blocks, rebasing links.
- `tools/install_visuals.py` applies the canonical figure placements after teaching integration.
- `tools/build_books.py` generates reading pages and both books, converges printed contents to actual destinations, and builds the visual preview.
- `tools/verify_books.py` checks structure, links, figures, activities, standalone prose, fresh-practice presence and PDF navigation.
- The Digital practice desk uses local browser state and downloads only. Its simulated recipient settings are explicitly distinct from online access-control performance.

See [VALIDATION.md](VALIDATION.md) for completed checks and final artifact measurements. The [28 October review](research/book-gap-analysis-2026-10-28.md) remains a historical assessment of revision `928cda6`; its original evidence and action register preserve that snapshot.

## Asphalt resource integration

The asphalt pathway now includes a complete 2006 specifications workshop, manufacturer manuals with an offline ZIP and nine-skill reading lesson, and indexed PDF/text chunks for all available asphalt PDFs. These resources retain source editions and equipment scopes. MS-4 Seventh Edition is the selected primary asphalt textbook; its original upload remains pending transfer because it exceeds the workspace transfer tool's limit. The textbook planning map records verified publisher information without inventing chapter or page alignment.
