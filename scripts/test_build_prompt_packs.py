#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_prompt_packs import render_prompt_pack


def main() -> int:
    candidate = {
        "id": "early-greg",
        "chapter": 5,
        "chapter_title": "THE WARRIOR",
        "kind": "chapter_illustration",
        "fit_target": "exact",
        "spoiler_level": "low",
        "status": "prompt_ready",
        "scene_summary": "Greg trains in the yard.",
        "visual_hook": "Greg is down in the sand after his body lags behind his knowledge.",
        "characters": ["Greg", "Jorren"],
        "continuity_notes": "Pre-amputation Greg: both legs intact; no crutches or prosthesis.",
    }
    evidence = {
        "candidate_id": "early-greg",
        "evidence_condition": "prose_temporal",
        "character_states": {
            "Greg": {
                "state_id": "greg-early-pre-amputation",
                "appearance": {
                    "age": "nineteen",
                    "facial_hair": "light beard/stubble/fuzz; visibly not clean-shaven",
                },
                "body_state": {"left_leg": "intact", "right_leg": "intact"},
                "mobility_state": {"default": "unassisted"},
                "must_not_show": ["crutches", "prosthesis"],
            }
        },
    }
    text = render_prompt_pack(candidate, visual_scene_evidence=evidence)
    assert "Pre-amputation Greg" in text, text
    assert "TEMPORAL CHARACTER STATE" in text, text
    assert "light beard/stubble/fuzz" in text, text
    assert "Scene-local continuity overrides temporal body/mobility fields" in text, text
    assert "permanent LEFT BKA" not in text, text
    assert "two crutches" not in text, text

    temporal_only = dict(candidate)
    temporal_only.pop("continuity_notes")
    temporal_text = render_prompt_pack(temporal_only, visual_scene_evidence=evidence)
    assert "left_leg: intact" in temporal_text, temporal_text
    assert "default: unassisted" in temporal_text, temporal_text
    assert "must not show: crutches, prosthesis" in temporal_text, temporal_text
    assert "permanent LEFT BKA" not in temporal_text, temporal_text

    legacy_text = render_prompt_pack(temporal_only)
    assert "permanent LEFT BKA" in legacy_text, legacy_text

    print("build prompt packs regressions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
