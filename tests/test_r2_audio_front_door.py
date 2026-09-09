import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "r2"
AUDIO = ROOT / "greg-again" / "audio"


class R2AudioFrontDoorTests(unittest.TestCase):
    def test_audio_page_is_presented_as_the_listening_edition(self):
        html = (AUDIO / "index.html").read_text(encoding="utf-8")
        self.assertIn("Peg-Leg Greg R2", html)
        self.assertIn("R2 Listening Edition", html)
        self.assertIn("../../r2/assets/images/r2-cover-wide.webp", html)
        self.assertNotIn("Audio Experiments", html)
        self.assertNotIn("Listening lab", html)
        self.assertNotIn("Experimental", html)
        self.assertNotIn("proving render", html)

    def test_audio_page_uses_light_listening_edition_shell(self):
        html = (AUDIO / "index.html").read_text(encoding="utf-8")
        css = (AUDIO / "audio.css").read_text(encoding="utf-8")
        front_css = (AUDIO / "audio-front-door.css").read_text(encoding="utf-8")
        self.assertIn("R2 Listening Edition", html)
        self.assertIn('id="availability-summary"', html)
        self.assertIn('id="chapter-list"', html)
        self.assertNotIn("color-scheme: dark", css + front_css)
        self.assertIn("--paper:", css)
        self.assertIn("--accent:", css + front_css)

    def test_presentation_manifest_is_stable_identity_only(self):
        payload = json.loads((AUDIO / "presentation.json").read_text(encoding="utf-8"))
        for stable_id, metadata in payload.get("chapters", {}).items():
            self.assertRegex(stable_id, r"^ga-\d{3}$")
            self.assertNotIn("title", metadata)
            self.assertNotIn("duration_seconds", metadata)
            self.assertNotIn("audio_src", metadata)
            self.assertNotIn("published", metadata)

    def test_player_joins_optional_presentation_metadata_without_blocking_audio(self):
        js = (AUDIO / "player.js").read_text(encoding="utf-8")
        self.assertIn("presentation.json", js)
        self.assertIn("stableId", js)
        self.assertIn("Promise", js)
        self.assertIn("availability-summary", js)
        self.assertIn("chapter-art", js)
        self.assertIn("chapter-quote", js)
        self.assertIn("Audio chapters are temporarily unavailable.", js)

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
