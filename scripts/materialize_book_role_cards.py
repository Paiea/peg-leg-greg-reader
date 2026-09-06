#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
from pathlib import Path

ROOT = Path(__file__).parents[1]
SOURCE = ROOT / 'state' / 'visual' / 'book-role-card-source' / 'book-v-investor-446'
TARGET = ROOT / 'assets' / 'book-role-cards' / 'book-v-investor-446.webp'


def materialize(*, cleanup_source: bool = False) -> bool:
    parts = sorted(SOURCE.glob('part-*')) if SOURCE.exists() else []
    if not parts:
        if TARGET.is_file():
            return False
        raise FileNotFoundError(f'missing Book V role-card source parts: {SOURCE}')

    encoded = ''.join(path.read_text(encoding='ascii').strip() for path in parts)
    data = base64.b64decode(encoded, validate=True)
    if data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        raise ValueError('Book V role-card source did not decode to WebP')

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    changed = not TARGET.exists() or TARGET.read_bytes() != data
    if changed:
        TARGET.write_bytes(data)

    if cleanup_source:
        for path in parts:
            path.unlink()
        try:
            SOURCE.rmdir()
            SOURCE.parent.rmdir()
        except OSError:
            pass
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleanup-source', action='store_true')
    args = parser.parse_args()
    changed = materialize(cleanup_source=args.cleanup_source)
    print('materialized Book V role card' if changed else 'Book V role card already materialized')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
