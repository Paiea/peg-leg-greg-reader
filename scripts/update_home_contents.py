#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path

START = '<!-- READER BOOK CONTENTS START -->'
END = '<!-- READER BOOK CONTENTS END -->'
TOC_OPEN = '<section aria-labelledby="chapters-heading" class="toc toc-acts" id="chapters">'
BOOK_CSS = '<link href="assets/book-contents.css" rel="stylesheet"/>'


def parse_chapter_index(text: str) -> dict[int, str]:
    chapters: dict[int, str] = {}
    for match in re.finditer(r'^(\d+)\.\s+\*\*(.+?)\*\*\s*$', text, re.MULTILINE):
        chapters[int(match.group(1))] = match.group(2).strip()
    if not chapters:
        raise ValueError('no chapters found in manuscript chapter index')
    return chapters


def chapter_href(number: int, generated_light: set[int]) -> str:
    if number <= 155:
        return f'chapters/{number:03d}.html'
    if number in generated_light:
        return f'light/{number:03d}.html'
    return f'light.html?chapter={number}'


def _find_section_end(text: str, start: int) -> int:
    depth = 0
    for match in re.finditer(r'</?section\b[^>]*>', text[start:], re.IGNORECASE):
        tag = match.group(0)
        if tag.startswith('</'):
            depth -= 1
            if depth == 0:
                return start + match.end()
        else:
            depth += 1
    raise ValueError('could not find closing </section> for reader contents')


def ensure_stylesheet(text: str) -> str:
    if BOOK_CSS in text:
        return text
    reader_css = '<link href="assets/reader.css" rel="stylesheet"/>'
    if reader_css not in text:
        raise ValueError('reader.css link not found in index.html')
    return text.replace(reader_css, reader_css + '\n' + BOOK_CSS, 1)


def patch_home_contents(text: str, rendered_books: str) -> str:
    replacement = f'{START}\n{TOC_OPEN}{rendered_books}</section>\n{END}'
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        return before + replacement + after

    start = text.find(TOC_OPEN)
    if start < 0:
        raise ValueError('illustrated contents section not found')
    end = _find_section_end(text, start)
    return text[:start] + replacement + text[end:]


def render_home_contents(
    chapters: dict[int, str],
    generated_light: set[int],
    *,
    illustrated: bool = True,
) -> str:
    from reader_sections import render_book_sections

    links = {
        number: (
            f'<a href="{chapter_href(number, generated_light)}">'
            f'<span class="num">{number:02d}</span>'
            f'<span class="title">{html.escape(title.title())}</span>'
            f'</a>'
        )
        for number, title in sorted(chapters.items())
    }
    return render_book_sections(links, illustrated=illustrated, open_first_act=True)


def load_generated_light(path: Path) -> set[int]:
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding='utf-8'))
    return {
        int(item['number'])
        for item in data.get('chapters', [])
        if str(item.get('number', '')).isdigit()
    }


def main() -> int:
    chapter_index = Path('state/MANUSCRIPT_CHAPTER_INDEX.md')
    light_manifest = Path('light/manifest.json')
    index_path = Path('index.html')

    chapters = parse_chapter_index(chapter_index.read_text(encoding='utf-8'))
    generated_light = load_generated_light(light_manifest)
    original = index_path.read_text(encoding='utf-8')
    rendered = render_home_contents(chapters, generated_light, illustrated=True)
    updated = ensure_stylesheet(patch_home_contents(original, rendered))
    if updated != original:
        index_path.write_text(updated, encoding='utf-8')
        print(f'updated illustrated Book/Act contents through Chapter {max(chapters)}')
    else:
        print('illustrated Book/Act contents already current')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
