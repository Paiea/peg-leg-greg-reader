#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_generation_packet import render_generation_packet


def main() -> int:
    record = {
        "candidate_id": "performance-backed",
        "chapter": 7,
        "chapter_title": "THE BUYER",
        "coverage_before": 1,
        "priority": "high",
        "style_family": "sketch-ink-paint",
        "framing_preference": "above_waist",
        "visual_hook": "Antonius turns back for the gray frame.",
        "scene_summary": "The object changes category through Antonius's physical response.",
        "characters": ["Greg", "Antonius"],
        "location": "Antonius storeroom",
        "mood": "working negotiation",
        "character_reference_assets": [],
        "selected_character_references": [],
        "character_appearance_notes": {},
        "reference_selection_notes": "",
        "continuity_notes": "Pre-amputation Greg.",
        "prompt_pack": "state/visual/prompt-packs/performance-backed.md",
        "target_asset": "visual/chapter_art/007/performance-backed-v1.webp",
        "visual_scene_evidence": {
            "candidate_id": "performance-backed",
            "chapter": 7,
            "evidence_condition": "prose_temporal_performance",
            "character_states": {
                "Greg": {
                    "state_id": "greg-early-pre-amputation",
                    "appearance": {"facial_hair": "light beard/stubble/fuzz"},
                    "body_state": {"left_leg": "intact", "right_leg": "intact"},
                    "mobility_state": {"default": "unassisted"},
                    "must_not_show": ["crutches", "prosthesis"],
                }
            },
        },
        "performance_reference": {
            "archive_path": "state/editorial/performance-roundtrip/007",
            "visual_reference": {
                "active_task": "Antonius is cleaning while Greg evaluates the gray Tere reference set.",
                "props": ["gray Tere reference set", "broom"],
                "physical_beats": [
                    "Greg's value claim makes Antonius stop, return, and pick up the frame himself."
                ],
            },
        },
    }
    text = render_generation_packet([record])
    assert "Evidence condition: prose_temporal_performance" in text, text
    assert "TEMPORAL Greg" in text, text
    assert "light beard/stubble/fuzz" in text, text
    assert "must not show: crutches, prosthesis" in text, text
    assert "PERFORMANCE visual reference" in text, text
    assert "Antonius is cleaning while Greg evaluates" in text, text
    assert "stop, return, and pick up the frame himself" in text, text

    print("build generation packet regressions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
