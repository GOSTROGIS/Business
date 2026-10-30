# Asphalt curriculum validation record

## Study textbook Volume 1 · 30 October 2026

The [new standalone study volume](textbook/README.md) contains a 77-page textbook, a 20-page worked-answer guide, 60 activities, 44 image placements and 13 original SVGs. It develops A1–A6 and all seven B1 safety-orientation tasks. [Book verification](textbook/VALIDATION.md) records 533 local-target checks, 47 fragment checks, 17 browser/interaction checks, image and pinned-source identity checks, PDF inspection and complete answer coverage. Technical approval and classroom pilot are pending. The updated competency register leaves 61 complete technical units, B2–L6, for subsequent authoring.

Existing material and Line A checks pass (827 and 351). The context index now contains 322 unique PDFs / 7,856 pages / 382 chunks, with 114 representative page-render comparisons and 2,379 retained URI links verified. Historical validation snapshots below describe their original editions.


**ACCESS IS4S classroom edition · updated 29 October 2026**

## Roadbuilding foundations · 29 October 2026

The [Line A learner book](line-a/roadbuilding-foundations.pdf) and [teaching and answer guide](line-a/teaching-guide.pdf) deliver six authored classroom units with **37 unique activities**. Separate answer guides map **33 learning-task criteria**: A1.6, A1.8 and A1.9, plus all 30 tasks across A2–A6. The original 18-activity opening case introduces the broader A1 context. The [whole-program status register](line-a/competency-status.md) accounts for **68 competencies**, separating the six authored Line A classroom units from 62 later competencies without complete technical units. F2/F3 receive a foundation bridge only.

**Recorded Line A check run: 299 checks, zero errors.** The learner PDF has **34 pages** and the teaching PDF **17 pages** in this validated build. Checks cover unique activity IDs and keyed answers; the 33 learning-task mappings; all 68 competency codes and unfilled technical/practical approvals; 20 curated public evidence records; Statistics Canada source scope and category totals; 23 arithmetic comparisons; local generated links; readable PDFs containing every activity; and the absence of machine-local PDF links.

The source checks distinguish the 427 B.C. NAICS 237310 statistical locations with employees from unique employers or worker counts. They retain the publisher's December 2025 table title alongside the downloaded `2025-07` reference-period field. Answer arithmetic includes percentage points, funding shares, elapsed years, fictional hours, metric conversions, road quantities and bounded historical cost comparisons. Passing these checks validates the recorded structure and calculations; it does not independently approve all technical content or establish workplace competence.

From the asphalt-paving directory:

```sh
python tools/build_line_a.py
python tools/verify_line_a.py --require-generated
```

The six units distinguish dated public evidence from invented classroom inputs. The current A1 material now includes public industry measures, selected legal/contract information, actual reported project funding and evidenced recovery pathways. It does not claim an asphalt-only employer total, confirm a particular contract's governing requirements or rank pavement materials through a matched B.C. project life-cycle analysis. These limits are retained in the teaching criteria and [technical review record](line-a/technical-handoff.md).

## Current opening-case artifacts · 29 October 2026

The original 18-activity case remains available with its separate answer key and printable materials. Its current exports contain **13 learner pages, 12 instructor pages, 12 response-sheet pages, one change-card page and three process-card pages**. This is distinct from the current 38-page and 17-page Line A books.

The current opening-case verifier passed **769 offline checks** after the updated textbook links. The opening dataset, distances, project brief and roles remain labelled classroom inventions. Their arithmetic is useful practice; those values have not become current industry statistics. Current public evidence is identified separately in the Line A lessons and research record.

Rebuild and check the opening case from this directory:

```sh
python -m pip install -r tools/requirements.txt
python tools/build_materials.py
python tools/verify_materials.py
```

## Earlier opening-case record · 23 October 2026

This dated record describes the initial build and its checks; its page counts are historical.

- All three supplied PDFs were preserved byte for byte. SHA-256 hashes, byte counts and page counts are recorded in [sources/manifest.json](sources/manifest.json).
- The A1–A6 titles, nine A1 learning tasks, relevant equipment references and PDF-versus-printed page numbering were reviewed against the supplied documents.
- The skills map connected all nine skills to actual question IDs and observable evidence without assigning official proficiency levels.
- Independent review checked the 18 activities, instructor answers, three 60-minute plans, dataset arithmetic and scope claims. Corrections added an explicit road-type description in Q06, separated the change card and marked tasks A1.6, A1.8 and A1.9 for further evidence work. That evidence work is now authored in Line A; application and technical-review limits remain explicit.
- Fictional-data checks confirmed 10 employers, 300 workers, $15,000,000 contract value, Central's 3/10 share, a $2,000,000 North/Central difference and $120,000 fictional project funding. Contract value was not presented as profit.

**The initial run passed 445 offline checks.** It produced nine HTML pages and five PDFs: learner workbook 10 pages, instructor guide 12, response sheet 11, change card one and process cards three. The verifier covered source integrity, question IDs across the workbook/answer key/response sheet, nine-skill task references, practice-data calculations, local links, source PDF page bounds, readable PDF pages and machine-local link exclusion.

The initial learner and instructor pages, curriculum landing page and three handouts were rendered at 390, 768 and 1440 CSS-pixel widths. Review covered overflow, images, local fonts, failed resource requests and browser errors. Wide tables scrolled within their containers on narrow screens. Screenshots and representative printed pages were reviewed. The palette and badge followed the Numeracy Hub direction documented in [assets/README.md](assets/README.md); local fonts included their licences.

## Reviews and delivery evidence still pending

These are authored classroom materials. Independent qualified technical review, ACCESS delivery agreement, local co-design and classroom pilot are not yet recorded. The [technical handoff](line-a/technical-handoff.md) identifies concrete review questions for statistics, law and specifications, environmental comparisons, history, technology, worker expectations, road documents and trends. Its sign-off fields remain blank; the status register makes no practical-assessment claim.

The historical profile's 120 hours, the provider's published 140 accumulated-hour statement and the proposed classroom practice time remain separate records. The provider statement is verified as published; its allocation and relationship to the historical pathway still need clarification from the responsible provider or regulator.

The [specifications workshop](specifications/README.md) and [manual resource pack](manuals/README.md) record their editions, acquisition, content and packaging checks in their own folders. The complete uploaded 2006 specifications PDF is preserved byte for byte and registered in the source manifest. These artifact checks do not establish machine suitability or approval for a current project.

A pilot should record actual durations, access arrangements, confusing terms, individual activity evidence, calculation errors, learner feedback and revisions. Retaining identifiable learner work requires consent. Equipment operation, workplace practical assessment and later Lines B–L require their own authorized instruction and evidence.

## Specifications, manuals and PDF context

The specifications workshop contains 18 activities with full keys, five SVGs, two source figures made from three faithful crops, and five CSVs. Its learner PDF has 18 pages and its teaching guide has 11. The module passed 354 offline checks and 61 browser checks; independent review confirmed the selected historical table values, source-crop pixels, figure citations and exercise calculations. The original table also has a complete text alternative.

The manual ZIP contains 715 files, including six complete OEM PDFs (650 pages), the complete John Deere 410G HTML collection and the 441-page historical specification. Its nine MAN activities and four new VIS activities have separate answer guidance. The 12-page learner lesson and five-page instructor guide use four faithful manufacturer crops with APA figure notes and exact page/model scope. [Visual validation](manuals/VISUAL-VALIDATION.md) records the checks. Archive CRC, package hashes, original PDF page counts, original-file hashes, offline links and printed layouts passed checks. Repository files were independently compared byte for byte with the final archive members. Exact required course-publication gaps are stated in the resource index.

Before the MS-4 integration, the context library indexed 22 asphalt PDF paths as 21 unique PDFs and 1,492 pages. That earlier snapshot provided 71 PDF chunks and 71 text extracts. Each chunk has at most 25 pages; the largest is 4,034,508 bytes. Original PDFs are preserved, duplicate paths are recorded and text extraction limitations are explicit. The library's manifest is the detailed inventory. All 71 chunks passed hash, range, size and text-page checks; 60 representative original-versus-chunk page renders matched exactly, with annotations disabled for that comparison.

## Visual and terminology integration

The [curriculum review](review-and-integration.md) checks the six Line A competencies and exact terminology against the supplied outline. The [integrated teaching route](teaching-route.md) connects all nine Skills for Success chapters with individual asphalt activity evidence. Later I2, J1 and L1 component-reading links remain introductory; the later technical units are not marked complete.

Seven new source-image crops form six cited figures across the manual and specification lessons. The Line A technology unit reuses the labelled LeeBoy overview with its own figure note and reading task. Original manufacturer/source files remain unchanged. Adjacent APA figure notes, references, alt text, source hashes, page labels and crop rectangles preserve provenance. Independent checks compared all seven crop regions with the original PDF pixels and confirmed selected labels, quantities, answer keys and model limits. The new opening EPS SVG is an original ACCESS diagram based on clause 502.03.01, PDF 297 / printed 1 of 22; it is not an MS-4 adaptation.

The opening, integrated route and review pages passed 12 browser checks at 320, 390 and 1280 CSS pixels. All 18 Line A pages passed the same three widths (54 checks), and the manual pages passed nine viewport checks. No document overflow or failed images was reported. Representative printed source figures, the EPS diagram and the dedicated Q10 response page were visually inspected. Line A now uses the Numeracy Hub cream, ink, red and gold palette.

## Complete primary textbook · 30 October 2026

The Google Drive permission change enabled acquisition of the full MS-4 seventh edition. All 834 scanned pages are now available in 62 HTML sections, with page images, searchable OCR and 34 native source PDF parts. Six cited SVG redraws and twelve complete concept activities include separate answer guidance; three redraws are integrated into Line A. [Textbook validation](ms-4/VALIDATION.md) records the current conversion and lesson checks. The whole-book transcription is unproofread OCR; preserved source pages remain available for exact technical checking. The source is in the repository's separate textbook collection, outside the OEM ZIP.

After the MS-4 integration and before the CAT expansion, the context snapshot contained **58 PDF paths, 57 unique PDFs, 2,353 pages, 107 PDF chunks and 107 text extracts**. Its largest PDF part is **11,682,239 bytes**, and all parts have at most 25 pages. The 34 MS-4 source parts are reused directly, avoiding a second copy of the handbook. Their text records include both the part-local and complete-book viewer page. `tools/verify_context.py` passed inventory, hash, page-range, byte-limit, OCR mapping, annotation and CSV checks; **66 representative page renders** matched their originals. The separate MS-4 verifier compared **every one of its 834 native PDF pages** with the original scan.

The refreshed OEM archive still contains **715 files** and seven complete OEM references. Its current size and SHA-256 are recorded in [archive-info.json](manuals/archive-info.json); the complete textbook remains in its own collection to keep this ZIP below the repository file-size limit.


## CAT identification and WHMIS expansion · 30 October 2026

The [CAT/WHMIS validation record](caterpillar/VALIDATION.md) covers 22 CAT publications (1,883 source pages in 88 parts), a 20-figure/89-component atlas, ten identification tasks, official WHMIS PNG/EPS/SVG artwork, seven WHMIS source PDFs and six WHMIS tasks. Four CAT ZIP volumes are each under 34 MiB; the WHMIS ZIP is 8,175,558 bytes. The new classroom pages passed 417 local-link checks and 24 browser cases. All 20 atlas crops match their recorded source regions exactly. The existing asphalt verifier passed 799 checks.

The context snapshot for that expansion contained **159 PDF paths, 158 unique PDFs, 4,508 pages and 215 chunks/text extracts**. All 88 CAT parts and 34 MS-4 parts are reused directly. Hashes, inventory, ranges, text page maps, annotation destinations and 105 representative render comparisons passed. Its largest part remains 11,682,239 bytes, with at most 25 pages and no size exceptions.

The original OEM ZIP was refreshed with links to the separate CAT and WHMIS collections. It still contains 715 entries and seven complete OEM references; its new size is **57,007,655 bytes**, SHA-256 `fb4e22f7a13a3ca6dbcc9959aa6efd7b288bad76e1a7ff93a96ba6b0373566d4`. Its CRC and relative-path checks passed. The CAT/WHMIS files are packaged separately to keep those downloads smaller.


## Full-outline source and tool audit · 30 October 2026

The [new collection validation](readiness/VALIDATION.md) covers 41 complete PDF publications (3,240 pages in 161 small parts), 30 complete archived web articles and 33 source figures. Every PDF page passed visual comparison; original article text and image hashes were checked. A recorded NIOSH alternate-text extraction variation preserves the original text extract and matches the original visible page at 100 dpi.

The collection includes a complete 68-competency source map, 32 tool/equipment groups, three original SVGs, four credited source-page images, an 11-page visual guide and eight ZIPs below 40 MiB. Checks passed for 1,218 local HTML targets, 957 offline ZIP HTML targets, all archive CRCs and source-part hashes, and 12 browser page/viewport cases. The existing material verifier passed 827 checks.

The current context snapshot contains **321 PDF paths, 320 unique PDFs, 7,759 pages and 377 chunks/text extracts**. It directly reuses all 161 readiness, 88 CAT and 34 MS-4 source parts. Inventory, hashes, page maps, sizes, destinations, 108 representative render comparisons and 2,256 retained URI links passed. Exact course manuals, fleet/instrument applicability and site/qualified-review requirements remain recorded in the delivery gap register.
