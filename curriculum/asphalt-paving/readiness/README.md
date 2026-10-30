# Tools, safety and full-outline source coverage

**41 complete PDF publications · 3,240 source pages · 161 small PDF parts · 30 archived web sources · 33 web figures.** Acquired and reviewed 30 October 2026.

[Visual tool and rigging guide](field-guide.html) · [Printable guide](field-guide.pdf) · [Source catalogue](index.html) · [ZIP downloads](downloads.html)

[All 68 competencies](coverage.html) · [32 tool/equipment groups](tools.html) · [Remaining delivery requirements](gaps.html)

This collection audits the entire August 2016 SkilledTradesBC outline, including B1's explicit WorkSafeBC Part 15 requirement and every Section 4 tool. It adds actual documents for rigging, hand tools, propane, air hammers, compactors, measuring instruments, nuclear gauges, traffic control, cargo securement, dust/heat, pits/plants and current highway specifications. Existing MS-4, CAT, WHMIS and 2006 specification collections remain linked from each relevant competency.

## What is included

- WorkSafeBC Parts 1, 3–8, 10–12, 14–16 and 18–20; guidelines for Parts 3, 8, 15 and 18; official crane signals and rigging-failure guidance. The archived regulation articles retain their complete selected text, tables and figures.
- Seymour Midwest's full tool catalogue and actual lute, brace, brush and scraper assembly/parts sheets; CCOHS hand-tool and shovelling information; Lincoln grease-gun instructions.
- Tiger Torch 95-B/445 instructions, propane information, complete Chicago Pneumatic breaker instructions and a CP 1230 parts list, plus a complete Multiquip plate-compactor operation/parts manual.
- ThermoWorks thermometer instructions and measurement diagram, Leica level brochure/data sheet, measuring-wheel guidance, the full Troxler 3430 manual and Canadian CNSC gauge requirements.
- The complete 2020 Traffic Management Manual, both 2025 highway specification volumes and the acquired amendment, 2026 Mines Code, NSC cargo-securement standard and interpretations, utility guidance and environmental regulation/reporting sources.
- Three accessible original SVG diagrams, four credited manufacturer/WorkSafeBC page images, a visual reading guide, source/tool registers and an editable delivery checklist.

Publication types and editions remain explicit. A catalogue is not described as an operating manual, a historical edition is not described as current, and a general regulatory source does not establish applicability to an unknown machine or site. The [gap register](gaps.html) identifies the exact six course manuals, instructor package, fleet-specific manuals, instrument documents, licensed project references and provider records still required.

## Source integrity and use

All 3,240 PDF pages are retained, including covers, contents, notices, multilingual sections and blank pages. Parts are at most **25 pages and 10 MiB**. Native PDF page content is preserved without image downsampling. Three parts of the 2025 Volume 2 specification required lossless unused-resource cleanup, recorded per part. Small whole publications retain the exact acquired bytes. Split parts omit internal/non-URI link annotations that depend on the original whole-document page tree; use the source page ranges to navigate.

Every publication has a pinned original SHA-256 and source URL in [catalogue.json](catalogue.json). The [manifest](manifest.json) records individual parts, page ranges, hashes, text files and archived web figures. Publisher HTML is retained as inert `.source.html.txt`; the readable HTML removes website controls/scripts and localizes images without changing the selected article text. These are dated snapshots; check live requirements before delivery.

Text files are search aids. Inspect the actual source page for technical wording, tables and figures. The Tiger Torch sheet is image-only; the historical BC Hydro handout has defective text encoding. No OCR accuracy is claimed for those pages. The NIOSH source page 74 has a recorded alternate-text extraction variation after splitting; its visible page matches at 100 dpi and its original extracted text is retained. See the [validation record](VALIDATION.md).

The current official SkilledTradesBC outline and profile downloads were checked and are byte-identical to the existing repository originals; [verification record](official-program-check.json). They were not duplicated.

Each PDF ZIP lists its exact source-page ranges. Download all PDF volumes for all 41 publications. The web/guide ZIP contains the full regulatory articles and their local figures; links to PDFs and other curriculum collections open the repository. Extract each volume into its own folder.

## Edit and rebuild

The editable teaching prose is in [field-guide.md](field-guide.md) and [gaps.md](gaps.md). Source mappings are in [coverage-data.psv](coverage-data.psv) and [tools-data.psv](tools-data.psv); their CSV/HTML outputs are generated. Preserve filled provider records in [delivery-checklist.csv](delivery-checklist.csv).

```sh
python -m pip install -r curriculum/asphalt-paving/tools/requirements.txt
python curriculum/asphalt-paving/readiness/tools/build_library.py --downloads /path/to/pinned-downloads
python curriculum/asphalt-paving/readiness/tools/build_diagrams.py
python curriculum/asphalt-paving/readiness/tools/build_guides.py --downloads /path/to/pinned-downloads
python curriculum/asphalt-paving/readiness/tools/export_guide.py
python curriculum/asphalt-paving/readiness/tools/package_downloads.py
python curriculum/asphalt-paving/readiness/tools/verify_library.py --downloads /path/to/pinned-downloads
python curriculum/asphalt-paving/tools/build_context.py
python curriculum/asphalt-paving/tools/verify_context.py
```

The catalogue identifies the exact `.raw` download filename and hash for rebuilding. A changed upstream publication needs review and a deliberate catalogue update. Previously archived web images are reused. Chromium and the existing PDF/text tools must be installed for export and verification.
