import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from reader_sections import BOOKS, render_book_sections


def webp_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        raise AssertionError(f'{path} is not a WebP file')

    chunk = data[12:16]
    if chunk == b'VP8 ':
        if data[23:26] != b'\x9d\x01\x2a':
            raise AssertionError(f'{path} has an invalid VP8 frame header')
        width = int.from_bytes(data[26:28], 'little') & 0x3FFF
        height = int.from_bytes(data[28:30], 'little') & 0x3FFF
        return width, height
    if chunk == b'VP8L':
        bits = int.from_bytes(data[21:25], 'little')
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if chunk == b'VP8X':
        width = int.from_bytes(data[24:27], 'little') + 1
        height = int.from_bytes(data[27:30], 'little') + 1
        return width, height
    raise AssertionError(f'{path} has unsupported WebP chunk {chunk!r}')


class ReaderSectionsTests(unittest.TestCase):
    def test_book_and_act_map(self):
        self.assertEqual(len(BOOKS), 3)
        book_one, book_two, book_three = BOOKS
        self.assertEqual((book_one.start, book_one.end), (1, 82))
        self.assertEqual((book_two.start, book_two.end), (83, 180))
        self.assertEqual((book_three.start, book_three.end), (181, None))
        self.assertEqual(book_three.slug, 'book-iii')
        self.assertEqual(book_one.card_src, 'assets/book-role-cards/book-i-warrior-005.webp')
        self.assertEqual(book_two.card_src, 'assets/book-role-cards/book-ii-stagehand-177.webp')
        self.assertEqual(book_three.card_src, 'assets/book-role-cards/book-iii-magistrate-231.webp')
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

    def test_role_card_paths_resolve_to_individual_720_by_960_webps(self):
        root = Path(__file__).parents[1]
        expected = {
            'assets/book-role-cards/book-i-warrior-005.webp',
            'assets/book-role-cards/book-ii-stagehand-177.webp',
            'assets/book-role-cards/book-iii-magistrate-231.webp',
        }
        self.assertEqual({book.card_src for book in BOOKS}, expected)
        for relative_path in expected:
            path = root / relative_path
            self.assertTrue(path.is_file(), f'missing role-card asset: {relative_path}')
            self.assertEqual(webp_size(path), (720, 960))

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
        self.assertIn('src="assets/book-role-cards/book-i-warrior-005.webp"', rendered)
        self.assertIn('src="assets/book-role-cards/book-ii-stagehand-177.webp"', rendered)
        self.assertIn('src="assets/book-role-cards/book-iii-magistrate-231.webp"', rendered)
        self.assertIn('width="720" height="960"', rendered)
        self.assertIn('href="chapters/005.html"', rendered)
        self.assertIn('href="light/177.html"', rendered)
        self.assertIn('href="light/231.html"', rendered)
        self.assertNotIn('reader-book-card-art--', rendered)
        self.assertEqual(rendered.count('<details class="reader-act" open>'), 1)


if __name__ == '__main__':
    unittest.main()
