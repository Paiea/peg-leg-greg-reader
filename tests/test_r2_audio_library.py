import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
AUDIO = ROOT / 'greg-again' / 'audio'


class R2AudioLibraryTests(unittest.TestCase):
    def test_audio_library_is_explicitly_listen_first(self):
        html = (AUDIO / 'index.html').read_text(encoding='utf-8')
        self.assertIn('AUDIO LIBRARY', html)
        self.assertIn('LISTEN FIRST', html)
        self.assertIn('Reading available. Listening is the point.', html)
        self.assertIn('id="continue-listening"', html)
        self.assertIn('id="chapter-search"', html)

    def test_audio_library_uses_uploaded_library_art_with_cover_fallback(self):
        html = (AUDIO / 'index.html').read_text(encoding='utf-8')
        self.assertIn('assets/images/Library.png', html)
        self.assertIn('r2-cover-wide.webp', html)

    def test_player_supports_resume_search_and_written_renditions(self):
        js = (AUDIO / 'player.js').read_text(encoding='utf-8')
        self.assertIn('localStorage', js)
        self.assertIn('timeupdate', js)
        self.assertIn('chapter-search', js)
        self.assertIn('Written rendition', js)
        self.assertIn('chapter.html?id=r2-ch', js)
        self.assertIn("document.createElement('audio')", js)

    def test_audio_library_uses_responsive_card_grid(self):
        css = ((AUDIO / 'audio.css').read_text(encoding='utf-8') + '\n' +
               (AUDIO / 'audio-front-door.css').read_text(encoding='utf-8'))
        self.assertIn('grid-template-columns: repeat(3, minmax(0, 1fr))', css)
        self.assertIn('grid-template-columns: 1fr', css)
        self.assertIn('.chapter-card', css)
        self.assertIn('.listen-warning', css)

    def test_desktop_hero_separates_copy_from_art_while_mobile_keeps_overlay(self):
        css = (AUDIO / 'audio-front-door.css').read_text(encoding='utf-8')
        self.assertIn('@media (min-width: 761px)', css)
        self.assertIn('inset: 0 0 0 38%', css)
        self.assertIn('width: 62%', css)
        self.assertIn('width: 38%', css)
        self.assertIn('@media (max-width: 760px)', css)
        self.assertIn('inset: auto 0 0', css)


if __name__ == '__main__':
    unittest.main()
