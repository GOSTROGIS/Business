# Asphalt study textbook · Volume 1

A standalone illustrated study volume for ACCESS IS4S: **roadbuilding foundations and safe work**, following **A1–A6 and B1** of the SkilledTradesBC Asphalt Paving/Laydown Technician outline. Readings, trade vocabulary, worked examples, individual and group practice, and answer guidance are included.

- **[Read the study textbook](study-textbook.html)** · **[Download the textbook PDF](study-textbook.pdf)**
- **[Worked answers](answers.html)** · **[Answer-guide PDF](answers.pdf)**
- **[Interactive Cedar plan desk](plan-desk.html)** — inspect fictional map records, switch revisions, check quantities and export a study note.
- [Chapter coverage and delivery record](coverage.html)
- [Figure credits](figure-register.html) · [Figure data](figures.json) · [Complete image inventory](image-inventory.json)
- [CONSULTING reuse record](provenance/consulting.json) · [Verification](VALIDATION.md)

This is the 30 October 2026 classroom development edition. Qualified technical review and classroom pilot are pending. B2–L6 remain to be authored in later study volumes; the [68-competency source audit](../readiness/coverage.html) and [remaining acquisition requirements](../readiness/gaps.html) track that work.

## Chapters

1. [The industry and its work](01-industry-evidence.html)
2. [How roads changed](02-history.html)
3. [Materials, machines and placement](03-technology.html)
4. [Working in a paving team](04-workers.html)
5. [Read road documents and quantities](05-road-documents.html)
6. [Investigate a paving trend](06-trends.html)
7. [Recognize hazards and prepare for safe work](07-safe-work.html)

The editable Markdown chapters are the teaching source. All nine Skills for Success are integrated with individual evidence. Visuals include MS-4 source crops and redraws, manufacturer component pictures, official WHMIS symbols, original SVGs and an actual screenshot of the offline plan desk. Every figure carries a source or original-art credit.

## Build and maintain

Use the repository's Python requirements and Chromium. From the repository root, run the scripts in `curriculum/asphalt-paving/textbook/tools/`: `draw.py`, `build_desk.py`, `export.py --desk-only`, `prepare_figures.py`, `build.py`, `export.py`, then `verify.py`. Keep figure captions with the artwork. The source/library paths remain relative to this folder so the complete repository can be used offline.

The five imported CONSULTING documentation snapshots are unchanged, pinned by commit and Git blob identity. The learning desk and illustrations use entirely fictional geometry; no real property, utility, student or client dataset is included.
