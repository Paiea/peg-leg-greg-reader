#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from generate_light import SHOWCASE_MANIFEST, load_all_sources
from showcase import build_showcase_map, load_showcase_manifest

LIGHT_ACTION = '<a class="secondary-action" href="light/index.html">Text Reader</a>'
BEGIN_ACTION_RE = re.compile(
    r'<a class="start primary-action" href="chapters/\d{3}\.html">Begin Reading</a>'
)
LIGHT_ACTION_RE = re.compile(
    r'<a class="secondary-action" href="light/index\.html">(?:Read Light|Text Reader)</a>'
)


def begin_action(canon: int) -> str:
    return f'<a class="start primary-action" href="chapters/{canon:03d}.html">Begin Reading</a>'


def patch_home(path: Path, *, begin_canon: int = 1) -> bool:
    original = path.read_text(encoding='utf-8')
    begin_match = BEGIN_ACTION_RE.search(original)
    if begin_match is None:
        raise SystemExit(f'could not find homepage Begin Reading action in {path}')

    updated = LIGHT_ACTION_RE.sub('', original)
    desired_begin = begin_action(begin_canon)
    updated = BEGIN_ACTION_RE.sub(desired_begin + LIGHT_ACTION, updated, count=1)

    if updated == original:
        return False
    path.write_text(updated, encoding='utf-8')
    return True


def first_showcase_canon() -> int:
    chapters = load_all_sources()
    if not chapters:
        raise SystemExit('could not resolve canonical chapters for Begin Reading')
    showcase = build_showcase_map(
        sorted(chapters),
        load_showcase_manifest(SHOWCASE_MANIFEST),
    )
    if not showcase.visible_canon:
        raise SystemExit('showcase contains no visible chapters')
    return showcase.visible_canon[0]


def main() -> int:
    parser = argparse.ArgumentParser(description='Keep homepage cross-mode reading navigation current.')
    parser.add_argument('homepage', nargs='?', default='index.html')
    args = parser.parse_args()
    changed = patch_home(Path(args.homepage), begin_canon=first_showcase_canon())
    print('updated homepage reading-mode navigation' if changed else 'homepage reading-mode navigation already current')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
