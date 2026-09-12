import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
R2 = ROOT / 'r2'
AUDIO = ROOT / 'greg-again' / 'audio'


class R2MobileRefreshTests(unittest.TestCase):
    def test_home_uses_responsive_verified_webp_banner(self):
        html = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('<picture>', html)
        self.assertIn('assets/images/r2-hero-wide.webp', html)
        self.assertIn('assets/images/r2-hero-portrait.webp', html)
        self.assertNotIn('assets/images/Home.png', html)

    def test_audio_hero_uses_responsive_verified_webp_banner_without_duplicate_visible_title(self):
        html = (AUDIO / 'index.html').read_text(encoding='utf-8')
        self.assertIn('<picture>', html)
        self.assertIn('../../r2/assets/images/r2-cover-wide.webp', html)
        self.assertIn('../../r2/assets/images/r2-cover-portrait.webp', html)
        self.assertIn('<h1 id="listen-title" class="sr-only">Audio Library</h1>', html)
        self.assertNotIn('<p class="hero-brand">', html)
        self.assertNotIn('../../r2/assets/images/Library.png', html)

    def test_audio_cards_treat_missing_art_as_quiet_fallback(self):
        js = (AUDIO / 'player.js').read_text(encoding='utf-8')
        css = (AUDIO / 'audio.css').read_text(encoding='utf-8')
        self.assertIn("visual.classList.add('has-image')", js)
        self.assertIn("visual.classList.add('no-image')", js)
        self.assertIn("image.decoding = 'async'", js)
        self.assertIn('.chapter-visual.no-image', css)
        self.assertNotIn('repeating-linear-gradient', css)

    def test_mobile_audio_cards_are_compact(self):
        css = (AUDIO / 'audio.css').read_text(encoding='utf-8')
        self.assertIn('@media (max-width: 620px)', css)
        self.assertIn('.chapter-visual.has-image', css)
        self.assertIn('min-height: 124px', css)
        self.assertIn('.chapter-card-body { padding: 14px 14px 13px; }', css)


if __name__ == '__main__':
    unittest.main()
