import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / 'scripts' / 'generate_light.py'

BOOK1_ACTS = (
    ('ACT I', 'THE SECOND LIFE', 'Chapters 1–20', 1, 20),
    ('ACT II', 'MAKING A PLACE', 'Chapters 21–63', 21, 63),
    ('ACT III', 'THE NEW BASELINE', 'Chapters 64–82', 64, 82),
)
BOOK2_ACTS = (
    ('ACT I', 'A LIFE IN CARROW', 'Chapters 83–111', 83, 111),
    ('ACT II', 'THE STAGE DOOR', 'Chapters 112–137', 112, 137),
    ('ACT III', 'THE COMPANY ROAD', 'Chapters 138–180', 138, 180),
    ('ACT IV', 'THE WORKING COMPANY', 'Chapters 181–217', 181, 217),
    ('ACT V', 'THE PRICE OF ATTENTION', 'Chapters 218–220', 218, 220),
)

PUBLISHED = '<!doctype html><html><body><h1>THE SAMPLE</h1><article class="prose"><p>Published prose.</p></article></body></html>'


def recovered_fixture() -> str:
    chunks = []
    for number in (156, 180, 181, 217, 218, 219):
        chunks.append(f'# CHAPTER {number}\n\n## THE RECOVERED {number}\n\nRecovered prose {number}.\n')
    return '\n'.join(chunks)


class ReaderActTests(unittest.TestCase):
    def test_light_toc_uses_same_book_and_story_act_structure(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'state/manuscript').mkdir(parents=True)
            (root / 'chapters').mkdir()
            (root / 'state/manuscript/Peg_Leg_Greg_Running_Manuscript.md').write_text(
                '# CHAPTER 220\n\n## THE CURRENT\n\nCurrent prose.\n', encoding='utf-8'
            )
            (root / 'state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md').write_text(
                recovered_fixture(), encoding='utf-8'
            )
            for _, _, _, start, end in BOOK1_ACTS + BOOK2_ACTS:
                for number in (start, end):
                    if number <= 155:
                        (root / f'chapters/{number:03d}.html').write_text(PUBLISHED, encoding='utf-8')

            result = subprocess.run(
                [sys.executable, str(GENERATOR), 'current'], cwd=root, text=True, capture_output=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (root / 'light/index.html').read_text(encoding='utf-8')

            self.assertIn('BOOK I', text)
            self.assertIn('BOOK II', text)
            self.assertIn('Chapters 1–82', text)
            self.assertIn('Chapters 83–220', text)
            for numeral, title, chapter_range, start, end in BOOK1_ACTS + BOOK2_ACTS:
                self.assertIn(numeral, text)
                self.assertIn(title, text)
                self.assertIn(chapter_range, text)
                if start <= 155:
                    self.assertIn(f'chapter={start}', text)
                if end <= 155:
                    self.assertIn(f'chapter={end}', text)
            self.assertEqual(text.count('class="reader-book"'), 2)
            self.assertEqual(text.count('class="reader-act"'), 8)
            self.assertNotIn('Book01_Plate.jpg', text)
            self.assertNotIn('Book02_Plate.jpg', text)


if __name__ == '__main__':
    unittest.main()
