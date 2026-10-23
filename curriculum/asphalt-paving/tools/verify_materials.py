"""Validate the complete asphalt curriculum packet offline.

Run from any directory after build_materials.py. Requires only pypdf from
tools/requirements.txt plus Python's standard library. This verifies artefact
integrity, linked resources, question coverage and practice-data arithmetic;
it does not replace instructor review of curriculum or current requirements.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import hashlib
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, unquote, urlsplit

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
QUESTION_IDS = {f"A1-Q{number:02d}" for number in range(1, 19)}
SKILLS = (
    "Reading", "Writing", "Numeracy", "Digital", "Problem solving",
    "Communication", "Collaboration", "Adaptability", "Creativity and innovation",
)
EXPECTED_DATA = {
    "North": (4, 120, 6_000_000),
    "Central": (3, 90, 4_000_000),
    "South": (3, 90, 5_000_000),
}


class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.references.append(value)

    handle_startendtag = handle_starttag


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold().replace("&", " and ")).strip()


def numbers_in(text: str) -> set[Decimal]:
    """Read numeric values independent of currency, separators and typography."""
    values = set()
    pattern = r"(?<![\w.])(\d+(?:,\d{3})*(?:\.\d+)?)\s*(million\b|thousand\b|m\b|k\b)?"
    for match in re.finditer(pattern, text, flags=re.I):
        value = Decimal(match.group(1).replace(",", ""))
        suffix = (match.group(2) or "").casefold()
        value *= {"million": 1_000_000, "m": 1_000_000,
                  "thousand": 1_000, "k": 1_000}.get(suffix, 1)
        values.add(value)
    return values


def answer_block(instructor: str, question_id: str) -> str:
    """Find an answer entry, excluding earlier coverage-table references."""
    heading = re.search(r"(?im)^#{1,6}\s+[^\n]*answer[^\n]*key[^\n]*$", instructor)
    scope = instructor[heading.end():] if heading else instructor
    entries = list(re.finditer(r"(?m)^(?:\*\*|#{1,6}\s+)?(A1-Q\d{2})\b", scope))
    for index, match in enumerate(entries):
        if match.group(1) == question_id:
            end = entries[index + 1].start() if index + 1 < len(entries) else len(scope)
            return scope[match.start():end]
    return ""


class Verifier:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.counts = Counter()
        self.errors: list[str] = []
        self.pdf_readers: dict[Path, PdfReader] = {}

    def check(self, condition, group: str, message: str):
        self.counts[group] += 1
        if not condition:
            self.errors.append(message)

    def require_file(self, relative: str, group: str) -> Path | None:
        path = self.root / relative
        self.check(path.is_file(), group, f"Missing file: {relative}")
        return path if path.is_file() else None

    def read(self, relative: str, group: str) -> str:
        path = self.require_file(relative, group)
        return path.read_text(encoding="utf-8") if path else ""

    def pdf(self, path: Path) -> PdfReader:
        path = path.resolve()
        if path not in self.pdf_readers:
            reader = PdfReader(path)
            if reader.is_encrypted and not reader.decrypt(""):
                raise ValueError(f"PDF requires a password: {path.name}")
            self.pdf_readers[path] = reader
        return self.pdf_readers[path]

    def verify_sources(self):
        manifest_path = self.require_file("sources/manifest.json", "sources")
        if not manifest_path:
            return
        entries = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(entries, list):
            raise ValueError("sources/manifest.json must contain a list")
        self.check(len(entries) == 3, "sources", "Source manifest must describe the three supplied PDFs")
        declared = []
        for entry in entries:
            relative = Path("sources") / entry["file"]
            path = (self.root / relative).resolve()
            self.check(path.is_relative_to(self.root / "sources"), "sources",
                       f"Manifest path escapes sources/: {entry['file']}")
            if not path.is_relative_to(self.root / "sources"):
                continue
            declared.append(path)
            if not self.require_file(str(relative), "sources"):
                continue
            data = path.read_bytes()
            self.check(hashlib.sha256(data).hexdigest() == entry["sha256"], "sources",
                       f"Source hash differs from manifest: {entry['file']}")
            self.check(len(data) == entry["bytes"], "sources",
                       f"Source byte count differs from manifest: {entry['file']}")
            self.check(len(self.pdf(path).pages) == entry["pdf_pages"], "sources",
                       f"Source PDF page count differs from manifest: {entry['file']}")
        self.check(len(declared) == len(set(declared)), "sources", "Duplicate source manifest entries")
        actual = {path.resolve() for path in (self.root / "sources").glob("*.pdf")}
        self.check(actual == set(declared), "sources", "Source PDFs and manifest membership differ")

    def verify_questions_and_skills(self):
        for relative in ("unit-01/learner.md", "unit-01/instructor.md",
                         "unit-01/materials/response-sheet.md"):
            text = self.read(relative, "question coverage")
            found = set(re.findall(r"\bA1-Q\d{2}\b", text))
            for question_id in sorted(QUESTION_IDS):
                self.check(question_id in found, "question coverage",
                           f"{relative} does not include {question_id}")
            self.check(not (found - QUESTION_IDS), "question coverage",
                       f"{relative} contains unknown question IDs: {sorted(found - QUESTION_IDS)}")

        text = self.read("skills-map.md", "skills mapping")
        # Support either a table row or a headed section for each skill.
        candidates = [line for line in text.splitlines() if line.lstrip().startswith("|")]
        candidates += re.findall(r"(?ms)^#{1,6} [^\n]+\n.*?(?=^#{1,6} |\Z)", text)
        for skill in SKILLS:
            name = normalized(skill)
            matching = [block for block in candidates if re.search(
                rf"\b{re.escape(name)}\b", normalized(block.split("\n", 1)[0]))]
            self.check(any(re.search(r"\bA1-Q\d{2}\b", block) for block in matching),
                       "skills mapping", f"Skills map needs a question/evidence reference for {skill}")

    def verify_practice_data(self):
        path = self.require_file("unit-01/materials/fictional-industry.csv", "practice data")
        if not path:
            return
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            headings = {normalized(name): name for name in (reader.fieldnames or [])}
            fields = {}
            for key in ("area", "employers", "workers", "contract value"):
                matches = [original for normal, original in headings.items()
                           if normal == key or (key == "area" and normal == "fictional area")
                           or (key == "contract value" and normal.startswith("contract value"))]
                if len(matches) != 1:
                    raise ValueError(f"CSV requires one unambiguous {key!r} column")
                fields[key] = matches[0]
            rows = {}
            for row in reader:
                name = row[fields["area"]].strip()
                if not name and all(not value for value in row.values()):
                    continue
                self.check(name not in rows, "practice data", f"Duplicate CSV area: {name}")
                values = []
                for key in ("employers", "workers", "contract value"):
                    raw = row[fields[key]].strip().replace(",", "").replace("$", "")
                    try:
                        value = Decimal(raw)
                    except InvalidOperation as error:
                        raise ValueError(f"Invalid CSV number in {name}/{key}: {raw!r}") from error
                    self.check(value >= 0 and value == int(value), "practice data",
                               f"CSV {name}/{key} should contain a nonnegative whole number")
                    values.append(value)
                rows[name] = tuple(values)
        self.check(rows == EXPECTED_DATA, "practice data",
                   "CSV differs from the workbook's North/Central/South practice dataset")
        if set(rows) != set(EXPECTED_DATA):
            return
        totals = tuple(sum(values[column] for values in rows.values()) for column in range(3))
        expected_results = set(totals) | {rows["North"][2] - rows["Central"][2]}
        instructor = self.read("unit-01/instructor.md", "practice data")
        block = answer_block(instructor, "A1-Q11")
        self.check(bool(block), "practice data", "Could not locate the A1-Q11 answer-key entry")
        written_numbers = numbers_in(block)
        for result in expected_results:
            self.check(result in written_numbers, "practice data",
                       f"A1-Q11 answer key is missing computed result {result}")
        fraction = Fraction(rows["Central"][0]) / Fraction(totals[0])
        written_fractions = {Fraction(int(a), int(b)) for a, b in
                             re.findall(r"(\d+)\s*/\s*(\d+)", block) if int(b)}
        self.check(fraction in written_fractions, "practice data",
                   f"A1-Q11 answer key does not contain Central's fraction {fraction}")
        funding = answer_block(instructor, "A1-Q09")
        self.check(Decimal(60_000 + 40_000 + 20_000) in numbers_in(funding), "practice data",
                   "A1-Q09 answer key does not contain the $120,000 funding total")

    def verify_html(self):
        for relative in ("index.html", "unit-01/index.html", "unit-01/instructor.html",
                         "curriculum-map.html", "skills-map.html"):
            self.require_file(relative, "HTML links")
        pages = sorted(self.root.rglob("*.html"))
        self.check(bool(pages), "HTML links", "No generated HTML pages found; run build_materials.py")
        for page in pages:
            parser = Links()
            parser.feed(page.read_text(encoding="utf-8"))
            for reference in parser.references:
                url = urlsplit(reference)
                if url.scheme or url.netloc or not url.path:
                    continue
                decoded = unquote(url.path)
                target = ((self.root / decoded.lstrip("/")) if decoded.startswith("/")
                          else (page.parent / decoded)).resolve()
                label = f"{page.relative_to(self.root)} -> {reference}"
                self.check(target.is_relative_to(self.root), "HTML links",
                           f"Local HTML link escapes the curriculum folder: {label}")
                self.check(target.is_file(), "HTML links", f"Broken local HTML link: {label}")
                if target.is_file() and target.suffix.casefold() == ".pdf":
                    for raw_page in parse_qs(url.fragment).get("page", []):
                        valid_number = raw_page.isdigit()
                        self.check(valid_number, "PDF page links", f"Invalid PDF page number: {label}")
                        if valid_number:
                            self.check(1 <= int(raw_page) <= len(self.pdf(target).pages),
                                       "PDF page links", f"PDF page outside document range: {label}")

    @staticmethod
    def machine_local(reference: str) -> bool:
        decoded = unquote(reference).replace("\\", "/")
        url = urlsplit(decoded)
        if url.scheme.casefold() == "file":
            return True
        hostname = (url.hostname or "").casefold()
        if hostname == "localhost" or hostname.endswith(".localhost"):
            return True
        if hostname:
            try:
                if ipaddress.ip_address(hostname).is_loopback:
                    return True
            except ValueError:
                pass
        return bool(re.search(r"(?:^|file://)(?:/workspace(?:/|$)|/tmp(?:/|$)|/home(?:/|$)|[A-Za-z]:/)", decoded))

    def verify_generated_pdfs(self):
        for relative in ("unit-01/learner-workbook.pdf", "unit-01/instructor-guide.pdf"):
            self.require_file(relative, "generated PDFs")
        generated = sorted(path for path in self.root.rglob("*.pdf")
                           if not path.is_relative_to(self.root / "sources"))
        self.check(bool(generated), "generated PDFs", "No generated PDFs found")
        for path in generated:
            reader = self.pdf(path)
            relative = path.relative_to(self.root)
            self.check(bool(reader.pages), "generated PDFs", f"Generated PDF has no pages: {relative}")
            for index, page in enumerate(reader.pages, start=1):
                extracted = page.extract_text() or ""
                body_text = "\n".join(line for line in extracted.splitlines()
                                      if not line.startswith("ACCESS IS4S · Asphalt A1 ·"))
                self.check(bool(body_text.strip()), "readable PDF pages",
                           f"PDF page has no extractable text: {relative}, page {index}")
                for annotation in page.get("/Annots", []):
                    record = annotation.get_object()
                    pending = [record.get("/A", {})]
                    seen = set()
                    while pending:
                        action = pending.pop()
                        action = action.get_object() if hasattr(action, "get_object") else action
                        if isinstance(action, list):
                            pending.extend(action)
                            continue
                        if not hasattr(action, "get") or id(action) in seen:
                            continue
                        seen.add(id(action))
                        for key in ("/URI", "/F", "/UF"):
                            value = action.get(key)
                            if value is None:
                                continue
                            value = value.get_object() if hasattr(value, "get_object") else value
                            if isinstance(value, dict):
                                pending.append(value)
                                continue
                            reference = str(value)
                            self.check(not self.machine_local(reference), "PDF annotation links",
                                       f"Machine-local PDF link in {relative}, page {index}: {reference}")
                        if action.get("/Next"):
                            pending.append(action["/Next"])

    def run(self) -> int:
        for group, task in (
            ("sources", self.verify_sources),
            ("questions/skills", self.verify_questions_and_skills),
            ("practice data", self.verify_practice_data),
            ("HTML", self.verify_html),
            ("PDFs", self.verify_generated_pdfs),
        ):
            try:
                task()
            except Exception as error:
                self.errors.append(f"{group}: {type(error).__name__}: {error}")
        for name, count in self.counts.items():
            print(f"Checked {count:3d} {name}")
        for error in self.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        if self.errors:
            print(f"FAIL: {len(self.errors)} issue(s); {sum(self.counts.values())} checks attempted.")
            return 1
        print(f"PASS: {sum(self.counts.values())} offline checks; source, content and export checks passed.")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Curriculum folder (default: this tool's parent)")
    return Verifier(parser.parse_args().root).run()


if __name__ == "__main__":
    raise SystemExit(main())
