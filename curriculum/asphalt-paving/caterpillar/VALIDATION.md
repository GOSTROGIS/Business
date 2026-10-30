# CAT and WHMIS collection validation

**30 October 2026 · editorial/source checks, not independent technical approval**

## Delivered files

| Collection | Verified extent |
|---|---|
| CAT original publication sequences | 22 publications; 1,883 pages; 88 native PDF parts |
| Largest CAT PDF part | 9,223,322 bytes; all parts at most 25 pages and 10 MiB |
| Source atlas | 20 credited illustrations; 89 component rows in HTML/JSON/CSV; 23-page PDF |
| CAT identification practice | 10 complete tasks; 6-page learner PDF; 7-page teaching/answer PDF |
| WHMIS artwork | 10 official pictograms, each in PNG/EPS/SVG; nine WHMIS families plus environment |
| WHMIS source publications | Seven PDFs; 218 pages; five CCOHS sheets revised 28 May 2026 and two historical 2019 WorkSafeBC books |
| WHMIS classroom books | 10-page reference; six tasks in a 4-page learner PDF; 4-page answer guide |
| CAT ZIP volumes | Four complete-publication volumes: 31.74, 26.72, 23.00 and 33.79 MiB |
| WHMIS classroom ZIP | 8,175,558 bytes; 56 members |

## Provenance and image checks

The original download URL, source-file SHA-256, page count, publication identity and model scope are pinned in the catalogue and per-publication records. The full page sequences are retained in native PDF parts, with original notices and no image downsampling. Small originals are byte-identical; larger sources are split with pypdf while preserving page resources. Internal/non-URI page-link annotations are omitted from splits; external links remain. Whole-source URLs remain in the index.

Every one of the 20 atlas PNGs was regenerated from its recorded original source page and crop rectangle and matched its recorded SHA-256 exactly. Source-page links, model scopes and the 89-row CSV were checked. All selected conveyor callouts 1–7, track callouts 1–6, roller-control callouts 1–19 and loader-pin letters A/B/C/D/E/F/G/K/Y/S1/S2 are present. Selected source labels were checked directly against their PDF text and illustrations. Crops and printed contact sheets were visually reviewed; cut-off neighbouring text was removed from the crop bounds.

The official CCOHS PNG and EPS files match the corresponding members of the preserved original download ZIP byte-for-byte. All ten SVGs parse as SVG and were visually checked together. They are vector conversions of the official EPS artwork; no symbol, frame geometry or colour redesign was made. The biohazard circular frame is retained. Two complete CAT safety pages preserve the full warning text and location context.

## Navigation, print and packaging

- **417 local links** checked, including file existence, HTML anchors and PDF page bounds.
- **24 browser cases** passed across eight pages at 320, 390 and 1280 CSS pixels: no horizontal document overflow, broken images, failed bundled fonts or JavaScript errors.
- Atlas filtering checked for a matching term and an empty result; full-publication search returns source-page links.
- Six new printed books have readable text and no localhost links. PDF links use repository URLs; HTML supplies local offline navigation. Atlas figures, WHMIS pictogram pages and warning reproductions were visually inspected.
- All four CAT ZIPs passed CRC checks, contain each publication exactly once across the volumes, and contain byte-identical copies of their indexed PDF/text parts. Each volume has its own working local index, fonts, records and instructions. No publication is split across volumes.
- The WHMIS ZIP passed CRC and local-link checks. Its external CAT links use repository URLs; its WHMIS source files, artwork and lessons are local.
- The existing asphalt material verifier passed **799 checks** after navigation integration.

## Context library

The refreshed asphalt context library indexes **159 PDF paths, 158 unique PDFs, 4,508 pages and 215 chunks/text extracts**. It reuses all 88 CAT source parts and 34 MS-4 source parts directly, avoiding another copy of their PDF payloads. CAT text records retain both part-local and complete-publication viewer page numbers. The verifier passed source hashes, complete inventory, sizes, page ranges, text maps, source reuse, link destinations and CSV checks; 105 representative context render comparisons passed. The complete CAT source comparison is recorded below separately.

## Remaining limits

Parts reference guides contain selected service/wear parts. Complete fleet-specific parts catalogues and additional OMMs require the actual model, serial and attachment identities. Only the two listed roller model families have complete OMMs in this CAT addition. The 2016 outline's six named course manuals and historical CDs remain separate access gaps. Neither these resources nor the classroom exercises claim complete technical competency coverage, workplace-specific WHMIS training, equipment authorization or independent technical review.

Reproduce checks with `tools/verify_sources.py --downloads PATH`, `tools/verify_classroom.py` (repository served on localhost:8765), and the asphalt `tools/verify_context.py`. The source verifier compares native page content, page appearance, normalized extracted text, hashes, complete ranges and part size limits. Text normalization covers whitespace, Unicode compatibility forms and soft hyphens; original extracted text files are retained independently.


## Complete CAT page fidelity result

**All 1,883 source pages passed** across all 22 publications and 88 PDF parts. Native page content streams matched exactly. Normalized extracted text matched on every page. At 36 dpi, 1,880 page renders matched exactly; three low-resolution sampling differences (CAT-01 p. 269, CAT-02 p. 35, CAT-03 p. 40) were rechecked at 100 dpi and matched exactly there. No page image was resampled in the PDFs. Hashes, continuous page ranges, part page/byte limits and retained in-part link bounds passed. The initial splitter's colour/resource differences were corrected before this final comparison.

[Machine-readable verification results](validation-results.json) records the source-page, classroom and context outcomes.
