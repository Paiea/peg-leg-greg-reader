import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
R2 = ROOT / 'r2'
AUDIO = ROOT / 'greg-again' / 'audio'


class R2ReaderStyleTests(unittest.TestCase):
    def test_shared_reader_css_is_clean_and_parchment_based(self):
        css = (R2 / 'assets/css/r2.css').read_text(encoding='utf-8')
        self.assertNotIn('<<<<<<<', css)
        self.assertNotIn('=======', css)
        self.assertNotIn('>>>>>>>', css)
        self.assertIn('--paper:', css)
        self.assertIn('--ink:', css)
        self.assertIn('background: var(--paper)', css)
        self.assertIn("'Iowan Old Style'", css)
        self.assertIn('Baskerville', css)

    def test_homepage_uses_same_parchment_palette_and_book_type(self):
        css = (R2 / 'assets/css/r2-home-clean.css').read_text(encoding='utf-8')
        html = (R2 / 'index.html').read_text(encoding='utf-8')
        self.assertIn('color-scheme: light', css)
        self.assertIn('--paper: #e5d8bd', css)
        self.assertIn('--ink: #241d16', css)
        self.assertIn('background: var(--paper)', css)
        self.assertIn("'Iowan Old Style'", css)
        self.assertIn('Baskerville', css)
        self.assertIn('<meta name="theme-color" content="#e5d8bd">', html)

    def test_r2_surfaces_expose_audio_experiments_as_first_class_navigation(self):
        homepage = (R2 / 'index.html').read_text(encoding='utf-8')
        chapter = (R2 / 'chapter.html').read_text(encoding='utf-8')
        self.assertIn('../greg-again/audio/', homepage)
        self.assertIn('>Audio<', homepage)
        self.assertIn('../greg-again/audio/', chapter)
        self.assertIn('>Audio<', chapter)
        for path in ['chapters/index.html', 'gallery/index.html', 'about/index.html']:
            html = (R2 / path).read_text(encoding='utf-8')
            self.assertIn('../../greg-again/audio/', html, path)
            self.assertIn('>Audio<', html, path)

    def test_audio_experiments_links_back_to_r2_and_matches_publication_surface(self):
        html = (AUDIO / 'index.html').read_text(encoding='utf-8')
        css = (AUDIO / 'audio.css').read_text(encoding='utf-8')
        self.assertIn('PEG-LEG GREG', html)
        self.assertIn('../../r2/', html)
        self.assertIn('R2 Home', html)
        self.assertIn('../../r2/chapters/', html)
        self.assertIn('Chapters', html)
        self.assertIn('color-scheme: light', css)
        self.assertIn('--paper: #e5d8bd', css)
        self.assertIn('background: var(--paper)', css)
        self.assertIn("'Iowan Old Style'", css)

    def test_chapter_page_prioritizes_reading_over_panels(self):
        css = (R2 / 'assets/css/r2.css').read_text(encoding='utf-8')
        self.assertIn('.chapter-page', css)
        self.assertIn('.reading-copy', css)
        self.assertIn('max-width: 720px', css)
        self.assertIn('line-height: 1.82', css)
        self.assertIn('.audio-panel', css)
        self.assertIn('max-width: 760px', css)
        self.assertIn('.written-panel', css)

    def test_chapter_shell_uses_story_brand_and_quiet_navigation(self):
        html = (R2 / 'chapter.html').read_text(encoding='utf-8')
        self.assertIn('PEG-LEG GREG', html)
        self.assertIn('R2', html)
        self.assertIn('Chapters', html)
        self.assertIn('About', html)
        self.assertIn('Run 1', html)
        self.assertNotIn('>Look<', html)

    def test_audio_renderer_does_not_repeat_internal_rendition_label(self):
        js = (R2 / 'assets/js/chapter.js').read_text(encoding='utf-8')
        self.assertNotIn("label.className = 'audio-label'", js)
        self.assertNotIn('chapter.audio.label', js)

    def test_secondary_pages_share_story_brand_and_plain_language_nav(self):
        for path in ['chapters/index.html', 'gallery/index.html', 'about/index.html']:
            html = (R2 / path).read_text(encoding='utf-8')
            self.assertIn('PEG-LEG GREG', html, path)
            self.assertIn('Run 1', html, path)
            self.assertNotIn('>Look<', html, path)
            self.assertNotIn('>Listen<', html, path)
            self.assertNotIn('>Read<', html, path)


if __name__ == '__main__':
    unittest.main()
