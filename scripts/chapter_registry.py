#!/usr/bin/env python3
"""Build a stable chapter identity registry from current reader chapter pages."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

NUMBER_RE = re.compile(r'<div class="number">CHAPTER\s+(\d+)</div>', re.I)
TITLE_RE = re.compile(r'<h1>(.*?)</h1>', re.I | re.S)


def _book_and_act(number: int) -> tuple[str, str]:
    if number <= 82:
        book = 'book-i'
        act = 'act-i' if number <= 20 else 'act-ii' if number <= 63 else 'act-iii'
    elif number <= 180:
        book = 'book-ii'
        act = 'act-i' if number <= 99 else 'act-ii' if number <= 137 else 'act-iii'
    else:
        book = 'book-iii'
        act = 'act-i' if number <= 219 else 'act-ii'
    return book, act


def _load_art(root: Path) -> dict[str, list[str]]:
    path = root / 'publishing/chapter_art_coverage.json'
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding='utf-8'))
    return {
        key: list(value.get('assets', []))
        for key, value in data.get('chapters', {}).items()
    }


def build_registry(root: Path) -> dict:
    root = root.resolve()
    art = _load_art(root)
    records = []
    for page in sorted((root / 'chapters').glob('[0-9][0-9][0-9].html')):
        text = page.read_text(encoding='utf-8')
        number_match = NUMBER_RE.search(text)
        title_match = TITLE_RE.search(text)
        number = int(number_match.group(1)) if number_match else int(page.stem)
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else f'CHAPTER {number}'
        book, act = _book_and_act(number)
        slug = f'chapters/{number:03d}.html'
        records.append({
            'chapter_id': f'plg-ch-{number:06d}',
            'origin_chapter_number': number,
            'current_display_number': number,
            'current_title': title,
            'book': book,
            'act': act,
            'status': 'active',
            'merged_into': None,
            'source_path': slug,
            'public_slug': slug,
            'legacy_slugs': [slug],
            'illustration_refs': art.get(f'{number:03d}', []),
            'notes': '',
        })
    ids = [row['chapter_id'] for row in records]
    numbers = [row['current_display_number'] for row in records]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate stable chapter ids')
    if len(numbers) != len(set(numbers)):
        raise ValueError('duplicate active display numbers')
    return {'schema_version': 1, 'chapters': records}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, default=Path('publishing/chapter_identity_registry.json'))
    parser.add_argument('--stdout', action='store_true')
    args = parser.parse_args()
    payload = build_registry(args.root)
    if args.stdout:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        output = args.output if args.output.is_absolute() else args.root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        print(f'wrote {len(payload["chapters"])} chapter identities to {output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
