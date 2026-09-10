import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "greg-again" / "audio"
R2 = ROOT / "r2"


class R2AudioFrontDoorTests(unittest.TestCase):
    def test_listening_edition_uses_light_editorial_shell(self):
        html = (AUDIO / "index.html").read_text(encoding="utf-8")
        css = (AUDIO / "audio.css").read_text(encoding="utf-8")
        shelf_css = (AUDIO / "audio-front-door.css").read_text(encoding="utf-8")
        self.assertIn("R2 Listening Edition", html)
        self.assertIn('id="availability-summary"', html)
        self.assertIn("Listening shelf", html)
        self.assertIn("color-scheme: light", css)
        self.assertNotIn("color-scheme: dark", css)
        self.assertIn("grid-template-columns: repeat(2", shelf_css)

    def test_presentation_metadata_is_optional_and_stable_identity_only(self):
        presentation = json.loads((AUDIO / "presentation.json").read_text(encoding="utf-8"))
        self.assertEqual(presentation["version"], 1)
        self.assertIn("hero", presentation)
        self.assertIn("chapters", presentation)
        for stable_id, metadata in presentation["chapters"].items():
            self.assertRegex(stable_id, r"^ga-\d{3}$")
            self.assertNotIn("title", metadata)
            self.assertNotIn("duration", metadata)
            self.assertNotIn("duration_seconds", metadata)
            self.assertNotIn("audio_src", metadata)
            self.assertNotIn("status", metadata)

    def test_audio_renderer_joins_optional_presentation_without_making_it_authority(self):
        js = (AUDIO / "player.js").read_text(encoding="utf-8")
        self.assertIn("loadOptionalPresentation", js)
        self.assertIn("function stableId", js)
        self.assertIn("Promise.all", js)
        self.assertIn("presentation.chapters[id]", js)
        self.assertIn("chapter-art", js)
        self.assertIn("chapter-quote", js)
        self.assertIn("availability-summary", js)
        self.assertIn("Audio chapters are temporarily unavailable.", js)

    def test_public_audio_page_does_not_expose_production_scaffolding(self):
        html = (AUDIO / "index.html").read_text(encoding="utf-8").lower()
        js = (AUDIO / "player.js").read_text(encoding="utf-8").lower()
        public = f"{html}\n{js}"
        for phrase in ["experiment", "production notes", "take count", "renderer adapter"]:
            self.assertNotIn(phrase, public)

    def test_homepage_prominently_routes_to_audio(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        self.assertIn("Start Listening", html)
        self.assertIn("../greg-again/audio/", html)
        self.assertIn("The audio shelf is the front door.", html)

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

    def test_availability_summary_exposes_frontier_without_overclaiming_gaps(self):
        js = (AUDIO / "player.js").read_text(encoding="utf-8")
        self.assertIn("function availabilityLabel", js)
        self.assertIn("through Chapter ${latest}", js)
        self.assertIn("latest Chapter ${latest}", js)
        self.assertIn("audio gap", js)
        self.assertIn("missing.length", js)

    def test_art_drop_folder_contract_is_documented_for_manual_uploads(self):
        guide = (AUDIO / "assets" / "art" / "README.md").read_text(encoding="utf-8")
        self.assertIn("listening-edition-hero.webp", guide)
        self.assertIn("chapter-NNN.webp", guide)
        self.assertIn("presentation.json", guide)
        self.assertIn("ga-NNN", guide)
        self.assertIn("Audio publication never waits on art", guide)


if __name__ == "__main__":
    unittest.main()
