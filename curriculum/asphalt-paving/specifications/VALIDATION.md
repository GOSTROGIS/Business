# Specifications module validation

**29 October 2026 · classroom teaching edition**

- **354 offline checks passed**, no errors: [validation.json](validation.json).
- **61 browser checks passed**, no errors, across five HTML pages at 375, 768 and 1280 px: [browser-validation.json](browser-validation.json).
- Learner workbook: **18 PDF pages**. Teaching and answer guide: **11 PDF pages**. Printed contents-page numbers were compared with the final PDFs' named destinations; both books converged in two export passes.
- **18 learner activities and 18 complete answer entries**, with evidence criteria for all **nine Skills for Success**; **five CSV datasets** and **five original SVG diagrams**, plus **two source figures made from three faithful PDF crops**. Every learner figure has a source/provenance note; the new source figures use APA-style captions and full reference entries.
- Original specification: **441 pages**, **4,949,922 bytes**, SHA-256 `0e57525e900390dc04451855039de6daa2b39bae79329d2878800228e69d1c13`. Original bytes preserved.

## Visual and terminology integration

The complete Table 501-E crop preserves its title, five mix columns, all twelve sieve rows and original footer. The paired Road Checker’s Summary crops preserve the clause heading, both paragraphs and the entire continued list, including the open-list and minimum-frequency qualifiers. The crop manifest records page numbers, bounding boxes, source and asset hashes, and rendering parameters. Verification renders those exact source regions again and compares every pixel. A complete table text alternative and a delivery-paragraph/list transcript support the image reading. Two previously mistyped words in the latter transcript were corrected against the actual PDF.

New SP-01 and SP-08 steps ask learners to trace a row/column and a paragraph continuation; the answer guide explicitly checks both. The module identifies its support for A5.4, F2.1/F2.4 and introductory F3.2/F3.4 context without marking those technical competencies complete. Printed learner pages 5 and 11 were reviewed at full size for readable source crops and uninterrupted figure notes.

## What was checked

The selected Table 501-E values, Table 501-F tolerance and record/application-rate clauses were compared with the actual PDF pages, including visual inspection of pages 286, 287, 300 and 309. An independent curriculum review checked the supplied inputs, all activity IDs, answer alignment, mathematical results, four 90-minute session sums and observable skill evidence. The two specification strands and the distinction between a ten-load monitoring block and a formal acceptance Lot remain explicit.

The offline verifier checks the original-file hash/size/pages, source-library manifest, selected historical table values, sample comparisons, means, ticket uniqueness, times, replacement corrections, rectangular areas, unit conversions, material-rate calculations, target ratio, activity/skill coverage, SVG XML/title/description, local HTML assets, source page bounds, readable PDFs, PDF link portability and contents-page destinations. Browser checks cover document overflow, image loading, alternative text, a single main title and failed HTTP requests. These are bounded technical checks, not a general accessibility certification.

Every page was included in the final PDF contact-sheet review. Full-size checks covered source addressing, grading constraints, dimensions, the version-change calculation, spreadsheet instructions and the nine-skill evidence table. The five SVGs were rendered and inspected for legible labels, quantitative scale, non-overlapping area geometry, clipping and correct units. The learner reflection and teacher observation record retain writing space. Two response-only overflow pages found in an earlier export were removed before this release.

## Reproduce

```sh
python curriculum/asphalt-paving/specifications/tools/build_source_crops.py
python curriculum/asphalt-paving/specifications/tools/build_module.py
python curriculum/asphalt-paving/specifications/tools/verify_module.py
python curriculum/asphalt-paving/specifications/tools/check_browser.py
```

Use the existing asphalt tools requirements and a local Chromium executable. Browser checks write their report beside the books. The offline verifier does not fetch external URLs or establish current legal or contractual applicability.

## Delivery status

The module is a complete classroom draft using selected historical technical reading and invented practice data. **Qualified technical review and a classroom pilot remain pending.** No current project specification, mix acceptance, payment decision, official proficiency level or trade certification is established by these checks. Record the responsible review and any changes before extending the exercises into project-specific training.
