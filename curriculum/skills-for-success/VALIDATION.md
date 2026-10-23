# Build and content validation

Validated **23 October 2026** for the second ACCESS IS4S visual teaching edition. These checks establish source coverage, internal consistency and artifact integrity. Instructor pilot, learner feedback and local Indigenous community review remain delivery work; the materials do not claim those reviews have occurred.

## Delivered books

| Artifact | Pages | Contents |
|---|---|---|
| [Learner textbook](learner-textbook.pdf) | 129 | 12 chapters including the nine skills, two integrated projects, reference and portfolio. |
| [Practitioner guide](practitioner-guide.pdf) | 185 | 13 teaching chapters, 10 answer sections and three research/reference sections. |

Both PDFs contain selectable text, tagged structure, bookmarks and clickable contents. Their source HTML and individual chapter reading pages are committed alongside editable Markdown. Chromium generated the PDFs using bundled fonts. PDF links to companion chapters resolve to actual PDF page numbers; source-document links preserve their page targets. Temporary localhost URLs are removed from PDF annotations.

## Coverage and content review

- All **148 source pages** are accounted for in the page inventory and nonoverlapping section crosswalk. The source PDF SHA-256 remains `32dad4699b1ef1ab281ad4bdf95bef310048741703fc401094c57f6c62e33caf`.
- All **nine skills and 54 components** are mapped to actual learner activities. Each skill chapter supplies **18 numbered activities**, with corresponding answer guidance. The two integrated projects add **12 activities**, for **174 matched activity/answer pairs**.
- The practitioner guide accounts for **six teaching approaches, 27 instructional strategy groups, 27 grab-and-go patterns, three appendix lessons, six historical professional-development listings and 122 indexed bibliography entries**. Outside bibliography works are distinguished from sources actually read.
- Independent chapter review checked task inputs, component opportunities, worked examples, answer alignment and arithmetic. Repairs included missing digital-task inputs and six equipment-purpose cards, receipt/recount fields, journey-time boundaries and realistic Adaptability timing. Reflection prompts allow truthful evidence rather than requiring invented gaps.
- The three integrated practitioner lessons have complete handouts, worked models, answers and **90-minute schedules**. The teaching-approaches chapter also supplies a complete **45-minute sequence**, including the independent changed-date notice pair.
- Independent project review checked both project budgets, revised totals, capacity, rotation feasibility, schedules, activity IDs and response word limits.
- Feedback labels are consistent: Not observed; Not yet demonstrated; Demonstrated with support; Demonstrated independently. Official proficiency levels are not inferred from these local records. Writing, Digital, Communication and Collaboration retain observable evidence appropriate to each skill.

## Visual teaching validation

- **38 unique SVG assets**: 37 newly authored graphics and one attributed vector extraction from the supplied guide. The two covers and 65 body placements provide **67 SVG placements** across the books. Four generated illustrations add fictional human context.
- Every learner skill chapter contains a six-component map and two case-specific diagrams. Matching diagrams appear in the practitioner teaching chapters. Three more diagrams support the two integrated projects and the learning portfolio.
- The canonical visual manifest records **69 body figure placements** with an exact source location, caption and alternative text. All managed blocks occur once per source chapter and once in each intended reading/book output. Reinstalling them is idempotent.
- Independent diagram reviews checked time scales, quantities, costs, measurement intervals, case versions, equipment roles, component labels and capstone boundaries. Text bounds and rendered images were checked; identified label overlaps were corrected before export.
- PDF inspection confirms the graphics remain vectors: the full learner PDF has one raster-image placement and the practitioner PDF has three, matching the four contextual illustrations. All pages contain text. Both PDFs retain their tagged structure, bookmarks and valid companion-book page links.
- The [eight-page visual sampler](visual-sampler.pdf) gives a quick view of the redesigned cover, component map, numerical diagrams, equipment roles, revised timetable, fishbone and annotated email.

## Research and presentation checks

The research ledger contains **15 online source records and 11 search records**, with retrieval status, exact source URLs, supported claims and limitations. Current federal pages and BC institutional resources were inspected; unavailable original pages and unreviewed linked reports are explicitly distinguished. No scraped third-party pages or downloaded research PDFs are redistributed in this directory.

Desktop, tablet and mobile browser checks covered both complete books and their landing page at **390, 768 and 1440 pixels**. All nine combinations loaded bundled fonts and images, produced no page errors or failed requests, and had no page-level horizontal overflow. Wide tables and diagrams remain horizontally scrollable within their own regions on small screens. Figures also link to the full-size asset; SVG labels remain sharp when enlarged.

Visual inspection covered the revised covers, component maps, numerical/technical diagrams, communication and social-skill sequences, projects, practitioner teaching diagrams, source inset and mobile reading. Print checks confirm every PDF page contains body text. Chapter headings begin on new pages; table headers repeat, rows avoid splitting where they fit, and worked examples use the Hub's gold treatment. The bibliography uses a compact reference layout. These checks do not constitute a full assistive-technology or PDF accessibility certification.

## Reproduce the structural checks

```sh
python -m pip install -r curriculum/skills-for-success/tools/requirements.txt
python curriculum/skills-for-success/tools/build_books.py
python curriculum/skills-for-success/tools/verify_books.py --require-generated --report /tmp/is4s-book-verification.json
```

The verifier checks source identity, complete page coverage, component/strategy/activity inventory, paired activity IDs and answer bodies, manifest membership, book titles and chapter presence, local links and fragments, PDF source-page bounds, generated HTML identifiers, nonempty PDF pages, absence of localhost PDF links, all 174 activity IDs in both PDFs, figure placement, image alternative text, captions, SVG accessibility metadata and self-contained SVG resources. It requires at least three SVG figures in each of the nine learner skill chapters. It skips external URL validation because the live research ledger records those checks separately. The script itself was checked against deliberately invalid paths, fragments, page targets and localhost URLs in temporary files.

The build requires Python dependencies and a Chromium executable. `--html-only` supports environments without PDF rendering. The repository retains the supplied source PDFs, original asphalt A1 unit and earlier program research; this expansion adds the foundation books without claiming completion of the full asphalt trade curriculum.
