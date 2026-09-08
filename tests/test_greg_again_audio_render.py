import json
import tempfile
import unittest
from pathlib import Path

from scripts.greg_again_audio_render import (
    build_renderer_request,
    export_bootstrap_bundle,
    register_take,
)


class GregAgainAudioRenderTests(unittest.TestCase):
    def test_bootstrap_bundle_separates_hidden_direction_from_spoken_text(self):
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
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = export_bootstrap_bundle(score, "ONE PRIMARY NARRATOR", root)
            payload = json.loads(paths[0].read_text(encoding="utf-8"))
            self.assertEqual("I woke because my back didn't hurt.", payload["spoken_text"])
            self.assertEqual("quiet confusion", payload["performance_context"]["intention"])
            self.assertNotIn("quiet confusion", payload["spoken_text"])
            self.assertTrue((root / "index.json").exists())

    def test_renderer_request_carries_prior_continuity_and_pronunciation_notes(self):
        block = {
            "id": "ga-001-b002",
            "spoken_text": "Carrow was outside.",
            "direction": {"continuity": "body evidence established"},
            "pronunciation_notes": ["Carrow: confirm before render"],
        }
        req = build_renderer_request(block, "narrator brief", prior_block_text="previous spoken line")
        self.assertEqual("ga-001-b002", req.block_id)
        self.assertEqual("previous spoken line", req.prior_block_text)
        self.assertEqual(("Carrow: confirm before render",), req.pronunciation_notes)

    def test_take_registration_rejects_generic_tts_state(self):
        with self.assertRaisesRegex(ValueError, "renderer_status"):
            register_take({}, block_id="ga-001-b001", take_id="t1", relative_path="takes/t1.wav", adapter="tts", model=None, voice=None, renderer_status="good_enough_tts")

    def test_take_registration_does_not_auto_select(self):
        manifest = {"takes": {}, "selected_takes": {}}
        updated = register_take(manifest, block_id="ga-001-b001", take_id="take-a", relative_path="takes/a.wav", adapter="bootstrap_chatgpt", model=None, voice="reference", renderer_status="qualified")
        self.assertEqual("bootstrap_chatgpt", updated["takes"]["ga-001-b001"]["take-a"]["adapter"])
        self.assertEqual({}, updated["selected_takes"])
        self.assertEqual({"takes": {}, "selected_takes": {}}, manifest)


if __name__ == "__main__":
    unittest.main()
