"""Build both ACCESS IS4S books, individual reading pages and printable PDFs.

Install requirements.txt and Chromium. Run with --html-only to omit PDF export.
No network request or hosted service is needed to build the supplied materials.
"""
from __future__ import annotations

import argparse
from functools import partial
from html import escape, unescape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import shutil
from tempfile import TemporaryDirectory
from threading import Thread
from urllib.parse import unquote, urlsplit

import markdown

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
        href = unescape(match[1])
        if urlsplit(href).scheme or href.startswith('//'):
            return match[0]
        path, separator, fragment = href.partition('#')
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
            if separator:
                destination += '#' + fragment
        return f'href="{escape(destination, quote=True)}"'

    body = re.sub(r'href="([^"]+)"', rewrite, body)
    body = re.sub(r'(<h[2-6])([^>]*>)([A-Z]{2}-\d{2}\s*[•·—:])', r'\1 class="activity"\2\3', body)
    body = re.sub(r'(<h[2-6])([^>]*>)(Worked example[^<]*)', r'\1 class="example-title"\2\3', body)
    body = body.replace('<table>', '<div class="table-wrap" tabindex="0" role="region" aria-label="Learning table"><table>').replace('</table>', '</table></div>')
    return body


def shell(title_text, body, target, toolbar='', kind='reading', description=''):
    prefix = os.path.relpath(ROOT, target.parent)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title_text)} | ACCESS IS4S</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="stylesheet" href="{prefix}/assets/books.css"><link rel="icon" href="{prefix}/assets/is4s-badge.svg" type="image/svg+xml">
</head><body class="{kind}"><a class="skip" href="#content">Skip to learning material</a>
<nav class="toolbar" aria-label="Book resources"><a href="{prefix}/index.html">ACCESS IS4S books</a>{toolbar}</nav>
{body}<footer class="site-footer">ACCESS · Indigenous Skills 4 Success · Curriculum development edition · 23 October 2026</footer></body></html>'''


def build_book(book, manifest):
    target = ROOT / (book['name'] + '.html')
    sections = []
    contents = []
    for number, source_name in enumerate(book['chapters'], 1):
        source = ROOT / source_name
        chapter_id = slug(Path(source_name))
        chapter_title = title(source)
        group = source.parent.name.title()
        contents.append(f'<li><a href="#{chapter_id}"><span>{group} {Path(source_name).stem[:2] if source.parent.name != "research" else ""}</span>{escape(chapter_title)}</a></li>')
        sections.append(f'<section class="chapter" id="{chapter_id}"><p class="chapter-label">{escape(group)} · ACCESS IS4S</p>{render_body(source, target, manifest, book)}</section>')
    skill_list = ''.join(f'<li>{escape(skill)}</li>' for skill in manifest['skills'])
    cover = f'''<header class="cover"><img src="assets/is4s-badge.svg" alt="ACCESS Indigenous Skills4Success" width="150" height="150">
<p class="eyebrow">{escape(book['eyebrow'])}</p><h1>{escape(book['title'])}</h1>
<p class="cover-deck">{escape(book['description'])}</p><ul class="skill-list">{skill_list}</ul>
<div class="cover-note"><strong>Learning, work and community in British Columbia</strong><p>Original ACCESS IS4S curriculum draft informed by the complete 148-page SkillPlan guide, current federal Skills for Success resources and attributed BC Indigenous education sources.</p><p>23 October 2026 · Edition 1 · For instructor review and learner pilot</p></div></header>'''
    intro = f'''<section class="edition-note"><h2>About this edition</h2><p>{escape(book['edition_note'])}</p><p>The original supplied guide remains in the repository. The practitioner book includes the source crosswalk, reference index and online research record. The books use original practice cases and contemporary BC learning contexts. Nation-specific knowledge and protocols require the direction of the relevant people; this draft does not claim community endorsement or official certification.</p><p>Keep your responses in a notebook, accessible digital document or the supplied learning templates. Each numbered activity has companion answer guidance. Reading pages, editable source and both PDF books are available from the repository.</p></section>'''
    toc = '<nav class="contents" aria-label="Book contents"><h2>In this book</h2><ol>' + ''.join(contents) + '</ol></nav>'
    body = cover + '<main id="content">' + intro + toc + ''.join(sections) + '</main>'
    companion = 'practitioner-guide' if book['name'] == 'learner-textbook' else 'learner-textbook'
    toolbar = f'<a class="primary" href="{book["name"]}.pdf">Download this PDF</a><a href="{companion}.html">Open companion book</a>'
    target.write_text(shell(book['title'], body, target, toolbar, 'book', book['description']))


def build_standalone(source, manifest):
    target = source.with_name('index.html') if source.name == 'README.md' else source.with_suffix('.html')
    body = render_body(source, target, manifest)
    prefix = os.path.relpath(ROOT, target.parent)
    mast = f'<header class="reading-mast"><img src="{prefix}/assets/is4s-badge.svg" width="100" height="100" alt="ACCESS Indigenous Skills4Success"><p class="eyebrow">ACCESS IS4S · Learning resources</p></header>'
    target.write_text(shell(title(source), mast + f'<main id="content" class="reading-sheet">{body}</main>', target))


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
                    raw = Path(temporary) / (book['name'] + '.pdf')
                    page.pdf(path=str(raw), format='Letter', prefer_css_page_size=True, print_background=True,
                             tagged=True, outline=True, display_header_footer=True, header_template='<div></div>',
                             footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#625D58">ACCESS IS4S · ' + escape(book['short_title']) + ' · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
                    writer = PdfWriter()
                    writer.clone_document_from_reader(PdfReader(raw))
                    for pdf_page in writer.pages:
                        for reference in pdf_page.get('/Annots', []):
                            action = reference.get_object().get('/A', {})
                            uri = str(action.get('/URI', ''))
                            if uri.startswith(origin):
                                path = uri[len(origin):]
                                # GitHub displays PDFs and editable Markdown directly; raw HTML is not a reading host.
                                path = re.sub(r'\.html(?=#|$)', '.md', path) if '/learner/' in path or '/practitioner/' in path or '/answers/' in path or '/research/' in path else path
                                path = path.replace('learner-textbook.html', 'learner-textbook.pdf').replace('practitioner-guide.html', 'practitioner-guide.pdf')
                                path = path.replace('/index.html', '/README.md')
                                action[NameObject('/URI')] = TextStringObject(PUBLIC + path)
                    writer.add_metadata({'/Title': 'ACCESS IS4S — ' + book['title'], '/Author': 'ACCESS IS4S curriculum development', '/Subject': book['description'], '/Language': 'en-CA'})
                    with (ROOT / (book['name'] + '.pdf')).open('wb') as output:
                        writer.write(output)
                    print(f"Built {book['name']}.pdf ({len(writer.pages)} pages)")
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html-only', action='store_true')
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    for book in manifest['books']:
        build_book(book, manifest)
    sources = sorted(ROOT.glob('*.md')) + [p for directory in ['learner', 'practitioner', 'answers', 'research', 'assets'] for p in sorted((ROOT / directory).glob('*.md'))]
    for source in sources:
        build_standalone(source, manifest)
    print(f'Built {len(sources)} individual pages and {len(manifest["books"])} complete HTML books')
    if not args.html_only:
        export_pdfs(manifest)


if __name__ == '__main__':
    main()
