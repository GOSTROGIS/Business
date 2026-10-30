# Study textbook verification · 30 October 2026

**Passed:** [detailed book checks](verification.json), [browser and interaction checks](browser-checks.json), and [SVG text-layout checks](diagram-checks.json).

- Textbook: **78 pages**, 60 unique activities, including 23 added activities. Worked-answer guide: **24 pages**. Every activity appears in the textbook and the answer guide, including extracted PDF text.
- **44 image placements / 44 unique files**, with alt text and adjacent figure credits. Thirteen new SVGs include twelve instructional diagrams and cover art. Every original SVG has a title and description; browser geometry checks found no overlapping text or text outside its canvas.
- Source/crop records and asset SHA-256 values checked. Five CONSULTING documentation snapshots match both their recorded SHA-256 and Git blob identity at commit `9e409ba9d5bc28e7da3d400671ec6e7707615613`.
- **559 local targets and 47 HTML fragments** checked. The generated PDFs contain no machine-local URLs, no near-empty pages and no text outside page bounds.
- **16 page/viewport checks** cover eight pages at 390 and 1280 pixels, with no document overflow, broken images, duplicate IDs or browser errors. A seventeenth interaction check verifies revision C quantities, utility-record selection, layer visibility, exported/reopened JSON and operation from a local server with external network requests blocked. Direct `file://` navigation could not be tested because the managed browser blocks that scheme.
- Initial-edition visual inspection included a contact sheet of all 77 textbook pages, the 12 instructional SVGs, the revised cover, WHMIS page and the actual plan-desk screenshot. A label collision found in the rigging diagram was corrected and the books/context index rebuilt. Diagram layout checks then passed for all 13 SVGs.
- The whole-program source map, delivery gap record and offline web/guide ZIP now reflect the new B1 classroom chapter. The seven original PDF ZIP volumes are unchanged. All eight archive CRCs/hashes, 161 uniquely packaged source parts and 957 offline HTML targets pass; 1,219 readiness HTML targets pass.
- Existing curriculum checks remain green: **989 material checks** and **350 Line A checks**. Updated context index: **350 unique PDFs, 9,058 pages and 440 chunks**; 159 representative page-render comparisons and 2,928 retained URI links pass.

The full textbook is about 8.8 MB and the answer guide about 0.2 MB. Context copies split the 78-page textbook into four parts of at most 25 pages, alongside extracted text. Original source manuals remain in their existing verified libraries.

These checks establish the recorded content, file integrity, navigation and layout. Qualified technical approval, classroom pilot, fleet/venue applicability and practical assessment remain pending. The scope is A1–A6 and B1; all B2–L6 classroom chapters are now available in Volumes 2–8.


## Plain-language and AI update

The reading editions now show descriptive activity names and full-width named answer sections. The technology note adds AI creation/audit and audio/video study practice with actual file checks. Updated exports are 78 study pages and 24 answer pages. All 60 activities retain answer guidance. The complete B2–L6 continuation is available in [Volumes 2–8](series/index.html).

The updated full-width answer layout was inspected in the actual PDF; task names and answers remain readable together.
