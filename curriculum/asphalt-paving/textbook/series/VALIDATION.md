# Study-series validation · 30 October 2026

All **61 B2–L6 chapters** and **218 outline learning tasks** have authored classroom readings. The seven study volumes contain **383 pages**, with **184 pages** of separate teaching and answer guidance. Together they provide 183 named chapter activities, seven complete nine-skill cases, a five-question density quiz and supervised observation records.

The exact task wording and source pages are preserved in `outline/` and mapped one-to-one in [coverage.csv](coverage.csv). The eight specified maintenance/shutdown checklists retain an 80% minimum; the density quiz retains 70%. Critical safety items must pass regardless of a numerical score. No practical qualification is prefilled.

## Visual and source checks

The books use **84 unique teaching figures across 131 chapter placements**, including **42 new original SVGs**. Manual and MS-4 crops retain page/edition/model information, crop coordinates, hashes and adjacent APA-style credits. Publisher image contributors are retained where identified. Source identity, local targets, HTML fragments, answer coverage, calculation examples and final PDF text bounds are checked by `tools/verify.py`.

All 42 new diagrams passed SVG text-bound and text-overlap checks. Visual review sampled the machine/interface, transport, pneumatic-tool, screed, rolling-coverage and density diagrams, the full new-crop contact sheet and actual pages from all seven study PDFs. Crops were corrected where figure captions or machine details were cut off. The LeeBoy loading crop retains the complete picture and caption; the full applicable loading procedure remains linked. These are bounded visual checks, not an accessibility certification.

Browser checks at 390 and 1280 pixels passed for 13 representative reading/index/answer pages: no page-level horizontal overflow, missing images or duplicate IDs. All 14 PDFs have readable text, contents links, tagged output and outlines; checks found no near-empty pages, out-of-page text or localhost links. Every chapter activity appears in its study and answer PDF.

## Smaller downloads

Each volume has a ZIP containing its study and answer PDFs. The newly acquired Rosco RB50 manual retains all 314 original pages and is also available as 13 native parts, each at most 25 pages and 10 MiB, with an ordered manifest and ZIP. The manual applies to publication 1017258-03 Rev. B, serial 255027 and above; it is not automatically the provider’s machine manual.

## Reproduce

Run `tools/draw.py` and `tools/prepare_figures.py` when figures change, followed by `tools/build.py`, `tools/export.py`, `tools/package.py`, `tools/check_diagrams.py` and `tools/verify.py`. The final run passed **7,440 checks**, including exact rendered-page comparisons for all **314 Rosco source pages**. The split method preserves page transparency groups; internal links to omitted pages are removed, and the full original retains its navigation.

The final [verification report](verification.json), [browser checks](browser-checks.json), [diagram checks](diagram-checks.json) and [PDF inventory](pdf-inventory.json) record the tested artifacts.

Classroom authoring and artifact verification are complete. Qualified trade/provider review, actual fleet/site matching, local teaching pilot and observed practical qualification remain delivery requirements. No such approval or observation is claimed here.
