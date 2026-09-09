import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "r2"


class R2Chapter4AudioRouteTest(unittest.TestCase):
    def test_chapter_four_routes_existing_published_audio(self):
        chapter = json.loads((R2 / "data/chapters/ch004.json").read_text(encoding="utf-8"))
        self.assertEqual("Thirty Days", chapter["title"])
        self.assertEqual("published", chapter["audio"]["status"])
        self.assertEqual(
            "../greg-again/audio/assets/chapter-004.mp3",
            chapter["audio"]["path"],
        )
        self.assertTrue((ROOT / "greg-again/audio/assets/chapter-004.mp3").exists())


if __name__ == "__main__":
    unittest.main()
