#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import one_off_renumber_after_220_v2 as migration

ROOT = Path(__file__).resolve().parents[1]


def rewrite_production_refs_only() -> None:
    skip = {p.resolve() for _, _, p in migration.ABC.values()}
    skip.add(migration.INDEX.resolve())
    for path in ROOT.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in migration.TEXT_SUFFIXES:
            continue
        if '.git' in path.parts or 'tests' in path.parts or '.github' in path.parts:
            continue
        if path.resolve() in skip or path.name.startswith('one_off_renumber_after_220'):
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        new = migration.rewrite_contextual_refs(text)
        if new != text:
            path.write_text(new, encoding='utf-8')


def update_role_card_and_contract_test() -> None:
    migration.update_book_role_card_original()
    test_path = ROOT / 'tests/test_reader_sections.py'
    text = test_path.read_text(encoding='utf-8')
    text = text.replace('book-iii-magistrate-231.webp', 'book-iii-magistrate-234.webp')
    text = text.replace('The Magistrate, Chapter 231:', 'The Magistrate, Chapter 234:')
    text = text.replace('light/231.html', 'light/234.html')
    test_path.write_text(text, encoding='utf-8')


migration.rewrite_text_files_once = rewrite_production_refs_only
migration.update_book_role_card_original = migration.update_book_role_card
migration.update_book_role_card = update_role_card_and_contract_test

if __name__ == '__main__':
    raise SystemExit(migration.main())
