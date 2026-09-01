import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / 'scripts' / 'generate_light.py'

ACTS = (
    ('ACT I', 'THE SECOND LIFE', 'Chapters 1–20', 1, 20),
    ('ACT II', 'MAKING A PLACE', 'Chapters 21–63', 21, 63),
    ('ACT III', 'THE NEW BASELINE', 'Chapters 64–82', 64, 82),
    ('ACT IV', 'A LIFE IN CARROW', 'Chapters 83–137', 83, 137),
    ('ACT V', 'THE COMPANY ROAD', 'Chapters 138–155', 138, 155),
)

PUBLISHED = '<!doctype html><html><body><h1>THE SAMPLE</h1><article class="prose"><p>Published prose.</p></article></body></html>'


class ReaderActTests(unittest.TestCase):
    def test_light_toc_uses_same_story_based_acts_as_illustrated(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'state/manuscript').mkdir(parents=True)
            (root / 'chapters').mkdir()
            (root / 'state/manuscript/Peg_Leg_Greg_Running_Manuscript.md').write_text(
                '# CHAPTER 220\n\n## THE CURRENT\n\nCurrent prose.\n', encoding='utf-8'
            )
            (root / 'state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md').write_text(
                '# CHAPTER 156\n\n## THE RECOVERED\n\nRecovered prose.\n', encoding='utf-8'
            )
            for _, _, _, start, end in ACTS:
                for number in (start, end):
                    (root / f'chapters/{number:03d}.html').write_text(PUBLISHED, encoding='utf-8')

            result = subprocess.run(
                [sys.executable, str(GENERATOR), 'current'], cwd=root, text=True, capture_output=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (root / 'light/index.html').read_text(encoding='utf-8')

            self.assertLess(text.index('Current'), text.index('ACT I'))
            self.assertLess(text.index('Chapters 156–219'), text.index('ACT I'))
            for numeral, title, chapter_range, start, end in ACTS:
                self.assertIn(numeral, text)
                self.assertIn(title, text)
                self.assertIn(chapter_range, text)
                self.assertIn(f'chapter={start}', text)
                self.assertIn(f'chapter={end}', text)
            self.assertEqual(text.count('class="reader-act"'), 5)


if __name__ == '__main__':
    unittest.main()
