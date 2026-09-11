import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "r2"
AUDIO = ROOT / "greg-again" / "audio"


class R2AudioFrontDoorTests(unittest.TestCase):
    def test_audio_page_is_presented_as_the_listening_edition(self):
        html = (AUDIO / "index.html").read_text(encoding="utf-8")
        self.assertIn("AUDIO LIBRARY", html)
        self.assertIn("LISTEN FIRST", html)
        self.assertIn("../../r2/assets/images/Library.png", html)
        self.assertIn("../../r2/assets/images/r2-cover-wide.webp", html)
        self.assertNotIn("Audio Experiments", html)
        self.assertNotIn("Listening lab", html)
        self.assertNotIn("Experimental", html)
        self.assertNotIn("proving render", html)

    def test_audio_player_hides_production_scaffolding(self):
        js = (AUDIO / "player.js").read_text(encoding="utf-8")
        self.assertNotIn("performance takes", js)
        self.assertNotIn("Playable experimental render", js)
        self.assertNotIn("Approved render", js)
        self.assertNotIn("chapter.note", js)

    def test_homepage_features_the_listening_edition(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        self.assertIn("Listening edition", html)
        self.assertIn("../greg-again/audio/", html)
        self.assertIn("Start Listening", html)
        self.assertIn('class="button button-primary" href="../greg-again/audio/"', html)


if __name__ == "__main__":
    unittest.main()
