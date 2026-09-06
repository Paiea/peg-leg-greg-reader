#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import generate_light as gl
from showcase import build_showcase_map, load_showcase_manifest


def fail(message: str) -> None:
    raise SystemExit(message)


def page_body(text: str) -> str:
    match = re.search(r'<article\b[^>]*\blight-prose\b[^>]*>(.*?)</article>', text, re.I | re.S)
    if not match:
        fail('missing Light prose article')
    return match.group(1).strip()


def page_title(text: str) -> str:
    match = re.search(r'<header\b[^>]*class="light-chapter-title"[^>]*>.*?<h1>(.*?)</h1>', text, re.I | re.S)
    if not match:
        fail('missing Light chapter title')
    return html.unescape(re.sub(r'<[^>]+>', '', match.group(1))).strip()


def expected_href(number: int, generated: set[int]) -> str:
    return f'{number:03d}.html' if number in generated else f'../light.html?chapter={number}'


def verify(spec: str) -> int:
    all_chapters = gl.load_all_sources()
    showcase = build_showcase_map(
        sorted(all_chapters),
        load_showcase_manifest(gl.SHOWCASE_MANIFEST),
    )
    requested = gl.selected_numbers(spec, all_chapters)
    wanted = [number for number in requested if showcase.showcase_number(number) is not None]

    manifest_path = Path('light/manifest.json')
    if not manifest_path.exists():
        fail('missing light/manifest.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    entries = manifest.get('chapters', [])
    numbers = [int(item['number']) for item in entries]
    if len(numbers) != len(set(numbers)):
        fail('duplicate chapter number in Light manifest')
    generated = set(numbers)

    hidden_in_manifest = sorted(
        number for number in generated
        if showcase.showcase_number(number) is None
    )
    if hidden_in_manifest:
        fail(f'hidden canonical chapters leaked into Light manifest: {hidden_in_manifest[:12]}')

    numeric_pages = {
        int(path.stem)
        for path in Path('light').glob('[0-9][0-9][0-9].html')
        if path.stem.isdigit()
    }
    unknown_pages = sorted(numeric_pages - set(all_chapters))
    if unknown_pages:
        fail(f'orphan generated Light pages: {unknown_pages[:12]}')

    missing = [n for n in wanted if n not in generated]
    if missing:
        fail(f'missing generated Light chapters: {missing[:12]}')

    for number in wanted:
        chapter = all_chapters[number]
        path = Path('light') / f'{number:03d}.html'
        if not path.exists():
            fail(f'Chapter {number}: generated page missing')
        text = path.read_text(encoding='utf-8')
        if page_title(text) != chapter.title:
            fail(f'Chapter {number}: title mismatch')
        if page_body(text) != chapter.prose_html.strip():
            fail(f'Chapter {number}: prose mismatch')
        if '<img' in text.lower():
            fail(f'Chapter {number}: illustration leaked into Light page')
        lower = text.lower()
        if 'peg_leg_greg_running_manuscript.md' in lower or 'peg_leg_greg_recovered_ch156-219_exact.md' in lower:
            fail(f'Chapter {number}: source manuscript path leaked into Light page')
        if 'href="../index.html"' not in text or 'href="index.html"' not in text:
            fail(f'Chapter {number}: HOME or TOC link missing')

        previous_number = showcase.previous_visible(number)
        next_number = showcase.next_visible(number)
        if previous_number is not None:
            if f'href="{expected_href(previous_number, generated)}"' not in text:
                fail(f'Chapter {number}: previous showcase link mismatch')
            previous_display = showcase.showcase_number(previous_number)
            if f'Chapter {previous_display}</a>' not in text:
                fail(f'Chapter {number}: previous showcase label mismatch')
        elif 'rel="prev"' in text:
            fail(f'Chapter {number}: previous link crosses a showcase boundary or authority gap')
        if next_number is not None:
            if f'href="{expected_href(next_number, generated)}"' not in text:
                fail(f'Chapter {number}: next showcase link mismatch')
            next_display = showcase.showcase_number(next_number)
            if f'Chapter {next_display} →</a>' not in text:
                fail(f'Chapter {number}: next showcase label mismatch')
        elif 'rel="next"' in text:
            fail(f'Chapter {number}: next link crosses a showcase boundary or authority gap')

    visible = [number for number in showcase.visible_canon if number in all_chapters]
    latest = visible[-1] if visible else None
    latest_display = showcase.showcase_number(latest) if latest is not None else None
    if manifest.get('latest') != latest:
        fail(f'manifest latest mismatch: expected {latest}, found {manifest.get("latest")}')
    if manifest.get('latest_showcase') not in {None, latest_display}:
        fail(
            f'manifest latest_showcase mismatch: expected {latest_display}, '
            f'found {manifest.get("latest_showcase")}'
        )
    if latest is not None:
        latest_html = Path('latest.html').read_text(encoding='utf-8')
        target = f'light/{latest:03d}.html' if latest in generated else f'light.html?chapter={latest}'
        if f'href="{target}"' not in latest_html:
            fail('latest.html does not point to current showcase endpoint')

    print(f'verified {len(wanted)} showcase Light chapters for {spec}')
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        fail('usage: python scripts/verify_light.py current|N-N')
    return verify(sys.argv[1])


if __name__ == '__main__':
    raise SystemExit(main())
