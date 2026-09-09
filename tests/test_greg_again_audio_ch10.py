import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO_ROOT = ROOT / "greg-again" / "audio"
R2_ROOT = ROOT / "r2"


class GregAgainChapter10AudioTest(unittest.TestCase):
    def test_chapter_ten_is_published_and_durable(self):
        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        by_id = {chapter["chapter_id"]: chapter for chapter in manifest["chapters"]}
        chapter = by_id["ga-010"]

        self.assertEqual(10, chapter["number"])
        self.assertEqual("The Returner", chapter["title"])
        self.assertEqual("shared-greg-surface", chapter["lens"])
        self.assertEqual("processing-space", chapter["audio_finish"])
        self.assertEqual("assets/chapter-010.mp3", chapter["audio_src"])
        self.assertGreater(chapter["duration_seconds"], 60)

        audio = AUDIO_ROOT / chapter["audio_src"]
        self.assertTrue(audio.exists())
        self.assertGreater(audio.stat().st_size, 1_000_000)

    def test_chapter_ten_preserves_return_residue_contract(self):
        script = (AUDIO_ROOT / "scripts" / "010-the-returner.md").read_text(encoding="utf-8")
        self.assertIn("DO NOT OPTIMIZE AWAY PROCESSING TIME", script)
        self.assertIn("SMOOTHNESS IS NOT AUTOMATICALLY CLARITY", script)
        self.assertIn("TIME MUST LEAVE RESIDUE", script)
        self.assertIn("The road took him.", script)
        self.assertIn("My heel blister became skin.", script)
        self.assertIn("The work had continued anyway.", script)
        self.assertIn("Time had happened.", script)
        self.assertIn("That was different from time passing.", script)

    def test_r2_chapter_ten_routes_published_audio(self):
        chapter = json.loads((R2_ROOT / "data/chapters/ch010.json").read_text(encoding="utf-8"))
        self.assertEqual("The Returner", chapter["title"])
        self.assertEqual("published", chapter["audio"]["status"])
        self.assertEqual(
            "../greg-again/audio/assets/chapter-010.mp3",
            chapter["audio"]["path"],
        )


if __name__ == "__main__":
    unittest.main()
