import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from reader_sections import BOOKS, render_book_sections


class ReaderSectionsTests(unittest.TestCase):
    def test_book_and_act_map(self):
        self.assertEqual(len(BOOKS), 3)
        book_one, book_two, book_three = BOOKS
        self.assertEqual((book_one.start, book_one.end), (1, 82))
        self.assertEqual((book_two.start, book_two.end), (83, 180))
        self.assertEqual((book_three.start, book_three.end), (181, None))
        self.assertEqual(book_three.slug, 'book-iii')
        self.assertEqual(book_one.card_src, 'assets/book-role-cards/book-i-warrior-005.avif')
        self.assertEqual(book_two.card_src, 'assets/book-role-cards/book-ii-stagehand-177.avif')
        self.assertEqual(book_three.card_src, 'assets/book-role-cards/book-iii-magistrate-231.avif')
        self.assertEqual(
            [(act.start, act.end, act.title) for act in book_two.acts],
            [
                (83, 99, 'A LIFE IN CARROW'),
                (100, 137, 'THE STAGE DOOR'),
                (138, 180, 'THE COMPANY ROAD'),
            ],
        )
        self.assertEqual(
            [(act.start, act.end, act.title) for act in book_three.acts],
            [
                (181, 219, 'THE WORKING COMPANY'),
                (220, None, 'THE PRICE OF ATTENTION'),
            ],
        )

    def test_light_renderer_has_shared_book_hierarchy_without_images(self):
        links = {n: f'<a href="{n:03d}.html">Chapter {n}</a>' for n in range(1, 243)}
        rendered = render_book_sections(links, illustrated=False)
        self.assertIn('BOOK I', rendered)
        self.assertIn('Chapters 1–82', rendered)
        self.assertIn('BOOK II', rendered)
        self.assertIn('Chapters 83–180', rendered)
        self.assertIn('BOOK III', rendered)
        self.assertIn('Chapters 181–242', rendered)
        self.assertIn('ACT II · Chapters 220–242', rendered)
        self.assertIn('THE PRICE OF ATTENTION', rendered)
        self.assertNotIn('reader-book-card-image', rendered)
        self.assertNotIn('<img', rendered)

    def test_illustrated_renderer_has_three_clickable_high_res_role_cards(self):
        links = {n: f'<a href="chapters/{n:03d}.html">Chapter {n}</a>' for n in range(1, 243)}
        rendered = render_book_sections(links, illustrated=True, open_first_act=True)
        self.assertEqual(rendered.count('class="reader-book-plate"'), 3)
        self.assertEqual(rendered.count('class="reader-book-card-image"'), 3)
        self.assertIn('src="assets/book-role-cards/book-i-warrior-005.avif"', rendered)
        self.assertIn('src="assets/book-role-cards/book-ii-stagehand-177.avif"', rendered)
        self.assertIn('src="assets/book-role-cards/book-iii-magistrate-231.avif"', rendered)
        self.assertIn('width="500" height="667"', rendered)
        self.assertIn('href="chapters/005.html"', rendered)
        self.assertIn('href="light/177.html"', rendered)
        self.assertIn('href="light/231.html"', rendered)
        self.assertNotIn('reader-book-card-art--', rendered)
        self.assertEqual(rendered.count('<details class="reader-act" open>'), 1)


if __name__ == '__main__':
    unittest.main()
