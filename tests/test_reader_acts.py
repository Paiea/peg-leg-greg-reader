import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / 'scripts' / 'generate_light.py'

BOOK_ACTS = (
    ('BOOK I', 'ACT I', 'THE SECOND LIFE', 'Chapters 1–20', 1, 20),
    ('BOOK I', 'ACT II', 'MAKING A PLACE', 'Chapters 21–63', 21, 63),
    ('BOOK I', 'ACT III', 'THE NEW BASELINE', 'Chapters 64–82', 64, 82),
    ('BOOK II', 'ACT I', 'A LIFE IN CARROW', 'Chapters 83–99', 83, 99),
    ('BOOK II', 'ACT II', 'THE STAGE DOOR', 'Chapters 100–137', 100, 137),
    ('BOOK II', 'ACT III', 'THE COMPANY ROAD', 'Chapters 138–180', 138, 180),
    ('BOOK III', 'ACT I', 'THE WORKING COMPANY', 'Chapters 181–219', 181, 219),
    ('BOOK III', 'ACT II', 'THE PRICE OF ATTENTION', 'Chapters 220–242', 220, 242),
)

PUBLISHED = '<!doctype html><html><body><h1>THE SAMPLE</h1><article class="prose"><p>Published prose.</p></article></body></html>'


def markdown_chapter(number: int) -> str:
    return f'# CHAPTER {number}\n\n## THE CHAPTER {number}\n\nProse {number}.\n'


class ReaderActTests(unittest.TestCase):
    def test_light_toc_uses_shared_book_and_act_hierarchy(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'state/manuscript').mkdir(parents=True)
            (root / 'chapters').mkdir()
            (root / 'state/manuscript/Peg_Leg_Greg_Running_Manuscript.md').write_text(
                markdown_chapter(220) + '\n' + markdown_chapter(242), encoding='utf-8'
            )
            (root / 'state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md').write_text(
                '\n'.join(markdown_chapter(n) for n in (156, 180, 181, 219)), encoding='utf-8'
            )
            for number in (1, 20, 21, 63, 64, 82, 83, 99, 100, 137, 138, 155):
                (root / f'chapters/{number:03d}.html').write_text(PUBLISHED, encoding='utf-8')

            result = subprocess.run(
                [sys.executable, str(GENERATOR), 'current'], cwd=root, text=True, capture_output=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (root / 'light/index.html').read_text(encoding='utf-8')

            self.assertEqual(text.count('class="reader-book"'), 3)
            self.assertEqual(text.count('class="reader-act"'), 8)
            self.assertEqual(text.count('<img'), 0)
            self.assertIn('BOOK I', text)
            self.assertIn('BOOK II', text)
            self.assertIn('BOOK III', text)
            self.assertIn('Chapters 1–82', text)
            self.assertIn('Chapters 83–180', text)
            self.assertIn('Chapters 181–242', text)
            for _, numeral, title, chapter_range, _, _ in BOOK_ACTS:
                self.assertIn(numeral, text)
                self.assertIn(title, text)
                self.assertIn(chapter_range, text)

            self.assertLess(text.index('THE SECOND LIFE'), text.index('MAKING A PLACE'))
            self.assertLess(text.index('THE NEW BASELINE'), text.index('A LIFE IN CARROW'))
            self.assertLess(text.index('THE STAGE DOOR'), text.index('THE COMPANY ROAD'))
            self.assertLess(text.index('THE COMPANY ROAD'), text.index('THE WORKING COMPANY'))
            self.assertLess(text.index('THE WORKING COMPANY'), text.index('THE PRICE OF ATTENTION'))
            self.assertIn('href="220.html"', text)
            self.assertIn('href="242.html"', text)
            self.assertIn('../assets/book-contents.css', text)


if __name__ == '__main__':
    unittest.main()
