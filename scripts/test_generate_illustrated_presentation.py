#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
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

    registry = [
        {
            "id": "feature-seven",
            "candidate_id": "feature-seven",
            "chapter": 7,
            "kind": "chapter_illustration",
            "status": "live",
            "live_asset": "visual/chapter_art/007/feature.webp",
            "paragraph_anchor": "",
            "alt_text": "Feature.",
            "caption": "",
            "presentation_role": "feature-illustration",
            "editorial_purpose": "Make this a visual scene anchor.",
        }
    ]
    with tempfile.TemporaryDirectory() as tmp:
        missing = Path(tmp) / "missing-presentation.json"
        derived = generate_illustrated.load_reader_presentation(missing, registry=registry)
    assert derived["visual/chapter_art/007/feature.webp"]["presentation_role"] == "feature-illustration", derived
    assert derived["visual/chapter_art/007/feature.webp"]["editorial_purpose"].startswith("Make this"), derived

    print("illustrated reader presentation regressions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
