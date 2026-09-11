import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "r2"


class R2ProfessionalHomepageTests(unittest.TestCase):
    def test_homepage_uses_uploaded_banner_with_existing_cover_fallback(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        self.assertIn("assets/images/Home.png", html)
        self.assertIn("assets/images/r2-cover-wide.webp", html)
        self.assertNotIn("r2-harbor-hero.webp", html)

    def test_homepage_navigation_is_quiet_and_audio_first(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        nav = html.split('<nav class="site-nav" aria-label="Primary">', 1)[1].split("</nav>", 1)[0]
        self.assertIn(">Listen<", nav)
        self.assertIn(">Written<", nav)
        self.assertIn("About", nav)
        self.assertIn("Run 1", nav)
        self.assertNotIn(">Look<", nav)

    def test_homepage_uses_cover_and_entry_layout(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="cover-section"', html)
        self.assertIn('class="cover-frame"', html)
        self.assertIn('class="entry-panel"', html)
        self.assertIn('assets/css/r2-home-clean.css', html)
        self.assertNotIn('class="r2-home-hero"', html)

    def test_homepage_prioritizes_listen_then_written_reference(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        listen_index = html.index("Start Listening")
        read_index = html.index("Written rendition →")
        self.assertLess(listen_index, read_index)
        self.assertNotIn("Start Reading", html)
        self.assertNotIn(">Look<", html)

    def test_homepage_uses_compact_lineage_and_no_empty_art_section(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="lineage-strip"', html)
        self.assertNotIn('class="lineage-grid"', html)
        self.assertNotIn('class="section recent-art"', html)
        self.assertNotIn("Art will grow with the story.", html)


if __name__ == "__main__":
    unittest.main()
