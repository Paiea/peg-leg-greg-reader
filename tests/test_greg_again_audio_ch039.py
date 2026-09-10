import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class TestGregAgainAudioCh039(unittest.TestCase):
    def test_ch039_publication_contract(self):
        manifest=json.loads((ROOT/"greg-again/audio/manifest.json").read_text())
        entry=next(c for c in manifest["chapters"] if c["chapter_id"]=="ga-039")
        self.assertEqual(entry["number"],39)
        self.assertEqual(entry["title"],"The East Desk")
        self.assertEqual(entry["take_count"],32)
        self.assertAlmostEqual(entry["duration_seconds"],628.104,places=3)
        self.assertEqual(entry["audio_src"],"assets/chapter-039.mp3")
        route=json.loads((ROOT/"r2/data/chapters/ch039.json").read_text())
        self.assertEqual(route["audio"],{"status":"published","path":"../greg-again/audio/assets/chapter-039.mp3"})
        reg=json.loads((ROOT/"r2/data/chapter-registry.json").read_text())
        self.assertEqual(reg["chapters"]["r2-ch039"]["pipeline"]["audio"],"published")
        takes=json.loads((ROOT/"greg-again/audio/production/039/takes.json").read_text())
        self.assertEqual(len(takes["takes"]),32)
        self.assertEqual([t["take"] for t in takes["takes"]],list(range(1,33)))
        final=ROOT/"greg-again/audio/assets/chapter-039.mp3"
        self.assertEqual(final.stat().st_size,5560533)
        self.assertEqual(hashlib.sha256(final.read_bytes()).hexdigest(),"ea2b6761297cc3ddf284dd5ad93e394aca28afcc4c4cbb28c88a28aaa9aa8070")
        self.assertTrue(takes["takes"][-1]["last_anchor"].endswith("..."))
        self.assertFalse((ROOT/".github/workflows/ga039-capture.yml").exists())
        self.assertFalse((ROOT/".github/workflows/ga039-publish-prep.yml").exists())

if __name__=="__main__": unittest.main()
