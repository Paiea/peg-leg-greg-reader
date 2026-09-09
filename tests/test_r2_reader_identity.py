import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
R2 = ROOT / 'r2'


class R2ReaderIdentityTests(unittest.TestCase):
    def test_home_stays_light_while_reader_surface_is_dark(self):
        home_css = (R2 / 'assets/css/r2-home-clean.css').read_text(encoding='utf-8')
        reader_css = (R2 / 'assets/css/r2.css').read_text(encoding='utf-8')

        self.assertIn('color-scheme: light', home_css)
        self.assertIn('--paper: #fbfaf7', home_css)
        self.assertIn('--ink: #231f1a', home_css)
        self.assertIn('--link: #3e4a42', home_css)

        self.assertIn('color-scheme: dark', reader_css)
        self.assertIn('--paper: #171614', reader_css)
        self.assertIn('--ink: #e8e2d9', reader_css)
        self.assertIn('--muted: #aaa197', reader_css)
        self.assertIn('--link: #bdc8bd', reader_css)
        self.assertNotIn('--gold:', reader_css)

    def test_r2_chapter_titles_use_embodied_default_grammar(self):
        project = json.loads((R2 / 'data/project.json').read_text(encoding='utf-8'))
        titles = []
        for chapter_id in project['chapters']:
            number = int(chapter_id[-3:])
            chapter = json.loads((R2 / f'data/chapters/ch{number:03d}.json').read_text(encoding='utf-8'))
            titles.append(chapter['title'])

        self.assertGreaterEqual(len(titles), 19)
        for title in titles[:19]:
            self.assertRegex(title, r'^The [A-Z][A-Za-z\' -]+$', title)

    def test_reader_chapter_heading_is_centered_book_style(self):
        html = (R2 / 'chapter.html').read_text(encoding='utf-8')
        css = (R2 / 'assets/css/r2.css').read_text(encoding='utf-8')
        self.assertIn('class="chapter-header"', html)
        self.assertIn('.chapter-header {', css)
        self.assertIn('text-align: center', css)
        self.assertIn('max-width: 760px', css)

    def test_run_one_and_r2_cross_link_each_other(self):
        run1_home_updater = (ROOT / 'scripts/update_reader_navigation.py').read_text(encoding='utf-8')
        run1_generator = (ROOT / 'scripts/generate_illustrated.py').read_text(encoding='utf-8')
        run1_shell_updater = (ROOT / 'scripts/update_showcase_chapter_shells.py').read_text(encoding='utf-8')
        r2_home = (R2 / 'index.html').read_text(encoding='utf-8')

        self.assertIn('href="r2/"', run1_home_updater)
        self.assertIn('href="../r2/"', run1_generator)
        self.assertIn('href="../r2/"', run1_shell_updater)
        self.assertIn('href="../index.html"', r2_home)


if __name__ == '__main__':
    unittest.main()
