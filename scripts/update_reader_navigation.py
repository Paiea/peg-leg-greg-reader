#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

LIGHT_ACTION = '<a class="secondary-action" href="light/index.html">Read Light</a>'
BEGIN_ACTION = '<a class="start primary-action" href="chapters/001.html">Begin Reading</a>'


def patch_home(path: Path) -> bool:
    original = path.read_text(encoding='utf-8')
    updated = original
    if LIGHT_ACTION not in updated:
        if BEGIN_ACTION not in updated:
            raise SystemExit(f'could not find homepage Begin Reading action in {path}')
        updated = updated.replace(BEGIN_ACTION, BEGIN_ACTION + LIGHT_ACTION, 1)
    if updated == original:
        return False
    path.write_text(updated, encoding='utf-8')
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description='Keep homepage cross-mode reading navigation current.')
    parser.add_argument('homepage', nargs='?', default='index.html')
    args = parser.parse_args()
    changed = patch_home(Path(args.homepage))
    print('updated homepage reading-mode navigation' if changed else 'homepage reading-mode navigation already current')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
