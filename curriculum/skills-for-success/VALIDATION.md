# Build and content validation

**Edition 4 · 30 October 2026.** These checks cover authored content, generated artifacts, software behaviour and sampled visual presentation. Qualified teaching review, a classroom pilot and local Indigenous community participation remain delivery work; this record does not claim they have occurred.

## Delivered books

| Artifact | Pages | Contents |
|---|---|---|
| [Learner textbook](learner-textbook.pdf) | 216 | 12 chapters: nine skills, entry teaching, fresh practice, two projects, learning reference and portfolio. |
| [Practitioner guide](practitioner-guide.pdf) | 287 | 14 teaching and delivery chapters, integrated fresh cases and keys, and 10 core answer sections. |
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

The current books contain **105 image placements**: 101 SVG placements and four contextual illustrations. Thirteen new SVGs add one concrete walkthrough for every skill and four AI/file/audit explanations. The canonical visual manifest contains 107 placements, including separate authoring material. Component tables render as readable practice cards, and dense activity-code lists have been replaced with short teaching sequences and numbered routes.

Reading editions display descriptive task names; authoring identifiers remain only in internal tracking and HTML metadata. All sixteen AI activities appear in both books, with independent case inputs and full teaching/answer guidance. The practitioner book has no repository or asphalt-course dependency. PDF checks confirm the media activities are included.

New browser checks cover Communication, Digital, instructor Digital and the media player at 390 and 1280 pixels. They found no page-level overflow or failed loaded images. All thirteen new SVGs fit their view boxes. Actual PDF pages were visually inspected for the communication exchange, instructor component guide and audio activity. The updated eight-page sampler includes the communication exchange, file-format guide and AI audit alongside selected core visuals.

The supplied practice pack contains real DOCX, XLSX formulas, CSV, HTML and PDF files, plus a 58.54-second narrated study video, MP3/WAV audio, seven SVG scenes, SRT/VTT captions, transcript, storyboard and flashcard CSV. The narration uses the local Flite synthetic voice; the example does not claim generation by a named commercial AI platform. Thirty-nine additional checks passed for file opening, calculations, ZIP integrity, audio/video streams, caption timing, browser media metadata and task visibility.

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

The current structural run passed with zero errors; the detailed check totals are recorded in the generated verification output. Counts may grow when linked editorial records are added. Checks cover source integrity, coverage inventory, activity/answer IDs, book membership, standalone prose, fresh-practice presence, local links and fragments, contents destinations, companion PDF targets, nonempty PDF pages, figures, alternative descriptions and SVG self-containment. External URLs are outside this offline verifier.

The previous edition’s installer idempotence check covered 69 authoring and editorial files. The current edition adds AI lesson sources and preserves the same managed-block installation approach. Build tools preserve unmarked prose and replace only their declared managed blocks. Python bytecode is excluded from version control; PDF and ZIP artifacts are tracked as binary files.

For asphalt-specific validation and remaining technical review, see the [asphalt record](../asphalt-paving/VALIDATION.md) and [Roadbuilding delivery record](../asphalt-paving/line-a/technical-handoff.md).
