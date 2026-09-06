import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from build_notebooklm_export import build_readable_chunks, validate_readable_chunks


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


if __name__ == '__main__':
    unittest.main()
