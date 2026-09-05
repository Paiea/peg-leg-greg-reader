#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from pathlib import Path

import generate_light as gl


def discover_published_chapters(root: Path) -> list[int]:
    chapters_dir = root / 'chapters'
    numbers = sorted(
        int(path.stem)
        for path in chapters_dir.glob('[0-9][0-9][0-9].html')
        if path.stem.isdigit()
    )
    if not numbers:
        raise AssertionError('no published Illustrated chapters found')
    if numbers[0] != 1:
        raise AssertionError(f'published chapters start at {numbers[0]}, expected 1')
    published = set(numbers)
    for number in range(1, numbers[-1] + 1):
        if number not in published:
            raise AssertionError(f'missing published chapter {number}')
    return numbers


def page_h1(text: str) -> str:
    match = re.search(r'<h1\b[^>]*>(.*?)</h1>', text, re.I | re.S)
    if not match:
        raise AssertionError('missing chapter h1')
    return html.unescape(re.sub(r'<[^>]+>', '', match.group(1))).strip()


def verify_reader_frontier(
    root: Path,
    *,
    expected_latest: int | None = None,
    expected_title: str | None = None,
) -> int:
    numbers = discover_published_chapters(root)
    latest = numbers[-1]
    if expected_latest is not None and latest != expected_latest:
        raise AssertionError(
            f'Illustrated frontier mismatch: published {latest}, manuscript authority {expected_latest}'
        )

    illustrated_page = root / 'chapters' / f'{latest:03d}.html'
    light_page = root / 'light' / f'{latest:03d}.html'
    if not illustrated_page.is_file():
        raise AssertionError(f'missing latest Illustrated page: {illustrated_page}')
    if not light_page.is_file():
        raise AssertionError(f'missing latest Text page: {light_page}')

    illustrated_text = illustrated_page.read_text(encoding='utf-8')
    light_text = light_page.read_text(encoding='utf-8')
    if expected_title is not None:
        illustrated_title = page_h1(illustrated_text)
        if illustrated_title != expected_title:
            raise AssertionError(
                f'Illustrated title mismatch: expected {expected_title!r}, found {illustrated_title!r}'
            )
        text_title = page_h1(light_text)
        if text_title != expected_title:
            raise AssertionError(
                f'Text title mismatch: expected {expected_title!r}, found {text_title!r}'
            )

    if f'href="../light/{latest:03d}.html"' not in illustrated_text:
        raise AssertionError('Illustrated page does not link matching Text chapter')

    index_text = (root / 'index.html').read_text(encoding='utf-8')
    light_index_text = (root / 'light' / 'index.html').read_text(encoding='utf-8')
    expected_book_range = f'Chapters 321–{latest}'
    expected_act_range = f'ACT II · Chapters 331–{latest}'

    for label, text in (('Illustrated index', index_text), ('Text index', light_index_text)):
        if 'BOOK IV' not in text:
            raise AssertionError(f'{label} is missing BOOK IV')
        if expected_book_range not in text:
            raise AssertionError(f'{label} is missing current Book IV range {expected_book_range}')
        if latest >= 331 and expected_act_range not in text:
            raise AssertionError(f'{label} is missing current Act II range {expected_act_range}')

    if f'href="chapters/{latest:03d}.html"' not in index_text:
        raise AssertionError('Illustrated index does not link the latest chapter')
    if f'href="{latest:03d}.html">Read newest · Chapter {latest}' not in light_index_text:
        raise AssertionError('Text index newest-chapter action is stale')

    return latest


def main() -> int:
    all_chapters = gl.load_all_sources()
    if not all_chapters:
        raise SystemExit('no manuscript chapters found')
    manuscript_latest = max(all_chapters)
    manuscript_title = all_chapters[manuscript_latest].title
    try:
        latest = verify_reader_frontier(
            Path('.'),
            expected_latest=manuscript_latest,
            expected_title=manuscript_title,
        )
    except AssertionError as exc:
        raise SystemExit(str(exc)) from exc
    print(f'verified reader frontier through Chapter {latest}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
