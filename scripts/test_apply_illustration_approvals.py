#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.apply_illustration_approvals import apply_approvals


def generated_record(candidate_id: str = "candidate-one") -> dict:
    return {
        "id": f"{candidate_id}-v1",
        "candidate_id": candidate_id,
        "chapter": 7,
        "kind": "chapter_illustration",
        "status": "generated",
        "style_family": "sketch-ink-paint",
        "source_asset": f"visual/chapter_art/007/{candidate_id}-v1.webp",
        "live_asset": "",
        "caption": "",
        "alt_text": "",
        "approved_fit": "exact",
        "prompt_pack": f"state/visual/prompt-packs/{candidate_id}.md",
        "paragraph_anchor": "Exact anchor.",
    }


def main() -> int:
    registry = [generated_record()]
    approval = {
        "candidate_id": "candidate-one",
        "asset": "visual/chapter_art/007/candidate-one-v1.webp",
        "decision": "approve",
        "approved_fit": "exact",
        "alt_text": "Antonius turns back to lift the gray frame.",
        "caption": "",
        "presentation_role": "feature-portrait",
        "editorial_purpose": "Make the negotiation reversal a visual scene anchor.",
        "editorial_note": "The action reads immediately and Antonius owns the beat.",
    }
    updated, changed = apply_approvals(registry, [approval])
    assert changed == 1
    record = updated[0]
    assert record["status"] == "approved"
    assert record["presentation_role"] == "feature-portrait"
    assert record["editorial_purpose"] == "Make the negotiation reversal a visual scene anchor."
    assert record["editorial_note"] == "The action reads immediately and Antonius owns the beat."

    legacy, changed = apply_approvals(
        [generated_record("legacy")],
        [
            {
                "candidate_id": "legacy",
                "asset": "visual/chapter_art/007/legacy-v1.webp",
                "decision": "approve",
                "approved_fit": "exact",
                "alt_text": "Legacy approved image.",
                "caption": "",
            }
        ],
    )
    assert changed == 1
    assert legacy[0]["status"] == "approved"
    assert "presentation_role" not in legacy[0]

    try:
        apply_approvals(
            [generated_record("bad-role")],
            [
                {
                    "candidate_id": "bad-role",
                    "asset": "visual/chapter_art/007/bad-role-v1.webp",
                    "decision": "approve",
                    "approved_fit": "exact",
                    "alt_text": "Bad role.",
                    "presentation_role": "gigantic-splash",
                    "editorial_purpose": "Bad test.",
                }
            ],
        )
    except ValueError as exc:
        assert "presentation_role" in str(exc), exc
    else:
        raise AssertionError("invalid presentation role must fail")

    print("illustration approval taste regressions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
