import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class ThirdLegAudioLibraryConsistencyTests(unittest.TestCase):
    def test_record_001_archive_matches_published_record_audio(self):
        record = (ROOT / "3l" / "records" / "001.html").read_text(encoding="utf-8")
        archive = (ROOT / "3l" / "audio" / "index.html").read_text(encoding="utf-8")

        published_asset = "../assets/audio/record-001-headspace-v6.mp3"
        stale_asset = "../assets/audio/record-001.mp3"

        self.assertIn(published_asset, record)
        self.assertIn(published_asset, archive)
        self.assertNotIn(stale_asset, archive)


if __name__ == "__main__":
    unittest.main()
