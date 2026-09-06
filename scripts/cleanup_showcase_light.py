#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from generate_light import LIGHT_DIR, SHOWCASE_MANIFEST, load_all_sources
from showcase import ShowcaseMap, build_showcase_map, load_showcase_manifest


def clean_numeric_pages(directory: Path, canonical_numbers: set[int], showcase: ShowcaseMap) -> list[int]:
    removed: list[int] = []
    for path in sorted(directory.glob('[0-9][0-9][0-9].html')):
        if not path.stem.isdigit():
            continue
        number = int(path.stem)
        if number not in canonical_numbers or showcase.showcase_number(number) is None:
            path.unlink()
            removed.append(number)
    return removed


def main() -> int:
    all_chapters = load_all_sources()
    showcase = build_showcase_map(
        sorted(all_chapters),
        load_showcase_manifest(SHOWCASE_MANIFEST),
    )
    removed = clean_numeric_pages(LIGHT_DIR, set(all_chapters), showcase)
    print(f'removed {len(removed)} hidden or orphan Text Reader pages')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
