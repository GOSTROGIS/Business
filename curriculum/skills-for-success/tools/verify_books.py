#!/usr/bin/env python3
"""Check ACCESS IS4S book sources and generated artifacts without network access.

Run from any directory. Use --require-generated after building both books and
--report PATH to retain a JSON result. Only pypdf and the standard library are
required. Checks cover content, links, figure placement, accessible figure
descriptions and self-contained SVGs. They do not replace curriculum,
cultural-context, accessibility, or visual-layout review.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from html import unescape
from html.parser import HTMLParser
import ipaddress
import json
import math
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import parse_qs, unquote, urlsplit
from xml.etree import ElementTree

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PAGES = 148
SOURCE_SHA256 = "32dad4699b1ef1ab281ad4bdf95bef310048741703fc401094c57f6c62e33caf"
SKILLS = (
    ("01-reading", "RD", "Reading"),
    ("02-writing", "WR", "Writing"),
    ("03-numeracy", "NU", "Numeracy"),
    ("04-digital", "DG", "Digital"),
    ("05-problem-solving", "PS", "Problem Solving"),
    ("06-communication", "CM", "Communication"),
    ("07-collaboration", "CL", "Collaboration"),
    ("08-adaptability", "AD", "Adaptability"),
    ("09-creativity-innovation", "CI", "Creativity and Innovation"),
)
BOOKS = ("learner-textbook", "practitioner-guide")


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKC", unescape(value)).casefold()
    return re.sub(r"[^\w]+", " ", value.replace("&", " and ")).strip()


def without_code(text: str) -> str:
    """Ignore fenced examples and inline code when inspecting Markdown links."""
    result = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            result.append("")
        else:
            result.append(line if fence is None else "")
    return re.sub(r"(`+).*?\1", "", "\n".join(result))


def destination_at(text: str, start: int) -> str:
    """Read a Markdown destination, preserving balanced URL parentheses."""
    while start < len(text) and text[start].isspace():
        start += 1
    if start >= len(text):
        return ""
    if text[start] == "<":
        end = text.find(">", start + 1)
        return text[start + 1:end] if end >= 0 else ""
    result = []
    depth = 0
    index = start
    while index < len(text):
        char = text[index]
        if char == "\\" and index + 1 < len(text):
            result.append(text[index + 1])
            index += 2
            continue
        if (char.isspace() or char == ")") and depth == 0:
            break
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        result.append(char)
        index += 1
    return "".join(result)


class HTMLDocument(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.headings: list[str] = []
        self.text: list[str] = []
        self.figures: list[dict] = []
        self.body_attributes: dict = {}
        self.toc_pages: list[dict] = []
        self._toc_page: dict | None = None
        self._figure_stack: list[dict] = []
        self._caption_stack: list[dict] = []
        self._heading: list[str] | None = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "body":
            self.body_attributes = attributes
        if "toc-page" in attributes.get("class", "").split():
            self._toc_page = {"target": attributes.get("data-toc-target", ""),
                              "page": attributes.get("data-page", ""), "text": []}
            self.toc_pages.append(self._toc_page)
        if tag == "figure":
            figure = {"id": attributes.get("data-visual", ""), "images": [],
                      "caption": [], "closed": False}
            self.figures.append(figure)
            self._figure_stack.append(figure)
        elif tag == "img" and self._figure_stack:
            self._figure_stack[-1]["images"].append(attributes)
        elif tag == "figcaption" and self._figure_stack:
            self._caption_stack.append(self._figure_stack[-1])
        for name, value in attrs:
            if value is None:
                continue
            if name == "id" or (tag == "a" and name == "name"):
                self.ids.append(value)
            if name in {"href", "src"}:
                self.links.append(value)
        if re.fullmatch(r"h[1-6]", tag):
            self._heading = []

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        if tag == "span" and self._toc_page is not None:
            self._toc_page = None
        if tag == "figcaption" and self._caption_stack:
            self._caption_stack.pop()
        elif tag == "figure" and self._figure_stack:
            self._figure_stack.pop()["closed"] = True
        if re.fullmatch(r"h[1-6]", tag) and self._heading is not None:
            self.headings.append("".join(self._heading))
            self._heading = None

    def handle_data(self, data):
        self.text.append(data)
        if self._toc_page is not None:
            self._toc_page["text"].append(data)
        if self._heading is not None:
            self._heading.append(data)
        if self._caption_stack:
            self._caption_stack[-1]["caption"].append(data)


class CrosswalkStructure(HTMLParser):
    """Keep section/table relationships that plain text presence cannot prove."""

    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.headings: list[dict] = []
        self.tables: list[dict] = []
        self._path: dict[int, str] = {}
        self._heading: list[str] | None = None
        self._heading_level = 0
        self._table: dict | None = None
        self._row: list[str] | None = None
        self._cell: list[str] | None = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if re.fullmatch(r"h[1-6]", tag):
            self._heading_level = int(tag[1])
            self._heading = []
        elif tag == "table":
            self._table = {"path": dict(self._path), "rows": []}
            self.tables.append(self._table)
        elif tag == "tr" and self._table is not None:
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell = []

    def handle_data(self, data):
        if self._heading is not None:
            self._heading.append(data)
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag):
        if re.fullmatch(r"h[1-6]", tag) and self._heading is not None:
            level = self._heading_level
            title = " ".join("".join(self._heading).split())
            self._path = {key: value for key, value in self._path.items() if key < level}
            self._path[level] = title
            self.headings.append({"level": level, "text": title, "path": dict(self._path)})
            self._heading = None
        elif tag in {"td", "th"} and self._cell is not None:
            self._row.append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self._table["rows"].append(self._row)
            self._row = None
        elif tag == "table":
            self._table = None


def markdown_links(text: str) -> list[str]:
    text = without_code(text)
    targets = [destination_at(text, match.end()) for match in re.finditer(r"\]\(", text)]
    targets += [destination_at(text, match.end()) for match in
                re.finditer(r"(?m)^\s{0,3}\[[^\]\n]+\]:[ \t]*", text)]
    targets += HTMLDocument(text).links
    return [unescape(target) for target in targets if target]


def markdown_anchors(text: str) -> set[str]:
    """Accept common GitHub/Python-Markdown heading IDs and explicit HTML IDs.

    Markdown has no universal heading-slug standard. Keep both established
    conventions here; generated HTML is checked against its actual IDs instead.
    """
    text = without_code(text)
    ids = set(HTMLDocument(text).ids)
    headings = re.findall(r"(?m)^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", text)
    headings += re.findall(r"(?m)^([^\n]+)\n(?:={3,}|-{3,})\s*$", text)
    github_seen: Counter = Counter()
    python_seen: Counter = Counter()
    for heading in headings:
        explicit = re.search(r"\{[^}]*#([^\s}]+)[^}]*\}\s*$", heading)
        if explicit:
            ids.add(explicit.group(1))
            heading = heading[:explicit.start()]
        heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        heading = unescape(re.sub(r"<[^>]+>", "", heading)).strip().casefold()
        github = "".join(c for c in heading if c in "-_ " or c.isalnum()).replace(" ", "-")
        count = github_seen[github]
        ids.add(github if count == 0 else f"{github}-{count}")
        github_seen[github] += 1
        ascii_heading = unicodedata.normalize("NFKD", heading).encode("ascii", "ignore").decode()
        python = re.sub(r"[^\w\s-]", "", ascii_heading)
        python = re.sub(r"[-\s]+", "-", python).strip("-")
        count = python_seen[python]
        ids.add(python if count == 0 else f"{python}_{count}")
        python_seen[python] += 1
    return ids


def local_host(uri: str) -> bool:
    try:
        host = (urlsplit(uri).hostname or "").rstrip(".").casefold()
        if host == "localhost" or host.endswith(".localhost"):
            return True
        try:
            return ipaddress.ip_address(host).is_loopback
        except ValueError:
            return False
    except ValueError:
        return False


class Verifier:
    def __init__(self, root: Path, require_generated: bool):
        self.root = root.resolve()
        self.repo_root = next((p for p in self.root.parents if (p / ".git").exists()), self.root)
        self.require_generated = require_generated
        self.counts: Counter = Counter()
        self.errors: list[str] = []
        self.notes: list[str] = []
        self.artifacts: dict = {}
        self._pdfs: dict[Path, PdfReader] = {}
        self._html: dict[Path, HTMLDocument] = {}
        self._anchors: dict[Path, set[str]] = {}
        self.book_specs: dict[str, dict] = {}
        self._checked_svgs: set[Path] = set()

    def label(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.root))
        except ValueError:
            return str(path)

    def check(self, condition, group: str, message: str):
        self.counts[group] += 1
        if not condition:
            self.errors.append(message)

    def read(self, path: Path, group: str) -> str:
        self.check(path.is_file(), group, f"Missing file: {self.label(path)}")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def pdf(self, path: Path) -> PdfReader:
        path = path.resolve()
        if path not in self._pdfs:
            reader = PdfReader(path)
            if reader.is_encrypted and not reader.decrypt(""):
                raise ValueError(f"Encrypted PDF requires a password: {self.label(path)}")
            self._pdfs[path] = reader
        return self._pdfs[path]

    def html(self, path: Path) -> HTMLDocument:
        path = path.resolve()
        if path not in self._html:
            self._html[path] = HTMLDocument(path.read_text(encoding="utf-8"))
        return self._html[path]

    def verify_inventory(self):
        path = self.root / "research/sfs-inventory.json"
        text = self.read(path, "source inventory")
        if not text:
            return
        inventory = json.loads(text)
        pages = inventory.get("page_inventory", [])
        numbers = [page.get("pdf_page") for page in pages]
        self.check(numbers == list(range(1, SOURCE_PAGES + 1)), "source inventory",
                   "page_inventory must contain each PDF page 1–148 once, in order")
        sections = {item.get("id"): item for item in inventory.get("major_sections", [])}
        subsections = {item.get("id"): item for item in inventory.get("subsections", [])}
        for key in ("major_sections", "subsections"):
            coverage: list[int] = []
            entries = inventory.get(key, [])
            self.check(len({e.get('id') for e in entries}) == len(entries), "source inventory",
                       f"Duplicate IDs in inventory {key}")
            for entry in entries:
                start, end = entry.get("pdf_start"), entry.get("pdf_end")
                valid = isinstance(start, int) and isinstance(end, int) and 1 <= start <= end <= SOURCE_PAGES
                self.check(valid, "source inventory", f"Invalid page interval in {key}/{entry.get('id')}")
                if valid:
                    expected = list(range(start, end + 1))
                    self.check(entry.get("pdf_pages") == expected, "source inventory",
                               f"pdf_pages differs from interval in {key}/{entry.get('id')}")
                    coverage.extend(expected)
            self.check(sorted(coverage) == list(range(1, SOURCE_PAGES + 1)), "source inventory",
                       f"{key} must cover pages 1–148 without gaps or overlaps")
        for page in pages:
            number = page.get("pdf_page")
            self.check(bool(page.get("source_text_as_extracted", "").strip()), "source inventory",
                       f"Inventory page {number} has no extracted source text")
            self.check(bool(page.get("content_summary", "").strip()), "source inventory",
                       f"Inventory page {number} has no content summary")
            for key, entries in (("section_id", sections), ("subsection_id", subsections)):
                entry = entries.get(page.get(key), {})
                self.check(number in entry.get("pdf_pages", []), "source inventory",
                           f"Inventory page {number} is outside its {key}")
        skill_ids = [entry.get("id") for entry in inventory.get("skills", [])]
        self.check(skill_ids == [stem[3:] for stem, _, _ in SKILLS], "source inventory",
                   "Inventory must include all nine skills once in book order")
        for skill in inventory.get("skills", []):
            self.check(len(skill.get("components", [])) == 6, "source inventory",
                       f"Inventory skill {skill.get('id')} must retain six components")
            for key in ("learner", "practitioner", "answer_guidance"):
                target = skill.get("access_destinations", {}).get(key)
                self.check(bool(target), "source inventory", f"Missing {key} destination for {skill.get('id')}")
                if target:
                    self.verify_link(path, target)
        for key in ("access_crosswalk_file", "original_bibliography_index_file"):
            target = inventory.get(key)
            self.check(bool(target), "source inventory", f"Inventory missing {key}")
            if target:
                self.verify_link(path, target)
        source = inventory.get("source", {})
        self.check(source.get("pdf_pages") == SOURCE_PAGES, "source identity", "Inventory source page count must be 148")
        self.check(source.get("sha256") == SOURCE_SHA256, "source identity", "Inventory source SHA-256 differs from the supplied PDF identity")
        source_path = source.get("local_source_path")
        self.check(bool(source_path), "source identity", "Inventory missing source.local_source_path")
        if source_path:
            pdf_path = (path.parent / source_path).resolve()
            self.check(pdf_path.is_file(), "source identity", f"Missing supplied PDF: {pdf_path}")
            if pdf_path.is_file():
                data = pdf_path.read_bytes()
                actual_hash = hashlib.sha256(data).hexdigest()
                self.check(actual_hash == SOURCE_SHA256, "source identity", "Supplied PDF SHA-256 mismatch")
                self.check(len(data) == source.get("bytes"), "source identity", "Supplied PDF byte count differs from inventory")
                self.check(len(self.pdf(pdf_path).pages) == SOURCE_PAGES, "source identity", "Supplied PDF does not contain 148 pages")
                self.artifacts["source"] = {"path": str(pdf_path), "sha256": actual_hash, "pages": len(self.pdf(pdf_path).pages)}

    def verify_activities(self):
        pairs = [(stem, prefix, 18) for stem, prefix, _ in SKILLS]
        pairs.append(("10-integrated-projects", "CP", 12))
        for stem, prefix, count in pairs:
            expected = [f"{prefix}-{number:02d}" for number in range(1, count + 1)]
            for folder in ("learner", "answers"):
                path = self.root / folder / f"{stem}.md"
                text = without_code(self.read(path, "activity coverage"))
                # Additional teaching packets may use their own IDs. Preserve
                # the original sequence without treating unrelated IDs as edits.
                headings = list(re.finditer(rf"(?m)^#{{1,6}}\s+(?:\*\*)?({prefix}-\d{{2}})\b[^\n]*", text))
                actual = [match.group(1) for match in headings]
                self.check(actual == expected, "activity coverage",
                           f"{self.label(path)} activity headings must be {expected[0]}–{expected[-1]} exactly once in order; found {actual}")
                for match in headings:
                    # A heading alone is not an activity or an answer. Require
                    # actual body content before the next Markdown heading.
                    remainder = text[match.end():]
                    block = re.split(r"(?m)^#{1,6}\s+", remainder, maxsplit=1)[0]
                    self.check(bool(block.strip()), "activity coverage",
                               f"{self.label(path)} has an empty {match.group(1)} entry")

    def verify_manifest(self):
        text = self.read(self.root / "book-manifest.json", "book manifest")
        if not text:
            return
        manifest = json.loads(text)
        books = manifest.get("books", [])
        self.check([book.get("name") for book in books] == list(BOOKS), "book manifest",
                   "Book manifest must identify the learner textbook and practitioner guide once each")
        self.check([normalized(skill) for skill in manifest.get("skills", [])] ==
                   [normalized(name) for _, _, name in SKILLS], "book manifest",
                   "Book manifest must list all nine Skills for Success")
        for book in books:
            name = book.get("name")
            self.book_specs[name] = book
            self.check(bool(book.get("title", "").strip()), "book manifest", f"Missing book title: {name}")
            chapters = book.get("chapters", [])
            self.check(bool(chapters) and len(chapters) == len(set(chapters)), "book manifest",
                       f"Missing or duplicate chapter list in {name}")
            for chapter in chapters:
                self.check((self.root / chapter).is_file(), "book manifest",
                           f"Manifest chapter missing from {name}: {chapter}")
        for folder, name in (("learner", "learner-textbook"), ("practitioner", "practitioner-guide"),
                             ("answers", "practitioner-guide")):
            chapters = self.book_specs.get(name, {}).get("chapters", [])
            for path in (self.root / folder).glob("*.md"):
                self.check(str(path.relative_to(self.root)) in chapters, "book manifest",
                           f"{name} omits source chapter: {self.label(path)}")

    def verify_link(self, origin: Path, target: str):
        try:
            parsed = urlsplit(target)
        except ValueError:
            self.check(False, "links", f"Invalid URL in {self.label(origin)}: {target}")
            return
        if parsed.scheme or parsed.netloc:
            self.counts["external links skipped"] += 1
            return
        if parsed.path.startswith("/"):
            path = (self.repo_root / unquote(parsed.path).lstrip("/")).resolve()
        else:
            path = (origin.parent / unquote(parsed.path)).resolve() if parsed.path else origin.resolve()
        self.check(path.exists(), "links", f"Broken link in {self.label(origin)}: {target}")
        if not path.exists() or not parsed.fragment:
            return
        fragment = unquote(parsed.fragment)
        suffix = path.suffix.casefold()
        if suffix == ".pdf":
            params = parse_qs(fragment)
            if "page" in params:
                value = params["page"]
                valid = len(value) == 1 and value[0].isdigit() and 1 <= int(value[0]) <= len(self.pdf(path).pages)
                self.check(valid, "fragments", f"Invalid PDF page target in {self.label(origin)}: {target}")
            else:
                self.counts["unsupported fragments skipped"] += 1
        elif suffix in {".html", ".htm"}:
            self.check(fragment in self.html(path).ids, "fragments",
                       f"Missing HTML fragment in {self.label(origin)}: {target}")
        elif suffix == ".md":
            if path not in self._anchors:
                self._anchors[path] = markdown_anchors(path.read_text(encoding="utf-8"))
            self.check(fragment in self._anchors[path], "fragments",
                       f"Missing Markdown heading/explicit fragment in {self.label(origin)}: {target}")
        elif suffix == ".svg":
            self.check(fragment in self.html(path).ids, "fragments",
                       f"Missing SVG fragment in {self.label(origin)}: {target}")
        else:
            self.counts["unsupported fragments skipped"] += 1

    def verify_markdown(self):
        paths = sorted(self.root.rglob("*.md"))
        self.check(bool(paths), "markdown", "No Markdown source files found")
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.check(bool(text.strip()), "markdown", f"Empty Markdown source: {self.label(path)}")
            for target in markdown_links(text):
                self.verify_link(path, target)
        self.artifacts["markdown_files"] = len(paths)

    def verify_html(self):
        for stem in BOOKS:
            path = self.root / f"{stem}.html"
            if self.require_generated:
                self.check(path.is_file(), "generated HTML", f"Missing generated book: {path.name}")
            elif not path.is_file():
                self.notes.append(f"Not built; skipped {path.name}")
        for path in sorted(self.root.rglob("*.html")):
            doc = self.html(path)
            self.check(bool("".join(doc.text).strip()), "generated HTML", f"Empty HTML: {self.label(path)}")
            duplicates = [key for key, count in Counter(doc.ids).items() if count > 1]
            self.check(not duplicates, "generated HTML", f"Duplicate HTML IDs in {self.label(path)}: {duplicates}")
            for target in doc.links:
                self.check(not local_host(target), "generated HTML", f"Localhost link in {self.label(path)}: {target}")
                self.verify_link(path, target)
            if path.parent == self.root and path.stem in BOOKS:
                body = normalized(" ".join(doc.text))
                self.check("access" in body and "skills for success" in body, "book identity",
                           f"Missing ACCESS / Skills for Success identity in {path.name}")
                reference_framing = re.findall(
                    r"\bskillplan\b|\b(?:supplied|original|source) guide\b|\bget started guide\b|\b148[- ]page\b",
                    body, re.I)
                self.check(not reference_framing, "standalone books",
                           f"Reference-guide framing remains in {path.name}: {reference_framing[:8]}")
                for prefix in ("RD", "WR", "NU", "DG", "PS", "CM", "CL", "AD", "CI"):
                    self.check(bool(re.search(rf"\bck\s+{prefix.lower()}\b", body)), "fresh practice coverage",
                               f"Fresh {prefix} practice missing from {path.name}")
                headings = [normalized(heading) for heading in doc.headings]
                spec = self.book_specs.get(path.stem, {})
                if spec:
                    self.check(normalized(spec["title"]) in headings, "book identity",
                               f"Declared book title is absent from {path.name}")
                    for source_name in spec.get("chapters", []):
                        source = self.root / source_name
                        if source.is_file():
                            match = re.search(r"(?m)^#\s+(.+)$", source.read_text(encoding="utf-8"))
                            self.check(bool(match) and normalized(match.group(1)) in headings,
                                       "book chapters", f"Source chapter heading absent from {path.name}: {source_name}")
                for _, _, skill in SKILLS:
                    name = normalized(skill)
                    self.check(any(re.search(rf"\b{re.escape(name)}\b", heading) for heading in headings),
                               "book chapters", f"No {skill} chapter heading found in {path.name}")
                self.artifacts[path.name] = {"bytes": path.stat().st_size, "headings": len(doc.headings), "ids": len(doc.ids)}
        if self.require_generated:
            for folder in ("learner", "practitioner", "answers"):
                for source in sorted((self.root / folder).glob("*.md")):
                    self.check(source.with_suffix(".html").is_file(), "generated HTML",
                               f"Missing standalone chapter: {self.label(source.with_suffix('.html'))}")

    def check_crosswalk_structure(self, source: str, label: str):
        """Verify the actual rendered crosswalk, including both past failure modes."""
        doc = CrosswalkStructure(source)
        group = "crosswalk structure"
        component_section = normalized("Fifty-four skill components")
        expected_skills = [normalized(name) for _, _, name in SKILLS]
        component_headings = [normalized(h["text"]) for h in doc.headings
                              if h["level"] == 3 and
                              normalized(h["path"].get(2, "")).startswith(component_section)]
        self.check(component_headings == expected_skills, group,
                   f"{label}: component crosswalk needs nine real skill headings in order")
        tables = [table for table in doc.tables
                  if normalized(table["path"].get(2, "")).startswith(component_section)]
        self.check(len(tables) == 9, group,
                   f"{label}: component crosswalk needs one table for each of nine skills")
        for skill in expected_skills:
            matching = [table for table in tables if normalized(table["path"].get(3, "")) == skill]
            valid = len(matching) == 1 and len(matching[0]["rows"]) == 7
            self.check(valid, group, f"{label}: {skill} needs one header row and six component rows")
            if matching:
                rows = matching[0]["rows"]
                self.check(all(len(row) == 3 for row in rows), group,
                           f"{label}: {skill} component table needs three cells per row")
                self.check([row[0] for row in rows[1:] if row] == [str(n) for n in range(1, 7)],
                           group, f"{label}: {skill} component numbers must be 1–6 once in order")
        for section, columns in (("Twenty-seven instructional strategy groups", 4),
                                 ("Twenty-seven grab-and-go activity patterns", 3)):
            matching = [table for table in doc.tables
                        if normalized(table["path"].get(2, "")) == normalized(section)]
            self.check(len(matching) == 1, group, f"{label}: {section} must render as one HTML table")
            if len(matching) != 1:
                continue
            rows = matching[0]["rows"]
            self.check(len(rows) == 28, group, f"{label}: {section} needs a header and 27 body rows")
            self.check(all(len(row) == columns for row in rows), group,
                       f"{label}: {section} needs {columns} cells in every row")
            actual_skills = [normalized(row[0].split(",")[0]) for row in rows[1:] if row]
            self.check(actual_skills == [skill for skill in expected_skills for _ in range(3)], group,
                       f"{label}: {section} needs three rows per skill in book order")
            treatments = ("adapted", "partially adapted", "replaced", "summarized", "indexed", "deferred")
            self.check(all(row and any(normalized(row[-1]).startswith(status + " ")
                                      for status in treatments) for row in rows[1:]), group,
                       f"{label}: {section} rows need explicit treatment labels")
        self.check(not any(re.match(r"\s*#{1,6}\s", cell) for table in doc.tables
                           for row in table["rows"] for cell in row), group,
                   f"{label}: a Markdown heading has been swallowed by a table cell")

    def verify_crosswalk(self):
        paths = ["research/source-coverage.html"]
        if "research/source-coverage.md" in self.book_specs.get("practitioner-guide", {}).get("chapters", []):
            paths.append("practitioner-guide.html")
        for relative in paths:
            path = self.root / relative
            if not path.is_file():
                if self.require_generated:
                    self.check(False, "crosswalk structure", f"Missing generated crosswalk: {relative}")
                else:
                    self.notes.append(f"Not built; skipped crosswalk structure in {relative}")
                continue
            self.check_crosswalk_structure(path.read_text(encoding="utf-8"), relative)

    def verify_contents_destinations(self):
        """Compare generated contents labels and cross-book links with final PDFs."""
        group = "PDF contents destinations"
        for stem in BOOKS:
            html_path = self.root / f"{stem}.html"
            pdf_path = self.root / f"{stem}.pdf"
            if not html_path.is_file() or not pdf_path.is_file():
                if self.require_generated:
                    self.check(False, group, f"Contents check needs {stem}.html and {stem}.pdf")
                continue
            doc, reader = self.html(html_path), self.pdf(pdf_path)
            verified = doc.body_attributes.get("data-pdf-pagination") == "verified"
            if not verified and not self.require_generated:
                self.notes.append(f"Pagination not exported; skipped final contents labels in {stem}")
                continue
            self.check(verified, group, f"{stem}: HTML does not record converged PDF pagination")
            self.check(doc.body_attributes.get("data-pdf-pages") == str(len(reader.pages)), group,
                       f"{stem}: recorded pagination page count differs from the final PDF")
            expected = ["-".join(Path(chapter).with_suffix("").parts)
                        for chapter in self.book_specs.get(stem, {}).get("chapters", [])]
            self.check([entry["target"] for entry in doc.toc_pages] == expected, group,
                       f"{stem}: contents page slots must match manifest chapters once in order")
            destinations = reader.named_destinations
            for entry in doc.toc_pages:
                target = entry["target"]
                destination = destinations.get("/" + target)
                if destination is None:
                    destination = destinations.get(target)
                self.check(destination is not None, group, f"{stem}: missing PDF contents destination {target}")
                if destination is None:
                    continue
                index = reader.get_destination_page_number(destination)
                valid = isinstance(index, int) and 0 <= index < len(reader.pages)
                self.check(valid, group, f"{stem}: invalid PDF contents destination {target}")
                if valid:
                    shown = "".join(entry["text"]).strip()
                    self.check(entry["page"] == shown == str(index + 1), group,
                               f"{stem}: contents label for {target} must match final PDF page {index + 1}")

            # A valid chapter target does not prove that a deep cross-book
            # heading survived export. Inspect the actual final URI targets too.
            uri_targets = set()
            for page in reader.pages:
                for reference in page.get("/Annots", []):
                    action = reference.get_object().get("/A")
                    if not action:
                        continue
                    uri = str(action.get_object().get("/URI", ""))
                    if not uri:
                        continue
                    parsed = urlsplit(uri)
                    params = parse_qs(parsed.fragment)
                    if parsed.path.endswith(".pdf") and len(params.get("page", [])) == 1:
                        uri_targets.add((Path(parsed.path).stem, params["page"][0]))
            checked = set()
            for link in doc.links:
                parsed = urlsplit(link)
                target_stem = Path(parsed.path).stem
                if (parsed.scheme or parsed.netloc or target_stem not in BOOKS or target_stem == stem
                        or not parsed.path.endswith(".html") or not parsed.fragment):
                    continue
                fragment = unquote(parsed.fragment)
                key = target_stem, fragment
                if key in checked:
                    continue
                checked.add(key)
                target_pdf = self.root / f"{target_stem}.pdf"
                if not target_pdf.is_file():
                    self.check(False, group, f"{stem}: missing companion PDF {target_pdf.name}")
                    continue
                companion = self.pdf(target_pdf)
                destination = companion.named_destinations.get("/" + fragment)
                if destination is None:
                    destination = companion.named_destinations.get(fragment)
                self.check(destination is not None, group,
                           f"{stem}: companion PDF omits destination {target_stem}#{fragment}")
                if destination is not None:
                    index = companion.get_destination_page_number(destination)
                    self.check(isinstance(index, int) and 0 <= index < len(companion.pages), group,
                               f"{stem}: invalid companion destination {target_stem}#{fragment}")
                    if isinstance(index, int) and index >= 0:
                        self.check((target_stem, str(index + 1)) in uri_targets, group,
                                   f"{stem}: exported link to {target_stem}#{fragment} must point to PDF page {index + 1}")

    def figure_image_path(self, origin: Path, source: str) -> Path | None:
        """Resolve a figure image locally; network and embedded HTML images are invalid."""
        try:
            parsed = urlsplit(source)
        except ValueError:
            parsed = None
        valid = bool(parsed and parsed.path and not parsed.scheme and not parsed.netloc)
        self.check(valid, "visual images", f"Figure image must be a local file in {self.label(origin)}: {source}")
        if not valid:
            return None
        base = self.repo_root if parsed.path.startswith("/") else origin.parent
        path = (base / unquote(parsed.path).lstrip("/")).resolve()
        self.check(path.is_file(), "visual images", f"Missing figure image in {self.label(origin)}: {source}")
        if path.is_file() and path.suffix.casefold() == ".svg":
            self.verify_svg(path)
        return path

    def verify_svg(self, path: Path):
        """Check self-contained instructional SVGs without interpreting their artwork."""
        if path in self._checked_svgs:
            return
        self._checked_svgs.add(path)
        text = path.read_text(encoding="utf-8")
        self.check(not re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", text, re.I), "SVG structure",
                   f"SVG must not declare external entities or a DTD: {self.label(path)}")
        try:
            root = ElementTree.fromstring(text)
        except ElementTree.ParseError as error:
            self.check(False, "SVG structure", f"Invalid SVG XML in {self.label(path)}: {error}")
            return
        local_name = lambda tag: tag.rsplit("}", 1)[-1].casefold()
        self.check(local_name(root.tag) == "svg", "SVG structure", f"Non-SVG root in {self.label(path)}")
        try:
            box = [float(v) for v in re.split(r"[\s,]+", root.get("viewBox", "").strip())]
            valid_box = len(box) == 4 and all(math.isfinite(v) for v in box) and box[2] > 0 and box[3] > 0
        except ValueError:
            valid_box = False
        self.check(valid_box, "SVG structure", f"Missing or invalid SVG viewBox: {self.label(path)}")
        for tag in ("title", "desc"):
            value = " ".join("".join(child.itertext()) for child in root if local_name(child.tag) == tag)
            self.check(bool(value.strip()), "SVG accessibility", f"SVG needs a nonempty {tag}: {self.label(path)}")

        def internal_reference(value: str) -> bool:
            # Fragment references and embedded raster/font data are self-contained.
            # Nested SVG/HTML data is excluded so scripts cannot hide in another document.
            return value.startswith("#") or bool(re.match(
                r"data:(?:image/(?:png|jpeg|gif|webp)|font/[\w.+-]+|application/(?:font-woff|octet-stream));base64,",
                value, re.I))

        for element in root.iter():
            tag = local_name(element.tag)
            self.check(tag not in {"script", "foreignobject"}, "SVG resources",
                       f"Active SVG content ({tag}) in {self.label(path)}")
            values = []
            for attribute, value in element.attrib.items():
                name = local_name(attribute)
                self.check(not name.startswith("on"), "SVG resources",
                           f"SVG event handler {name} in {self.label(path)}")
                if name in {"href", "src"}:
                    self.check(internal_reference(value.strip()), "SVG resources",
                               f"External SVG reference in {self.label(path)}: {value[:160]}")
                values.append(value)
            if tag == "style":
                values.append("".join(element.itertext()))
            for value in values:
                self.check(not re.search(r"@import\b", value, re.I), "SVG resources",
                           f"SVG CSS import in {self.label(path)}")
                for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", value, re.I | re.S):
                    self.check(internal_reference(match.group(2).strip()), "SVG resources",
                               f"External SVG CSS resource in {self.label(path)}: {match.group(2)[:160]}")

    def verify_visuals(self):
        manifest_path = self.root / "assets/visuals-manifest.json"
        text = self.read(manifest_path, "visual manifest")
        if not text:
            return
        manifest = json.loads(text)
        entries = manifest.get("figures", []) if isinstance(manifest, dict) else manifest
        self.check(isinstance(entries, list) and bool(entries), "visual manifest",
                   "Visuals manifest must contain a nonempty figure array")
        if not isinstance(entries, list):
            return
        cover = manifest.get("cover") if isinstance(manifest, dict) else None
        if cover is not None:
            self.check(isinstance(cover, dict), "visual manifest", "Cover entry must be an object")
            if isinstance(cover, dict):
                self.check(bool((cover.get("alt") or "").strip()), "visual accessibility",
                           "Cover illustration needs nonempty alt text")
                cover_path = self.figure_image_path(self.root / "index.html", cover.get("file") or "")
                self.check(cover_path is not None and cover_path.suffix.casefold() == ".svg", "visual manifest",
                           "Cover illustration must identify a local SVG")
        documents: dict[Path, HTMLDocument] = {}
        for path in self.root.rglob("*.md"):
            documents[path.resolve()] = HTMLDocument(without_code(path.read_text(encoding="utf-8")))
        for path in self.root.rglob("*.html"):
            documents[path.resolve()] = self.html(path)
        figure_paths: dict[Path, dict[str, list[Path]]] = {}
        for path, document in documents.items():
            by_id: dict[str, list[Path]] = {}
            for figure in document.figures:
                visual_id = figure["id"]
                context = f"{self.label(path)} figure {visual_id or '(no data-visual ID)'}"
                self.check(bool(visual_id), "visual figures", f"Missing data-visual ID: {context}")
                self.check(visual_id not in by_id, "visual figures", f"Duplicate visual ID: {context}")
                self.check(figure["closed"], "visual figures", f"Unclosed figure: {context}")
                self.check(bool(figure["images"]), "visual figures", f"Figure has no image: {context}")
                self.check(bool("".join(figure["caption"]).strip()), "visual accessibility",
                           f"Figure has no nonempty figcaption: {context}")
                paths = []
                for image in figure["images"]:
                    self.check(bool((image.get("alt") or "").strip()), "visual accessibility",
                               f"Figure image lacks meaningful alt text: {context}")
                    image_path = self.figure_image_path(path, image.get("src") or "")
                    if image_path is not None:
                        paths.append(image_path)
                by_id[visual_id] = paths
            figure_paths[path] = by_id

        registered: set[str] = set()
        for entry in entries:
            self.check(isinstance(entry, dict), "visual manifest", "Visual manifest entry must be an object")
            if not isinstance(entry, dict):
                continue
            file = entry.get("file", "")
            source = entry.get("source", "")
            visual_id = entry.get("id") or Path(file).stem
            self.check(bool(file and source and visual_id), "visual manifest",
                       f"Visual manifest entry needs file, source and ID: {entry}")
            self.check(visual_id not in registered, "visual manifest", f"Duplicate manifest visual ID: {visual_id}")
            registered.add(visual_id)
            asset = (self.root / file).resolve()
            source_path = (self.root / source).resolve()
            self.check(source_path.is_file(), "visual manifest", f"Missing visual source chapter: {source}")
            self.check(asset.is_file(), "visual manifest", f"Missing visual asset: {file}")
            if asset.is_file() and asset.suffix.casefold() == ".svg":
                self.verify_svg(asset)
            expected_documents = [source_path]
            standalone = source_path.with_suffix(".html")
            if standalone.is_file() or self.require_generated:
                expected_documents.append(standalone)
            for name, spec in self.book_specs.items():
                if source in spec.get("chapters", []):
                    book = self.root / f"{name}.html"
                    if book.is_file() or self.require_generated:
                        expected_documents.append(book.resolve())
            for document in expected_documents:
                actual = figure_paths.get(document, {}).get(visual_id, [])
                self.check(asset in actual, "visual placement",
                           f"Visual {visual_id} missing or uses wrong asset in {self.label(document)}")
        for path, figures in figure_paths.items():
            for visual_id in figures:
                self.check(visual_id in registered, "visual manifest",
                           f"Unregistered visual {visual_id} in {self.label(path)}")

        skill_sources = sorted((self.root / "learner").glob("0[1-9]-*.md"))
        expected = [self.root / "learner" / f"{stem}.md" for stem, _, _ in SKILLS]
        self.check(skill_sources == expected, "visual skill coverage", "Visual coverage requires exactly the nine named skill chapters")
        for source in expected:
            versions = [source]
            if source.with_suffix(".html").is_file() or self.require_generated:
                versions.append(source.with_suffix(".html"))
            for path in versions:
                figures = figure_paths.get(path.resolve(), {})
                count = sum(any(asset.suffix.casefold() == ".svg" for asset in assets) for assets in figures.values())
                self.check(count >= 3, "visual skill coverage",
                           f"{self.label(path)} needs at least 3 SVG figures; found {count}")
        self.artifacts["visuals"] = {"manifest_entries": len(entries), "SVG_assets": len(self._checked_svgs),
                                    "figure_occurrences": sum(len(doc.figures) for doc in documents.values())}

    def verify_pdfs(self):
        for stem in BOOKS:
            path = self.root / f"{stem}.pdf"
            if not path.is_file():
                if self.require_generated:
                    self.check(False, "generated PDF", f"Missing generated book: {path.name}")
                else:
                    self.notes.append(f"Not built; skipped {path.name}")
                continue
            self.check(path.stat().st_size > 0, "generated PDF", f"Empty PDF file: {path.name}")
            reader = self.pdf(path)
            self.check(len(reader.pages) > 0, "generated PDF", f"PDF has no pages: {path.name}")
            texts = []
            annotations = 0
            for number, page in enumerate(reader.pages, 1):
                texts.append(page.extract_text() or "")
                for reference in page.get("/Annots", []):
                    annotation = reference.get_object()
                    action = annotation.get("/A")
                    if action:
                        action = action.get_object()
                        uri = str(action.get("/URI", ""))
                        if uri:
                            annotations += 1
                            self.check(not local_host(uri), "PDF annotations",
                                       f"Localhost annotation in {path.name}, page {number}: {uri}")
            body = normalized(" ".join(texts))
            self.check(bool(body), "generated PDF", f"PDF has no extractable text: {path.name}")
            opening = normalized(" ".join(texts[:3]))
            self.check("access" in opening and "skills for success" in opening, "book identity",
                       f"Missing ACCESS / Skills for Success identity near the start of {path.name}")
            spec = self.book_specs.get(stem, {})
            if spec:
                self.check(normalized(spec["title"]) in opening, "book identity",
                           f"Declared title is absent near the start of {path.name}")
            for _, _, skill in SKILLS:
                self.check(re.search(rf"\b{re.escape(normalized(skill))}\b", body), "book chapters",
                           f"Missing {skill} text in {path.name}")
            # SVG figures can repeat labels and IDs; require content presence,
            # never an exact occurrence count or a fixed page count.
            for prefix, count in [(prefix, 18) for _, prefix, _ in SKILLS] + [("CP", 12)]:
                for number in range(1, count + 1):
                    activity = f"{prefix}-{number:02d}"
                    self.check(re.search(rf"\b{re.escape(normalized(activity))}\b", body), "PDF activity coverage",
                               f"Missing activity {activity} from {path.name}")
            self.artifacts[path.name] = {"bytes": path.stat().st_size, "pages": len(reader.pages), "URI_annotations": annotations}

    def verify_sampler(self):
        """Validate the eight-page preview against the actual full-book page bounds."""
        path = self.root / "visual-sampler.pdf"
        manifest_path = self.root / "visual-sampler.json"
        if not self.require_generated and not path.exists() and not manifest_path.exists():
            self.notes.append("Not built; skipped visual-sampler.pdf")
            return
        text = self.read(manifest_path, "visual sampler")
        self.check(path.is_file(), "visual sampler", "Missing visual-sampler.pdf")
        if not text or not path.is_file():
            return
        manifest = json.loads(text)
        entries = manifest.get("pages", []) if isinstance(manifest, dict) else []
        self.check(isinstance(entries, list) and len(entries) == 8, "visual sampler",
                   "Sampler manifest must contain eight page references")
        if not isinstance(entries, list):
            return
        reader = self.pdf(path)
        self.check(len(reader.pages) == 8, "visual sampler", "Visual sampler must contain eight PDF pages")
        self.check(len(reader.pages) == len(entries), "visual sampler", "Sampler PDF and manifest page counts differ")
        for number, entry in enumerate(entries, 1):
            if not isinstance(entry, dict):
                self.check(False, "visual sampler", f"Invalid sampler entry {number}")
                continue
            book, page = entry.get("book"), entry.get("page")
            valid_book = book in {f"{stem}.pdf" for stem in BOOKS}
            self.check(valid_book, "visual sampler", f"Unknown full book in sampler entry {number}: {book}")
            self.check(bool((entry.get("label") or "").strip()), "visual sampler",
                       f"Sampler entry {number} needs a label")
            if valid_book:
                source = self.root / book
                self.check(source.is_file(), "visual sampler", f"Sampler source PDF missing: {book}")
                if source.is_file():
                    self.check(type(page) is int and 1 <= page <= len(self.pdf(source).pages), "visual sampler",
                               f"Sampler entry {number} references an out-of-range page: {book} page {page}")
        annotations = 0
        for number, page in enumerate(reader.pages, 1):
            self.check(bool((page.extract_text() or "").strip()), "visual sampler",
                       f"Sampler page {number} has no readable text")
            for reference in page.get("/Annots", []):
                action = reference.get_object().get("/A")
                if action:
                    uri = str(action.get_object().get("/URI", ""))
                    if uri:
                        annotations += 1
                        self.check(not local_host(uri), "visual sampler",
                                   f"Localhost annotation in sampler page {number}: {uri}")
        self.artifacts[path.name] = {"bytes": path.stat().st_size, "pages": len(reader.pages),
                                     "source_references": len(entries), "URI_annotations": annotations}

    def run(self) -> dict:
        for operation in (self.verify_inventory, self.verify_activities, self.verify_manifest, self.verify_markdown,
                          self.verify_html, self.verify_crosswalk, self.verify_visuals,
                          self.verify_pdfs, self.verify_contents_destinations, self.verify_sampler):
            try:
                operation()
            except Exception as error:
                self.errors.append(f"{operation.__name__}: {type(error).__name__}: {error}")
        return {
            "status": "failed" if self.errors else "passed",
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "root": str(self.root),
            "require_generated": self.require_generated,
            "checks": dict(sorted(self.counts.items())),
            "artifacts": self.artifacts,
            "errors": self.errors,
            "notes": self.notes,
            "limits": "Offline structural verification; external URLs, instructional correctness, cultural context and visual layout require separate review.",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Skills for Success source directory")
    parser.add_argument("--require-generated", action="store_true", help="Require both full books and standalone chapter HTML")
    parser.add_argument("--report", type=Path, help="Also save the JSON result at this path")
    args = parser.parse_args()
    result = Verifier(args.root, args.require_generated).run()
    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
