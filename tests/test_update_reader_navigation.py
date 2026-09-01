import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'update_reader_navigation.py'

HOME = '''<!doctype html><html><body><div aria-label="Start or explore the book" class="home-actions"><a class="start primary-action" href="chapters/001.html">Begin Reading</a><a class="secondary-action" href="#chapters">Chapter List</a><a class="tertiary-action" href="art.html">Illustrations</a></div></body></html>'''

ACT_HOME = '''<!doctype html><html><body><div aria-label="Start or explore the book" class="home-actions"><a class="start primary-action" href="chapters/001.html">Begin Reading</a><a class="secondary-action" href="#chapters">Chapter List</a><a class="tertiary-action" href="art.html">Illustrations</a></div><section aria-labelledby="chapters-heading" class="toc" id="chapters"><a href="chapters/001.html"><span class="num">01</span><span class="title">The Boy</span></a><a href="chapters/020.html"><span class="num">20</span><span class="title">The Volunteer</span></a><a href="chapters/021.html"><span class="num">21</span><span class="title">The Tenant</span></a><a href="chapters/063.html"><span class="num">63</span><span class="title">The Backstop</span></a><a href="chapters/064.html"><span class="num">64</span><span class="title">The Patient</span></a><a href="chapters/082.html"><span class="num">82</span><span class="title">The Reconciler</span></a><a href="chapters/083.html"><span class="num">83</span><span class="title">The Suitor</span></a><a href="chapters/137.html"><span class="num">137</span><span class="title">The Shape</span></a><a href="chapters/138.html"><span class="num">138</span><span class="title">The Shopkeeper</span></a><a href="chapters/155.html"><span class="num">155</span><span class="title">The Leak</span></a></section></body></html>'''


class NavigationPatchTests(unittest.TestCase):
    def test_adds_light_home_action_once_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'index.html'
            path.write_text(HOME, encoding='utf-8')
            first = subprocess.run([sys.executable, str(SCRIPT), str(path)], text=True, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            second = subprocess.run([sys.executable, str(SCRIPT), str(path)], text=True, capture_output=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            text = path.read_text(encoding='utf-8')
            self.assertIn('href="light/index.html">Read Light</a>', text)
            self.assertEqual(text.count('href="light/index.html">Read Light</a>'), 1)
            self.assertIn('href="chapters/001.html">Begin Reading</a>', text)
            self.assertIn('href="#chapters">Chapter List</a>', text)

    def test_groups_illustrated_toc_into_story_based_acts(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'index.html'
            path.write_text(ACT_HOME, encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            text = path.read_text(encoding='utf-8')
            for label in (
                'ACT I', 'THE SECOND LIFE', 'Chapters 1–20',
                'ACT II', 'MAKING A PLACE', 'Chapters 21–63',
                'ACT III', 'THE NEW BASELINE', 'Chapters 64–82',
                'ACT IV', 'A LIFE IN CARROW', 'Chapters 83–137',
                'ACT V', 'THE COMPANY ROAD', 'Chapters 138–155',
            ):
                self.assertIn(label, text)
            self.assertEqual(text.count('class="reader-act"'), 5)
            for number in ('001', '020', '021', '063', '064', '082', '083', '137', '138', '155'):
                self.assertEqual(text.count(f'href="chapters/{number}.html"'), 1)
            self.assertLess(text.index('THE SECOND LIFE'), text.index('MAKING A PLACE'))
            self.assertLess(text.index('MAKING A PLACE'), text.index('THE NEW BASELINE'))
            self.assertLess(text.index('THE NEW BASELINE'), text.index('A LIFE IN CARROW'))
            self.assertLess(text.index('A LIFE IN CARROW'), text.index('THE COMPANY ROAD'))

    def test_desktop_chapter_images_preserve_intrinsic_width(self):
        css = (ROOT / 'assets/reader.css').read_text(encoding='utf-8')
        self.assertIn('@media (min-width:601px)', css)
        self.assertIn('.chapter-art img {\n    width:auto;', css)
        self.assertIn('max-width:min(820px, calc(100vw - 48px));', css)
        self.assertIn('.chapter-art.sketch-beat img {\n    max-width:min(560px, calc(100vw - 48px));', css)
        self.assertIn('.chapter-art.feature-illustration img {\n    max-width:min(1180px, calc(100vw - 48px));', css)
        self.assertIn('@media (max-width:600px)', css)
        self.assertIn('width:calc(100vw - 32px);', css)


if __name__ == '__main__':
    unittest.main()
