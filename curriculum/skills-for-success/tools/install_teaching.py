"""Integrate complete practice materials into the editable book chapters.

teaching-manifest.json identifies authoring inputs and their chapter positions.
Only managed teaching blocks are replaced; other chapter prose is preserved.
Relative links are rebased so a chapter remains independently readable.
"""
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
BLOCK = re.compile(r'\n*<!-- teaching:[^\n]+ -->\n.*?\n<!-- /teaching:[^\n]+ -->\n*', re.S)


def integrated_text(source, target, offset=1, section=None, include_intro=False):
    text = source.read_text(encoding='utf-8').strip()
    if section:
        lines = text.splitlines()
        matches = [(i, len(m[1])) for i, line in enumerate(lines)
                   if (m := re.fullmatch(r'(#{1,6}) (.+)', line)) and m[2] == section]
        if len(matches) != 1:
            raise ValueError(f'Expected one source section: {source}: {section}')
        start, level = matches[0]
        end = len(lines)
        for i in range(start + 1, len(lines)):
            m = re.match(r'(#{1,6}) ', lines[i])
            if m and len(m[1]) <= level:
                end = i
                break
        selected = lines[start:end]
        if include_intro:
            first_section = next((i for i, line in enumerate(lines[1:], 1) if re.match(r'^#{1,6} ', line)), len(lines))
            selected[1:1] = [''] + lines[1:first_section]
        # The chosen section becomes the top-level title of this input block.
        selected = [re.sub(r'^#{' + str(level - 1) + r'}(?=# )', '', line) if level > 1 else line for line in selected]
        # Demote nested headings by the same amount without touching ordinary text.
        selected = [re.sub(r'^(#{' + str(level) + r',6}) ', lambda m: '#' * (len(m[1]) - level + 1) + ' ', line)
                    if level > 1 else line for line in selected]
        text = '\n'.join(selected)
    # Figures are installed from the canonical visual manifest after this pass.
    text = re.sub(r'\n*<!-- visual:[^\n]+ -->\n.*?\n<!-- /visual:[^\n]+ -->\n*', '\n\n', text, flags=re.S)
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            char = marker[1][0]
            fence = None if fence == char else char if fence is None else fence
        elif not fence:
            match = re.match(r'^(#{1,6}) (.*)', line)
            if match:
                level = len(match[1]) + offset
                if level > 6:
                    raise ValueError(f'Heading too deep when integrating {source}')
                line = '#' * level + ' ' + match[2]
        lines.append(line)
    text = '\n'.join(lines)

    def relative(href):
        if not href or href.startswith(('#', '//')) or urlsplit(href).scheme:
            return href
        path, sep, fragment = href.partition('#')
        resolved = (source.parent / path).resolve()
        result = os.path.relpath(resolved, target.parent)
        return result + (sep + fragment if sep else '')

    text = re.sub(r'(\[[^\]\n]*\]\()([^\s)]+)(\))', lambda m: m[1] + relative(m[2]) + m[3], text)
    text = re.sub(r'((?:href|src)=")([^"]+)(")', lambda m: m[1] + relative(m[2]) + m[3], text)
    return text


def install_teaching():
    path = ROOT / 'teaching-manifest.json'
    if not path.exists():
        return 0
    rows = json.loads(path.read_text())['blocks']
    groups = defaultdict(list)
    for row in rows:
        groups[row['target']].append(row)
    for name, blocks in groups.items():
        target = ROOT / name
        original = target.read_text()
        clean = BLOCK.sub('\n\n', original)
        lines = clean.splitlines()
        insertions = defaultdict(list)
        for row in blocks:
            text = integrated_text(ROOT / row['source'], target, row.get('heading_offset', 1),
                                   row.get('source_section'), row.get('include_intro', False))
            block = f'<!-- teaching:{row["id"]} -->\n{text}\n<!-- /teaching:{row["id"]} -->'
            if row.get('placement', 'append') == 'append':
                position = len(lines)
            else:
                matches = [i for i, line in enumerate(lines) if re.fullmatch(r'#{1,6} ' + re.escape(row['before_heading']), line)]
                if len(matches) != 1:
                    raise ValueError(f'Expected one teaching insertion heading: {name}: {row["before_heading"]}')
                position = matches[0]
            insertions[position].append(block)
        for position in sorted(insertions, reverse=True):
            lines[position:position] = ['', '\n\n'.join(insertions[position]), '']
        revised = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).rstrip() + '\n'
        if revised != original:
            target.write_text(revised)
    return len(rows)


if __name__ == '__main__':
    print(f'Integrated {install_teaching()} teaching blocks')
