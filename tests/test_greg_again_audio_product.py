import json
import unittest
from pathlib import Path

from scripts.greg_again_audio import validate_manifest, validate_score

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "state/experiments/greg-again/audio"


class GregAgainAudioProductTests(unittest.TestCase):
    def test_chapter_1_audio_state_is_complete_and_unrendered(self):
        score = json.loads((AUDIO / "chapters/001/score.json").read_text(encoding="utf-8"))
        manifest = json.loads((AUDIO / "chapters/001/manifest.json").read_text(encoding="utf-8"))
        validate_score(score)
        validate_manifest(manifest, score)
        self.assertEqual("The Boy", score["title"])
        self.assertGreaterEqual(len(score["blocks"]), 8)
        self.assertEqual("unrendered", manifest["renderer_status"])
        self.assertEqual("experimental", manifest["approval_state"])
        self.assertEqual({}, manifest["selected_takes"])

    def test_narrator_brief_has_audio_first_rules(self):
        narrator = (AUDIO / "narrator.md").read_text(encoding="utf-8").lower()
        for phrase in ("one primary narrator", "dry humor", "speaker clarity", "do not overperform", "male/masculine", "thought-thread"):
            self.assertIn(phrase, narrator)

    def test_pronunciations_are_not_silently_guessed(self):
        pronunciation = json.loads((AUDIO / "pronunciation.json").read_text(encoding="utf-8"))
        self.assertEqual("greg_again_pronunciation/v1", pronunciation["schema"])
        self.assertEqual({"confirm_before_render"}, {entry["status"] for entry in pronunciation["entries"]})

    def test_public_audio_page_is_small_and_audio_first(self):
        html = (ROOT / "greg-again/audio/index.html").read_text(encoding="utf-8")
        self.assertIn("GREG, AGAIN", html)
        self.assertIn("Audio-Native Proving Run", html)
        self.assertIn("The Boy", html)
        self.assertIn("<audio", html)
        self.assertNotIn("waveform", html.lower())
        self.assertNotIn("dashboard", html.lower())

    def test_public_manifest_can_expose_unqualified_narrator_audition(self):
        public = json.loads((ROOT / "greg-again/audio/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("experimental", public["status"])
        self.assertEqual("narrator_audition", public["sample_status"])
        self.assertTrue(public["audio_src"].startswith("https://"))
        self.assertEqual("deep", public["voice_style"])

    def test_player_labels_audition_without_promoting_it_to_qualified(self):
        js = (ROOT / "greg-again/audio/player.js").read_text(encoding="utf-8")
        self.assertIn("Experimental narrator audition.", js)
        self.assertIn("sample_status", js)
        self.assertIn("Audio render not yet qualified.", js)


if __name__ == "__main__":
    unittest.main()
