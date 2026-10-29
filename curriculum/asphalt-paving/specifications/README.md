# Asphalt specifications · Read, calculate, check

**ACCESS · Indigenous Skills 4 Success**

A complete classroom module for interpreting asphalt specification tables, maintaining delivery records and explaining calculations. Eighteen activities connect all nine Skills for Success through a fictional paving-record assignment. Learners work with supplied information, compare evidence, make corrections and explain what still needs confirmation.

- [Learner workbook · PDF](learner-workbook.pdf) · [accessible HTML](learner-workbook.html) · [editable Markdown](learner.md)
- [Teaching and answer guide · PDF](teaching-guide.pdf) · [HTML](teaching-guide.html) · [editable Markdown](instructor.md)
- [Source map and edition boundaries](source-map.html) · [selected source excerpts](source-excerpts.html)
- [Original 2006 specifications · 441-page PDF](../sources/design_build_standard_specs_2006.pdf)
- [Practice data](data/README.md) · [validation notes](VALIDATION.md) · [verification report](validation.json)

The technical reading is selected from the **2006 Design Build Standard Specifications for Highway Construction**, adopted **20 February 2006**, issued by the British Columbia Ministry of Transportation, Construction and Maintenance Branch. Original bytes are preserved. The module uses Section 501 grading tables and Section 502 records and material application calculations, with short process references from Sections 503 and 511. It does not cover all 441 pages.

The numerical test results, loads, dimensions, people and delivery events in the exercises are invented. The table limits identified as Table 501-E or 501-F are transcribed from the historical document. Its current contractual applicability has not been established. Before using a specification on a real project, the responsible project team must identify the governing edition, amendments, design, project conditions and authorized reviewer. Classroom calculations do not authorize mix acceptance, payment decisions or equipment operation.

Two source figures place the original grading table and the Road Checker’s Summary continuation beside the explanations. Their three faithful crops retain headings, units and qualifiers; APA figure notes and the [crop manifest](crop-manifest.json) make the exact source traceable.

## Teaching route

Plan four 90-minute sessions, with flexibility for language, access and prior experience. The teaching guide includes a complete key, worked calculations, a role rotation, independent evidence criteria and a practical next-step record. Timings are an ACCESS teaching proposal, not a trade-program time allocation. A facilitator can act as the partner in a cohort of one.

Use the workbook on paper, in HTML, or as an editable document. The Digital activity requires an actual spreadsheet task; a paper simulation can prepare for that task but does not demonstrate digital performance. Learners may use calculators, read-aloud support, larger print and a scribe where these preserve the skill being observed. No learner is asked to disclose personal information, speak for a Nation or contribute cultural knowledge.

## Build and verify

From the repository root, install the existing asphalt tool requirements with `python -m pip install -r curriculum/asphalt-paving/tools/requirements.txt`. Provide Chromium through `IS4S_CHROMIUM_PATH` or install Playwright Chromium with `python -m playwright install chromium`.

```sh
python curriculum/asphalt-paving/specifications/tools/build_source_crops.py
python curriculum/asphalt-paving/specifications/tools/build_module.py
python curriculum/asphalt-paving/specifications/tools/verify_module.py
python curriculum/asphalt-paving/specifications/tools/check_browser.py
```

The independent builder reads the Markdown, keeps local fonts and SVGs, and generates the two PDFs and five HTML reading pages. The verifier checks the original PDF hash, selected table data, exercise arithmetic, activity coverage, local links, SVG accessibility, PDF links and printed contents-page numbers. Visual inspection and qualified technical review remain separate from these automated checks.
