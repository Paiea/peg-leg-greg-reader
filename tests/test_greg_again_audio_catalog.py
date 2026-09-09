import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO_ROOT = ROOT / "greg-again" / "audio"


class GregAgainAudioCatalogTest(unittest.TestCase):
    def test_catalog_publishes_chapters_one_through_four(self):
        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        chapters = manifest["chapters"]
        by_id = {chapter["chapter_id"]: chapter for chapter in chapters}

        self.assertIn("ga-001", by_id)
        self.assertIn("ga-002", by_id)
        self.assertIn("ga-003", by_id)
        self.assertIn("ga-004", by_id)
        self.assertEqual("The Boy", by_id["ga-001"]["title"])
        self.assertEqual("Two Things", by_id["ga-002"]["title"])
        self.assertEqual("The Borrower", by_id["ga-003"]["title"])
        self.assertEqual("Thirty Days", by_id["ga-004"]["title"])
        self.assertEqual("assets/chapter-001.mp3", by_id["ga-001"]["audio_src"])
        self.assertEqual("assets/chapter-002.mp3", by_id["ga-002"]["audio_src"])
        self.assertEqual("assets/chapter-003.mp3", by_id["ga-003"]["audio_src"])
        self.assertEqual("assets/chapter-004.mp3", by_id["ga-004"]["audio_src"])
        self.assertEqual("greg-dominant", by_id["ga-002"]["lens"])
        self.assertEqual("greg-dominant", by_id["ga-003"]["lens"])
        self.assertEqual("shared-greg-surface", by_id["ga-004"]["lens"])

    def test_chapters_two_through_four_audio_are_durable_and_nontrivial(self):
        for number in (2, 3, 4):
            chapter = AUDIO_ROOT / "assets" / f"chapter-{number:03d}.mp3"
            self.assertTrue(chapter.exists())
            self.assertGreater(chapter.stat().st_size, 1_000_000)

    def test_chapter_three_preserves_performance_script_and_audio_rules(self):
        script = (AUDIO_ROOT / "scripts" / "003-the-borrower.md").read_text(encoding="utf-8")
        self.assertIn("ATTENTION GRAVITY", script)
        self.assertIn("VOICE BREACH", script)
        self.assertIn("LANGUAGE AS ACTION", script)
        self.assertIn("You're nineteen.", script)
        self.assertIn("That's predatory.", script)
        self.assertIn("Yes.", script)

    def test_chapter_four_uses_shared_surface_repair_first_posture(self):
        script = (AUDIO_ROOT / "scripts" / "004-thirty-days.md").read_text(encoding="utf-8")
        self.assertIn("SHARED GREG SURFACE", script)
        self.assertIn("REPAIR-FIRST", script)
        self.assertIn("PAUSES COME FROM CONTRAST, NOT FRAGMENTATION", script)
        self.assertIn("DO NOT WRITE TICS FOR PERFORMANCE", script)
        self.assertIn("HEAR → MOVE → UNDERSTAND", script)
        self.assertIn("STOP BUYING SHALE. COME SEE THIS.", script)

    def test_public_page_renders_catalog_instead_of_one_hardcoded_chapter(self):
        html = (AUDIO_ROOT / "index.html").read_text(encoding="utf-8")
        player = (AUDIO_ROOT / "player.js").read_text(encoding="utf-8")
        self.assertIn('id="chapter-list"', html)
        self.assertIn("manifest.chapters", player)
        self.assertIn("document.createElement('audio')", player)


if __name__ == "__main__":
    unittest.main()
