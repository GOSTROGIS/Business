# Asphalt A1 validation record

**Teaching draft · 23 October 2026**

## Source and content review

- All three supplied PDFs are preserved byte for byte; SHA-256, byte counts and page counts are recorded in `sources/manifest.json`.
- The outline's A1–A6 titles, all nine A1 learning tasks, relevant equipment references, and the distinction between PDF and printed page numbers were reviewed against the supplied documents.
- The Skills for Success map links each skill to selected named guide components, exact guide pages, actual question IDs and observable evidence. It does not assign official proficiency levels.
- Independent review checked the 18 learner activities against the instructor answers, the three 60-minute plans, dataset arithmetic and scope claims. Corrections added an explicit road-type description in Q06, separated the revision card, and marked A1 tasks 6, 8 and 9 as requiring current-source supplements.
- Fictional examples, project roles, funding, industry data and distances are labelled. The verified totals are 10 employers, 300 workers, $15,000,000 contract value, Central's 3/10 share, a $2,000,000 North/Central difference and $120,000 fictional project funding. Contract value is not presented as profit.

## Reproducible checks

From this folder:

```sh
python -m pip install -r tools/requirements.txt
python tools/build_materials.py
python tools/verify_materials.py
```

**Completed:** 445 offline checks passed. The builder produced nine HTML pages and five printable PDFs: learner workbook (10 pages), instructor guide (12), response sheet (11), change card (1) and process cards (3). The offline verifier checks original source integrity, all 18 question IDs across the workbook/answer key/response sheet, nine skills with task references, practice-data calculations, local HTML resource links, PDF page-link bounds, readable PDF pages and the absence of machine-local links in exported PDFs.

## Presentation review

The learner workbook, instructor guide, curriculum landing page and three printable handouts were rendered in Chromium at 390, 768 and 1440 CSS-pixel widths. Checks cover document overflow, missing images, loaded local fonts, failed resource requests and browser errors. Wide tables scroll within their containers on narrow screens. Desktop/mobile screenshots and representative printed pages were reviewed. Print pagination keeps the short learner tables together and separates response-sheet work areas at appropriate question boundaries.

The badge and palette follow the Numeracy Hub reference recorded in `assets/README.md`. Local fonts include their licences. Exported PDF links point to the Business repository rather than a temporary preview server.

## Teaching validation still needed

These are newly authored materials, not a classroom-tested or provider-approved course. An asphalt instructor should review terminology, accessibility, pacing and assessment evidence, then record findings from a pilot. Current B.C. industry data, applicable regulation/funding documents and a sourced asphalt/concrete environmental comparison are still needed for A1 tasks 6, 8 and 9. A2–A6 are mapped for development but their lessons are not yet written.
