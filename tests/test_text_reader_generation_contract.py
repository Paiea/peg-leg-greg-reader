import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'generate_light.py'

RUNNING = '''# PEG-LEG GREG — RUNNING MANUSCRIPT\n\n# CHAPTER 220\n\n## THE LANDLORD\n\nFirst paragraph.\n\n# CHAPTER 221\n\n## THE PARTICIPANT\n\nSecond paragraph.\n'''


def generate(root: Path) -> None:
    (root / 'state/manuscript').mkdir(parents=True)
    (root / 'chapters').mkdir()
    (root / 'state/manuscript/Peg_Leg_Greg_Running_Manuscript.md').write_text(RUNNING, encoding='utf-8')
    (root / 'state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md').write_text('', encoding='utf-8')
    result = subprocess.run(
        [sys.executable, str(SCRIPT), 'current'],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)


class TextReaderGenerationContractTests(unittest.TestCase):
    def with_generated_repo(self) -> Path:
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        generate(root)
        return root

    def test_text_chapter_illustrated_nav_targets_books_anchor(self):
        root = self.with_generated_repo()
        page = (root / 'light/220.html').read_text(encoding='utf-8')
        self.assertIn('../index.html#books', page)
        self.assertNotIn('../index.html#chapters', page)

    def test_text_index_illustrated_links_target_books_anchor(self):
        root = self.with_generated_repo()
        index = (root / 'light/index.html').read_text(encoding='utf-8')
        self.assertGreaterEqual(index.count('../index.html#books'), 2)
        self.assertNotIn('../index.html#chapters', index)

    def test_latest_page_illustrated_nav_targets_books_anchor(self):
        root = self.with_generated_repo()
        latest = (root / 'latest.html').read_text(encoding='utf-8')
        self.assertIn('index.html#books', latest)
        self.assertNotIn('index.html#chapters', latest)

    def test_text_chapter_is_generated_with_current_public_labels(self):
        root = self.with_generated_repo()
        page = (root / 'light/220.html').read_text(encoding='utf-8')
        self.assertIn('TEXT READER · CHAPTER 220', page)
        self.assertIn('Text-only reading · no chapter illustrations', page)
        self.assertIn('>TEXT READER</a>', page)
        self.assertNotIn('LIGHT EDITION', page)
        self.assertNotIn('>LIGHT</a>', page)

    def test_text_index_and_latest_use_current_public_labels(self):
        root = self.with_generated_repo()
        index = (root / 'light/index.html').read_text(encoding='utf-8')
        latest = (root / 'latest.html').read_text(encoding='utf-8')
        self.assertIn('<h1>Text Reader</h1>', index)
        self.assertIn('TEXT READER', index)
        self.assertIn('TEXT READER', latest)
        self.assertNotIn('Light Edition', index)
        self.assertNotIn('>LIGHT</a>', index)
        self.assertNotIn('>LIGHT</a>', latest)


if __name__ == '__main__':
    unittest.main()
