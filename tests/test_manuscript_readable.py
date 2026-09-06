import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from build_notebooklm_export import (
    build_readable_chunks,
    html_chapter_to_readable,
    join_exact_ranges,
    validate_readable_chunks,
)


class ManuscriptReadableTests(unittest.TestCase):
    def test_chunks_are_exact_ordered_ten_chapter_windows(self):
        chapters = {
            number: f"CHAPTER {number}\nTITLE {number}\n\nBody {number}.\n"
            for number in range(1, 13)
        }
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            paths = build_readable_chunks(chapters, out, chunk_size=10)
            self.assertEqual([path.name for path in paths], ['001-010.md', '011-012.md'])
            first = paths[0].read_text(encoding='utf-8')
            self.assertIn('DERIVED EDITORIAL READ SURFACE', first)
            self.assertIn('DO NOT EDIT', first)
            self.assertLess(first.index('CHAPTER 1\n'), first.index('CHAPTER 10\n'))
            self.assertIn('CHAPTER 10\nTITLE 10\n\nBody 10.\n', first)

    def test_validation_rejects_missing_duplicate_or_reordered_chapters(self):
        chapters = {number: f"CHAPTER {number}\nTITLE {number}\n\nBody {number}.\n" for number in range(1, 4)}
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            build_readable_chunks(chapters, out, chunk_size=2)
            validate_readable_chunks(out, expected_numbers=[1, 2, 3])
            second = out / '003-003.md'
            second.write_text(second.read_text(encoding='utf-8') + '\nCHAPTER 2\nTITLE 2\n\nBody 2.\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'coverage/order mismatch'):
                validate_readable_chunks(out, expected_numbers=[1, 2, 3])

    def test_html_extraction_uses_canonical_id_not_showcase_shell_number(self):
        html = '''<!doctype html><html><body>
        <header class="chapter-title"><div class="number">CHAPTER 73</div><h1>THE BEGINNER</h1></header>
        <article class="prose"><p>First line.</p><figure><img alt="art words" src="x.png"/></figure><p>Second line.<br/>Third line.</p></article>
        </body></html>'''
        readable = html_chapter_to_readable(html, canonical_number=91)
        self.assertTrue(readable.startswith('CHAPTER 91\nTHE BEGINNER\n\n'))
        self.assertIn('First line.\n\nSecond line.\nThird line.\n', readable)
        self.assertNotIn('CHAPTER 73', readable)
        self.assertNotIn('art words', readable)

    def test_exact_ranges_join_without_cross_file_boundary_lookup(self):
        recovered = 'CHAPTER 156\nA\n\nOne.\n\nCHAPTER 157\nB\n\nTwo.\n'
        running = 'CHAPTER 158\nC\n\nThree.\n\nCHAPTER 159\nD\n\nFour.\n'
        joined = join_exact_ranges([recovered, running])
        self.assertEqual(list(joined), [156, 157, 158, 159])
        self.assertEqual(joined[157], 'CHAPTER 157\nB\n\nTwo.\n')


if __name__ == '__main__':
    unittest.main()
