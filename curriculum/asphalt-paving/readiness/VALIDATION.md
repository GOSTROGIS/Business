# Validation · 30 October 2026

The complete source audit and collection passed verification. [Detailed source checks](verification.json), [PDF phase](pdf-page-checks.json), [browser checks](browser-checks.json) and [ZIP checks](archive-checks.json) preserve the results.

- **41 PDF publications / 3,240 pages / 161 parts:** original and derived hashes, contiguous ranges, page counts, dimensions, extracted source text and every-page rendering checked. Parts are at most 25 pages and 10 MiB; the largest is 9,193,895 bytes. Three parts of the 2025 Volume 2 specification required unused-resource cleanup without image resampling.
- Every source page was visually compared at 36 dpi. Two comparisons were rechecked at 100 dpi and matched exactly. NIOSH source page 74 extracts alternate/caption text differently after splitting; its visible page matches at 100 dpi and the original source extraction remains in the text file. This is explicitly recorded rather than treated as exact text-layer identity.
- **30 web articles / 33 figures:** original HTML hashes, complete selected article text, local figures and hashes checked. Original extracted text files match exactly. Re-parsing Part 3 merges some whitespace/text-node boundaries; all non-whitespace characters remain in their original order.
- **1,218 local HTML targets** resolve. All 68 competencies and 32 tool/equipment groups have source records and remaining requirements.
- **12 browser cases:** index, visual guide, tool register, coverage, gaps and Part 15 at 390 px and 1280 px; no horizontal page overflow or JavaScript errors. PDF text search and category filtering work. The illustrated PDF is 11 pages; the official signal image and its credit remain together.
- **Eight ZIPs:** seven PDF volumes plus the web/guide volume, each below 40 MiB. All 161 PDF parts occur exactly once across the PDF volumes. CRCs, archive/source hashes, member counts and 957 offline HTML targets passed. Publisher and cross-collection links require internet as stated in each pack.
- The existing asphalt material verifier passed **827 checks**. The refreshed context verifier passed with **321 paths, 320 unique PDFs, 7,759 pages and 377 chunks/texts**. It directly reuses 161 new parts, 88 CAT parts and 34 MS-4 parts; 108 representative render checks and 2,256 URI-link checks passed.
- Current official SkilledTradesBC outline/profile downloads are byte-identical to the existing repository copies. The original documents were not edited.

Qualified technical approval, classroom pilots, complete later technical units and practical delivery are not claimed by these file/content checks. The [gap register](gaps.html) retains the exact remaining course-publication, fleet, instrument and site requirements.

## Post-textbook status update

A1–A6 and B1 now point to the standalone study volume. The generated competency/gap pages and web/guide ZIP have been refreshed. [Post-update checks](post-textbook-checks.json) confirm 1,219 local HTML targets; all eight ZIP CRCs/hashes, all 161 PDF parts exactly once and 957 offline HTML targets pass. Source PDFs and their previously verified page fidelity are unchanged.
