# Technical source map and edition boundaries

The original document is [2006 Design Build Standard Specifications for Highway Construction](../sources/design_build_standard_specs_2006.pdf), adopted **20 February 2006**, published by the **British Columbia Ministry of Transportation, Construction and Maintenance Branch**. The user supplied this 441-page file on 29 October 2026. The original PDF bytes are preserved; [source-metadata.json](source-metadata.json) and the [source-library manifest](../sources/manifest.json) record its hash, size and metadata.

The cover is the edition authority used here. The catalogue page describes an ongoing annual publication and is not evidence that this file is a different year's edition. The cover's month spelling is normalized to February in authored prose. No current public edition, project adoption or amendments have been verified for this file.

## Exact reading locations

PDF page numbers are one-based file-viewer pages. Printed pages restart within sections. Use both numbers when sharing a location.

| Selected content | Exact location | PDF page | Printed footer | Curriculum use |
|---|---|---:|---|---|
| Title and adoption date | Cover | [1](../sources/design_build_standard_specs_2006.pdf#page=1) | Unnumbered | SP-01 edition and provenance |
| General Description of Work | 501.02 | [284](../sources/design_build_standard_specs_2006.pdf#page=284) | Section 501, 1 of 13 | SP-02 high-level descriptions |
| Gradation Limits | 501.15.01; Table 501-E | [286](../sources/design_build_standard_specs_2006.pdf#page=286) | Section 501, 3 of 13 | SP-03–05 Medium Asphalt Mix selected rows |
| Grading Curve and four-test mean | 501.15.03, continuing onto next page; Table 501-F and following paragraph | [286–287](../sources/design_build_standard_specs_2006.pdf#page=286) | Section 501, 3–4 of 13 | SP-06–07 moving mean and both constraints |
| Sample Mean definition | 502.03.05 | [297](../sources/design_build_standard_specs_2006.pdf#page=297) | Section 502, 1 of 22 | Arithmetic vocabulary; no transfer of Section 501 acceptance rules |
| Lot definition | 502.03.07, continuing onto next page | [297–298](../sources/design_build_standard_specs_2006.pdf#page=297) | Section 502, 1–2 of 22 | Distinguish ten-load monitoring from an acceptance Lot |
| Sub-Lot definition | 502.03.08 | [298](../sources/design_build_standard_specs_2006.pdf#page=298) | Section 502, 2 of 22 | Additional context only; no sampling exercise |
| Quality Management Records | 502.04.04 and continued five-item list | [299–300](../sources/design_build_standard_specs_2006.pdf#page=299) | Section 502, 3–4 of 22 | SP-08–09 delivery fields and ten-load calculation frequency |
| Determination of Material Application Rate | 502.14.01 | [309](../sources/design_build_standard_specs_2006.pdf#page=309) | Section 502, 13 of 22 | SP-10–13 delivered mass divided by covered area |
| Base Preparation | 503.01, opening sentence | [319](../sources/design_build_standard_specs_2006.pdf#page=319) | Section 503, 1 of 1 | SP-02 high-level description only |
| Cold Milling Scope | 511.01 | [339](../sources/design_build_standard_specs_2006.pdf#page=339) | Section 511, 1 of 1 | SP-02 high-level description only |

## Keep the technical boundaries intact

**Section 501 and Section 502 are distinct specifications.** The grading exercise uses the Section 501 Medium Asphalt Mix limits and the stated four-test mean tolerance. The delivery exercise uses Section 502's record fields and dimensional relationship. It does not combine the two into an acceptance procedure.

**Six table rows are a selection.** SP-03–05 uses six Medium Asphalt Mix rows from Table 501-E. The original table contains other rows and mix columns. SP-07 demonstrates why a mean can be close to a curve while outside an applicable grading interval. Neither exercise establishes complete material compliance.

**A ten-load calculation is not a Lot designation.** Clause 502.04.04 gives a minimum calculation frequency of every ten loads. Clause 502.03.07 defines acceptance/payment Lots differently for different properties. Its daily-production definition includes criteria and provisions for shorter production. The workbook's ten loads over 90 minutes do not establish those criteria. No historical payment/rejection band is applied to the fictional check block.

**The target and corrections are invented.** The 200 kg/m² target, all loads, grading results, curve values, station references, times, dimensions and correction card are classroom inputs. The 2006 document does not prescribe that target for this exercise. The extra version/checker fields, role rotation, form test and access-change card are ACCESS teaching design.

**The process cards are descriptions.** Clauses 503.01 and 511.01 support vocabulary and the explicitly given scenario order, not a complete construction sequence, milling procedure or operational threshold. Real work depends on the governing project documents, equipment instructions and authorized supervision.

## Verification and next review

Selected Table 501-E and 501-F values and the Road Checker's Summary/application-rate clauses were checked against rendered source PDF pages, not only text extraction. The automated verifier checks the preserved PDF hash, selected transcription, datasets, worked arithmetic, activity IDs, local assets and generated documents. Its success does not substitute for technical sign-off or a classroom pilot.

Before a delivery team extends this module into current project training, identify the actual specification and amendments, have a qualified reviewer check the proposed technical use, confirm accessible delivery arrangements, then pilot the learning sequence and record changes. Do not infer current contractual authority from the document being available in the source library.

## Source figures and editable diagrams

Figure S1 reproduces Table 501-E from PDF286 as a faithful crop. Figure S2 joins two separately labelled crops from PDF299–300 so the clause introduction and complete list can be read together. The [crop manifest](crop-manifest.json) records exact coordinates, printed/viewer pages, source hashes and output hashes. Regenerate them with `tools/build_source_crops.py`; the original PDF is never modified. The source-excerpts page includes the complete table as text and the delivery paragraph/list transcript.

The five SVGs remain original ACCESS IS4S illustrations. The document-address and two-constraint diagrams use historical identifiers or limits and now credit those exact locations. Passing-mass, area-plan and revision-trail illustrations identify their fictional classroom data. The books provide APA figure notes and full source references.
