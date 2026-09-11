import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO_ROOT = ROOT / "greg-again" / "audio"
R2_ROOT = ROOT / "r2"


class GregAgainAudioCatalogTest(unittest.TestCase):
    def test_catalog_uses_stable_chapter_identity(self):
        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        v2_manifest = json.loads((AUDIO_ROOT / "v2/manifest.json").read_text(encoding="utf-8"))
        v2_numbers = {chapter["number"] for chapter in v2_manifest.get("chapters", [])}
        self.assertIn("chapter_id and number are stable identity", manifest["identity_policy"])
        chapters = manifest["chapters"]
        by_id = {chapter["chapter_id"]: chapter for chapter in chapters}
        for number in range(1, 15):
            chapter_id = f"ga-{number:03d}"
            self.assertIn(chapter_id, by_id)
            self.assertEqual(number, by_id[chapter_id]["number"])
            generation = "v2/" if number in v2_numbers else ""
            self.assertEqual(f"assets/{generation}chapter-{number:03d}.mp3", by_id[chapter_id]["audio_src"])
        self.assertEqual("greg-dominant", by_id["ga-002"]["lens"])
        self.assertEqual("greg-dominant", by_id["ga-003"]["lens"])
        self.assertEqual("shared-greg-surface", by_id["ga-004"]["lens"])
        self.assertEqual("shared-greg-surface", by_id["ga-005"]["lens"])
        self.assertEqual("shared-greg-surface", by_id["ga-006"]["lens"])
        self.assertEqual("shared-greg-surface", by_id["ga-007"]["lens"])
        self.assertEqual("processing-space", by_id["ga-005"]["audio_finish"])
        self.assertEqual("processing-space", by_id["ga-006"]["audio_finish"])
        self.assertEqual("processing-space", by_id["ga-007"]["audio_finish"])
        self.assertEqual(14, by_id["ga-007"]["take_count"])
        self.assertEqual(818.136, by_id["ga-007"]["duration_seconds"])

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
        self.assertIn("Turn it.", script)
        self.assertIn("Horses first.", script)
        self.assertIn("The world had not paused because I left the city.", script)
        self.assertIn("Also progress.", script)
        self.assertIn("Production takes: **14**", script)

    def test_r2_chapter_five_routes_published_audio(self):
        chapter = json.loads((R2_ROOT / "data/chapters/ch005.json").read_text(encoding="utf-8"))
        self.assertEqual("The Partner", chapter["title"])
        self.assertEqual("published", chapter["audio"]["status"])
        self.assertEqual("../greg-again/audio/assets/chapter-005.mp3", chapter["audio"]["path"])

    def test_r2_chapter_six_routes_published_audio(self):
        chapter = json.loads((R2_ROOT / "data/chapters/ch006.json").read_text(encoding="utf-8"))
        self.assertEqual("The Troubleshooter", chapter["title"])
        self.assertEqual("published", chapter["audio"]["status"])
        self.assertEqual("../greg-again/audio/assets/chapter-006.mp3", chapter["audio"]["path"])

    def test_r2_chapter_seven_routes_published_audio(self):
        chapter = json.loads((R2_ROOT / "data/chapters/ch007.json").read_text(encoding="utf-8"))
        self.assertEqual("The Extra Guard", chapter["title"])
        self.assertEqual("published", chapter["audio"]["status"])
        self.assertEqual("../greg-again/audio/assets/chapter-007.mp3", chapter["audio"]["path"])

    def test_chapter_ten_preserves_time_residue_and_publishes_audio(self):
        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        by_id = {chapter["chapter_id"]: chapter for chapter in manifest["chapters"]}
        self.assertIn("ga-010", by_id)
        self.assertEqual(10, by_id["ga-010"]["number"])
        self.assertEqual("shared-greg-surface", by_id["ga-010"]["lens"])
        self.assertEqual("processing-space", by_id["ga-010"]["audio_finish"])
        self.assertEqual(12, by_id["ga-010"]["take_count"])
        self.assertEqual(710.544, by_id["ga-010"]["duration_seconds"])
        self.assertEqual("assets/chapter-010.mp3", by_id["ga-010"]["audio_src"])
        audio = AUDIO_ROOT / "assets" / "chapter-010.mp3"
        self.assertTrue(audio.exists())
        self.assertGreater(audio.stat().st_size, 10_000_000)
        script = (AUDIO_ROOT / "scripts" / "010-the-returner.md").read_text(encoding="utf-8")
        self.assertIn("DO NOT OPTIMIZE AWAY PROCESSING TIME", script)
        self.assertIn("PROCESSING SPACE", script)
        self.assertIn("TIME MUST LEAVE RESIDUE", script)
        self.assertIn("Time had happened.", script)
        self.assertIn("That was different from time passing.", script)
        take_map = (AUDIO_ROOT / "scripts" / "010-the-returner-takes.md").read_text(encoding="utf-8")
        self.assertIn("Production takes: **12**", take_map)
        for number in range(1, 13):
            take = AUDIO_ROOT / "assets" / "chunks" / "010" / f"{number:02d}.mp3"
            self.assertTrue(take.exists())
            self.assertGreater(take.stat().st_size, 10_000)
        chapter = json.loads((R2_ROOT / "data/chapters/ch010.json").read_text(encoding="utf-8"))
        self.assertEqual("The Returner", chapter["title"])
        self.assertEqual("published", chapter["audio"]["status"])
        self.assertEqual("../greg-again/audio/assets/chapter-010.mp3", chapter["audio"]["path"])

    def test_chapter_eleven_preserves_future_uncertainty_and_publishes_audio(self):
        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        by_id = {chapter["chapter_id"]: chapter for chapter in manifest["chapters"]}
        self.assertIn("ga-011", by_id)
        self.assertEqual(11, by_id["ga-011"]["number"])
        self.assertEqual("shared-greg-surface", by_id["ga-011"]["lens"])
        self.assertEqual("processing-space", by_id["ga-011"]["audio_finish"])
        self.assertEqual("assets/chapter-011.mp3", by_id["ga-011"]["audio_src"])
        audio = AUDIO_ROOT / "assets" / "chapter-011.mp3"
        self.assertTrue(audio.exists())
        self.assertGreater(audio.stat().st_size, 1_000_000)
        script = (AUDIO_ROOT / "scripts" / "011-the-gate-hand.md").read_text(encoding="utf-8")
        self.assertIn("DO NOT OPTIMIZE AWAY PROCESSING TIME", script)
        self.assertIn("PROCESSING SPACE", script)
        self.assertIn("FUTURE KNOWLEDGE IS NOT PRESENT PROOF", script)
        self.assertIn("Correct future fact.", script)
        self.assertIn("Missing history.", script)
        self.assertIn("For once, I let that remain true.", script)
        chapter = json.loads((R2_ROOT / "data/chapters/ch011.json").read_text(encoding="utf-8"))
        self.assertEqual("The Gate Hand", chapter["title"])
        self.assertEqual("published", chapter["audio"]["status"])
        self.assertEqual("../greg-again/audio/assets/chapter-011.mp3", chapter["audio"]["path"])

    def test_chapter_thirteen_preserves_tool_judgment_and_publishes_audio(self):
        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        by_id = {chapter["chapter_id"]: chapter for chapter in manifest["chapters"]}
        self.assertIn("ga-013", by_id)
        self.assertEqual(13, by_id["ga-013"]["number"])
        self.assertEqual("shared-greg-surface", by_id["ga-013"]["lens"])
        self.assertEqual("processing-space", by_id["ga-013"]["audio_finish"])
        self.assertEqual(13, by_id["ga-013"]["take_count"])
        self.assertEqual(621.456, by_id["ga-013"]["duration_seconds"])
        self.assertEqual("assets/chapter-013.mp3", by_id["ga-013"]["audio_src"])
        audio = AUDIO_ROOT / "assets" / "chapter-013.mp3"
        self.assertTrue(audio.exists())
        self.assertGreater(audio.stat().st_size, 9_000_000)
        script = (AUDIO_ROOT / "scripts" / "013-the-fighter.md").read_text(encoding="utf-8")
        self.assertIn("THE RIGHT TOOL IS NOT THE RIGHT ANSWER", script)
        self.assertIn("production takes: 13", script)
        take_map = json.loads((AUDIO_ROOT / "takes" / "013.json").read_text(encoding="utf-8"))
        self.assertEqual(13, len(take_map["takes"]))
        self.assertEqual(["01", "02", "03a", "03b", "04", "05", "06", "07", "08", "09", "10", "11", "12"], [take["take"] for take in take_map["takes"]])
        for take in take_map["takes"]:
            durable = ROOT / take["durable_file"]
            self.assertTrue(durable.exists())
            self.assertGreater(durable.stat().st_size, 10_000)
        chapter = json.loads((R2_ROOT / "data/chapters/ch013.json").read_text(encoding="utf-8"))
        self.assertEqual("The Fighter", chapter["title"])
        self.assertEqual("published", chapter["audio"]["status"])
        self.assertEqual("../greg-again/audio/assets/chapter-013.mp3", chapter["audio"]["path"])

    def test_chapter_nineteen_recovered_audio_is_durable(self):
        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        by_id = {chapter["chapter_id"]: chapter for chapter in manifest["chapters"]}
        self.assertIn("ga-019", by_id)
        chapter = by_id["ga-019"]
        self.assertEqual(19, chapter["number"])
        self.assertEqual(36, chapter["take_count"])
        self.assertEqual(868.68, chapter["duration_seconds"])
        self.assertEqual("assets/chapter-019.mp3", chapter["audio_src"])
        audio = AUDIO_ROOT / "assets" / "chapter-019.mp3"
        self.assertTrue(audio.exists())
        self.assertGreater(audio.stat().st_size, 10_000_000)

    def test_chapter_twenty_one_preserves_contact_and_publishes_audio(self):
        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        by_id = {chapter["chapter_id"]: chapter for chapter in manifest["chapters"]}
        self.assertIn("ga-021", by_id)
        self.assertEqual(21, by_id["ga-021"]["number"])
        self.assertEqual("shared-greg-surface", by_id["ga-021"]["lens"])
        self.assertEqual("processing-space", by_id["ga-021"]["audio_finish"])
        self.assertEqual(13, by_id["ga-021"]["take_count"])
        self.assertEqual(771.816, by_id["ga-021"]["duration_seconds"])
        self.assertEqual("assets/chapter-021.mp3", by_id["ga-021"]["audio_src"])
        audio = AUDIO_ROOT / "assets" / "chapter-021.mp3"
        self.assertTrue(audio.exists())
        self.assertGreater(audio.stat().st_size, 10_000_000)
        script = (AUDIO_ROOT / "scripts" / "021-the-reply.md").read_text(encoding="utf-8")
        self.assertIn("DO NOT OPTIMIZE AWAY PROCESSING TIME", script)
        self.assertIn("CONTACT, NOT DOCUMENTATION", script)
        take_map = (AUDIO_ROOT / "scripts" / "021-the-reply-takes.md").read_text(encoding="utf-8")
        self.assertIn("Production takes: **13**", take_map)
        for number in range(1, 14):
            take = AUDIO_ROOT / "assets" / "chunks" / "021" / f"{number:02d}.mp3"
            self.assertTrue(take.exists())
            self.assertGreater(take.stat().st_size, 10_000)
        chapter = json.loads((R2_ROOT / "data/chapters/ch021.json").read_text(encoding="utf-8"))
        self.assertEqual("The Letter Writer", chapter["title"])
        self.assertEqual("published", chapter["audio"]["status"])
        self.assertEqual("../greg-again/audio/assets/chapter-021.mp3", chapter["audio"]["path"])
