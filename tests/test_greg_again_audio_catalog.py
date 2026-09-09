import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO_ROOT = ROOT / "greg-again" / "audio"


class GregAgainAudioCatalogTest(unittest.TestCase):
    def test_catalog_publishes_chapters_one_and_two(self):
        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        chapters = manifest["chapters"]
        by_id = {chapter["chapter_id"]: chapter for chapter in chapters}

        self.assertIn("ga-001", by_id)
        self.assertIn("ga-002", by_id)
        self.assertEqual("The Boy", by_id["ga-001"]["title"])
        self.assertEqual("Two Things", by_id["ga-002"]["title"])
        self.assertEqual("assets/chapter-001.mp3", by_id["ga-001"]["audio_src"])
        self.assertEqual("assets/chapter-002.mp3", by_id["ga-002"]["audio_src"])
        self.assertEqual("greg-dominant", by_id["ga-002"]["lens"])

    def test_chapter_two_audio_is_durable_and_nontrivial(self):
        chapter_two = AUDIO_ROOT / "assets" / "chapter-002.mp3"
        self.assertTrue(chapter_two.exists())
        self.assertGreater(chapter_two.stat().st_size, 1_000_000)

    def test_public_page_renders_catalog_instead_of_one_hardcoded_chapter(self):
        html = (AUDIO_ROOT / "index.html").read_text(encoding="utf-8")
        player = (AUDIO_ROOT / "player.js").read_text(encoding="utf-8")
        self.assertIn('id="chapter-list"', html)
        self.assertIn("manifest.chapters", player)
        self.assertIn("document.createElement('audio')", player)


if __name__ == "__main__":
    unittest.main()
