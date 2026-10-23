# ACCESS IS4S visual system

The palette, badge and typography follow the [ACCESS Numeracy Hub](https://github.com/GOSTROGIS/access-trades-numeracy/tree/7c0ceaab485e36aa45c596ac58e43bba63e4f824): warm cream #F7F4F1, ink #1A1512, ACCESS red #D2181F and gold #FFBC00. Archivo headings, IBM Plex Sans text and IBM Plex Mono figures are bundled locally, with Fontsource provenance and licences in fonts/. The badge is preserved unchanged.

## Diagrams lead the teaching

The visual edition contains **38 unique SVG assets**: 37 newly authored cover, framework, component, case and teaching graphics, plus one vector figure extracted from the supplied guide. Every skill has a six-component visual map and two case-specific diagrams. Additional diagrams support the integrated projects, portfolio and practitioner lessons. Four generated illustrations add human context.

The [visual manifest](visuals-manifest.json) controls 69 source-figure placements: 65 SVG placements and four illustrations. The two covers add two more SVG placements. Matching diagrams appear in the learner chapter and its practitioner companion so an instructor can teach from the same example. The per-author manifests in diagrams/ record the initial component handoffs; the canonical file above controls the actual build.

SVGs use explicit labels, shapes, arrows, quantities and meaningful alternative descriptions. They remain vector graphics in the exported PDFs. Rulers and dimensioned drawings teach relationships; they are not calibrated physical measuring tools. Worked visual checks appear after the learner's first attempt where they reveal a solution. For independent assessment, use the changed case or a comparable new task.

The diagram titles, labels and arithmetic were checked against the chapter cases. The portfolio and project diagrams explain the supplied process without giving away the independent capstone decisions. Dark outlines, printed labels and differentiated shapes keep the diagrams usable in greyscale.

## Source figure and adaptations

`diagrams/source-transition-chart.svg` preserves the original vector geometry of SkillPlan's historical transition chart, *Skills for Success Get Started Guide for Practitioners*, March 2024, PDF p.18. It was extracted from the user-supplied PDF using a page crop in PDF points `(248, 172, 552, 535)` and text converted to paths to preserve typography. The nearby caption and practitioner explanation retain the historical context and qualify the simplified arrows. The guide remains available in the [source folder](../../asphalt-paving/sources/README.md).

The new nine-skills planning map, fishbone and annotated email draw on teaching functions found in the supplied guide; their wording, layout and case data are authored for these books. The [visual audit](../research/visual-audit.md) identifies the original pages and the design decisions. SkillPlan is credited as the source guide's author; Government of Canada funding is distinguished from authorship.

## Original illustrations

Four fictional scenes were generated for this edition using the image-generation tool on 23 October 2026: community learning, comparing notices, writing with reader feedback, and safe tabletop measuring. They depict contemporary adult learning in BC and supply atmosphere and human interaction. Exact mathematical or document content comes from the authored SVGs and text, not incidental marks in these illustrations. The scenes are not documentary photographs or depictions of actual learners.

No Nation-specific artwork, cultural pattern, ceremony or sacred symbol is added. The chapter layouts, line icons, diagrams and pictograms are original. Local direction remains necessary for Nation-specific teaching content.

## Editing and rebuilding

Edit SVGs directly in a vector editor or as XML. Keep the `viewBox`, `title` and `desc`, and update captions and alternative text in the canonical manifest when a teaching claim changes. `tools/install_visuals.py` installs marked figure blocks in the editable Markdown and preserves all unmarked prose. The book builder invokes it automatically and resolves paths for both complete books and individual reading pages. Re-running the installer does not duplicate figures.
