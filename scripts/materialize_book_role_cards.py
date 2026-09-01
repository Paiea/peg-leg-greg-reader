from __future__ import annotations

import base64
import hashlib
from pathlib import Path


ROOT = Path(__file__).parents[1]
SOURCE_DIR = ROOT / 'assets' / 'book-role-cards-source'
OUTPUT_DIR = ROOT / 'assets' / 'book-role-cards'

CARDS = {
    'book-i-warrior-005': '08601853cccac4eeabe843436c66aaf2447349d5ccf76f87b6c7399e82ad52cb',
    'book-ii-stagehand-177': '9cc5c54d69a9bc3cf79268af7ea3453a1f4ca6284e56af117940769c40907112',
    'book-iii-magistrate-231': '6ea5c9c2951f7364a11eddad1e081a3caca0c930fcb8ac6d9413c62de94a72d9',
}


def materialize_card(stem: str, expected_sha256: str) -> Path:
    parts = sorted(SOURCE_DIR.glob(f'{stem}.part*.b64part'))
    if not parts:
        raise FileNotFoundError(f'No source parts found for {stem}')

    encoded = ''.join(part.read_text(encoding='ascii').strip() for part in parts)
    data = base64.b64decode(encoded, validate=True)
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected_sha256:
        raise ValueError(f'{stem}: sha256 mismatch: {digest} != {expected_sha256}')
    if len(data) < 12 or data[4:8] != b'ftyp' or b'avif' not in data[8:16]:
        raise ValueError(f'{stem}: decoded source is not an AVIF file')

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / f'{stem}.avif'
    output.write_bytes(data)
    return output


def main() -> None:
    for stem, digest in CARDS.items():
        output = materialize_card(stem, digest)
        print(f'{output.relative_to(ROOT)} {output.stat().st_size} bytes')


if __name__ == '__main__':
    main()
