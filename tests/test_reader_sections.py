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
        width = int.from_bytes(data[26:28], 'little') & 0x3FFF
        height = int.from_bytes(data[28:30], 'little') & 0x3FFF
        return width, height
    if chunk == b'VP8L':
        bits = int.from_bytes(data[21:25], 'little')
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if chunk == b'VP8X':
        return int.from_bytes(data[24:27], 'little') + 1, int.from_bytes(data[27:30], 'little') + 1
    raise AssertionError(f'{path} has unsupported WebP chunk {chunk!r}')


class ReaderSectionsTests(unittest.TestCase):
    def test_book_and_act_map(self):
        self.assertEqual([(b.start, b.end) for b in BOOKS], [(1, 82), (83, 180), (181, 320), (321, None)])
        self.assertEqual([(a.start, a.end, a.title) for a in BOOKS[2].acts], [(181, 219, 'THE WORKING COMPANY'), (220, 280, 'THE PRICE OF ATTENTION'), (281, 320, 'THE WIDER LIFE')])
        self.assertEqual([(a.start, a.end, a.title) for a in BOOKS[3].acts], [(321, 330, 'WHAT THINGS COST'), (331, None, 'BEYOND THE DOOR')])

    def test_published_role_card_paths_resolve(self):
        root = Path(__file__).parents[1]
        for book in BOOKS:
            self.assertTrue((root / book.card_src).is_file(), f'missing role-card asset: {book.card_src}')
            self.assertEqual(webp_size(root / book.card_src), (720, 960))

    def test_text_renderer_has_shared_hierarchy_without_images(self):
        links = {n: f'<a href="{n:03d}.html">Chapter {n}</a>' for n in range(1, 348)}
        rendered = render_book_sections(links, illustrated=False)
        for label in ('BOOK I', 'BOOK II', 'BOOK III', 'BOOK IV'):
            self.assertIn(label, rendered)
        self.assertIn('Chapters 321–347', rendered)
        self.assertIn('ACT II · Chapters 331–347', rendered)
        self.assertNotIn('reader-book-card-image', rendered)
        self.assertNotIn('<img', rendered)

    def test_books_are_primary_disclosures_and_default_is_compressed(self):
        links = {n: f'<a href="chapters/{n:03d}.html">Chapter {n}</a>' for n in range(1, 348)}
        rendered = render_book_sections(links, illustrated=False)
        self.assertEqual(rendered.count('class="reader-book"'), 4)
        self.assertEqual(rendered.count('class="reader-book-summary"'), 4)
        self.assertNotIn('<details class="reader-book" open>', rendered)
        self.assertNotIn('<details class="reader-act" open>', rendered)

    def test_latest_book_can_be_explicitly_opened(self):
        links = {n: f'<a href="chapters/{n:03d}.html">Chapter {n}</a>' for n in range(1, 348)}
        rendered = render_book_sections(links, illustrated=False, open_latest_book=True)
        self.assertEqual(rendered.count('<details class="reader-book" open>'), 1)
        self.assertEqual(rendered.count('<details class="reader-act" open>'), 1)

    def test_illustrated_renderer_uses_all_four_role_cards(self):
        links = {n: f'<a href="chapters/{n:03d}.html">Chapter {n}</a>' for n in range(1, 348)}
        rendered = render_book_sections(links, illustrated=True)
        self.assertEqual(rendered.count('class="reader-book-card-image"'), 4)
        for book in BOOKS:
            self.assertIn(f'src="{book.card_src}"', rendered)
        self.assertNotIn('<details class="reader-book" open>', rendered)


if __name__ == '__main__':
    unittest.main()
