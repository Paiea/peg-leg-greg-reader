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
    text = render_prompt_pack(candidate)
    assert "Pre-amputation Greg" in text, text
    assert "permanent LEFT BKA" not in text, text
    assert "two crutches" not in text, text

    legacy = dict(candidate)
    legacy.pop("continuity_notes")
    legacy_text = render_prompt_pack(legacy)
    assert "permanent LEFT BKA" in legacy_text, legacy_text

    print("build prompt packs regressions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
