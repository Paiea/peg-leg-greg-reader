from pathlib import Path
import pytest

from scripts.greg_again_audio import (
    build_public_metadata,
    selected_take_paths,
    validate_manifest,
    validate_score,
)


def minimal_score():
    return {
        "schema": "greg_again_audio_score/v1",
        "run_id": "greg-again",
        "chapter_id": "ga-001",
        "title": "The Boy",
        "score_revision": 1,
        "blocks": [{
            "id": "ga-001-b001",
            "scene_id": "wake-young-body",
            "spoken_text": "I woke because my back didn't hurt.",
            "direction": {
                "narrator_mode": "narration",
                "entering_state": "confused, physically alert",
                "intention": "notice bodily wrongness before explaining it",
                "physical_context": "Greg is still in bed",
                "pace": "unhurried opening, curiosity building",
                "continuity": "chapter opening",
                "listener_risks": [],
            },
        }],
    }


def minimal_manifest():
    return {
        "schema": "greg_again_audio_manifest/v1",
        "run_id": "greg-again",
        "chapter_id": "ga-001",
        "title": "The Boy",
        "score_revision": 1,
        "block_order": ["ga-001-b001"],
        "renderer_status": "unrendered",
        "approval_state": "experimental",
        "takes": {},
        "selected_takes": {},
        "assembled_asset": None,
        "duration_seconds": None,
    }


def test_score_rejects_duplicate_or_unstable_block_ids():
    score = minimal_score()
    score["blocks"].append(dict(score["blocks"][0]))
    with pytest.raises(ValueError, match="duplicate block id"):
        validate_score(score)


def test_manifest_rejects_unknown_quality_state():
    score = minimal_score()
    manifest = minimal_manifest()
    manifest["renderer_status"] = "good_enough_tts"
    with pytest.raises(ValueError, match="renderer_status"):
        validate_manifest(manifest, score)


def test_assembly_inputs_require_one_selected_take_per_block(tmp_path: Path):
    score = minimal_score()
    manifest = minimal_manifest()
    validate_manifest(manifest, score)
    with pytest.raises(ValueError, match="missing selected take"):
        selected_take_paths(manifest, tmp_path)


def test_selected_take_must_be_qualified(tmp_path: Path):
    score = minimal_score()
    manifest = minimal_manifest()
    manifest["takes"] = {"ga-001-b001": {"t1": {"relative_path": "takes/t1.wav", "renderer_status": "experimental"}}}
    manifest["selected_takes"] = {"ga-001-b001": "t1"}
    validate_manifest(manifest, score)
    with pytest.raises(ValueError, match="qualified"):
        selected_take_paths(manifest, tmp_path)


def test_public_metadata_hides_production_notes_and_maps_audio_src():
    score = minimal_score()
    manifest = minimal_manifest()
    manifest["production_notes"] = "private renderer diagnosis"
    manifest["assembled_asset"] = "assets/chapter-001.wav"
    public = build_public_metadata(validate_manifest(manifest, score))
    assert "production_notes" not in public
    assert public["status"] == "experimental"
    assert public["audio_src"] == "assets/chapter-001.wav"
