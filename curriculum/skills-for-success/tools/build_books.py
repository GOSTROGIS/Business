"""Build both ACCESS IS4S books, individual reading pages and printable PDFs.

Install requirements.txt and Chromium. Run with --html-only to omit PDF export.
No network request or hosted service is needed to build the supplied materials.
"""
from __future__ import annotations

import argparse
from datetime import date
from functools import partial
from html import escape, unescape
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import shutil
from tempfile import TemporaryDirectory
from threading import Thread
from urllib.parse import unquote, urlencode, urlsplit

import markdown

from install_visuals import install_visuals
from build_sampler import build_sampler
from plain_language import transform as plain_language

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
PUBLIC = 'https://github.com/GOSTROGIS/Business/blob/main/'
MANIFEST = ROOT / 'book-manifest.json'


def slug(path):
    return '-'.join(path.with_suffix('').parts)


def title(path):
    return re.search(r'^# (.+)$', path.read_text(), re.M).group(1)


def converter():
    return markdown.Markdown(extensions=['tables', 'fenced_code', 'toc', 'sane_lists'])


def destinations(manifest):
    return {str(Path(source)): (book['name'], slug(Path(source)))
            for book in manifest['books'] for source in book['chapters']}


def plain_text(value):
    return ' '.join(unescape(re.sub(r'<[^>]+>', '', value)).split())


class TableInfo(HTMLParser):
    """Read the generated table shape without introducing a new HTML dependency."""

    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.current_row = None
        self.current_cell = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.current_row = []
        elif tag in {'td', 'th'}:
            self.current_cell = []

    def handle_data(self, data):
        if self.current_cell is not None:
            self.current_cell.append(data)

    def handle_endtag(self, tag):
        if tag in {'td', 'th'} and self.current_cell is not None:
            if self.current_row is not None:
                self.current_row.append(' '.join(''.join(self.current_cell).split()))
            self.current_cell = None
        elif tag == 'tr' and self.current_row is not None:
            self.rows.append(self.current_row)
            self.current_row = None


def enhance_tables(body):
    """Give simple tables room to reflow; reserve writing space only for blank forms."""
    count = 0

    def replace(match):
        nonlocal count
        count += 1
        info = TableInfo(match[0])
        if not info.rows:
            return match[0]
        columns = max(map(len, info.rows))
        headers, rows = info.rows[0], info.rows[1:]
        headings = re.findall(r'<h[1-6]\b[^>]*>(.*?)</h[1-6]>', body[:match.start()], re.S)
        context = plain_text(headings[-1]) if headings else 'Learning material'
        name = f'{context} — table {count}: ' + ', '.join(headers)
        classes = ['table-simple' if columns <= 2 else 'table-wide']
        blank = lambda value: not value.strip('_—–. \t\xa0')
        writing = bool(rows) and columns >= 2 and all(len(row) == columns and blank(row[-1]) for row in rows)
        if writing:
            classes.append('writing-form')
        # Short factual schedules/counts can stay together; prose-heavy tables must split.
        compact = not writing and len(rows) <= 7 and sum(len(cell) for row in info.rows for cell in row) <= 850
        if compact:
            classes.append('table-compact')
        def table_tag(opening):
            attrs = opening[1]
            existing = re.search(r'\bclass="([^"]*)"', attrs)
            merged = ' '.join(classes + (existing[1].split() if existing else []))
            attrs = re.sub(r'\s*class="[^"]*"', '', attrs)
            return f'<table class="{escape(merged, quote=True)}"{attrs}>'
        table = re.sub(r'<table\b([^>]*)>', table_tag, match[0], count=1)
        table = re.sub(r'<th\b(?![^>]*\bscope=)([^>]*)>', r'<th scope="col"\1>', table)
        if writing:
            def response(row_match):
                row = row_match[0]
                cells = list(re.finditer(r'<td\b[^>]*>.*?</td>', row, re.S))
                if not cells:
                    return row
                last = cells[-1]
                return row[:last.start()] + '<td class="response-space"><span class="sr-only">Write your response here.</span><span class="response-lines" aria-hidden="true"></span></td>' + row[last.end():]
            table = re.sub(r'<tr\b[^>]*>.*?</tr>', response, table, flags=re.S)
        cue = '<p class="table-scroll-hint">If needed, scroll across this table. Keyboard: focus the table, then use the arrow keys.</p>' if columns > 2 else ''
        return f'{cue}<div class="table-wrap {" ".join(classes)}" tabindex="0" role="region" aria-label="{escape(name, quote=True)}">{table}</div>'

    return re.sub(r'<table\b[^>]*>.*?</table>', replace, body, flags=re.S)


def enhance_figures(body, target):
    """Keep authored SVGs and expose their descriptions without requiring a screen reader."""
    def replace(match):
        figure = match[0]
        image = re.search(r'<img\b[^>]*\bsrc="([^"]+)"[^>]*\balt="([^"]*)"', figure)
        if not image:
            return figure
        alt = unescape(image[2])
        image_path = (target.parent / unquote(urlsplit(unescape(image[1])).path)).resolve()
        try:
            asset = image_path.relative_to(ROOT / 'assets').as_posix()
        except ValueError:
            return figure
        if not re.fullmatch(r'(?:diagrams|illustrations)/[\w.-]+\.(?:svg|png|jpe?g|webp)', asset):
            return figure
        before = body[:match.start()]
        headings = re.findall(r'<h[1-6]\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h[1-6]>', before, re.S)
        fragment, label = headings[-1] if headings else ('content', 'Learning visual')
        label = plain_text(label)
        figure = re.sub(r'aria-label="Learning visual"', f'aria-label="{escape(label + " — visual", quote=True)}"', figure)
        return_path = os.path.relpath(target, ROOT / 'assets') + '#' + fragment
        viewer_path = os.path.relpath(ROOT / 'assets/visual-viewer.html', target.parent)
        viewer = viewer_path + '?' + urlencode({'asset': asset, 'title': label, 'description': alt, 'return': return_path})
        figure = re.sub(r'(<a\b[^>]*class="visual-original"[^>]*href=")[^"]+("[^>]*>)[^<]*(</a>)', lambda m: m[1] + escape(viewer, quote=True) + m[2] + 'Open visual viewer' + m[3], figure)
        if 'class="visual-description"' not in figure:
            description = f'<details class="visual-description"><summary>Read the visual description</summary><p>{escape(alt)}</p></details>'
            figure = figure.replace('</figure>', description + '</figure>')
        return figure
    return re.sub(r'<figure\b[^>]*>.*?</figure>', replace, body, flags=re.S)


def keep_change_cards(body):
    """Keep a short change heading and its conditions together, not an entire activity."""
    pattern = r'(<h([2-6])\b[^>]*>Change card[^<]*</h\2>)(.*?)(?=<h[1-6]\b|$)'
    def replace(match):
        content = match[0]
        if len(plain_text(content)) <= 1600 and '<table' not in content:
            return '<aside class="change-card" aria-label="Changed task conditions">' + content + '</aside>'
        return content
    return re.sub(pattern, replace, body, flags=re.S | re.I)


def edition_text(manifest):
    raw_date = manifest.get('date', '')
    formatted = date.fromisoformat(raw_date).strftime('%d %B %Y').lstrip('0') if raw_date else ''
    edition = str(manifest.get('edition', '')).strip()
    label = manifest.get('edition_label', '')
    return ' · '.join(filter(None, [formatted, f'Edition {edition}' if edition else '', label]))


def render_body(source, target, manifest, book=None):
    parsed = converter()
    body = parsed.convert(source.read_text(encoding='utf-8'))
    source_key = source.relative_to(ROOT)
    namespace = slug(source_key)
    mapping = destinations(manifest)
    if book:
        # Preserve every original heading fragment inside a unique chapter namespace.
        body = re.sub(r'id="([^"]+)"', lambda m: f'id="{namespace}--{m[1]}"', body)
        body = re.sub(r'<(/?)h([1-5])\b', lambda m: f'<{m[1]}h{int(m[2])+1}', body)

    def rewrite(match):
        attribute, href = match[1], unescape(match[2])
        parts = urlsplit(href)
        if parts.scheme or href.startswith('//'):
            return match[0]
        path, fragment = parts.path, parts.fragment
        resolved = (source.parent / path).resolve() if path else source
        try:
            key = str(resolved.relative_to(ROOT))
        except ValueError:
            key = ''
        if book and key in mapping:
            destination_book, chapter_id = mapping[key]
            anchor = chapter_id + ('--' + fragment if fragment else '')
            destination = ('' if destination_book == book['name'] else destination_book + '.html') + '#' + anchor
        elif resolved.suffix == '.md' and resolved.exists() and key:
            destination_path = resolved.with_suffix('.html') if resolved.name != 'README.md' else resolved.with_name('index.html')
            destination = os.path.relpath(destination_path, target.parent)
            if fragment:
                destination += '#' + fragment
        else:
            destination = os.path.relpath(resolved, target.parent)
            if fragment:
                destination += '#' + fragment
        if parts.query:
            base, marker, anchor = destination.partition('#')
            destination = base + '?' + parts.query + (marker + anchor if marker else '')
        return f'{attribute}="{escape(destination, quote=True)}"'

    body = re.sub(r'(href|src)="([^"]+)"', rewrite, body)
    body = re.sub(r'(<h[2-6])([^>]*>)([A-Z]{2}-\d{2}\s*[•·—:])', r'\1 class="activity"\2\3', body)
    body = re.sub(r'(<h[2-6])([^>]*>)(Worked example[^<]*)', r'\1 class="example-title"\2\3', body)
    return keep_change_cards(enhance_figures(enhance_tables(plain_language(body, convert_cards="research" not in source.parts)), target))


def shell(title_text, body, target, toolbar='', kind='reading', description='', manifest=None):
    prefix = os.path.relpath(ROOT, target.parent)
    edition = edition_text(manifest or {})
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title_text)} | ACCESS IS4S</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="stylesheet" href="{prefix}/assets/books.css"><link rel="icon" href="{prefix}/assets/is4s-badge.svg" type="image/svg+xml">
</head><body class="{kind}"><a class="skip" href="#content">Skip to learning material</a>
<nav class="toolbar" aria-label="Book resources"><a href="{prefix}/index.html">ACCESS IS4S books</a>{toolbar}</nav>
{body}<footer class="site-footer">ACCESS · Indigenous Skills 4 Success · {escape(edition or 'Curriculum development edition')}</footer></body></html>'''


def build_book(book, manifest):
    target = ROOT / (book['name'] + '.html')
    sections = []
    contents = []
    for number, source_name in enumerate(book['chapters'], 1):
        source = ROOT / source_name
        chapter_id = slug(Path(source_name))
        chapter_title = title(source)
        group = source.parent.name.title()
        chapter_number = Path(source_name).stem[:2] if Path(source_name).stem[:2].isdigit() else ''
        contents.append(f'<li><a class="toc-link" href="#{chapter_id}"><span class="toc-text"><span class="toc-group">{escape(group)} {chapter_number}</span><span class="toc-title">{escape(chapter_title)}</span></span><span class="toc-page" data-toc-target="{chapter_id}" data-page="" aria-label="PDF page not yet generated">—</span></a></li>')
        sections.append(f'<section class="chapter" id="{chapter_id}"><p class="chapter-label">{escape(group)} · ACCESS IS4S</p>{render_body(source, target, manifest, book)}</section>')
    visual_manifest = json.loads((ROOT / 'assets/visuals-manifest.json').read_text())
    cover_visual = visual_manifest['cover']
    cover = f'''<header class="cover"><div class="cover-brand"><img src="assets/is4s-badge.svg" alt="ACCESS Indigenous Skills4Success" width="90" height="90"><span>ACCESS<br>INDIGENOUS SKILLS 4 SUCCESS</span></div>
<p class="eyebrow">{escape(book['eyebrow'])}</p><h1>{escape(book['title'])}</h1>
<p class="cover-deck">{escape(book['description'])}</p><div class="cover-visual"><img src="{cover_visual['file']}" alt="{escape(cover_visual['alt'], quote=True)}"></div>
<div class="cover-note"><strong>Learning, work and community in British Columbia</strong><p>Practical lessons, complete cases and visual guides for using the nine Skills for Success.</p><p>{escape(edition_text(manifest))}</p></div></header>'''
    intro = f'''<section class="edition-note"><h2>Using this book</h2><p>{escape(book['edition_note'])}</p><p>Use the explanations, worked examples and case documents to practise a useful task. Keep your thinking visible, check your result and choose a next step. You can use the fictional cases without sharing personal records or cultural knowledge.</p><p>Keep responses in a notebook, accessible digital document or the learning templates. Each named learner activity has answer guidance in the practitioner book. Use the contents to find a skill, and return to a model whenever another example would help.</p></section>'''
    toc = '<nav class="contents" aria-label="Book contents"><h2>In this book</h2><ol>' + ''.join(contents) + '</ol></nav>'
    body = cover + '<main id="content">' + intro + toc + ''.join(sections) + '</main>'
    companion = 'practitioner-guide' if book['name'] == 'learner-textbook' else 'learner-textbook'
    toolbar = f'<a class="primary" href="{book["name"]}.pdf">Download this PDF</a><a href="{companion}.html">Open companion book</a>'
    target.write_text(shell(book['title'], body, target, toolbar, 'book', book['description'], manifest))


def build_standalone(source, manifest):
    target = source.with_name('index.html') if source.name == 'README.md' else source.with_suffix('.html')
    body = render_body(source, target, manifest)
    prefix = os.path.relpath(ROOT, target.parent)
    mast = f'<header class="reading-mast"><img src="{prefix}/assets/is4s-badge.svg" width="100" height="100" alt="ACCESS Indigenous Skills4Success"><p class="eyebrow">ACCESS IS4S · Learning resources</p></header>'
    target.write_text(shell(title(source), mast + f'<main id="content" class="reading-sheet">{body}</main>', target, manifest=manifest))


def pdf_chapter_pages(reader, chapter_ids):
    """Use Chromium's actual named destinations, never estimated DOM page heights."""
    result = {}
    for chapter_id in chapter_ids:
        destination = reader.named_destinations.get('/' + chapter_id)
        if destination is None:
            destination = reader.named_destinations.get(chapter_id)
        if destination is None:
            raise ValueError(f'Missing contents destination in exported PDF: {chapter_id}')
        number = reader.get_destination_page_number(destination)
        if number is None or number < 0:
            raise ValueError(f'Invalid contents destination in exported PDF: {chapter_id}')
        result[chapter_id] = number + 1
    return result


def export_paginated_pdf(page, output, book, max_passes=6):
    """Converge printed contents numbers against the PDF that actually contains them.

    Fixed-width page slots normally make this a two-pass export. The bounded
    equality check still catches layout changes or oscillation and fails closed.
    Post-export link edits do not repaginate the document.
    """
    from pypdf import PdfReader

    ids = [slug(Path(source)) for source in book['chapters']]
    shown = page.locator('.toc-page').evaluate_all('(nodes) => Object.fromEntries(nodes.map(n => [n.dataset.tocTarget, Number(n.dataset.page) || null]))')
    if set(shown) != set(ids):
        raise ValueError(f'Contents slots do not match chapters for {book["name"]}')
    seen = set()
    for attempt in range(1, max_passes + 1):
        page.pdf(path=str(output), format='Letter', prefer_css_page_size=True, print_background=True,
                 tagged=True, outline=True, display_header_footer=True, header_template='<div></div>',
                 footer_template='<div style="font-size:9px;width:100%;text-align:center;color:#55504B">ACCESS IS4S · ' + escape(book['short_title']) + ' · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
        reader = PdfReader(output)
        actual = pdf_chapter_pages(reader, ids)
        if shown == actual:
            page.evaluate('(count) => { document.body.dataset.pdfPages = String(count); document.body.dataset.pdfPagination = "verified"; }', len(reader.pages))
            return {'passes': attempt, 'pages': len(reader.pages), 'chapters': actual}
        signature = tuple(actual.items())
        if signature in seen:
            raise ValueError(f'Contents pagination did not stabilize for {book["name"]}; refusing stale page numbers')
        seen.add(signature)
        page.locator('.toc-page').evaluate_all('''(nodes, pages) => nodes.forEach(node => {
            const number = pages[node.dataset.tocTarget];
            node.textContent = String(number);
            node.dataset.page = String(number);
            node.setAttribute('aria-label', 'PDF page ' + number);
        })''', actual)
        shown = actual
    raise ValueError(f'Contents pagination exceeded {max_passes} passes for {book["name"]}')


def add_heading_destinations(writer, reader, page):
    """Preserve cross-book deep links even when Chromium omits an unused named anchor.

    Chromium supplies accurate outline coordinates for headings but creates some
    named destinations only when a same-document link references them. Match the
    ordered, verified outline to DOM headings and retain those exact coordinates.
    """
    from pypdf.generic import ArrayObject, NameObject, TextStringObject

    def flattened(items):
        for item in items:
            if isinstance(item, list):
                yield from flattened(item)
            else:
                yield item

    headings = page.locator('h1,h2,h3,h4,h5,h6').evaluate_all('(nodes) => nodes.map(n => ({id:n.id, title:n.textContent}))')
    outline = list(flattened(reader.outline))
    normalize = lambda value: re.sub(r'\s+', '', value)
    if len(headings) != len(outline):
        raise ValueError('PDF outline and HTML headings differ; cannot verify heading destinations')
    existing = reader.named_destinations
    for heading, destination in zip(headings, outline):
        if normalize(heading['title']) != normalize(str(destination['/Title'])):
            raise ValueError(f'PDF outline heading mismatch: {heading["title"]!r}')
        identifier = heading['id']
        if not identifier or '/' + identifier in existing or identifier in existing:
            continue
        number = reader.get_destination_page_number(destination)
        if number is None or number < 0:
            raise ValueError(f'Invalid heading page: {identifier}')
        coordinates = ArrayObject([writer.pages[number].indirect_reference, *destination.dest_array[1:]])
        legacy_destinations = writer.root_object.get('/Dests')
        if legacy_destinations is not None:
            # Chromium uses this dictionary. Adding a parallel /Names tree can
            # leave readers seeing only /Dests, so extend the existing format.
            legacy_destinations.get_object()[NameObject('/' + identifier)] = coordinates
        else:
            writer.add_named_destination_array(TextStringObject('/' + identifier), coordinates)


def export_pdfs(manifest):
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, TextStringObject

    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(REPOSITORY)))
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}/'
    folder = ROOT.relative_to(REPOSITORY).as_posix() + '/'
    try:
        with TemporaryDirectory(prefix='is4s-books-') as temporary, sync_playwright() as p:
            executable = os.environ.get('IS4S_CHROMIUM_PATH') or shutil.which('chromium')
            browser = p.chromium.launch(headless=True, **({'executable_path': executable} if executable else {}))
            try:
                for book in manifest['books']:
                    page = browser.new_page()
                    page.goto(origin + folder + book['name'] + '.html', wait_until='networkidle')
                    page.evaluate('document.fonts.ready')
                    page.evaluate('Promise.all([...document.images].map(i => i.decode()))')
                    raw = Path(temporary) / (book['name'] + '.pdf')
                    pagination = export_paginated_pdf(page, raw, book)
                    # Persist verified PDF-page references in the matching HTML edition too.
                    (ROOT / (book['name'] + '.html')).write_text(page.content())
                    writer = PdfWriter()
                    raw_reader = PdfReader(raw)
                    writer.clone_document_from_reader(raw_reader)
                    add_heading_destinations(writer, raw_reader, page)
                    for pdf_page in writer.pages:
                        for reference in pdf_page.get('/Annots', []):
                            action = reference.get_object().get('/A', {})
                            uri = str(action.get('/URI', ''))
                            if uri.startswith(origin):
                                path = uri[len(origin):]
                                # GitHub displays PDFs and editable Markdown directly; raw HTML is not a reading host.
                                path = path.replace('learner-textbook.html', 'learner-textbook.pdf').replace('practitioner-guide.html', 'practitioner-guide.pdf')
                                split = urlsplit(path)
                                local = REPOSITORY / unquote(split.path)
                                markdown_path = local.with_name('README.md') if local.name == 'index.html' else local.with_suffix('.md')
                                if local.suffix == '.html' and markdown_path.exists():
                                    replacement = markdown_path.relative_to(REPOSITORY).as_posix()
                                    path = replacement + ('?' + split.query if split.query else '') + ('#' + split.fragment if split.fragment else '')
                                action[NameObject('/URI')] = TextStringObject(PUBLIC + path)
                    writer.add_metadata({'/Title': 'ACCESS IS4S — ' + book['title'], '/Author': 'ACCESS IS4S curriculum development', '/Subject': book['description'], '/Language': 'en-CA'})
                    with (ROOT / (book['name'] + '.pdf')).open('wb') as output:
                        writer.write(output)
                    print(f"Built {book['name']}.pdf ({len(writer.pages)} pages; contents verified in {pagination['passes']} passes)")
                    page.close()
                # Cross-book HTML fragments become stable PDF page targets after both PDFs exist.
                readers = {b['name']: PdfReader(ROOT / (b['name'] + '.pdf')) for b in manifest['books']}
                for book in manifest['books']:
                    writer = PdfWriter()
                    writer.clone_document_from_reader(readers[book['name']])
                    for pdf_page in writer.pages:
                        for reference in pdf_page.get('/Annots', []):
                            action = reference.get_object().get('/A', {})
                            uri = str(action.get('/URI', ''))
                            if not uri.startswith(PUBLIC):
                                continue
                            split = urlsplit(uri)
                            target_name = Path(split.path).stem
                            if target_name in readers and split.path.endswith('.pdf') and split.fragment:
                                destination = readers[target_name].named_destinations.get('/' + unquote(split.fragment))
                                if destination is None:
                                    destination = readers[target_name].named_destinations.get(unquote(split.fragment))
                                if destination is None:
                                    raise ValueError(f'Missing companion PDF destination: {uri}')
                                number = readers[target_name].get_destination_page_number(destination) + 1
                                action[NameObject('/URI')] = TextStringObject(uri.split('#')[0] + f'#page={number}')
                    fixed = Path(temporary) / ('linked-' + book['name'] + '.pdf')
                    with fixed.open('wb') as output:
                        writer.write(output)
                    shutil.copyfile(fixed, ROOT / (book['name'] + '.pdf'))
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()


def main():
    from install_teaching import install_teaching

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html-only', action='store_true')
    args = parser.parse_args()
    install_teaching()
    print(f'Installed {install_visuals()} curated figure placements')
    manifest = json.loads(MANIFEST.read_text())
    for book in manifest['books']:
        build_book(book, manifest)
    sources = sorted(ROOT.rglob('*.md'))
    for source in sources:
        build_standalone(source, manifest)
    print(f'Built {len(sources)} individual pages and {len(manifest["books"])} complete HTML books')
    if not args.html_only:
        export_pdfs(manifest)
        print(f'Built visual-sampler.pdf ({build_sampler()} selected pages)')


if __name__ == '__main__':
    main()
