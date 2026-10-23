"""Build an eight-page visual preview from the current complete PDF books."""
from pathlib import Path
import json
import re
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, NameObject

ROOT = Path(__file__).resolve().parents[1]
SELECTIONS = [
    ('learner-textbook', None, 'Redesigned nine-skills cover'),
    ('learner-textbook', 'Six parts of a useful reading process', 'Reading component map'),
    ('learner-textbook', 'Whole packs → the complete order', 'Whole packs and the complete order cost'),
    ('learner-textbook', 'Test the fit in both directions', 'Dimensioned board, margins and card layout'),
    ('learner-textbook', 'Six equipment cards. Different roles.', 'Equipment roles and the screed component'),
    ('learner-textbook', 'Revise the plan without losing the goal', 'Original and revised time plan'),
    ('practitioner-guide', 'Build a cause map from evidence', 'Evidence-led fishbone diagram'),
    ('practitioner-guide', 'Anatomy of a fictional classroom draft', 'Annotated email specimen'),
]


def normalize(text):
    return re.sub(r'\s+', ' ', text).strip().casefold()


def build_sampler():
    readers = {name: PdfReader(ROOT / (name + '.pdf')) for name in {row[0] for row in SELECTIONS}}
    texts = {name: [normalize(p.extract_text() or '') for p in reader.pages] for name, reader in readers.items()}
    writer = PdfWriter()
    selections = []
    for book, phrase, label in SELECTIONS:
        hits = [0] if phrase is None else [i for i, text in enumerate(texts[book]) if normalize(phrase) in text]
        if len(hits) != 1:
            raise ValueError(f'Expected one visual preview page for {phrase!r}: {hits}')
        index = hits[0]
        page = writer.add_page(readers[book].pages[index])
        # This preview is an excerpt; keep external links, not destinations to omitted pages.
        if '/Annots' in page:
            page[NameObject('/Annots')] = ArrayObject([ref for ref in page['/Annots']
                if ref.get_object().get('/A', {}).get('/S') == '/URI'])
        writer.add_outline_item(label, len(writer.pages) - 1)
        selections.append({'book': book + '.pdf', 'page': index + 1, 'label': label})
    writer.add_metadata({'/Title': 'ACCESS IS4S — Visual teaching preview', '/Author': 'ACCESS IS4S curriculum development', '/Subject': 'Eight selected pages from the current complete learner and practitioner books'})
    with (ROOT / 'visual-sampler.pdf').open('wb') as stream:
        writer.write(stream)
    (ROOT / 'visual-sampler.json').write_text(json.dumps({'pages': selections}, ensure_ascii=False, indent=2) + '\n')
    return len(writer.pages)


if __name__ == '__main__':
    print(f'Built visual-sampler.pdf ({build_sampler()} selected pages)')
