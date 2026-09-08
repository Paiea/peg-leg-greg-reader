#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import generate_illustrated


def markup(role: str | None) -> str:
    presentation = None if role is None else {"presentation_role": role}
    return generate_illustrated._art_figure(
        Path("visual/chapter_art/007/example.webp"),
        7,
        record={"alt_text": "Example.", "caption": ""},
        presentation=presentation,
    )


def main() -> int:
    assert '<figure class="chapter-art scene-illustration">' in markup(None)
    assert '<figure class="chapter-art sketch-beat">' in markup("sketch-beat")
    assert '<figure class="chapter-art scene-illustration">' in markup("scene-illustration")
    assert '<figure class="chapter-art feature-illustration">' in markup("feature-illustration")
    assert '<figure class="chapter-art feature-illustration feature-portrait">' in markup("feature-portrait")

    try:
        markup("gigantic-splash")
    except ValueError as exc:
        assert "presentation role" in str(exc).lower(), exc
    else:
        raise AssertionError("invalid presentation role must fail")

    print("illustrated reader presentation regressions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
