import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from reader_sections import BOOKS, render_book_sections


class BookIVRoleCardTests(unittest.TestCase):
    def test_book_iv_uses_surveyor_role_card(self):
        book_four = BOOKS[3]
        self.assertEqual(book_four.card_src, 'assets/book-role-cards/book-iv-surveyor-331.webp')
        self.assertEqual(book_four.card_href, 'chapters/331.html')
        self.assertIn('Surveyor', book_four.card_alt)

    def test_illustrated_contents_renders_all_four_role_cards(self):
        links = {n: f'<a href="chapters/{n:03d}.html">Chapter {n}</a>' for n in range(1, 345)}
        rendered = render_book_sections(links, illustrated=True)
        self.assertEqual(rendered.count('class="reader-book-card-image"'), 4)
        self.assertIn('src="assets/book-role-cards/book-iv-surveyor-331.webp"', rendered)
        self.assertIn('href="chapters/331.html"', rendered)


if __name__ == '__main__':
    unittest.main()
