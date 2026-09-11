import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO_ROOT = ROOT / "greg-again" / "audio"
R2_ROOT = ROOT / "r2"


class GregAgainAudioCatalogTest(unittest.TestCase):
    def test_catalog_uses_stable_chapter_identity(self):
        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        v2_manifest = json.loads((AUDIO_ROOT / "v2" / "manifest.json").read_text(encoding="utf-8"))
        verified_v2 = {
            chapter["number"]
            for chapter in v2_manifest.get("chapters", [])
            if chapter.get("status") == "verified"
        }
        self.assertIn("chapter_id and number are stable identity", manifest["identity_policy"])
        chapters = manifest["chapters"]
        by_id = {chapter["chapter_id"]: chapter for chapter in chapters}
        for number in range(1, 15):
            chapter_id = f"ga-{number:03d}"
            self.assertIn(chapter_id, by_id)
            self.assertEqual(number, by_id[chapter_id]["number"])
            expected_src = (
                f"assets/v2/chapter-{number:03d}.mp3"
                if number in verified_v2
                else f"assets/chapter-{number:03d}.mp3"
            )
            self.assertEqual(expected_src, by_id[chapter_id]["audio_src"])
        self.assertEqual("greg-dominant", by_id["ga-002"]["lens"])
        self.assertEqual("greg-dominant", by_id["ga-003"]["lens"])
        self.assertEqual("shared-greg-surface", by_id["ga-004"]["lens"])
        self.assertEqual("shared-greg-surface", by_id["ga-005"]["lens"])
        self.assertEqual("shared-greg-surface", by_id["ga-006"]["lens"])
        self.assertEqual("shared-greg-surface", by_id["ga-007"]["lens"])
        self.assertEqual("processing-space", by_id["ga-005"]["audio_finish"])
        self.assertEqual("processing-space", by_id["ga-006"]["audio_finish"])
        self.assertEqual("processing-space", by_id["ga-007"]["audio_finish"])
        self.assertEqual(31, by_id["ga-007"]["take_count"])
        self.assertEqual(623.448, by_id["ga-007"]["duration_seconds"])

    def test_chapters_two_through_seven_audio_are_durable_and_nontrivial(self):
        for number in (2, 3, 4, 5, 6, 7):
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
        self.assertIn("For one ugly second I was fifty-nine again in my head and nineteen everywhere that mattered.", script)
        self.assertIn("Support was what I had become.", script)

    def test_chapter_seven_anchors_motion_and_action_ownership(self):
        script = (AUDIO_ROOT / "scripts" / "007-the-extra-guard.md").read_text(encoding="utf-8")
        self.assertIn("DO NOT OPTIMIZE AWAY PROCESSING TIME", script)
        self.assertIn("PROCESSING SPACE", script)
        self.assertIn("MOTION NEEDS ANCHORS", script)
        self.assertIn("Don't stop it.", script)
