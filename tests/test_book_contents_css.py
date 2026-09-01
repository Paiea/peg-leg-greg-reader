import unittest
from pathlib import Path


class BookContentsCssTests(unittest.TestCase):
    def test_book_plate_is_small_on_desktop_and_sits_beside_heading_on_mobile(self):
        css = (Path(__file__).parents[1] / 'assets' / 'book-contents.css').read_text(encoding='utf-8')
        self.assertIn('grid-template-columns: minmax(180px, 220px) minmax(0, 1fr)', css)
        self.assertIn('max-width: 210px', css)
        self.assertIn('.reader-book-meta', css)
        self.assertIn('grid-template-columns: minmax(0, 1fr) auto', css)
        self.assertIn('width: 88px', css)
        self.assertIn('.reader-book-layout--illustrated .reader-book-meta', css)
        self.assertIn('display: contents', css)
        self.assertNotIn('animation:', css)


if __name__ == '__main__':
    unittest.main()
