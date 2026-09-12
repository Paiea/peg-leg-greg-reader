import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
R2 = ROOT / 'r2'


class R2ListenFirstSiteTests(unittest.TestCase):
    def test_home_prefers_listening_and_uses_responsive_banner(self):
        html = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('assets/images/r2-hero-wide.webp', html)
        self.assertIn('assets/images/r2-hero-portrait.webp', html)
        self.assertNotIn('assets/images/Home.png', html)
        self.assertIn('▶ Start Listening', html)
        self.assertIn('Written rendition →', html)
        self.assertNotIn('Start Reading</a>', html)
        self.assertNotIn('id="chapter-list"', html)
        self.assertIn('Written reference', html)

    def test_chapter_prose_is_one_intentional_click_away(self):
        html = (R2 / 'chapter.html').read_text(encoding='utf-8')
        js = (R2 / 'assets/js/chapter.js').read_text(encoding='utf-8')
        self.assertIn('<details id="read"', html)
        self.assertIn('Read written rendition', html)
        self.assertIn('location.hash === \'#read\'', js)
        self.assertIn('details.open = true', js)

    def test_written_shelf_points_back_to_audio_and_prioritizes_listen_actions(self):
        html = (R2 / 'chapters/index.html').read_text(encoding='utf-8')
        js = (R2 / 'assets/js/site.js').read_text(encoding='utf-8')
        css = (R2 / 'assets/css/r2-listen-first-shared.css').read_text(encoding='utf-8')
        self.assertIn('Prefer listening?', html)
        self.assertIn('Open Audio Library', html)
        self.assertIn('chapter-action-listen', js)
        self.assertIn('chapter-action-read', js)
        self.assertIn('.chapter-action-listen', css)


if __name__ == '__main__':
    unittest.main()
