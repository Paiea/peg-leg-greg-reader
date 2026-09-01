#!/usr/bin/env python3
from __future__ import annotations

import base64
from pathlib import Path


STAGING = Path("visual/book_plates/_staging")
DESTINATION = Path("visual/book_plates")
SUFFIX = ".b64part"


def main() -> None:
    if not STAGING.exists():
        return

    groups: dict[str, list[Path]] = {}
    for part in sorted(STAGING.glob(f"*{SUFFIX}*")):
        stem = part.name.split(SUFFIX, 1)[0]
        groups.setdefault(stem, []).append(part)

    for filename, parts in groups.items():
        encoded = "".join(part.read_text(encoding="ascii").strip() for part in parts)
        payload = base64.b64decode(encoded, validate=True)
        if len(payload) < 16 or payload[:4] != b"RIFF" or payload[8:12] != b"WEBP":
            raise ValueError(f"Decoded payload is not a WebP: {filename}")

        target = DESTINATION / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        print(f"materialized {target} ({len(payload)} bytes)")

        for part in parts:
            part.unlink()

    try:
        STAGING.rmdir()
    except OSError:
        pass


if __name__ == "__main__":
    main()
