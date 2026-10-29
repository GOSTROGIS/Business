# ACCESS IS4S visual system

**Edition 3 · 29 October 2026.**

The palette, badge and typography follow the [ACCESS Numeracy Hub](https://github.com/GOSTROGIS/access-trades-numeracy/tree/7c0ceaab485e36aa45c596ac58e43bba63e4f824): warm cream #F7F4F1, ink #1A1512, ACCESS red #D2181F and gold #FFBC00. Archivo headings, IBM Plex Sans text and IBM Plex Mono figures are bundled locally, with Fontsource provenance and licences in fonts/. The badge is preserved unchanged.

## Diagrams lead the teaching

The active teaching library contains **43 unique SVG graphics**: 42 instructional diagrams and one cover learning scene. Of these, **41 appear in the Skills for Success books**, including the cover; two support the roadbuilding lessons. This count excludes badges and the archived figure described below. Every skill has a six-component visual map and two case diagrams. Additional visuals support fraction regrouping, quantity checks, learning routes, practical trials, integrated projects, portfolios and teaching. Four fictional generated illustrations add human context.

The [canonical visual manifest](visuals-manifest.json) controls **77 body placements: 73 SVG placements and four illustrations**. Two SVG placements belong to separately editable teaching materials; the two complete books contain the other **75 body placements: 71 SVGs and four illustrations**. Their covers add two placements of the same cover SVG. Repeated placements let an instructor and learner use the same example without creating additional unique assets. The two roadbuilding diagrams are linked directly from their lesson Markdown, outside this manifest. The smaller manifests in diagrams/ record authoring handoffs; the canonical manifest controls the book figures.

SVGs use explicit labels, shapes, arrows, quantities and meaningful alternative descriptions. They remain vector graphics in the exported PDFs. Rulers and dimensioned drawings teach relationships; they are not calibrated physical measuring tools. Worked visual checks appear after the learner's first attempt where they reveal a solution. For independent assessment, use the changed case or a comparable new task.

The diagrams use the quantities and tasks in their chapters. The portfolio and project diagrams explain the process without supplying the independent capstone decisions. Dark outlines, printed labels and differentiated shapes communicate meaning without relying on colour alone. The [validation record](../VALIDATION.md) identifies the checks actually performed; a design choice alone is not a completed accessibility test.

## Edition 3 teaching graphics

The [cover scene](diagrams/cover-nine-skills.svg) connects a notebook, tablet, revised note and pencil with a clear nine-skill index. The teaching diagrams use concise labels and visible actions: component routes, paired versions, physical quantities, handovers and test cycles.

Four additional book diagrams make specific learning steps visible:

- [Equivalent fractions and regrouping](diagrams/edition3-fractions-regrouping.svg) uses eighths and sixteenths to show addition, mixed-number subtraction and an inverse check.
- [Quantity check](diagrams/edition3-quantity-check.svg) follows 19 needed labels through available stock, three whole packs, a $6.60 cost and two labels remaining beyond the target.
- [Learner route](diagrams/edition3-learner-route.svg) connects a starting task, foundation or core practice, a fresh check and a next step.
- [Prediction and trial cycle](diagrams/edition3-prediction-trial-cycle.svg) separates an observed action from a possible explanation before a keep, adjust or retest decision.

The roadbuilding lessons use a [conceptual cross-section](diagrams/edition3-road-cross-section.svg) showing layers, shoulders, crown and outward surface-water direction, and a [material-flow diagram](diagrams/edition3-material-flow.svg) distinguishing plant production, placement, compaction and separate recycling routes. Neither supplies design dimensions, acceptance standards or operating settings. The [visual index](../VISUALS.md) links all 43 active SVGs and their teaching contexts.

## Archived asset provenance

`diagrams/source-transition-chart.svg` is retained solely as an archived editorial asset. It was extracted from SkillPlan's March 2024 practitioner guide, PDF p.18, with crop `(248, 172, 552, 535)` and text converted to paths. It is **not used in the current books or active visual manifest** and is excluded from the active counts above.

## Original illustrations

Four fictional scenes were generated for this edition using the image-generation tool on 23 October 2026: community learning, comparing notices, writing with reader feedback, and safe tabletop measuring. They depict contemporary adult learning in BC and supply atmosphere and human interaction. Exact mathematical or document content comes from the authored SVGs and text, not incidental marks in these illustrations. The scenes are not documentary photographs or depictions of actual learners.

The scenes do not claim to depict a particular Nation or community. No Nation-specific artwork, cultural pattern, ceremony or sacred symbol is added. Local direction and appropriate permission remain necessary for any proposed Nation-specific teaching content.

## Editing and rebuilding

Edit SVGs directly in a vector editor or as XML. Keep the `viewBox`, `title` and `desc`, and update captions and alternative text in the canonical manifest when a teaching claim changes. `tools/install_visuals.py` installs marked figure blocks in the editable Markdown and preserves all unmarked prose. The book builder invokes it automatically and resolves paths for both complete books and individual reading pages. Re-running the installer does not duplicate figures.
