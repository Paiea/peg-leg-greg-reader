#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import generate_light as gl
from reader_sections import book_and_act_for_chapter
from showcase import ShowcaseMap, build_showcase_map, load_showcase_manifest


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


def page_tag_text(text: str, tag: str) -> str:
    match = re.search(fr'<{tag}\b[^>]*>(.*?)</{tag}>', text, re.I | re.S)
    if not match:
        raise AssertionError(f'missing chapter {tag}')
    return html.unescape(re.sub(r'<[^>]+>', '', match.group(1))).strip()


def page_h1(text: str) -> str:
    return page_tag_text(text, 'h1')


def _range_label(showcase: ShowcaseMap, start: int, end: int) -> str:
    visible = [number for number in showcase.visible_canon if start <= number <= end]
    if not visible:
        raise AssertionError(f'no Showcase chapters in canonical range {start}-{end}')
    first = showcase.showcase_number(visible[0])
    last = showcase.showcase_number(visible[-1])
    return f'Chapters {first}–{last}'


def verify_reader_frontier(
    root: Path,
    *,
    expected_latest: int | None = None,
    expected_title: str | None = None,
) -> int:
    numbers = discover_published_chapters(root)
    canonical_latest = numbers[-1]
    if expected_latest is not None and canonical_latest != expected_latest:
        raise AssertionError(
            f'Illustrated frontier mismatch: published {canonical_latest}, manuscript authority {expected_latest}'
        )

    showcase = build_showcase_map(
        numbers,
        load_showcase_manifest(root / 'publishing' / 'showcase_chapters.json'),
    )
    if not showcase.visible_canon:
        raise AssertionError('Showcase has no visible published chapters')
    latest = showcase.visible_canon[-1]
    latest_display = showcase.showcase_number(latest)

    illustrated_page = root / 'chapters' / f'{latest:03d}.html'
    light_page = root / 'light' / f'{latest:03d}.html'
    if not illustrated_page.is_file():
        raise AssertionError(f'missing latest Showcase Illustrated page: {illustrated_page}')
    if not light_page.is_file():
        raise AssertionError(f'missing latest Showcase Text page: {light_page}')

    illustrated_text = illustrated_page.read_text(encoding='utf-8')
    light_text = light_page.read_text(encoding='utf-8')
    if expected_title is not None and latest == canonical_latest:
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
    if f'href="../chapters/{latest:03d}.html"' not in light_text:
        raise AssertionError('Text page does not link matching Illustrated chapter')

    if 'rel="next"' in illustrated_text:
        raise AssertionError('Illustrated latest next link should be disabled')
    if 'rel="next"' in light_text:
        raise AssertionError('Text latest next link should be disabled')

    previous = showcase.previous_visible(latest)
    if previous is not None:
        expected_previous = f'rel="prev" href="{previous:03d}.html"'
        if expected_previous not in illustrated_text:
            raise AssertionError('Illustrated latest previous link is stale')
        if expected_previous not in light_text:
            raise AssertionError('Text latest previous link is stale')

        illustrated_previous_page = root / 'chapters' / f'{previous:03d}.html'
        text_previous_page = root / 'light' / f'{previous:03d}.html'
        if not illustrated_previous_page.is_file():
            raise AssertionError('missing Illustrated previous Showcase page')
        if not text_previous_page.is_file():
            raise AssertionError('missing Text previous Showcase page')
        illustrated_previous_text = illustrated_previous_page.read_text(encoding='utf-8')
        text_previous_text = text_previous_page.read_text(encoding='utf-8')
        expected_next = f'rel="next" href="{latest:03d}.html"'
        if expected_next not in illustrated_previous_text:
            raise AssertionError('Illustrated previous Showcase next link is stale')
        if expected_next not in text_previous_text:
            raise AssertionError('Text previous Showcase next link is stale')
    elif 'rel="prev"' in illustrated_text or 'rel="prev"' in light_text:
        raise AssertionError('latest Showcase page has unexpected previous link')

    index_text = (root / 'index.html').read_text(encoding='utf-8')
    light_index_text = (root / 'light' / 'index.html').read_text(encoding='utf-8')
    try:
        current_book, current_act = book_and_act_for_chapter(latest)
    except ValueError as exc:
        raise AssertionError(str(exc)) from exc

    book_end = current_book.effective_end(latest)
    act_end = current_act.effective_end(latest)
    expected_book_range = _range_label(showcase, current_book.start, book_end)
    expected_act_range = f'{current_act.numeral} · {_range_label(showcase, current_act.start, act_end)}'

    for label, text in (('Illustrated index', index_text), ('Text index', light_index_text)):
        if current_book.numeral not in text:
            raise AssertionError(f'{label} is missing current {current_book.numeral}')
        if expected_book_range not in text:
            raise AssertionError(f'{label} is missing current Book range {expected_book_range}')
        if expected_act_range not in text:
            raise AssertionError(f'{label} is missing current Act range {expected_act_range}')
        if current_act.title not in text:
            raise AssertionError(f'{label} is missing current Act title {current_act.title}')

    if f'href="chapters/{latest:03d}.html"' not in index_text:
        raise AssertionError('Illustrated index does not link the latest Showcase chapter')
    if f'href="{latest:03d}.html">Read newest · Chapter {latest_display}' not in light_index_text:
        raise AssertionError('Text index newest-Showcase action is stale')

    latest_page = root / 'latest.html'
    if not latest_page.is_file():
        raise AssertionError('missing latest landing page')
    latest_text = latest_page.read_text(encoding='utf-8')
    if (
        f'href="light/{latest:03d}.html"' not in latest_text
        or f'Read Chapter {latest_display}' not in latest_text
    ):
        raise AssertionError('Latest landing page is stale')
    if page_h1(latest_text) != f'Chapter {latest_display}':
        raise AssertionError('Latest landing chapter number is stale')
    if expected_title is not None and latest == canonical_latest:
        if page_tag_text(latest_text, 'h2') != expected_title:
            raise AssertionError('Latest landing title is stale')

    manifest_path = root / 'light' / 'manifest.json'
    if not manifest_path.is_file():
        raise AssertionError('missing Text manifest')
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError) as exc:
        raise AssertionError('invalid Text manifest') from exc
    if manifest.get('latest') != latest:
        raise AssertionError('Text manifest latest field is stale')
    if manifest.get('latest_showcase') not in {None, latest_display}:
        raise AssertionError('Text manifest latest_showcase field is stale')
    entries = manifest.get('chapters')
    if not isinstance(entries, list):
        raise AssertionError('Text manifest chapters field is invalid')
    if any(isinstance(entry, dict) and entry.get('number', 0) > canonical_latest for entry in entries):
        raise AssertionError('Text manifest contains chapter beyond published frontier')

    manifest_numbers = sorted(
        entry.get('number')
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get('number'), int)
    )
    if not manifest_numbers:
        raise AssertionError('Text manifest chapter range is empty')
    expected_manifest_numbers = [
        number for number in showcase.visible_canon
        if manifest_numbers[0] <= number <= latest
    ]
    if manifest_numbers != expected_manifest_numbers:
        raise AssertionError('Text manifest chapter range does not match Showcase visibility')

    frontier_entries = [
        entry for entry in entries
        if isinstance(entry, dict) and entry.get('number') == latest
    ]
    if len(frontier_entries) != 1:
        raise AssertionError('Text manifest frontier entry is stale')
    frontier_entry = frontier_entries[0]
    expected_manifest_title = expected_title if expected_title is not None and latest == canonical_latest else page_h1(light_text)
    if (
        frontier_entry.get('title') != expected_manifest_title
        or frontier_entry.get('path') != f'{latest:03d}.html'
        or frontier_entry.get('showcase_number', latest_display) != latest_display
    ):
        raise AssertionError('Text manifest frontier entry is stale')

    return canonical_latest


def main() -> int:
    all_chapters = gl.load_all_sources()
    if not all_chapters:
        raise SystemExit('no manuscript chapters found')
    manuscript_latest = max(all_chapters)
    manuscript_title = all_chapters[manuscript_latest].title
    try:
        canonical_latest = verify_reader_frontier(
            Path('.'),
            expected_latest=manuscript_latest,
            expected_title=manuscript_title,
        )
    except AssertionError as exc:
        raise SystemExit(str(exc)) from exc
    print(f'verified canonical reader frontier through Chapter {canonical_latest} and Showcase public frontier')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
