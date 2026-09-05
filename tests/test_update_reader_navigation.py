import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'update_reader_navigation.py'
HOME = '<!doctype html><html><body><div class="home-actions"><a class="start primary-action" href="chapters/001.html">Begin Reading</a><a class="secondary-action" href="#chapters">Chapters</a><a class="tertiary-action" href="art.html">Illustrations</a></div></body></html>'


class NavigationPatchTests(unittest.TestCase):
    def test_normalizes_home_actions_once_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'index.html'
            path.write_text(HOME, encoding='utf-8')
            for _ in range(2):
                result = subprocess.run([sys.executable, str(SCRIPT), str(path)], text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            text = path.read_text(encoding='utf-8')
            self.assertEqual(text.count('>Begin Reading</a>'), 1)
            self.assertEqual(text.count('>Text Reader</a>'), 1)
            self.assertEqual(text.count('>Illustrated Reader</a>'), 1)
            self.assertEqual(text.count('>Illustrations</a>'), 1)
            self.assertIn('href="#books">Illustrated Reader</a>', text)
            self.assertNotIn('href="#chapters">Chapters</a>', text)

    def test_collapses_historical_reader_labels(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'index.html'
            path.write_text(HOME.replace('</div>', '<a class="secondary-action" href="light/index.html">Read Light</a><a class="secondary-action" href="light/index.html">Text Reader</a></div>'), encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            text = path.read_text(encoding='utf-8')
            self.assertEqual(text.count('href="light/index.html">Text Reader</a>'), 1)
            self.assertNotIn('>Read Light</a>', text)

    def test_desktop_chapter_images_preserve_intrinsic_width(self):
        css = (ROOT / 'assets/reader.css').read_text(encoding='utf-8')
        self.assertIn('@media (min-width:601px)', css)
        self.assertIn('.chapter-art img {\n    width:auto;', css)
        self.assertIn('@media (max-width:600px)', css)
        self.assertIn('width:calc(100vw - 32px);', css)


if __name__ == '__main__':
    unittest.main()
