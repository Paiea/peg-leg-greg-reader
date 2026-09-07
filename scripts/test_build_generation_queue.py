#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_generation_queue import build_generation_queue


HOLD = {
    "active": True,
    "mode": "structural_edit_hold",
    "generation_allowed": False,
}


def candidate(candidate_id: str, chapter: int) -> dict:
    return {
        "id": candidate_id,
        "chapter": chapter,
        "chapter_title": "TEST",
        "kind": "chapter_illustration",
        "priority": "high",
        "fit_target": "exact",
        "spoiler_level": "low",
        "status": "prompt_ready",
        "scene_summary": "A bounded test scene.",
        "visual_hook": "A physical test beat.",
        "characters": [],
        "location": "test room",
        "mood": "focused",
        "paragraph_anchor": "Unique test anchor.",
        "anchor_status": "valid",
    }


def main() -> int:
    global_candidate = candidate("global-candidate", 200)
    approved_candidate = candidate("bounded-approved", 5)

    held = build_generation_queue(
        [global_candidate],
        [],
        production_hold=HOLD,
        bounded_candidates=[approved_candidate],
        generation_batch_id="definitive-pilot-001",
    )
    assert [item["candidate_id"] for item in held] == ["bounded-approved"], held
    assert held[0]["generation_approval"] == "explicit_bounded", held[0]
    assert held[0]["generation_batch_id"] == "definitive-pilot-001", held[0]

    blocked = build_generation_queue(
        [global_candidate],
        [],
        production_hold=HOLD,
    )
    assert blocked == [], blocked

    open_queue = build_generation_queue(
        [global_candidate],
        [],
        production_hold={"active": False},
        bounded_candidates=[approved_candidate],
        generation_batch_id="definitive-pilot-001",
    )
    assert [item["candidate_id"] for item in open_queue] == ["global-candidate"], open_queue
    assert "generation_approval" not in open_queue[0], open_queue[0]
    assert "generation_batch_id" not in open_queue[0], open_queue[0]

    print("build generation queue regressions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
