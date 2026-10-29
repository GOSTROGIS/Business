"""Install curated figure blocks into editable chapters from the visual manifest.

The blocks remain visible in Markdown/GitHub as well as both generated books.
Only marked blocks are replaced. Re-running does not duplicate any figures.
"""
from __future__ import annotations
from collections import defaultdict
from html import escape
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BLOCK = re.compile(r'\n*<!-- visual:[^\n]+ -->\n.*?\n<!-- /visual:[^\n]+ -->\n*', re.S)


def figure_block(row, source):
    image = os.path.relpath(ROOT / row['file'], source.parent)
    kind = row.get('kind', 'diagram')
    label = 'Teaching scene' if kind == 'scene' else 'Source figure' if kind == 'source-diagram' else 'Visual guide'
    return f'''<!-- visual:{row['id']} -->
<figure class="teaching-figure {kind}" data-visual="{row['id']}">
<div class="figure-art" tabindex="0" role="region" aria-label="{escape(row['after_heading'] + ' — visual', quote=True)}"><img src="{escape(image, quote=True)}" alt="{escape(row['alt'], quote=True)}" loading="eager" decoding="sync"></div>
<figcaption><span class="figure-label">{label}</span> {escape(row['caption'])} <a class="visual-original" href="{escape(image, quote=True)}">Open full-size visual</a></figcaption>
<details class="visual-description"><summary>Read the visual description</summary><p>{escape(row['alt'])}</p></details>
</figure>
<!-- /visual:{row['id']} -->'''


def install_visuals():
    manifest = json.loads((ROOT / 'assets/visuals-manifest.json').read_text())
    grouped = defaultdict(list)
    for row in manifest['figures']:
        grouped[row['source']].append(row)
    for source_name, rows in grouped.items():
        source = ROOT / source_name
        original = source.read_text()
        clean = BLOCK.sub('\n\n', original)
        lines = clean.splitlines()
        inserts = defaultdict(list)
        for row in rows:
            matches = [(i, len(m[1])) for i, line in enumerate(lines)
                       if (m := re.fullmatch(r'(#{1,6}) (.+)', line)) and m[2] == row['after_heading']]
            if len(matches) != 1:
                raise ValueError(f'Expected one insertion heading: {source_name}: {row["after_heading"]}')
            at, level = matches[0]
            position = at + 1
            if row.get('placement') == 'after_section':
                position = len(lines)
                for i in range(at + 1, len(lines)):
                    m = re.match(r'(#{1,6}) ', lines[i])
                    if m and len(m[1]) <= level:
                        position = i
                        break
            inserts[position].append(figure_block(row, source))
        for position in sorted(inserts, reverse=True):
            lines[position:position] = ['', '\n\n'.join(inserts[position]), '']
        revised = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).rstrip() + '\n'
        if revised != original:
            source.write_text(revised)
    return len(manifest['figures'])


if __name__ == '__main__':
    print(f'Installed {install_visuals()} curated figure placements')
