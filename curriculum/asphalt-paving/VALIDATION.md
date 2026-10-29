# Asphalt curriculum validation record

**ACCESS IS4S classroom edition · updated 29 October 2026**

## Roadbuilding foundations · 29 October 2026

The [Line A learner book](line-a/roadbuilding-foundations.pdf) and [teaching and answer guide](line-a/teaching-guide.pdf) deliver six authored classroom units with **37 unique activities**. Separate answer guides map **33 learning-task criteria**: A1.6, A1.8 and A1.9, plus all 30 tasks across A2–A6. The original 18-activity opening case introduces the broader A1 context. The [whole-program status register](line-a/competency-status.md) accounts for **68 competencies**, separating the six authored Line A classroom units from 62 later competencies without complete technical units. F2/F3 receive a foundation bridge only.

**Recorded Line A check run: 276 checks, zero errors.** The learner PDF has **28 pages** and the teaching PDF **17 pages** in this validated build. Checks cover unique activity IDs and keyed answers; the 33 learning-task mappings; all 68 competency codes and unfilled technical/practical approvals; 20 curated public evidence records; Statistics Canada source scope and category totals; 23 arithmetic comparisons; local generated links; readable PDFs containing every activity; and the absence of machine-local PDF links.

The source checks distinguish the 427 B.C. NAICS 237310 statistical locations with employees from unique employers or worker counts. They retain the publisher's December 2025 table title alongside the downloaded `2025-07` reference-period field. Answer arithmetic includes percentage points, funding shares, elapsed years, fictional hours, metric conversions, road quantities and bounded historical cost comparisons. Passing these checks validates the recorded structure and calculations; it does not independently approve all technical content or establish workplace competence.

From the asphalt-paving directory:

```sh
python tools/build_line_a.py
python tools/verify_line_a.py --require-generated
```

The six units distinguish dated public evidence from invented classroom inputs. The current A1 material now includes public industry measures, selected legal/contract information, actual reported project funding and evidenced recovery pathways. It does not claim an asphalt-only employer total, confirm a particular contract's governing requirements or rank pavement materials through a matched B.C. project life-cycle analysis. These limits are retained in the teaching criteria and [technical review record](line-a/technical-handoff.md).

## Current opening-case artifacts · 29 October 2026

The original 18-activity case remains available with its separate answer key and printable materials. Its current exports contain **11 learner pages, 12 instructor pages, 11 response-sheet pages, one change-card page and three process-card pages**. This is distinct from the 28-page and 17-page Line A books.

The current opening-case verifier passed **586 offline checks**. The opening dataset, distances, project brief and roles remain labelled classroom inventions. Their arithmetic is useful practice; those values have not become current industry statistics. Current public evidence is identified separately in the Line A lessons and research record.

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

The specifications workshop contains 18 activities with full keys, five SVGs and five CSVs. Its final learner PDF has 15 pages and its teaching guide has 10. The module passed 291 offline checks and 61 browser checks; independent review confirmed the selected historical table values and exercise calculations.

The manual ZIP contains 709 files, including six complete OEM PDFs (650 pages), the complete John Deere 410G HTML collection and the 441-page historical specification. Its nine-activity lesson and separate key cover all nine skills. Archive CRC, package hashes, original PDF page counts, original-file hashes, offline links and printed layouts passed checks. Repository files were independently compared byte for byte with the final archive members. Exact required course-publication gaps are stated in the resource index.

The context library indexes all 22 available asphalt PDF paths as 21 unique PDFs and 1,470 pages. It provides 71 PDF chunks and 71 text extracts. Each chunk has at most 25 pages; the largest is 4,034,508 bytes. Original PDFs are preserved, duplicate paths are recorded and text extraction limitations are explicit. The library's manifest is the detailed inventory.

## Primary textbook transfer

MS-4 Seventh Edition is the selected primary textbook. The user supplied the handbook on 29 October 2026, but the upload exceeds the workspace transfer tool's 32 MiB limit. It has not been copied into the repository, read in full, added to the ZIP or split into context chunks. The textbook integration plan distinguishes publisher-verified contents from alignment that still requires the actual book. The context manifest inventories the available PDFs only.
