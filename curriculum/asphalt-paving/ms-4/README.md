# The Asphalt Handbook · MS-4 Seventh Edition

**Primary asphalt textbook · full source collection · accessed 30 October 2026**

[Open the complete HTML reader](index.html) · [Learn the illustrated concepts](concepts/index.html) · [Learner PDF](concepts/learner-workbook.pdf) · [Teaching and answer guide](concepts/teaching-guide.pdf) · [Verified chapter map](chapter-map.md)

The complete supplied scan is now in this repository as **834 preserved source pages**, **62 linked HTML reading sections**, **834 page images and editable text records**, and **34 small source PDFs**. The source has 15 chapters, with front matter, contents, illustration/table lists, contributor credits, index and end matter retained. The six ACCESS SVG redraws and twelve concept activities connect selected verified passages to the SkilledTradesBC outline and all nine Skills for Success.

## Source identity

| Field | Verified record |
|---|---|
| Publication | *The Asphalt Handbook*, MS-4, seventh edition |
| Corporate author | Asphalt Institute |
| Publication year | 2007, verified on source PDF page 4 |
| ISBN | 978-1-934154-27-4 |
| Supplied filename | `the-asphalt-handbook -MS-4-7th-ed.pdf` |
| Acquisition | [User-supplied Google Drive download record](acquisition.json); downloaded 30 October 2026 |
| Actual scan | 834 PDF pages; 180,202,618 bytes |
| Original SHA-256 | `cb4708d2854d06d492af6dfdf0d39600af0ec45feef4c179c48fcff107da046b` |
| Edition evidence | Original cover/title/publication pages, PDF 1, 3 and 4; back cover PDF 834 |
| Contents evidence | Source PDF 9–19; actual chapter opening pages verified against this sequence |

The publisher's earlier catalogue listing of 832 pages is not the page count of this supplied scan. Use **834** for this file. The original 180 MB download exceeds GitHub's per-file limit, so its page content is preserved without resampling in the 34 PDFs under `pdf/`. [Source-parts metadata](source-parts.json) records the original identity, every range and each part's hash. The largest part is 11,682,239 bytes. The unsplit download remains unchanged in the acquisition workspace; everyday editing does not require it.

## Read, search and inspect

Open `index.html` in a browser, or serve the repository with `python -m http.server 8000`. The reader has chapter navigation, previous/next section links, page jumps, full-book search, and text/scan/both reading views. Search and chapter reading use local files, with no external API or account requirement. Select a page image to enlarge it, or open its linked original PDF part for the full-resolution source. The page link already includes the correct part-local page number.

The source scan contains no text layer. Tesseract produced **244,217 OCR words** across all 834 pages. The transcription is **not fully proofread**: it can misread numbers, symbols, table columns and faint headings. The source images and native PDF pages retain the original figures, tables and layout. Check those before using a technical value. Seven pages yielded no OCR words; this includes the faint cover, whose publication text has a separately recorded editorial transcription. Do not interpret a no-word result as proof that a page is blank.

The displayed images are lossless WebP encodings of 150 dpi grayscale page renders. OCR used 250 dpi renders. The native PDF parts preserve the original scan resolution and page content. No book page was dropped to make the HTML.

## Manage the content

- `book-map.json`: verified titles and page ranges; the chapter text begins at PDF 35, printed page 1.
- `reader/`: generated HTML sections, at most 16 source pages per file.
- `text/`: complete machine OCR, one UTF-8 file per original viewer page.
- `data/`: OCR word boxes, confidence and source/image/text hashes.
- `edits/`: editable page overrides; keep the original OCR and record the reason/source check for each correction.
- `assets/pages/`: all source-page display images; `assets/search-index.js` carries local search text.
- `pdf/`: the 34 native source parts, each at most 25 pages and 12 MiB.
- `concepts/`: complete ACCESS learner/teaching books, six SVG redraws, exact figure provenance and twelve activities with answers.
- `manifest.json`: complete inventory, page locations, extraction coverage and confidence flags.

To correct a transcription, copy the corresponding `text/pNNNN.txt` to `edits/pNNNN.txt`, edit while comparing with the scan, and record the change in `edits/README.md`. Then rebuild the reader. Edit the concept teaching prose in `concepts/learner.md` and `concepts/instructor.md`; figure placeholders resolve from `concepts/figure-manifest.json` and their reproducible SVG generator.

```sh
python -m pip install -r curriculum/asphalt-paving/ms-4/tools/requirements.txt
python curriculum/asphalt-paving/ms-4/tools/build_reader.py
python curriculum/asphalt-paving/ms-4/tools/build_concepts.py
python curriculum/asphalt-paving/ms-4/tools/verify_reader.py
python curriculum/asphalt-paving/tools/build_context.py
```

Tesseract with English language data is needed only to rerun OCR. Chromium is required for concept PDF export. To recreate extraction from the original download, run `tools/extract_book.py /path/to/original.pdf --workers 4` and `tools/split_source.py /path/to/original.pdf` before rebuilding. Existing verified OCR pages are reused. These tools never modify the original download.

## Curriculum and figure review

The [chapter map](chapter-map.md) replaces the earlier topic-only planning map with actual chapter titles/ranges. The conceptual lessons use visually checked passages and figures on printed pages 13–14, 309–312, 377–378, 383–384 and 416. Original contributor credits on printed pages 769–770 identify Terex Roadbuilding, National Highway Institute and Volvo Construction Equipment for the relevant source illustrations; those credits accompany the redraws.

The occupational outline sets the training scope; the handbook supplies technical reading; the actual contract and identified machine manuals supply applicable requirements. The six authored Line A classroom units and the new conceptual lessons are not a completed set of all 68 technical units. Qualified technical review, local delivery agreement and practical assessment are recorded separately in the [program status register](../line-a/competency-status.md).

## APA reference

Asphalt Institute. (2007). *The asphalt handbook* (7th ed., MS-4). ISBN 978-1-934154-27-4. [Local complete reader](index.html).

[Validation and known limitations](VALIDATION.md) · [Return to asphalt curriculum](../README.md)
