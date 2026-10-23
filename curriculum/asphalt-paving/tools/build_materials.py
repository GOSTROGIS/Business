"""Build the asphalt curriculum reading pages and printable A1 materials.

Run from any directory. Install tools/requirements.txt first.
Use --html-only when no Chromium browser is available.
"""

from __future__ import annotations

import argparse
from functools import partial
from html import escape, unescape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import re
import shutil
from tempfile import TemporaryDirectory
from threading import Thread
from urllib.parse import urlsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = "https://github.com/GOSTROGIS/Business/blob/main/curriculum/asphalt-paving/"
DOCUMENTS = [
    ("README.md", "index.html", "Asphalt paving", "Curriculum workspace", None),
    ("unit-01/learner.md", "unit-01/index.html", "Roads, resources & equipment", "A1 · Learner workbook", "learner-workbook.pdf"),
    ("unit-01/instructor.md", "unit-01/instructor.html", "Teaching the opening unit", "A1 · Instructor guide", "instructor-guide.pdf"),
    ("curriculum-map.md", "curriculum-map.html", "The opening learning sequence", "Line A · Curriculum map", None),
    ("skills-map.md", "skills-map.html", "Nine skills in the work", "A1 · Skills and evidence", None),
    ("unit-01/materials/README.md", "unit-01/materials/index.html", "Tools for the opening unit", "A1 · Classroom materials", None),
    ("unit-01/materials/response-sheet.md", "unit-01/materials/response-sheet.html", "Your work and reflections", "A1 · Response sheet", "response-sheet.pdf"),
    ("unit-01/materials/change-card.md", "unit-01/materials/change-card.html", "A change to the brief", "A1 · Instructor handout", "change-card.pdf"),
    ("unit-01/materials/process-cards.md", "unit-01/materials/process-cards.html", "Connect the paving process", "A1 · Cut-out cards", "process-cards.pdf"),
]
HTML_FOR_SOURCE = {(ROOT / source).resolve(): (ROOT / target).resolve() for source, target, *_ in DOCUMENTS}


def render_document(source_name, target_name, title, eyebrow, pdf_name):
    source, target = ROOT / source_name, ROOT / target_name
    converter = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"], extension_configs={"toc": {"toc_depth": "2-2"}})
    body = converter.convert(source.read_text(encoding="utf-8"))
    body = re.sub(r"^<h1[^>]*>.*?</h1>\s*", "", body, count=1, flags=re.S)

    def rewrite(match):
        href = unescape(match[1])
        if urlsplit(href).scheme or href.startswith(("#", "//")):
            return match[0]
        path, separator, fragment = href.partition("#")
        resolved = (source.parent / path).resolve()
        dest = HTML_FOR_SOURCE.get(resolved, resolved)
        relative = os.path.relpath(dest, target.parent)
        return f'href="{escape(relative + (separator + fragment if separator else ""), quote=True)}"'

    body = re.sub(r'href="([^"]+)"', rewrite, body)
    body = re.sub(r"<p>_{20,}</p>", '<div class="writing-line" aria-hidden="true"></div>', body)
    body = re.sub(r"<p>(<strong>A1-Q\d{2})", r'<p class="task-prompt">\1', body)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    prefix = os.path.relpath(ROOT, target.parent)
    home = f"{prefix}/index.html"
    toolbar = f'<a href="{home}">Asphalt curriculum</a>'
    if pdf_name:
        toolbar += f'<a class="primary" href="{pdf_name}">Download printable PDF</a>'
    toolbar += f'<a href="{prefix}/sources/asphalt-paving-laydown-technician-program-outline-august-2016.pdf#page=22">Source outline · A1</a>'
    description = "Read the task. Work through an example. Practise, check and explain."
    if source_name == "README.md":
        description = "Start with the paving industry. Build trade knowledge and the nine Skills for Success together."
    handout = "/materials/" in source_name
    page_class = "handout" if handout else "reading-page"
    if source_name == "unit-01/instructor.md":
        page_class += " instructor"
    if source_name == "unit-01/materials/response-sheet.md":
        page_class += " response-sheet"
    contents = f'<nav class="contents" aria-label="On this page"><h2>In this document</h2>{converter.toc}</nav>' if converter.toc and not handout else ""
    document = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | ACCESS IS4S Asphalt</title>
<meta name="description" content="{escape(description, quote=True)}">
<link rel="stylesheet" href="{prefix}/assets/workbook.css">
<link rel="icon" href="{prefix}/assets/is4s-badge.svg" type="image/svg+xml">
</head><body class="{page_class}">
<a class="skip" href="#content">Skip to learning material</a>
<header class="mast"><div class="wrap"><div class="head">
<img class="badge" src="{prefix}/assets/is4s-badge.svg" width="142" height="142" alt="ACCESS Indigenous Skills4Success">
<div><p class="eyebrow">{escape(eyebrow)}</p><h1>{escape(title)}</h1><p class="lede">{escape(description)}</p>
<div class="meta"><span class="tag">Asphalt Paving/Laydown Technician</span><span class="tag">Teaching draft · 23 October 2026</span></div></div>
</div><nav class="toolbar" aria-label="Document resources">{toolbar}</nav></div></header>
<main class="wrap" id="content">{contents}<article class="sheet">{body}</article></main>
<footer><div class="wrap"><p>ACCESS · Indigenous Skills 4 Success · Asphalt curriculum development</p>
<p>Based on the supplied SkilledTradesBC outline and SkillPlan's March 2024 guide. Proposed learning materials for instructor review and pilot.</p></div></footer>
</body></html>'''
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(document, encoding="utf-8")


def export_pdfs():
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, TextStringObject

    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f"http://127.0.0.1:{server.server_port}/"
    try:
        with TemporaryDirectory(prefix="is4s-asphalt-") as temporary, sync_playwright() as p:
            executable = os.environ.get("IS4S_CHROMIUM_PATH") or shutil.which("chromium")
            browser = p.chromium.launch(headless=True, **({"executable_path": executable} if executable else {}))
            try:
                for _, target_name, title, _, pdf_name in DOCUMENTS:
                    if not pdf_name:
                        continue
                    page = browser.new_page()
                    page.goto(origin + target_name, wait_until="networkidle")
                    page.evaluate("document.fonts.ready")
                    raw = Path(temporary) / pdf_name
                    page.pdf(path=str(raw), format="Letter", prefer_css_page_size=True, print_background=True,
                             display_header_footer=True, header_template="<div></div>",
                             footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#625D58">ACCESS IS4S · Asphalt A1 · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
                    writer = PdfWriter()
                    writer.clone_document_from_reader(PdfReader(raw))
                    for pdf_page in writer.pages:
                        for reference in pdf_page.get("/Annots", []):
                            action = reference.get_object().get("/A", {})
                            uri = str(action.get("/URI", ""))
                            if uri.startswith(origin):
                                action[NameObject("/URI")] = TextStringObject(PUBLIC + uri[len(origin):])
                    writer.add_metadata({"/Title": f"ACCESS IS4S Asphalt A1 — {title}", "/Subject": "Teaching draft based on supplied standards and Skills for Success guide"})
                    destination = ROOT / Path(target_name).parent / pdf_name
                    with destination.open("wb") as output:
                        writer.write(output)
                    print(f"Built {destination.relative_to(ROOT)} ({len(writer.pages)} pages)")
                    page.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html-only", action="store_true")
    args = parser.parse_args()
    for document in DOCUMENTS:
        render_document(*document)
    print(f"Built {len(DOCUMENTS)} reading pages")
    if not args.html_only:
        export_pdfs()


if __name__ == "__main__":
    main()
