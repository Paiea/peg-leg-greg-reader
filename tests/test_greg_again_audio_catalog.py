import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO_ROOT = ROOT / "greg-again" / "audio"
R2_ROOT = ROOT / "r2"


class GregAgainAudioCatalogTest(unittest.TestCase):
    def test_catalog_publishes_chapters_one_through_six(self):
        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        chapters = manifest["chapters"]
        by_id = {chapter["chapter_id"]: chapter for chapter in chapters}

        for number in range(1, 7):
            self.assertIn(f"ga-{number:03d}", by_id)

        self.assertEqual("The Boy", by_id["ga-001"]["title"])
        self.assertEqual("The Novice", by_id["ga-002"]["title"])
        self.assertEqual("The Borrower", by_id["ga-003"]["title"])
        self.assertEqual("The Contractor", by_id["ga-004"]["title"])
        self.assertEqual("The Partner", by_id["ga-005"]["title"])
        self.assertEqual("The Troubleshooter", by_id["ga-006"]["title"])

        for number in range(1, 7):
            self.assertEqual(
                f"assets/chapter-{number:03d}.mp3",
                by_id[f"ga-{number:03d}"]["audio_src"],
            )

        self.assertEqual("greg-dominant", by_id["ga-002"]["lens"])
        self.assertEqual("greg-dominant", by_id["ga-003"]["lens"])
        self.assertEqual("shared-greg-surface", by_id["ga-004"]["lens"])
        self.assertEqual("shared-greg-surface", by_id["ga-005"]["lens"])
        self.assertEqual("shared-greg-surface", by_id["ga-006"]["lens"])
        self.assertEqual("processing-space", by_id["ga-005"]["audio_finish"])
        self.assertEqual("processing-space", by_id["ga-006"]["audio_finish"])

    def test_chapters_two_through_six_audio_are_durable_and_nontrivial(self):
        for number in (2, 3, 4, 5, 6):
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

    def test_chapter_five_preserves_processing_space_contract(self):
        script = (AUDIO_ROOT / "scripts" / "005-the-partner.md").read_text(encoding="utf-8")
        self.assertIn("DO NOT OPTIMIZE AWAY PROCESSING TIME", script)
        self.assertIn("PROCESSING SPACE", script)
        self.assertIn("SMOOTHNESS IS NOT AUTOMATICALLY CLARITY", script)
        self.assertIn("Being smarter had not removed the idiot.", script)
        self.assertIn("It had given him better arguments.", script)

    def test_chapter_six_uses_processing_space_for_spatial_causality(self):
        script = (AUDIO_ROOT / "scripts" / "006-the-first-customer.md").read_text(encoding="utf-8")
        self.assertIn("DO NOT OPTIMIZE AWAY PROCESSING TIME", script)
        self.assertIn("PROCESSING SPACE", script)
        self.assertIn("SPATIAL CAUSALITY MUST SURVIVE THE EAR", script)
        self.assertIn("It worked. Then it broke. Those are two facts.", script)
        self.assertIn(
            "For one ugly second I was fifty-nine again in my head and nineteen everywhere that mattered.",
            script,
        )
        self.assertIn("Support was what I had become.", script)

    def test_r2_chapter_five_routes_published_audio(self):
        chapter = json.loads((R2_ROOT / "data/chapters/ch005.json").read_text(encoding="utf-8"))
        self.assertEqual("The Partner", chapter["title"])
        self.assertEqual("published", chapter["audio"]["status"])
        self.assertEqual(
            "../greg-again/audio/assets/chapter-005.mp3",
            chapter["audio"]["path"],
        )

    def test_r2_chapter_six_routes_published_audio(self):
        chapter = json.loads((R2_ROOT / "data/chapters/ch006.json").read_text(encoding="utf-8"))
        self.assertEqual("The Troubleshooter", chapter["title"])
        self.assertEqual("published", chapter["audio"]["status"])
        self.assertEqual(
            "../greg-again/audio/assets/chapter-006.mp3",
            chapter["audio"]["path"],
        )

    def test_public_page_renders_catalog_instead_of_one_hardcoded_chapter(self):
        html = (AUDIO_ROOT / "index.html").read_text(encoding="utf-8")
        player = (AUDIO_ROOT / "player.js").read_text(encoding="utf-8")
        self.assertIn('id="chapter-list"', html)
        self.assertIn("manifest.chapters", player)
        self.assertIn("document.createElement('audio')", player)


if __name__ == "__main__":
    unittest.main()
