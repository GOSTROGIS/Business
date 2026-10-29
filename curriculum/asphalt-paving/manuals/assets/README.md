# Manual figures for ACCESS IS4S

Four faithful manufacturer-page crops support the visual practices in the [learner lesson](../lesson.html). They retain the source's actual equipment geometry and labels. Their teaching captions and accessible tables are authored in `lesson.md`; complete answer guidance is in `instructor.md`.

| Figure | File | Original location | Reading purpose |
|---|---|---|---|
| MF-01 | [Paver overview](crops/leeboy-8680-machine-overview.png) | LeeBoy 8680, Figure 3-1; PDF 43 / printed 3-7 | Locate numbered paver and screed components. |
| MF-02 | [Auger-area photograph](crops/leeboy-8680-augers.png) | LeeBoy 8680, unnumbered photograph; PDF 42 / printed 3-6 | Connect equipment terms to the material route. |
| MF-03 | [Roller components](crops/multiquip-ar13-roller-components.png) | Multiquip AR13HA/AR13HAR Rev. 1, Figure 4; PDF/printed 14; legend on 15 | Link a numbered drawing to its following legend. |
| MF-04 | [Dimension diagram and table](crops/multiquip-mrh800gs-dimensions.png) | Multiquip MRH800GS Rev. 10, Figure 1 and Table 3; PDF/printed 12 | Connect a letter, dimension and unit without separating the figure from its table. |

[Figure manifest](figure-manifest.json) records source and image hashes, crop rectangles, original page labels, publication/serial scope, source URLs, alt text, copyright attribution and APA-style reference text. Full formatted APA-style notes accompany each figure in the lesson. Credits identify the source; they do not assert publisher permission or an open licence.

Reproduce the crops from unchanged local source PDFs:

```sh
python -m pip install -r curriculum/asphalt-paving/manuals/tools/requirements-figures.txt
python curriculum/asphalt-paving/manuals/tools/extract_figures.py
python curriculum/asphalt-paving/manuals/tools/build_pack.py
```

The extractor uses PDF coordinates measured from the top-left page corner and renders at 216 dpi. It checks each source checksum before rendering. It does not edit an original, generate missing equipment detail, remove a label or recolour a photograph. The full source pages remain linked beside the crops so readers can recover all surrounding context.

The figure packet introduces vocabulary and document-reading skills. Machine configuration, safe work procedures and qualified practical instruction remain part of the actual technical training. The MS-4 handbook is not represented by these OEM images.
