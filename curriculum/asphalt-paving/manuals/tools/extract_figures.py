"""Extract four faithful teaching crops from the locally preserved OEM PDFs.

Run from the repository root:
    python curriculum/asphalt-paving/manuals/tools/extract_figures.py

Requires PyMuPDF. Crop rectangles use PDF points (72 points per inch),
top-left origin. Source files and their page content are never modified.
"""
from pathlib import Path
import hashlib
import json

import fitz

ROOT = Path(__file__).resolve().parents[1]
MANUALS = {d['id']: d for d in json.loads((ROOT / 'manifest.json').read_text())['documents']}
REFERENCES = {
    'OEM-01': 'LeeBoy. (2026). LeeBoy model 8680 commercial paver: Safety and operations manual (Manual No. 1033428-SOP). https://www.leeboy.com/wp-content/uploads/2024/03/1033428-SOP-MANUAL-8680-REV-A_WEB.pdf',
    'OEM-02': 'Multiquip Inc. (2020, June 11). MRH800GS vibratory roller: Operation manual (Rev. 10). https://www.multiquip.com/multiquip/pdfs/MRH800GS_rev_10_ops_manual.pdf',
    'OEM-03': 'Multiquip Inc. (2021, June 18). AR13HA/AR13HAR ride-on tandem drum roller: Operation manual (Rev. 1; serial no. 110301 and above). https://service.multiquip.com/pdfs/AR13HA-R-rev-1-SN-110301-and-above-ops-manual.pdf',
}
SPECS = [
    dict(id='MF-01', file='leeboy-8680-machine-overview.png', source='OEM-01',
         page=43, printed_page='3-7', source_figure='Figure 3-1. Machine Overview',
         bbox=[88, 106, 510, 410], title='Locate the paver components',
         author='LeeBoy', year=2026,
         alt='LeeBoy 8680 paver photograph with the original numbered callouts 1 to 12. Callout 7 identifies the hopper, 10 the screed extension, 11 the end gate and 12 the rubber tracks. The adjacent table gives all twelve names.',
         context='Original numbered photograph and caption retained. Surrounding page and full function table omitted; all twelve component names are supplied in accessible lesson text. Full source page remains linked.'),
    dict(id='MF-02', file='leeboy-8680-augers.png', source='OEM-01',
         page=42, printed_page='3-6', source_figure='Unnumbered photograph above the Augers heading',
         bbox=[40, 89, 288, 247], title='Look at the auger area',
         author='LeeBoy', year=2026,
         alt='Close view of the auger area beneath the LeeBoy 8680 paver. The source photograph shows equipment details rather than an operating sequence. The adjoining explanation distinguishes conveyors, augers and screed.',
         context='Complete photograph cropped from the page; the manufacturer heading and discussion remain in the linked full source page. No labels, controls, colours or equipment geometry are altered.'),
    dict(id='MF-03', file='multiquip-ar13-roller-components.png', source='OEM-03',
         page=14, printed_page='14', source_figure='Figure 4. Roller Components',
         bbox=[36, 77, 572, 720], title='Read a roller component diagram',
         author='Multiquip Inc.', year=2021,
         alt='Numbered line drawing of an AR13HA/AR13HAR tandem drum roller. The visible rear drum, operator position and machine body connect to callouts 1 to 25; selected names from the next source page are listed beside this figure.',
         context='Complete component drawing, all callouts and original figure caption retained. Page header/footer omitted. The complete component descriptions are on source page 15; selected names only are used for identification, not operation.'),
    dict(id='MF-04', file='multiquip-mrh800gs-dimensions.png', source='OEM-02',
         page=12, printed_page='12', source_figure='Figure 1. MRH800GS Dimensions and Table 3. Dimensions',
         bbox=[54, 83, 535, 733], title='Connect a dimension letter to its value',
         author='Multiquip Inc.', year=2020,
         alt='Plan and side views of the MRH800GS roller with dimension letters A to L, followed by the complete dimensions table in inches and millimetres. Width F is 692 millimetres and each half-width G is 346 millimetres.',
         context='Both drawings, dimension letters, figure caption and entire associated table retained together. Page header/footer omitted. Values are copied visually as published; no operating clearance is inferred.'),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    out = ROOT / 'assets' / 'crops'
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for spec in SPECS:
        source = MANUALS[spec['source']]
        original = ROOT / source['local_file']
        assert sha(original) == source['sha256'], f'Source changed: {original}'
        with fitz.open(original) as document:
            page = document[spec['page'] - 1]
            rectangle = fitz.Rect(spec['bbox'])
            assert page.rect.contains(rectangle), spec['id']
            target = out / spec['file']
            page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=rectangle, alpha=False).save(target)
        record = dict(spec)
        record.update(
            local_file='assets/crops/' + spec['file'],
            source_file=source['local_file'], source_sha256=source['sha256'],
            source_title=source['title'], source_document_number=source['document_number'],
            source_edition=source['edition'], source_serial_scope=source['serial_scope'],
            source_url=source['source_url'], image_sha256=sha(target),
            image_bytes=target.stat().st_size, resolution_dpi=216,
            processing='PyMuPDF page-region render to PNG; no generative edits, recolouring, annotation removal or retouching.',
            copyright=f"Copyright {spec['year']} by {spec['author'].rstrip('.')}.",
            apa_reference_plain_text=REFERENCES[spec['source']],
            figure_note_locator=f"Cropped from {spec['source_figure']}, printed page {spec['printed_page']} (PDF viewer page {spec['page']}).",
            figure_note_location=f"lesson.md, figure {spec['id'].replace('MF-0', '')}; formatted APA-style note beneath the image",
            credit_status='APA-style attribution identifies the source; no publisher permission or open licence is asserted.',
        )
        records.append(record)
    manifest = dict(schema_version=1, collection='Faithful OEM teaching crops',
                    coordinates='PDF points, top-left origin; [x0,y0,x1,y1]',
                    renderer='PyMuPDF ' + fitz.VersionBind,
                    sources_preserved=True, figures=records)
    (ROOT / 'assets' / 'figure-manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f'Extracted and recorded {len(records)} figures; original hashes verified.')


if __name__ == '__main__':
    main()
