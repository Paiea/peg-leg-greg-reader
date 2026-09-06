import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from reader_sections import BOOKS, render_book_sections


class BookVStructureTests(unittest.TestCase):
    def test_book_iv_closes_and_book_v_opens_at_441(self):
        self.assertEqual(len(BOOKS), 5)
        book_four = BOOKS[3]
        book_five = BOOKS[4]
        self.assertEqual((book_four.start, book_four.end), (321, 440))
        self.assertEqual(
            [(act.start, act.end, act.title) for act in book_four.acts],
            [
                (321, 330, 'WHAT THINGS COST'),
                (331, 388, 'BEYOND THE DOOR'),
                (389, 440, 'THE FARTHER ROAD'),
            ],
        )
        self.assertEqual((book_five.start, book_five.end), (441, None))
        self.assertEqual(
            [(act.start, act.end, act.title) for act in book_five.acts],
            [(441, None, 'THE LONGER REACH')],
        )

    def test_book_v_uses_investor_role_card(self):
        book_five = BOOKS[4]
        self.assertEqual(book_five.card_src, 'assets/book-role-cards/book-v-investor-446.webp')
        self.assertEqual(book_five.card_href, 'chapters/446.html')
        self.assertIn('Investor', book_five.card_alt)
        asset = Path(__file__).parents[1] / book_five.card_src
        self.assertTrue(asset.is_file(), f'missing Book V role card: {book_five.card_src}')

    def test_renderer_marks_book_v_as_current(self):
        links = {n: f'<a href="chapters/{n:03d}.html">Chapter {n}</a>' for n in range(1, 477)}
        rendered = render_book_sections(links, illustrated=True)
        self.assertIn('BOOK V', rendered)
        self.assertIn('Chapters 441–476', rendered)
        self.assertIn('ACT I · Chapters 441–476', rendered)
        self.assertIn('THE LONGER REACH', rendered)
        self.assertIn('book-v-investor-446.webp', rendered)
        self.assertIn('id="book-v-heading" aria-current="true"', rendered)
        self.assertNotIn('Chapters 321–476', rendered)


if __name__ == '__main__':
    unittest.main()
