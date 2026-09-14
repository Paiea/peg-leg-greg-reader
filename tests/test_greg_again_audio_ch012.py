import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "greg-again" / "audio"
R2 = ROOT / "r2"


class GregAgainChapter12AudioTest(unittest.TestCase):
    def test_chapter_12_is_durably_published(self):
        manifest = json.loads((AUDIO / "manifest.json").read_text(encoding="utf-8"))
        by_id = {item["chapter_id"]: item for item in manifest["chapters"]}
        entry = by_id["ga-012"]
        self.assertEqual(12, entry["number"])
        self.assertEqual("assets/light/chapter-012.mp3", entry["audio_src"])
        self.assertEqual("shared-greg-surface", entry["lens"])
        self.assertEqual("audio-score-light", entry["audio_finish"])
        self.assertEqual(23, entry["take_count"])
        self.assertEqual(608.328, entry["duration_seconds"])
        final = AUDIO / entry["audio_src"]
        self.assertTrue(final.exists())
        self.assertGreater(final.stat().st_size, 1_000_000)

        light_map = json.loads((AUDIO / "light/takes/012/short-takes.json").read_text(encoding="utf-8"))
        self.assertEqual(23, light_map["take_count"])
        self.assertEqual(23, len(light_map["takes"]))
        self.assertEqual("durable_takes_verified_and_assembled", light_map["status"])
        self.assertTrue(all(t.get("durable_file") for t in light_map["takes"]))
        self.assertTrue(all(t.get("audio_sha256") for t in light_map["takes"]))

        # Preserve the previous production generation as historical durability evidence.
        take_map = json.loads((AUDIO / "takes/012.json").read_text(encoding="utf-8"))
        self.assertEqual(25, take_map["take_count"])
        self.assertEqual(25, len(take_map["takes"]))
        for take in take_map["takes"]:
            self.assertEqual("verified", take["status"])
            durable = (AUDIO / "takes" / take["durable_audio"]).resolve()
            self.assertTrue(durable.exists())
            self.assertGreater(durable.stat().st_size, 10_000)

        meta = json.loads((R2 / "data/chapters/ch012.json").read_text(encoding="utf-8"))
        self.assertEqual("published", meta["audio"]["status"])
        self.assertEqual("../greg-again/audio/assets/chapter-012.mp3", meta["audio"]["path"])

    def test_chapter_12_preserves_audio_contract_and_original_provider_identity(self):
        script = (AUDIO / "scripts/012-the-stranger.md").read_text(encoding="utf-8")
        self.assertIn("DO NOT OPTIMIZE AWAY PROCESSING TIME", script)
        self.assertIn("SMOOTHNESS IS NOT AUTOMATICALLY CLARITY", script)
        self.assertIn("MEMORY ABSENCE MUST STAY ABSENCE", script)
        take_map = json.loads((AUDIO / "takes/012.json").read_text(encoding="utf-8"))
        self.assertEqual("98aef78da55b4520a8acf2c5636c7d56", take_map["historical_provider_work"]["context_id"])


if __name__ == "__main__":
    unittest.main()
