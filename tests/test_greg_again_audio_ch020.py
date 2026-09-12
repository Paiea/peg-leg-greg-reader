import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "greg-again" / "audio"
R2 = ROOT / "r2"


class GregAgainChapter20AudioTest(unittest.TestCase):
    def test_chapter_20_current_light_audio_is_durable_and_published(self):
        manifest = json.loads((AUDIO / "manifest.json").read_text(encoding="utf-8"))
        chapter = {c["chapter_id"]: c for c in manifest["chapters"]}["ga-020"]
        self.assertEqual(20, chapter["number"])
        self.assertEqual("Ward Hand", chapter["title"])
        self.assertEqual("audio-score-light", chapter["audio_finish"])
        self.assertEqual(38, chapter["take_count"])
        self.assertEqual(995.376, chapter["duration_seconds"])
        self.assertEqual("assets/light/chapter-020.mp3", chapter["audio_src"])

        final = AUDIO / chapter["audio_src"]
        self.assertTrue(final.exists())
        self.assertGreater(final.stat().st_size, 8_000_000)

        take_map = json.loads(
            (AUDIO / "light" / "takes" / "020" / "short-takes.json").read_text(encoding="utf-8")
        )
        self.assertEqual("ga-020", take_map["chapter_id"])
        self.assertEqual("light", take_map["generation"])
        self.assertEqual("Ward Hand", take_map["title"])
        self.assertEqual("deep", take_map["voice"])
        self.assertEqual("durable_takes_verified_and_assembled", take_map["status"])
        self.assertEqual(38, take_map["take_count"])
        self.assertEqual(38, len(take_map["takes"]))
        self.assertEqual(list(range(1, 39)), [take["order"] for take in take_map["takes"]])
        for take in take_map["takes"]:
            durable = ROOT / take["durable_file"]
            self.assertTrue(durable.exists())
            self.assertGreater(durable.stat().st_size, 10_000)
            self.assertEqual(64, len(take["audio_sha256"]))

        route = json.loads((R2 / "data" / "chapters" / "ch020.json").read_text(encoding="utf-8"))
        self.assertEqual("Ward Hand", route["title"])
        self.assertEqual("published", route["audio"]["status"])

        registry = json.loads((R2 / "data" / "chapter-registry.json").read_text(encoding="utf-8"))
        self.assertEqual("Ward Hand", registry["chapters"]["r2-ch020"]["title"])
        self.assertEqual("published", registry["chapters"]["r2-ch020"]["pipeline"]["audio"])


if __name__ == "__main__":
    unittest.main()
