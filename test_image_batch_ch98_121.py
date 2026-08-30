import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parent
MANIFEST = ROOT / "publishing" / "image_batch_ch98_121_001.json"


class ImageBatchTest(unittest.TestCase):
    def test_manifest_batch_is_fully_placed(self):
        batch = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(batch["generated_count"], 30)
        self.assertEqual(len(batch["items"]), 30)
        for item in batch["items"]:
            target = ROOT / item["target"]
            chapter = ROOT / "chapters" / f'{item["chapter"]}.html'
            self.assertTrue(target.exists(), target)
            self.assertIn(f'../{item["target"]}', chapter.read_text(encoding="utf-8"))
        self.assertTrue((ROOT / batch["contact_sheet"]).exists())


if __name__ == "__main__":
    unittest.main()
