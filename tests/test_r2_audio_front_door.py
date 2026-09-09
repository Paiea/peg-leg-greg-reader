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

    def test_audio_cards_have_stable_deep_link_anchors(self):
        js = (AUDIO / "player.js").read_text(encoding="utf-8")
        self.assertIn("card.id = id", js)
        self.assertIn("card.dataset.chapterId = id", js)

    def test_each_audio_card_routes_to_the_matching_written_reference(self):
        js = (AUDIO / "player.js").read_text(encoding="utf-8")
        self.assertIn("function writtenReferenceHref", js)
        self.assertIn("../../r2/chapter.html?id=", js)
        self.assertIn("Written reference", js)
        self.assertIn("#read", js)

    def test_start_listening_routes_to_first_playable_chapter(self):
        html = (AUDIO / "index.html").read_text(encoding="utf-8")
        js = (AUDIO / "player.js").read_text(encoding="utf-8")
        self.assertIn('id="hero-listen-start"', html)
        self.assertIn("startListening.href = `#${stableId(playable[0])}`", js)

    def test_availability_summary_exposes_current_audio_frontier(self):
        js = (AUDIO / "player.js").read_text(encoding="utf-8")
        self.assertIn("const latestPlayable = playable[playable.length - 1]", js)
        self.assertIn("through Chapter ${latestPlayable.number}", js)

    def test_art_drop_folder_contract_is_documented_for_manual_uploads(self):
        guide = (AUDIO / "assets" / "art" / "README.md").read_text(encoding="utf-8")
        self.assertIn("listening-edition-hero.webp", guide)
        self.assertIn("chapter-NNN.webp", guide)
        self.assertIn("presentation.json", guide)
        self.assertIn("ga-NNN", guide)
        self.assertIn("Audio publication never waits on art", guide)


if __name__ == "__main__":
    unittest.main()
