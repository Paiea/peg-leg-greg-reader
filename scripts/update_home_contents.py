#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path

from showcase import ShowcaseMap, build_showcase_map, load_showcase_manifest

START = '<!-- READER BOOK CONTENTS START -->'
END = '<!-- READER BOOK CONTENTS END -->'
BOOKS_TOC_OPEN = '<section aria-labelledby="books-heading" class="toc toc-acts" id="books">'
LEGACY_TOC_OPEN = '<section aria-labelledby="chapters-heading" class="toc toc-acts" id="chapters">'
BOOK_CSS = '<link href="assets/book-contents.css" rel="stylesheet"/>'
R2_HOME_LINK = '<a class="tertiary-action" href="r2/">R2 · Run 2</a>'
THIRD_LEG_HOME_LINK = '<a class="tertiary-action" href="3l/">3L · The Third Leg</a>'
SHOWCASE_MANIFEST = Path('publishing/showcase_chapters.json')


def parse_chapter_index(text: str) -> dict[int, str]:
    chapters: dict[int, str] = {}
    for match in re.finditer(r'^\s*(?:[-*]\s*)?(\d+)\.\s+\*\*(.+?)\*\*\s*$', text, re.MULTILINE):
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


def ensure_project_routes(text: str) -> str:
    if THIRD_LEG_HOME_LINK in text:
        return text
    if R2_HOME_LINK not in text:
        raise ValueError('R2 home link not found in index.html')
    return text.replace(R2_HOME_LINK, R2_HOME_LINK + THIRD_LEG_HOME_LINK, 1)


def upgrade_home_book_labels(text: str) -> str:
    text = text.replace('href="#chapters">Chapters</a>', 'href="#books">Illustrated Reader</a>')
    text = text.replace('aria-labelledby="chapters-heading" class="home-chapters"', 'aria-labelledby="books-heading" class="home-chapters"')
    text = text.replace('<p class="home-kicker">Read straight through</p>', '<p class="home-kicker">The novel</p>')
    text = text.replace('<h2 id="chapters-heading">Chapters</h2>', '<h2 id="books-heading">Books</h2>')
    return ensure_project_routes(text)


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
    showcase: ShowcaseMap | None = None,
) -> str:
    from reader_sections import render_book_sections

    visible_numbers = [
        number for number in sorted(chapters)
        if showcase is None or showcase.showcase_number(number) is not None
    ]
    display_numbers = (
        {number: showcase.showcase_number(number) for number in visible_numbers}
        if showcase is not None else None
    )
    links = {
        number: (
            f'<a href="{chapter_href(number)}">'
            f'<span class="num">{(display_numbers[number] if display_numbers else number):02d}</span>'
            f'<span class="title">{html.escape(chapters[number].title())}</span>'
            f'</a>'
        )
        for number in visible_numbers
    }
    return render_book_sections(
        links,
        illustrated=illustrated,
        open_first_act=True,
        display_numbers=display_numbers,
    )


def main() -> int:
    from generate_light import load_all_sources

    chapter_index = Path('state/MANUSCRIPT_CHAPTER_INDEX.md')
    light_manifest = Path('light/manifest.json')
    index_path = Path('index.html')

    chapters = parse_chapter_index(chapter_index.read_text(encoding='utf-8'))
    chapters.update(load_manifest_chapters(light_manifest))
    exact_sources = load_all_sources()
    chapters.update({number: chapter.title for number, chapter in exact_sources.items()})
    showcase = build_showcase_map(sorted(exact_sources), load_showcase_manifest(SHOWCASE_MANIFEST))

    original = index_path.read_text(encoding='utf-8')
    rendered = render_home_contents(chapters, illustrated=True, showcase=showcase)
    updated = ensure_stylesheet(patch_home_contents(original, rendered))
    if updated != original:
        index_path.write_text(updated, encoding='utf-8')
        visible_count = len([n for n in showcase.visible_canon if n in chapters])
        print(f'updated illustrated Book/Act contents with {visible_count} showcase chapters')
    else:
        print('illustrated Book/Act contents already current')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
