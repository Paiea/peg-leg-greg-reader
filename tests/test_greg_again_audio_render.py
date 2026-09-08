from pathlib import Path
import json
import pytest

from scripts.greg_again_audio_render import (
    build_renderer_request,
    export_bootstrap_bundle,
    register_take,
)


def test_bootstrap_bundle_separates_hidden_direction_from_spoken_text(tmp_path: Path):
    score = {
        "chapter_id": "ga-001",
        "score_revision": 1,
        "blocks": [{
            "id": "ga-001-b001",
            "scene_id": "opening",
            "spoken_text": "I woke because my back didn't hurt.",
            "direction": {"intention": "quiet confusion", "pace": "slow"},
        }],
    }
    paths = export_bootstrap_bundle(score, "ONE PRIMARY NARRATOR", tmp_path)
    payload = json.loads(paths[0].read_text(encoding="utf-8"))
    assert payload["spoken_text"] == "I woke because my back didn't hurt."
    assert payload["performance_context"]["intention"] == "quiet confusion"
    assert "quiet confusion" not in payload["spoken_text"]
    assert (tmp_path / "index.json").exists()


def test_renderer_request_carries_prior_continuity_and_pronunciation_notes():
    block = {
        "id": "ga-001-b002",
        "spoken_text": "Carrow was outside.",
        "direction": {"continuity": "body evidence established"},
        "pronunciation_notes": ["Carrow: confirm before render"],
    }
    req = build_renderer_request(block, "narrator brief", prior_block_text="previous spoken line")
    assert req.block_id == "ga-001-b002"
    assert req.prior_block_text == "previous spoken line"
    assert req.pronunciation_notes == ("Carrow: confirm before render",)


def test_take_registration_rejects_generic_tts_state():
    with pytest.raises(ValueError, match="renderer_status"):
        register_take({}, block_id="ga-001-b001", take_id="t1", relative_path="takes/t1.wav", adapter="tts", model=None, voice=None, renderer_status="good_enough_tts")


def test_take_registration_does_not_auto_select():
    manifest = {"takes": {}, "selected_takes": {}}
    updated = register_take(manifest, block_id="ga-001-b001", take_id="take-a", relative_path="takes/a.wav", adapter="bootstrap_chatgpt", model=None, voice="reference", renderer_status="qualified")
    assert updated["takes"]["ga-001-b001"]["take-a"]["adapter"] == "bootstrap_chatgpt"
    assert updated["selected_takes"] == {}
    assert manifest == {"takes": {}, "selected_takes": {}}
