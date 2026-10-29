# Roadbuilding foundations · Validation record

Checked 29 October 2026. This record describes editorial, arithmetic, file and presentation checks. Qualified technical review and classroom pilot remain pending; the blank sign-off record is in [technical-handoff.md](technical-handoff.md).

## Authored scope

- Six self-contained teaching units with 37 learner activities and 37 separate keyed answer rows.
- Thirty-three locally authored learning-task criteria: A1.6, A1.8 and A1.9, plus every A2–A6 task (5, 6, 9, 5 and 5 respectively). The existing introductory A1 packet covers the earlier introductory sequence; this book does not claim 39 complete occupational assessments.
- All 68 occupational competencies appear in the status CSV and readable status map. Later occupational work is distinguished from authored classroom work. No practical assessment or technical approval is prefilled.
- Twenty curated public evidence records, including dated official B.C. industry data, applicable-document examples, public project funding and bounded material-recovery evidence. Nine Statistics Canada source rows retain the title, raw reference-period field, measure and classification.
- Two stable explanatory SVGs: material flow and conceptual road cross-section. Neither supplies design dimensions, operating settings or acceptance thresholds.

## Automated checks

Run from the repository root, with Markdown, Playwright and pypdf installed according to the existing tooling requirements:

```sh
python curriculum/asphalt-paving/tools/build_line_a.py
python curriculum/asphalt-paving/tools/verify_line_a.py --require-generated
```

The final verifier passes **276 checks with zero errors**. Checks cover activity/key correspondence, all 33 learning-task codes, all 68 competency codes and pending-review fields, evidence-record structure and retained hash formats, Statistics Canada row scope and totals, 23 independent Decimal arithmetic calculations, expected answer-key results, local HTML links, both readable PDFs, all activity IDs in both PDFs, and absence of local-workspace or localhost PDF links. Hash-format checks do not independently re-download a source; retrieval provenance remains in the research register.

The learner PDF has **28 pages**. The teaching and answer guide has **17 pages**. Generated reading pages include the standalone index, eight learner sections, six answer chapters, the technical handoff, and the two combined books: **18 HTML pages**.

## Browser and visual checks

All 18 HTML pages were opened through a local HTTP server in Chromium at widths **320, 390 and 1280 pixels**: **54 page/viewport checks passed**. No document-level horizontal overflow was detected. Every displayed image loaded. All table header cells have a column scope. Tables have keyboard-focusable scrolling regions where narrow screens require them. These checks are not a complete accessibility audit.

Rendered PDF samples were visually inspected for learner source/quantity pages, the material-flow diagram, the road cross-section, the first answer table and the closing review record. The final material-flow and cross-section figures are legible, fully contained and paired with their explanatory text. Table text, numerical units and footer/page numbering are readable; source/reference and technical-handoff spacing was corrected before the final rebuild. No clipped content was identified in the inspected samples. This is sampled visual review, not a claim that every printed page was manually inspected.

## Skills for Success evidence

| Skill | Concrete opportunity |
|---|---|
| Reading | LA1-01 identifies publisher, period, measure and scope |
| Writing | LA1-01 produces a checked industry note |
| Numeracy | LA5-04 checks units, geometric quantities and records |
| Digital | LA1-02 retrieves, saves and reopens a source record on a device |
| Problem Solving | LA1-05 separates supported comparison evidence from missing inputs |
| Communication | LA4-04 uses an accurate handover and check-back |
| Collaboration | LA5-06 rotates checking responsibilities and records individual evidence |
| Adaptability | LA5-05 revises quantities after a documented change |
| Creativity and Innovation | LA6-03 develops useful questions for a product enquiry |

The tasks preserve individual evidence, support used, revision and next practice. A paper plan does not substitute for observed digital use. Group membership alone does not demonstrate collaboration.

## Open delivery and technical questions

The IUOE provider's published **140 accumulated hours** statement is verified as a provider-page statement. It does not resolve the relationship with the historical **120 technical hours**, the regulator's current pathway, or an ACCESS cohort agreement. The proposed classroom sequence totals **555 minutes / 9 hours 15 minutes** and is not a technical-credit allocation.

A1.9 uses real documented recovery pathways and a complete fictional comparison brief. No matched project life-cycle ranking, emissions percentage or environmental winner is invented. Statistics Canada's 427 observations are statistical locations with employees, not unique employers or workers. The supplied 2006 specifications explicitly define **EPS as End Product Specification** in [502.03.01, PDF 297](../sources/design_build_standard_specs_2006.pdf#page=297). That document meaning is confirmed; the historical outline A1 label’s intended relationship and current provider context still need confirmation. Expanded polystyrene is the separate geofoam meaning. The supplied-document reference does not change the count of 20 public-web evidence records. Site-specific specifications, licensing, equipment procedures and practical competence need qualified review and the appropriate current records before workplace use.
