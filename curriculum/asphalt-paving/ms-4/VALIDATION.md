# MS-4 conversion and lesson validation

**Checked 30 October 2026.** These are source-integrity, editorial, content-structure, rendering and browser checks. Qualified independent technical review and local classroom piloting remain pending.

## Complete source and conversion

The actual supplied file contains **834 PDF pages**, including front matter, credits, index and end matter. Its 180,202,618-byte SHA-256 is `cb4708d2854d06d492af6dfdf0d39600af0ec45feef4c179c48fcff107da046b`. The publication page identifies Asphalt Institute, 2007, seventh edition, ISBN 978-1-934154-27-4. Contents pages and the fifteen chapter-opening pages establish the [chapter map](chapter-map.md).

- **34 native source PDF parts**, at most 25 pages / 12 MiB each. All source pages are retained in their original order without resampling. Every part hash, size and range passed verification. Every one of the **834 part pages matched the original's 36 dpi render exactly**, with annotations disabled for comparison; page dimensions also matched. Original source pages contain no link annotations.
- **834 display images**, lossless WebP encodings of 150 dpi grayscale renders, with per-page hashes. Native PDFs retain the original scan resolution.
- **834 OCR text files and word-coordinate records**, generated with English Tesseract at 250 dpi. The complete machine result has **244,217 detected words**. Seven pages produced no words and 53 pages have mean confidence below 75. These are extraction flags, not a declaration that a page is empty or unreadable.
- **62 HTML reading sections**, each at most 16 source pages, plus the collection index and two concept books. Coverage checks found exactly one displayed source-page article for every viewer page. All local assets, HTML anchors and source-PDF page destinations passed checks.
- Full-book search contains all 834 effective text records and links to the exact page article. A documented editorial override supplies the faint cover's publication text while retaining the empty original OCR. Page downloads use the displayed text; an overridden page also links its original machine OCR.

The full OCR is **not proofread**. Numbers, symbols, tables, diagrams and technical conditions must be checked against the retained scan or native PDF. All source-page images remain available beside their transcription. Complete conversion does not mean complete technical review of every sentence.

## Illustrated learner and teaching books

The complete concept sequence has **17 learner PDF pages**, **six teaching/answer PDF pages**, six SVG redraws and twelve activities **MS4-01–MS4-12**, each with separate answer guidance. All nine Skills for Success have explicit opportunities and individual evidence. Numerical keys distinguish the 300 mm worked example from the 350 mm / 0.350 m new model. The pass/coverage key distinguishes two passes at a point from one established full-width coverage.

Selected source passages and figures were visually checked on PDF pages **47–48, 343–346, 411–412, 417–418 and 450**. Contributor credits were checked on **803–805**. The [figure manifest](concepts/figure-manifest.json) records exact figures, printed/viewer pages, source and asset hashes, meaningful adaptations and original contributor credits. Terex Roadbuilding, National Highway Institute and Volvo Construction Equipment are credited with their applicable source figures. No drawing supplies a new numerical design, machine control setting or rolling procedure.

All six printed diagrams were inspected with their captions on learner pages **4, 5, 7, 9, 11 and 13**. The pages show clear labels and contained diagrams with source notes. Automated checks confirmed readable PDF pages, text within page bounds and portable PDF links. All SVGs are valid XML and their recorded hashes match the files. Three redraws also appear in the [Line A learner book](../line-a/roadbuilding-foundations.html), with matching tasks and keys; see its [validation record](../line-a/VALIDATION.md).

## Browser checks

**30 page/viewport cases** passed in Chromium at **320, 390 and 1280 px**. The cases covered the book landing page, front matter, selected production/paving/compaction/credit sections, both concept books and both modified Line A learner units. There was no document-level horizontal overflow, failed image/resource request or browser script error. Bundled fonts loaded.

Functional checks passed for keyword search, result counts, exact-page result links, zero-result feedback, clear-and-refocus, text/scan/combined view controls, page jumps and previous/next navigation. The reader uses local assets and local search data; no account or external search service is required. These checks are not a complete assistive-technology audit.

## Context and reproducibility

The overall asphalt context inventory includes the 34 handbook source parts directly, without making another PDF copy. Each associated text chunk records its part-local and complete-book page numbers, OCR status and upstream text hash. The context verifier checks complete coverage, all hashes, file limits, text mappings and PDF fidelity. Source and generated lesson PDFs remain separately identified.

```sh
python -m pip install -r curriculum/asphalt-paving/ms-4/tools/requirements.txt
python curriculum/asphalt-paving/ms-4/tools/verify_reader.py --browser
python curriculum/asphalt-paving/ms-4/tools/verify_reader.py --original /path/to/acquired-original.pdf
python curriculum/asphalt-paving/tools/verify_line_a.py --require-generated
python curriculum/asphalt-paving/tools/verify_context.py
```

The full original-file comparison run passed **16,388 assertions**, including 834 page renders and 30 viewport cases. A subsequent reader-only correction made downloads use the displayed editorial text and retain a separate original-OCR link; source pages and lesson PDFs were unchanged. Visual inspection also identified a stretched cover image on the desktop landing page; the stylesheet now preserves its aspect ratio and the browser checks verify image proportions. Follow-up reader/link/browser verification passed. This validation record preserves the distinction between a complete source collection, checked introductory concept lessons and the later technical units still requiring authoring, review and practical assessment.
