import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "greg-again" / "audio"
R2 = ROOT / "r2"

class GregAgainBatch012014Test(unittest.TestCase):
    def test_batch_012_014_is_durably_published(self):
        manifest = json.loads((AUDIO / "manifest.json").read_text(encoding="utf-8"))
        by_id = {item["chapter_id"]: item for item in manifest["chapters"]}
        expected = {12:("The Stranger",25,606.504),13:("The Fighter",28,653.952),14:("The Helper",29,678.096)}
        for chapter, (title, take_count, duration) in expected.items():
            entry = by_id[f"ga-{chapter:03d}"]
            self.assertEqual(title, entry["title"])
            self.assertEqual("shared-greg-surface", entry["lens"])
            self.assertEqual("processing-space", entry["audio_finish"])
            self.assertEqual(take_count, entry["take_count"])
            self.assertEqual(duration, entry["duration_seconds"])
            final = AUDIO / entry["audio_src"]
            self.assertTrue(final.exists())
            self.assertGreater(final.stat().st_size, 1_000_000)
            take_map = json.loads((AUDIO / "takes" / f"{chapter:03d}.json").read_text(encoding="utf-8"))
            self.assertEqual(take_count, take_map["take_count"])
            self.assertEqual(take_count, len(take_map["takes"]))
            for take in take_map["takes"]:
                self.assertEqual("verified", take["status"])
                self.assertTrue(take["provider_artifact"].endswith(".mp3"))
                durable = (AUDIO / "takes" / take["durable_audio"]).resolve()
                self.assertTrue(durable.exists())
                self.assertGreater(durable.stat().st_size, 10_000)
            meta = json.loads((R2 / "data/chapters" / f"ch{chapter:03d}.json").read_text(encoding="utf-8"))
            self.assertEqual("published", meta["audio"]["status"])
            self.assertEqual(f"../greg-again/audio/assets/chapter-{chapter:03d}.mp3", meta["audio"]["path"])

    def test_audio_finish_guardrails_are_durable(self):
        cases={"012-the-stranger.md":"MEMORY ABSENCE MUST STAY ABSENCE","013-the-good-sword.md":"A BETTER TOOL DOES NOT REPLACE JUDGMENT","014-the-back-room.md":"ORDINARY SPACE CARRIES HISTORY"}
        for filename, guardrail in cases.items():
            script=(AUDIO / "scripts" / filename).read_text(encoding="utf-8")
            self.assertIn("DO NOT OPTIMIZE AWAY PROCESSING TIME", script)
            self.assertIn("SMOOTHNESS IS NOT AUTOMATICALLY CLARITY", script)
            self.assertIn(guardrail, script)

    def test_chapter_12_preserves_original_provider_identity(self):
        take_map=json.loads((AUDIO / "takes/012.json").read_text(encoding="utf-8"))
        self.assertEqual("98aef78da55b4520a8acf2c5636c7d56", take_map["historical_provider_work"]["context_id"])

if __name__ == "__main__":
    unittest.main()
