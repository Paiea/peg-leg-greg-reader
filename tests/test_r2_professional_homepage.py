import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "r2"


class R2ProfessionalHomepageTests(unittest.TestCase):
    def test_homepage_uses_new_responsive_hero_assets(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        self.assertIn("assets/images/r2-hero-wide.webp", html)
        self.assertIn("assets/images/r2-hero-portrait.webp", html)
        self.assertIn("<picture", html)
        self.assertNotIn("r2-harbor-hero.webp", html)

    def test_homepage_navigation_is_quiet_and_reader_focused(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        nav = html.split('<nav aria-label="Primary">', 1)[1].split("</nav>", 1)[0]
        self.assertIn("Chapters", nav)
        self.assertIn("About", nav)
        self.assertIn("Run 1", nav)
        self.assertNotIn(">Listen<", nav)
        self.assertNotIn(">Read<", nav)
        self.assertNotIn(">Look<", nav)

    def test_homepage_has_frontispiece_hero_without_floating_card(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        css = (R2 / "assets/css/r2-home.css").read_text(encoding="utf-8")
        self.assertIn('class="r2-home-hero-copy"', html)
        self.assertIn('class="r2-home-hero-media"', html)
        self.assertIn("position: absolute", css)
        self.assertNotIn("margin: -1.4rem auto 0", css)
        self.assertNotIn("box-shadow: 0 16px 36px", css)

    def test_homepage_prioritizes_listen_then_read(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        hero = html.split('<section class="r2-home-hero"', 1)[1].split("</section>", 1)[0]
        listen_index = hero.index("Start Listening")
        read_index = hero.index("Start Reading")
        self.assertLess(listen_index, read_index)
        self.assertNotIn(">Look<", hero)

    def test_homepage_uses_compact_lineage_and_no_empty_art_section(self):
        html = (R2 / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="r2-home-lineage"', html)
        self.assertNotIn('class="lineage-grid"', html)
        self.assertNotIn('class="section recent-art"', html)
        self.assertNotIn("Art will grow with the story.", html)


if __name__ == "__main__":
    unittest.main()
