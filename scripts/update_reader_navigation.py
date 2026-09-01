#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

LIGHT_ACTION = '<a class="secondary-action" href="light/index.html">Read Light</a>'
BEGIN_ACTION = '<a class="start primary-action" href="chapters/001.html">Begin Reading</a>'


def patch_home(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if LIGHT_ACTION in text:
        return False
    if BEGIN_ACTION not in text:
        raise SystemExit(f'could not find homepage Begin Reading action in {path}')
    updated = text.replace(BEGIN_ACTION, BEGIN_ACTION + LIGHT_ACTION, 1)
    path.write_text(updated, encoding='utf-8')
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description='Add stable cross-mode navigation to reader publishing surfaces.')
    parser.add_argument('homepage', nargs='?', default='index.html')
    args = parser.parse_args()
    changed = patch_home(Path(args.homepage))
    print('updated homepage reader actions' if changed else 'homepage reader actions already current')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
