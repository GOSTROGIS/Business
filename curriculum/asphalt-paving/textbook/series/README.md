# Asphalt study series · Volumes 2–8

[Open all volumes](index.html) · [Learning-task coverage](coverage.html) · [Figure credits](figure-register.html)

All 61 B2–L6 classroom chapters and 218 learning tasks are authored. The series includes 183 chapter activities with worked answer guidance, seven integrated nine-skill cases, a 20-point density quiz and supervised practical observation records. Eight maintenance/shutdown competencies preserve the outline’s 80% checklist requirement; the density quiz preserves 70%. Critical safety failures cannot be offset by a numerical score.

The books use plain-language task names, original SVG explanations, verified manual/MS-4 crops and APA-style figure/source credits. AI literacy is integrated into the digital work: clear briefs, source checks, editable formats, formula inspection, file reopening and study-media verification.

Qualified technical review, actual fleet/site matching, local pilot and observed qualification remain separate from completed classroom authoring. No practical achievement is claimed without observation.

Editable chapter content is in `content/*.json`; readable Markdown and HTML are generated. `volumes.json` contains complete integrated cases. `outline/` retains the exact task wording and source-page record. Build with `PYTHONPATH=/workspace/.is4s-python python tools/build.py` from a configured environment, then use `tools/export.py` and `tools/verify.py`. Source and original figure builders preserve provenance and deterministic SVGs.
