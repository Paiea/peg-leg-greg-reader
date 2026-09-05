#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

LIGHT_ACTION = '<a class="secondary-action" href="light/index.html">Text Reader</a>'
BEGIN_ACTION = '<a class="start primary-action" href="chapters/001.html">Begin Reading</a>'
LIGHT_ACTION_RE = re.compile(
    r'<a class="secondary-action" href="light/index\.html">(?:Read Light|Text Reader)</a>'
)


def patch_home(path: Path) -> bool:
    original = path.read_text(encoding='utf-8')
    if BEGIN_ACTION not in original:
        raise SystemExit(f'could not find homepage Begin Reading action in {path}')

    # The public-label normalization pass renames the historical "Read Light"
    # label to "Text Reader". Remove either spelling first so repeated builds are
    # idempotent instead of appending another link on every run.
    updated = LIGHT_ACTION_RE.sub('', original)
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
