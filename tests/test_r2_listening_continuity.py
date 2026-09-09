import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "r2"
AUDIO = ROOT / "greg-again" / "audio"


class R2ListeningContinuityTests(unittest.TestCase):
    def test_chapters_index_reuses_light_home_row_language(self):
        html = (R2 / "chapters" / "index.html").read_text(encoding="utf-8")
        js = (R2 / "assets" / "js" / "site.js").read_text(encoding="utf-8")
        self.assertIn('../assets/css/r2-home-clean.css', html)
        self.assertIn('<meta name="theme-color" content="#fbfaf7">', html)
        self.assertIn('class="home-main"', html)
        self.assertIn("article.className = 'chapter-row'", js)
        self.assertIn("actions.className = 'chapter-row-actions'", js)

    def test_home_and_chapters_route_listening_to_audio_shelf(self):
        home_js = (R2 / "assets" / "js" / "home.js").read_text(encoding="utf-8")
        site_js = (R2 / "assets" / "js" / "site.js").read_text(encoding="utf-8")
        self.assertIn("function audioShelfHref", home_js)
        self.assertIn("listen.href = audioShelfHref(chapter)", home_js)
        self.assertIn("function audioShelfHref", site_js)
        self.assertIn("listen.href = audioShelfHref(chapter)", site_js)

    def test_written_chapter_can_return_to_same_listening_shelf_card(self):
        js = (R2 / "assets" / "js" / "chapter.js").read_text(encoding="utf-8")
        self.assertIn("function listeningEditionHref", js)
        self.assertIn("Open in Listening Edition", js)
        self.assertIn("slot.append(audio, shelfLink)", js)

    def test_conventional_chapter_art_autoloads_without_presentation_entry(self):
        js = (AUDIO / "player.js").read_text(encoding="utf-8")
        self.assertIn("function conventionalArtSrc", js)
        self.assertIn("presentation.image_src || conventionalArtSrc(chapter)", js)
        guide = (AUDIO / "assets" / "art" / "README.md").read_text(encoding="utf-8")
        self.assertIn("no `presentation.json` image entry is required", guide)

    def test_presentation_metadata_only_targets_real_audio_ids_and_art_paths(self):
        manifest = json.loads((AUDIO / "manifest.json").read_text(encoding="utf-8"))
        presentation = json.loads((AUDIO / "presentation.json").read_text(encoding="utf-8"))
        audio_ids = {chapter["chapter_id"] for chapter in manifest.get("chapters", [])}

        hero = presentation.get("hero") or {}
        if hero.get("image_src"):
            self.assertTrue(hero["image_src"].startswith("assets/art/"))

        for stable_id, metadata in presentation.get("chapters", {}).items():
            self.assertIn(stable_id, audio_ids)
            if metadata.get("image_src"):
                self.assertTrue(metadata["image_src"].startswith("assets/art/"))


if __name__ == "__main__":
    unittest.main()
