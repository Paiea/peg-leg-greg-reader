import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from reader_sections import render_book_sections


class ReaderSectionShowcaseTests(unittest.TestCase):
    def test_showcase_ranges_use_display_numbers_not_canonical_gaps(self):
        links = {
            1: '<a>one</a>',
            2: '<a>two</a>',
            4: '<a>four</a>',
        }
        rendered = render_book_sections(
            links,
            illustrated=False,
            display_numbers={1: 1, 2: 2, 4: 3},
        )
        self.assertIn('Chapters 1–3', rendered)
        self.assertNotIn('Chapters 1–4', rendered)


if __name__ == '__main__':
    unittest.main()
