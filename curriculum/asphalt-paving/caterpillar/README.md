# CAT equipment library and parts identification

**ACCESS IS4S · acquired and checked 30 October 2026**

[Search all publications](index.html) · [Visual parts atlas](parts-atlas.html) · [Atlas PDF](parts-atlas.pdf) · [ZIP volumes](downloads.html) · [WHMIS and machine warnings](../whmis/index.html)

The collection preserves **22 publications, 1,883 original pages and 88 native PDF parts**. Every part is at most 25 pages and 10 MiB; the largest is 9,223,322 bytes. Covers, notices, tables, illustrations and blank pages remain. Images were not downsampled. Whole-source URLs, SHA-256 fingerprints, publication dates, document types, model scopes and part ranges are recorded in [manifest.json](manifest.json).

The [parts atlas](parts-atlas.html) presents **20 manufacturer illustrations and 89 named components**, including every numbered callout in the selected conveyor, cold-planer track and roller-control diagrams, and every lettered pin in the selected loader linkage diagram. Large images, typed legends, plain-language functions and adjacent source credits make the diagrams usable in class. Full pages and model tables remain one click away. Supporting-machine table pages retain their original headings and qualifiers.

[Ten identification tasks](practice.html) · [Learner PDF](practice.pdf) · [Answers and observation guidance](teaching-guide.html) · [Teaching PDF](teaching-guide.pdf) · [Component CSV](component-register.csv)

All nine Skills for Success have observable evidence across CAT-ID-01–10. The tasks develop vocabulary and document use for A1/A3 and later I2 paver, J1 screed and L1 compaction-equipment study. They do not constitute complete later technical units or equipment-operation assessment. The WHMIS material provides selected B1 safety-orientation preparation.

## Direct ZIP downloads

Extract a whole volume and open its `index.html`. Each listed publication is complete within its volume.

| Volume | Size | Original pages | Publications |
|---|---:|---:|---|
| [Volume 01](downloads/cat-library-volume-01.zip) | 31.74 MiB | 300 | CAT-01 |
| [Volume 02](downloads/cat-library-volume-02.zip) | 26.72 MiB | 284 | CAT-02, CAT-03 |
| [Volume 03](downloads/cat-library-volume-03.zip) | 23.00 MiB | 333 | CAT-04, CAT-05, CAT-06, CAT-07, CAT-08, CAT-09 |
| [Volume 04](downloads/cat-library-volume-04.zip) | 33.79 MiB | 966 | CAT-10, CAT-11, CAT-12, CAT-13, CAT-14, CAT-15, CAT-16, CAT-17, CAT-18, CAT-19, CAT-20, CAT-21, CAT-22 |

## What is included

- Asphalt paving, asphalt compaction and soil compaction application guides.
- F Series large-paver handbook, Paving By The Numbers and a one-page Milling By The Numbers quick reference.
- Current retrieved paver/screed, cold-planer and reclaimer/stabilizer parts reference guides; the cold-planer edition is May 2026.
- Two complete model-specific roller operation and maintenance manuals: M0130633-02 and KEBU7520-08.
- Grader, backhoe, articulated truck, skid steer/compact track loader, small and medium wheel loader, mini excavator, dozer and hammer parts references.
- A Cat dealer attachment-operations guide and the 588-page Caterpillar Performance Handbook, Edition 50.

**A parts reference guide contains selected service and wear parts. It is not the complete serial-specific parts catalogue.** The [coverage record](coverage.md) identifies the remaining machine-identity and full-manual needs. Each document card states exactly what kind of publication it is; a quick reference or application handbook is not presented as a complete operation manual.

## Provenance and editing

The catalogue pins the original downloaded bytes and source URL. Most files come from Caterpillar or authorized Cat dealer websites; the two roller manuals' public host locations are recorded individually. The CB E-Series manual is a manufacturer publication supplied through a third-party public CDN. This provenance does not establish applicability to a particular training machine.

Original publication notices remain in the native PDFs. Public access does not imply an open licence. Cropped figures carry APA-style author/date/title/publication/page credits. [atlas.json](atlas.json) records source hashes, exact crop rectangles, output hashes and component legends. The instructional explanations are authored ACCESS prose; they do not replace the source operating instructions.

PDF page numbers in this collection are one-based viewer pages; printed labels can differ. Native part links use part-local viewer pages. Split parts omit internal/non-URI page-link annotations and retain external URI links; small whole originals retain their native navigation. The source download URL remains available. Search text is a navigation aid, and image-only pages may have no extracted text.

## Rebuild

From the repository root, with the asphalt Python requirements installed:

```sh
python curriculum/asphalt-paving/caterpillar/tools/build_collection.py --downloads /path/to/downloads
python curriculum/asphalt-paving/caterpillar/tools/prepare_atlas.py --downloads /path/to/downloads
python curriculum/asphalt-paving/caterpillar/tools/build_classroom.py
python curriculum/asphalt-paving/caterpillar/tools/export_pdfs.py
python curriculum/asphalt-paving/caterpillar/tools/package_downloads.py
python curriculum/asphalt-paving/tools/build_context.py
```

Use the catalogue's exact `download_filename` and `source_url` to retrieve each original into the supplied download directory. Changed source hashes require review, not silent replacement. Chromium is needed for PDF export. The exporter starts a temporary loopback server. The package builder creates self-contained ZIP volumes below 45 MiB and a WHMIS classroom ZIP. Each ZIP includes local navigation and source records.

[Validation record](VALIDATION.md)

To verify: run `tools/verify_sources.py --downloads /path/to/downloads` with Python. Serve the repository with `python -m http.server 8765 --bind 127.0.0.1` in another terminal, then run `tools/verify_classroom.py`. The context library has its own `../tools/verify_context.py`. Paths here are relative to this collection; use repository-relative paths when running from the repository root.
