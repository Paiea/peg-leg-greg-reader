#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


REPLACEMENTS = (
    ('<title>Light Edition — Peg-Leg Greg</title>', '<title>Text Reader — Peg-Leg Greg</title>'),
    ('Peg-Leg Greg Light edition: fast, text-first chapters without illustrations.', 'Peg-Leg Greg Text Reader: fast, text-only chapters without illustrations.'),
    ('text-first Light edition.', 'Text Reader.'),
    ('>Read Light<', '>Text Reader<'),
    ('>Chapter List<', '>Chapters<'),
    ('>ILLUSTRATED<', '>ILLUSTRATED READER<'),
    ('>LIGHT<', '>TEXT READER<'),
    ('LIGHT EDITION · CHAPTER', 'TEXT READER · CHAPTER'),
    ('LIGHT EDITION</div>', 'TEXT READER</div>'),
    ('<h1>Light Edition</h1>', '<h1>Text Reader</h1>'),
    ('Illustrated edition</a>', 'Illustrated Reader</a>'),
    ('Illustrated version</a>', 'Illustrated Reader</a>'),
    ('Text-first edition · no chapter illustrations', 'Text-only reading · no chapter illustrations'),
    ('Text-first reading with no chapter illustrations.', 'Text-only reading with no chapter illustrations.'),
    ('Fast, text-first Peg-Leg Greg with no chapter illustrations. Built for quick loading and uninterrupted reading.', 'Text-only Peg-Leg Greg with no chapter illustrations. Built for quick loading and uninterrupted reading.'),
    ('Browse the Light chapter list.', 'Browse the Text Reader chapter list.'),
    ('Light TOC', 'Chapters'),
    ('Light reader navigation', 'Text Reader navigation'),
    ('Light reader table of contents', 'Text Reader table of contents'),
    ('Light chapter sections', 'Text Reader chapter sections'),
    ('The newest chapter in the text-first edition.', 'The newest chapter in the Text Reader.'),
    ('Browse the Light edition', 'Browse the Text Reader'),
    ('— Peg-Leg Greg Light</title>', '— Peg-Leg Greg Text Reader</title>'),
)


def normalize_text(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text


def candidate_paths() -> list[Path]:
    paths = [Path('index.html'), Path('light.html'), Path('latest.html')]
    light_dir = Path('light')
    if light_dir.exists():
        paths.extend(sorted(light_dir.glob('*.html')))
    return paths


def main() -> int:
    changed = 0
    for path in candidate_paths():
        if not path.exists():
            continue
        original = path.read_text(encoding='utf-8')
        updated = normalize_text(original)
        if updated != original:
            path.write_text(updated, encoding='utf-8')
            changed += 1
    print(f'normalized reader labels in {changed} files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
