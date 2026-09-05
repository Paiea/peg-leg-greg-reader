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
        self.assertEqual(len(BOOKS), 4)
        book_one, book_two, book_three, book_four = BOOKS
        self.assertEqual((book_one.start, book_one.end), (1, 82))
        self.assertEqual((book_two.start, book_two.end), (83, 180))
        self.assertEqual((book_three.start, book_three.end), (181, 320))
        self.assertEqual((book_four.start, book_four.end), (321, None))
        self.assertEqual(book_three.slug, 'book-iii')
        self.assertEqual(book_four.slug, 'book-iv')
        self.assertEqual(
            [(act.start, act.end, act.title) for act in book_three.acts],
            [(181, 219, 'THE WORKING COMPANY'), (220, 280, 'THE PRICE OF ATTENTION'), (281, 320, 'THE WIDER LIFE')],
        )
        self.assertEqual(
            [(act.start, act.end, act.title) for act in book_four.acts],
            [(321, 330, 'WHAT THINGS COST'), (331, None, 'BEYOND THE DOOR')],
        )
        self.assertEqual(
            [book.card_href for book in BOOKS],
            ['chapters/005.html', 'chapters/177.html', 'chapters/231.html', 'chapters/331.html'],
        )

    def test_all_four_published_role_card_paths_resolve(self):
        root = Path(__file__).parents[1]
        expected = {
            'assets/book-role-cards/book-i-warrior-005.webp',
            'assets/book-role-cards/book-ii-stagehand-177.webp',
            'assets/book-role-cards/book-iii-magistrate-231.webp',
            'assets/book-role-cards/book-iv-surveyor-331.webp',
        }
        self.assertEqual({book.card_src for book in BOOKS}, expected)
        for book in BOOKS:
            path = root / book.card_src
            self.assertTrue(path.is_file(), f'missing role-card asset: {book.card_src}')
            self.assertGreater(path.stat().st_size, 50_000, f'role-card asset is suspiciously small: {book.card_src}')
            self.assertEqual(webp_size(path), (720, 960))

    def test_role_card_links_stay_inside_their_books(self):
        for book in BOOKS:
            self.assertTrue(book.card_href.startswith('chapters/'))
            self.assertTrue(book.card_href.endswith('.html'))
            chapter = int(Path(book.card_href).stem)
            self.assertGreaterEqual(chapter, book.start)
            if book.end is not None:
                self.assertLessEqual(chapter, book.end)

    def test_book_four_role_card_wiring_is_declared(self):
        book_four = BOOKS[3]
        self.assertEqual(book_four.card_src, 'assets/book-role-cards/book-iv-surveyor-331.webp')
        self.assertEqual(book_four.card_href, 'chapters/331.html')
        self.assertIn('Surveyor', book_four.card_alt)

    def test_light_renderer_has_shared_four_book_hierarchy_without_images(self):
        links = {n: f'<a href="{n:03d}.html">Chapter {n}</a>' for n in range(1, 352)}
        rendered = render_book_sections(links, illustrated=False)
        for label in ('BOOK I', 'BOOK II', 'BOOK III', 'BOOK IV'):
            self.assertIn(label, rendered)
        self.assertIn('Chapters 181–320', rendered)
        self.assertIn('ACT III · Chapters 281–320', rendered)
        self.assertIn('THE WIDER LIFE', rendered)
        self.assertIn('Chapters 321–351', rendered)
        self.assertIn('ACT II · Chapters 331–351', rendered)
        self.assertIn('BEYOND THE DOOR', rendered)
        self.assertNotIn('reader-book-card-image', rendered)
        self.assertNotIn('<img', rendered)

    def test_books_are_primary_disclosures_and_latest_book_opens(self):
        links = {n: f'<a href="chapters/{n:03d}.html">Chapter {n}</a>' for n in range(1, 352)}
        rendered = render_book_sections(links, illustrated=False)
        self.assertEqual(rendered.count('class="reader-book"'), 4)
        self.assertEqual(rendered.count('class="reader-book-summary"'), 4)
        self.assertEqual(rendered.count('<details class="reader-book" open>'), 1)
        self.assertEqual(rendered.count('aria-current="true"'), 1)
        self.assertIn('<details class="reader-book" open><summary class="reader-book-summary" id="book-iv-heading" aria-current="true">', rendered)
        self.assertIn('Chapters 321–351', rendered)
        self.assertLess(rendered.rindex('BOOK IV'), rendered.rindex('ACT II'))

    def test_book_four_frontier_opens_last_visible_act(self):
        links_330 = {n: f'<a href="chapters/{n:03d}.html">Chapter {n}</a>' for n in range(1, 331)}
        rendered_330 = render_book_sections(links_330, illustrated=False)
        self.assertIn('ACT I · Chapters 321–330', rendered_330)
        self.assertNotIn('BEYOND THE DOOR', rendered_330)
        self.assertIn('<details class="reader-act" open><summary class="reader-act-summary"><span class="reader-act-kicker">ACT I · Chapters 321–330', rendered_330)

        links_331 = {n: f'<a href="chapters/{n:03d}.html">Chapter {n}</a>' for n in range(1, 332)}
        rendered_331 = render_book_sections(links_331, illustrated=False)
        self.assertIn('ACT II · Chapters 331–331', rendered_331)
        self.assertIn('BEYOND THE DOOR', rendered_331)
        self.assertIn('<details class="reader-act" open><summary class="reader-act-summary"><span class="reader-act-kicker">ACT II · Chapters 331–331', rendered_331)

    def test_illustrated_renderer_uses_all_four_role_cards_and_illustrated_links(self):
        links = {n: f'<a href="chapters/{n:03d}.html">Chapter {n}</a>' for n in range(1, 352)}
        rendered = render_book_sections(links, illustrated=True)
        self.assertEqual(rendered.count('class="reader-book-card-image"'), 4)
        for src in (
            'assets/book-role-cards/book-i-warrior-005.webp',
            'assets/book-role-cards/book-ii-stagehand-177.webp',
            'assets/book-role-cards/book-iii-magistrate-231.webp',
            'assets/book-role-cards/book-iv-surveyor-331.webp',
        ):
            self.assertIn(f'src="{src}"', rendered)
        for href in ('chapters/005.html', 'chapters/177.html', 'chapters/231.html', 'chapters/331.html'):
            self.assertIn(f'href="{href}"', rendered)
        for chapter in ('005', '177', '231', '331'):
            self.assertIn(f'aria-label="Open Chapter {chapter} in the Illustrated Reader"', rendered)
        self.assertIn('Chapters 321–351', rendered)
        self.assertEqual(rendered.count('<details class="reader-book" open>'), 1)


if __name__ == '__main__':
    unittest.main()
