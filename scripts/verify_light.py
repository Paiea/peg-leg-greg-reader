#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import generate_light as gl


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
    wanted = gl.selected_numbers(spec, all_chapters)
    manifest_path = Path('light/manifest.json')
    if not manifest_path.exists():
        fail('missing light/manifest.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    entries = manifest.get('chapters', [])
    numbers = [int(item['number']) for item in entries]
    if len(numbers) != len(set(numbers)):
        fail('duplicate chapter number in Light manifest')
    generated = set(numbers)

    numeric_pages = {
        int(path.stem)
        for path in Path('light').glob('[0-9][0-9][0-9].html')
        if path.stem.isdigit()
    }
    orphans = sorted(numeric_pages - generated)
    if orphans:
        fail(f'orphan generated Light pages: {orphans[:12]}')

    missing = [n for n in wanted if n not in generated]
    if missing:
        fail(f'missing generated Light chapters: {missing[:12]}')

    all_numbers = sorted(all_chapters)
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

        idx = all_numbers.index(number)
        if idx > 0:
            prev = all_numbers[idx - 1]
            if f'href="{expected_href(prev, generated)}"' not in text:
                fail(f'Chapter {number}: previous link mismatch')
        if idx + 1 < len(all_numbers):
            nxt = all_numbers[idx + 1]
            if f'href="{expected_href(nxt, generated)}"' not in text:
                fail(f'Chapter {number}: next link mismatch')

    latest = max(all_chapters) if all_chapters else None
    if manifest.get('latest') != latest:
        fail(f'manifest latest mismatch: expected {latest}, found {manifest.get("latest")}')
    if latest is not None:
        latest_html = Path('latest.html').read_text(encoding='utf-8')
        target = f'light/{latest:03d}.html' if latest in generated else f'light.html?chapter={latest}'
        if f'href="{target}"' not in latest_html:
            fail('latest.html does not point to current endpoint')

    print(f'verified {len(wanted)} Light chapters for {spec}')
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        fail('usage: python scripts/verify_light.py current|N-N')
    return verify(sys.argv[1])


if __name__ == '__main__':
    raise SystemExit(main())
