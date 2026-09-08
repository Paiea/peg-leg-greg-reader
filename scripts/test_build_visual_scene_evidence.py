#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_visual_scene_evidence import build_visual_scene_evidence


def candidate(candidate_id: str, chapter: int, anchor: str, characters: list[str]) -> dict:
    return {
        "id": candidate_id,
        "chapter": chapter,
        "chapter_title": "TEST",
        "scene_summary": "A test scene.",
        "visual_hook": "A visible action.",
        "characters": characters,
        "location": "test location",
        "mood": "focused",
        "scene_tags": ["test"],
        "paragraph_anchor": anchor,
    }


def main() -> int:
    candidates = [
        candidate("early-control", 5, "Early anchor.", ["Greg"]),
        candidate("performance-backed", 7, "Exact performance anchor.", ["Greg", "Antonius"]),
        candidate("unknown-era", 100, "Unknown anchor.", ["Greg"]),
    ]
    registry = [
        {
            "id": "legacy-seven",
            "candidate_id": "legacy-seven",
            "chapter": 7,
            "kind": "chapter_illustration",
            "status": "live",
            "live_asset": "visual/chapter_art/007/existing.webp",
            "alt_text": "Existing scene.",
            "caption": "",
            "paragraph_anchor": "Old anchor.",
        }
    ]
    temporal_states = [
        {
            "character": "Greg",
            "state_id": "greg-early-pre-amputation",
            "chapter_start": 1,
            "chapter_end": 18,
            "authority": "derived_editorial_reference",
            "canon_authority": False,
            "evidence": ["early evidence"],
            "appearance": {"facial_hair": "light beard/stubble/fuzz"},
            "body_state": {"left_leg": "intact", "right_leg": "intact"},
            "mobility_state": {"default": "unassisted"},
        }
    ]
    performance_references = {
        5: {
            "archive_path": "state/editorial/performance-roundtrip/005",
            "chapter": 5,
            "scene_anchors": ["Different anchor."],
            "visual_reference": {"active_task": "wrong scene", "props": [], "physical_beats": []},
        },
        7: {
            "archive_path": "state/editorial/performance-roundtrip/007",
            "chapter": 7,
            "scene_anchors": ["Exact performance anchor."],
            "visual_reference": {
                "active_task": "Antonius reverses the object's category through action.",
                "props": ["gray frame", "broom"],
                "physical_beats": ["Antonius stops and returns."],
            },
        },
    }

    evidence = build_visual_scene_evidence(candidates, registry, temporal_states, performance_references)
    by_id = {record["candidate_id"]: record for record in evidence}

    early = by_id["early-control"]
    assert early["evidence_condition"] == "prose_temporal"
    assert early["character_states"]["Greg"]["state_id"] == "greg-early-pre-amputation"
    assert "performance_reference" not in early

    backed = by_id["performance-backed"]
    assert backed["evidence_condition"] == "prose_temporal_performance"
    assert backed["performance_reference"]["archive_path"].endswith("/007")
    assert backed["existing_art"][0]["asset"] == "visual/chapter_art/007/existing.webp"

    unknown = by_id["unknown-era"]
    assert unknown["evidence_condition"] == "prose_only"
    assert unknown["character_states"] == {}

    assert [record["candidate_id"] for record in evidence] == ["early-control", "performance-backed", "unknown-era"]

    print("visual scene evidence regressions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
