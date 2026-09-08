import tempfile
import unittest
from pathlib import Path

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


class GregAgainAudioContractTests(unittest.TestCase):
    def test_score_rejects_duplicate_or_unstable_block_ids(self):
        score = minimal_score()
        score["blocks"].append(dict(score["blocks"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate block id"):
            validate_score(score)

    def test_manifest_rejects_unknown_quality_state(self):
        score = minimal_score()
        manifest = minimal_manifest()
        manifest["renderer_status"] = "good_enough_tts"
        with self.assertRaisesRegex(ValueError, "renderer_status"):
            validate_manifest(manifest, score)

    def test_assembly_inputs_require_one_selected_take_per_block(self):
        score = minimal_score()
        manifest = minimal_manifest()
        validate_manifest(manifest, score)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "missing selected take"):
                selected_take_paths(manifest, Path(tmp))

    def test_selected_take_must_be_qualified(self):
        score = minimal_score()
        manifest = minimal_manifest()
        manifest["takes"] = {"ga-001-b001": {"t1": {"relative_path": "takes/t1.wav", "renderer_status": "experimental"}}}
        manifest["selected_takes"] = {"ga-001-b001": "t1"}
        validate_manifest(manifest, score)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "qualified"):
                selected_take_paths(manifest, Path(tmp))

    def test_public_metadata_hides_production_notes_and_maps_audio_src(self):
        score = minimal_score()
        manifest = minimal_manifest()
        manifest["production_notes"] = "private renderer diagnosis"
        manifest["assembled_asset"] = "assets/chapter-001.wav"
        public = build_public_metadata(validate_manifest(manifest, score))
        self.assertNotIn("production_notes", public)
        self.assertEqual("experimental", public["status"])
        self.assertEqual("assets/chapter-001.wav", public["audio_src"])


if __name__ == "__main__":
    unittest.main()
