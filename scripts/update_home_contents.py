#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path

START = '<!-- READER BOOK CONTENTS START -->'
END = '<!-- READER BOOK CONTENTS END -->'
BOOKS_TOC_OPEN = '<section aria-labelledby="books-heading" class="toc toc-acts" id="books">'
LEGACY_TOC_OPEN = '<section aria-labelledby="chapters-heading" class="toc toc-acts" id="chapters">'
BOOK_CSS = '<link href="assets/book-contents.css" rel="stylesheet"/>'


def parse_chapter_index(text: str) -> dict[int, str]:
    chapters: dict[int, str] = {}
    for match in re.finditer(r'^(\d+)\.\s+\*\*(.+?)\*\*\s*$', text, re.MULTILINE):
        chapters[int(match.group(1))] = match.group(2).strip()
    if not chapters:
        raise ValueError('no chapters found in manuscript chapter index')
    return chapters


def load_manifest_chapters(path: Path) -> dict[int, str]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding='utf-8'))
    chapters: dict[int, str] = {}
    for item in data.get('chapters', []):
        number = item.get('number')
        title = item.get('title')
        if isinstance(number, int) and isinstance(title, str) and title.strip():
            chapters[number] = title.strip()
    return chapters


def chapter_href(number: int) -> str:
    # This is the Illustrated Reader contents page. Its chapter grid must stay
    # in illustrated mode instead of silently routing later chapters to Light.
    return f'chapters/{number:03d}.html'


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


def upgrade_home_book_labels(text: str) -> str:
    text = text.replace('href="#chapters">Chapters</a>', 'href="#books">Illustrated Reader</a>')
    text = text.replace('aria-labelledby="chapters-heading" class="home-chapters"', 'aria-labelledby="books-heading" class="home-chapters"')
    text = text.replace('<p class="home-kicker">Read straight through</p>', '<p class="home-kicker">The novel</p>')
    text = text.replace('<h2 id="chapters-heading">Chapters</h2>', '<h2 id="books-heading">Books</h2>')
    return text


def patch_home_contents(text: str, rendered_books: str) -> str:
    replacement = f'{START}\n{BOOKS_TOC_OPEN}{rendered_books}</section>\n{END}'
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        return upgrade_home_book_labels(before + replacement + after)

    for toc_open in (BOOKS_TOC_OPEN, LEGACY_TOC_OPEN):
        start = text.find(toc_open)
        if start >= 0:
            end = _find_section_end(text, start)
            return upgrade_home_book_labels(text[:start] + replacement + text[end:])
    raise ValueError('illustrated contents section not found')


def render_home_contents(
    chapters: dict[int, str],
    *,
    illustrated: bool = True,
) -> str:
    from reader_sections import render_book_sections

    links = {
        number: (
            f'<a href="{chapter_href(number)}">'
            f'<span class="num">{number:02d}</span>'
            f'<span class="title">{html.escape(title.title())}</span>'
            f'</a>'
        )
        for number, title in sorted(chapters.items())
    }
    return render_book_sections(links, illustrated=illustrated, open_first_act=True)


def main() -> int:
    chapter_index = Path('state/MANUSCRIPT_CHAPTER_INDEX.md')
    light_manifest = Path('light/manifest.json')
    index_path = Path('index.html')

    # Preserve the durable early chapter index, then let the generated manifest
    # extend and refresh it. The handwritten index has historically lagged the
    # manuscript endpoint, while the manifest is generated from exact authority.
    chapters = parse_chapter_index(chapter_index.read_text(encoding='utf-8'))
    chapters.update(load_manifest_chapters(light_manifest))

    original = index_path.read_text(encoding='utf-8')
    rendered = render_home_contents(chapters, illustrated=True)
    updated = ensure_stylesheet(patch_home_contents(original, rendered))
    if updated != original:
        index_path.write_text(updated, encoding='utf-8')
        print(f'updated illustrated Book/Act contents through Chapter {max(chapters)}')
    else:
        print('illustrated Book/Act contents already current')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
