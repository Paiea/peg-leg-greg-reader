import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO_ROOT = ROOT / "greg-again" / "audio"
R2_ROOT = ROOT / "r2"


class GregAgainChapter22AudioTest(unittest.TestCase):
    def test_chapter_22_is_durable_and_routed(self):
        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        by_id = {chapter["chapter_id"]: chapter for chapter in manifest["chapters"]}
        chapter = by_id["ga-022"]
        self.assertEqual("The Neighbor", chapter["title"])
        self.assertEqual("shared-greg-surface", chapter["lens"])
        self.assertEqual("processing-space", chapter["audio_finish"])
        self.assertEqual(10, chapter["take_count"])
        self.assertEqual(731.616, chapter["duration_seconds"])
        self.assertEqual("assets/chapter-022.mp3", chapter["audio_src"])

        final_audio = AUDIO_ROOT / "assets" / "chapter-022.mp3"
        self.assertTrue(final_audio.exists())
        self.assertGreater(final_audio.stat().st_size, 10_000_000)

        take_map = json.loads((AUDIO_ROOT / "takes" / "022.json").read_text(encoding="utf-8"))
        self.assertEqual("verified_playable", take_map["status"])
        self.assertEqual("33b0bfef83dacb09c290b42b1213e652d86bd7cb", take_map["written_source_sha"])
        self.assertEqual(10, len(take_map["takes"]))
        self.assertEqual(731.616, take_map["assembled_duration_seconds"])
        for take in take_map["takes"]:
            self.assertEqual("artifact_captured", take["status"])
            durable = ROOT / take["durable_file"]
            self.assertTrue(durable.exists())
            self.assertGreater(durable.stat().st_size, 10_000)

        route = json.loads((R2_ROOT / "data" / "chapters" / "ch022.json").read_text(encoding="utf-8"))
        self.assertEqual("The Neighbor", route["title"])
        self.assertEqual("published", route["audio"]["status"])
        self.assertEqual("../greg-again/audio/assets/chapter-022.mp3", route["audio"]["path"])


if __name__ == "__main__":
    unittest.main()
