# ACCESS IS4S · Skills for Success

[Download the learner textbook](learner-textbook.pdf) · [Download the practitioner guide](practitioner-guide.pdf) · [Preview the visual edition](visual-sampler.pdf)

[Read the learner book](learner-textbook.html) · [Read the practitioner book](practitioner-guide.html) · [Explore the diagrams](VISUALS.md)

**Edition 3 · 29 October 2026**

Two complete ACCESS Indigenous Skills 4 Success books bring the nine skills into learning, work and community life in British Columbia. Each skill chapter contains a usable process, illustrated explanations, worked examples, complete practice documents and new tasks. The practitioner guide provides teaching routines, full cases, answer guidance and observation tools.

## Start with a useful purpose

Use [Start here](learner/00-start-here.md) to choose a goal and agree useful supports. Every skill chapter offers a way into the work, followed by practice and a new opportunity to apply it. Keep evidence of the action you completed and use feedback to decide the next step.

| Skill | Learner chapter | Teaching and practice |
|---|---|---|
| Reading | [Find, connect and evaluate information](learner/01-reading.md) | [Teach Reading](practitioner/03-reading.md) |
| Writing | [Write for a reader and a purpose](learner/02-writing.md) | [Teach Writing](practitioner/04-writing.md) |
| Numeracy | [Find quantities and check the result](learner/03-numeracy.md) | [Teach Numeracy](practitioner/05-numeracy.md) |
| Digital | [Use tools and keep a useful record](learner/04-digital.md) | [Teach Digital](practitioner/06-digital.md) |
| Problem solving | [Compare options and test a decision](learner/05-problem-solving.md) | [Teach Problem solving](practitioner/07-problem-solving.md) |
| Communication | [Receive, explain and check meaning](learner/06-communication.md) | [Teach Communication](practitioner/08-communication.md) |
| Collaboration | [Contribute to a shared result](learner/07-collaboration.md) | [Teach Collaboration](practitioner/09-collaboration.md) |
| Adaptability | [Adjust a plan and try again](learner/08-adaptability.md) | [Teach Adaptability](practitioner/10-adaptability.md) |
| Creativity and innovation | [Develop, test and improve an idea](learner/09-creativity-innovation.md) | [Teach Creativity and innovation](practitioner/11-creativity-innovation.md) |

Bring the skills together in the [integrated projects](learner/10-integrated-projects.md) and select work for your [portfolio](learner/11-reference-and-portfolio.md). The chapters retain 174 core activities and add fresh practice across all nine skills. New exercises and their teaching guidance are integrated into the books.

## Tools for practice and teaching

- [Digital practice desk](teaching/digital-lab/index.html): edit a fictional record, inspect a review copy, save/reopen versions and download evidence. Recipient and access settings are explicitly simulated.
- [Plan a session and collect evidence](practitioner/14-delivery-and-review.md): prepare materials, schedule individual turns, record supports and organize the next attempt.
- [Roadbuilding foundations](../asphalt-paving/line-a/README.md): asphalt industry evidence, history, material flow, worker expectations, road documents and developments.
- [Answer guidance](answers/01-reading.md): use the practitioner book's complete answer sections and the fresh-case keys within its skill chapters.

Learners can work with the supplied fictional cases or choose an appropriate example. Personal history and cultural knowledge are voluntary contributions. Local people direct any Nation-specific knowledge, language or protocols they choose to bring into the learning.

## Visuals and reading formats

The books use custom SVG illustrations, technical diagrams, annotated documents and four contextual illustrations. The colours and typography follow the ACCESS Numeracy Hub. Diagrams remain sharp when enlarged; reading pages offer a visual viewer and text descriptions. Printed contents identify chapter destinations, and response pages provide space to write.

GitHub previews the PDFs and Markdown. Serve the repository locally or host its static files to use the HTML reading pages and Digital practice desk.

## Editing and rebuilding

Editable chapters contain the full teaching content. Managed practice blocks come from the authoring files listed in [teaching-manifest.json](teaching-manifest.json); [visuals-manifest.json](assets/visuals-manifest.json) controls figure placement. The builder integrates those blocks before producing the books and reading pages.

```sh
python -m pip install -r curriculum/skills-for-success/tools/requirements.txt
python curriculum/skills-for-success/tools/build_books.py
python curriculum/skills-for-success/tools/verify_books.py --require-generated
```

Chromium must be installed. Set `IS4S_CHROMIUM_PATH` to another Chromium executable if necessary. `--html-only` builds the reading pages without PDF export. The tools use bundled fonts and a temporary local server; PDF links resolve to repository documents or exact book pages.

[Validation](VALIDATION.md) · [Edition 3 implementation record](IMPLEMENTATION.md) · [Editorial research and provenance](research/online-research.md) · [28 October review](research/book-gap-analysis-2026-10-28.md)
