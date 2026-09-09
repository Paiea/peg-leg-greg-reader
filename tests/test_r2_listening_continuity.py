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

    def test_audio_shelf_sorts_by_stable_number_and_reports_gaps_without_overclaiming(self):
        js = (AUDIO / "player.js").read_text(encoding="utf-8")
        self.assertIn("function orderedPlayable", js)
        self.assertIn(".sort((a, b) => Number(a.number) - Number(b.number))", js)
        self.assertIn("function availabilityLabel", js)
        self.assertIn("missing.length", js)
        self.assertIn("latest Chapter", js)
        self.assertIn("through Chapter", js)

    def test_audio_card_title_is_a_stable_same_page_permalink(self):
        js = (AUDIO / "player.js").read_text(encoding="utf-8")
        css = (AUDIO / "audio-front-door.css").read_text(encoding="utf-8")
        self.assertIn("headingLink.href = `#${id}`", js)
        self.assertIn("headingLink.textContent = chapter.title", js)
        self.assertIn("heading.append(headingLink)", js)
        self.assertIn(".chapter-card:target", css)

    def test_local_art_sync_registers_and_prunes_conventional_files_without_losing_metadata(self):
        from scripts.sync_r2_listening_art import sync_presentation

        manifest = {
            "chapters": [
                {"chapter_id": "ga-001", "number": 1, "title": "The Boy"},
                {"chapter_id": "ga-002", "number": 2, "title": "Two Things"},
                {"chapter_id": "ga-003", "number": 3, "title": "The Borrower"},
                {"chapter_id": "ga-004", "number": 4, "title": "Thirty Days"},
            ]
        }
        presentation = {
            "version": 1,
            "chapters": {
                "ga-001": {"quote": "Existing exact quote."},
                "ga-003": {
                    "image_src": "assets/art/chapter-003.webp",
                    "quote": "Keep me after art removal.",
                },
                "ga-004": {
                    "image_src": "assets/art/special-scene.webp",
                    "alt": "Manual nonconventional art.",
                },
            },
        }

        updated = sync_presentation(
            manifest,
            presentation,
            ["chapter-001.webp", "chapter-002.webp", "chapter-999.webp", "notes.txt"],
        )

        self.assertEqual(updated["chapters"]["ga-001"]["image_src"], "assets/art/chapter-001.webp")
        self.assertEqual(updated["chapters"]["ga-001"]["quote"], "Existing exact quote.")
        self.assertEqual(updated["chapters"]["ga-002"]["image_src"], "assets/art/chapter-002.webp")
        self.assertNotIn("image_src", updated["chapters"]["ga-003"])
        self.assertEqual(updated["chapters"]["ga-003"]["quote"], "Keep me after art removal.")
        self.assertEqual(updated["chapters"]["ga-004"]["image_src"], "assets/art/special-scene.webp")
        self.assertNotIn("ga-999", updated["chapters"])

        guide = (AUDIO / "assets" / "art" / "README.md").read_text(encoding="utf-8")
        self.assertIn("python scripts/sync_r2_listening_art.py", guide)
        self.assertIn("--check", guide)

    def test_art_sync_has_check_mode_and_current_presentation_is_in_sync(self):
        from scripts.sync_r2_listening_art import sync_presentation

        script = (ROOT / "scripts" / "sync_r2_listening_art.py").read_text(encoding="utf-8")
        self.assertIn("--check", script)
        self.assertIn("return 1", script)

        manifest = json.loads((AUDIO / "manifest.json").read_text(encoding="utf-8"))
        presentation = json.loads((AUDIO / "presentation.json").read_text(encoding="utf-8"))
        filenames = [path.name for path in (AUDIO / "assets" / "art").glob("chapter-*.webp")]
        self.assertEqual(sync_presentation(manifest, presentation, filenames), presentation)

    def test_presentation_metadata_only_targets_real_audio_ids_and_existing_chapter_art(self):
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
                self.assertTrue((AUDIO / metadata["image_src"]).is_file(), metadata["image_src"])


if __name__ == "__main__":
    unittest.main()
