#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_reader_presentation import build_reader_presentation


def main() -> int:
    registry = [
        {
            "id": "legacy-seven",
            "candidate_id": "legacy-seven",
            "chapter": 7,
            "kind": "chapter_illustration",
            "status": "live",
            "live_asset": "visual/chapter_art/007/legacy.webp",
            "paragraph_anchor": "Seven anchor.",
            "alt_text": "Legacy seven.",
            "caption": "",
        },
        {
            "id": "thirteen-feature",
            "candidate_id": "thirteen-feature",
            "chapter": 13,
            "kind": "chapter_illustration",
            "status": "live",
            "live_asset": "visual/chapter_art/013/feature.webp",
            "paragraph_anchor": "Thirteen anchor.",
            "alt_text": "Feature thirteen.",
            "caption": "A controlled notebook share.",
            "presentation_role": "feature-portrait",
            "editorial_purpose": "Slow the reader down for a relationship boundary beat.",
        },
        {
            "id": "approved-not-live",
            "candidate_id": "approved-not-live",
            "chapter": 5,
            "kind": "chapter_illustration",
            "status": "approved",
            "live_asset": "visual/chapter_art/005/approved.webp",
            "paragraph_anchor": "Approved anchor.",
            "alt_text": "Approved only.",
            "caption": "",
        },
        {
            "id": "role-card-live",
            "candidate_id": "role-card-live",
            "chapter": 1,
            "kind": "role_card",
            "status": "live",
            "live_asset": "assets/role.webp",
            "paragraph_anchor": "",
            "alt_text": "Role card.",
            "caption": "",
        },
    ]

    presentation = build_reader_presentation(registry)
    assert [(record["chapter"], record["asset"]) for record in presentation] == [
        (7, "visual/chapter_art/007/legacy.webp"),
        (13, "visual/chapter_art/013/feature.webp"),
    ]
    assert presentation[0]["presentation_role"] == "scene-illustration"
    assert presentation[0]["editorial_purpose"] == ""
    assert presentation[1]["presentation_role"] == "feature-portrait"
    assert presentation[1]["editorial_purpose"].startswith("Slow the reader")

    print("reader presentation regressions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
