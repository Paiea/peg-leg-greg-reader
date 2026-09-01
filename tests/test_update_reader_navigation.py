import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'update_reader_navigation.py'

HOME = '''<!doctype html><html><body><div aria-label="Start or explore the book" class="home-actions"><a class="start primary-action" href="chapters/001.html">Begin Reading</a><a class="secondary-action" href="#chapters">Chapter List</a><a class="tertiary-action" href="art.html">Illustrations</a></div></body></html>'''


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


if __name__ == '__main__':
    unittest.main()
