#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

TEXT_ACTION = '<a class="secondary-action" href="light/index.html">Text Reader</a>'
ILLUSTRATED_ACTION = '<a class="secondary-action" href="#books">Illustrated Reader</a>'
ILLUSTRATIONS_ACTION = '<a class="tertiary-action" href="art.html">Illustrations</a>'
BEGIN_ACTION = '<a class="start primary-action" href="chapters/001.html">Begin Reading</a>'
TEXT_ACTION_RE = re.compile(r'<a class="secondary-action" href="light/index\.html">(?:Read Light|Text Reader)</a>')
LEGACY_CONTENTS_RE = re.compile(r'<a class="secondary-action" href="#(?:chapters|books)">(?:Chapters|Illustrated Reader)</a>')
ART_RE = re.compile(r'<a class="tertiary-action" href="art\.html">Illustrations</a>')


def patch_home(path: Path) -> bool:
    original = path.read_text(encoding='utf-8')
    if BEGIN_ACTION not in original:
        raise SystemExit(f'could not find homepage Begin Reading action in {path}')

    updated = TEXT_ACTION_RE.sub('', original)
    updated = LEGACY_CONTENTS_RE.sub('', updated)
    updated = ART_RE.sub('', updated)
    actions = BEGIN_ACTION + TEXT_ACTION + ILLUSTRATED_ACTION + ILLUSTRATIONS_ACTION
    updated = updated.replace(BEGIN_ACTION, actions, 1)

    if updated == original:
        return False
    path.write_text(updated, encoding='utf-8')
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description='Keep homepage reading-mode navigation current.')
    parser.add_argument('homepage', nargs='?', default='index.html')
    args = parser.parse_args()
    changed = patch_home(Path(args.homepage))
    print('updated homepage reading-mode navigation' if changed else 'homepage reading-mode navigation already current')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
