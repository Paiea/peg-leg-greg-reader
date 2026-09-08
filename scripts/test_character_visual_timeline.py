#!/usr/bin/env python3
from __future__ import annotations

from scripts.character_visual_timeline import resolve_character_visual_state, validate_visual_timeline


def main() -> int:
    records = [
        {
            "character": "Greg",
            "state_id": "greg-early-pre-amputation",
            "chapter_start": 1,
            "chapter_end": 18,
            "authority": "derived_editorial_reference",
            "canon_authority": False,
            "evidence": ["early-story pilot continuity"],
            "appearance": {"facial_hair": "light beard/stubble/fuzz"},
            "body_state": {"left_leg": "intact", "right_leg": "intact"},
            "mobility_state": {"default": "unassisted"},
            "must_not_show": ["crutches", "prosthesis"],
        },
        {
            "character": "Greg",
            "state_id": "greg-prosthetic-trial",
            "chapter_start": 496,
            "chapter_end": 499,
            "authority": "derived_editorial_reference",
            "canon_authority": False,
            "evidence": ["ch496/ch499 PERFORMANCE evidence"],
            "appearance": {},
            "body_state": {"left_leg": "below-knee amputation"},
            "mobility_state": {
                "default": "two crutches",
                "prosthesis": "supervised fitting/trial only",
            },
        },
    ]
    validate_visual_timeline(records)

    early = resolve_character_visual_state(records, "Greg", 5)
    assert early is not None
    assert early["state_id"] == "greg-early-pre-amputation"
    assert early["appearance"]["facial_hair"] == "light beard/stubble/fuzz"
    assert early["body_state"]["left_leg"] == "intact"
    assert "crutches" in early["must_not_show"]

    late = resolve_character_visual_state(records, "Greg", 497)
    assert late is not None
    assert late["state_id"] == "greg-prosthetic-trial"
    assert late["mobility_state"]["default"] == "two crutches"
    assert "supervised" in late["mobility_state"]["prosthesis"]

    assert resolve_character_visual_state(records, "Greg", 100) is None
    assert resolve_character_visual_state(records, "Arlo", 5) is None

    overlapping = records + [
        {
            "character": "Greg",
            "state_id": "bad-overlap",
            "chapter_start": 10,
            "chapter_end": 20,
            "authority": "derived_editorial_reference",
            "canon_authority": False,
            "evidence": ["bad test"],
            "appearance": {},
            "body_state": {},
            "mobility_state": {},
        }
    ]
    try:
        validate_visual_timeline(overlapping)
    except ValueError as exc:
        assert "overlap" in str(exc).lower(), exc
    else:
        raise AssertionError("overlapping character visual states must fail validation")

    print("character visual timeline regressions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
