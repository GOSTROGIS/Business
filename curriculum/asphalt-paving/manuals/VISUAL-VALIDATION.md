# Manual visual integration · Validation record

**Checked 29 October 2026.** This record covers the authored manual-reading lesson and its visual additions. Qualified technical review and classroom piloting remain pending.

## Delivered learning material

- All nine existing MAN-01–09 activities and their separate answer guidance remain.
- Four new VIS-01–04 practices add source-based component vocabulary, material-route explanation, a model/fuel correction and dimension-table calculations.
- The learner book contains **12 pages** and **four image placements**. The teaching and answer book contains **five pages**.
- Four cropped figures have APA-style notes and full references; source hashes, page labels and exact crop rectangles are in `assets/figure-manifest.json`.
- Accessible text reproduces all twelve paver component names, six selected roller component names and all twelve metric dimension rows used in the lesson.

## Source and alignment checks

The eight source entry files in `manifest.json` retained their recorded checksums. Each crop was compared pixel-for-pixel with an independent render of the recorded original page region at 216 dpi; all four matched. The full photo/figure caption was inspected where included, all source callouts remain visible, and the dimension diagram retains its complete associated table.

Paver labels 7, 10, 11 and 12 were checked against LeeBoy Figure 3-1 and its table (PDF 43 / printed 3-7). Roller callouts were checked against Multiquip Figure 4 and its following component descriptions (pages 14–15). The engine correction was checked against the AR13HA/AR13HAR cover and page 12. Dimension values and arithmetic were checked against MRH800GS page 12: 2 × 346 = 692 mm; 692 mm = 0.692 m; 1,990 − 1,170 = 820 mm; 700 − 692 = 8 mm.

The instructor's mapping was checked against the supplied trade outline: A1 PDF 22 / printed 20; A3 24 / 22; I2 72 / 70; J1 84 / 82; L1 95 / 93. Component vocabulary maps to **J1**, not J2. Supporting dimension practice does not replace L1's specific drum-width/weight requirement. Neither these figures nor the short vocabulary practices complete the later technical units.

## Output checks

- Both final PDFs opened with strict pypdf parsing and PyMuPDF; all thirteen activity IDs appeared in both books, every page had substantive text, and all four learner figures were embedded.
- Both PDF link sets were checked for temporary localhost addresses; none remained.
- The learner, instructor and index pages were checked at **320, 390 and 1280 pixels**. All nine page/viewport cases had no document-width overflow, failed image loads or JavaScript errors. Every image had alternative text and every learner figure had its credit immediately beneath it.
- Figure pages and the mobile paver figure were visually inspected for readable labels, complete crops and intact captions. A larger-image link and complete-source-page link accompany each picture; the portrait dimension image also has a text table.
- All local links in the three generated reading/index pages resolved. The rebuilt ZIP passed CRC/path checks, and every packaged file was compared byte-for-byte with its repository counterpart.

The tests check faithful extraction, page rendering, navigation, calculations and authored answer consistency. They do not establish manufacturer approval, equipment applicability, external assessment validity or completed technical competence.
