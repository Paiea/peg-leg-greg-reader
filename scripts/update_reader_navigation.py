#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reader_sections import render_book_sections

LIGHT_ACTION = '<a class="secondary-action" href="light/index.html">Read Light</a>'
BEGIN_ACTION = '<a class="start primary-action" href="chapters/001.html">Begin Reading</a>'
TOC_RE = re.compile(
    r'<section\b(?=[^>]*\bclass="[^"]*\btoc\b[^"]*")(?=[^>]*\bid="chapters")[^>]*>.*?</section>',
    re.IGNORECASE | re.DOTALL,
)
CHAPTER_LINK_RE = re.compile(
    r'<a\b[^>]*href="chapters/(?P<number>\d{3})\.html"[^>]*>.*?</a>',
    re.IGNORECASE | re.DOTALL,
)
TITLE_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.IGNORECASE | re.DOTALL)


def chapter_link_from_file(path: Path) -> tuple[int, str] | None:
    if not path.stem.isdigit():
        return None
    number = int(path.stem)
    text = path.read_text(encoding='utf-8')
    match = TITLE_RE.search(text)
    if not match:
        return None
    title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
    title = html.unescape(title).title()
    link = (
        f'<a href="chapters/{number:03d}.html">'
        f'<span class="num">{number:02d}</span>'
        f'<span class="title">{html.escape(title)}</span>'
        '</a>'
    )
    return number, link


def group_illustrated_toc(text: str, root: Path) -> str:
    match = TOC_RE.search(text)
    if not match:
        return text
    current = match.group(0)
    chapter_links: dict[int, str] = {}
    for link_match in CHAPTER_LINK_RE.finditer(current):
        chapter_links[int(link_match.group('number'))] = link_match.group(0)
    chapters_dir = root / 'chapters'
    if chapters_dir.exists():
        for path in sorted(chapters_dir.glob('[0-9][0-9][0-9].html')):
            discovered = chapter_link_from_file(path)
            if discovered:
                number, link = discovered
                chapter_links[number] = link
    if not chapter_links:
        return text
    grouped = (
        '<section aria-labelledby="chapters-heading" class="toc toc-acts" id="chapters">'
        + render_book_sections(chapter_links, include_heroes=True, open_first_act=True)
        + '</section>'
    )
    return text[:match.start()] + grouped + text[match.end():]


def patch_home(path: Path) -> bool:
    original = path.read_text(encoding='utf-8')
    updated = original
    if LIGHT_ACTION not in updated:
        if BEGIN_ACTION not in updated:
            raise SystemExit(f'could not find homepage Begin Reading action in {path}')
        updated = updated.replace(BEGIN_ACTION, BEGIN_ACTION + LIGHT_ACTION, 1)
    updated = group_illustrated_toc(updated, path.parent)
    if updated == original:
        return False
    path.write_text(updated, encoding='utf-8')
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description='Keep homepage reading modes and book/act contents navigation current.')
    parser.add_argument('homepage', nargs='?', default='index.html')
    args = parser.parse_args()
    changed = patch_home(Path(args.homepage))
    print('updated homepage reader presentation' if changed else 'homepage reader presentation already current')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
